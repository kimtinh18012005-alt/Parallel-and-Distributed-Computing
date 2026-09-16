# PHÂN CÔNG CHI TIẾT NHÓM 6 THÀNH VIÊN

> **BẢN V1 LƯU TRỮ — KHÔNG DÙNG ĐỂ GIAO VIỆC MỚI.** Xem [phân công A–Z chính thức](02_PHAN_CONG_6_THANH_VIEN_A_Z.md) và [README](../README.md).

> Tài liệu này là **kế hoạch phân công để nhóm duyệt**, chưa phải nội dung PowerPoint hoàn chỉnh. Thay `TV1`…`TV6` bằng họ tên và MSSV sau khi thống nhất.

## 1. Nguyên tắc chia việc

Nhóm không chia việc theo kiểu “mỗi người tự làm vài slide rồi ghép lại”. Mỗi người phải sở hữu một **mạch kiến thức hoàn chỉnh**, có trách nhiệm:

1. nghiên cứu và đối chiếu tài liệu;
2. viết nội dung của phần mình;
3. đề xuất hình minh họa, sơ đồ hoặc đoạn code;
4. ghi rõ nguồn cho những nội dung lấy từ bên ngoài;
5. review phần của một thành viên khác;
6. trả lời được câu hỏi phản biện thuộc phần mình;
7. bàn giao mạch lạc cho người trình bày tiếp theo.

Các nhãn dùng trong tài liệu:

- **[Gốc C4]**: nội dung xuất hiện trực tiếp trong file Chương 4 của giảng viên.
- **[Nền tảng]**: kiến thức cần bổ sung để giải thích được nội dung gốc.
- **[Mở rộng]**: nội dung thực hành hiện đại giúp bài báo cáo đầy đủ hơn.
- **[Demo]**: nội dung gắn với bài toán minh họa của nhóm.

## 2. Bảng phân công tổng quát

| Thành viên | Slide dự kiến | Thời lượng | Mạch kiến thức sở hữu | Người review chéo |
|---|---:|---:|---|---|
| **TV1 – Trưởng nhóm** | 1–7 | 6–7 phút | Đặt vấn đề, mục tiêu và bản đồ khái niệm | TV4 |
| **TV2 – Nền tảng hệ thống** | 8–14 | 7 phút | Blocking, loại tải, process, thread, coroutine và GIL | TV5 |
| **TV3 – `concurrent.futures`** | 15–21 | 7–8 phút | Executor, Future, ThreadPool và ProcessPool | TV6 |
| **TV4 – `asyncio` cốt lõi** | 22–28 | 7–8 phút | Event loop, coroutine, awaitable, Task và TaskGroup | TV1 |
| **TV5 – Độ tin cậy** | 29–35 | 7–8 phút | Timeout, cancellation, giới hạn tải và lỗi thường gặp | TV2 |
| **TV6 – Demo và kết luận** | 36–42 | 8–10 phút | Đặc tả demo, benchmark, kết luận và Q&A | TV3 |

Tổng phần nói dự kiến: **43–48 phút**. Nếu giáo viên chỉ cho 30 phút, giữ các slide chính và chuyển ví dụ phụ sang phần dự phòng.

---

# THÀNH VIÊN 1 — TRƯỞNG NHÓM, ĐẶT VẤN ĐỀ VÀ KHÁI NIỆM

## 3.1. Mục tiêu của TV1

TV1 phải giúp lớp hiểu **vì sao Chương 4 tồn tại** trước khi nhìn thấy cú pháp Python. Sau phần này, người nghe phải phân biệt được tuần tự, đồng thời, song song và bất đồng bộ ở mức trực giác.

TV1 đồng thời là người kiểm soát mạch chung, bảo đảm sáu phần không lặp lại định nghĩa hoặc mâu thuẫn thuật ngữ.

## 3.2. Phạm vi phải nghiên cứu

- [Gốc C4] Trang 2–8: sequential, concurrency, parallel và asynchronous.
- [Nền tảng] Khái niệm task, khoảng thời gian và thời điểm thực thi.
- [Nền tảng] Ví dụ hệ điều hành xen kẽ nhiều công việc trên một lõi.
- [Nền tảng] Vì sao chờ I/O tạo ra thời gian CPU nhàn rỗi.
- [Mở rộng] Phân biệt “nhiều công việc cùng tiến triển” với “nhiều công việc chạy đúng cùng lúc”.

## 3.3. Nội dung từng slide

### Slide 1 — Trang bìa

- Tên chương: **Chương 4 — Tính toán bất đồng bộ**.
- Tên môn học, giảng viên, lớp, nhóm.
- Danh sách 6 thành viên và MSSV.
- Một câu định hướng ngắn: “Tận dụng khoảng chờ để công việc khác tiếp tục tiến triển”.

Không đưa định nghĩa dài lên trang bìa. TV1 chỉ giới thiệu bài báo cáo đi từ nền tảng → công cụ Python → demo.

### Slide 2 — Tình huống mở đầu

Đưa ra bài toán: chương trình phải lấy dữ liệu từ 8 trạm, mỗi trạm trả kết quả sau khoảng 0,3–0,6 giây.

TV1 hỏi lớp:

- Nếu gọi từng trạm một, tổng thời gian gần bằng bao nhiêu?
- Trong lúc chờ trạm thứ nhất, CPU có bắt buộc đứng yên không?
- Có thể bắt đầu các yêu cầu khác trước khi yêu cầu đầu hoàn tất không?

Mục đích slide này là tạo vấn đề, chưa đưa đáp án kỹ thuật.

### Slide 3 — Vì sao tuần tự có thể lãng phí thời gian

- Vẽ timeline gồm “chạy CPU” và “chờ I/O”.
- Chỉ ra phần lớn thời gian của ví dụ nằm ở chờ.
- Giải thích: tăng tốc không nhất thiết đến từ CPU nhanh hơn; có thể đến từ việc chồng lấp các khoảng chờ.
- Nêu điều kiện: nếu công việc không có khoảng chờ và hoàn toàn là tính toán CPU thì cách giải sẽ khác.

