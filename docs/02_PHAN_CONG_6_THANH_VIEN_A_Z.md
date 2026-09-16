# PHÂN CÔNG 6 THÀNH VIÊN — CHƯƠNG 4 TỪ A ĐẾN Z

> **Chủ đề:** Phương pháp tính toán bất đồng bộ trong môn Tính toán song song và phân tán
> **Loại tài liệu:** Sườn nội dung, kế hoạch học và phân công; chưa phải PowerPoint
> **Ba cấu hình:** 36 slide rút gọn, 48 slide chuẩn, 18 slide phụ lục
> **Nguyên tắc cốt lõi:** Phân công thuyết trình theo chuyên môn, nhưng cả sáu thành viên phải học và bảo vệ được toàn bộ Chương 4.

---

## 1. Mục tiêu của bản phân công

Bản phân công này không chia Chương 4 thành sáu mảnh rời để mỗi người chỉ học tám slide của mình. Nhóm làm việc theo ba tầng:

1. **Kiến thức chung:** cả sáu người học, chạy thử, giải thích và làm bài kiểm tra về toàn bộ chương.
2. **Chuyên môn chính:** mỗi người sở hữu một cụm kiến thức liền mạch, nghiên cứu sâu, viết nội dung và chịu trách nhiệm độ chính xác.
3. **Reviewer/backup:** mỗi cụm có thêm một người kiểm tra chéo, hiểu đủ sâu và có thể thuyết trình thay.

Kết thúc quá trình, bất kỳ thành viên nào cũng phải trả lời được:

- Bất đồng bộ là gì và khác tuần tự, đồng thời, song song như thế nào?
- Python tổ chức công việc qua Future, Executor, thread, process, coroutine, Task và event loop ra sao?
- Khi nào chọn tuần tự, ThreadPool, ProcessPool, asyncio hoặc mô hình lai?
- Timeout, cancellation, exception, race condition, deadlock và backpressure được xử lý thế nào?
- Làm sao chứng minh chương trình đúng trước khi kết luận nó nhanh?
- Một chương trình bất đồng bộ trên một máy liên hệ nhưng không đồng nhất với hệ thống phân tán như thế nào?

### 1.1. Phạm vi “A–Z”

“A–Z” ở đây là:

- Đủ toàn bộ nội dung bắt buộc trong file Chương 4.
- Bổ sung kiến thức nền cần để người mới hiểu đúng.
- Bổ sung kỹ thuật trực tiếp cần để viết chương trình bất đồng bộ đúng, chịu lỗi và đo được.
- Có demo nhỏ để kiểm chứng, không chỉ đọc định nghĩa.
- Có câu hỏi, bài debug và cơ chế học chéo để chứng minh cả sáu người đều hiểu.

“A–Z” không có nghĩa là khảo sát mọi framework async trên thế giới. Trio, AnyIO, aiohttp, framework web, distributed task queue và các interpreter Python khác chỉ xuất hiện ở phần định hướng nếu giúp làm rõ quyết định. Phạm vi và phần không đi sâu phải được ghi công khai, không âm thầm bỏ qua.

---

## 2. Chuẩn kiến thức chung bắt buộc cho cả sáu thành viên

Mỗi thành viên phải giải thích được 40 năng lực sau mà không nói “phần đó bạn khác làm”.

### 2.1. Nền tảng

1. Bài toán mà tính toán bất đồng bộ giải quyết.
2. Sequential, concurrent và parallel.
3. Synchronous và asynchronous.
4. Blocking và non-blocking.
5. Vì sao hai cặp synchronous/asynchronous và blocking/non-blocking không phải từ đồng nghĩa.
6. Task, job, process, thread, coroutine, awaitable, Task và Future.
7. I/O-bound, CPU-bound và mixed workload.
8. Preemptive scheduling, cooperative scheduling, context switch và yield point.
9. Trạng thái created, ready/pending, running, waiting, completed, failed và cancelled.
10. Vì sao bất đồng bộ không tự động có nghĩa là song song.

### 2.2. concurrent.futures

11. Vai trò abstraction của Executor và Future.
12. Vòng đời của concurrent.futures.Future.
13. submit, map, result, exception, cancel, cancelled, running, done và callback.
14. wait, as_completed và sự khác nhau về thứ tự tiêu thụ kết quả.
15. Context manager và shutdown.
16. ThreadPoolExecutor và workload blocking I/O.
17. Shared state, thread safety, race condition và deadlock trong pool.
18. ProcessPoolExecutor và workload pure-Python CPU-bound đủ lớn.
19. GIL trong interpreter/phiên bản Python mục tiêu.
20. Serialization, pickling, main guard, IPC và khác biệt nền tảng.

### 2.3. asyncio

21. Event loop, ready queue, timer và I/O waiting ở mức khái niệm.
22. Coroutine function và coroutine object.
23. Awaitable, asyncio.Task, asyncio.Future và concurrent.futures.Future.
24. async def, await, asyncio.run, create_task và asyncio.sleep.
25. Điểm await nào thật sự trao quyền lại cho event loop.
26. gather, wait, as_completed và TaskGroup.
27. Structured concurrency và phạm vi sống của child task.
28. Async iterator, async generator, async for, async context manager và async with.
29. to_thread hoặc executor để cô lập lời gọi blocking.
30. Lỗi gọi coroutine nhưng không await và lỗi chặn event loop.

### 2.4. Tính đúng đắn, độ tin cậy và hiệu năng

31. Timeout, cancellation, propagation, shield có kiểm soát và cleanup.
32. Exception propagation, ExceptionGroup, retry, backoff, jitter và idempotency.
33. Lock, Event, Condition, Semaphore, BoundedSemaphore và Barrier.
34. Queue, producer–consumer, task_done, join và backpressure.
35. Deadlock, starvation, livelock, resource exhaustion và unbounded concurrency.
36. Debug, logging, Task bị bỏ quên, coroutine chưa await và callback chậm.
37. Baseline, latency, throughput, overhead, speedup, efficiency và Amdahl.
38. Correctness trước performance; benchmark có warm-up, lặp và mô tả môi trường.
39. Cây quyết định tuần tự/thread/process/async/hybrid.
40. Khác biệt giữa asynchronous computing trên một máy và distributed computing nhiều nút.

---

## 3. Kiến trúc slide 36/48/18

### 3.1. Bản chuẩn 48 slide

- Mỗi thành viên có tám slide chính.
- Phần nội dung khoảng 48–55 phút; cộng demo 8–10 phút và Q&A khoảng 10 phút, tổng dự kiến 66–75 phút.
- Mỗi slide có một thông điệp chính; chi tiết nằm trong lời thuyết trình, tài liệu học và phụ lục.

### 3.2. Bản rút gọn 36 slide

- Mỗi thành viên có sáu slide.
- Hai cặp slide trong bộ tám được ghép có chủ đích.
- Không xóa kiến thức khỏi tài liệu; chỉ giảm phần trình bày trực tiếp.
- Phần nội dung khoảng 30–36 phút; cộng demo 8–10 phút và Q&A 8–10 phút, tổng dự kiến 46–56 phút.

### 3.3. Phụ lục 18 slide

- Mỗi thành viên sở hữu ba slide phụ lục.
- Phụ lục chứa bảng API, phản ví dụ, platform/version caveat, benchmark chi tiết và câu hỏi khó.
- Phụ lục vẫn phải được cả nhóm học vì giáo viên có thể hỏi tới.

### 3.4. Quy ước mô tả từng slide

Mỗi slide bên dưới có:

- **Thông điệp:** một câu người nghe phải nhớ.
- **Nội dung:** các ý bắt buộc.
- **Minh họa/code/diagram:** tài sản cần chuẩn bị.
- **Lời giải thích:** logic người nói cần diễn đạt; không phải đoạn văn để chép lên slide.
- **Câu hỏi chuyển:** nối kiến thức hoặc kiểm tra người nghe.

---

## 4. Ma trận chuyên gia, reviewer và backup

| Cụm kiến thức | Chuyên gia chính | Reviewer/backup | Bốn người còn lại |
|---|---:|---:|---|
| Nền tảng và bản đồ khái niệm | TV1 | TV4 | Học, chạy baseline, làm quiz và bảo vệ miệng |
| Future, Executor và ThreadPool | TV2 | TV5 | Chạy ví dụ, dự đoán state/exception và làm bài debug |
| ProcessPool, GIL và hiệu năng | TV3 | TV6 | Chạy benchmark, giải thích overhead và platform caveat |
| Event loop, coroutine và Task | TV4 | TV1 | Vẽ scheduling trace, chạy ví dụ và làm quiz |
| Điều phối, lỗi và độ tin cậy | TV5 | TV2 | Chạy failure scenario, sửa race/cancellation và làm quiz |
| Lựa chọn kiến trúc, tích hợp và phân tán | TV6 | TV3 | Chạy năm mode, bảo vệ decision tree và kết luận |

Reviewer/backup phải:

1. Kiểm tra nguồn, thuật ngữ, ví dụ và tính logic.
2. Đặt ít nhất năm câu hỏi phản biện cho chuyên gia chính.
3. Trình bày thử toàn bộ phần của chuyên gia chính ít nhất một lần.
4. Có thể trả lời phần đó khi chuyên gia chính vắng hoặc giáo viên đổi người.

---

## 5. Công việc xuyên suốt được rải đều

Không dồn nguồn, kiểm thử, thuật ngữ, QA hoặc rehearsal cho một người.

| Thành viên | Vai trò xuyên suốt | Việc phải làm |
|---|---|---|
| TV1 | Phạm vi và thuật ngữ | Duy trì glossary; đối chiếu file gốc với sườn; mọi người vẫn phải gửi thuật ngữ phần mình |
| TV2 | Quy ước ví dụ và test | Tạo template ví dụ đúng/sai và test plan; mỗi người vẫn tự thiết kế test cho phần mình |
| TV3 | Nguồn và benchmark | Chuẩn hóa citation, phiên bản và môi trường đo; mỗi người vẫn tự tìm nguồn chính thức |
| TV4 | Diagram và mạch kể | Chuẩn hóa timeline, state diagram, màu/ký hiệu và câu chuyển; mỗi người vẫn tự thiết kế hình phần mình |
| TV5 | QA và failure cases | Gom ngân hàng câu hỏi, rubric và fault injection; mỗi người vẫn nộp 20 câu/bài cho phần mình |
| TV6 | Tích hợp GitHub và rehearsal | Quản lý milestone, runbook, lịch diễn tập và bản chốt; không viết thay nội dung người khác |

Quy tắc “người quản lý không phải người làm thay” áp dụng cho cả sáu vai trò.

---

## 6. Demo chung cần thiết kế — giám sát nhiều trạm cảm biến

### 6.1. Bài toán

Nhiều trạm cảm biến gửi dữ liệu với độ trễ khác nhau. Hệ thống lấy dữ liệu, kiểm tra/làm sạch, thực hiện một bước phân tích CPU, tạo cảnh báo và tổng hợp kết quả. Một số trạm có thể chậm, lỗi hoặc vượt timeout.

~~~text
Trạm cảm biến
  → lấy dữ liệu có độ trễ
  → giới hạn concurrency
  → bounded queue
  → kiểm tra/làm sạch
  → phân tích CPU
  → tổng hợp cảnh báo
  → metric và báo cáo
~~~

### 6.2. Năm mode phải có trong đặc tả

1. **sequential:** correctness oracle và baseline.
2. **thread:** ThreadPool cho blocking I/O.
3. **process:** ProcessPool cho bước CPU đủ lớn.
4. **async:** coroutine cho concurrent I/O.
5. **hybrid:** asyncio cho I/O và process pool cho CPU.

