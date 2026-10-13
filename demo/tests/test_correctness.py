"""
test_correctness.py - Kiểm thử tính đúng (Correctness & Oracle Digest).
Đảm bảo tất cả các chế độ chạy cùng seed thì kết quả nghiệp vụ và digest phải khớp nhau 100%.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sensor_demo import (
    get_default_stations,
    run_sequential,
    run_thread_pool,
    run_async,
    run_process_pool,
    run_hybrid
)
from sensor_demo.models import RunReport


class TestSensorPipelineCorrectness(unittest.TestCase):

    def setUp(self):
        self.stations = get_default_stations(count=6, high_cpu=False)
        self.seed = 12345

    def test_all_modes_match_oracle_digest(self):
        """Tất cả 5 chế độ phải cho cùng digest với Sequential Baseline khi cùng seed."""
        seq_report = run_sequential(self.stations, seed=self.seed)
        oracle_digest = seq_report.result_digest

        thread_report = run_thread_pool(self.stations, max_workers=3, seed=self.seed)
        async_report = run_async(self.stations, concurrency_limit=3, seed=self.seed)
        proc_report = run_process_pool(self.stations, max_workers=3, seed=self.seed)
        hyb_report = run_hybrid(self.stations, concurrency_limit=3, cpu_workers=2, seed=self.seed)

        self.assertEqual(thread_report.result_digest, oracle_digest, "Thread mode digest must match oracle")
        self.assertEqual(async_report.result_digest, oracle_digest, "Async mode digest must match oracle")
        self.assertEqual(proc_report.result_digest, oracle_digest, "Process mode digest must match oracle")
        self.assertEqual(hyb_report.result_digest, oracle_digest, "Hybrid mode digest must match oracle")

    def test_station_counts_and_statuses(self):
        """Số lượng bản ghi thành công và lỗi phải đồng nhất giữa các chế độ."""
        seq_report = run_sequential(self.stations, seed=self.seed)
        async_report = run_async(self.stations, concurrency_limit=3, seed=self.seed)

        self.assertEqual(seq_report.success_count, async_report.success_count)
        self.assertEqual(seq_report.timeout_count, async_report.timeout_count)
        self.assertEqual(seq_report.failure_count, async_report.failure_count)


if __name__ == "__main__":
    unittest.main()
