"""
hybrid_mode.py - Chế độ Lai (Hybrid: Asyncio I/O + ProcessPoolExecutor CPU).
Phục vụ mục tiêu:
1. Kiến trúc tối ưu cho workload hỗn hợp (Mixed I/O & CPU-bound).
2. Dùng Asyncio thu thập đồng thời hàng loạt trạm I/O trễ thấp trên Single-Thread Event Loop.
3. Dùng ProcessPoolExecutor để chia sẻ bước phân tích Anomaly CPU nặng cho các lõi CPU vật lý.
4. Điều tiết tải qua Bounded Queue (Backpressure).
"""

from __future__ import annotations
import time
import asyncio
import platform
import sys
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional, Tuple
from datetime import datetime, timezone
from .models import StationConfig, StationResult, RunReport, SensorRecord
from .simulator import async_fetch_station, cpu_intensive_anomaly_detection


def _cpu_worker_task(args: Tuple[SensorRecord, int]) -> Tuple[float, bool]:
    """Top-level worker function pickleable cho ProcessPool."""
    rec, cpu_size = args
    return cpu_intensive_anomaly_detection(rec, cpu_size)


async def _producer_task(
    cfg: StationConfig,
    sem: asyncio.Semaphore,
    queue: asyncio.Queue,
    seed: int,
    timeout_ms: Optional[int]
):
    """Producer: Chờ I/O qua Async adapter rồi đưa kết quả vào Queue (chịu Backpressure)."""
    async with sem:
        res = await async_fetch_station(cfg, seed, attempt=1, timeout_ms=timeout_ms)
        # Đưa vào queue (nếu queue đầy sẽ tạm dừng tại put để tạo backpressure)
        await queue.put(res)


async def _run_hybrid_pipeline(
    stations: List[StationConfig],
    concurrency_limit: int = 4,
    cpu_workers: int = 2,
    queue_maxsize: int = 5,
    seed: int = 42,
    timeout_ms: Optional[int] = None
) -> List[StationResult]:
    """Pipeline kết hợp Asyncio I/O và ProcessPoolExecutor."""
    sem = asyncio.Semaphore(concurrency_limit)
    queue: asyncio.Queue = asyncio.Queue(maxsize=queue_maxsize)
    loop = asyncio.get_running_loop()

    # Khởi tạo producers
    producers = [
        asyncio.create_task(_producer_task(cfg, sem, queue, seed, timeout_ms))
        for cfg in stations
    ]

    results: List[StationResult] = []
    
    with ProcessPoolExecutor(max_workers=cpu_workers) as process_pool:
        # Consumer: Lấy từng item từ queue và đẩy CPU task sang ProcessPool
        pending_cpu_tasks = []

        for _ in range(len(stations)):
            res: StationResult = await queue.get()
            if res.status == "success" and res.record is not None:
                cfg = next(c for c in stations if c.station_id == res.station_id)
                # Bọc call ProcessPool qua run_in_executor để trả về asyncio Future
                fut = loop.run_in_executor(
                    process_pool,
                    _cpu_worker_task,
                    (res.record, cfg.cpu_size)
                )
                pending_cpu_tasks.append((res, fut))
            else:
                results.append(res)
            queue.task_done()

        # Đợi các CPU task hoàn tất
        for res, fut in pending_cpu_tasks:
            score, is_ano = await fut
            res.anomaly_score = score
            res.is_anomaly = is_ano
            results.append(res)

    await asyncio.gather(*producers)
    return results


def run_hybrid(
    stations: List[StationConfig],
    concurrency_limit: int = 4,
    cpu_workers: int = 2,
    queue_maxsize: int = 5,
    seed: int = 42,
    timeout_ms: Optional[int] = None
) -> RunReport:
    """Entrypoint đồng bộ cho chế độ Lai (Hybrid)."""
    started_at = datetime.now(timezone.utc).isoformat()
    t_start = time.perf_counter()

    results = asyncio.run(_run_hybrid_pipeline(
        stations=stations,
        concurrency_limit=concurrency_limit,
        cpu_workers=cpu_workers,
        queue_maxsize=queue_maxsize,
        seed=seed,
        timeout_ms=timeout_ms
    ))

    total_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

    success_cnt = sum(1 for r in results if r.status == "success")
    timeout_cnt = sum(1 for r in results if r.status == "timeout")
    fail_cnt = sum(1 for r in results if r.status in ("failed", "invalid"))
    cancel_cnt = sum(1 for r in results if r.status == "cancelled")

    throughput = (len(stations) / (total_elapsed_ms / 1000.0)) if total_elapsed_ms > 0 else 0.0
    digest = RunReport.compute_digest(results)

    return RunReport(
        run_id=f"hybrid_{int(time.time()*1000)}",
        mode="hybrid",
        python_version=sys.version.split()[0],
        platform=platform.platform(),
        parameters={
            "num_stations": len(stations),
            "concurrency_limit": concurrency_limit,
            "cpu_workers": cpu_workers,
            "queue_maxsize": queue_maxsize,
            "timeout_ms": timeout_ms,
            "seed": seed
        },
        seed=seed,
        started_at=started_at,
        elapsed_ms=round(total_elapsed_ms, 2),
        success_count=success_cnt,
        timeout_count=timeout_cnt,
        failure_count=fail_cnt,
        cancelled_count=cancel_cnt,
        max_in_flight=min(concurrency_limit, len(stations)),
        throughput_items_per_second=round(throughput, 2),
        result_digest=digest,
        station_results=results
    )