### 6.3. Tham số cần dự kiến

- Số trạm, số mẫu và random seed.
- Độ trễ I/O và tỷ lệ trạm chậm.
- Tỷ lệ lỗi, timeout và số lần retry.
- Thread/process worker.
- Giới hạn Semaphore và kích thước Queue.
- Độ nặng bước CPU.

### 6.4. Điều kiện nghiệm thu demo sau này

- Cùng input cho kết quả nghiệp vụ tương đương ở năm mode.
- Có correctness test trước benchmark.
- Ghi Python, interpreter, hệ điều hành, CPU, tham số và số lần lặp.
- Có workload nhỏ cho thấy concurrency/parallelism có thể chậm hơn vì overhead.
- Không chạy blocking I/O hoặc CPU-heavy trực tiếp trong event loop ở bản đúng.
- Không tạo Task vô hạn.
- Có timeout, cancellation và failure injection.
- Hoạt động đúng trên Windows với main guard.
- Có chế độ offline và ghi rõ dữ liệu/độ trễ mô phỏng.

Tài liệu này chỉ phân công và đặc tả. Không tạo code demo, PPTX hoặc PDF ở giai đoạn này.

---

# PHẦN I — PHÂN CÔNG THEO THÀNH VIÊN

## 7. Thành viên 1 — Nền tảng và bản đồ tư duy

### 7.1. Mục tiêu

TV1 xây nền chung để người nghe không nhầm thuật ngữ trước khi học API. TV1 phải:

- Phân biệt chính xác bảy khái niệm dễ nhầm.
- Vẽ timeline của cùng bài toán theo nhiều mô hình.
- Nhận diện I/O-bound, CPU-bound và mixed workload.
- Giải thích process, thread, coroutine và scheduling.
- Thiết lập baseline và nguyên tắc benchmark.
- Chứng minh “nhiều worker/task hơn” không đồng nghĩa “nhanh hơn”.

### 7.2. Kiến thức phải học sâu

- Task lifecycle.
- Preemptive và cooperative scheduling.
- Context switch và yield point.
- Latency, throughput, utilization, overhead, speedup, efficiency.
- Critical path và Amdahl’s Law.
- Quan hệ giữa async, concurrency, parallelism và distributed.
- Nền tảng Future và event loop đủ để review TV4.

### 7.3. Tám slide chuẩn — slide 1 đến 8

#### Slide 1 — Bài toán và câu hỏi trung tâm

- **Thông điệp:** Bất đồng bộ tận dụng khoảng chờ, nhưng phải xác định đúng loại chờ.
- **Nội dung:** Hệ thống đọc nhiều trạm; mỗi trạm có I/O delay; sau đó có bước CPU. Đặt ba câu hỏi: phần chờ có thể chồng lấp không, phần CPU có thể song song không, overhead bao nhiêu.
- **Minh họa/code/diagram:** Timeline tám trạm chạy tuần tự; màu riêng cho CPU, I/O wait và idle.
- **Lời giải thích:** Bắt đầu từ tài nguyên bị lãng phí thay vì cú pháp. Nhấn mạnh pipeline có hai loại workload nên một công cụ không mặc nhiên tối ưu toàn bộ.
- **Câu hỏi chuyển:** “Nhiều việc cùng tiến triển có nhất thiết chạy cùng một thời điểm không?”

#### Slide 2 — Tuần tự, đồng thời và song song

- **Thông điệp:** Concurrency nói về tiến triển; parallelism nói về thực thi đồng thời vật lý.
- **Nội dung:** Định nghĩa sequential/concurrent/parallel; xen kẽ trên một core; chạy trên nhiều core; trường hợp vừa concurrent vừa parallel.
- **Minh họa/code/diagram:** Ba timeline cùng bốn task A–D để so trực tiếp.
- **Lời giải thích:** Dùng timeline thay vì chỉ dùng ví dụ đời thường. Concurrency là cách tổ chức, parallelism là thuộc tính thực thi tại một thời điểm.
- **Câu hỏi chuyển:** “Synchronous và asynchronous nằm ở trục nào?”

#### Slide 3 — Đồng bộ, bất đồng bộ, blocking và non-blocking

- **Thông điệp:** Đây là hai trục liên quan nhưng không đồng nhất.
- **Nội dung:** Sync/async nhìn từ contract gọi–nhận kết quả; blocking/non-blocking nhìn từ việc luồng gọi có bị giữ; ma trận 2×2; await tạm dừng coroutine chứ không nhất thiết block event-loop thread.
- **Minh họa/code/diagram:** Ma trận call/return/Future/callback và trạng thái caller.
- **Lời giải thích:** Phân biệt tầng API với hoạt động hệ điều hành bên dưới. Tránh khẳng định mọi async API đều non-blocking ở mọi tầng.
- **Câu hỏi chuyển:** “Ai thực thi công việc, và ai quyết định lúc nào nó được chạy?”

#### Slide 4 — Process, thread, coroutine và scheduler

- **Thông điệp:** Ba đơn vị có vùng nhớ, chi phí và cơ chế scheduling khác nhau.
- **Nội dung:** Process có không gian địa chỉ riêng; thread chia sẻ bộ nhớ; coroutine là đơn vị logic nhẹ được lập lịch hợp tác; preemptive so với cooperative.
- **Minh họa/code/diagram:** Hai process, mỗi process có thread; một thread chứa event loop và nhiều coroutine.
- **Lời giải thích:** Không gọi coroutine đơn giản là “thread siêu nhẹ”. Coroutine chỉ tiến triển khi loop chạy và nhường quyền tại điểm phù hợp.
- **Câu hỏi chuyển:** “Chọn đơn vị nào nếu chủ yếu chờ I/O, và chọn gì nếu dùng CPU?”

#### Slide 5 — I/O-bound, CPU-bound và mixed workload

- **Thông điệp:** Phân loại nút thắt trước khi chọn công cụ.
- **Nội dung:** Dấu hiệu và phép đo; ví dụ đọc cảm biến, lọc tín hiệu, ghi file; ThreadPool/asyncio là ứng viên I/O, ProcessPool là ứng viên CPU nhưng còn phụ thuộc overhead/GIL/thư viện.
- **Minh họa/code/diagram:** Bảng triệu chứng → phép đo → công cụ ứng viên.
- **Lời giải thích:** Dùng từ “ứng viên”, không đưa quy tắc tuyệt đối. Phải đo workload thật và xem thư viện native có giải phóng GIL không.
- **Câu hỏi chuyển:** “Làm sao biết giải pháp mới thật sự tốt hơn?”

#### Slide 6 — Đo đúng trước khi kết luận

- **Thông điệp:** Không có baseline công bằng thì không có kết luận hiệu năng đáng tin.
- **Nội dung:** Wall time, latency, throughput, speedup, efficiency; warm-up, cùng input, nhiều lần lặp, median; correctness trước performance.
- **Minh họa/code/diagram:** Công thức speedup và bảng benchmark mẫu chưa điền số.
- **Lời giải thích:** Một phiên bản trả sai có thể chạy nhanh. Liệt kê overhead: tạo worker, scheduling, serialization, queue và contention.
- **Câu hỏi chuyển:** “Vô hạn worker có tạo ra vô hạn speedup không?”

#### Slide 7 — Giới hạn tăng tốc và ngộ nhận

- **Thông điệp:** Phần tuần tự, overhead và tài nguyên hữu hạn đặt trần tăng tốc.
- **Nội dung:** Amdahl trực quan; critical path; oversubscription; myth/fact: async luôn nhanh, nhiều worker luôn tốt, event loop một thread không có race.
- **Minh họa/code/diagram:** Đường cong speedup bão hòa và bảng Myth/Fact.
- **Lời giải thích:** Dùng Amdahl để lập luận, không biến phần này thành bài toán thuần công thức. Mô hình lý tưởng còn chưa tính overhead thực.
- **Câu hỏi chuyển:** “Ta dùng baseline nào xuyên suốt để không đổi bài toán giữa chừng?”

#### Slide 8 — Baseline demo và bản đồ Chương 4

- **Thông điệp:** Một baseline đúng và một bài toán chung giúp so sánh công cụ công bằng.
- **Nội dung:** Pipeline cảm biến, input/output chuẩn, năm mode, ánh xạ TV2–TV6.
- **Minh họa/code/diagram:** Pipeline có màu sở hữu; pseudocode tuần tự 8–12 dòng; bảng mode chưa điền kết quả.
- **Lời giải thích:** Sequential là correctness oracle, không phải “phiên bản kém”. Các phần sau phải giữ cùng input, phép tính và metric.
- **Câu hỏi chuyển:** “Làm sao giao việc cho pool và theo dõi kết quả mà không tự quản lý thread?”

### 7.4. Bản rút gọn sáu slide

1. Giữ slide 1.
2. Giữ slide 2.
3. Giữ slide 3.
4. Ghép slide 4+5: “Đơn vị thực thi và loại workload”.
5. Ghép slide 6+7: “Benchmark và giới hạn tăng tốc”.
6. Giữ slide 8.

Không xóa ma trận thuật ngữ, correctness check hoặc overhead; chuyển chi tiết Amdahl sang phụ lục.

### 7.5. Ba slide phụ lục — P01 đến P03

#### P01 — Ma trận thuật ngữ đầy đủ

- **Thông điệp:** Thuật ngữ có quan hệ nhưng không thay thế nhau.
- **Nội dung:** Định nghĩa, góc nhìn, ví dụ và phản ví dụ của bảy thuật ngữ.
- **Minh họa/code/diagram:** Ma trận nhiều trục kèm timeline nhỏ.
- **Lời giải thích:** Dùng khi giáo viên yêu cầu phân loại một API cụ thể.
- **Câu hỏi chuyển:** “Ta đang mô tả contract API hay cơ chế vật lý bên dưới?”

#### P02 — Amdahl và bài tính mẫu

- **Thông điệp:** Tỷ lệ phần tuần tự quan trọng hơn tăng worker vô hạn.
- **Nội dung:** Công thức; ví dụ 20% tuần tự; 2/4/8 worker và giới hạn.
- **Minh họa/code/diagram:** Đường cong speedup.
- **Lời giải thích:** Chỉ ra đây là upper bound lý tưởng, chưa tính overhead.
- **Câu hỏi chuyển:** “Phần tuần tự và overhead trong demo nằm ở đâu?”

#### P03 — Checklist benchmark công bằng

- **Thông điệp:** Benchmark phải tái lập và kiểm tra đúng kết quả.
- **Nội dung:** Phiên bản, phần cứng, seed, input, warm-up, repetitions, median, variance và correctness digest.
- **Minh họa/code/diagram:** Checklist có ô đánh dấu.
- **Lời giải thích:** Đây là hợp đồng mà TV3/TV6 phải dùng.
- **Câu hỏi chuyển:** “Hai mode xử lý lượng dữ liệu khác nhau có còn so được không?”

### 7.6. Đóng góp demo

- Định nghĩa data contract và tiêu chí đúng.
- Thiết kế sequential baseline và fixed seed.
- Chuẩn hóa input/output để mọi mode so được.
- Viết đặc tả timeline baseline; chưa viết code ở giai đoạn này.

### 7.7. Deliverables

- Tài liệu nền tảng 15–20 trang.
- Glossary và quy tắc thuật ngữ toàn nhóm.
- Coverage map nối file gốc với sườn.
- Ba timeline, ma trận thuật ngữ, sơ đồ process/thread/coroutine.
- Đặc tả baseline và correctness oracle.
- 12 câu trắc nghiệm, 6 câu tự luận, 2 bài bắt lỗi.
- Kịch bản giải thích 1/3/8 phút.
- Biên bản review phần TV4.

