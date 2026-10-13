"""
simulator.py - Bộ mô phỏng I/O trạm cảm biến và phân tích CPU xác định (Deterministic).
Cung cấp:
- Bộ sinh dữ liệu xác định dựa trên (seed, station_id, attempt)
- Blocking adapter (cho Sequential / ThreadPool)
- Async adapter (cho Asyncio / Event Loop)
- Phép tính Anomaly CPU-bound thực thụ (không sleep)
"""

from __future__ import annotations
import time
import asyncio
import hashlib
import math
from typing import Tuple, Optional
from datetime import datetime, timezone
from .models import StationConfig, SensorRecord, StationResult


def _deterministic_hash(seed: int, station_id: str, attempt: int, salt: str = "") -> int:
    """Tạo số băm xác định từ seed, station_id, attempt."""
    key = f"{seed}:{station_id}:{attempt}:{salt}"
    h = hashlib.sha256(key.encode()).hexdigest()
    return int(h[:8], 16)


def compute_station_delay_ms(config: StationConfig, seed: int, attempt: int) -> int:
    """Tính độ trễ xác định cho trạm."""
    raw = _deterministic_hash(seed, config.station_id, attempt, "delay")
    jitter = (raw % (2 * config.jitter_ms + 1)) - config.jitter_ms
    return max(10, config.base_delay_ms + jitter)


