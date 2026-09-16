# SƯỜN BÁO CÁO CHƯƠNG 4 — TÍNH TOÁN BẤT ĐỒNG BỘ

> **BẢN V1 LƯU TRỮ — KHÔNG DÙNG ĐỂ GIAO VIỆC MỚI.** Xem [phân công A–Z chính thức](02_PHAN_CONG_6_THANH_VIEN_A_Z.md) và [README](../README.md).

> Đây là **kế hoạch nội dung**, chưa phải PowerPoint hoàn chỉnh. Nhóm duyệt sườn, điền tên thành viên và thống nhất thời lượng trước khi thiết kế slide.

## 1. Kết quả đọc tài liệu gốc

Tài liệu `BaiGiang_TinhToanSongSong_PhanTan_C4.pdf` có 24 trang, chia thành bốn cụm:

1. Giới thiệu: tuần tự, đồng thời, song song, bất đồng bộ.
2. `concurrent.futures`: Executor, Future, ThreadPoolExecutor, ProcessPoolExecutor.
3. Quản lý vòng lặp sự kiện với `asyncio`.
4. Coroutine và xử lý nhiều tác vụ đồng thời.

Tài liệu gốc đủ để xác định phạm vi chương nhưng còn ngắn. Để người nghe hiểu cơ chế và trả lời phản biện, nhóm cần bổ sung nền tảng hệ điều hành, I/O-bound/CPU-bound, GIL, blocking/non-blocking, timeout, cancellation, giới hạn đồng thời và một demo có đo lường.

## 2. Mục tiêu bài báo cáo

Sau bài báo cáo, người nghe phải:

- phân biệt được sequential, concurrency, parallelism và asynchronous;
- không nhầm synchronous/asynchronous với blocking/non-blocking;
- hiểu process, thread, coroutine và event loop ở mức cơ chế;
- biết khi nào dùng ThreadPool, ProcessPool hoặc `asyncio`;
- hiểu vòng đời Future/Task, cách nhận kết quả, lỗi, timeout và hủy;
- chạy được một demo nhỏ và giải thích kết quả bằng bản chất workload.

## 3. Quy mô đề xuất

- 42 slide dự kiến, chia đều 7 slide cho 6 thành viên.
- 40–45 phút trình bày, 5 phút demo và 5–10 phút hỏi đáp.
- Slide chỉ giữ ý chính, sơ đồ, timeline và code ngắn.
- Phần giải thích đầy đủ sẽ đặt trong Speaker Notes hoặc kịch bản riêng sau khi sườn được duyệt.

## 4. Sườn chi tiết 42 slide

### Thành viên 1 — Đặt vấn đề và bản đồ khái niệm (slide 1–7)

1. Trang bìa: Chương 4 — Tính toán bất đồng bộ; tên môn, nhóm, giảng viên.
2. Tình huống mở đầu: chương trình phải chờ nhiều lời gọi mạng.
3. Câu hỏi trung tâm: làm gì trong khoảng CPU đang chờ I/O?
4. Mục tiêu học tập và những gì người nghe sẽ nắm được.
5. Bốn khái niệm: tuần tự, đồng thời, song song, bất đồng bộ.
6. Timeline minh họa bốn mô hình trên cùng một bài toán.
7. Ví dụ quán cà phê và câu hỏi kiểm tra nhanh để chuyển phần.

Điểm phải làm rõ: concurrent không mặc nhiên là parallel; async không tự động tạo thêm lõi CPU.

### Thành viên 2 — Nền tảng bắt buộc trước khi học async (slide 8–14)

8. Hai trục độc lập: sync/async và blocking/non-blocking.
9. Ma trận 2×2 kèm ví dụ cho từng trường hợp.
10. I/O-bound và CPU-bound: cách nhận diện.
11. Process: bộ nhớ riêng, IPC, khả năng dùng nhiều lõi.
12. Thread: bộ nhớ chung, race condition, lock và context switch.
13. Coroutine: thực thi hợp tác, tạm dừng tại `await`.
14. GIL của CPython và ma trận chọn process/thread/coroutine.