### 7.8. Câu hỏi phản biện

1. Concurrency khác parallelism chính xác ở đâu?
2. Một chương trình một thread có concurrent được không?
3. API async có luôn non-blocking không?
4. await có block thread không?
5. Vì sao I/O-bound và CPU-bound cần chiến lược khác?
6. Tại sao thêm worker có thể làm chậm?
7. Latency và throughput có thể cho hai kết luận khác nhau không?
8. Amdahl bỏ qua overhead nào?
9. Vì sao kiểm tra cùng kết quả trước benchmark?
10. Async trên một máy có phải distributed không?

### 7.9. Tiêu chí đạt, GitHub role và backup

TV1 đạt khi vẽ lại timeline không nhìn tài liệu, phân loại đúng tình huống, bảo vệ benchmark baseline, trình bày thay TV4 và được TV4 xác nhận thuật ngữ nhất quán.

- **GitHub role:** scope/terminology owner; quản lý Issue coverage và glossary.
- **Reviewer/backup của TV1:** TV4.
- **TV1 review/backup cho:** TV4.

---

## 8. Thành viên 2 — Future, Executor và ThreadPool

### 8.1. Mục tiêu

TV2 giải thích abstraction cấp cao của concurrent.futures và cách dùng thread pool an toàn cho blocking I/O. TV2 phải:

- Giải thích Future không phải thread hay kết quả đã có.
- Trình bày state, result, exception, timeout và cancellation.
- Phân biệt submit, map, wait và as_completed.
- Dùng lifecycle Executor an toàn.
- Nhận diện shared-state race, callback lỗi và pool deadlock.
- Phối hợp với TV4 để phân biệt hai họ Future.

### 8.2. Kiến thức phải học sâu

- Executor contract và Future state machine.
- Input order, completion order và collection strategy.
- Cancellation trước/sau khi chạy; timeout không dừng worker.
- Shared memory, Lock, thread safety và contention.
- Nested Future, pool starvation và deadlock.
- Context manager, shutdown và cleanup.
- Phiên bản API: chỉ ghi tham số sau khi kiểm tra tài liệu Python mục tiêu.

### 8.3. Tám slide chuẩn — slide 9 đến 16

#### Slide 9 — Vì sao cần Executor và Future

- **Thông điệp:** Executor tách gửi việc khỏi cơ chế worker; Future đại diện cho kết quả có thể chưa sẵn.
- **Nội dung:** Hạn chế quản lý thread thủ công; callable, queue, worker; Future làm handle quan sát kết quả/lỗi.
- **Minh họa/code/diagram:** Caller → Executor → work queue → workers → Future.
- **Lời giải thích:** Future không phải thread. Abstraction chung cho phép thay executor trong khi nhiều thao tác phía caller giữ nguyên.
- **Câu hỏi chuyển:** “Từ submit đến khi kết thúc, Future đi qua state nào?”

#### Slide 10 — State machine của Future

- **Thông điệp:** Có thể cancel công việc chưa chạy; cancel không phải nút dừng cưỡng bức công việc đang chạy.
- **Nội dung:** Pending, running, finished, cancelled; running/done/cancelled; kết thúc thành công hoặc exception; result/exception.
- **Minh họa/code/diagram:** State diagram có nhánh cancel thành công/thất bại.
- **Lời giải thích:** done bao gồm success, failure hoặc cancellation. result(timeout) chỉ giới hạn thời gian caller chờ; worker có thể vẫn chạy.
- **Câu hỏi chuyển:** “Ta gửi một việc hoặc một tập việc bằng API nào?”

#### Slide 11 — submit và map

- **Thông điệp:** submit cho quyền điều khiển từng Future; map tiện cho batch nhưng giữ logic thứ tự đầu vào.
- **Nội dung:** Một Future mỗi submit; iterable với map; exception khi tiêu thụ kết quả; chunksize/buffering phải gắn phiên bản.
- **Minh họa/code/diagram:** Bốn task A–D có thời gian khác nhau; pseudocode hai cách.
- **Lời giải thích:** Không liệt kê signature khô. Nêu lựa chọn theo nhu cầu điều khiển từng task, ordering và streaming.
- **Câu hỏi chuyển:** “Muốn xử lý tác vụ xong trước ngay lập tức thì làm sao?”

#### Slide 12 — wait và as_completed

- **Thông điệp:** Chờ một tập Future và tiêu thụ theo completion order là hai nhu cầu khác.
- **Nội dung:** done/not_done; điều kiện chờ; iterator completion; timeout; xử lý exception riêng từng Future.
- **Minh họa/code/diagram:** Timeline A–D và hai đường collect.
- **Lời giải thích:** Dùng cho progress/streaming result. Timeout của việc chờ không tự hủy toàn bộ Future còn lại.
- **Câu hỏi chuyển:** “ThreadPool thực thi các Future này thế nào?”

#### Slide 13 — ThreadPoolExecutor và blocking I/O

- **Thông điệp:** ThreadPool hữu ích khi chồng lấp được thời gian chờ nhưng phải giới hạn worker và tài nguyên.
- **Nội dung:** Pool, queue, worker reuse, max_workers; blocking I/O; connection/file limits; GIL chỉ giới thiệu để TV3 đào sâu.
- **Minh họa/code/diagram:** Nhiều thread xen kẽ pha I/O wait và Python ngắn.
- **Lời giải thích:** Không nói thread luôn dành cho I/O. Phải có đủ thời gian chờ, tác vụ độc lập và tài nguyên đích chấp nhận concurrency.
- **Câu hỏi chuyển:** “Chia sẻ bộ nhớ tiện, nhưng điều gì có thể sai?”

#### Slide 14 — Shared state và thread safety

- **Thông điệp:** Shared mutable state tạo race nếu thao tác không có ownership hoặc synchronization rõ.
- **Nội dung:** Read–modify–write; Lock; immutable/local result; aggregation một nơi; contention; GIL không phải khóa nghiệp vụ.
- **Minh họa/code/diagram:** Interleaving hai thread làm mất update; pseudocode sai/đúng.
- **Lời giải thích:** Ưu tiên thiết kế worker trả kết quả độc lập. Khóa toàn bộ có thể đúng nhưng triệt tiêu concurrency.
- **Câu hỏi chuyển:** “Nếu Future trong pool lại chờ Future khác cùng pool thì sao?”

#### Slide 15 — Exception, timeout, cancellation và deadlock

- **Thông điệp:** Lỗi được chuyển về caller; dependency sai có thể làm cạn worker và treo pool.
- **Nội dung:** Exception qua result; timeout; cancel limitation; callback phải nhẹ; mutual wait; single-worker nested wait.
- **Minh họa/code/diagram:** Wait-for graph và pool starvation.
- **Lời giải thích:** Phân biệt timeout, yêu cầu hủy và dừng thật. Tăng worker chỉ che triệu chứng; tổ chức dependency ở caller mới xử lý nguyên nhân.
- **Câu hỏi chuyển:** “Đóng pool an toàn cả khi có lỗi bằng cách nào?”

#### Slide 16 — Lifecycle an toàn và mode thread

- **Thông điệp:** Context manager, lỗi từng Future và worker limit tạo thành giải pháp hoàn chỉnh.
- **Nội dung:** with Executor; shutdown; submit/collect; demo sensor blocking I/O; correctness; metric.
- **Minh họa/code/diagram:** Pseudocode 12–15 dòng và bảng kết quả trống.
- **Lời giải thích:** Đi từ input, submit, collect, exception đến cleanup. Không khẳng định speedup trước benchmark.
- **Câu hỏi chuyển:** “Nếu nút thắt là pure-Python CPU, ThreadPool còn phù hợp nhất không?”

### 8.4. Bản rút gọn sáu slide

1. Giữ slide 9.
2. Giữ slide 10.
3. Ghép slide 11+12: “Gửi, chờ và thu kết quả”.
4. Giữ slide 13.
5. Ghép slide 14+15: “Shared state, lỗi và deadlock”.
6. Giữ slide 16.

### 8.5. Ba slide phụ lục — P04 đến P06

#### P04 — Bảng API Future/Executor

- **Thông điệp:** Mỗi API giải quyết một nhu cầu điều khiển khác nhau.
- **Nội dung:** Method, caller có chờ không, return, exception, cancellation và use case.
- **Minh họa/code/diagram:** Bảng tra cứu.
- **Lời giải thích:** Phân biệt API thay đổi worker hay chỉ đổi cách caller chờ.
- **Câu hỏi chuyển:** “Lời gọi nào thực sự có thể block caller?”

#### P05 — Hai mẫu pool deadlock

- **Thông điệp:** Deadlock đến từ dependency graph sai, không chỉ vì ít worker.
- **Nội dung:** Mutual wait và single-worker nested wait; nguyên nhân; cách tổ chức lại.
- **Minh họa/code/diagram:** Wait-for graph, pseudocode sai/đúng.
- **Lời giải thích:** Ví dụ demo phải có timeout bảo vệ, không làm treo buổi báo cáo.
- **Câu hỏi chuyển:** “Tăng max_workers có xóa nguyên nhân gốc không?”

#### P06 — Thread-safety checklist

- **Thông điệp:** Shared state phải có ownership hoặc synchronization.
- **Nội dung:** Immutable input, local result, lock scope, callback, log, library thread safety, cleanup.
- **Minh họa/code/diagram:** Checklist review.
- **Lời giải thích:** TV5 dùng checklist này khi review.
- **Câu hỏi chuyển:** “Thiết kế nào loại bỏ nhu cầu chia sẻ trạng thái?”

### 8.6. Đóng góp demo

- Đặc tả hàm đọc cảm biến blocking.
- Thiết kế mode ThreadPool và collection order.
- Xác định đường success, exception, timeout và cancellation.
- Thiết kế test một trạm lỗi không làm mất kết quả trạm khác.

### 8.7. Deliverables

- Tài liệu Future/Executor/ThreadPool 15–20 trang.
- State diagram, API table và hai collection timeline.
- Hai ví dụ đúng, hai phản ví dụ, một deadlock có timeout bảo vệ.
- Đặc tả mode thread và test plan; chưa viết code.
- 12 câu trắc nghiệm, 6 câu tự luận, 2 bài debug.
- Biên bản review phần TV5.

### 8.8. Câu hỏi phản biện

1. Future khác thread thế nào?
2. done có đồng nghĩa thành công không?
3. Vì sao cancel có thể thất bại?
4. Timeout của result có dừng worker không?
5. map và as_completed khác thứ tự thế nào?
6. Khi nào chọn wait?
7. GIL có làm thread luôn tuần tự không?
8. Vì sao GIL không thay Lock?
9. Hai kiểu deadlock Future là gì?
10. Context manager bảo đảm và không bảo đảm điều gì?

### 8.9. Tiêu chí đạt, GitHub role và backup

TV2 đạt khi vẽ state machine, dự đoán đúng ordering/exception, phát hiện deadlock, bảo vệ lifecycle và trình bày thay TV5.

- **GitHub role:** code-example/test-plan owner; duy trì template ví dụ đúng/sai và test case.
- **Reviewer/backup của TV2:** TV5.
- **TV2 review/backup cho:** TV5.

---

## 9. Thành viên 3 — ProcessPool, GIL và hiệu năng

### 9.1. Mục tiêu

TV3 giúp nhóm hiểu vì sao process có thể khai thác nhiều core cho pure-Python CPU-bound, đồng thời làm rõ chi phí serialization, startup và memory. TV3 phải:

- Giải thích GIL có điều kiện, không tuyệt đối hóa.
- Mô tả process isolation và IPC.
- Trình bày yêu cầu picklability và main guard.
- Phân tích khi ProcessPool nhanh hơn hoặc chậm hơn.
- Thiết kế benchmark tái lập và công bằng.
- Phối hợp TV6 tích hợp CPU stage vào pipeline hybrid.

