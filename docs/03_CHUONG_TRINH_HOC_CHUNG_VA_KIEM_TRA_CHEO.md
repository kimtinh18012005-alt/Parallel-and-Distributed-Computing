# CHƯƠNG TRÌNH HỌC CHUNG VÀ KIỂM TRA CHÉO CHƯƠNG 4

| Thuộc tính | Giá trị |
|---|---|
| Vai trò | Kế hoạch đào tạo nội bộ và kiểm định năng lực |
| Đối tượng | 6 owner, 3 cặp backup |
| Chuẩn đầu ra | Toàn bộ chuỗi từ workload đến chương trình bất đồng bộ đúng và đo được |
| Bằng chứng | Lab, quiz, oral defense, teach-back và rehearsal |

## 1. Chuẩn đầu ra chung của cả sáu thành viên

Mỗi thành viên chỉ được xem là đã học xong Chương 4 khi đạt đồng thời bốn mức sau:

| Mức | Biểu hiện quan sát được | Ví dụ bằng chứng |
|---|---|---|
| 1 — Nhận biết | Định nghĩa đúng thuật ngữ, không trộn các cặp khái niệm | Phân biệt concurrency/parallelism và async/non-blocking |
| 2 — Giải thích | Vẽ và thuyết minh được cơ chế, vòng đời và luồng điều khiển | Tự vẽ event loop, trạng thái Future/Task, hàng đợi producer–consumer |
| 3 — Áp dụng | Đọc, chạy, sửa và dự đoán được mã ví dụ | Thêm timeout, giới hạn concurrency, xử lý cancellation đúng |
| 4 — Phân tích | Chọn công cụ, chỉ ra đánh đổi, phản biện kết quả | Giải thích vì sao async **có thể** giảm elapsed time hoặc tăng throughput khi chồng thời gian chờ I/O, nhưng không tự làm CPU-bound chạy song song |

Điểm cốt lõi là **năng lực giải thích và xử lý tình huống**, không phải học thuộc tên API. Một người thuộc cú pháp `async`/`await` nhưng không dự đoán được lúc nào coroutine nhường quyền thì chưa đạt. Một người biết chạy benchmark nhưng không kiểm tra tính tương đương của kết quả thì cũng chưa đạt.

## 2. Bộ 40 năng lực bắt buộc — ai cũng phải nắm

### Nhóm A — Bản đồ khái niệm

1. Mô tả được chương trình tuần tự và chỉ ra thời gian CPU làm việc, thời gian chờ I/O.
2. Phân biệt **concurrency** (nhiều công việc cùng tiến triển) và **parallelism** (nhiều công việc thực thi thật sự cùng thời điểm).
3. Phân biệt **synchronous/asynchronous** là cách phối hợp và nhận kết quả với **blocking/non-blocking** là hành vi chặn luồng thực thi.
4. Giải thích được vì sao “asynchronous”, “concurrent”, “parallel” không phải ba từ đồng nghĩa.
5. Nhận diện đúng I/O-bound, CPU-bound và workload hỗn hợp; biết rằng phải đo thay vì đoán.
6. So sánh process, thread và coroutine theo đơn vị lập lịch, bộ nhớ, chi phí chuyển ngữ cảnh, khả năng song song và kiểu lỗi.

### Nhóm B — Nền tảng Python và `concurrent.futures`

7. Giải thích GIL trong CPython thông thường và ngoại lệ quan trọng: I/O/C extension có thể nhả GIL; free-threaded build từ Python 3.13 là tùy chọn, không phải mặc định.
8. Mô tả giao kèo `Executor`: nhận callable, lập lịch cho worker, trả `Future`, quản lý shutdown.
9. Vẽ vòng đời `concurrent.futures.Future`: pending → running → finished hoặc cancelled; biết trạng thái nào không thể hủy.
10. Dùng và phân biệt `submit`, `map`, `wait`, `as_completed`; hiểu thứ tự đầu vào, thứ tự hoàn thành và nơi ngoại lệ được ném lại.
11. Chọn `ThreadPoolExecutor` cho I/O blocking và biết rủi ro race/deadlock/tài nguyên dùng chung.
12. Chọn `ProcessPoolExecutor` cho CPU-bound thuần Python; hiểu serialization/pickling, chi phí IPC, yêu cầu import được `__main__`, khác biệt nền tảng.
13. Giải thích vì sao gọi chờ Future khác trong worker pool có thể deadlock khi pool hết worker.
14. Quản lý vòng đời pool bằng context manager hoặc `shutdown`; không để tài nguyên sống mơ hồ.

