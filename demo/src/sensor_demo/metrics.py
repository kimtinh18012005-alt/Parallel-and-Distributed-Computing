"""
metrics.py - Tổng hợp số liệu, in bảng kết quả và so sánh Benchmark.
"""

from __future__ import annotations
import os
import json
import csv
from typing import List, Dict, Any
from .models import RunReport


def print_run_summary(report: RunReport) -> None:
    """In tóm tắt kết quả chạy ra console."""
    sep = "=" * 70
    print(sep)
    print(f"📊 KẾT QUẢ THỰC THI: [{report.mode.upper()}] (Run ID: {report.run_id})")
    print(sep)
    print(f"  • Thời gian tổng cộng  : {report.elapsed_ms:.2f} ms ({report.elapsed_ms/1000.0:.3f} s)")
    print(f"  • Thông lượng          : {report.throughput_items_per_second:.2f} trạm/giây")
    print(f"  • Số tác vụ in-flight  : {report.max_in_flight}")
    print(f"  • Trạng thái các trạm  : ✅ Thành công: {report.success_count} | ⏱ Timeout: {report.timeout_count} | ❌ Lỗi: {report.failure_count}")
    print(f"  • Result Digest (Oracle): {report.result_digest}")
    print(sep)
    print(f"{'Station':<12} | {'Trạng thái':<10} | {'Thời gian(ms)':<14} | {'Nhiệt độ':<10} | {'Độ ẩm':<8} | {'AQI':<6} | {'Dị thường':<10}")
    print("-" * 70)
    for r in sorted(report.station_results, key=lambda x: x.station_id):
        if r.record:
            temp = f"{r.record.temperature_c:.1f}°C"
            hum = f"{r.record.humidity_percent:.1f}%"
            aqi = f"{r.record.air_quality_index}"
        else:
            temp = hum = aqi = "N/A"
        ano_str = "⚠️ CÓ" if r.is_anomaly else "An toàn"
        print(f"{r.station_id:<12} | {r.status:<10} | {r.elapsed_ms:<14.1f} | {temp:<10} | {hum:<8} | {aqi:<6} | {ano_str:<10}")
    print(sep)


def print_benchmark_comparison(reports: List[RunReport]) -> None:
    """In bảng so sánh hiệu năng giữa các chế độ."""
    seq_report = next((r for r in reports if r.mode == "sequential"), None)
    baseline_time = seq_report.elapsed_ms if seq_report else (reports[0].elapsed_ms if reports else 1.0)

    sep = "=" * 80
    print("\n" + sep)
    print("🚀 BẢNG ĐỐI CHIẾU BENCHMARK GIỮA CÁC CHẾ ĐỘ THỰC THI (CHƯƠNG 4)")
    print(sep)
    print(f"{'Chế độ (Mode)':<18} | {'Thời gian (ms)':<16} | {'Speedup':<10} | {'Throughput':<14} | {'Oracle Match'}")
    print("-" * 80)

    baseline_digest = seq_report.result_digest if seq_report else ""

    for r in reports:
        speedup = (baseline_time / r.elapsed_ms) if r.elapsed_ms > 0 else 1.0
        speedup_str = f"{speedup:.2f}x" if r.mode != "sequential" else "1.00x (Gốc)"
        digest_match = "✅ Khớp 100%" if (baseline_digest and r.result_digest == baseline_digest) else ("Baseline" if r.mode == "sequential" else "⚠️ Khác biệt")
        print(f"{r.mode.upper():<18} | {r.elapsed_ms:<16.2f} | {speedup_str:<10} | {r.throughput_items_per_second:<14.2f} | {digest_match}")
    print(sep)
    print("💡 Nhận xét sư phạm:")
    print("   1. ThreadPool & Asyncio giảm mạnh tổng thời gian nhờ gom chồng lấn chờ I/O.")
    print("   2. Asyncio đạt hiệu quả tương đương ThreadPool nhưng chỉ dùng DUY NHẤT 1 luồng (Single-thread).")
    print("   3. ProcessPool phát huy tối đa sức mạnh khi tải CPU-bound đủ lớn để bù đắp chi phí IPC/Fork.")
    print(sep + "\n")


def save_reports_to_disk(reports: List[RunReport], base_dir: str = "results") -> None:
    """Lưu báo cáo thô dạng JSON và CSV."""
    raw_dir = os.path.join(base_dir, "raw")
    sum_dir = os.path.join(base_dir, "summaries")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(sum_dir, exist_ok=True)

    # 1. Lưu từng run JSON
    for r in reports:
        fname = os.path.join(raw_dir, f"{r.run_id}_{r.mode}.json")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(r.to_json())

    # 2. Lưu bảng tổng hợp CSV
    summary_csv = os.path.join(sum_dir, "benchmark_summary.csv")
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["run_id", "mode", "elapsed_ms", "throughput", "success", "timeout", "failed", "digest"])
        for r in reports:
            writer.writerow([r.run_id, r.mode, r.elapsed_ms, r.throughput_items_per_second, r.success_count, r.timeout_count, r.failure_count, r.result_digest])
