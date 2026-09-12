# PHÂN CÔNG NHÓM 6 THÀNH VIÊN

> Thay `TV1`…`TV6` bằng họ tên và MSSV. Phân công theo **mạch kiến thức**, không chỉ theo số slide: mỗi người chịu trách nhiệm trả lời câu hỏi thuộc phần mình.

## Phân chia khi thuyết trình

| Thành viên | Slide | Thời lượng | Trọng tâm trình bày | Đầu ra phải chuẩn bị |
|---|---:|---:|---|---|
| **TV1 – Trưởng nhóm** | 1–7 | 6 phút | Mở bài, mục tiêu, ví dụ quán cà phê, bốn khái niệm nền tảng | Học thuộc tình huống dẫn nhập; điều phối chuyển phần; kiểm tra bản cuối |
| **TV2 – Nền tảng & Future** | 8–14 | 7 phút | Hai trục phân loại, I/O-bound/CPU-bound, process/thread/coroutine, ma trận chọn công cụ, Executor–Future và `submit` | Vẽ lại cây quyết định; chuẩn bị 2 ví dụ phản biện; chạy thử Future |
| **TV3 – Pools & event loop** | 15–21 | 7 phút | `map`, ThreadPool, ProcessPool, GIL, lỗi/deadlock và cầu nối sang event loop | Giải thích được vì sao thread không tối ưu CPU-bound trong CPython thông thường; vẽ cơ chế event loop |
| **TV4 – `asyncio` cốt lõi** | 22–28 | 7 phút | Coroutine, awaitable, task, `async`/`await`, `create_task`, `gather`, `TaskGroup`, hai loại Future và Semaphore | Chuẩn bị hoạt họa coroutine; giải thích “concurrent không đồng nghĩa parallel” |
| **TV5 – Độ tin cậy & demo** | 29–35 | 7 phút | Queue/backpressure, timeout/cancel, `to_thread`, debug; yêu cầu, kiến trúc và ba phiên bản I/O của demo | Nêu được cơ chế chống quá tải; kiểm tra luồng dữ liệu và tính tương đương của demo |
| **TV6 – Demo & kết luận** | 36–42 | 8–10 phút | Mã demo, benchmark I/O, ProcessPool cho CPU, cách chạy, checklist chọn mô hình, tổng kết và nguồn | Chạy demo trên máy trình chiếu; giữ bản quay/dữ liệu dự phòng; chủ trì Q&A |

Tổng: khoảng **42–44 phút**, còn 5–8 phút cho hỏi đáp.

## Công việc trước ngày báo cáo

| Việc | Chủ trì | Phối hợp | Tiêu chí hoàn thành |
|---|---|---|---|
| Chuẩn hóa thuật ngữ tiếng Việt/Anh | TV2 | TV1, TV4 | Một thuật ngữ chỉ dùng một cách viết trong toàn bộ tài liệu |
| Đối chiếu tài liệu gốc Chương 4 | TV1 | TV3, TV4 | Không bỏ sót `concurrent.futures`, event loop, coroutine/task |
| Kiểm tra mã và test | TV6 | TV3, TV5 | `python -m unittest demo/test_app.py -v` báo `OK` |
| Chạy benchmark trên máy thuyết trình | TV6 | TV5 | Lưu JSON và chụp kết quả; giải thích được sai số |
| Rà soát nguồn/citation | TV4 | TV2 | Link mở được; phân biệt tài liệu Python hiện hành với bài giảng 2023 |
| Ghép slide, font, hiệu ứng | TV1 | Cả nhóm | Không tràn chữ; dùng font phổ biến; video/demo không phụ thuộc Internet |
| Chuẩn bị phản biện | Mỗi người | TV1 điều phối | Mỗi người trả lời được ít nhất 5 câu trong `CAU_HOI_PHAN_BIEN.md` |

## Quy tắc phối hợp trên GitHub

1. Mỗi thành viên tạo nhánh `tvN/ten-cong-viec`, ví dụ `tv3/futures`.
2. Commit nhỏ và rõ: `docs: bổ sung vòng đời Future`, `demo: thêm timeout`.
3. Không sửa trực tiếp nhánh `main`; mở Pull Request và nhờ ít nhất một người khác đọc.
4. Khi sửa nội dung slide, sửa dữ liệu trong `scripts/build_slides.py`, sinh lại `.pptx`, rồi commit cả hai.
5. Trước khi ghép: `git pull`, chạy test, chạy lại script tạo slide.

## Kịch bản bàn giao giữa các thành viên

- TV1 → TV2: “Ta đã có bốn cách tổ chức công việc. Muốn chọn đúng, cần nhìn thêm loại tải và đơn vị thực thi.”
- TV2 → TV3: “Với API cấp cao, Python thống nhất thread và process qua mô hình Executor–Future.”
- TV3 → TV4: “Pool giải quyết bằng worker hệ điều hành; còn `asyncio` tổ chức nhiều việc chờ trên event loop.”
- TV4 → TV5: “Tạo task thì dễ; làm hệ thống chịu lỗi, không quá tải mới là phần quan trọng.”
- TV5 → TV6: “Bây giờ ta kiểm chứng toàn bộ lựa chọn bằng hệ thống cảm biến thu nhỏ.”

## Checklist tập dượt

- Tập lần 1: đúng nội dung, chưa bấm giờ.
- Tập lần 2: bấm giờ từng người, cắt phần trùng lặp.
- Tập lần 3: dùng đúng máy/phòng dự kiến, chạy demo ngoại tuyến.
- Mỗi người phải tự nói lại được ba câu: “bài toán là gì”, “vì sao chọn mô hình này”, “đánh đổi là gì”.
- Chuẩn bị phương án B: ảnh/JSON benchmark có sẵn nếu máy trình chiếu không chạy Python.
