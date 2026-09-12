# ĐỀ CƯƠNG BÁO CÁO CHƯƠNG 4

## TÍNH TOÁN BẤT ĐỒNG BỘ

Repository lập kế hoạch cho nhóm **6 thành viên**, học phần **Tính toán song song và phân tán**.


## Mục tiêu

Bài báo cáo phải giúp người nghe:

- phân biệt tuần tự, đồng thời, song song và bất đồng bộ;
- không nhầm synchronous/asynchronous với blocking/non-blocking;
- hiểu process, thread, coroutine, Future, Task và event loop;
- biết khi nào dùng ThreadPoolExecutor, ProcessPoolExecutor hoặc `asyncio`;
- hiểu timeout, cancellation, giới hạn đồng thời và backpressure;
- quan sát các khái niệm qua một demo thực tế nhỏ, có kiểm thử và benchmark.

## Thành viên và phần phụ trách

| Thành viên | Slide dự kiến | Nội dung chính |
|---|---:|---|
| TV1 – Trưởng nhóm | 1–7 | Đặt vấn đề và bản đồ khái niệm |
| TV2 | 8–14 | Nền tảng process, thread, coroutine, I/O-bound/CPU-bound và GIL |
| TV3 | 15–21 | `concurrent.futures`, Executor, Future và các pool |
| TV4 | 22–28 | `asyncio`, event loop, coroutine, Task và TaskGroup |
| TV5 | 29–35 | Timeout, cancellation, Semaphore, Queue và lỗi thường gặp |
| TV6 | 36–42 | Đặc tả demo, cách đánh giá, kết luận và tài liệu tham khảo |



## Tài liệu trong repository

```text
.
├── README.md
└── docs/
    ├── SUON_BAO_CAO_CHUONG_4.md
    ├── PHAN_CONG_6_THANH_VIEN.md
    └── PHAN_CONG_CHI_TIET_6_THANH_VIEN.md
```

- [`SUON_BAO_CAO_CHUONG_4.md`](docs/SUON_BAO_CAO_CHUONG_4.md): sườn chi tiết 42 slide, nền tảng cần nghiên cứu, đặc tả demo và cấu trúc dự án dự kiến.
- [`PHAN_CONG_6_THANH_VIEN.md`](docs/PHAN_CONG_6_THANH_VIEN.md): nhiệm vụ, thời lượng, đầu ra và cách phối hợp của từng người.
- [`PHAN_CONG_CHI_TIET_6_THANH_VIEN.md`](docs/PHAN_CONG_CHI_TIET_6_THANH_VIEN.md): nhiệm vụ dài và cụ thể cho từng thành viên, gồm nội dung từng slide, phần phải nghiên cứu, sản phẩm phải nộp, câu hỏi phản biện, tiêu chí hoàn thành, review chéo và lịch thực hiện.

## Demo dự kiến

**Trung tâm tổng hợp dữ liệu chất lượng không khí từ 8 trạm cảm biến**:

1. Chạy tuần tự để lấy mốc thời gian.
2. Dùng ThreadPool cho lời gọi I/O blocking.
3. Dùng `asyncio` và Semaphore cho I/O bất đồng bộ có giới hạn.
4. Bổ sung một phép tính CPU để so tuần tự với ProcessPool.
5. Kiểm tra các phiên bản trả cùng kết quả trước khi benchmark.

Demo phải chạy ngoại tuyến để không phụ thuộc Wi-Fi khi báo cáo.

## Các mốc thực hiện
- [ ] Duyệt sườn tính cỡ bao nhiêu slide và thời lượng báo cáo.
- [ ] Chốt bài toán demo.
- [ ] Chia nguồn nghiên cứu và deadline.
- [ ] Viết nội dung chi tiết từng phần.
- [ ] Review chéo giữa các thành viên.
- [ ] Thiết kế PowerPoint sau khi nội dung được duyệt.
- [ ] Viết, kiểm thử và benchmark demo.
- [ ] Tập dượt và chuẩn bị câu hỏi phản biện.

## Quy trình GitHub
1. Mỗi thành viên nhận một Issue tương ứng với phần được giao.
2. Làm việc trên nhánh riêng, ví dụ `tv3/concurrent-futures`.
3. Commit nhỏ, nêu rõ nội dung: `docs: bổ sung vòng đời Future`.
4. Mở Pull Request và nhờ ít nhất một thành viên khác review.
5. Không đưa trực tiếp thay đổi chưa duyệt vào nhánh `main`.
## Nguồn nghiên cứu chính

- Tài liệu Chương 4 do giảng viên cung cấp — chỉ dùng nội bộ, không upload lên repository công khai.
- [`concurrent.futures` — Python documentation](https://docs.python.org/3/library/concurrent.futures.html)
- [`asyncio` — Python documentation](https://docs.python.org/3/library/asyncio.html)
- [Coroutines and Tasks — Python documentation](https://docs.python.org/3/library/asyncio-task.html)
- [Event Loop — Python documentation](https://docs.python.org/3/library/asyncio-eventloop.html)
- [`threading` — Python documentation](https://docs.python.org/3/library/threading.html)

## Nguyên tắc

Repository công khai này chỉ lưu nội dung do nhóm tự xây dựng và liên kết tới nguồn tham khảo. Không đăng lại nguyên bộ slide/PDF của giảng viên khi chưa có sự cho phép.