### Slide 4 — Mục tiêu học tập

Sau bài báo cáo, người nghe phải làm được:

1. phân biệt các mô hình;
2. nhận diện I/O-bound và CPU-bound;
3. hiểu `concurrent.futures`;
4. hiểu event loop và `asyncio`;
5. biết cách xử lý lỗi, timeout, hủy và giới hạn tải;
6. đọc được kết quả demo.

### Slide 5 — Tuần tự và đồng thời

- [Gốc C4] Tuần tự: hoàn tất A rồi mới bắt đầu B.
- [Gốc C4] Đồng thời: A và B cùng trong quá trình xử lý; có thể xen kẽ.
- Nêu ví dụ một đầu bếp xử lý nhiều món: lúc món A đang nướng, người đó chuẩn bị món B.
- Khẳng định: một hệ thống một lõi vẫn có thể có concurrency.

### Slide 6 — Song song và bất đồng bộ

- [Gốc C4] Song song: nhiều tác vụ thực thi đúng cùng thời điểm, thường nhờ nhiều lõi hoặc nhiều máy.
- [Gốc C4] Bất đồng bộ: yêu cầu được bắt đầu, kết quả đến sau; bên gọi có thể làm việc khác.
- Chỉ ra hai khái niệm có thể kết hợp nhưng không đồng nghĩa.
- Ví dụ: một event loop một thread có async/concurrency nhưng không thực thi hai đoạn Python cùng lúc.

### Slide 7 — Bảng tổng hợp và câu hỏi kiểm tra

Tạo bảng bốn hàng: tuần tự, đồng thời, song song, bất đồng bộ. Các cột:

- cách công việc tiến triển;
- có cần nhiều lõi không;
- có thể chồng thời gian chờ không;
- ví dụ thực tế.

Câu hỏi chuyển phần: “Muốn chọn đúng mô hình, ngoài bốn khái niệm này ta còn phải biết loại tải và đơn vị thực thi nào?”

## 3.4. Sản phẩm TV1 phải nộp

- Một bản mở bài khoảng 500–700 từ.
- Hai timeline: tuần tự và concurrent/async.
- Bảng thuật ngữ Việt–Anh dùng chung cho toàn nhóm.
- Danh sách nội dung trùng lặp cần loại bỏ khi ghép sáu phần.
- Bản agenda và thời lượng cuối cùng.
- Checklist kiểm tra tên, MSSV, số slide, font và nguồn.

## 3.5. Câu hỏi TV1 phải trả lời được

1. Concurrency và parallelism khác nhau ở đâu?
2. Bất đồng bộ có bắt buộc phải dùng nhiều thread không?
3. Một lõi CPU có thể xử lý concurrent bằng cách nào?
4. Bất đồng bộ có luôn nhanh hơn tuần tự không?
5. Trường hợp nào tuần tự là lựa chọn tốt hơn?

## 3.6. Tiêu chí hoàn thành

- Không dùng “đồng thời” và “song song” như hai từ đồng nghĩa.
- Mỗi thuật ngữ có một ví dụ và một phản ví dụ.
- Phần mở đầu không vượt quá 7 phút.
- Câu hỏi trung tâm của bài được nhắc lại ở phần kết luận.

## 3.7. Câu bàn giao cho TV2

“Ta đã phân biệt bốn cách tổ chức công việc. Nhưng để chọn được công cụ, cần biết chương trình đang chờ I/O hay bận tính CPU, và công việc được thực thi bằng process, thread hay coroutine.”

---

# THÀNH VIÊN 2 — NỀN TẢNG HỆ THỐNG

## 4.1. Mục tiêu của TV2

TV2 xây nền tảng để người nghe không xem `async` như một “từ khóa thần kỳ”. Sau phần này, lớp phải biết phân loại workload và hiểu sự khác nhau về chi phí, bộ nhớ, lịch thực thi giữa process, thread và coroutine.

## 4.2. Phạm vi phải nghiên cứu

- [Nền tảng] Synchronous/asynchronous và blocking/non-blocking.
- [Nền tảng] I/O-bound và CPU-bound.
- [Gốc C4] Process, task và việc hệ điều hành điều phối chương trình.
- [Nền tảng] Process, thread, chia sẻ bộ nhớ, context switch.
- [Gốc C4] Coroutine có thể tạm dừng và tiếp tục.
- [Mở rộng] GIL trong CPython và điều kiện áp dụng của nhận định về GIL.

## 4.3. Nội dung từng slide

### Slide 8 — Hai trục không được trộn lẫn

Trục thứ nhất: **synchronous ↔ asynchronous**, trả lời “kết quả được nhận khi nào và luồng điều khiển được tổ chức ra sao?”.

Trục thứ hai: **blocking ↔ non-blocking**, trả lời “thread có bị giữ trong lúc chờ không?”.

TV2 phải giải thích rằng async thường kết hợp với non-blocking nhưng hai từ này không phải định nghĩa của nhau.

### Slide 9 — Ma trận sync/async và blocking/non-blocking

Đưa bốn ô minh họa:

- sync + blocking: gọi `time.sleep` hoặc đọc file theo cách blocking;
- sync + non-blocking: thử đọc socket rồi nhận thông báo chưa có dữ liệu;
- async + blocking worker: đưa hàm blocking sang ThreadPool;
- async + non-blocking: event loop theo dõi socket và tiếp tục task khi sẵn sàng.

Đây là slide nền tảng mở rộng, phải nói ngắn và có ví dụ thay vì định nghĩa trừu tượng.

### Slide 10 — I/O-bound và CPU-bound

- I/O-bound: phần lớn thời gian chờ mạng, ổ đĩa, database hoặc thiết bị.
- CPU-bound: phần lớn thời gian tính toán.
- Chỉ dấu quan sát: CPU thấp nhưng latency cao so với CPU/lõi bận cao.
- Cùng một ứng dụng có thể có cả hai tầng.

