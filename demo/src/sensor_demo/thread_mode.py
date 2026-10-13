"""
thread_mode.py - Chế độ Đa luồng (ThreadPoolExecutor).
Phục vụ mục tiêu:
1. Bao bọc các thao tác I/O blocking trong pool các worker threads.
2. Quản lý vòng đời Future (pending, running, done, cancelled).
3. Thu kết quả ngay khi hoàn thành bằng concurrent.futures.as_completed.
"""

from __future__ import annotations
import time
import platform
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
from datetime import datetime, timezone
from .models import StationConfig, StationResult, RunReport
from .simulator import blocking_fetch_station


def run_thread_pool(
    stations: List[StationConfig],
    max_workers: int = 4,
    seed: int = 42,
    timeout_ms: Optional[int] = None
) -> RunReport:
    """
    Thực thi thu thập dữ liệu bằng ThreadPoolExecutor.
    Các worker threads chạy song song, cho phép chồng lấn thời gian chờ I/O blocking.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    t_start = time.perf_counter()

    results: List[StationResult] = []

    # Dùng context manager để đảm bảo executor.shutdown(wait=True)
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="SensorWorker") as executor:
        # Submit toàn bộ tác vụ, ánh xạ Future -> StationConfig
        future_to_station = {
            executor.submit(blocking_fetch_station, cfg, seed, 1, timeout_ms): cfg
            for cfg in stations
        }

        # Thu hoạch kết quả theo completion order bằng as_completed
        for future in as_completed(future_to_station):
            station_cfg = future_to_station[future]
            try:
                res = future.result()
                results.append(res)
            except Exception as exc:
                results.append(StationResult(
                    station_id=station_cfg.station_id,
                    status="failed",
                    error_type=type(exc).__name__,
                    error_message=str(exc)
                ))

    total_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

    success_cnt = sum(1 for r in results if r.status == "success")
    timeout_cnt = sum(1 for r in results if r.status == "timeout")
    fail_cnt = sum(1 for r in results if r.status in ("failed", "invalid"))
    cancel_cnt = sum(1 for r in results if r.status == "cancelled")

    throughput = (len(stations) / (total_elapsed_ms / 1000.0)) if total_elapsed_ms > 0 else 0.0
    digest = RunReport.compute_digest(results)

    return RunReport(
        run_id=f"thread_{int(time.time()*1000)}",
        mode="thread",
        python_version=sys.version.split()[0],
        platform=platform.platform(),
        parameters={
            "num_stations": len(stations),
            "max_workers": max_workers,
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
        max_in_flight=min(max_workers, len(stations)),
        throughput_items_per_second=round(throughput, 2),
        result_digest=digest,
        station_results=results
    )