### 9.2. Kiến thức phải học sâu

- CPython GIL và khác biệt interpreter/build/version.
- Worker process, address space và IPC.
- Pickle của callable, argument, result và exception.
- Windows spawn/main guard; start method và platform caveat.
- Process startup, data copy, memory footprint, chunksize và task granularity.
- Broken worker/pool, timeout và cancellation limitation.
- Speedup, efficiency, saturation, Amdahl và measurement noise.

### 9.3. Tám slide chuẩn — slide 17 đến 24

#### Slide 17 — Tại sao ThreadPool có thể không tăng tốc CPU-bound

- **Thông điệp:** Với pure-Python CPU-bound trên CPython có GIL, nhiều thread thường không thực thi bytecode Python song song như mong đợi.
- **Nội dung:** CPU saturation; GIL ở mức khái niệm; context-switch overhead; thư viện native có thể giải phóng GIL; phải ghi interpreter/version.
- **Minh họa/code/diagram:** Timeline hai thread tranh quyền thực thi và biểu đồ CPU.
- **Lời giải thích:** Tránh câu “Python không chạy song song”. Process và native code vẫn có thể song song; free-threaded build/khác interpreter phải được nêu là ngoại lệ theo phiên bản.
- **Câu hỏi chuyển:** “Tách công việc sang process khác thay đổi điều gì?”

#### Slide 18 — Process isolation và ProcessPool

- **Thông điệp:** ProcessPool đổi shared memory lấy khả năng cô lập và khai thác nhiều core, nhưng cần truyền dữ liệu.
- **Nội dung:** Address space riêng; worker process; parent/child; IPC; Executor interface tương tự nhưng cơ chế khác.
- **Minh họa/code/diagram:** Parent → serialized task → worker processes → serialized result.
- **Lời giải thích:** Không nói process “chia sẻ không gì cả”; hệ điều hành và cơ chế IPC vẫn tồn tại. Ở mức ứng dụng, dữ liệu gửi qua pool phải được chuyển/serialize.
- **Câu hỏi chuyển:** “Đối tượng nào có thể gửi qua ranh giới process?”

#### Slide 19 — Pickling và main guard

- **Thông điệp:** Callable và dữ liệu phải serializable/importable; main guard là điều kiện sống còn trên môi trường spawn.
- **Nội dung:** Top-level function; lambda/nested function thường có vấn đề; object chứa resource không pickle; if-name-main; REPL/notebook caveat.
- **Minh họa/code/diagram:** Bảng pickle được/không; pseudocode cấu trúc module đúng.
- **Lời giải thích:** Giải thích worker cần import module và dựng lại object. Không học thuộc lỗi; hiểu đường đi dữ liệu.
- **Câu hỏi chuyển:** “Ngay cả khi chạy được, truyền dữ liệu lớn có miễn phí không?”

#### Slide 20 — Startup, serialization và granularity

- **Thông điệp:** ProcessPool chỉ có lợi khi lượng tính toán đủ bù startup và truyền dữ liệu.
- **Nội dung:** Startup, serialization, copy, scheduling, memory; task quá nhỏ; batching/chunksize có điều kiện phiên bản; worker count.
- **Minh họa/code/diagram:** Tổng thời gian = compute + startup + serialization + scheduling; đồ thị task size.
- **Lời giải thích:** Chia càng nhỏ không luôn tốt. Task quá lớn giảm cân bằng tải; quá nhỏ tăng overhead. Phải thử nhiều granularity.
- **Câu hỏi chuyển:** “Thu kết quả và xử lý lỗi process khác ThreadPool ở đâu?”

#### Slide 21 — Future, exception và pool failure

- **Thông điệp:** Interface Future quen thuộc nhưng failure của worker/process có hậu quả riêng.
- **Nội dung:** Exception qua Future; process chết; broken pool; dữ liệu/exception không serialize; timeout/cancellation limitation; cleanup.
- **Minh họa/code/diagram:** Failure tree: task exception, serialization error, worker crash, pool unusable.
- **Lời giải thích:** Phân biệt lỗi nghiệp vụ trong task với lỗi hạ tầng pool. Không giả định retry mọi lỗi đều an toàn.
- **Câu hỏi chuyển:** “Đo ProcessPool thế nào để không tạo benchmark giả?”

#### Slide 22 — Quy trình benchmark CPU đúng

- **Thông điệp:** Benchmark phải giữ cùng thuật toán/kết quả và thay đúng một yếu tố.
- **Nội dung:** Baseline; warm-up; repetitions; median/spread; worker sweep; task-size sweep; correctness digest; environment.
- **Minh họa/code/diagram:** Ma trận workers × workload size; checklist P03.
- **Lời giải thích:** Không so một phiên bản làm ít việc với phiên bản làm nhiều việc. Tránh chỉ chụp một con số đẹp.
- **Câu hỏi chuyển:** “Speedup thay đổi thế nào khi tăng worker?”

#### Slide 23 — Speedup, efficiency và điểm bão hòa

- **Thông điệp:** Tăng worker chỉ hữu ích đến khi chạm giới hạn core, memory, IPC hoặc phần tuần tự.
- **Nội dung:** T1/Tp; efficiency; Amdahl; oversubscription; CPU core logical/physical; workload nhỏ chậm hơn.
- **Minh họa/code/diagram:** Hai đường cong workload nhỏ/lớn theo số worker.
- **Lời giải thích:** Kết luận phải dùng “trên cấu hình và workload này”. Không tổng quát hóa benchmark của một laptop thành định luật.
- **Câu hỏi chuyển:** “Đưa CPU stage này vào demo cảm biến bằng cách nào?”

#### Slide 24 — Mode process và bài học lựa chọn

- **Thông điệp:** ProcessPool là công cụ cho CPU stage đủ thô, không phải sự thay thế mặc định cho mọi code tuần tự.
- **Nội dung:** Chọn phép phân tích cảm biến CPU-heavy có thể điều chỉnh; input nhỏ/lớn; main guard; expected result; metric; bàn giao sang async/hybrid.
- **Minh họa/code/diagram:** Pseudocode process mode và bảng trade-off ThreadPool/ProcessPool.
- **Lời giải thích:** Chỉ thiết kế workload có ý nghĩa, không tạo vòng lặp vô nghĩa để “ép” process thắng. Có thể dùng lọc/tương quan/anomaly calculation thuần Python với độ nặng điều chỉnh.
- **Câu hỏi chuyển:** “Trong khi process xử lý CPU, ai điều phối hàng nghìn tác vụ I/O nhẹ?”

### 9.4. Bản rút gọn sáu slide

1. Giữ slide 17.
2. Giữ slide 18.
3. Giữ slide 19.
4. Ghép slide 20+21: “Chi phí và lỗi qua ranh giới process”.
5. Ghép slide 22+23: “Benchmark và scalability”.
6. Giữ slide 24.

### 9.5. Ba slide phụ lục — P07 đến P09

#### P07 — GIL: điều đúng và điều không được nói

- **Thông điệp:** GIL là chi tiết interpreter có hệ quả cụ thể, không phải khẩu hiệu “Python không song song”.
- **Nội dung:** CPython/version mục tiêu; bytecode; blocking I/O/native extension; process; free-threaded/khác interpreter ghi như caveat.
- **Minh họa/code/diagram:** Bảng claim đúng/sai/cần điều kiện.
- **Lời giải thích:** Mỗi claim phải nói rõ phạm vi.
- **Câu hỏi chuyển:** “Workload dùng thư viện native giải phóng GIL có thể đổi quyết định không?”

#### P08 — Pickle và platform checklist

- **Thông điệp:** Khả năng chạy phụ thuộc cấu trúc module và nền tảng.
- **Nội dung:** Top-level callable, main guard, resource object, start method, REPL, Windows/macOS/Linux caveat.
- **Minh họa/code/diagram:** Checklist trước khi chạy.
- **Lời giải thích:** Chỉ ghi chi tiết đã xác minh trên Python mục tiêu.
- **Câu hỏi chuyển:** “Lỗi xảy ra lúc submit, serialize hay worker import?”

#### P09 — Bảng benchmark chi tiết

- **Thông điệp:** Phải nhìn cả phân bố và correctness, không chỉ speedup tốt nhất.
- **Nội dung:** workers, size, runs, median, p95/spread, speedup, efficiency, digest.
- **Minh họa/code/diagram:** Bảng và đồ thị hai workload.
- **Lời giải thích:** Giải thích điểm bão hòa và outlier.
- **Câu hỏi chuyển:** “Nếu kết quả khác digest thì số thời gian còn giá trị không?”

### 9.6. Đóng góp demo

- Đặc tả CPU stage thực tế và điều chỉnh được độ nặng.
- Đặc tả ProcessPool mode, main guard và dữ liệu truyền.
- Thiết kế worker/task-size sweep.
- Chuẩn hóa benchmark metadata và correctness digest.

### 9.7. Deliverables

- Tài liệu ProcessPool/GIL/benchmark 15–20 trang.
- Sơ đồ IPC, bảng pickling và platform checklist.
- Benchmark protocol, schema CSV/JSON và biểu đồ dự kiến.
- Hai workload size để chứng minh overhead.
- 12 câu trắc nghiệm, 6 câu tự luận, 2 bài debug.
- Biên bản review phần TV6.

### 9.8. Câu hỏi phản biện

1. GIL thực sự giới hạn điều gì?
2. Tại sao không được nói “Python không thể song song”?
3. Khi nào ThreadPool vẫn tăng tốc code có phần CPU?
4. Vì sao lambda/nested function có thể lỗi trong ProcessPool?
5. Main guard cần để làm gì?
6. Process truyền dữ liệu bằng cách nào ở mức ứng dụng?
7. Vì sao task nhỏ làm ProcessPool chậm?
8. BrokenProcessPool khác task exception ra sao?
9. Speedup và efficiency khác nhau thế nào?
10. Tại sao benchmark phải ghi interpreter/version/platform?

### 9.9. Tiêu chí đạt, GitHub role và backup

TV3 đạt khi giải thích GIL có điều kiện, sửa được lỗi pickle/main guard, thiết kế benchmark công bằng, giải thích điểm bão hòa và trình bày thay TV6.

- **GitHub role:** source/benchmark owner; quản lý citation format, version note và environment record.
- **Reviewer/backup của TV3:** TV6.
- **TV3 review/backup cho:** TV6.

---

## 10. Thành viên 4 — Event loop, coroutine và Task

### 10.1. Mục tiêu

TV4 xây mental model chính xác về asyncio. Sau phần này, người nghe phải hiểu chương trình async tiến triển thế nào thay vì chỉ biết thêm từ khóa async/await.

TV4 phải:

- Giải thích lifecycle event loop và cooperative scheduling.
- Phân biệt coroutine function/object, awaitable, Task và Future.
- Dùng đúng asyncio.run, create_task và asyncio.sleep.
- So sánh gather, wait, as_completed và TaskGroup.
- Giới thiệu async iterator/context manager.
- Cô lập blocking code và chỉ ra cách event loop bị đóng băng.

### 10.2. Kiến thức phải học sâu

- Ready queue, timer, I/O readiness ở mức khái niệm.
- Coroutine creation versus execution.
- Task scheduling, reference/lifetime và exception observation.
- Await semantics và yield point.
- Structured concurrency.
- Async iteration và async resource management.
- Bridge asyncio–thread/process executor.
- Nền tảng terminology đủ để review TV1.

### 10.3. Tám slide chuẩn — slide 25 đến 32

#### Slide 25 — Event loop là gì?

