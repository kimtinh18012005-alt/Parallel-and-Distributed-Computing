"""
async_mode.py - Chế độ Bất đồng bộ (Asyncio Event Loop & Coroutines).
Phục vụ mục tiêu:
1. Minh họa mô hình đơn luồng điều phối nhiều tác vụ (Single-thread cooperative multitasking).
2. Dùng Semaphore để giới hạn concurrency (bounded concurrency).
3. Gom và xử lý các Coroutine/Task trên Event Loop.
"""

from __future__ import annotations
import time
import asyncio
import platform
import sys
from typing import List, Optional
from datetime import datetime, timezone
from .models import StationConfig, StationResult, RunReport
from .simulator import async_fetch_station


async def _fetch_with_semaphore(
    sem: asyncio.Semaphore,
    cfg: StationConfig,
    seed: int,
    timeout_ms: Optional[int]
) -> StationResult:
    """Bọc lời gọi async_fetch_station qua Semaphore để giới hạn concurrency."""
    async with sem:
        return await async_fetch_station(cfg, seed, attempt=1, timeout_ms=timeout_ms)


async def _run_async_pipeline(
    stations: List[StationConfig],
    concurrency_limit: int = 4,
    seed: int = 42,
    timeout_ms: Optional[int] = None
) -> List[StationResult]:
    """Pipeline Asyncio điều phối bằng TaskGroup hoặc gather."""
    sem = asyncio.Semaphore(concurrency_limit)
    
    # Tạo danh sách các coroutine được bảo vệ bởi Semaphore
    tasks = [
        asyncio.create_task(_fetch_with_semaphore(sem, cfg, seed, timeout_ms))
        for cfg in stations
    ]

    # Chờ tất cả task hoàn tất bằng gather
    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results


def run_async(
    stations: List[StationConfig],
    concurrency_limit: int = 4,
    seed: int = 42,
    timeout_ms: Optional[int] = None
) -> RunReport:
    """
    Entrypoint đồng bộ chạy Event Loop thông qua asyncio.run().
    """
    started_at = datetime.now(timezone.utc).isoformat()
    t_start = time.perf_counter()

    # Khởi chạy Event Loop cô lập
    results = asyncio.run(_run_async_pipeline(
        stations=stations,
        concurrency_limit=concurrency_limit,
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
        run_id=f"async_{int(time.time()*1000)}",
        mode="async",
        python_version=sys.version.split()[0],
        platform=platform.platform(),
        parameters={
            "num_stations": len(stations),
            "concurrency_limit": concurrency_limit,
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