### Nhóm C — Mô hình thực thi `asyncio`

15. Vẽ được event source → ready/timer/I/O queues → event loop → callback/Task → suspend/resume.
16. Giải thích `async def` tạo coroutine function và lời gọi tạo coroutine object; coroutine chưa tự chạy chỉ vì đã được tạo.
17. Giải thích `await` chỉ dùng với awaitable và là điểm có thể tạm dừng task hiện tại; `await` không đồng nghĩa tạo song song.
18. Phân biệt coroutine, awaitable, `asyncio.Task`, `asyncio.Future` và `concurrent.futures.Future`.
19. Biết `asyncio.run` chịu trách nhiệm tạo/đóng loop cho điểm vào cấp cao; không gọi lồng trong cùng thread đang có loop chạy.
20. Biết `create_task` lập lịch coroutine, cần giữ tham chiếu khi thích hợp, và phải quan sát kết quả/ngoại lệ.
21. So sánh tuần tự bằng hai lần `await` với concurrent bằng task; dự đoán timeline trước khi chạy.
22. So sánh `gather`, `wait`, `as_completed` và `TaskGroup` theo thứ tự kết quả, lỗi, timeout và cancellation.
23. Hiểu structured concurrency: task con có phạm vi sống rõ; lỗi một task trong `TaskGroup` dẫn tới hủy các sibling còn lại và có thể phát sinh `ExceptionGroup`.
24. Biết vai trò của `async with`, `async for`, asynchronous context manager, asynchronous iterator và asynchronous generator.

### Nhóm D — Tính đúng, độ tin cậy và kiểm soát tải

25. Xử lý timeout/deadline; phân biệt timeout một thao tác với ngân sách thời gian cho cả yêu cầu.
26. Hiểu cancellation là hợp tác: `CancelledError` được đưa vào task ở điểm nhường quyền; cleanup phải nằm trong `finally`/context manager và thường phải ném lại cancellation.
27. Biết khi nào `shield` bảo vệ awaitable con và vì sao nó không biến thao tác thành “không thể hủy”.
28. Nhận diện race condition dù chương trình chỉ có một event-loop thread: task có thể xen kẽ tại các điểm `await`.
29. Chọn đúng `Lock`, `Event`, `Condition`, `Semaphore`, `BoundedSemaphore`, `Barrier`; biết primitive của `asyncio` không thread-safe.
30. Dùng Queue hữu hạn để tạo backpressure; hiểu `put`, `get`, `task_done`, `join`, sentinel/shutdown và rủi ro quên `task_done`.
31. Không chạy code blocking/CPU nặng trực tiếp trên event loop; biết cầu nối `to_thread`, `run_in_executor`, `run_coroutine_threadsafe`, `call_soon_threadsafe` và phạm vi dùng.
32. Nhận diện deadlock, livelock, starvation, unbounded fan-out, retry storm, task leak và resource leak.

### Nhóm E — Kiểm chứng và quyết định kỹ thuật

33. Viết test cho success, partial failure, timeout, cancellation, cleanup, giới hạn concurrency và kết quả tương đương.
34. Dùng debug mode/logging/task introspection để tìm coroutine không được await, exception không được lấy, callback chậm và task còn treo.
35. Benchmark công bằng: warm-up, nhiều lần chạy, cùng input/output, tách I/O và CPU, báo median/p95 hoặc độ phân tán, không kết luận chỉ từ một lần.
36. Dùng cây quyết định: tuần tự khi đơn giản/ít việc; thread cho API blocking I/O; process cho CPU-bound; `asyncio` cho nhiều I/O có API async; phối hợp mô hình khi workload hỗn hợp.
37. Hiểu async I/O cấp ứng dụng: streams, `drain`, đóng kết nối, subprocess; biết đây là Applied và không cần nhồi mọi API mức thấp vào slide chính.
38. Ghi rõ baseline Python và caveat hệ điều hành; không dùng API 3.13/3.14 như thể có sẵn ở 3.11 và không dựa vào một process start method bất biến.
39. Thiết kế ownership và graceful shutdown: ngừng nhận việc, hủy/chờ task, làm sạch Queue, đóng stream/context, shutdown executor và xác nhận không còn công việc rò.
40. Phân biệt async trên một máy với distributed computing nhiều nút; liên hệ timeout, partial failure, duplicate, retry/backoff và idempotency mà không đánh đồng hai phạm vi.

