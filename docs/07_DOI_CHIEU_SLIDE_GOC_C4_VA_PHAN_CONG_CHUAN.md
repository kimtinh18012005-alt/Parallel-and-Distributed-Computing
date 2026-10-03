# ĐỐI CHIẾU NHIỆM VỤ THÀNH VIÊN VỚI SLIDE GỐC (BaiGiang_TinhToanSongSong_PhanTan_C4.pdf)

> **Mục tiêu tài liệu:** Rà soát, đối chiếu toàn bộ phân công nhiệm vụ từ Thành viên 1 (TV1) đến Thành viên 6 (TV6) với tài liệu bài giảng gốc của giảng viên: **Chương 4 — Lập trình Đồng thời và Bất đồng bộ trong Python** (gồm 24 trang slide chuẩn).
> **Nguyên tắc cốt lõi:** Bám sát 100% nội dung học thuật chuẩn mực trong slide gốc; loại bỏ các nội dung ngoài lề, không cần thiết để bài giảng tập trung, sư phạm và đạt điểm tối đa khi báo cáo/giảng dạy.

---

## 1. TỔNG QUAN NỘI DUNG SLIDE GỐC CHƯƠNG 4 (24 SLIDE)

Slide bài giảng gốc của môn học gồm 6 phần lớn được phân bổ trên 24 trang:

| Trang Slide gốc | Tiêu đề phần trong slide gốc | Nội dung cốt lõi của giảng viên | Phân công phụ trách |
|---|---|---|---|
| **Slide 1 – 8** | **PHẦN I: GIỚI THIỆU** | • Tuần tự (Sequential execution)<br>• Đồng thời (Concurrency) & Process ID<br>• Song song (Parallelism) & Multi-core CPU<br>• So sánh Tuần tự vs Đồng thời vs Song song<br>• Bất đồng bộ (Asynchronous execution)<br>• Mô hình luồng đơn bất đồng bộ (Single-thread concurrent async execution model)<br>• Hai ví dụ thực tế gốc: Bãi giữ xe & Đi thi | **Thành viên 1 (TV1)** |
| **Slide 9 – 12** | **PHẦN II: CONCURRENT.FUTURES & THREADPOOLEXECUTOR** | • Giới thiệu module `concurrent.futures`<br>• Khái niệm Executor Objects & Future Objects<br>• `ThreadPoolExecutor` và cách khởi tạo thread worker<br>• Cơ chế `submit()`, `map()`, thu hoạch kết quả | **Thành viên 2 (TV2)** |
| **Slide 13 – 15** | **PHẦN III: PROCESSPOOLEXECUTOR & QUẢN LÝ TIẾN TRÌNH** | • Khái niệm Nhóm tiến trình (Process Pool)<br>• `ProcessPoolExecutor` vượt qua rào cản GIL<br>• So sánh hiệu năng CPU-bound giữa Thread và Process<br>• Latency khởi tạo worker và quản lý tài nguyên | **Thành viên 3 (TV3)** |
| **Slide 16 – 19** | **PHẦN IV: ASYNCIO & QUẢN LÝ VÒNG LẶP SỰ KIỆN** | • Giới thiệu thư viện `asyncio`<br>• Khái niệm Event Loop (Vòng lặp sự kiện)<br>• 3 thành phần: Event Source, Event Handler, Event Loop<br>• Coroutines và Tasks trong Asyncio (`async`/`await`) | **Thành viên 4 (TV4)** |
| **Slide 20 – 22** | **PHẦN V: XỬ LÝ TÁC VỤ ĐỒNG THỜI VỚI ASYNCIO & PIPELINE** | • Subroutine vs Coroutine<br>• Cơ chế yielding a value và kiểm soát luồng điều khiển<br>• Xây dựng đường ống (Pipeline) xử lý bất đồng bộ | **Thành viên 5 (TV5)** |
| **Slide 23 – 24** | **PHẦN VI: LƯU Ý & TỔNG KẾT TOÀN CHƯƠNG** | • Các lưu ý quan trọng khi chọn giải pháp đồng thời/bất đồng bộ<br>• Tổng kết, ma trận so sánh các mô hình và ứng dụng thực tế | **Thành viên 6 (TV6)** |

---

## 2. KẾT QUẢ RÀ SOÁT & TINH GỌN (LỌC BỎ CÁC YẾU TỐ NGOÀI LỀ)