- **Thông điệp:** Event loop là bộ điều phối chạy coroutine sẵn sàng và quay lại chúng khi sự kiện hoàn tất.
- **Nội dung:** Ready work, timer, I/O waiting; một thread có thể quản lý nhiều tác vụ đang chờ; không phải mỗi coroutine có một thread.
- **Minh họa/code/diagram:** Vòng lặp ready → run → await → waiting → ready.
- **Lời giải thích:** Event loop chạy từng đoạn coroutine cho tới điểm nhường phù hợp. “Nhiều task” không có nghĩa bytecode của tất cả chạy cùng lúc trên một thread.
- **Câu hỏi chuyển:** “async def tạo ra thứ gì và khi nào code bên trong chạy?”

#### Slide 26 — Coroutine function, object và awaitable

- **Thông điệp:** Gọi async function tạo coroutine object; code chỉ tiến triển khi được await hoặc schedule.
- **Nội dung:** async def; coroutine object; awaitable categories; lỗi “coroutine was never awaited”.
- **Minh họa/code/diagram:** Code ngắn call-only, await và create_task; lifecycle tương ứng.
- **Lời giải thích:** Chỉ ra ba thời điểm khác nhau: tạo coroutine, schedule và hoàn thành. Không đồng nhất coroutine với Task.
- **Câu hỏi chuyển:** “Task thêm điều gì lên coroutine?”

#### Slide 27 — Task và hai họ Future

- **Thông điệp:** Task schedule coroutine trong event loop; asyncio.Future và concurrent Future thuộc hai hệ điều phối khác nhau.
- **Nội dung:** Task là awaitable; result/exception/cancel; asyncio.Future low-level; concurrent Future từ executor; bridge/wrap theo API chính thức.
- **Minh họa/code/diagram:** Sơ đồ type relationship và hai domain.
- **Lời giải thích:** Không dùng hai Future thay thế trực tiếp. Nhấn mạnh Task phải được quản lý vòng đời và exception phải được quan sát.
- **Câu hỏi chuyển:** “Tạo và chạy Task an toàn bằng API nào?”

#### Slide 28 — asyncio.run, create_task và cooperative scheduling

- **Thông điệp:** asyncio.run quản lý entry event loop; create_task cho phép tiến triển đồng thời khi coroutine thực sự nhường quyền.
- **Nội dung:** Một async entry point; create_task; giữ reference; asyncio.sleep; time.sleep block loop; CPU loop không await.
- **Minh họa/code/diagram:** Scheduling trace ba task và phản ví dụ time.sleep.
- **Lời giải thích:** create_task không bảo đảm task chạy xong nếu chương trình thoát hoặc không quản lý. Điểm await trên operation đã sẵn sàng có thể không tạo mức xen kẽ như người viết tưởng.
- **Câu hỏi chuyển:** “Thu nhiều kết quả với ngữ nghĩa nào?”

#### Slide 29 — gather, wait và as_completed

- **Thông điệp:** Chọn primitive theo ordering, mức điều khiển và cách muốn quan sát lỗi.
- **Nội dung:** gather giữ vị trí kết quả; wait trả done/pending; as_completed theo completion; cancellation/exception ở mức tổng quan.
- **Minh họa/code/diagram:** Bốn task thời gian khác nhau; bảng so sánh.
- **Lời giải thích:** Không nói một primitive luôn tốt hơn. Ngữ nghĩa exception phải kiểm tra đúng phiên bản; phần reliability do TV5 đào sâu.
- **Câu hỏi chuyển:** “Nếu một nhóm task cùng thuộc một thao tác, quản lý vòng đời có cấu trúc thế nào?”

#### Slide 30 — TaskGroup và structured concurrency

- **Thông điệp:** Structured concurrency gắn vòng đời child task vào một scope rõ ràng.
- **Nội dung:** TaskGroup context; tạo child; chờ scope; sibling cancellation khi lỗi; ExceptionGroup chuyển TV5.
- **Minh họa/code/diagram:** Cây parent–children có scope enter/exit.
- **Lời giải thích:** So với fire-and-forget, TaskGroup giảm orphan task và làm cleanup/error propagation rõ hơn. Không khẳng định thay thế mọi gather use case.
- **Câu hỏi chuyển:** “Ngoài coroutine thông thường, Python hỗ trợ stream và resource async bằng cú pháp nào?”

#### Slide 31 — Async iteration, async generator và async context

- **Thông điệp:** async for và async with cho phép chờ trong quá trình lặp và quản lý tài nguyên.
- **Nội dung:** Async iterator/generator; stream item theo thời gian; async context manager; acquire/release có await; use case sensor stream.
- **Minh họa/code/diagram:** Pseudocode async generator và async with; sequence diagram mở–dùng–đóng.
- **Lời giải thích:** Đây là mở rộng trực tiếp giúp code async có cấu trúc. Không đưa low-level magic methods quá sâu lên slide chính; để phụ lục nếu cần.
- **Câu hỏi chuyển:** “Nếu thư viện chỉ có hàm blocking hoặc CPU-heavy thì tích hợp vào loop ra sao?”

#### Slide 32 — Cô lập blocking code và mode async

- **Thông điệp:** Event loop phải được giữ phản hồi bằng cách đưa blocking work ra thread/process thích hợp.
- **Nội dung:** to_thread cho blocking function phù hợp; run_in_executor/bridge; CPU stage gửi process pool; demo async fetch; phản ví dụ block loop.
- **Minh họa/code/diagram:** Event loop → thread adapter/process pool; pseudocode mode async.
- **Lời giải thích:** Không biến mọi hàm sync thành async chỉ bằng từ khóa. Hành vi bên trong quyết định loop có bị block. Bàn giao timeout/queue/cancel cho TV5.
- **Câu hỏi chuyển:** “Nếu task chậm, lỗi hoặc cần hủy, hệ thống giữ nhất quán thế nào?”

### 10.4. Bản rút gọn sáu slide

1. Giữ slide 25.
2. Ghép slide 26+27: “Coroutine, Task và Future”.
3. Giữ slide 28.
4. Giữ slide 29.
5. Ghép slide 30+31: “Structured concurrency và cấu trúc async”.
6. Giữ slide 32.

### 10.5. Ba slide phụ lục — P10 đến P12

#### P10 — Scheduling trace từng bước

- **Thông điệp:** Muốn hiểu asyncio phải theo dõi từng đoạn chạy và điểm await.
- **Nội dung:** Ba task, timer khác nhau, ready/waiting transitions và output order.
- **Minh họa/code/diagram:** Timeline có số thứ tự từng bước.
- **Lời giải thích:** Yêu cầu cả nhóm dự đoán log trước khi xem đáp án.
- **Câu hỏi chuyển:** “Điểm await nào không tạo cơ hội cho task khác?”

#### P11 — Coroutine, Task và Future cheat sheet

- **Thông điệp:** Tạo ra, schedule và lưu kết quả là ba vai trò khác.
- **Nội dung:** Ai tạo, ai schedule, await được không, thuộc loop/executor nào, cancellation.
- **Minh họa/code/diagram:** Bảng type comparison.
- **Lời giải thích:** Phối hợp TV2 để tránh định nghĩa mâu thuẫn.
- **Câu hỏi chuyển:** “Có thể await trực tiếp concurrent Future không, hay cần bridge?”

#### P12 — Anti-pattern block event loop

- **Thông điệp:** Một lời gọi blocking có thể đóng băng mọi task cùng loop.
- **Nội dung:** time.sleep, sync network/file, CPU loop, callback dài; cách cô lập.
- **Minh họa/code/diagram:** Code sai/đúng và latency spike.
- **Lời giải thích:** Không hứa to_thread phù hợp với mọi CPU workload.
- **Câu hỏi chuyển:** “Ta đo loop responsiveness bằng dấu hiệu nào?”

### 10.6. Đóng góp demo

- Đặc tả coroutine lấy dữ liệu từng trạm.
- Thiết kế mode asyncio và scheduling trace.
- Chuẩn bị phản ví dụ time.sleep/CPU trong loop và cách sửa.
- Xác định cách bridge CPU stage sang ProcessPool.

### 10.7. Deliverables

- Tài liệu asyncio core 18–22 trang.
- Event-loop diagram, ba scheduling trace và type comparison.
- Hai ví dụ đúng, hai phản ví dụ.
- Đặc tả mode async; chưa viết code.
- 12 câu trắc nghiệm, 6 câu tự luận, 2 bài debug.
- Biên bản review phần TV1.

### 10.8. Câu hỏi phản biện

1. Gọi async function có chạy code ngay không?
2. Coroutine khác Task thế nào?
3. asyncio.Future khác concurrent Future thế nào?
4. create_task có tự bảo đảm task hoàn thành không?
5. await có luôn nhường quyền không?
6. asyncio.sleep khác time.sleep ra sao?
7. gather và as_completed khác ordering thế nào?
8. TaskGroup giải quyết vấn đề gì?
9. Khi nào dùng async generator?
10. Tại sao CPU-heavy code làm loop mất phản hồi?

### 10.9. Tiêu chí đạt, GitHub role và backup

TV4 đạt khi vẽ event-loop trace, dự đoán output order, phân biệt đúng type, sửa block-loop anti-pattern, bảo vệ TaskGroup và trình bày thay TV1.

- **GitHub role:** diagram/story-flow owner; chuẩn hóa màu, ký hiệu, timeline, state diagram và câu chuyển.
- **Reviewer/backup của TV4:** TV1.
- **TV4 review/backup cho:** TV1.

---

## 11. Thành viên 5 — Điều phối, lỗi và độ tin cậy

### 11.1. Mục tiêu

TV5 biến chương trình “chạy được khi mọi thứ tốt” thành chương trình xử lý được lỗi, hủy, tải cao và cleanup. TV5 phải:

- Giải thích cancellation như control flow.
- Thiết kế timeout và cleanup đúng.
- Trình bày exception propagation/ExceptionGroup.
- Chọn đúng synchronization primitive.
- Thiết kế Queue/backpressure và concurrency limit.
- Xây retry có giới hạn, jitter và idempotency.
- Dạy cả nhóm debug task leak và race qua await.

### 11.2. Kiến thức phải học sâu

- Cancellation propagation và CancelledError theo phiên bản.
- Timeout context/API và khác biệt wait_for.
- try/finally, async context, shield có kiểm soát.
- TaskGroup failure semantics và ExceptionGroup.
- Lock/Event/Condition/Semaphore/BoundedSemaphore/Barrier.
- Queue producer–consumer và backpressure.
- Retry/backoff/jitter/idempotency.
- Graceful shutdown, debug/logging và async testing.

### 11.3. Tám slide chuẩn — slide 33 đến 40

#### Slide 33 — Failure model của chương trình async

- **Thông điệp:** Hệ thống phải định nghĩa cách xử lý success, slow, timeout, error và cancel trước khi chạy.
- **Nội dung:** Năm outcome; local failure so với operation-wide failure; partial result; policy thay vì catch-all.
- **Minh họa/code/diagram:** Outcome tree của một trạm và toàn pipeline.
- **Lời giải thích:** Không coi exception là trường hợp hiếm. Với nhiều task, lỗi có thể xảy ra đồng thời và cần policy rõ.
- **Câu hỏi chuyển:** “Timeout có đồng nghĩa tác vụ đã dừng hoàn toàn không?”

#### Slide 34 — Timeout và cancellation

