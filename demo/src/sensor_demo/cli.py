"""
cli.py - Giao diện dòng lệnh (CLI) điều khiển Demo Chương 4.
Hỗ trợ:
- Chạy từng mode độc lập: --mode [seq|thread|async|process|hybrid]
- Chạy toàn bộ benchmark so sánh: --benchmark
- Thử nghiệm các bẫy/fault: --fault [f7|f8]
"""

import argparse
import sys
import os
import asyncio

# Cấu hình UTF-8 cho Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Đảm bảo đường dẫn module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sensor_demo import (
    get_default_stations,
    run_sequential,
    run_thread_pool,
    run_async,
    run_process_pool,
    run_hybrid,
    demo_f7_blocking_trap,
    demo_f8_race_condition
)
from sensor_demo.metrics import print_run_summary, print_benchmark_comparison, save_reports_to_disk


def main():
    parser = argparse.ArgumentParser(description="PDC Chapter 4 - Sensor Pipeline Demo")
    parser.add_argument("--mode", choices=["seq", "thread", "async", "process", "hybrid"], default=None,
                        help="Chọn chế độ thực thi cụ thể")
    parser.add_argument("--benchmark", action="store_true",
                        help="Chạy toàn bộ 5 chế độ và xuất bảng so sánh Benchmark đối đầu")
    parser.add_argument("--fault", choices=["f7", "f8"], default=None,
                        help="Chạy kịch bản tiêm lỗi F7 (Blocking sleep trap) hoặc F8 (Race condition)")
    parser.add_argument("--stations", type=int, default=8,
                        help="Số lượng trạm cảm biến (mặc định 8)")
    parser.add_argument("--concurrency", type=int, default=4,
                        help="Giới hạn worker/concurrency (mặc định 4)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed để tái lập kết quả xác định (mặc định 42)")
    parser.add_argument("--timeout", type=int, default=None,
                        help="Ngưỡng timeout cho mỗi trạm tính bằng ms")
    parser.add_argument("--high-cpu", action="store_true",
                        help="Tăng khối lượng tính toán CPU Anomaly để kiểm chứng ProcessPool")

    args = parser.parse_args()

    stations = get_default_stations(count=args.stations, high_cpu=args.high_cpu)

    if args.fault == "f7":
        print("⚡ [THÍ NGHIỆM F7]: Bẫy time.sleep() trong Coroutine làm chết đứng Event Loop")
        print("1. Chạy bản LỖI (broken with time.sleep)...")
        res_broken = asyncio.run(demo_f7_blocking_trap(use_fix=False, duration_sec=0.5))
        print(f"   -> Kết quả: Heartbeat ticks = {res_broken['heartbeat_ticks']} | Frozen: {res_broken['is_loop_frozen']}")
        print(f"   -> Giải thích: {res_broken['explanation']}")
        
        print("\n2. Chạy bản ĐÃ SỬA (fixed with asyncio.sleep)...")
        res_fixed = asyncio.run(demo_f7_blocking_trap(use_fix=True, duration_sec=0.5))
        print(f"   -> Kết quả: Heartbeat ticks = {res_fixed['heartbeat_ticks']} | Frozen: {res_fixed['is_loop_frozen']}")
        print(f"   -> Giải thích: {res_fixed['explanation']}")
        return

    if args.fault == "f8":
        print("⚡ [THÍ NGHIỆM F8]: Race Condition khi thiếu asyncio.Lock")
        print("1. Chạy không có Lock...")
        res_broken = asyncio.run(demo_f8_race_condition(use_lock=False, num_tasks=50))
        print(f"   -> {res_broken['message']}")
        print("\n2. Chạy có asyncio.Lock...")
        res_fixed = asyncio.run(demo_f8_race_condition(use_lock=True, num_tasks=50))
        print(f"   -> {res_fixed['message']}")
        return

    if args.benchmark or args.mode is None:
        print(f"🚀 BẮT ĐẦU CHẠY TOÀN BỘ BENCHMARK (Số trạm: {args.stations}, Concurrency: {args.concurrency}, Seed: {args.seed})...")
        reports = []

        print("\n[1/5] Đang chạy Sequential Baseline...")
        rep_seq = run_sequential(stations, seed=args.seed, timeout_ms=args.timeout)
        reports.append(rep_seq)

        print("[2/5] Đang chạy ThreadPoolExecutor...")
        rep_thread = run_thread_pool(stations, max_workers=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
        reports.append(rep_thread)

        print("[3/5] Đang chạy Asyncio Event Loop...")
        rep_async = run_async(stations, concurrency_limit=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
        reports.append(rep_async)

        print("[4/5] Đang chạy ProcessPoolExecutor (CPU-bound)...")
        rep_proc = run_process_pool(stations, max_workers=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
        reports.append(rep_proc)

        print("[5/5] Đang chạy Hybrid (Async I/O + Process CPU)...")
        rep_hyb = run_hybrid(stations, concurrency_limit=args.concurrency, cpu_workers=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
        reports.append(rep_hyb)

        print_benchmark_comparison(reports)
        save_reports_to_disk(reports)
        print("📁 Dữ liệu kết quả chi tiết đã được lưu vào thư mục demo/results/.")
        return

    # Chạy từng mode riêng lẻ
    if args.mode == "seq":
        rep = run_sequential(stations, seed=args.seed, timeout_ms=args.timeout)
    elif args.mode == "thread":
        rep = run_thread_pool(stations, max_workers=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
    elif args.mode == "async":
        rep = run_async(stations, concurrency_limit=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
    elif args.mode == "process":
        rep = run_process_pool(stations, max_workers=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
    elif args.mode == "hybrid":
        rep = run_hybrid(stations, concurrency_limit=args.concurrency, cpu_workers=args.concurrency, seed=args.seed, timeout_ms=args.timeout)
    else:
        return

    print_run_summary(rep)


if __name__ == "__main__":
    main()
