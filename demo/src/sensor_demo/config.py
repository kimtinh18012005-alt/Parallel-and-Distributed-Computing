"""
config.py - Cấu hình mặc định cho kịch bản cảm biến IoT.
Tạo danh sách trạm với các đặc tính:
- Station 1..8 (hoặc 12)
- Độ trễ nền (base_delay_ms)
- Jitter
- Xác suất lỗi
- CPU computation complexity
"""

from typing import List
from .models import StationConfig


def get_default_stations(count: int = 8, high_cpu: bool = False) -> List[StationConfig]:
    """Tạo danh sách các trạm cảm biến chuẩn hóa cho demo."""
    cpu_size = 50000 if high_cpu else 15000
    
    # Kịch bản 8 trạm với độ trễ từ 150ms đến 650ms
    base_delays = [200, 350, 150, 500, 250, 400, 600, 300, 450, 220, 380, 550]
    
    stations = []
    for i in range(count):
        sid = f"STATION_{i+1:02d}"
        delay = base_delays[i % len(base_delays)]
        # Một số trạm có thể có lỗi kết nối nhẹ hoặc jitter cao
        fail_prob = 0.10 if (i == 3) else 0.0  # Trạm 4 có 10% rủi ro rớt mạng
        mal_prob = 0.05 if (i == 6) else 0.0   # Trạm 7 có 5% dữ liệu bất thường
        
        stations.append(StationConfig(
            station_id=sid,
            base_delay_ms=delay,
            jitter_ms=40,
            failure_probability=fail_prob,
            malformed_probability=mal_prob,
            cpu_size=cpu_size
        ))
    return stations
