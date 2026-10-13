# HỆ THỐNG DEMO THỰC TẾ TRỰC QUAN HÓA (CHƯƠNG 4 - PDC)

> **Dự án:** Parallel and Distributed Computing — Chương 4: Phương pháp tính toán bất đồng bộ trong Python  
> **Kiến trúc:** Trung tâm giám sát và phân tích dữ liệu cảm biến IoT đa chế độ (`Sequential`, `ThreadPool`, `ProcessPool`, `Asyncio`, `Hybrid`).  
> **Đặc tả nguồn:** Tuân thủ 100% tài liệu [`docs/04_DAC_TA_DEMO_THUC_TE_NHO.md`](../docs/04_DAC_TA_DEMO_THUC_TE_NHO.md).

---

## 🌟 ĐIỂM ĐẶC BIỆT CỦA BẢN DEMO THỰC TẾ

Thay vì những đoạn code khô khan trên Jupyter Notebook / Google Colab khó quan sát được hiện tượng đồng thời, hệ thống cung cấp **Giao Diện Trực Quan Hóa Chia Đôi Màn Hình (Split-Screen Interactive Visualizer)**:

1. **Bên Trái (Interactive Visual Simulator — Mô phỏng như Video Động):**
   - **Mạng lưới trạm cảm biến IoT:** Trạm $S_1 \dots S_N$ phát tín hiệu, gửi các gói tin dữ liệu cảm biến bay trên đường truyền.
   - **Động cơ điều phối trực quan:**
     - `Sequential`: Nút thắt cổ chai, từng trạm nối đuôi nhau, CPU rảnh rỗi lãng phí thời gian khi chờ I/O.
     - `ThreadPoolExecutor`: Khối 4 Worker Threads cùng nhận task song song.
     - `Asyncio`: **Vòng tròn Event Loop** quay tròn nhịp nhàng! 1 Single-Thread duy nhất điều phối hàng loạt coroutines mà không tốn chi phí đa luồng.
     - `ProcessPoolExecutor`: 4 lõi CPU độc lập vượt rào cản GIL của Python để tính toán dị thường.
     - `Hybrid`: Asyncio thu gom I/O tốc độ cao $\to$ Bounded Queue (Backpressure) $\to$ ProcessPool xử lý CPU.
     - `Bẫy F7`: Khi gọi `time.sleep()` trong coroutine, **Event Loop bị ĐÓNG BĂNG MÀU ĐỎ**, heartbeat ngưng trệ, toàn bộ trạm bị tê liệt!
   - **Gantt Timeline thời gian thực:** Quan sát rõ từng trạm bắt đầu lúc nào, chờ I/O bao lâu, tính CPU lúc nào và hoàn tất khi nào.
   - **Đồng hồ HUD:** Thời gian chạy (ms), Thông lượng (trạm/s), Tác vụ in-flight, Oracle Digest (SHA-256).

2. **Bên Phải (Live Code Execution Flow — Luồng Code chạy tới đâu sáng tới đó):**
   - Hiển thị đúng mã nguồn Python thực tế của mode đang chạy.
   - **Dòng code đang thực thi sáng rực rỡ theo thời gian thực (Active Line Glowing Marker `►`)**, đồng bộ từng mili-giây với chuyển động bên trái!
   - **Bảng soi biến (Variable Inspector):** Cập nhật giá trị biến tức thời (`in_flight`, `sem_permits`, `event_loop_state`, `queue_size`).
   - **Terminal Console:** In log tiến trình chuẩn xác có timestamp micro-giây.

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY NHANH

### Cách 1: Mở Giao diện Trực quan hóa Split-Screen (Khuyên dùng)

**Cách nhanh nhất:**
- Click đúp chuột trực tiếp vào file **`index.html`** trong thư mục `demo` (hoặc mở bằng bất kỳ trình duyệt Chrome/Edge/Firefox nào). Hoàn toàn offline, không cần cài thêm thư viện!

**Hoặc chạy qua Web Server nội bộ của Python:**
```bash
python serve_visualizer.py
```
> Trình duyệt web sẽ tự động mở địa chỉ: `http://localhost:8000/index.html`.

---

### Cách 2: Chạy Benchmark Đối Đầu 5 Chế Độ (CLI)

Chạy đối đầu toàn bộ 5 chế độ trên cùng một bộ dữ liệu, kiểm tra Oracle Digest và xuất bảng so sánh hiệu năng:

```bash
python run_demo.py --benchmark
```