Ví dụ: tải 1.000 ảnh là I/O-bound; resize các ảnh sau khi tải có thể CPU-bound.

### Slide 11 — Process

- Có không gian bộ nhớ riêng.
- Được hệ điều hành lập lịch.
- Có thể chạy trên nhiều lõi.
- Cách ly lỗi và trạng thái tốt hơn thread.
- Đổi lại phải trả chi phí tạo process, IPC và chuyển dữ liệu.

TV2 chưa đi sâu vào ProcessPool; phần đó thuộc TV3.

### Slide 12 — Thread

- Nhiều thread trong một process chia sẻ bộ nhớ.
- Chuyển dữ liệu thuận tiện nhưng có race condition.
- Hệ điều hành có thể chuyển lịch giữa các thread.
- Thread hữu ích khi một thread phải chờ I/O blocking.
- Quá nhiều thread làm tăng bộ nhớ và context switch.

### Slide 13 — Coroutine

- Coroutine là đơn vị thực thi hợp tác ở mức ngôn ngữ.
- Có thể tạm dừng tại `await`, giữ lại trạng thái cục bộ và tiếp tục từ điểm đã dừng.
- Nhẹ hơn thread vì không phải mỗi coroutine là một kernel thread.
- Nếu chạy code blocking hoặc CPU dài mà không nhường quyền, event loop bị chặn.

### Slide 14 — GIL và ma trận chọn công cụ

Phần GIL phải nói có điều kiện:

- trong bản CPython thông thường, GIL khiến tại một thời điểm chỉ một thread chạy Python bytecode;
- thread vẫn hữu ích cho I/O-bound;
- extension native có thể nhả GIL;
- Python hiện đại có free-threaded build tùy chọn nhưng không phải giả định mặc định của bài.

Kết thúc bằng ma trận:

| Bài toán | Lựa chọn đầu tiên |
|---|---|
| I/O blocking, số lượng vừa phải | ThreadPool |
| I/O async, nhiều kết nối | `asyncio` |
| CPU-bound thuần Python | ProcessPool |
| Task quá nhỏ | Tuần tự hoặc gom batch |

## 4.4. Sản phẩm TV2 phải nộp

- Bảng định nghĩa sync/async và blocking/non-blocking.
- Sơ đồ process–thread–coroutine.
- Bảng so sánh bộ nhớ, bộ lập lịch, chi phí và trường hợp dùng.
- Một đoạn giải thích GIL khoảng 200–300 từ, có điều kiện và nguồn.
- Ba ví dụ workload để lớp tự phân loại.
- Danh sách thuật ngữ cần TV1 chuẩn hóa.

## 4.5. Câu hỏi TV2 phải trả lời được

1. Async và non-blocking có hoàn toàn giống nhau không?
2. Tại sao gọi một hàm blocking trong coroutine có thể làm treo cả loop?
3. Thread và process khác nhau về bộ nhớ thế nào?
4. Vì sao thread vẫn tốt cho I/O-bound dù có GIL?
5. Vì sao task quá nhỏ có thể chạy song song chậm hơn tuần tự?
6. Free-threaded Python có làm mọi lời khuyên về GIL mất hiệu lực không?

## 4.6. Tiêu chí hoàn thành

- Không nói “Python không hỗ trợ đa luồng”.
- Không nói “I/O-bound lúc nào cũng dùng asyncio”.
- Mọi khuyến nghị đều có điều kiện về workload và thư viện.
- Ma trận chọn công cụ phải thống nhất với phần demo của TV6.

## 4.7. Câu bàn giao cho TV3

“Với API blocking hoặc công việc CPU độc lập, Python cung cấp một giao diện cấp cao để gửi việc cho thread/process và nhận kết quả tương lai: `concurrent.futures`.”

---

# THÀNH VIÊN 3 — `CONCURRENT.FUTURES`

## 5.1. Mục tiêu của TV3

TV3 chịu trách nhiệm phần công cụ đầu tiên xuất hiện trực tiếp trong bài giảng. Sau phần này, người nghe phải hiểu mô hình Executor–Future, đọc được đoạn code cơ bản và chọn ThreadPool/ProcessPool đúng trường hợp.

## 5.2. Phạm vi phải nghiên cứu

- [Gốc C4] Module `concurrent.futures` và mục đích của API cấp cao.
- [Gốc C4] Executor, `submit`, `map`, `shutdown`.
- [Gốc C4] Future và các phương thức `cancel`, `cancelled`, `running`, `done`, `result`, `exception`, `add_done_callback`.
- [Gốc C4] ThreadPoolExecutor và ProcessPoolExecutor.
- [Gốc C4] Ý tưởng tái sử dụng worker trong pool.
- [Mở rộng] `as_completed`, timeout, lỗi, deadlock và chi phí pickle/IPC.

Lưu ý: tên module chính xác là `concurrent.futures`, có chữ **s**.

## 5.3. Nội dung từng slide

### Slide 15 — Vì sao cần `concurrent.futures`

- API cấp cao, có từ Python 3.2.
- Che bớt chi tiết tạo/quản lý thread và process thủ công.
- Cung cấp giao diện chung cho việc gửi callable và nhận kết quả.
- Hai lớp trọng tâm của phạm vi môn: ThreadPoolExecutor và ProcessPoolExecutor.

### Slide 16 — Kiến trúc Executor

Sơ đồ đề xuất:

`Hàm + tham số → submit/map → hàng đợi → worker pool → Future/kết quả`

Giải thích trách nhiệm:

- chương trình chính mô tả công việc;
- Executor quản lý hàng đợi và worker;
- worker thực thi;
- Future đại diện cho kết quả chưa có hoặc đã có.

### Slide 17 — Vòng đời Future

Các trạng thái:

1. pending: đang chờ worker;
2. running: đã bắt đầu;
3. finished: kết thúc bằng kết quả hoặc exception;
4. cancelled: bị hủy trước khi chạy.

Điểm phải nhấn mạnh:

