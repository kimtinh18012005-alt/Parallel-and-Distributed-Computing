"""
models.py - Mô hình dữ liệu chuẩn theo Đặc tả Demo Chương 4 (D05).
Bao gồm: StationConfig, SensorRecord, StationResult, RunReport.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import hashlib
import json


@dataclass(frozen=True)
class StationConfig:
    """Cấu hình cho từng trạm cảm biến."""
    station_id: str
    base_delay_ms: int
    jitter_ms: int = 50
    failure_probability: float = 0.0
    malformed_probability: float = 0.0
    cpu_size: int = 15000  # Độ phức tạp tính toán CPU anomaly


@dataclass
class SensorRecord:
    """Bản ghi cảm biến đo được từ trạm."""
    station_id: str
    sequence: int
    observed_at: str
    temperature_c: float
    humidity_percent: float
    air_quality_index: int
    payload_checksum: str = ""

    def __post_init__(self):
        if not self.payload_checksum:
            raw = f"{self.station_id}:{self.sequence}:{self.temperature_c:.2f}:{self.humidity_percent:.2f}:{self.air_quality_index}"
            object.__setattr__(self, "payload_checksum", hashlib.sha256(raw.encode()).hexdigest()[:12])


@dataclass
class StationResult:
    """Kết quả thu thập và phân tích của một trạm."""
    station_id: str
    status: str  # "success" | "timeout" | "failed" | "invalid" | "cancelled"
    attempts: int = 1
    elapsed_ms: float = 0.0
    record: Optional[SensorRecord] = None
    anomaly_score: float = 0.0
    is_anomaly: bool = False
    error_type: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RunReport:
    """Báo cáo tổng hợp một lần chạy demo."""
    run_id: str
    mode: str
    python_version: str
    platform: str
    parameters: Dict[str, Any]
    seed: int
    started_at: str
    elapsed_ms: float
    success_count: int
    timeout_count: int
    failure_count: int
    cancelled_count: int
    max_in_flight: int
    throughput_items_per_second: float
    result_digest: str
    station_results: List[StationResult] = field(default_factory=list)

    @classmethod
    def compute_digest(cls, results: List[StationResult]) -> str:
        """
        Oracle tính đúng: Chuẩn hóa theo thứ tự station_id và băm digest.
        Đảm bảo mọi chế độ (sequential, thread, async, process, hybrid)
        khi chạy cùng seed sẽ cho ra cùng một digest duy nhất.
        """
        sorted_results = sorted(results, key=lambda r: r.station_id)
        tokens = []
        for r in sorted_results:
            rec_str = r.record.payload_checksum if r.record else "NONE"
            tokens.append(f"{r.station_id}:{r.status}:{rec_str}:{r.anomaly_score:.4f}")
        raw = "|".join(tokens)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)
