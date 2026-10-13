"""
run_demo.py - Điểm khởi chạy nhanh cho toàn bộ hệ thống Demo Chương 4.
Ví dụ sử dụng:
    python run_demo.py --benchmark
    python run_demo.py --mode async
    python run_demo.py --fault f7
"""

import sys
import os

# Cấu hình UTF-8 cho Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Thêm đường dẫn src vào PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from sensor_demo.cli import main

if __name__ == "__main__":
    main()