## 3. Chuẩn “chuyên gia chính — người dự phòng — mọi người cùng biết”

Mỗi cụm kiến thức có ba tầng trách nhiệm:

- **Owner**: nghiên cứu sâu nhất, viết nội dung, tạo hình minh họa và chịu câu hỏi khó.
- **Reviewer/backup**: kiểm tra semantics, chạy lại ví dụ và có thể trình bày thay owner.
- **Bốn thành viên còn lại**: phải đạt 40 năng lực chung, làm quiz và trả lời được câu hỏi mức nền tảng–áp dụng.

| Cụm | Owner | Backup | Bằng chứng chung của cả sáu |
|---|---|---|---|
| Bản đồ khái niệm và nền tảng hệ thống | TV1 | TV4 | Tự hoàn thành ma trận 2×2 và cây chọn công cụ |
| `Future`, `Executor` và `ThreadPoolExecutor` | TV2 | TV5 | Chạy/trace được ví dụ submit–wait–as_completed |
| `ProcessPoolExecutor`, GIL, serialization và hiệu năng | TV3 | TV6 | Sửa được lỗi pickle/main guard và đọc benchmark |
| Event loop, coroutine, Task và structured concurrency | TV4 | TV1 | Tự vẽ timeline và dự đoán thứ tự log |
| Timeout, cancellation, đồng bộ, Queue và backpressure | TV5 | TV2 | Sửa được chương trình rò task/tài nguyên và quá tải |
| Kiến trúc lai, demo và liên hệ hệ thống phân tán | TV6 | TV3 | Chạy đủ biến thể, kiểm tra output, bảo vệ quyết định |

Không dùng mô hình “TV6 biết hết demo, năm người còn lại chỉ nói slide”. Mỗi thành viên phải clone repo, chạy cùng lệnh, biết cấu trúc input/output, chỉ ra một lỗi được tiêm vào và đọc được benchmark.

### 3.1. Cổng công bằng trước khi tính là hoàn thành

Owner khác nhau về chủ đề nhưng không khác nhau về lượng việc. Cả sáu cùng phải hoàn thành định mức 100 điểm/48 giờ trong tài liệu phân công: cùng khối lượng nghiên cứu, slide, tài sản minh họa, module demo, sáu loại test, ngân hàng 20 câu, teach-back, backup và GitHub. Vai trò tổng hợp không cho phép đẩy việc của người khác sang người điều phối.

Khi kiểm tra tiến độ, nhóm phải xem đồng thời ba lớp:

1. **Khối lượng:** điểm việc và giờ thực tế chênh không quá ngưỡng đã quy định.
2. **Chất lượng:** sản phẩm qua review, nguồn và test; không chỉ đủ số lượng.
3. **Kiến thức:** mọi người cùng đạt quiz/oral/lab, kể cả câu ngoài chuyên môn.

Nếu một người xong sớm, người đó nhận một task độc lập từ backlog chung qua GitHub issue; không sửa âm thầm hoặc làm hộ toàn bộ module của người khác.

## 4. Lộ trình học chung tám buổi

Mỗi buổi nên dài 90–120 phút. Nếu thời gian gấp, có thể ghép hai buổi nhưng không bỏ bài kiểm tra đầu ra.

### Buổi 1 — Khảo sát đầu vào và thống nhất thuật ngữ

**Trước buổi:** cả nhóm đọc 24 trang tài liệu gốc, đánh dấu câu chưa hiểu.

**Trong buổi:**

1. TV1 trình bày timeline tuần tự của ba thao tác I/O.
2. Sáu người tự điền bảng: sequential/concurrent/parallel/asynchronous.
3. Nhóm tranh luận bốn mệnh đề dễ sai: “async luôn nhanh”, “một thread không có concurrency”, “non-blocking chính là async”, “thread luôn chạy song song”.
4. Chốt glossary có cả tiếng Anh, tiếng Việt và một câu định nghĩa vận hành.

**Đầu ra:** mỗi người quay hoặc trình bày trực tiếp 3 phút giải thích bốn khái niệm mà không nhìn tài liệu.