**Kết quả đối chiếu thực tế:**
```text
================================================================================
🚀 BẢNG ĐỐI CHIẾU BENCHMARK GIỮA CÁC CHẾ ĐỘ THỰC THI (CHƯƠNG 4)
================================================================================
Chế độ (Mode)      | Thời gian (ms)   | Speedup    | Throughput     | Oracle Match
--------------------------------------------------------------------------------
SEQUENTIAL         | 2891.15          | 1.00x (Gốc) | 2.77           | ✅ Khớp 100%
THREAD             | 968.34           | 2.99x      | 8.26           | ✅ Khớp 100%
ASYNC              | 975.95           | 2.96x      | 8.20           | ✅ Khớp 100%
PROCESS            | 3527.87          | 0.82x      | 2.27           | ✅ Khớp 100%
HYBRID             | 1081.73          | 2.67x      | 7.40           | ✅ Khớp 100%
================================================================================
```

---

### Cách 3: Chạy Thí Nghiệm Tiêm Lỗi (Fault Injections)

**1. Thí nghiệm F7 — Bẫy `time.sleep()` làm đơ Event Loop:**
```bash
python run_demo.py --fault f7
```
> So sánh trực quan giữa việc Event Loop bị đóng băng hoàn toàn khi dùng sai `time.sleep()` và khi sửa đúng bằng `asyncio.sleep()`.

**2. Thí nghiệm F8 — Race Condition khi thiếu `asyncio.Lock`:**
```bash
python run_demo.py --fault f8
```

---

### Cách 4: Chạy Unit Tests Kiểm Thử Tính Đúng

Chạy bộ test kiểm thử tính đúng (Correctness Suite & Oracle Digest):
```bash
python -m unittest discover -s tests
```

---

## 📁 CẤU TRÚC THƯ MỤC MÃ NGUỒN

```text
demo/
├── index.html                   # Giao diện trực quan hóa 2 màn hình (chạy ngay không cần cài đặt)
├── serve_visualizer.py          # Web Server Python mở visualizer với 1 lệnh
├── run_demo.py                  # Entrypoint CLI chạy các chế độ và benchmark
├── visualizer/
│   └── index.html               # Bản sao module visualizer
├── src/
│   └── sensor_demo/
│       ├── __init__.py
│       ├── models.py            # Mô hình dữ liệu: StationConfig, SensorRecord, RunReport
│       ├── config.py            # Cấu hình danh sách trạm cảm biến
│       ├── simulator.py         # Bộ sinh dữ liệu xác định, Blocking/Async adapters, CPU anomaly
│       ├── sequential_mode.py   # Chế độ Tuần tự (Sequential Baseline & Oracle)
│       ├── thread_mode.py       # Chế độ Đa luồng (ThreadPoolExecutor & as_completed)
│       ├── async_mode.py        # Chế độ Bất đồng bộ (Asyncio Event Loop, Tasks, Semaphore)
│       ├── process_mode.py      # Chế độ Đa tiến trình (ProcessPoolExecutor vượt GIL)
│       ├── hybrid_mode.py       # Chế độ Lai (Asyncio I/O + Bounded Queue + ProcessPool)
│       ├── resilience.py        # Kịch bản tiêm lỗi F7 (blocking sleep trap) & F8 (race condition)
│       ├── metrics.py           # Tổng hợp số liệu, in bảng và lưu báo cáo CSV/JSON
│       └── cli.py               # Xử lý tham số dòng lệnh CLI
├── tests/
│   └── test_correctness.py      # Kiểm thử đối chiếu Oracle Digest giữa cả 5 mode
└── results/
    ├── raw/                     # File JSON chi tiết của từng lần chạy
    └── summaries/               # File CSV tổng hợp kết quả benchmark
```

---

## 👥 ÁNH XẠ TRÁCH NHIỆM 6 THÀNH VIÊN (THEO D03 & D05)

| Thành viên | Phụ trách chuyên môn | Module Mã nguồn đã xây dựng |
|---|---|---|
| **TV1** | Data contract, Deterministic Simulator, Baseline Oracle | `models.py`, `simulator.py`, `sequential_mode.py` |
| **TV2** | Future lifecycle, ThreadPoolExecutor, Blocking Adapter | `thread_mode.py` |
| **TV3** | CPU Anomaly, ProcessPoolExecutor, GIL & IPC Overhead | `process_mode.py` |
| **TV4** | Event loop, Coroutine, Tasks, Bẫy Blocking F7 | `async_mode.py`, `resilience.py (F7)` |
| **TV5** | Bounded Concurrency, Semaphore, Backpressure Queue, Lock | `resilience.py (F8)`, Semaphore & Queue logic |
| **TV6** | Mô hình Lai (Hybrid), CLI, Visualizer Dashboard, Runbook | `hybrid_mode.py`, `cli.py`, `visualizer/index.html` |
