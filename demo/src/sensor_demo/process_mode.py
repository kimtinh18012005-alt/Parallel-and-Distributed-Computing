"""
process_mode.py - Chế độ Đa tiến trình (ProcessPoolExecutor).
Phục vụ mục tiêu:
1. Vượt qua giới hạn GIL của CPython đối với các tác vụ CPU-bound nặng.
2. Tách bước phân tích dữ liệu CPU sang các worker process độc lập.
3. Đo lường chi phí IPC / serialization (Pickling) so với hiệu năng đạt được.
"""

from __future__ import annotations
import time
import platform
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Optional, Tuple
from datetime import datetime, timezone
from .models import StationConfig, StationResult, RunReport, SensorRecord
from .simulator import (
    blocking_fetch_station,
    cpu_intensive_anomaly_detection
)


def _worker_process_cpu_task(args: Tuple[SensorRecord, int]) -> Tuple[float, bool]:
    """
    Top-level worker function để chạy trong ProcessPoolExecutor.
    Bắt buộc phải nằm ở top-level module để Windows spawn process có thể pickle được.
    """
    record, cpu_size = args
    return cpu_intensive_anomaly_detection(record, cpu_size)


def run_process_pool(
    stations: List[StationConfig],
    max_workers: int = 4,
    seed: int = 42,
    timeout_ms: Optional[int] = None
) -> RunReport:
    """
    Thực thi với ProcessPoolExecutor cho bước tính toán CPU-bound.
    Lưu ý: I/O có thể thu thập rồi dispatch batch CPU tính toán song song ra pool tiến trình.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    t_start = time.perf_counter()

    # Bước 1: Thu thập bản ghi
    raw_results = [
        blocking_fetch_station(cfg, seed=seed, attempt=1, timeout_ms=timeout_ms)
        for cfg in stations
    ]

    # Bước 2: Tách các bản ghi hợp lệ cần phân tích CPU nặng
    records_to_process = []
    station_map = {}
    for r in raw_results:
        if r.status == "success" and r.record is not None:
            # Tìm cpu_size tương ứng
            cfg = next(c for c in stations if c.station_id == r.station_id)
            records_to_process.append((r.station_id, r.record, cfg.cpu_size))
            station_map[r.station_id] = r

    # Bước 3: Đẩy vào ProcessPoolExecutor
    if records_to_process:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_sid = {
                executor.submit(_worker_process_cpu_task, (rec, csize)): sid
                for sid, rec, csize in records_to_process
            }
            for fut in as_completed(future_to_sid):
                sid = future_to_sid[fut]
                score, is_ano = fut.result()
                target_res = station_map[sid]
                target_res.anomaly_score = score
                target_res.is_anomaly = is_ano

    total_elapsed_ms = (time.perf_counter() - t_start) * 1000.0

    success_cnt = sum(1 for r in raw_results if r.status == "success")
    timeout_cnt = sum(1 for r in raw_results if r.status == "timeout")
    fail_cnt = sum(1 for r in raw_results if r.status in ("failed", "invalid"))
    cancel_cnt = sum(1 for r in raw_results if r.status == "cancelled")

    throughput = (len(stations) / (total_elapsed_ms / 1000.0)) if total_elapsed_ms > 0 else 0.0
    digest = RunReport.compute_digest(raw_results)

    return RunReport(
        run_id=f"process_{int(time.time()*1000)}",
        mode="process",
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
        station_results=raw_results
    )