### Buổi 2 — Workload, process, thread, coroutine và GIL

**Thực hành giấy:** phân loại mười tình huống như đọc 1.000 URL, nén ảnh, chờ cảm biến, nhân ma trận, gọi thư viện blocking, xử lý một tệp nhỏ.

**Câu hỏi bắt buộc:**

- Chi phí tạo process/thread/task khác nhau ở đâu?
- Chia sẻ bộ nhớ làm thread tiện hơn nhưng tăng rủi ro gì?
- Vì sao coroutine cần tự nguyện nhường quyền?
- Tại sao GIL không làm thread vô dụng cho I/O?
- Tại sao không được phát biểu tuyệt đối “thread không song song” mà phải nêu bối cảnh CPython/build/C extension?

**Đầu ra:** mỗi người nộp cây quyết định một trang và được một người khác phản biện.

### Buổi 3 — Executor và Future

**Thực hành:** dùng cùng một hàm giả lập công việc để quan sát `submit`, `result`, `exception`, `cancel`, callback, `map`, `wait`, `as_completed`.

**Phải dự đoán trước khi chạy:**

- Kết quả `map` theo thứ tự nào?
- `as_completed` trả theo thứ tự nào?
- Ngoại lệ xuất hiện lúc gọi hàm hay lúc lấy kết quả?
- `cancel()` có thành công sau khi task đã running không?
- Pool một worker sẽ ra sao nếu task A chờ Future của task B trong cùng pool?

**Đầu ra:** sơ đồ trạng thái Future có điều kiện chuyển trạng thái, không chỉ bốn ô tên trạng thái.

### Buổi 4 — Event loop, coroutine và Task

**Hoạt động đóng vai:** một người là event loop, ba người là Task, một người giữ timer queue, một người giữ I/O-ready queue. Mỗi Task chỉ tiếp tục khi được loop chọn và trả quyền khi gặp điểm chờ.

**Bài đọc mã:** dự đoán thứ tự log của:

1. gọi coroutine nhưng không await;
2. await hai coroutine liên tiếp;
3. tạo hai task rồi await;
4. task dùng `sleep(0)` để nhường quyền;
5. một task ném ngoại lệ nhưng không ai lấy kết quả.

**Đầu ra:** mỗi người tự vẽ một tick của loop và giải thích “một thread vẫn quản lý nhiều I/O in-flight” mà không nói sai thành parallelism.

### Buổi 5 — Tổ hợp công việc và lỗi

**So sánh bắt buộc:** `gather`, `wait`, `as_completed`, `TaskGroup`.

Nhóm phải trả lời bằng bảng cho từng API:

- nhận đầu vào gì;
- kết quả theo input order hay completion order;
- khi một task lỗi thì caller thấy gì;
- task còn lại có bị hủy không;
- timeout có hủy pending không;
- cách thu thập mọi lỗi;
- phiên bản Python liên quan.

**Bài tập:** tiêm hai lỗi khác loại vào `TaskGroup`, đọc `ExceptionGroup`, xử lý chọn lọc bằng `except*`, giải thích vì sao không nên dùng `except Exception: pass`.

### Buổi 6 — Cancellation, synchronization và backpressure

**Thí nghiệm:**

1. hủy task khi đang `sleep` và quan sát `finally`;
2. hủy parent có child được shield;
3. tạo race bằng read–await–write trên biến chung rồi sửa bằng Lock;
4. giới hạn số thao tác bằng Semaphore;
5. producer nhanh, consumer chậm với Queue vô hạn rồi Queue hữu hạn;
6. cố ý quên `task_done` để thấy `join` không kết thúc.

**Đầu ra:** mỗi người giải thích một primitive khác nhau; sau đó đổi câu hỏi để bảo đảm không ai chỉ thuộc primitive mình vừa nói.

### Buổi 7 — Tích hợp blocking code, test, debug và benchmark

**Tích hợp:** biết khi nào dùng `to_thread`; khi nào cần ProcessPool; thao tác nào được gọi từ thread khác qua API thread-safe; vì sao logging/network sync có thể làm loop chậm.

**Test bắt buộc:** success, timeout, cancellation cleanup, partial error, max concurrency, deterministic input, output equivalence.

**Debug bắt buộc:** bật debug mode; nhận diện never-awaited coroutine, never-retrieved exception, slow callback và pending task.

