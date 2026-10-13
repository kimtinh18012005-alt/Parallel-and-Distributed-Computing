"""
sensor_demo package - Mô phỏng hệ thống thu thập và phân tích cảm biến Chương 4.
"""

from .models import StationConfig, SensorRecord, StationResult, RunReport
from .config import get_default_stations
from .sequential_mode import run_sequential
from .thread_mode import run_thread_pool
from .async_mode import run_async
from .process_mode import run_process_pool
from .hybrid_mode import run_hybrid
from .resilience import demo_f7_blocking_trap, demo_f8_race_condition

__all__ = [
    "StationConfig",
    "SensorRecord",
    "StationResult",
    "RunReport",
    "get_default_stations",
    "run_sequential",
    "run_thread_pool",
    "run_async",
    "run_process_pool",
    "run_hybrid",
    "demo_f7_blocking_trap",
    "demo_f8_race_condition",
]