- **Thông điệp:** Timeout là giới hạn chờ; cancellation cần propagation và cooperation để cleanup.
- **Nội dung:** Timeout scope; cancel request; CancelledError; parent/child propagation; khác biệt API theo Python mục tiêu.
- **Minh họa/code/diagram:** State/timeline caller timeout → cancel → finally → done.
- **Lời giải thích:** Không nuốt cancellation vô ý. Nêu việc một operation bên dưới có thể chưa dừng tức thì. Phải xác minh semantics từ tài liệu chính thức.
- **Câu hỏi chuyển:** “Tài nguyên mở và trạng thái dở dang được xử lý ở đâu?”

#### Slide 35 — Cleanup, shield và graceful shutdown

- **Thông điệp:** try/finally và scope rõ ràng bảo vệ tài nguyên; shield chỉ dùng khi hiểu trách nhiệm vòng đời.
- **Nội dung:** Cleanup trong finally; async with; shield caveat; đóng producer, drain consumer, cancel pending, await cleanup.
- **Minh họa/code/diagram:** Shutdown sequence diagram.
- **Lời giải thích:** Shield không làm task bất tử và có thể làm task tiếp tục ngoài caller nếu quản lý kém. Cleanup cũng phải có thời hạn/policy.
- **Câu hỏi chuyển:** “Nếu nhiều child cùng lỗi, parent nhìn thấy gì?”

#### Slide 36 — Exception propagation và structured failure

- **Thông điệp:** Cách gom task quyết định cách lỗi truyền, task còn lại bị xử lý và nhiều lỗi được biểu diễn.
- **Nội dung:** gather options ở mức phiên bản; TaskGroup sibling cancellation; ExceptionGroup; xử lý lỗi cụ thể; không catch BaseException bừa.
- **Minh họa/code/diagram:** Cây ba child với hai lỗi và một sibling bị cancel.
- **Lời giải thích:** Phối hợp TV4, tránh lặp syntax. TV5 tập trung hậu quả và policy: fail-fast, best-effort hay partial result.
- **Câu hỏi chuyển:** “Một event-loop thread có cần Lock không?”

#### Slide 37 — Race condition và synchronization primitives

- **Thông điệp:** Race vẫn xảy ra nếu invariant bị chia cắt bởi await.
- **Nội dung:** Read–await–modify; Lock; Event; Condition; Barrier; use case; lock scope; không await I/O dài khi giữ lock nếu tránh được.
- **Minh họa/code/diagram:** Interleaving hai coroutine vi phạm invariant; bảng primitive.
- **Lời giải thích:** Một task chạy tại một thời điểm không có nghĩa chuỗi thao tác nghiệp vụ atomic. Chọn primitive theo tín hiệu/trạng thái/tài nguyên.
- **Câu hỏi chuyển:** “Làm sao giới hạn số thao tác ngoài hệ thống cùng lúc?”

#### Slide 38 — Semaphore và giới hạn concurrency

- **Thông điệp:** Semaphore giới hạn số operation đồng thời, nhưng không tự tạo rate limit theo thời gian.
- **Nội dung:** Semaphore/BoundedSemaphore; connection quota; acquire/release bằng async with; fairness caveat; concurrency limit versus requests/second.
- **Minh họa/code/diagram:** Mười task qua ba permit; bảng concurrency/rate.
- **Lời giải thích:** Chọn limit theo tài nguyên thật. Limit quá thấp giảm throughput; quá cao gây overload/timeouts.
- **Câu hỏi chuyển:** “Giới hạn task đang chạy có đủ khi producer tạo dữ liệu nhanh hơn consumer?”

#### Slide 39 — Queue, producer–consumer và backpressure

- **Thông điệp:** Bounded Queue truyền áp lực ngược để hệ thống không tích lũy vô hạn.
- **Nội dung:** put/get; maxsize; task_done/join; sentinel hoặc close protocol; nhiều producer/consumer; queue full.
- **Minh họa/code/diagram:** Pipeline producer → bounded queue → consumers với mức nước.
- **Lời giải thích:** Unbounded Queue có thể che overload cho tới khi hết memory. task_done phải khớp item được xử lý, kể cả đường lỗi.
- **Câu hỏi chuyển:** “Khi I/O tạm lỗi, có nên retry mọi lần ngay lập tức không?”

#### Slide 40 — Retry, observability và mode chịu lỗi

- **Thông điệp:** Retry chỉ an toàn khi có giới hạn, delay, jitter, phân loại lỗi và idempotency.
- **Nội dung:** Transient/permanent error; max attempts; exponential backoff; jitter; idempotent operation; log task/station/attempt; debug mode; failure injection.
- **Minh họa/code/diagram:** Retry timeline và structured log mẫu; pseudocode policy.
- **Lời giải thích:** Retry storm có thể làm hệ thống xấu hơn. Kết thúc bằng mode robust của demo và bàn giao tích hợp cho TV6.
- **Câu hỏi chuyển:** “Gộp tất cả công cụ thành một kiến trúc có thể giải thích và đo được thế nào?”

### 11.4. Bản rút gọn sáu slide

1. Giữ slide 33.
2. Ghép slide 34+35: “Timeout, cancellation và cleanup”.
3. Giữ slide 36.
4. Giữ slide 37.
5. Ghép slide 38+39: “Giới hạn concurrency và backpressure”.
6. Giữ slide 40.

### 11.5. Ba slide phụ lục — P13 đến P15

#### P13 — Bảng synchronization primitives

- **Thông điệp:** Primitive được chọn theo invariant và kiểu phối hợp.
- **Nội dung:** Lock/Event/Condition/Semaphore/BoundedSemaphore/Barrier/Queue; ownership; lỗi thường gặp.
- **Minh họa/code/diagram:** Decision table.
- **Lời giải thích:** Không dùng Lock như đáp án mặc định.
- **Câu hỏi chuyển:** “Đây là bảo vệ shared state hay giới hạn capacity?”

#### P14 — Cancellation và cleanup checklist

- **Thông điệp:** Mọi đường hủy phải kết thúc ở trạng thái biết được và không rò tài nguyên.
- **Nội dung:** Propagate, finally, await child, close resource, timeout cleanup, observe exception.
- **Minh họa/code/diagram:** Checklist và state diagram.
- **Lời giải thích:** Áp dụng cả demo trực tiếp và shutdown cuối chương trình.
- **Câu hỏi chuyển:** “Task nào còn sống sau khi scope thoát?”

#### P15 — Failure injection matrix

- **Thông điệp:** Độ tin cậy phải được thử bằng lỗi có chủ đích.
- **Nội dung:** Slow station, timeout, transient error, permanent error, queue full, consumer crash, cancel user; expected behavior.
- **Minh họa/code/diagram:** Matrix fault → expected signal → cleanup → metric.
- **Lời giải thích:** Một test pass chỉ khi cả output và trạng thái tài nguyên đúng.
- **Câu hỏi chuyển:** “Hệ thống có phân biệt partial success với total failure không?”

### 11.6. Đóng góp demo

- Đặc tả bounded Queue và Semaphore.
- Chính sách timeout/retry/backoff/idempotency.
- Cancellation toàn pipeline và graceful shutdown.
- Failure-injection matrix và expected behavior.

### 11.7. Deliverables

- Tài liệu reliability/coordination 18–22 trang.
- Primitive table, cancellation state diagram và shutdown sequence.
- Hai race/resource-leak phản ví dụ và cách sửa.
- Đặc tả robust mode/test matrix; chưa viết code.
- 12 câu trắc nghiệm, 6 câu tự luận, 2 bài debug.
- Biên bản review phần TV2.

### 11.8. Câu hỏi phản biện

1. Timeout có bảo đảm operation đã dừng không?
2. Vì sao không nên nuốt cancellation?
3. shield bảo vệ điều gì và tạo rủi ro gì?
4. TaskGroup xử lý sibling khi một child lỗi ra sao?
5. Một thread event loop vì sao vẫn có race?
6. Lock khác Semaphore thế nào?
7. Semaphore có phải rate limiter không?
8. Queue maxsize tạo backpressure ra sao?
9. Retry khi nào làm tình hình xấu hơn?
10. Idempotency liên quan retry thế nào?

### 11.9. Tiêu chí đạt, GitHub role và backup

TV5 đạt khi dự đoán propagation, sửa race, chọn đúng primitive, thiết kế shutdown/failure policy, trình bày thay TV2 và chứng minh không có orphan task trong thiết kế.

- **GitHub role:** QA/failure owner; gom câu hỏi, rubric, fault matrix và kiểm tra đường lỗi.
- **Reviewer/backup của TV5:** TV2.
- **TV5 review/backup cho:** TV2.

---

## 12. Thành viên 6 — Kiến trúc tích hợp, lựa chọn và liên hệ phân tán

### 12.1. Mục tiêu

TV6 kết nối các mảnh thành một quy trình ra quyết định và demo thống nhất. TV6 không làm thay năm người còn lại. TV6 phải:

- Xây decision tree dựa trên workload, correctness và chi phí.
- Thiết kế pipeline hybrid async I/O + process CPU.
- Tổng hợp kết quả theo cùng baseline.
- Phân biệt rõ async, concurrent, parallel và distributed.
- Trình bày giới hạn, anti-pattern và khi không nên dùng async.
- Quản lý runbook/rehearsal/release trên GitHub.

### 12.2. Kiến thức phải học sâu

- Architecture trade-off và boundary giữa sync/async.
- Resource budgeting: workers, tasks, queue, connection và memory.
- Hybrid bridge, ownership và shutdown order.
- Correctness/observability/performance report.
- Distributed concerns: network, partial failure, duplicate, ordering, idempotency.
- Ecosystem overview có giới hạn.
- Nền tảng ProcessPool đủ để review TV3.

### 12.3. Tám slide chuẩn — slide 41 đến 48

#### Slide 41 — Không có một công cụ thắng mọi workload

- **Thông điệp:** Lựa chọn bắt đầu từ nút thắt, ràng buộc và độ phức tạp chấp nhận được.
- **Nội dung:** Sequential, thread, process, asyncio, hybrid; workload; latency; throughput; memory; library sync/async; team skill.
- **Minh họa/code/diagram:** Decision matrix năm phương án.
- **Lời giải thích:** Sequential là lựa chọn tốt khi workload nhỏ hoặc complexity cost lớn. Không dùng async chỉ để “hiện đại”.
- **Câu hỏi chuyển:** “Quy trình chọn công cụ có thể biến thành decision tree không?”

#### Slide 42 — Decision tree từ bài toán tới công cụ

- **Thông điệp:** Đo, phân loại, chọn ứng viên, kiểm tra đúng, benchmark rồi mới chốt.
- **Nội dung:** Có concurrency hữu ích không; blocking I/O hay async API; CPU pure Python hay native; dữ liệu truyền; yêu cầu cancellation/backpressure; complexity budget.
- **Minh họa/code/diagram:** Cây quyết định có nhánh “giữ tuần tự”.
- **Lời giải thích:** Cây không phải định luật. Mỗi lá có điều kiện đo lại. Nêu ví dụ cảm biến đi qua cây.
- **Câu hỏi chuyển:** “Workload vừa có I/O vừa có CPU thì kiến trúc nào?”

#### Slide 43 — Kiến trúc hybrid

- **Thông điệp:** Dùng event loop cho I/O và process pool cho CPU, với boundary và ownership rõ.
- **Nội dung:** Async producers; bounded queue; validation; ProcessPool; aggregation; result/error channel; shutdown order.
- **Minh họa/code/diagram:** Sơ đồ hybrid đầy đủ, tô màu module TV1–TV6.
- **Lời giải thích:** Không tạo process cho từng request. Pool sống theo application scope. Dữ liệu qua boundary phải serializable và đủ thô.
- **Câu hỏi chuyển:** “Giới hạn tài nguyên toàn pipeline được tính thế nào?”

#### Slide 44 — Resource budget và backpressure toàn hệ thống