## 3. CHI TIẾT PHÂN CÔNG CHUẨN XÁC CHO 6 THÀNH VIÊN

### THÀNH VIÊN 1 (TV1) — NỀN TẢNG CỐT LÕI & CÁC MÔ HÌNH THỰC THI (SLIDE GỐC 1 – 8)
- **Phạm vi slide gốc:** Slide 1 đến Slide 8 (Toàn bộ Phần I - Giới thiệu).
- **Trọng tâm kiến thức:**
  1. *Tuần tự (Sequential):* Khái niệm, timeline tác vụ, thời gian thực thi là tổng thời gian của từng bước.
  2. *Đồng thời (Concurrency):* Nhiều tác vụ cùng tiến triển trong một khoảng thời gian, cơ chế chia sẻ thời gian (time-slicing), quan sát qua Process ID.
  3. *Song song (Parallelism):* Thực thi vật lý đồng thời trên nhiều lõi CPU độc lập (Multi-core), điều kiện phần cứng.
  4. *So sánh 3 mô hình:* Bảng và đồ thị phân biệt rõ ràng Tuần tự vs Đồng thời vs Song song.
  5. *Bất đồng bộ (Asynchronous):* Không chờ đợi I/O, ủy thác tác vụ, mô hình luồng đơn bất đồng bộ (Single-thread concurrent async execution model).
  6. *Ví dụ thực tế gốc:* Phân tích chuyên sâu ví dụ Bãi giữ xe và ví dụ Đi thi.
- **Sản phẩm bàn giao đã hoàn tất:**
  - `slides/TV1_BaiGiang_ChuanFileGoc_C4.pptx`: Phiên bản bài giảng chuẩn 100% bám sát 8 slide gốc (11 slides).
  - `slides/TV1_BaiGiang_TinhToanSongSong_PhanTan_C4_BaiGiangChinhThuc.pptx`: Phiên bản mở rộng chuyên sâu (24 slides) với sư phạm hoàn hảo.
  - `reports/TV1_BaoCao_ChiTiet_A_Z_PDC_Chuong4.docx` & `.pdf`: Báo cáo khoa học từ A-Z.
  - Bộ hình ảnh minh họa chất lượng cao trong `slides/images/`.

---

### THÀNH VIÊN 2 (TV2) — CONCURRENT.FUTURES & THREADPOOLEXECUTOR (SLIDE GỐC 9 – 12)
- **Phạm vi slide gốc:** Slide 9 đến Slide 12 (Phần II).
- **Trọng tâm kiến thức:**
  1. Module `concurrent.futures`: Kiến trúc cấp cao xử lý bất đồng bộ trong chuẩn Python.
  2. *Executor Objects & Future Objects:* Vòng đời của một đối tượng Future (PENDING, RUNNING, FINISHED, CANCELLED).
  3. *ThreadPoolExecutor:* Quản lý thread pool, tái sử dụng worker, thích hợp cho I/O-bound.
  4. Phương thức điều phối: `submit()`, `map()`, `as_completed()`, bắt lỗi exception từ Future.
- **Yêu cầu tinh gọn:** Tập trung vào cú pháp và luồng hoạt động trong slide gốc, tránh đi sâu vào lý thuyết race-condition phức tạp của hệ điều hành.

---

### THÀNH VIÊN 3 (TV3) — NHÓM TIẾN TRÌNH & PROCESSPOOLEXECUTOR (SLIDE GỐC 13 – 15)
- **Phạm vi slide gốc:** Slide 13 đến Slide 15 (Phần III).
- **Trọng tâm kiến thức:**
  1. *Khái niệm Nhóm tiến trình (Process Pool):* Bộ nhớ độc lập, an toàn cách ly dữ liệu.
  2. *ProcessPoolExecutor:* Giải pháp xử lý CPU-bound vượt qua Global Interpreter Lock (GIL) của CPython.
  3. Chi phí đánh đổi: Startup latency (chi phí sinh tiến trình con) và IPC serialization (Pickle overhead).
  4. Nguyên tắc tái sử dụng worker để tối ưu hóa hiệu năng tính toán.
- **Yêu cầu tinh gọn:** Tập trung vào sự khác biệt thực tế giữa ThreadPool và ProcessPool khi chạy CPU-bound.

---