- `done()` không có nghĩa task thành công;
- `cancel()` thường không hủy được task đã chạy;
- `result()` là nơi lấy giá trị hoặc nhận lại exception.

### Slide 18 — `submit` và xử lý từng Future

Code dự kiến:

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    future = executor.submit(fetch, station)
    result = future.result(timeout=2)
```

Giải thích từng dòng, không chỉ chiếu code. Cho thấy main nhận Future trước khi công việc hoàn tất.

### Slide 19 — `map`, `wait` và `as_completed`

- `map`: gọn, áp dụng cùng hàm cho nhiều input, kết quả theo thứ tự input.
- `as_completed`: Future nào xong trước được xử lý trước.
- `wait`: chờ theo điều kiện như tất cả hoàn tất hoặc task đầu tiên hoàn tất.
- Khi cần gắn task với metadata, dùng dict `Future → context`.

TV3 phải chuẩn bị một timeline cho thấy thứ tự submit, thứ tự hoàn tất và thứ tự trả kết quả có thể khác nhau.

### Slide 20 — ThreadPoolExecutor

- Dùng nhiều thread trong cùng process.
- Hợp với lời gọi I/O blocking độc lập.
- Worker được tái sử dụng, giảm chi phí tạo/hủy thread liên tục.
- Số worker phải giới hạn theo connection pool, rate limit và tài nguyên.
- Rủi ro: trạng thái chia sẻ, race condition, deadlock và quá nhiều thread.

Liên hệ demo: lấy dữ liệu từ 8 trạm bằng 4 worker.

### Slide 21 — ProcessPoolExecutor

- Mỗi worker là một process riêng.
- Có thể dùng nhiều lõi cho CPU-bound Python.
- Input/output phải truyền qua IPC và thường phải pickle được.
- Task phải đủ lớn để bù overhead.
- Trên Windows cần bảo vệ entry point bằng `if __name__ == "__main__":`.

Liên hệ demo: chia 6 job tính toán cho tối đa 4 process.

## 5.4. Nội dung thực hành TV3 phải chuẩn bị

TV3 viết hai ví dụ tối giản, chưa cần là demo chính:

1. ThreadPool chạy 4 hàm `sleep` khác độ trễ và in thứ tự hoàn tất.
2. ProcessPool chạy 4 phép tính CPU độc lập.

Mỗi ví dụ phải có:

- phiên bản tuần tự;
- phiên bản pool;
- kiểm tra hai phiên bản trả cùng kết quả;
- đo thời gian bằng `perf_counter`;
- xử lý exception;
- chú thích lý do chọn executor.

## 5.5. Sản phẩm TV3 phải nộp

- Sơ đồ Executor–Future.
- State diagram của Future.
- Bảng `submit`/`map`/`as_completed`.
- Hai đoạn code thực hành ngắn.
- Danh sách ít nhất bốn lỗi thường gặp.
- Nguồn chính thức cho từng API được nhắc tới.
- Review phần demo CPU của TV6.

## 5.6. Câu hỏi TV3 phải trả lời được

1. `submit` trả về gì và trả về lúc nào?
2. `map` có phát kết quả theo thứ tự hoàn tất không?
3. Exception trong worker đi đâu?
4. `cancel()` có dừng được task đang chạy không?
5. Vì sao ProcessPool yêu cầu dữ liệu pickle được?
6. Vì sao ProcessPool có thể chậm hơn tuần tự?
7. Deadlock xảy ra thế nào khi một worker chờ Future trong cùng pool?

## 5.7. Tiêu chí hoàn thành

- Ví dụ chạy được trên Windows và Python 3.11+.
- Không đánh đồng Future của `concurrent.futures` với `asyncio.Future`.
- Code có context manager hoặc shutdown rõ ràng.
- Benchmark chỉ được trình bày sau khi xác nhận output giống nhau.

## 5.8. Câu bàn giao cho TV4

“Executor dùng worker thread hoặc process để chạy callable. Với số lượng lớn thao tác I/O có API non-blocking, Python còn có một mô hình khác: nhiều coroutine được event loop điều phối.”

---

# THÀNH VIÊN 4 — `ASYNCIO` CỐT LÕI

## 6.1. Mục tiêu của TV4

TV4 phải làm rõ cơ chế event loop và mối quan hệ giữa coroutine, awaitable, Task và Future. Sau phần này, người nghe phải đọc được chương trình `async` cơ bản và giải thích tại sao các task có thể cùng tiến triển trên một thread.

## 6.2. Phạm vi phải nghiên cứu

- [Gốc C4] Event source, event handler/callback và event loop.
- [Gốc C4] Vai trò của event loop trong toàn bộ thời gian chạy.
- [Gốc C4] `asyncio` dùng cú pháp `async`/`await`.
- [Gốc C4] Coroutine, Future và Task.
- [Gốc C4] Coroutine có thể tạm dừng và tiếp tục.
- [Mở rộng] `asyncio.run`, `create_task`, `gather` và TaskGroup.

## 6.3. Nội dung từng slide

### Slide 22 — Event loop là gì

Mô tả ở mức khái niệm:

- event loop giữ hàng đợi task/callback sẵn sàng;
- theo dõi timer, socket và sự kiện I/O;
- gọi handler/task tương ứng khi sự kiện hoàn tất;
- lặp lại trong suốt vòng đời chương trình.

Nối với ví dụ gốc về bàn phím/chuột, sau đó mở rộng sang mạng và timer.

### Slide 23 — Một vòng event loop hoạt động thế nào

Sơ đồ bốn bước:

1. lấy task từ ready queue;
2. chạy đến khi hoàn tất hoặc gặp `await`;
3. đăng ký đối tượng đang chờ với hệ điều hành;
4. khi sự kiện sẵn sàng, đưa task trở lại queue.

TV4 phải nói rõ event loop không “đoán” chỗ dừng; coroutine nhường quyền tại điểm await.

### Slide 24 — Coroutine và `async def`

- `async def` khai báo coroutine function.
- Gọi coroutine function tạo coroutine object nhưng chưa chạy thân hàm ngay.
- Coroutine object phải được `await` hoặc lập lịch thành Task.
- Nếu tạo rồi bỏ quên, chương trình có thể cảnh báo “coroutine was never awaited”.

### Slide 25 — `await`

- Chỉ dùng trong coroutine.
- Tạm dừng coroutine hiện tại khi awaitable chưa hoàn tất.
- Trả quyền cho event loop để chạy task khác.
- Khi kết quả sẵn sàng, coroutine tiếp tục từ đúng điểm đã dừng.
- `await` không tự tạo thread mới.

So sánh `await asyncio.sleep(...)` với `time.sleep(...)` trong event loop.

### Slide 26 — Coroutine, awaitable, Task và Future

Tạo bảng bốn hàng:

| Đối tượng | Vai trò |
|---|---|
| Coroutine object | computation có thể được await |
| Awaitable | giao diện chung cho đối tượng dùng được với await |
| Task | wrapper đã lập lịch coroutine trên loop |
| `asyncio.Future` | đại diện kết quả tương lai ở mức loop/thư viện |

TV4 phải chỉ ra `Task` là Future chuyên quản lý coroutine, nhưng code ứng dụng thường không tự tạo Future mức thấp.

### Slide 27 — `create_task` và `gather`

Mẫu code:

```python
tasks = [asyncio.create_task(fetch(x)) for x in items]
results = await asyncio.gather(*tasks)
```

Giải thích:

- tạo task trước để nhiều fetch cùng tiến triển;
- `gather` chờ nhóm awaitable;
- danh sách kết quả giữ thứ tự đầu vào;
- thứ tự hoàn tất thực tế có thể khác;
- phải hiểu hành vi khi một task lỗi.

### Slide 28 — TaskGroup và structured concurrency

- TaskGroup có từ Python 3.11.
- Nhóm các task có cùng phạm vi sống.
- Khi rời `async with`, toàn bộ task đã kết thúc.
- Một task lỗi dẫn đến hủy các task anh em và tổng hợp lỗi.
- So sánh với `gather` nhưng không khẳng định TaskGroup thay thế mọi trường hợp.

Nội dung này là mở rộng hiện đại, không phải trọng tâm trực tiếp của slide giảng viên năm 2023.

## 6.4. Minh họa TV4 phải chuẩn bị

- Một sơ đồ event loop gồm ready queue, coroutine, I/O watcher và completion event.
- Một timeline ba coroutine A/B/C xen kẽ tại `await`.
- Một đoạn code cố tình dùng `time.sleep` trong coroutine để giải thích loop bị block.
- Một đoạn code đúng dùng `asyncio.sleep`.

Không cần chạy đoạn code lỗi trong lúc báo cáo; có thể dùng hình timeline.

## 6.5. Sản phẩm TV4 phải nộp

- Sơ đồ event loop có chú thích.
- Bảng phân biệt coroutine/awaitable/Task/Future.
- Hai đoạn code nhỏ: await tuần tự và tạo task concurrent.
- Bảng so sánh `gather` với TaskGroup.
- Review phần thuật ngữ của TV1 để bảo đảm không mâu thuẫn.
- Danh sách nguồn chính thức của `asyncio`.

## 6.6. Câu hỏi TV4 phải trả lời được

1. Gọi một hàm `async def` có chạy ngay không?
2. `await` có tạo thread không?
3. Event loop biết khi nào tiếp tục coroutine bằng cách nào?
4. Coroutine khác Task ra sao?
5. `gather` giữ thứ tự đầu vào hay thứ tự hoàn tất?
6. TaskGroup khác `gather` ở bảo đảm lỗi và vòng đời thế nào?
7. Vì sao `time.sleep` gây hại khi chạy trên event-loop thread?

## 6.7. Tiêu chí hoàn thành

- Sơ đồ phải cho thấy rõ “run → await → chờ I/O → ready → resume”.
- Không nói nhiều coroutine chạy Python song song trên cùng một event loop.
- Không mô tả `await` như lời gọi làm chương trình đứng im.
- Phân biệt được `asyncio.Future` và `concurrent.futures.Future`.

## 6.8. Câu bàn giao cho TV5

“Tạo nhiều task chỉ là bước đầu. Một chương trình bất đồng bộ dùng được trong thực tế còn phải giới hạn tải, đặt timeout, xử lý hủy và thu gom mọi lỗi.”

---

# THÀNH VIÊN 5 — ĐỘ TIN CẬY VÀ KIỂM SOÁT TẢI

## 7.1. Mục tiêu của TV5

TV5 biến phần lý thuyết thành tư duy thiết kế hệ thống. Sau phần này, người nghe phải hiểu “càng nhiều task càng tốt” là sai và biết những cơ chế tối thiểu để chương trình async không chờ vô hạn, không quá tải và không làm thất lạc lỗi.

## 7.2. Phạm vi phải nghiên cứu

- [Mở rộng] Timeout và deadline.
- [Mở rộng] Task cancellation và `CancelledError`.
- [Mở rộng] `asyncio.Semaphore`.
- [Mở rộng] `asyncio.Queue` và backpressure.
- [Mở rộng] `asyncio.to_thread` và cầu nối với code blocking.
- [Nền tảng] Race condition, deadlock, starvation và task mồ côi.
- [Gốc C4] Ý nghĩa của việc quản lý task, synchronization và event loop.

Phần này mở rộng từ ý “quản lý tác vụ, luồng và đồng bộ hóa” của bài giảng; phải trình bày như kiến thức giúp vận dụng, không nói rằng mọi API đều xuất hiện trong file gốc.

## 7.3. Nội dung từng slide

### Slide 29 — Timeout và deadline

- Không chờ một dịch vụ vô hạn.
- Timeout phải xuất phát từ yêu cầu nghiệp vụ.
- Phân biệt timeout cho một thao tác và deadline cho cả chuỗi thao tác.
- Dùng `asyncio.timeout(...)` hoặc timeout của thư viện I/O.
- Khi timeout xảy ra cần log context và giải phóng tài nguyên.

### Slide 30 — Cancellation

- `task.cancel()` yêu cầu task hủy, không phải kill ngay lập tức.
- `CancelledError` xuất hiện ở cơ hội tiếp theo, thường tại `await`.
- Dọn tài nguyên trong `try/finally`.
- Nếu bắt `CancelledError`, thông thường phải ném lại sau cleanup.
- Code blocking hoặc CPU dài phản ứng hủy chậm.

### Slide 31 — Semaphore và giới hạn đồng thời

Ví dụ: có 1.000 trạm nhưng API chỉ cho 20 kết nối đồng thời.

```python
sem = asyncio.Semaphore(20)