- **Thông điệp:** Worker, Task, Queue, connection và memory phải được thiết kế như một ngân sách chung.
- **Nội dung:** Concurrency cap; queue maxsize; process workers; input rate/output rate; overload policy; admission control.
- **Minh họa/code/diagram:** Bảng resource budget và bottleneck map.
- **Lời giải thích:** Tăng async tasks trong khi CPU consumers cố định chỉ đẩy backlog vào Queue. Cần xem end-to-end, không tối ưu từng stage cô lập.
- **Câu hỏi chuyển:** “Ta chứng minh năm mode vừa đúng vừa nhanh bằng báo cáo nào?”

#### Slide 45 — Correctness và benchmark end-to-end

- **Thông điệp:** Chỉ so thời gian sau khi output equivalence và đường lỗi đã được xác minh.
- **Nội dung:** Fixed seed; digest; successful/failed count; latency/throughput; repetitions; environment; small/large workload.
- **Minh họa/code/diagram:** Dashboard/bảng năm mode và correctness column.
- **Lời giải thích:** Không chọn riêng lần chạy nhanh nhất. Phân biệt kết quả dự kiến với kết quả đã đo. Nếu chưa code thì slide chỉ là schema, không bịa số.
- **Câu hỏi chuyển:** “Async trên một máy liên hệ với môn tính toán phân tán thế nào?”

#### Slide 46 — Async không đồng nhất với distributed

- **Thông điệp:** Async là mô hình điều phối; distributed thêm ranh giới máy và failure model mới.
- **Nội dung:** Một process/máy so với nhiều node; network latency; partial failure; duplicate; ordering; clock; idempotency; serialization.
- **Minh họa/code/diagram:** Một event loop trên máy A so với ba node nối mạng.
- **Lời giải thích:** Không biến phần này thành một chương distributed systems khác. Chỉ ra async thường dùng để quản lý network I/O trong distributed app, nhưng hai khái niệm vẫn khác.
- **Câu hỏi chuyển:** “Những anti-pattern nào làm thiết kế đúng lý thuyết nhưng thất bại thực tế?”

#### Slide 47 — Anti-pattern và giới hạn

- **Thông điệp:** Async có giá trị khi xử lý đúng vấn đề; dùng sai làm code phức tạp, khó debug và có thể chậm hơn.
- **Nội dung:** Async-all-the-things; fire-and-forget; unbounded gather; blocking loop; tiny ProcessPool tasks; shared mutable state; retry storm; benchmark cherry-picking.
- **Minh họa/code/diagram:** Bảng anti-pattern → hậu quả → cách sửa.
- **Lời giải thích:** Kết nối lỗi từ tất cả thành viên. Đưa tiêu chí giữ sequential hoặc dùng giải pháp đơn giản hơn.
- **Câu hỏi chuyển:** “Ba kết luận nào người nghe phải mang về?”

#### Slide 48 — Tổng kết, demo và bản đồ kiến thức

- **Thông điệp:** Phân loại workload, chọn abstraction phù hợp, bảo vệ correctness/reliability và đo trên dữ liệu thật.
- **Nội dung:** Tóm tắt bốn nguyên tắc; năm mode demo; kết quả học; giới hạn; đường dẫn tài liệu GitHub; mời câu hỏi.
- **Minh họa/code/diagram:** Bản đồ từ vấn đề → công cụ → an toàn → đo lường; QR/link repo sau này.
- **Lời giải thích:** Không chỉ liệt kê. Quay lại câu hỏi slide 1 và trả lời bằng decision framework. Trong demo, mỗi thành viên giải thích stage mình sở hữu.
- **Câu hỏi chuyển:** “Với một workload mới, bước đầu tiên bạn sẽ đo hoặc hỏi điều gì?”

### 12.4. Bản rút gọn sáu slide

1. Giữ slide 41.
2. Giữ slide 42.
3. Ghép slide 43+44: “Hybrid architecture và resource budget”.
4. Giữ slide 45.
5. Ghép slide 46+47: “Phân tán, giới hạn và anti-pattern”.
6. Giữ slide 48.

### 12.5. Ba slide phụ lục — P16 đến P18

#### P16 — Decision matrix đầy đủ

- **Thông điệp:** Quyết định là trade-off nhiều chiều.
- **Nội dung:** Workload, parallelism, memory, startup, serialization, cancellation, library support, complexity, portability.
- **Minh họa/code/diagram:** Bảng năm phương án.
- **Lời giải thích:** Mỗi ô dùng “thường/phụ thuộc”, tránh tuyệt đối hóa.
- **Câu hỏi chuyển:** “Yếu tố nào là constraint cứng của bài toán hiện tại?”

#### P17 — Demo runbook và fallback

- **Thông điệp:** Demo đáng tin phải tái lập, giới hạn thời gian và có phương án dự phòng.
- **Nội dung:** Environment check, command order, seed, expected output, timeout, recorded result, người nói mỗi stage.
- **Minh họa/code/diagram:** Timeline demo 8–10 phút.
- **Lời giải thích:** Không live-edit code; không phụ thuộc Internet; dừng đúng thời lượng.
- **Câu hỏi chuyển:** “Nếu máy không chạy ProcessPool thì nhóm chứng minh kiến thức bằng gì?”

#### P18 — Async ecosystem và hướng mở rộng

- **Thông điệp:** Thư viện ngoài chuẩn mở rộng I/O và structured concurrency nhưng không thay đổi nền tảng quyết định.
- **Nội dung:** aiohttp/AnyIO/Trio/framework chỉ ở mức vai trò; distributed queue là lớp khác; tiêu chí chọn dependency.
- **Minh họa/code/diagram:** Ecosystem map có ranh giới “trong phạm vi/ngoài phạm vi”.
- **Lời giải thích:** Không quảng cáo công cụ; chỉ định hướng học tiếp và ghi rõ chưa triển khai.
- **Câu hỏi chuyển:** “Khái niệm nào từ Chương 4 vẫn giữ nguyên khi đổi framework?”

### 12.6. Đóng góp demo

- Tích hợp đặc tả năm mode; không viết thay module.
- Định nghĩa CLI/runbook/output/report schema.
- Thiết kế hybrid diagram và shutdown order.
- Điều phối phần trình diễn để mỗi người giải thích stage của mình.

### 12.7. Deliverables

- Tài liệu decision/integration/distributed 15–20 trang.
- Decision tree, decision matrix, hybrid architecture và resource budget.
- Demo specification tổng, runbook và fallback.
- Report schema năm mode; chưa có số liệu giả.
- 12 câu trắc nghiệm, 6 câu tự luận, 2 bài debug/architecture.
- Biên bản review phần TV3.

### 12.8. Câu hỏi phản biện

1. Khi nào sequential là lựa chọn tốt nhất?
2. Khi nào ThreadPool và asyncio đều là ứng viên?
3. Khi nào ProcessPool không đáng chi phí?
4. Boundary async–process đặt ở đâu?
5. Queue lớn có giải quyết overload không?
6. Vì sao cần resource budget end-to-end?
7. Async khác distributed thế nào?
8. Partial failure là gì?
9. Tại sao không được bịa speedup trước khi đo?
10. Nếu demo lỗi, bằng chứng dự phòng nào vẫn chứng minh kết luận?

### 12.9. Tiêu chí đạt, GitHub role và backup

TV6 đạt khi dùng decision tree cho tình huống mới, giải thích hybrid/shutdown/resource budget, phân biệt async–distributed, bảo vệ benchmark report và trình bày thay TV3.

- **GitHub role:** integration/release/rehearsal owner; quản lý milestone, runbook, rehearsal và bản chốt.
- **Reviewer/backup của TV6:** TV3.
- **TV6 review/backup cho:** TV3.

---

# PHẦN II — HỌC CHÉO, KIỂM TRA VÀ NGHIỆM THU

## 13. Cơ chế học chéo bắt buộc

### 13.1. Vòng 1 — Diagnostic

- Đề 30 câu bao phủ cả sáu cụm.
- Không tính điểm; dùng để nhận diện lỗ hổng.
- Mỗi người ghi ba phần yếu nhất và lịch bù.

### 13.2. Vòng 2 — Hồ sơ chuyên môn

Mỗi chuyên gia viết phần mình theo template:

1. Vấn đề.
2. Mục tiêu học.
3. Kiến thức tiên quyết.
4. Thuật ngữ.
5. Mental model.
6. Cơ chế/state/lifecycle.
7. API hoặc quy tắc.
8. Timeline/diagram.
9. Ví dụ đúng.
10. Giải thích từng khối.
11. Phản ví dụ.
12. Lỗi thường gặp.
13. Correctness.
14. Performance/overhead.
15. Version/platform caveat.
16. Test/failure scenario.
17. Câu hỏi phản biện.
18. Nguồn chính thức.

### 13.3. Vòng 3 — Teach-back

- Mỗi chuyên gia dạy 25–30 phút.
- Reviewer đặt ít nhất năm câu hỏi.
- Bốn người còn lại viết bản tóm tắt bằng lời của mình.
- Mỗi người phải nêu một điều “trước đây hiểu sai” và cách sửa.

### 13.4. Vòng 4 — Lab chung

Cả sáu phải làm:

- Dự đoán output order của Future và coroutine.
- Tìm coroutine chưa await.
- Tìm lời gọi blocking trong event loop.
- Sửa race condition qua await.
- Phân tích pool deadlock.
- Sửa lỗi pickle/main guard.
- Thiết kế timeout/cancellation/cleanup.
- Giải thích benchmark thay đổi theo task size.

### 13.5. Vòng 5 — Quiz chéo

Mỗi người nộp 20 mục:

- 12 câu trắc nghiệm.
- 6 câu tự luận.
- 2 bài đọc code/debug.

Ngân hàng chung có 120 mục. Mỗi thành viên làm đề ngẫu nhiên:

- Tối thiểu 85% tổng điểm.
- Không cụm nào dưới 70%.
- Không đạt phải học và thi lại bằng đề khác.

### 13.6. Vòng 6 — Bảo vệ miệng

Mỗi người:

- Trả lời sáu câu ngẫu nhiên, mỗi cụm một câu.
- Tóm tắt ba phút về phần không phải chuyên môn.
- Giải thích một diagram/code do người khác tạo.
- Sửa một lỗi chưa biết trước.
- Nêu một trường hợp không nên dùng công cụ đang nói.

### 13.7. Vòng 7 — Hoán đổi người nói

- Reviewer trình bày toàn bộ phần của chuyên gia.
- Chuyên gia chỉ được ghi chú lỗi sau khi reviewer nói xong.
- Nhóm bốc thăm một thành viên khác trả lời Q&A.
- Chỉ chốt khi mỗi cụm có hai người nói đầy đủ và bốn người tóm tắt đúng.

---

## 14. Phân công demo theo stage

| Thành viên | Stage sở hữu | Stage phải kiểm tra chéo |
|---|---|---|
| TV1 | Data contract, sequential baseline, correctness oracle | Async scheduling của TV4 |
| TV2 | Blocking fetch, ThreadPool mode, Future error paths | Reliability policy của TV5 |
| TV3 | CPU analysis, ProcessPool mode, benchmark | Integration/report của TV6 |
| TV4 | Async fetch, event-loop trace, blocking anti-pattern | Baseline/terminology của TV1 |
| TV5 | Queue, Semaphore, timeout, retry, cancellation | Thread/Future paths của TV2 |
| TV6 | CLI/spec integration, hybrid architecture, runbook | Process/platform paths của TV3 |

Khi demo:

- TV6 điều khiển luồng trình diễn.
- Mỗi thành viên có 45–75 giây giải thích stage của mình.
- Người sở hữu nêu cơ chế.
- Reviewer nêu failure/giới hạn.
- Bảng kết quả chỉ hiện số đã đo thật sau khi demo được triển khai.