Điểm phải làm rõ: quyết định công cụ bắt đầu từ loại tải và API đang sử dụng, không bắt đầu từ sở thích cú pháp.

### Thành viên 3 — `concurrent.futures` (slide 15–21)

15. Vì sao cần API cấp cao `concurrent.futures`.
16. Kiến trúc Executor → hàng đợi → worker → kết quả.
17. Future là gì và vòng đời pending/running/finished/cancelled.
18. `submit`, `result`, `done`, `exception`, `cancel`, callback.
19. `map`, `wait`, `as_completed`: khác nhau về thứ tự nhận kết quả.
20. ThreadPoolExecutor cho I/O blocking; ví dụ và giới hạn worker.
21. ProcessPoolExecutor cho CPU-bound; pickle, IPC, `__main__` và overhead.

Điểm phải làm rõ: cùng một giao diện Executor nhưng thread và process có chi phí, bộ nhớ và cách song song khác nhau.

### Thành viên 4 — `asyncio` và event loop (slide 22–28)

22. Event loop là gì; ready queue và I/O watcher.
23. Một vòng event loop hoạt động như thế nào.
24. `async def`: gọi hàm tạo coroutine object, chưa chạy ngay.
25. `await`: tạm dừng hợp tác và trả quyền cho event loop.
26. Phân biệt coroutine, awaitable, Task và `asyncio.Future`.
27. `create_task` và `gather`: bắt đầu trước, chờ chung sau.
28. `TaskGroup` và structured concurrency; khác biệt với `gather`.

Điểm phải làm rõ: event loop thường chỉ chạy một đoạn Python tại một thời điểm; concurrency xuất hiện vì các coroutine nhường quyền khi chờ.

### Thành viên 5 — Xây chương trình async đúng và tin cậy (slide 29–35)

29. Timeout: deadline theo nghiệp vụ, không chờ vô hạn.
30. Cancellation: `CancelledError`, cleanup bằng `try/finally`.
31. Semaphore: giới hạn số thao tác đang chạy.
32. Queue và backpressure: producer nhanh hơn consumer.
33. Đưa hàm blocking ra khỏi loop bằng `asyncio.to_thread`.
34. Race condition, deadlock, task mồ côi và exception không được thu gom.
35. Checklist chọn mô hình và các lỗi thiết kế thường gặp.

Điểm phải làm rõ: tạo thật nhiều task không đồng nghĩa nhanh; một hệ thống tốt phải có giới hạn tải, vòng đời và đường đi của lỗi.

### Thành viên 6 — Demo, đánh giá và kết luận (slide 36–42)

36. Bài toán demo: trung tâm lấy dữ liệu từ 8 trạm cảm biến.
37. Yêu cầu và kiến trúc: cùng input/output, ba chiến lược I/O.
38. Phiên bản tuần tự và dự đoán thời gian chạy.
39. Phiên bản ThreadPool và `asyncio`; giải thích điểm khác nhau.
40. Benchmark I/O; bổ sung một phép tính CPU bằng ProcessPool.
41. Kết luận: chọn công cụ theo workload; câu hỏi kiểm tra cuối.
42. Tài liệu tham khảo và Q&A.

Điểm phải làm rõ: demo phải kiểm tra tính đúng trước khi so tốc độ; kết quả benchmark chỉ có ý nghĩa trên workload và máy cụ thể.

## 5. Đề xuất demo nhỏ

### Tên demo

**Trung tâm tổng hợp dữ liệu chất lượng không khí từ nhiều trạm**.

### Input

Danh sách 8 trạm; mỗi trạm có mã, quận, độ trễ mô phỏng, PM2.5 và nhiệt độ.

### Ba cách lấy dữ liệu

1. Tuần tự: dùng hàm blocking và chờ từng trạm.
2. ThreadPool: bốn worker chạy các lời gọi blocking.
3. `asyncio`: tám coroutine nhưng Semaphore chỉ cho bốn yêu cầu đang bay.