async def bounded_fetch(item):
    async with sem:
        return await fetch(item)
```

Giải thích số task được tạo có thể lớn hơn số thao tác thật sự đang bay.

### Slide 32 — Queue và backpressure

- Producer tạo dữ liệu.
- Queue làm vùng đệm.
- Consumer xử lý theo năng lực.
- `Queue(maxsize=N)` khiến producer phải chờ khi hàng đợi đầy.
- Nhờ đó RAM và latency không tăng vô hạn.

TV5 phải đưa một ví dụ: đọc sensor nhanh nhưng ghi database chậm.

### Slide 33 — Đưa code blocking ra khỏi event loop

- Không gọi trực tiếp hàm blocking lâu trên loop thread.
- Với I/O blocking ngắn: `await asyncio.to_thread(...)`.
- Với CPU-bound lớn: dùng process pool hoặc service riêng.
- `to_thread` giữ event loop phản hồi nhưng không biến thuật toán CPU thuần Python thành nhanh hơn.

### Slide 34 — Các lỗi thiết kế thường gặp

Ít nhất sáu lỗi:

1. tạo task không giới hạn;
2. quên await coroutine;
3. không giữ reference tới background task;
4. nuốt exception hoặc `CancelledError`;
5. gọi code blocking trong loop;
6. nhiều task sửa chung trạng thái mà không đồng bộ;
7. retry vô hạn không backoff;
8. dùng thread/process cho task quá nhỏ.

### Slide 35 — Checklist thiết kế

Đặt sáu câu hỏi:

1. Kết quả có đúng không?
2. Workload là I/O hay CPU?
3. API blocking hay async?
4. Giới hạn worker/task/kết nối là bao nhiêu?
5. Timeout, hủy, retry và exception đi đâu?
6. Đo latency, throughput, CPU và RAM thế nào?

Slide này là cầu nối trực tiếp sang demo.

## 7.4. Tình huống phản biện TV5 phải chuẩn bị

### Tình huống A — 10.000 task cùng lúc

Giải thích vì sao tạo 10.000 task có thể tăng RAM, số connection và timeout. Đề xuất Semaphore, Queue hoặc xử lý theo batch.

### Tình huống B — Một task lỗi trong nhóm

So sánh cách quản lý bằng `gather` và TaskGroup; giải thích cách lỗi được truyền ra.

### Tình huống C — Người dùng đóng ứng dụng

Các task đang chạy phải nhận cancellation, dọn file/socket và kết thúc trong deadline.

## 7.5. Sản phẩm TV5 phải nộp

- Sơ đồ Queue/backpressure.
- Code Semaphore ngắn.
- Code timeout/cancellation có `try/finally`.
- Checklist tám lỗi thiết kế.
- Danh sách metric cần đo: latency, throughput, loop lag, task count, CPU và RAM.
- Review phần phân loại workload của TV2.
- Cùng TV6 xác định giới hạn concurrency trong demo.

## 7.6. Câu hỏi TV5 phải trả lời được

1. Hủy task có xảy ra ngay không?
2. Vì sao không nên nuốt `CancelledError`?
3. Semaphore khác Queue ở mục đích gì?
4. Backpressure là gì?
5. `to_thread` dùng khi nào?
6. Vì sao một hàm `async def` vẫn có thể block event loop?
7. Có nên tạo một task cho mọi input ngay từ đầu không?

## 7.7. Tiêu chí hoàn thành

- Mỗi cơ chế phải gắn với một lỗi mà nó giải quyết.
- Không đưa quá nhiều API mà thiếu giải thích cơ chế.
- Code ví dụ có cleanup rõ ràng.
- Phần này không vượt quá 8 phút; chi tiết phụ đưa vào câu hỏi phản biện.

## 7.8. Câu bàn giao cho TV6

“Các nguyên tắc vừa nêu sẽ được kiểm chứng trên một bài toán nhỏ: lấy dữ liệu từ nhiều trạm, so ba cách xử lý I/O và đối chiếu với một bước tính toán CPU.”

---

# THÀNH VIÊN 6 — ĐẶC TẢ DEMO, ĐÁNH GIÁ VÀ KẾT LUẬN

## 8.1. Mục tiêu của TV6

TV6 chưa cần viết demo ngay ở giai đoạn duyệt sườn. Nhiệm vụ hiện tại là viết **đặc tả đủ rõ** để sau khi nhóm duyệt, bất kỳ thành viên nào cũng biết demo phải làm gì, đo gì và chứng minh điều gì.

Khi chuyển sang giai đoạn triển khai, TV6 là người tích hợp mã, test, benchmark và chuẩn bị phương án trình diễn dự phòng.

## 8.2. Bài toán demo đề xuất

**Trung tâm tổng hợp dữ liệu chất lượng không khí từ 8 trạm cảm biến.**

Mỗi trạm có:

- mã trạm;
- quận/khu vực;
- độ trễ phản hồi mô phỏng;
- PM2.5;
- nhiệt độ.

Demo mô phỏng I/O bằng độ trễ cố định để chạy ngoại tuyến. Không sử dụng dữ liệu này cho quyết định sức khỏe thực tế.

## 8.3. Nội dung từng slide

### Slide 36 — Bài toán và yêu cầu

- Lấy dữ liệu từ 8 trạm.
- Mỗi trạm mất khoảng 0,25–0,65 giây để phản hồi.
- Chuẩn hóa thành cùng cấu trúc Reading.
- Đếm số trạm ở mức cảnh báo.
- So sánh ba cách lấy dữ liệu.
- Không phụ thuộc Internet.

### Slide 37 — Kiến trúc demo

Sơ đồ:

`Danh sách trạm → tầng lấy dữ liệu → chuẩn hóa → tổng hợp kết quả → benchmark`

Tầng lấy dữ liệu có ba implementation:

1. tuần tự;
2. ThreadPool;
3. `asyncio` có Semaphore.

Ba implementation phải có cùng input/output để so sánh công bằng.

### Slide 38 — Phiên bản tuần tự

- Gọi `fetch_station` theo vòng lặp.
- Tổng thời gian gần bằng tổng latency của tám trạm.
- Dùng làm baseline.
- In dữ liệu theo thứ tự danh sách trạm.
- Kiểm tra lỗi từng trạm.

TV6 yêu cầu lớp dự đoán runtime trước khi chạy.

### Slide 39 — ThreadPool và `asyncio`

ThreadPool:

- 4 worker;
- bọc lời gọi blocking;
- dùng `submit`/`as_completed` hoặc `map` tùy mục đích.

`asyncio`:

- coroutine dùng `await asyncio.sleep` để mô phỏng I/O;
- Semaphore giới hạn 4 thao tác đang bay;
- timeout cho mỗi trạm;
- `gather` hoặc TaskGroup quản lý nhóm task.

Slide phải giải thích cơ chế, không đặt hai khối code dài cạnh nhau.

### Slide 40 — Benchmark và phần CPU

Đo:

- thời gian tuần tự;
- thời gian ThreadPool;
- thời gian `asyncio`;
- speedup so với baseline.

Bổ sung 4–6 job tính toán CPU thuần Python:

- chạy tuần tự;
- chạy ProcessPool;
- kiểm tra cùng kết quả;
- giải thích overhead nên speedup không tuyến tính theo số worker.

### Slide 41 — Kết luận từ demo

- I/O có khoảng chờ → concurrency che được latency.
- API blocking → ThreadPool là cầu nối thực dụng.
- API async end-to-end → `asyncio` kiểm soát nhiều kết nối tốt.
- CPU-bound → ProcessPool hoặc giải pháp native phù hợp hơn.
- Không có công cụ thắng cho mọi workload.
- Benchmark phải kèm điều kiện máy và cấu hình.

### Slide 42 — Tài liệu tham khảo và Q&A

Nguồn bắt buộc:

- file bài giảng Chương 4 của giảng viên;
- Python documentation cho `concurrent.futures`;
- Python documentation cho `asyncio`, Task và event loop;
- Python documentation cho `threading`/GIL.

Kết thúc bằng câu hỏi: “Bài toán của bạn đang chờ I/O hay bận tính CPU?”

## 8.4. Đặc tả kỹ thuật demo sau khi được duyệt

### Các lệnh dự kiến

```bash
python demo/app.py compare-io
python demo/app.py compare-cpu
python -m unittest demo/test_app.py -v
```

### Test bắt buộc

1. Hàm phân loại dữ liệu đúng ở giá trị biên.
2. Ba mô hình I/O trả cùng nội dung.
3. Thứ tự output đúng contract.
4. Phiên bản CPU tuần tự và ProcessPool trả cùng kết quả.
5. Timeout được xử lý đúng.
6. Không còn task/process bị bỏ lại khi chương trình kết thúc.

### Số liệu phải lưu

- phiên bản Python;
- hệ điều hành;
- số lõi CPU;
- số worker/concurrency limit;
- số task;
- thời gian của từng lần chạy;
- trung vị của ít nhất ba lần nếu dùng cho kết luận;
- ghi chú tải nền của máy.

## 8.5. Kịch bản live demo

1. Mở terminal sẵn tại thư mục dự án.
2. Chạy test trước để chứng minh tính đúng.
3. Chạy phiên bản tuần tự và hỏi lớp dự đoán.
4. Chạy ThreadPool và `asyncio`.
5. So sánh số liệu, không tuyên bố asyncio luôn nhanh hơn.
6. Chạy CPU tuần tự/ProcessPool nếu còn thời gian.
7. Nếu demo lỗi, mở kết quả benchmark đã lưu và giải thích trung thực.

## 8.6. Sản phẩm TV6 phải nộp

Ở giai đoạn duyệt sườn:

- đặc tả bài toán;
- sơ đồ kiến trúc;
- danh sách command;
- danh sách test;
- mẫu bảng benchmark;
- kế hoạch dự phòng.

Sau khi sườn được duyệt:

- mã nguồn demo;
- unit test;
- README hướng dẫn chạy;
- kết quả benchmark;
- ảnh hoặc video dự phòng;
- review code cùng TV3 và TV5.

## 8.7. Câu hỏi TV6 phải trả lời được

1. Vì sao dùng độ trễ mô phỏng thay cho API Internet?
2. Làm sao biết so sánh ba phiên bản là công bằng?
3. Vì sao ThreadPool và `asyncio` có thể gần bằng nhau ở demo nhỏ?
4. Vì sao speedup ProcessPool không bằng đúng số worker?
5. Nếu ProcessPool chậm hơn tuần tự thì giải thích thế nào?
6. Vì sao phải chạy test trước benchmark?
7. Kết quả trên một máy có áp dụng tuyệt đối cho máy khác không?

## 8.8. Tiêu chí hoàn thành

- Demo chạy được khi không có Internet.
- Không cần cài quá nhiều package.
- Có phương án B nếu live demo lỗi.
- Mọi số liệu ghi rõ điều kiện đo.
- Không dùng sleep để mô phỏng CPU-bound.
- Không đưa demo vào repository trước khi nhóm duyệt đặc tả.

---

# 9. PHÂN CÔNG REVIEW CHÉO

| Người viết | Người review | Nội dung cần kiểm tra |
|---|---|---|
| TV1 | TV4 | Thuật ngữ concurrency/async có thống nhất với event loop không |
| TV2 | TV5 | Blocking, loại tải và lời khuyên chọn công cụ có đủ điều kiện không |
| TV3 | TV6 | API Executor/Future có khớp với thiết kế demo không |
| TV4 | TV1 | Phần asyncio có dễ hiểu với người chưa biết coroutine không |
| TV5 | TV2 | Timeout, cancel, Semaphore, Queue có đúng cơ chế không |
| TV6 | TV3 | Demo có đúng contract, test và benchmark công bằng không |

Reviewer không chỉ sửa chính tả. Mỗi review phải trả lời:

1. Nội dung có đúng với Chương 4 không?
2. Phần nào là mở rộng và đã ghi rõ chưa?
3. Có thuật ngữ nào mâu thuẫn với phần khác không?
4. Ví dụ có thực sự chứng minh luận điểm không?
5. Nguồn có phải nguồn chính thức không?
6. Người trình bày có thể nói phần này trong thời gian quy định không?

# 10. LỘ TRÌNH THỰC HIỆN

## Giai đoạn 1 — Duyệt sườn

- TV1 tổng hợp yêu cầu của giáo viên.
- Sáu thành viên đọc file Chương 4.
- Mỗi người comment vào phần được giao.
- Nhóm chốt 42 slide, thời lượng và demo.
- Chưa thiết kế PowerPoint ở giai đoạn này.

## Giai đoạn 2 — Nghiên cứu và viết nội dung

- Mỗi người viết research notes và nguồn.
- Review chéo theo bảng ở trên.
- TV1 xử lý phần trùng lặp.
- Chỉ nội dung đã review mới được chuyển sang bản thiết kế slide.

## Giai đoạn 3 — Thiết kế slide và demo

- Thống nhất template, font, màu và cách trình bày code.
- Mỗi slide chỉ giữ một thông điệp chính.
- TV6 triển khai demo sau khi đặc tả được duyệt.
- TV3 review phần process/thread; TV5 review timeout/giới hạn tải.

## Giai đoạn 4 — Kiểm thử và tập dượt

- Chạy test và benchmark trên máy trình chiếu.
- Tập lần 1 để sửa kiến thức.
- Tập lần 2 để bấm giờ.
- Tập lần 3 như buổi báo cáo thật, gồm demo và Q&A.

# 11. MỐC THỜI GIAN GỢI Ý

| Mốc | Việc phải hoàn tất |
|---|---|
| D−14 | Chốt sườn, tên thành viên, thời lượng và demo |
| D−11 | Mỗi người nộp nghiên cứu và nguồn phần mình |
| D−9 | Hoàn thành review chéo |
| D−7 | Chốt toàn bộ nội dung chữ và sơ đồ |
| D−5 | Hoàn thành bản slide đầu và demo đầu tiên |
| D−3 | Test, benchmark và tập lần 1 |
| D−2 | Sửa nội dung, tập bấm giờ |
| D−1 | Khóa bản cuối, sao lưu và tổng duyệt |
| D | Báo cáo; không sửa code/nội dung lớn ngay trước giờ |

# 12. QUY TẮC LÀM VIỆC TRÊN GITHUB

## Issue đề xuất

- `01-outline-and-story` — TV1.
- `02-foundation-process-thread-coroutine` — TV2.
- `03-concurrent-futures` — TV3.
- `04-asyncio-event-loop` — TV4.
- `05-reliability-and-backpressure` — TV5.
- `06-demo-specification` — TV6.
- `07-cross-review` — cả nhóm.
- `08-rehearsal-and-qa` — cả nhóm.

## Nhánh đề xuất

- `tv1/intro-concepts`
- `tv2/system-foundation`
- `tv3/concurrent-futures`
- `tv4/asyncio-core`
- `tv5/reliability`
- `tv6/demo-spec`

## Quy tắc commit

Ví dụ commit tốt:

- `docs: clarify concurrency vs parallelism`
- `docs: add Future lifecycle diagram notes`
- `docs: specify demo acceptance criteria`
- `review: correct asyncio cancellation explanation`

Không dùng commit message như `update`, `fix`, `them noi dung` vì không cho biết đã thay đổi gì.

## Quy tắc Pull Request

Mỗi Pull Request phải có:

- phần Chương 4 tương ứng;
- nội dung mới hoặc nội dung đã sửa;
- nguồn tham khảo;
- ảnh hưởng đến phần của thành viên khác;
- checklist tự kiểm tra;
- tên người review.

# 13. DEFINITION OF DONE CHO TOÀN NHÓM

Sườn chỉ được coi là duyệt xong khi:

- [ ] đủ 42 slide dự kiến và mỗi slide có một mục tiêu;
- [ ] nội dung gốc Chương 4 không bị bỏ sót;
- [ ] mọi nội dung mở rộng được đánh dấu;
- [ ] sáu thành viên đồng ý với phạm vi phần mình;
- [ ] không có định nghĩa mâu thuẫn giữa các phần;
- [ ] demo có đặc tả nhưng chưa bị triển khai quá sớm;
- [ ] thời lượng dự kiến phù hợp yêu cầu giáo viên;
- [ ] nguồn chính thức được ghi rõ;
- [ ] có phân công review chéo;
- [ ] có kế hoạch Q&A và phương án dự phòng.

# 14. BA VIỆC NHÓM CẦN LÀM NGAY

1. Điền họ tên, MSSV và thế mạnh của `TV1`…`TV6`.
2. Xác nhận giáo viên cho bao nhiêu phút và có bắt buộc demo hay không.
3. Mỗi thành viên xác nhận phần được giao bằng comment trong Issue tương ứng.

Sau khi ba việc này hoàn tất, nhóm mới bắt đầu viết nội dung chi tiết của từng slide và thiết kế PowerPoint.