**Benchmark bắt buộc:** tách latency từng request, tổng elapsed time, throughput, max in-flight, error count; chạy lặp; không trộn thời gian setup vào một biến thể nhưng bỏ khỏi biến thể khác.

### Buổi 8 — Dạy lại, phản biện và thi thử

1. Mỗi owner có 10 phút dạy chuyên môn cho cả nhóm nhưng không dùng slide chính thức.
2. Backup trình bày lại 5 phút; owner chỉ được sửa sau khi backup nói xong.
3. Bốc thăm ngẫu nhiên: mỗi người nhận một câu không thuộc chuyên môn chính.
4. Cả nhóm debug một lỗi mới chưa có trong kịch bản.
5. Chạy demo offline và dùng phương án dự phòng bằng ảnh/JSON nếu môi trường lỗi.
6. Chấm theo rubric ở mục 9; ai chưa đạt phải học và thi lại, không che bằng cách giao câu đó cho người khác.

## 5. Bộ bài tập chung tối thiểu

### Bài 1 — Dự đoán timeline

Cho ba tác vụ A, B, C lần lượt chờ 1, 2 và 3 giây. Mỗi người phải vẽ timeline cho:

- tuần tự;
- ba OS thread;
- ba coroutine được await tuần tự;
- ba Task chạy concurrent;
- ba process cho một phép tính CPU.

Không chấp nhận chỉ ghi tổng thời gian; phải chỉ ra ai đang chạy, ai đang chờ và tài nguyên thực thi nào đang bận.

### Bài 2 — Future lifecycle

Cho năm task và pool hai worker. Xác định trạng thái của từng Future ở các mốc: vừa submit, hai worker đang chạy, một task hoàn thành, một task pending bị cancel, pool shutdown. Nêu khi nào `result()` block và khi nào nó ném lại exception.

### Bài 3 — Coroutine không tự chạy

Giải thích sự khác nhau giữa:

```python
coro = fetch_one()
result = await fetch_one()
task = asyncio.create_task(fetch_one())
```

Mỗi người phải nói được kiểu đối tượng, thời điểm lập lịch, cách nhận kết quả và lỗi nếu bỏ quên.

### Bài 4 — Tổ hợp task

Cho năm công việc, trong đó công việc thứ hai lỗi sớm, công việc thứ tư treo lâu. Viết hoặc mô tả cách dùng `gather`, `as_completed`, `wait` và `TaskGroup`; phân tích hành vi lỗi/hủy/timeout của từng cách.

### Bài 5 — Cancellation-safe cleanup

Một task mở kết nối, lấy semaphore, ghi kết quả rồi đóng kết nối. Tiêm cancellation ở mọi điểm `await`. Chỉ ra tài nguyên nào có thể rò và thiết kế lại bằng `async with`/`try...finally`.

### Bài 6 — Backpressure

Producer tạo 100 item/giây, consumer xử lý 20 item/giây. Tính tốc độ backlog tăng nếu Queue vô hạn; đề xuất `maxsize`, số consumer và chính sách timeout/drop/retry. Giải thích đây là quyết định nghiệp vụ chứ không chỉ cú pháp.

### Bài 7 — Blocking event loop

Tìm ba lỗi trong chương trình async gọi `time.sleep`, thư viện đọc tệp blocking lớn và phép tính CPU dài. Chọn giữ sync, `to_thread`, ThreadPool hoặc ProcessPool cho từng thao tác và nêu đánh đổi.

### Bài 8 — Benchmark có kiểm soát

So sánh tuần tự, ThreadPool và asyncio trên cùng tập dữ liệu giả lập. Trước khi đo phải kiểm tra output bằng nhau. Báo ít nhất elapsed, throughput, error count và nhiều lần chạy; giải thích tại sao số liệu giả lập không chứng minh hiệu năng Internet thực.

## 6. Ma trận kiểm tra miệng chéo

Mỗi cặp kiểm tra nhau 15–20 phút, sau đó đổi cặp ở vòng tiếp theo.