def generate_sensor_record(config: StationConfig, seed: int, attempt: int) -> Tuple[Optional[SensorRecord], Optional[str]]:
    """
    Sinh bản ghi cảm biến xác định.
    Kiểm tra xác suất lỗi kết nối hoặc payload hỏng.
    """
    fail_rand = (_deterministic_hash(seed, config.station_id, attempt, "fail") % 1000) / 1000.0
    if fail_rand < config.failure_probability:
        return None, "ConnectionError: Network timeout or unreachable host"

    mal_rand = (_deterministic_hash(seed, config.station_id, attempt, "malformed") % 1000) / 1000.0
    now_iso = datetime.now(timezone.utc).isoformat()
    val_seed = _deterministic_hash(seed, config.station_id, attempt, "values")

    temp = 20.0 + (val_seed % 250) / 10.0  # 20.0 - 45.0 °C
    humidity = 40.0 + ((val_seed // 10) % 550) / 10.0  # 40.0 - 95.0 %
    aqi = 20 + ((val_seed // 100) % 200)  # 20 - 220

    if mal_rand < config.malformed_probability:
        # Tiêm dữ liệu hỏng: ví dụ nhiệt độ âm vô lý hoặc độ ẩm > 100
        temp = 999.9

    rec = SensorRecord(
        station_id=config.station_id,
        sequence=attempt,
        observed_at=now_iso,
        temperature_c=round(temp, 2),
        humidity_percent=round(humidity, 2),
        air_quality_index=int(aqi),
    )
    return rec, None


def validate_record(record: SensorRecord) -> Tuple[bool, Optional[str]]:
    """Kiểm tra tính hợp lệ của bản ghi cảm biến theo luật nghiệp vụ."""
    if not (-30.0 <= record.temperature_c <= 80.0):
        return False, f"Temperature out of valid range [-30, 80]: {record.temperature_c}"
    if not (0.0 <= record.humidity_percent <= 100.0):
        return False, f"Humidity out of valid range [0, 100]: {record.humidity_percent}"
    if record.air_quality_index < 0:
        return False, f"AQI cannot be negative: {record.air_quality_index}"
    return True, None


def cpu_intensive_anomaly_detection(record: SensorRecord, cpu_size: int = 15000) -> Tuple[float, bool]:
    """
    Hàm tính toán CPU-bound thực sự (không sleep).
    Mô phỏng phép phân tích FFT/đa thức tính chỉ số biến động môi trường.
    Hàm này ở top-level để ProcessPoolExecutor có thể pickle được trên Windows.
    """
    acc = 0.0
    base_val = record.temperature_c * 0.4 + record.humidity_percent * 0.3 + record.air_quality_index * 0.3
    # Vòng lặp tính toán tiêu tốn CPU thực tế
    for i in range(1, cpu_size + 1):
        x = (base_val + i) * 0.001
        acc += math.sin(x) * math.cos(x * 0.5) + math.sqrt(abs(x))
    
    anomaly_score = abs(acc) % 100.0
    is_anomaly = anomaly_score > 75.0 or record.air_quality_index > 150
    return round(anomaly_score, 4), is_anomaly


# -------------------------------------------------------------
# Adapters: Blocking & Async
# -------------------------------------------------------------

def blocking_fetch_station(
    config: StationConfig,
    seed: int,
    attempt: int = 1,
    timeout_ms: Optional[int] = None
) -> StationResult:
    """
    Blocking Adapter: Dùng time.sleep mô phỏng chờ I/O mạng đồng bộ.
    Dùng cho chế độ Sequential và ThreadPool.
    """
    t0 = time.perf_counter()
    delay_ms = compute_station_delay_ms(config, seed, attempt)
    
    if timeout_ms is not None and delay_ms > timeout_ms:
        time.sleep(timeout_ms / 1000.0)
        elapsed = (time.perf_counter() - t0) * 1000.0
        return StationResult(
            station_id=config.station_id,
            status="timeout",
            attempts=attempt,
            elapsed_ms=round(elapsed, 2),
            error_type="TimeoutError",
            error_message=f"I/O timeout exceeded {timeout_ms}ms (delay was {delay_ms}ms)"
        )

    # Chờ I/O hoàn tất
    time.sleep(delay_ms / 1000.0)
    record, err = generate_sensor_record(config, seed, attempt)
    elapsed = (time.perf_counter() - t0) * 1000.0

    if err:
        return StationResult(
            station_id=config.station_id,
            status="failed",
            attempts=attempt,
            elapsed_ms=round(elapsed, 2),
            error_type="ConnectionError",
            error_message=err
        )

    # Validate
    valid, val_err = validate_record(record)
    if not valid:
        return StationResult(
            station_id=config.station_id,
            status="invalid",
            attempts=attempt,
            elapsed_ms=round(elapsed, 2),
            record=record,
            error_type="ValidationError",
            error_message=val_err
        )

    # Phân tích CPU nhẹ tại chỗ
    score, is_ano = cpu_intensive_anomaly_detection(record, config.cpu_size)
    elapsed = (time.perf_counter() - t0) * 1000.0

    return StationResult(
        station_id=config.station_id,
        status="success",
        attempts=attempt,
        elapsed_ms=round(elapsed, 2),
        record=record,
        anomaly_score=score,
        is_anomaly=is_ano
    )


async def async_fetch_station(
    config: StationConfig,
    seed: int,
    attempt: int = 1,
    timeout_ms: Optional[int] = None
) -> StationResult:
    """
    Async Adapter: Dùng asyncio.sleep nhường quyền điều khiển cho Event Loop.
    Dùng cho Asyncio và Hybrid mode.
    """
    t0 = time.perf_counter()
    delay_ms = compute_station_delay_ms(config, seed, attempt)

    if timeout_ms is not None and delay_ms > timeout_ms:
        await asyncio.sleep(timeout_ms / 1000.0)
        elapsed = (time.perf_counter() - t0) * 1000.0
        return StationResult(
            station_id=config.station_id,
            status="timeout",
            attempts=attempt,
            elapsed_ms=round(elapsed, 2),
            error_type="TimeoutError",
            error_message=f"I/O timeout exceeded {timeout_ms}ms (delay was {delay_ms}ms)"
        )

    await asyncio.sleep(delay_ms / 1000.0)
    record, err = generate_sensor_record(config, seed, attempt)
    elapsed = (time.perf_counter() - t0) * 1000.0

    if err:
        return StationResult(
            station_id=config.station_id,
            status="failed",
            attempts=attempt,
            elapsed_ms=round(elapsed, 2),
            error_type="ConnectionError",
            error_message=err
        )

    valid, val_err = validate_record(record)
    if not valid:
        return StationResult(
            station_id=config.station_id,
            status="invalid",
            attempts=attempt,
            elapsed_ms=round(elapsed, 2),
            record=record,
            error_type="ValidationError",
            error_message=val_err
        )

    score, is_ano = cpu_intensive_anomaly_detection(record, config.cpu_size)
    elapsed = (time.perf_counter() - t0) * 1000.0

    return StationResult(
        station_id=config.station_id,
        status="success",
        attempts=attempt,
        elapsed_ms=round(elapsed, 2),
        record=record,
        anomaly_score=score,
        is_anomaly=is_ano
    )