### Phần CPU bổ sung

Sau khi lấy dữ liệu, chạy một phép tính CPU thuần Python theo nhiều lô; so sánh tuần tự với ProcessPool. Mục đích là chứng minh không nên dùng một công cụ cho cả I/O-bound và CPU-bound.

### Tiêu chí demo

- chạy ngoại tuyến, không phụ thuộc Wi-Fi;
- ba phiên bản I/O trả cùng dữ liệu và thứ tự;
- có unit test;
- đo bằng `time.perf_counter`;
- có timeout và giới hạn đồng thời;
- lưu sẵn kết quả dự phòng nếu live demo gặp lỗi.

## 6. Phân công công việc ngoài lúc trình bày

| Thành viên | Vai trò chính | Sản phẩm chịu trách nhiệm |
|---|---|---|
| TV1 | Trưởng nhóm, kiểm soát mạch kể chuyện | Sườn cuối, mở bài, ghép nội dung, điều phối tập dượt |
| TV2 | Nghiên cứu nền tảng | Thuật ngữ, process/thread/coroutine, GIL, sơ đồ timeline |
| TV3 | Nghiên cứu `concurrent.futures` | Ví dụ Future, ThreadPool, ProcessPool, lỗi và deadlock |
| TV4 | Nghiên cứu `asyncio` cốt lõi | Event loop, coroutine, Task, gather, TaskGroup |
| TV5 | Độ tin cậy và phản biện | Timeout, cancellation, Semaphore, Queue, câu hỏi phản biện |
| TV6 | Kỹ thuật demo và GitHub | Mã demo, test, benchmark, hướng dẫn chạy và quản lý repository |

Mỗi thành viên phải review phần của một người khác. Giáo viên có thể hỏi chéo nên không thành viên nào chỉ học đúng bảy slide của mình.

## 7. Cấu trúc GitHub dự kiến

```text
chapter-4-async-computing/
├── README.md                     # giới thiệu đề tài và thành viên
├── docs/
│   ├── outline.md                # sườn 42 slide
│   ├── assignment.md             # phân công và deadline
│   ├── research-notes.md         # ghi chú nghiên cứu
│   └── references.md             # nguồn đã dùng
├── slides/
│   └── README.md                 # quy ước thiết kế; chưa có PPTX khi chưa duyệt
├── demo/
│   ├── README.md                 # đặc tả demo
│   ├── app.py                    # tạo sau khi duyệt demo
│   └── test_app.py
├── results/                      # benchmark sau khi code hoàn tất
└── assets/                       # hình/sơ đồ tự tạo, có nguồn rõ ràng
```

Không nên upload công khai nguyên bộ PDF bài giảng của giảng viên. Repository công khai chỉ chứa nội dung nhóm tự viết, mã demo và đường dẫn tham khảo.

## 8. Cách chia việc trên GitHub

- Tạo một Issue cho mỗi cụm slide và một Issue cho demo.
- Dùng nhãn: `research`, `slides`, `demo`, `review`, `blocked`.
- Mỗi thành viên làm trên nhánh riêng: `tv2/foundation`, `tv4/asyncio-core`.
- Pull Request phải có ít nhất một người khác review.
- Mốc 1: duyệt sườn; mốc 2: chốt nội dung; mốc 3: ghép slide; mốc 4: chạy demo; mốc 5: tập dượt.

## 9. Những quyết định nhóm cần chốt trước khi làm PPTX

1. Thời lượng giáo viên cho phép chính xác.
2. Họ tên/MSSV và thế mạnh của sáu thành viên.
3. Có giữ demo cảm biến hay đổi sang bài toán khác.
4. Phiên bản Python trên máy trình chiếu.
5. Repository public hay private và có được phép đưa tài liệu giảng viên lên hay không.
6. Phong cách slide: học thuật tối giản hay trực quan nhiều sơ đồ.

Sau khi sáu quyết định này được thống nhất mới chuyển sang viết nội dung hoàn chỉnh và thiết kế PowerPoint.