| Vòng | Cặp | Chủ đề người A hỏi người B | Chủ đề người B hỏi người A |
|---|---|---|---|
| 1 | TV1 ↔ TV4 | khái niệm/workload | cancellation/timeout |
| 1 | TV2 ↔ TV5 | Future/pool | Queue/backpressure |
| 1 | TV3 ↔ TV6 | event loop/Task | benchmark/quyết định |
| 2 | TV1 ↔ TV5 | process/thread/coroutine | race/synchronization |
| 2 | TV2 ↔ TV6 | ProcessPool/GIL | demo/equivalence |
| 2 | TV3 ↔ TV4 | gather/TaskGroup | ExceptionGroup/cleanup |
| 3 | TV1 ↔ TV6 | cây chọn công cụ | giới hạn của kết luận |
| 3 | TV2 ↔ TV4 | deadlock/executor | bridge sync–async |
| 3 | TV3 ↔ TV5 | async protocols | test/debug/observability |

Người hỏi không chỉ đọc đáp án. Họ phải đưa tình huống biến đổi, chẳng hạn đổi từ I/O-bound sang CPU-bound, tăng số task, làm một child thất bại hoặc hủy parent giữa chừng.

## 7. Blueprint bài quiz chung

Blueprint kiểm tra gồm 60 câu trong 60 phút; mỗi lần sinh đề trộn thứ tự. Ngân hàng câu hỏi nằm trong hồ sơ học chung, không đưa toàn bộ lên slide.

| Phần | Số câu | Dạng câu |
|---|---:|---|
| Khái niệm và hai trục phân loại | 8 | chọn phát biểu đúng + giải thích ngắn |
| Workload, process, thread, coroutine, GIL | 8 | phân loại tình huống |
| Executor/Future/pools | 10 | trạng thái, dự đoán output, tìm deadlock |
| Event loop/coroutine/Task | 10 | timeline, kiểu đối tượng, thứ tự log |
| Tổ hợp task và structured concurrency | 8 | so sánh API, lỗi và thứ tự kết quả |
| Timeout/cancellation/synchronization | 8 | sửa lỗi, lựa chọn primitive |
| Queue/bridge/test/debug/benchmark | 8 | thiết kế và phản biện số liệu |

Điều kiện đạt:

- tổng điểm ít nhất 51/60 (85%);
- không phần nào dưới 70%;
- các câu “nguy hiểm” về cancellation, blocking event loop, ProcessPool entry point và Queue `task_done` phải đúng;
- sai câu nào phải tự giải thích lại câu đó, không chỉ xem đáp án.

## 8. Bộ câu hỏi phản biện mà cả sáu phải trả lời được

1. Một chương trình có thể concurrent nhưng không parallel không? Cho ví dụ đúng theo cơ chế.
2. Async có luôn non-blocking không? Nếu coroutine gọi `time.sleep` thì điều gì xảy ra?
3. Vì sao hai dòng `await fetch(a); await fetch(b)` chưa chắc concurrent?
4. `create_task` khác gọi coroutine function như thế nào?
5. `asyncio.Future` khác `concurrent.futures.Future` ở đâu và nối với nhau thế nào?
6. Khi nào `ThreadPoolExecutor` tốt hơn `asyncio`?
7. Khi nào ProcessPool tệ hơn tuần tự dù công việc CPU-bound?
8. GIL ảnh hưởng gì và không ảnh hưởng gì? Câu trả lời thay đổi thế nào với free-threaded build?
9. `map` và `as_completed` khác nhau về thứ tự kết quả ra sao?
10. Vì sao Future đang running thường không cancel được ngay?
11. Một worker chờ Future khác trong cùng pool có thể gây chuyện gì?
12. Event loop biết socket đã sẵn sàng bằng cách nào ở mức khái niệm?
13. `await` có nhường quyền trong mọi biểu thức không, hay phụ thuộc awaitable đã hoàn thành?
14. Vì sao giữ tham chiếu Task và lấy exception là quan trọng?
15. `gather` có tự hủy mọi sibling khi một task lỗi không? So với `TaskGroup`?
16. `wait` timeout khác `wait_for`/`timeout` ở hành vi hủy thế nào?
17. Cancellation đi vào coroutine tại đâu? Cleanup nên viết ở đâu?
18. Khi nào dùng `shield`, và caller vẫn có thể nhận `CancelledError` không?
19. Một thread/event loop có thể có race condition không? Tạo ví dụ read–await–write.
20. Lock và Semaphore giải quyết hai bài toán khác nhau thế nào?
21. Event và Condition khác gì? Khi nào phải kiểm tra lại predicate?
22. Queue hữu hạn tạo backpressure bằng cơ chế nào?
23. Quên `task_done` gây biểu hiện gì?
24. Vì sao tạo 100.000 task ngay lập tức có thể nguy hiểm dù từng task nhẹ?
25. `to_thread` có làm code CPU-bound thuần Python nhanh song song không?
26. Khi nào cần `run_coroutine_threadsafe` thay vì gọi trực tiếp coroutine từ thread khác?
27. Làm sao phát hiện coroutine chưa await và exception chưa retrieve?
28. Test cancellation làm sao chứng minh tài nguyên đã đóng?
29. Benchmark async thế nào để không so sánh hai bài toán khác nhau?
30. Nếu async chậm hơn tuần tự trong demo, kết luận hợp lý là gì?
31. Timeout khác retry; retry cần backoff/jitter và idempotency vì sao?
32. Nếu giảng viên yêu cầu chạy trên Python cũ hơn 3.11, thay `TaskGroup` và `asyncio.timeout` bằng gì, và phải nói rõ mất semantics nào?

