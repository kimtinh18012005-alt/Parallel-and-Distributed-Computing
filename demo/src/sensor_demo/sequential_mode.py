"""
sequential_mode.py - Chế độ tuần tự (Sequential Baseline & Oracle).
Phục vụ mục tiêu:
1. Đo mốc thời gian tuần tự (toàn bộ thời gian chờ I/O nối đuôi nhau).
2. Đóng vai trò Oracle tính đúng (Baseline) để các chế độ khác đối chiếu digest.
"""

from __future__ import annotations
import time
import platform
import sys
from typing import List, Optional
from datetime import datetime, timezone
from .models import StationConfig, StationResult, RunReport
from .simulator import blocking_fetch_station


def run_sequential(
    stations: List[StationConfig],
    seed: int = 42,
    timeout_ms: Optional[int] = None
) -> RunReport:
    """
    Thực thi thu thập dữ liệu tuần tự từng trạm một.
    CPU phần lớn thời gian rảnh rỗi (idle waiting) khi đang chờ từng trạm phản hồi.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    t_start = time.perf_counter()

    results: List[StationResult] = []

    # Luồng tuần tự: lặp qua từng trạm, gọi và chờ xong mới sang trạm kế
    for config in stations:
        res = blocking_fetch_station(config, seed=seed, attempt=1, timeout_ms=timeout_ms)
        results.append(res)

    total_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

    # Tổng hợp số liệu
    success_cnt = sum(1 for r in results if r.status == "success")
    timeout_cnt = sum(1 for r in results if r.status == "timeout")
    fail_cnt = sum(1 for r in results if r.status in ("failed", "invalid"))
    cancel_cnt = sum(1 for r in results if r.status == "cancelled")

    throughput = (len(stations) / (total_elapsed_ms / 1000.0)) if total_elapsed_ms > 0 else 0.0
    digest = RunReport.compute_digest(results)

    return RunReport(
        run_id=f"seq_{int(time.time()*1000)}",
        mode="sequential",
        python_version=sys.version.split()[0],
        platform=platform.platform(),
        parameters={
            "num_stations": len(stations),
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
        max_in_flight=1,  # Tuần tự chỉ có đúng 1 tác vụ in-flight
        throughput_items_per_second=round(throughput, 2),
        result_digest=digest,
        station_results=results
    )