---

## 15. Quy trình GitHub

### 15.1. Epic và Issue

Mỗi cụm kiến thức là một Epic. Mỗi thành viên có tối thiểu các Issue:

1. Đối chiếu file gốc.
2. Nghiên cứu nguồn chính thức.
3. Viết hồ sơ kiến thức.
4. Thiết kế tám slide chuẩn.
5. Thiết kế sáu slide rút gọn.
6. Thiết kế ba slide phụ lục.
7. Ví dụ đúng/phản ví dụ.
8. Demo specification.
9. Test/failure plan.
10. Question bank.
11. Reviewer pass.
12. Rehearsal fix.

### 15.2. Branch và Pull Request

- Không commit trực tiếp vào main.
- Tên branch gợi ý: member-1/foundations, member-2/futures-threadpool, member-3/process-performance, member-4/asyncio-core, member-5/reliability, member-6/integration.
- Một PR chỉ giải quyết một Issue hoặc một nhóm thay đổi liền mạch.
- PR phải nêu: phạm vi, nguồn, version, hình/code liên quan, cách tự kiểm, phần chưa chắc.
- Ít nhất reviewer/backup duyệt.
- Claim hiệu năng cần TV3 duyệt.
- Thuật ngữ mới cần TV1 duyệt.
- Failure/cancellation claim cần TV5 duyệt.
- Diagram/timeline chính cần TV4 duyệt.

### 15.3. Definition of Ready cho PR

PR chỉ mở review khi:

- Không còn placeholder mơ hồ.
- Có nguồn cho claim kỹ thuật.
- Có nhãn Core/Applied/Advanced.
- Có ví dụ hoặc diagram cho cơ chế khó.
- Có câu hỏi phản biện.
- Có version/platform note khi cần.
- Không upload trái phép tài liệu gốc của giảng viên.

---

## 16. Lịch thực hiện gợi ý 14 ngày

| Mốc | Công việc | Đầu ra |
|---|---|---|
| D−14 | Diagnostic, đọc file gốc, chốt scope | Coverage map và danh sách lỗ hổng |
| D−13 đến D−11 | Nghiên cứu chuyên môn, tìm nguồn | Source log và outline cấp mục |
| D−10 | Hồ sơ chuyên môn v1 | Sáu tài liệu module |
| D−9 | Reviewer pass 1 | Comment kỹ thuật và danh sách sửa |
| D−8 | Teach-back TV1–TV3 | Tóm tắt của sáu người |
| D−7 | Teach-back TV4–TV6 | Tóm tắt của sáu người |
| D−6 | Chốt 48/36/18 outline | Master slide outline, chưa làm PPTX |
| D−5 | Lab và demo specification | Năm mode, test/failure matrix |
| D−4 | Quiz chéo lần 1 | Điểm và kế hoạch học bù |
| D−3 | Rehearsal bản chuẩn | Timing, transition, Q&A log |
| D−2 | Hoán đổi người nói và thi lại | Backup sign-off |
| D−1 | Freeze tài liệu | Release candidate |
| D0 | Báo cáo | Runbook và phân công Q&A |

Nếu có nhiều thời gian hơn, giữ nguyên thứ tự và kéo dài giai đoạn nghiên cứu/review, không bỏ cổng kiểm tra.

---

## 17. Cổng nghiệm thu

### Gate 1 — Bao phủ

- Đối chiếu từng trang/ý trong file gốc.
- Không chủ đề bắt buộc nào chỉ xuất hiện dưới dạng tên.
- Phần nền tảng/mở rộng có nhãn rõ.

### Gate 2 — Chính xác

- Thuật ngữ nhất quán.
- API đúng phiên bản Python mục tiêu.
- Không dùng tên sai concurrent.future; module chuẩn là concurrent.futures.
- Mọi claim GIL/TaskGroup/timeout/cancellation có phạm vi/version.

### Gate 3 — Giải thích được

- Mỗi cơ chế khó có timeline/state/sequence diagram.
- Có ví dụ đúng, phản ví dụ và lỗi thường gặp.
- Người nói giải thích được “vì sao”, không chỉ đọc syntax.

### Gate 4 — Kiểm chứng

- Demo specification có correctness oracle.
- Mỗi mode có test/failure plan.
- Benchmark protocol công bằng, tái lập.
- Không có số liệu giả hoặc cherry-picking.

### Gate 5 — Học chéo

- Cả sáu đạt 85%.
- Không cụm nào dưới 70%.
- Reviewer trình bày thay được.
- Mỗi người giải thích được stage demo của người khác.

### Gate 6 — Trình bày

- Bản 48 slide đúng timing.
- Bản 36 slide ghép hợp lý.
- 18 phụ lục tra cứu nhanh.
- Chuyển người không đứt mạch.
- Q&A có người chính và backup.

---

## 18. Definition of Done từng thành viên

Một thành viên chỉ được đánh dấu hoàn thành khi có đủ:

- Tài liệu chuyên môn theo template.
- Tám slide chuẩn ở mức outline.
- Mapping sáu slide rút gọn.
- Ba slide phụ lục.
- Mục tiêu và prerequisite.
- Ít nhất hai minh họa cơ chế.
- Ít nhất một ví dụ đúng và một phản ví dụ.
- Demo specification cho stage mình.
- Test/failure plan.
- 12 MCQ, 6 tự luận, 2 debug.
- Câu trả lời mẫu có nguồn.
- Review phần backup.
- Sửa hết comment nghiêm trọng.
- Teach-back và rehearsal.
- Vượt quiz/oral.
- Có thể trình bày phần backup.

---

## 19. Definition of Done toàn nhóm

Báo cáo chỉ hoàn thành khi:

1. Coverage map cho thấy đủ file gốc.
2. Nội dung mở rộng được gắn Core/Applied/Advanced.
3. Không còn định nghĩa mâu thuẫn.
4. Mọi API gắn với phiên bản Python đã chọn.
5. Mọi claim quan trọng có nguồn chính thức.
6. Không có đoạn code/diagram không ai giải thích được.
7. Demo có năm mode trong đặc tả.
8. Correctness được định nghĩa trước performance.
9. Benchmark có environment, seed, lặp và spread.
10. Có workload nhỏ và lớn để thấy overhead.
11. Có timeout, cancel, error, retry và backpressure scenario.
12. Không block event loop ở thiết kế đúng.
13. Process plan có main guard và pickle check.
14. Không tạo Task hoặc Queue vô hạn.
15. Mỗi module có chuyên gia và backup.
16. Cả sáu vượt chuẩn kiến thức chung.
17. Có bản 36, 48 và 18 phụ lục ở mức outline.
18. Có runbook và fallback cho demo sau này.
19. Không upload tài liệu giảng viên nếu chưa có quyền.
20. Chỉ tạo PPTX/PDF/code sau khi sườn này được nhóm duyệt.

---

## 20. Rubric tự đánh giá 100 điểm

| Hạng mục | Điểm | Điều kiện |
|---|---:|---|
| Bao phủ file gốc | 15 | Có traceability, không bỏ ý bắt buộc |
| Độ chính xác | 20 | Thuật ngữ/API/version đúng, nguồn rõ |
| Chiều sâu giải thích | 15 | Có why, lifecycle, timeline, phản ví dụ |
| Tính đúng đắn và độ tin cậy | 15 | Error/cancel/race/backpressure được xử lý |
| Demo và khả năng kiểm chứng | 15 | Năm mode, oracle, test, benchmark protocol |
| Khả năng trình bày | 10 | Mạch kể rõ, đúng thời lượng, visual có ý nghĩa |
| Hiểu biết đồng đều của nhóm | 10 | Quiz/oral/backup đạt chuẩn |

Điều kiện loại dù tổng điểm cao:

- Có claim kỹ thuật sai nghiêm trọng.
- Không phân biệt được async với parallel.
- Không có correctness oracle.
- Bịa kết quả benchmark.
- Chỉ một người hiểu demo.
- Không có người backup.

---

## 21. Bộ câu hỏi toàn nhóm phải trả lời được

1. Bất đồng bộ giải quyết loại lãng phí nào?
2. Concurrent nhưng không parallel là trường hợp nào?
3. Async và non-blocking có phải đồng nghĩa không?
4. I/O-bound và CPU-bound được xác định bằng gì?
5. Future đại diện cho gì?
6. cancel Future khi đang chạy có ý nghĩa gì?
7. map khác as_completed ở thứ tự nào?
8. ThreadPool có thể deadlock thế nào?
9. GIL giới hạn gì và không giới hạn gì?
10. ProcessPool cần pickle/main guard vì sao?
11. Tại sao ProcessPool có thể chậm hơn tuần tự?
12. Event loop làm gì khi coroutine await I/O?
13. Gọi async function có chạy ngay không?
14. Coroutine, Task và Future khác gì?
15. gather, wait, as_completed và TaskGroup chọn thế nào?
16. time.sleep trong coroutine gây gì?
17. CPU-heavy code tích hợp asyncio bằng cách nào?
18. Timeout khác cancellation thế nào?
19. Vì sao cancellation cần cleanup?
20. Một event loop thread có race condition không?
21. Lock, Semaphore và Queue giải quyết ba vấn đề gì?
22. Backpressure là gì?
23. Retry storm là gì và jitter giúp gì?
24. Structured concurrency giải quyết orphan task thế nào?
25. Benchmark concurrency phải giữ yếu tố nào giống nhau?
26. Vì sao correctness phải kiểm trước speed?
27. Khi nào giữ code tuần tự?
28. Hybrid async+process có boundary ở đâu?
29. Async khác distributed ở failure model nào?
30. Nếu demo trực tiếp lỗi, nhóm dùng bằng chứng nào?

---

## 22. Chính sách nguồn và kiểm chứng

Thứ tự ưu tiên:

1. File Chương 4 của môn học để xác định phạm vi bắt buộc.
2. Python Language Reference, Python Standard Library documentation và PEP liên quan.
3. Tài liệu chính thức của thư viện ngoài nếu phần định hướng nhắc tới.
4. Sách/bài viết chất lượng để tạo trực giác, nhưng không dùng thay nguồn chính thức cho semantics API.

Mỗi claim về API phải ghi:

- Tên API chính xác.
- Phiên bản Python mục tiêu.
- Link/nguồn.
- Nội dung nào là diễn giải của nhóm.
- Nội dung nào là kết quả thực nghiệm.

Không sao chép nguyên slide của nguồn. Có thể học cấu trúc, nhưng phải diễn giải bằng ngôn ngữ của nhóm, tự dựng diagram và ghi nguồn.

---

## 23. Kết luận phân công

Mô hình này tạo sáu chuyên gia nhưng không tạo sáu “ốc đảo kiến thức”:

- TV1 giữ nền tảng và thuật ngữ.
- TV2 làm chủ Future/Executor/ThreadPool.
- TV3 làm chủ ProcessPool/GIL/benchmark.
- TV4 làm chủ event loop/coroutine/Task.
- TV5 làm chủ reliability/coordination.
- TV6 làm chủ decision/integration/distributed relation.

Các cặp TV1↔TV4, TV2↔TV5 và TV3↔TV6 bảo đảm mỗi cụm có hai người nói được. Quiz, lab, hoán đổi người nói và demo chung buộc cả sáu người hiểu toàn bộ chuỗi từ nền tảng đến ứng dụng.

Đầu ra của giai đoạn này là **sườn được duyệt**. Chỉ sau khi chốt phạm vi, thời lượng, phiên bản Python và phân công tên thật mới bắt đầu làm PPTX, PDF hoặc code demo.