## 9. Rubric đánh giá từng thành viên

| Tiêu chí | Trọng số | Chưa đạt | Đạt | Tốt |
|---|---:|---|---|---|
| Đúng khái niệm và thuật ngữ | 20% | trộn khái niệm | định nghĩa đúng | phản biện được trường hợp biên |
| Hiểu cơ chế | 20% | chỉ thuộc API | vẽ/giải thích được | dự đoán timeline và lỗi |
| Áp dụng vào mã/demo | 20% | chỉ đọc mã | chạy và sửa lỗi cơ bản | tiêm lỗi, debug và giải thích |
| Phần chuyên môn owner | 15% | thiếu nội dung lõi | đầy đủ Core | nối được Applied/Advanced |
| Hiểu các phần còn lại | 15% | né câu ngoài phần | trả lời mức nền tảng | trả lời tình huống biến đổi |
| Nguồn, giao tiếp và review | 10% | không nguồn/không review | nguồn chính thức, review đủ | phát hiện lỗi chéo và sửa mạch kể |

Ngưỡng đạt cá nhân: **85/100**, trong đó hai tiêu chí “đúng khái niệm” và “hiểu các phần còn lại” không được dưới mức Đạt.

## 10. Phân tán các việc không chuyên môn cho cả sáu người

Để một thành viên không bị biến thành “người làm hết việc phụ”, chia như sau:

| Người | Việc xuyên suốt chính | Việc xuyên suốt phụ | Bằng chứng bàn giao |
|---|---|---|---|
| TV1 | quản lý scope và mapping tài liệu gốc | glossary/kiểm thời lượng | coverage matrix + run sheet |
| TV2 | bảng API và semantics Future/ThreadPool | kiểm version của executor | API matrix + deadlock checklist |
| TV3 | giao thức benchmark và caveat nền tảng | kiểm ProcessPool/GIL/pickling | raw-data protocol + version notes |
| TV4 | sơ đồ event loop/timeline | kiểm citation cho asyncio runtime | source map + diagram spec |
| TV5 | fault-injection, test và debug checklist | kiểm backpressure/cleanup | error matrix + test plan |
| TV6 | tích hợp, decision tree và release rehearsal | đóng gói phương án B | architecture record + release checklist |

Mọi sản phẩm phải có owner và reviewer. Người review không được là chính người viết; mỗi Pull Request cần nêu đã kiểm gì, không chỉ bấm Approve.

## 11. Quy trình GitHub

### 11.1. Milestone

Tạo một milestone `chapter-4-report` với bốn pha:

1. `scope-and-research` — chốt coverage, thuật ngữ, nguồn.
2. `content-and-diagrams` — viết nội dung và đặc tả hình.
3. `demo-and-validation` — chỉ bắt đầu sau khi sườn được duyệt.
4. `slides-and-rehearsal` — chỉ bắt đầu sau khi nội dung được review.

### 11.2. Issue tối thiểu

- Sáu Issue chuyên môn tương ứng TV1–TV6.
- Một Issue glossary/version matrix.
- Một Issue kiểm tra truy vết tài liệu nguồn.
- Một Issue common quiz/oral defense.
- Một Issue demo requirements/test oracle.
- Một Issue benchmark protocol.
- Một Issue final consistency and citations.