### THÀNH VIÊN 4 (TV4) — ASYNCIO & QUẢN LÝ VÒNG LẶP SỰ KIỆN (SLIDE GỐC 16 – 19)
- **Phạm vi slide gốc:** Slide 16 đến Slide 19 (Phần IV).
- **Trọng tâm kiến thức:**
  1. Module `asyncio`: Thư viện chuẩn cho lập trình bất đồng bộ luồng đơn.
  2. *Mô hình Event Loop:* Khái niệm và nguyên lý hoạt động của vòng lặp sự kiện.
  3. Bộ ba thành phần: Event Source (nguồn sự kiện), Event Handler (trình xử lý sự kiện), Event Loop (bộ điều phối trung tâm).
  4. Coroutines và Tasks: Khai báo `async def`, toán tử `await`, tạo Task với `create_task()`.
- **Yêu cầu tinh gọn:** Giảng giải rõ mô hình tuần hoàn của Event loop theo đúng slide 17, 18 của slide gốc.

---

### THÀNH VIÊN 5 (TV5) — XỬ LÝ ĐỒNG THỜI VỚI ASYNCIO & PIPELINE (SLIDE GỐC 20 – 22)
- **Phạm vi slide gốc:** Slide 20 đến Slide 22 (Phần V).
- **Trọng tâm kiến thức:**
  1. So sánh chi tiết *Subroutine* (hàm truyền thống có 1 điểm vào, 1 điểm ra) và *Coroutine* (có thể tạm dừng và tiếp tục thực thi).
  2. Cơ chế *Yielding a value*: Tạm nhường quyền kiểm soát cho Event Loop khi chờ I/O.
  3. Xây dựng đường ống (Pipeline) xử lý dữ liệu đồng thời giữa các coroutines.
- **Yêu cầu tinh gọn:** Tập trung vào cơ chế nhường quyền và sơ đồ luồng điều khiển trong slide gốc.

---

### THÀNH VIÊN 6 (TV6) — LƯU Ý KHI CHỌN GIẢI PHÁP & TỔNG KẾT TOÀN CHƯƠNG (SLIDE GỐC 23 – 24)
- **Phạm vi slide gốc:** Slide 23 đến Slide 24 (Phần VI).
- **Trọng tâm kiến thức:**
  1. *Lưu ý quan trọng:* Khi nào nên dùng ThreadPool, khi nào dùng ProcessPool, khi nào dùng Asyncio.
  2. Các cạm bẫy cần tránh: Đưa blocking call vào Event Loop, lạm dụng ProcessPool cho bài toán quá nhỏ.
  3. Tổng kết toàn chương: Bảng so sánh tổng hợp các tiêu chí (Bộ nhớ, Đa lõi, Loại bài toán phù hợp, Độ phức tạp).
  4. Kết luận và định hướng áp dụng vào các hệ thống phân tán lớn hơn.
- **Yêu cầu tinh gọn:** Bám sát bảng kết luận và khuyến nghị của giảng viên ở slide 23 và 24.

---

## 4. TỔNG KẾT TRẠNG THÁI DỰ ÁN

| Thành viên | Trạng thái | Sản phẩm bàn giao chính |
|---|---|---|
| **TV1** | **HOÀN THÀNH XUẤT SẮC** | • Slide chuẩn gốc (`slides/TV1_BaiGiang_ChuanFileGoc_C4.pptx`)<br>• Slide bài giảng mở rộng (`slides/TV1_BaiGiang_TinhToanSongSong_PhanTan_C4_BaiGiangChinhThuc.pptx`)<br>• Báo cáo chi tiết (`reports/TV1_BaoCao_ChiTiet_A_Z_PDC_Chuong4.docx` & `.pdf`)<br>• Bộ sơ đồ minh họa gốc trong `slides/images/` |
| **TV2** | Sẵn sàng triển khai | Bám sát Slide gốc 9–12 (`concurrent.futures`, `ThreadPoolExecutor`) |
| **TV3** | Sẵn sàng triển khai | Bám sát Slide gốc 13–15 (`ProcessPoolExecutor`, GIL, quản lý tiến trình) |
| **TV4** | Sẵn sàng triển khai | Bám sát Slide gốc 16–19 (`asyncio`, Event Loop, Coroutines, Tasks) |
| **TV5** | Sẵn sàng triển khai | Bám sát Slide gốc 20–22 (Subroutine vs Coroutine, Yielding, Pipeline) |
| **TV6** | Sẵn sàng triển khai | Bám sát Slide gốc 23–24 (Lưu ý, so sánh tổng hợp, kết luận Chương 4) |