Mẫu acceptance criteria cho Issue:

```text
- [ ] Mapping tới mục A–Z và trang tài liệu gốc
- [ ] Có nguồn chính thức cho chi tiết ngoài file gốc
- [ ] Có ví dụ đúng và một phản ví dụ/lỗi thường gặp
- [ ] Có speaker notes hoặc lời giải thích dự kiến
- [ ] Có ít nhất 5 câu phản biện kèm đáp án
- [ ] Reviewer đã chạy/trace ví dụ độc lập
- [ ] Không trùng nội dung với phần trước/sau
```

### 11.3. Nhánh và Pull Request

- Nhánh: `tv1/foundations`, `tv2/futures-threadpool`, `tv3/processpool-performance`, `tv4/asyncio-runtime`, `tv5/reliability`, `tv6/integration-demo`.
- Commit nhỏ, nêu đúng bản chất: `docs: clarify gather failure semantics`.
- PR phải liên kết Issue, ghi nguồn, ảnh hưởng tới mục nào của coverage matrix và cách kiểm tra.
- Reviewer dùng checklist: **đúng — đủ — không trùng — giải thích được — kiểm chứng được — đúng phiên bản**.

## 12. Quality gates trước khi làm PowerPoint

### Gate 1 — Scope được duyệt

- Đã xác định thời lượng báo cáo và chọn cấu hình slide rút gọn/chuẩn/phụ lục.
- Coverage matrix không còn mục Core ở trạng thái “thiếu”.
- Mọi nội dung ngoài file gốc được gắn nhãn Mở rộng hoặc Nâng cao.

### Gate 2 — Kiến thức được kiểm chứng

- Sáu owner hoàn thành nội dung và backup review.
- Tất cả ví dụ được chạy trên phiên bản Python mục tiêu.
- Mọi phát biểu dễ thay đổi theo phiên bản có version note.
- Không dùng benchmark như bằng chứng tuyệt đối.

### Gate 3 — Cả nhóm thực sự hiểu

- Sáu người qua quiz.
- Sáu người qua oral defense ngẫu nhiên.
- Sáu người chạy/trace được demo và một kịch bản lỗi.
- Backup có thể thay owner trình bày mà không đứt mạch.

### Gate 4 — Mới bắt đầu PPTX

- Sườn và speaker notes được chốt trước.
- Mỗi slide có một thông điệp chính, nguồn và người chịu trách nhiệm.
- Nội dung chi tiết để trong speaker notes/phụ lục, không nhồi toàn bộ chữ lên mặt slide.

## 13. Definition of Done cuối cùng

Báo cáo Chương 4 chỉ hoàn tất khi:

- bao phủ đủ nội dung lõi của 24 trang tài liệu gốc;
- các khoảng trống thực hành thiết yếu đã được bổ sung bằng nguồn Python chính thức;
- thuật ngữ nhất quán và không có phát biểu tuyệt đối sai bối cảnh;
- mỗi người có một chuyên môn sâu, một phần backup và 40 năng lực chung;
- nội dung slide, lời nói, demo, test và benchmark kể cùng một câu chuyện;
- demo có input cố định, output oracle, fault injection và phương án offline;
- có bảng giới hạn: điều gì demo chứng minh được và không chứng minh được;
- mọi nguồn mở được, version note đúng và nội dung giảng viên được tôn trọng bản quyền;
- cả sáu qua quiz, oral defense và rehearsal có bốc thăm câu ngoài chuyên môn;
- chỉ sau các điều kiện trên nhóm mới tạo PPTX/PDF.

## 14. Kế hoạch khởi động

1. Điền họ tên/MSSV vào TV1–TV6 và xác nhận owner/backup.
2. Hỏi giảng viên thời lượng để chọn 36 hay 48 slide chính; giữ phần nâng cao ở phụ lục.
3. Mỗi người đọc `00_HO_SO_DU_AN_VA_MA_TRAN_TRUY_VET.md` và `01_BAN_DO_KIEN_THUC_A_Z.md`.
4. Tạo milestone và Issue theo mục 11; công việc PowerPoint chỉ mở sau quality gate.
5. Tổ chức Buổi 1 và Buổi 2; lưu glossary/cây quyết định vào repo.
6. Chỉ chốt demo sau khi toàn nhóm thống nhất workload và câu hỏi cần chứng minh.
