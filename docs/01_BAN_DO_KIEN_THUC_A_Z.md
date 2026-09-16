# BẢN ĐỒ KIẾN THỨC A–Z — CHƯƠNG 4: PHƯƠNG PHÁP TÍNH TOÁN BẤT ĐỒNG BỘ TRONG PYTHON

> Tài liệu kiểm soát phạm vi kiến thức cho nhóm 6 thành viên. Đây là **sườn học thuật và chuẩn đầu ra**, không phải nội dung PowerPoint hoàn chỉnh.
>
> Mốc đối chiếu kỹ thuật: tài liệu chính thức **Python 3.14.7**, kiểm tra ngày **15/09/2026**. Những API chỉ xuất hiện ở phiên bản mới đều được gắn nhãn phiên bản; không được trình bày chúng như thể có trên mọi bản Python.

---

## 1. Tuyên bố phạm vi và mục tiêu

Chương 4 không được hiểu đơn giản là “học vài hàm `asyncio`”. Để thật sự nắm phương pháp tính toán bất đồng bộ từ A đến Z, cả nhóm phải hiểu được bốn lớp vấn đề liên kết với nhau:

1. **Mô hình tư duy:** tuần tự, đồng thời, song song, bất đồng bộ, blocking, non-blocking, I/O-bound, CPU-bound khác nhau như thế nào.
2. **Cơ chế thực thi:** coroutine, awaitable, Task, Future, event loop và Executor hoạt động ra sao; lúc nào công việc bắt đầu, tạm dừng, tiếp tục, hoàn thành, lỗi hoặc bị hủy.
3. **Thiết kế chương trình đúng:** phối hợp nhiều tác vụ, giới hạn tải, tạo backpressure, bảo vệ trạng thái dùng chung, xử lý timeout, cancellation, lỗi dây chuyền và đóng tài nguyên.
4. **Đánh giá và vận hành:** chọn đúng công cụ, đo hiệu năng đúng, phát hiện blocking, deadlock, task bị bỏ quên, lỗi không được thu hồi; viết kiểm thử cho luồng thành công và luồng lỗi.

Chuẩn đầu ra của nhóm là: **mỗi thành viên đều giải thích được toàn bộ đường đi của một tác vụ bất đồng bộ**, từ lúc tạo coroutine đến lúc có kết quả hoặc bị hủy; đồng thời mỗi người có một cụm chuyên môn riêng để đào sâu và phản biện.

### 1.1. Điều tài liệu này cam kết bao phủ

- Nội dung cốt lõi thường có trong Chương 4: khái niệm bất đồng bộ, `concurrent.futures`, `Executor`, `Future`, `ThreadPoolExecutor`, `ProcessPoolExecutor`, event loop, coroutine, Task và `asyncio`.
- Nền tảng bắt buộc để không học thuộc lòng: blocking/non-blocking, I/O-bound/CPU-bound, scheduling hợp tác, vòng đời Task/Future và GIL.
- Phần thực hành cần có để báo cáo đầy đủ: chạy nhiều tác vụ, chờ kết quả, timeout, cancellation, truyền lỗi, giới hạn đồng thời, queue và backpressure.
- Phần mở rộng có giá trị học thuật: structured concurrency với `TaskGroup`, `ExceptionGroup`, `async with`, `async for`, async generator, streams, subprocess, `contextvars`, bridge giữa event loop và thread/process/interpreter.
- Phần đảm bảo chất lượng: đo hiệu năng, kiểm thử, debug, logging, introspection, graceful shutdown và các bẫy thường gặp.

### 1.2. Điều không được đánh đồng

- **Bất đồng bộ không đồng nghĩa song song.** Một event loop thông thường có thể quản lý nhiều Task đồng thời nhưng tại một thời điểm chỉ chạy mã Python của một Task trên thread của loop.
- **Đồng thời không bảo đảm nhanh hơn.** Nó thường tăng khả năng tận dụng thời gian chờ và throughput cho I/O; một tác vụ đơn lẻ không nhất thiết hoàn thành nhanh hơn.
- **`async def` không làm mọi lệnh bên trong trở thành non-blocking.** Nếu gọi `time.sleep()`, I/O đồng bộ chậm hoặc tính CPU dài trong coroutine, toàn event loop vẫn bị chặn.
- **`await` không tự tạo đồng thời.** Hai câu `await` nối tiếp vẫn chạy theo thứ tự; muốn chồng lấp thời gian chờ phải tạo Task hoặc dùng cơ chế phối hợp phù hợp.
- **`concurrent.futures.Future` không phải `asyncio.Future`.** Hai lớp có mục đích, khả năng chờ và quy tắc thread-safety khác nhau.
- **Thread không mặc nhiên giúp mã Python CPU-bound chạy đa lõi trên bản CPython thông thường có GIL.**
- **Timeout không phải cơ chế cưỡng bức dừng mọi loại công việc.** Một hàm đồng bộ đã chạy trong worker thread thường không thể bị giết an toàn chỉ bằng cách hủy Task đang chờ nó.

---

## 2. Hệ thống phân tầng kiến thức

Mỗi mục trong tài liệu được gắn một trong ba mức sau:

### `[CORE]` — Bắt buộc với cả 6 thành viên

Kiến thức này thuộc xương sống Chương 4. Mỗi thành viên phải:

- tự giải thích được mà không đọc slide;
- đọc được đoạn mã ngắn và dự đoán luồng chạy;
- phân biệt được trường hợp đúng/sai;
- trả lời được câu hỏi phản biện;
- sử dụng được trong demo hoặc giải thích vì sao demo không dùng nó.

Thiếu bất kỳ mục `[CORE]` nào thì chưa thể tuyên bố “nắm A–Z”.

### `[APPLIED]` — Bắt buộc ở mức vận dụng

Kiến thức này biến lý thuyết thành thiết kế có thể chạy và kiểm chứng. Cả nhóm phải hiểu ý nghĩa; ít nhất hai thành viên phải tự triển khai hoặc kiểm thử được. Bao gồm giới hạn đồng thời, queue, timeout, cleanup, bridge blocking code, benchmark và test.

### `[ADVANCED]` — Đào sâu và dùng để phản biện

Không nhất thiết đưa toàn bộ lên phần trình chiếu chính. Nên đặt ở phụ lục, speaker notes, tài liệu GitHub hoặc phần hỏi đáp. Mục đích là:

- tránh phát biểu sai vì khác phiên bản;
- giải thích được trường hợp biên;
- cho thấy nhóm hiểu sâu hơn tài liệu gốc;
- không làm loãng mạch báo cáo dành cho người mới.

---

## 3. Bản đồ tổng thể: từ bài toán đến công cụ

```text
Bài toán có nhiều công việc
│
├─ Công việc chủ yếu chờ mạng/đĩa/API/DB?
│  │
│  ├─ Thư viện có API async thật sự
│  │  └─ asyncio + coroutine + Task/TaskGroup
│  │     ├─ Semaphore: giới hạn số thao tác đang bay
│  │     ├─ Queue: producer/consumer + backpressure
│  │     ├─ timeout/cancellation: kiểm soát vòng đời
│  │     └─ Streams/subprocess async: khi bài toán cần
│  │
│  └─ Chỉ có API blocking
│     └─ asyncio.to_thread() hoặc ThreadPoolExecutor
│        └─ Không gọi blocking trực tiếp trên event-loop thread
│
├─ Công việc chủ yếu tính toán CPU bằng Python?
│  ├─ ProcessPoolExecutor: lựa chọn phổ biến trên CPython có GIL
│  └─ InterpreterPoolExecutor: Python 3.14+, nâng cao, dữ liệu cô lập
│
├─ Hàm native/C extension có giải phóng GIL?
│  └─ ThreadPool có thể đạt song song CPU; phải đo thay vì suy đoán
│
└─ Chỉ có một công việc hoặc công việc quá nhỏ?
   └─ Tuần tự có thể đơn giản và nhanh hơn vì không chịu overhead
```

Quy tắc chọn công cụ phải dựa trên **bản chất workload**, không dựa trên cảm giác rằng “async hiện đại hơn”. Tài liệu chính thức Python cũng nêu việc lựa chọn công cụ phụ thuộc CPU-bound hay I/O-bound và mô hình lập trình mong muốn: event-driven cooperative multitasking hay preemptive multitasking.

Nguồn: https://docs.python.org/3.14/library/concurrency.html

---

## 4. Taxonomy A–Z

Phần này là bảng kiểm 26 điểm. Sau bảng kiểm là các chương giải thích sâu.

### A — Awaitable, `async`, `await` `[CORE]`

- Awaitable là đối tượng có thể dùng trong biểu thức `await`.
- Ba nhóm thường gặp trong `asyncio`: coroutine object, Task và Future.
- `async def` định nghĩa coroutine function; gọi hàm chỉ tạo coroutine object, chưa bảo đảm nó đã chạy.
- `await` tạm dừng coroutine hiện tại cho đến khi awaitable hoàn thành, đồng thời trao quyền điều khiển về scheduler nếu awaitable chưa sẵn sàng.
- `await` chỉ hợp lệ trong ngữ cảnh bất đồng bộ thích hợp và chỉ nhận awaitable; `await` một giá trị thường gây `TypeError`.
- `async with` và `async for` là hai giao thức khác: quản lý tài nguyên bất đồng bộ và lặp bất đồng bộ.

### B — Blocking, non-blocking, backpressure `[CORE/APPLIED]`

- Blocking là thao tác giữ thread thực thi và không trả quyền điều khiển trong lúc chờ.
- Non-blocking không có nghĩa là “không chờ”; nó có nghĩa là trong lúc thao tác chưa sẵn sàng, thread có thể phục vụ việc khác.
- Blocking code trong coroutine làm trễ mọi Task cùng loop.
- Backpressure là cơ chế làm chậm phía sản xuất khi phía tiêu thụ hoặc tài nguyên đích không theo kịp.
- `Queue(maxsize=n)`, `Semaphore(n)`, flow control `writer.drain()` và `Executor.map(..., buffersize=n)` là những công cụ liên quan nhưng giải quyết các lớp khác nhau.

### C — Concurrency, coroutine, cancellation `[CORE]`

- Concurrency là nhiều công việc có tiến triển trong cùng khoảng thời gian; parallelism là thực thi đồng thời vật lý trên nhiều lõi/đơn vị xử lý.
- Coroutine có thể tạm dừng và tiếp tục tại nhiều điểm; subroutine thông thường chạy từ vào đến ra trừ khi bị ngắt bởi lỗi.
- Cancellation của Task là một yêu cầu hợp tác, được đưa vào coroutine dưới dạng `CancelledError` tại cơ hội kế tiếp.
- Cleanup phải dùng `try/finally`; nếu bắt `CancelledError`, thông thường phải `raise` lại sau cleanup.

### D — Deadline, debug, deadlock `[CORE/APPLIED]`

- Deadline là mốc tuyệt đối; timeout thường là khoảng thời gian tương đối.
- `asyncio.timeout()`/`timeout_at()` và `wait_for()` có semantics hủy khác nhau cần hiểu chính xác.
- Debug mode phát hiện callback chậm, gọi API non-thread-safe sai thread, coroutine không được await và lỗi Future không được lấy.
- Deadlock có thể xuất hiện cả ở coroutine, thread, process và executor: vòng chờ lẫn nhau, giữ lock rồi chờ vô hạn, thiếu `task_done()`, hoặc worker tự chờ việc mà chính pool hết worker phải thực hiện.

### E — Event loop, Executor, exception `[CORE]`

- Event loop là scheduler và bộ điều phối I/O của `asyncio`.
- Executor chạy callable thông thường trên worker thread, process hoặc interpreter.
- Exception có thể truyền qua `await`, `Future.result()`, iterator của `map()`, `gather()`, `TaskGroup` hoặc callback; mỗi cơ chế có quy tắc khác nhau.
- `TaskGroup` có thể phát sinh `ExceptionGroup`; xử lý bằng `except*` theo loại lỗi.

### F — Future, fairness, flow control `[CORE/APPLIED]`

- Future đại diện cho kết quả sẽ có trong tương lai.
- `asyncio.Future` là awaitable, gắn với event loop, không thread-safe và thường là API mức thấp.
- `concurrent.futures.Future` đại diện callable trong executor; `.result(timeout)` có thể chặn thread gọi.
- `asyncio.Lock.acquire()` được tài liệu bảo đảm công bằng theo thứ tự bắt đầu chờ; không được tự suy rộng bảo đảm này sang mọi primitive hoặc mọi lịch Task.
- Flow control bảo vệ bộ đệm và tài nguyên; ví dụ phải `await writer.drain()` khi ghi stream.

### G — `gather`, GIL, graceful shutdown `[CORE/APPLIED]`

- `gather()` chạy nhiều awaitable đồng thời và trả kết quả theo thứ tự đầu vào, không theo thứ tự hoàn thành.
- Khi một phần tử lỗi và `return_exceptions=False`, lỗi đầu tiên được truyền ngay; các phần tử khác **không tự bị hủy**.
- GIL giới hạn parallelism của Python bytecode qua nhiều thread trên bản CPython thông thường; I/O và một số native extension có thể giải phóng GIL.
- Graceful shutdown phải ngừng nhận việc mới, xử lý/đóng queue, hủy phần việc còn lại theo chính sách, await cleanup và đóng tài nguyên.

### H — Handling failures and cancellation `[CORE]`

- Phân biệt lỗi nghiệp vụ có thể retry, lỗi lập trình, timeout, cancellation và lỗi hạ tầng.
- Không dùng `except Exception:` như lý do để bỏ qua mọi lỗi; `CancelledError` từ Python 3.8 kế thừa `BaseException` nên thường không bị bắt bởi khối này.
- `return_exceptions=True` biến lỗi thành phần tử kết quả; bắt buộc kiểm tra từng phần tử, nếu không sẽ âm thầm che lỗi.
- Cleanup cũng có thể lỗi; cần quyết định lỗi nào giữ vai trò nguyên nhân, lỗi nào log bổ sung.

### I — I/O-bound, iteration, `InterpreterPoolExecutor` `[CORE/ADVANCED]`

- I/O-bound dành phần lớn thời gian chờ hệ thống ngoài CPU: mạng, database, file, dịch vụ khác.
- Async iterator cung cấp `__aiter__()` và `__anext__()` trả awaitable; dùng qua `async for`.
- Async generator kết hợp `async def`, `yield` và có thể `await`; phải quan tâm việc đóng bằng `aclose()` khi dừng sớm.
- `InterpreterPoolExecutor` có từ Python 3.14, cho parallelism đa lõi nhờ mỗi worker có interpreter/GIL riêng nhưng trạng thái mutable bị cô lập và dữ liệu/callable phải được truyền phù hợp, thường qua serialization.

### J — `join`, job lifecycle `[CORE/APPLIED]`

- `Queue.join()` chờ bộ đếm unfinished tasks về 0, không chỉ chờ queue “trông có vẻ rỗng”.
- Mỗi `get()` thành công phải có đúng một `task_done()`, tốt nhất đặt trong `finally` quanh khâu xử lý.
- `Executor.shutdown(wait=True)` chờ các Future đã submit còn pending/running hoàn tất; nếu đồng thời dùng `cancel_futures=True`, những Future pending chưa bắt đầu bị hủy còn công việc đã running vẫn được chờ.
- Job lifecycle cần trạng thái rõ: created/pending → running → success/error/cancelled, kèm quy tắc cleanup.

### K — Keep references, keywords, ownership `[CORE]`

- Event loop chỉ giữ weak reference tới Task; Task nền cần strong reference hoặc tốt hơn là nằm trong `TaskGroup`.
- “Fire-and-forget” không có quản lý dễ gây `Task exception was never retrieved`.
- Ai tạo Task phải xác định ai sở hữu, ai chờ, ai hủy và ai thu hồi exception của Task đó.
- Các keyword `async def`, `await`, `async with`, `async for` không có cùng chức năng; phải gọi đúng tên giao thức.

### L — Lock, lifecycle, latency `[CORE/APPLIED]`

- Single-threaded event loop vẫn có race condition logic nếu chuỗi read–await–write bị Task khác xen vào.
- `asyncio.Lock` bảo vệ critical section giữa các Task trong cùng loop; không dùng nó để đồng bộ OS thread.
- Không giữ lock qua I/O chậm nếu có thể tách snapshot/update, vì sẽ làm tăng latency và tạo convoy.
- Luôn nhả lock bằng `async with` hoặc `try/finally`.

### M — `map`, metrics, memory `[CORE/APPLIED]`

- `Executor.map()` giữ thứ tự đầu vào ở kết quả; `as_completed()` ưu tiên thứ tự hoàn thành.
- `chunksize` ảnh hưởng ProcessPool khi map tập dữ liệu lớn; không có tác dụng với ThreadPool và InterpreterPool.
- `buffersize` có từ Python 3.14, giới hạn số tác vụ đã submit nhưng kết quả chưa được yield.
- Đánh giá phải đo latency, throughput, CPU, memory, số lỗi và mức đồng thời; không chỉ đo một lần rồi kết luận.

### N — Networking, non-determinism, non-blocking `[CORE/ADVANCED]`

- `asyncio` đặc biệt phù hợp high-level network code và I/O-bound.
- Streams cung cấp `StreamReader`/`StreamWriter`; đọc có EOF/giới hạn buffer, ghi cần `drain()`, đóng cần `close()` rồi `await wait_closed()`.
- Thứ tự chạy giữa các Task nói chung không nên được dùng làm luật nghiệp vụ nếu API không bảo đảm.
- Không dùng `asyncio.sleep()` như bằng chứng rằng một thư viện blocking đã trở thành non-blocking; nó chỉ mô phỏng điểm chờ hợp tác.

### O — Orchestration, ordering, overload `[CORE/APPLIED]`

- Orchestration quyết định tạo bao nhiêu Task, chờ theo nhóm nào, lỗi nào làm dừng nhóm và kết quả được ghép ra sao.
- `gather()` bảo toàn thứ tự đầu vào; `as_completed()` cho kết quả sớm nhất trước; `wait()` trả hai tập done/pending.
- Tạo hàng trăm nghìn Task một lúc có thể quá tải memory/socket/API; cần bounded concurrency.
- Semaphore giới hạn số thao tác đồng thời nhưng không tự bảo đảm “N yêu cầu mỗi giây”; rate limiting cần thêm khái niệm thời gian/token phù hợp.

### P — Parallelism, ProcessPool, pickling `[CORE]`

- `ProcessPoolExecutor` dùng process nên vượt GIL cho CPU-bound Python và tận dụng nhiều lõi.
- Đổi lại có chi phí tạo process, serialize/deserialize và chuyển dữ liệu.
- Callable, argument và result phải picklable; lambda/hàm cục bộ hoặc code chỉ có trong REPL không nên kỳ vọng hoạt động.
- Module `__main__` phải import được bởi worker; chương trình phải dùng `if __name__ == "__main__":` khi phù hợp, đặc biệt trên Windows/spawn.
- Không gọi phương thức Executor/Future từ callable đang chạy trong `ProcessPoolExecutor`, vì tài liệu cảnh báo deadlock.

### Q — Queue and backpressure `[CORE/APPLIED]`

- `asyncio.Queue` dành cho Task async, không thread-safe.
- `Queue(maxsize>0)` khiến `put()` chờ khi đầy, tạo backpressure tự nhiên.
- Queue không có tham số timeout riêng; bọc thao tác bằng cơ chế timeout của `asyncio`.
- Biết `Queue`, `PriorityQueue`, `LifoQueue`, `put/get`, biến thể `nowait`, `task_done/join` và `shutdown()`.
- `Queue.shutdown()`/`QueueShutDown` có từ Python 3.13; nếu mục tiêu Python cũ hơn cần dùng sentinel/cancellation theo thiết kế riêng.

### R — Race condition, Runner, result, resilience `[CORE/APPLIED]`

- Race condition là kết quả phụ thuộc vào thứ tự xen kẽ không được kiểm soát.
- `asyncio.run()` là entry point cấp cao nên dùng cho chương trình thông thường; nó quản lý loop, finalization async generator và đóng default executor.
- Không gọi `asyncio.run()` khi cùng thread đã có event loop đang chạy.
- `asyncio.Runner` hữu ích khi cần nhiều lần chạy top-level async trong cùng loop/context.
- Resilience ở tầng ứng dụng gồm retry có giới hạn, backoff, idempotency và phân loại lỗi; retry không kiểm soát có thể tạo retry storm.

### S — Scheduling, synchronization, semaphore, shield, structured concurrency `[CORE]`

- Event loop dùng cooperative scheduling: một Task chạy đến khi yield/await một thứ chưa sẵn sàng hoặc hoàn thành.
- Coroutine chạy CPU dài mà không có điểm nhường sẽ starve các Task khác.
- `Lock`, `Event`, `Condition`, `Semaphore`, `BoundedSemaphore`, `Barrier` giải quyết các nhu cầu đồng bộ khác nhau.
- `shield()` ngăn cancellation của caller truyền trực tiếp vào awaitable được che chắn; caller vẫn nhận `CancelledError`. Nó không phải nút “tắt cancellation”.
- `TaskGroup` tạo structured concurrency: vòng đời child task nằm trong scope; lỗi không phải cancellation của một child làm hủy các child còn lại và lỗi được gom lại.

### T — Task, TaskGroup, ThreadPool, timeout, testing `[CORE]`

- Task schedule coroutine; coroutine object chưa schedule không phải Task.
- `Task` kế thừa hầu hết API của `asyncio.Future` nhưng không cho bên ngoài `set_result/set_exception`.
- `ThreadPoolExecutor` phù hợp cho blocking I/O và một số native work giải phóng GIL; chia sẻ memory nên phải quản lý race/thread safety.
- Timeout phải có chính sách: việc con có bị hủy không, có cleanup không, có retry không, tổng deadline có bị vượt không.
- Kiểm thử async phải bao phủ success, failure, timeout, cancellation, cleanup, giới hạn đồng thời và không để pending task rò rỉ.

### U — Unawaited, unretrieved, `uncancel()` `[CORE/ADVANCED]`

- Coroutine được tạo nhưng không await/schedule sẽ phát `RuntimeWarning: coroutine ... was never awaited`.
- Task hoặc `asyncio.Future` lỗi nhưng không ai await/lấy exception sẽ được event loop báo khi phát hiện; thông điệp thường phân biệt `Task exception was never retrieved` và `Future exception was never retrieved`.
- Không tùy tiện nuốt `CancelledError`; `TaskGroup` và `asyncio.timeout()` dùng cancellation nội bộ nên có thể hỏng semantics.
- `uncancel()` là API chuyên biệt; chỉ dùng khi thật sự chủ động xóa trạng thái cancellation và hiểu hệ quả.

### V — Version and platform caveats `[ADVANCED]`

- Mọi code, slide và demo phải ghi phiên bản Python mục tiêu.
- API từ 3.11 như `TaskGroup`, `timeout()` và `Barrier` không chạy nguyên trạng trên 3.10.
- API mới phải gắn nhãn riêng: eager task factory từ 3.12; `Queue.shutdown()` và async iteration của `as_completed()` từ 3.13; `InterpreterPoolExecutor`, `buffersize`, `create_task(..., eager_start=...)` và call-graph introspection từ 3.14.
- Windows và Unix khác nhau về event loop, signal, subprocess và process start method.
- Event-loop policy đã deprecated và dự kiến bị loại bỏ ở Python 3.16; code mới ưu tiên `loop_factory` khi cần cấu hình loop.

### W — `wait`, `wait_for`, `as_completed` `[CORE]`

- `asyncio.wait()` nhận Task/Future, trả `(done, pending)`, không raise `TimeoutError` khi hết thời gian và không tự hủy pending.
- Từ Python 3.11, đưa coroutine object trực tiếp vào `asyncio.wait()` là không được; tạo Task trước.
- `asyncio.wait_for()` mặc định hủy awaitable đích khi timeout và có thể mất lâu hơn timeout vì chờ quá trình hủy hoàn tất.
- `asyncio.as_completed()` cho phép xử lý kết quả theo thứ tự hoàn thành; timeout của nó có semantics riêng.
- Các hàm cùng tên trong `concurrent.futures` làm việc với Future của executor, không được trộn lẫn tùy ý với `asyncio.Future`.

### X — Cross-thread/cross-model bridge `[CORE/ADVANCED]`

- `asyncio.to_thread()` đưa hàm blocking chủ yếu I/O sang thread, đồng thời truyền `contextvars.Context` hiện tại.
- `loop.run_in_executor()` bridge event loop với ThreadPool, ProcessPool hoặc InterpreterPool; kết quả trả về là `asyncio.Future`.
- Từ thread khác, dùng `loop.call_soon_threadsafe()` cho callback hoặc `asyncio.run_coroutine_threadsafe()` cho coroutine.
- `run_coroutine_threadsafe()` trả `concurrent.futures.Future`, vì phía gọi đang ở ngoài event loop.
- Hầu hết đối tượng `asyncio` không thread-safe; không thao tác trực tiếp từ thread khác.

### Y — Yield, async generator, cooperative yielding `[ADVANCED]`

- `yield` trong `async def` tạo async generator, không phải coroutine thông thường.
- `async for` nhận từng giá trị qua awaitable `__anext__()` đến `StopAsyncIteration`.
- Khi dừng lặp sớm, nên đóng async generator rõ ràng bằng `aclose()` hoặc `contextlib.aclosing()` để cleanup chạy trong ngữ cảnh dự kiến.
- `await asyncio.sleep(0)` là đường tối ưu để nhường loop, nhưng không thay thế việc offload CPU-bound dài.
- Async comprehension giúp viết gọn, nhưng `[await f(x) for x in xs]` về bản chất vẫn await từng phần tử theo trình tự; cú pháp async không tự sinh fan-out.

### Z — Zero leaked work: kết thúc không rò rỉ `[CORE/APPLIED]`

- Kết thúc đúng nghĩa là không còn Task mồ côi, Future lỗi chưa đọc, lock chưa nhả, queue item chưa `task_done`, stream chưa đóng hoặc executor chưa shutdown.
- `asyncio.run()` xử lý nhiều bước shutdown cấp loop, nhưng không thể sửa logic ownership sai trong ứng dụng.
- Mỗi demo cần chứng minh cả đường thành công lẫn đường lỗi/hủy và in trạng thái cuối để xác nhận cleanup.
- Mục tiêu không chỉ là “chạy ra kết quả”, mà là **đúng, có giới hạn, có thể dừng và có thể quan sát**.

---

## 5. Nền tảng khái niệm bắt buộc

### 5.1. Tuần tự, đồng thời, song song và bất đồng bộ `[CORE]`

| Khái niệm | Câu hỏi cốt lõi | Đặc điểm | Ví dụ Python |
|---|---|---|---|
| Tuần tự | Công việc có chạy lần lượt không? | B hoàn tất sau khi A hoàn tất | Gọi hai hàm sync nối tiếp |
| Đồng thời (concurrency) | Nhiều công việc có cùng tiến triển trong một khoảng thời gian không? | Có thể xen kẽ trên một lõi | Nhiều `asyncio.Task` trên một loop |
| Song song (parallelism) | Có thật sự chạy cùng thời điểm trên nhiều đơn vị xử lý không? | Cần nhiều lõi/process/interpreter hoặc native work | `ProcessPoolExecutor` cho CPU-bound |
| Bất đồng bộ (asynchrony) | Caller có thể tiếp tục/nhường quyền thay vì bị giữ cứng khi chờ không? | Kết quả đến sau qua coroutine/Future/callback | `await` socket I/O non-blocking |

Một chương trình có thể:

- concurrent nhưng không parallel: nhiều Task trên một event loop;
- parallel nhưng caller vẫn chờ đồng bộ ở một điểm: submit vào process pool rồi lập tức gọi `.result()`;
- vừa asynchronous vừa concurrent: nhiều network coroutine được schedule cùng lúc;
- vừa asynchronous vừa parallel: event loop điều phối I/O và offload CPU sang nhiều process.

Phải dùng sơ đồ thời gian để minh họa thay vì chỉ đưa định nghĩa:

```text
Tuần tự:
Task A: [chạy][------chờ I/O------][chạy]
Task B:                                     [chạy][---chờ---][chạy]

Async concurrent trên một thread:
Task A: [chạy][......chờ I/O.......][chạy]
Task B:       [chạy][...chờ...][chạy]
Loop:   A---->B--------------->B--->A

Parallel CPU trên hai worker:
Worker 1: [---------CPU task A---------]
Worker 2: [---------CPU task B---------]
```

### 5.2. I/O-bound và CPU-bound `[CORE]`

**I/O-bound:** thời gian chủ yếu mất vào chờ mạng, database, file, socket hoặc hệ thống ngoài. Mục tiêu concurrency là lấp thời gian chờ bằng công việc khác. `asyncio` phù hợp khi stack I/O có API async; ThreadPool phù hợp để bao bọc I/O blocking.

**CPU-bound:** thời gian chủ yếu nằm ở tính toán. Coroutine không tạo thêm lõi CPU. Nếu chạy tính toán dài ngay trong event loop, mọi I/O và Task khác bị chậm. Trên CPython có GIL thông thường, dùng ProcessPool là lựa chọn phổ biến cho mã Python CPU-bound; InterpreterPool 3.14+ là hướng nâng cao; thread có thể hữu ích nếu code native giải phóng GIL hoặc dùng free-threaded build.

Không phân loại workload chỉ qua tên hàm. Một request mạng có thể tải dữ liệu xong rồi parse/compress/hash rất nặng; đó là pipeline hỗn hợp, cần đo từng giai đoạn.

Nguồn chính thức:

- https://docs.python.org/3.14/library/asyncio.html
- https://docs.python.org/3.14/library/threading.html
- https://docs.python.org/3.14/library/multiprocessing.html

### 5.3. Cooperative scheduling `[CORE]`

Event loop chạy một Task tại một thời điểm trên thread của nó. Khi Task `await` một Future chưa hoàn thành, Task tạm dừng và loop chạy Task/callback/I/O khác. Hệ quả:

- không có `await` hoặc điểm nhường thích hợp trong một đoạn chạy dài → Task khác bị starve;
- context switch diễn ra ở các điểm có thể nhường, giúp reasoning dễ hơn thread preemptive nhưng không xóa race condition;
- một `await` có thể hoàn thành ngay và không tạo khoảng nhường dài như người đọc tưởng;
- không dựa vào thứ tự xen kẽ không được API cam kết;
- `await asyncio.sleep(0)` chủ động nhường nhưng chỉ là biện pháp hợp tác ngắn, không phải giải pháp cho tính CPU lớn.

Nguồn: https://docs.python.org/3.14/library/asyncio-task.html

### 5.4. Blocking trong event loop `[CORE]`

Các ví dụ sai phải được cả nhóm nhận diện ngay:

```python
async def wrong():
    time.sleep(2)        # Chặn thread của event loop.
    data = sync_client.get("...")  # Nếu client blocking, loop cũng bị chặn.
    return heavy_python_loop(data)  # CPU dài cũng chặn loop.
```

Ba hướng sửa, tùy bản chất:

1. Dùng API async thật sự của thư viện và `await` nó.
2. Với blocking I/O không thể đổi thư viện, dùng `await asyncio.to_thread(...)` hoặc ThreadPool.
3. Với CPU-bound Python, dùng ProcessPool/InterpreterPool hoặc tái thiết kế/batching/native implementation.

Không được sửa giả bằng cách thêm `async def` quanh hàm blocking; từ khóa không thay đổi cơ chế bên trong.

---

## 6. Coroutine, awaitable, Task và Future

### 6.1. Phân biệt function và object `[CORE]`

```python
async def fetch():       # coroutine function
    return 42

coro = fetch()           # coroutine object; chưa tự chạy đến return
value = await coro       # thực thi/chờ trong async context
```

Sai lầm phổ biến là gọi `fetch()` rồi không `await` hoặc schedule. Debug mode sẽ giúp chỉ ra nơi coroutine được tạo nhưng không được chờ.

### 6.2. Awaitable `[CORE]`

Một awaitable là đối tượng hợp lệ ở vế phải của `await`. Trong thực hành `asyncio`, học viên cần nhận diện:

- coroutine object;
- `asyncio.Task`;
- `asyncio.Future`;
- object tùy biến có giao thức `__await__()` — mức nâng cao.

Không phải mọi đối tượng có chữ “Future” đều await trực tiếp được. `concurrent.futures.Future` không await được; cần bridge như `asyncio.wrap_future()` hoặc sử dụng API event-loop/executor phù hợp.

Nguồn:

- https://docs.python.org/3/glossary.html#term-awaitable
- https://peps.python.org/pep-0492/

### 6.3. Task `[CORE]`

Task là đối tượng schedule và lái một coroutine trên event loop. Vòng đời logic:

```text
coroutine object
      │ create_task / TaskGroup.create_task
      ▼
scheduled Task ──► running ──await pending──► suspended
      ▲                                  │
      └──────── event/Future ready ◄─────┘
                         │
                         ├─ return ─► result
                         ├─ raise  ─► exception
                         └─ cancel ─► CancelledError/cleanup/cancelled
```

Điểm phải nắm:

- `asyncio.create_task()` cần running loop;
- Task được schedule “soon”, không phải cam kết thứ tự nghiệp vụ tuyệt đối;
- phải giữ reference hoặc dùng `TaskGroup`;
- Task có thể được đặt tên để debug;
- `.result()` của `asyncio.Task` chỉ dùng khi đã done; nếu chưa done sẽ `InvalidStateError`, không dùng nó như lệnh chờ blocking;
- cách đúng để chờ Task trong coroutine là `await task`.

### 6.4. `asyncio.Future` `[CORE]`

Future mức thấp biểu diễn kết quả eventual và là cầu nối callback-based code với async/await. Trong application code, ưu tiên coroutine/Task; thư viện mức thấp tạo Future qua `loop.create_future()` để event-loop implementation có thể cung cấp kiểu tối ưu.

Trạng thái:

```text
PENDING ── set_result(value) ─► FINISHED(value)
   │
   ├────── set_exception(e) ──► FINISHED(exception)
   │
   └──────── cancel(msg) ─────► CANCELLED
```

`asyncio.Future`:

- awaitable;
- gắn với loop;
- không thread-safe;
- `.result()`/`.exception()` không nhận timeout;
- nếu pending, `.result()`/`.exception()` raise `InvalidStateError`;
- callback được schedule qua loop thay vì nhất thiết chạy ngay tại dòng đăng ký.

### 6.5. `concurrent.futures.Future` `[CORE]`

Future của executor được tạo bởi `Executor.submit()` và đại diện một callable thường. Nó:

- không await trực tiếp được;
- `.result(timeout)` có thể chặn thread caller;
- `.exception(timeout)` cũng có thể chờ;
- `.cancel()` chỉ thành công nếu công việc chưa chạy/hoàn tất;
- `.running()`, `.done()`, `.cancelled()` phản ánh trạng thái;
- callback chạy theo quy tắc của `concurrent.futures`, không phải event-loop callback.

### 6.6. Bảng phân biệt hai loại Future `[CORE]`

| Thuộc tính | `asyncio.Future`/Task | `concurrent.futures.Future` |
|---|---|---|
| Hệ sinh thái | Event loop, coroutine | Executor thread/process/interpreter |
| Await trực tiếp | Có | Không |
| `.result()` khi pending | `InvalidStateError` | Chặn đến khi xong hoặc timeout |
| Timeout trong `.result()` | Không | Có |
| Thread-safe | Không | Thiết kế cho executor/cross-thread access |
| Dùng với `asyncio.wait` | Có | Không trực tiếp |
| Dùng với `concurrent.futures.wait` | Không | Có |
| Bridge | Native | `wrap_future`, `run_in_executor`; `run_coroutine_threadsafe` trả loại này |

Nguồn chính thức:

- https://docs.python.org/3.14/library/asyncio-future.html
- https://docs.python.org/3.14/library/concurrent.futures.html

### 6.7. Không submit `async def` trực tiếp như callable sync `[CORE]`

`Executor.submit(fn, ...)` gọi `fn(...)` trên worker. Nếu `fn` là coroutine function, kết quả của lời gọi chỉ là coroutine object; executor không tự tạo event loop để await nó. Vì vậy:

- coroutine chạy trên event loop qua `await`, `create_task()` hoặc `TaskGroup`;
- hàm sync blocking/CPU mới là đối tượng điển hình cho executor;
- nếu thật sự cần một event loop riêng trong thread khác, đó là thiết kế nâng cao và phải quản lý loop/thread rõ ràng, không phải chỉ `submit(async_fn)`.

Đây là hệ quả trực tiếp của semantics coroutine trong PEP 492 và `Executor.submit()` trong tài liệu chuẩn.

---

## 7. Event loop và cách khởi chạy chương trình

### 7.1. Vai trò event loop `[CORE]`

Event loop:

- schedule Task và callback;
- theo dõi I/O readiness/completion;
- đánh thức Future/Task khi sự kiện sẵn sàng;
- quản lý timer dựa trên đồng hồ monotonic;
- có API cho network, subprocess, signal, executor và error handler.

Nó không phải một thread pool bí mật và cũng không tự chia một coroutine lên nhiều CPU core.

### 7.2. `asyncio.run()` `[CORE]`

Đây là entry point nên dùng cho chương trình thông thường:

```python
async def main():
    ...

if __name__ == "__main__":
    asyncio.run(main())
```

Nó tạo/quản lý/đóng loop, finalize async generator và đóng default executor. Không được gọi nó trong cùng thread khi một event loop khác đang chạy; trong notebook/REPL async có sẵn, dùng cơ chế `await` của môi trường thay vì lồng `asyncio.run()`.

Từ Python 3.14, đối số có thể là bất kỳ awaitable, không chỉ coroutine object. Nếu code đặt mục tiêu 3.11/3.12/3.13, giữ mẫu `asyncio.run(main())` với `main()` là coroutine để tương thích rõ ràng.

### 7.3. `asyncio.Runner` `[ADVANCED]`

Runner cho phép chạy nhiều top-level awaitable trong cùng event loop và `contextvars.Context`. Nó có từ Python 3.11 và hữu ích cho công cụ hoặc ứng dụng cần nhiều lần gọi top-level mà vẫn chia sẻ loop/context. Không biến nó thành mặc định nếu một lần `asyncio.run()` là đủ.

### 7.4. API loop mức thấp `[ADVANCED]`

- Trong coroutine/callback, ưu tiên `asyncio.get_running_loop()`.
- Python 3.14: `get_event_loop()` raise `RuntimeError` khi không có current event loop; không viết code dựa vào việc loop tự xuất hiện trong mọi context.
- Event-loop policy đã deprecated và dự kiến bị loại bỏ ở 3.16; code cấu hình mới ưu tiên `loop_factory`.
- Tự `new_event_loop()`, `run_forever()`, `stop()`, `shutdown_asyncgens()`, `shutdown_default_executor()` và `close()` chỉ nên nằm ở phần nâng cao/thư viện.

Nguồn:

- https://docs.python.org/3.14/library/asyncio-runner.html
- https://docs.python.org/3.14/library/asyncio-eventloop.html
- https://peps.python.org/pep-3156/

---

## 8. Tạo và phối hợp nhiều tác vụ

### 8.1. Hai `await` nối tiếp `[CORE]`

```python
a = await fetch_a()
b = await fetch_b()
```

`fetch_b()` chỉ được gọi sau khi `fetch_a()` hoàn tất. Cú pháp là async nhưng luồng logic tuần tự. Đây là lựa chọn đúng khi B phụ thuộc A; là lỗi hiệu năng khi hai việc độc lập và mục tiêu là chồng lấp thời gian chờ.

### 8.2. `create_task()` `[CORE]`

```python
task_a = asyncio.create_task(fetch_a(), name="fetch-a")
task_b = asyncio.create_task(fetch_b(), name="fetch-b")
a = await task_a
b = await task_b
```

Đây là fan-out/fan-in thủ công. Người viết chịu trách nhiệm:

- giữ reference;
- chờ cả hai ngay cả khi một cái lỗi;
- quyết định hủy sibling hay để chạy tiếp;
- thu hồi mọi exception;
- cleanup nếu caller bị hủy.

Vì trách nhiệm này dễ sai, công việc có cùng vòng đời thường nên dùng `TaskGroup`.

### 8.3. `asyncio.gather()` `[CORE]`

Semantics bắt buộc thuộc lòng và giải thích được:

- coroutine đầu vào được tự schedule thành Task;
- chạy đồng thời;
- kết quả là list theo **thứ tự đầu vào**;
- mặc định lỗi đầu tiên truyền ra caller ngay;
- những awaitable còn lại **không tự bị hủy** do một phần tử lỗi;
- `return_exceptions=True` đặt exception vào list kết quả;
- nếu chính `gather()` bị hủy, những awaitable chưa hoàn thành được hủy;
- nếu một child bị hủy, `gather()` xử lý nó như `CancelledError` của child thay vì tự coi toàn gather đã bị hủy.

Khi dùng `return_exceptions=True`, phải viết rõ vòng kiểm tra hoặc chính sách tổng hợp; nếu chỉ in list rồi bỏ qua thì demo đang dạy che lỗi.

### 8.4. `TaskGroup` và structured concurrency `[CORE]`

```python
async with asyncio.TaskGroup() as tg:
    task_a = tg.create_task(fetch_a(), name="fetch-a")
    task_b = tg.create_task(fetch_b(), name="fetch-b")

# Ra khỏi block nghĩa là mọi task trong nhóm đã kết thúc.
a = task_a.result()
b = task_b.result()
```

Semantics:

- context manager chờ toàn bộ child khi thoát;
- có thể thêm Task trong lúc group hoạt động;
- lần đầu một child lỗi không phải `CancelledError`, các child còn lại bị hủy;
- sau khi cleanup hoàn tất, lỗi được gom thành `ExceptionGroup` hoặc `BaseExceptionGroup`;
- nested TaskGroup và cancellation có xử lý chuyên biệt; không nuốt `CancelledError` vì làm hỏng structured concurrency;
- có từ Python 3.11.

**So sánh cốt lõi:** `gather()` thích hợp khi muốn kết quả aggregate và chính sách để sibling chạy tiếp; `TaskGroup` thích hợp cho các tác vụ con thuộc cùng một scope và muốn fail-fast có cấu trúc. Không nói “TaskGroup luôn tốt hơn” mà phải nói rõ semantics mong muốn.

### 8.5. `asyncio.wait()` `[CORE]`

```python
done, pending = await asyncio.wait(
    tasks,
    timeout=2.0,
    return_when=asyncio.FIRST_COMPLETED,
)
```

- Đầu vào là Task/Future; từ Python 3.11 không truyền coroutine object thô.
- `return_when`: `FIRST_COMPLETED`, `FIRST_EXCEPTION`, `ALL_COMPLETED`.
- Hết timeout trả pending, **không raise `TimeoutError`**.
- Hết timeout **không hủy** pending.
- Nếu chính `wait()` bị hủy, các Future trong tập không tự bị hủy theo semantics tài liệu 3.14.
- Caller phải quyết định await tiếp, hủy hay chuyển ownership của pending.

### 8.6. `asyncio.as_completed()` `[CORE]`

Dùng khi muốn xử lý kết quả nào xong trước thì dùng trước. Khác `gather`, nó thể hiện completion order.

- `as_completed(aws)` chạy các awaitable trong tập đầu vào theo kiểu concurrent.
- Từ Python 3.13, có thể `async for`: Task/Future đã truyền vào được yield lại chính nó; awaitable khác được tự bọc thành Task và Task đó được yield, nên dễ đối chiếu identity.
- Khi dùng plain `for`, mỗi lượt yield một coroutine mới; phải `await` coroutine này để lấy kết quả hoặc nhận exception của awaitable hoàn thành tiếp theo. Kiểu này tương thích các phiên bản trước 3.13.
- Nếu timeout xảy ra trước khi tất cả hoàn thành, built-in `TimeoutError` được ném trong vòng `async for` hoặc từ coroutine được yield ở plain iteration.
- Timeout hoặc hủy iteration **không tự hủy** các Task còn lại; caller phải quyết định tiếp tục await, hủy hay chuyển ownership.
- Nếu cần tương thích nhiều phiên bản, chỉ dùng pattern được tài liệu của baseline Python mục tiêu hỗ trợ.

### 8.7. Bảng lựa chọn orchestration `[CORE]`

| Nhu cầu | Công cụ phù hợp | Điều phải tự quản lý |
|---|---|---|
| Chờ một tác vụ | `await` | timeout/cancel nếu cần |
| Nhiều việc độc lập, giữ order input | `gather()` | policy khi một việc lỗi |
| Nhiều child cùng lifecycle, fail-fast | `TaskGroup` | xử lý `ExceptionGroup` |
| Chờ một số điều kiện, cần done/pending | `wait()` | xử lý pending |
| Stream kết quả theo completion order | `as_completed()` | timeout/lỗi từng task |
| Fire-and-forget thực sự | collection có ownership/callback, hoặc service-level supervisor | strong ref, exception, shutdown |

Nguồn: https://docs.python.org/3.14/library/asyncio-task.html

---

## 9. Cancellation và timeout

### 9.1. Cancellation là giao thức hợp tác `[CORE]`

`task.cancel()` yêu cầu event loop đưa `CancelledError` vào coroutine tại cơ hội kế tiếp. Nó không bảo đảm Task ngay lập tức chuyển thành cancelled, vì coroutine có thể đang chạy mã CPU không nhường hoặc có thể bắt lỗi.

Mẫu cleanup đúng:

```python
async def worker():
    resource = await acquire_resource()
    try:
        return await use_resource(resource)
    except asyncio.CancelledError:
        # Chỉ thêm thao tác cần thiết để quan sát/cleanup.
        raise
    finally:
        await resource.close()
```

Nguyên tắc:

- đặt cleanup trong `finally`;
- nếu bắt `CancelledError`, re-raise sau cleanup trong hầu hết trường hợp;
- cleanup cũng nên có giới hạn hoặc thiết kế không treo vô hạn;
- cancellation có thể đến tại bất kỳ `await` nào;
- state update phải được thiết kế để không ở trạng thái nửa vời;
- `CancelledError` kế thừa `BaseException` từ 3.8.

### 9.2. `asyncio.timeout()` `[CORE]`

```python
try:
    async with asyncio.timeout(2.0):
        await operation()
except TimeoutError:
    ...
```

- Có từ Python 3.11.
- Context manager hủy **Task hiện tại** khi quá hạn.
- Nó bắt `CancelledError` nội bộ và chuyển thành built-in `TimeoutError`.
- Vì chuyển đổi xảy ra khi thoát context, `TimeoutError` phải được bắt bên ngoài `async with`.
- Timeout context có thể lồng nhau; `Timeout` có thể reschedule và kiểm tra `expired()`.
- `timeout_at(when)` dùng deadline tuyệt đối theo clock của event loop.

### 9.3. `asyncio.wait_for()` `[CORE]`

```python
result = await asyncio.wait_for(operation(), timeout=2.0)
```

- Khi timeout, mặc định hủy awaitable đích và raise `TimeoutError`.
- Hàm chờ việc hủy thật sự hoàn tất, nên tổng wall-clock có thể vượt con số timeout.
- Nếu `wait_for()` bị hủy, awaitable đích cũng bị hủy.
- Muốn tránh hủy đích có thể dùng `shield()`, nhưng phải hiểu ownership của công việc tiếp tục chạy.
- Từ 3.11, raise built-in `TimeoutError`; `asyncio.TimeoutError` chỉ là alias deprecated.

### 9.4. `shield()` `[CORE]`

`await asyncio.shield(task)` ngăn cancellation của coroutine caller tự động truyền vào `task`. Tuy nhiên:

- caller vẫn nhận `CancelledError`;
- task được shield vẫn có thể bị hủy từ nguồn khác hoặc tự hủy;
- phải giữ strong reference đến task;
- sau khi caller bị hủy, cần quyết định ai tiếp tục await/thu hồi kết quả của task;
- lạm dụng shield dễ tạo công việc mồ côi và shutdown khó kiểm soát.

### 9.5. Hủy công việc trong executor `[CORE/APPLIED]`

- `concurrent.futures.Future.cancel()` trả `False` nếu callable đã running hoặc done.
- `Executor.shutdown(cancel_futures=True)` chỉ hủy future chưa chạy; running work tiếp tục.
- Hủy coroutine đang `await asyncio.to_thread(...)` hoặc `run_in_executor(...)` không nên được diễn giải là thread function đã bị cưỡng bức dừng.
- Muốn dừng hợp tác, hàm worker cần cờ/event mà nó chủ động kiểm tra, hoặc chia việc thành đơn vị ngắn.
- Python 3.14 có `ProcessPoolExecutor.terminate_workers()` và `kill_workers()` để tác động toàn worker pool, không phải cơ chế hủy sạch một callable riêng lẻ; đây là giải pháp mạnh và cần cleanup/recovery.

### 9.6. Timeout không phải hard real-time guarantee `[CORE]`

Deadline có thể bị trễ nếu:

- event loop đang bị blocking;
- coroutine không đi qua điểm await;
- cleanup/cancellation mất thời gian;
- OS scheduling và timer resolution có giới hạn;
- worker bên ngoài loop không dừng ngay.

Vì vậy báo cáo phải dùng cách nói “yêu cầu hủy khi quá hạn” hoặc “giới hạn thời gian chờ theo semantics API”, không tuyên bố “chắc chắn dừng đúng mili-giây”.

Nguồn:

- https://docs.python.org/3.14/library/asyncio-task.html#task-cancellation
- https://docs.python.org/3.14/library/asyncio-task.html#timeouts
- https://docs.python.org/3.14/library/asyncio-exceptions.html

---

## 10. Xử lý lỗi và structured failure

### 10.1. Đường truyền exception `[CORE]`

| Nơi lỗi | Lỗi xuất hiện ở đâu |
|---|---|
| Coroutine được `await` trực tiếp | Tại câu `await` |
| Task được `await` | Tại câu `await task` |
| `asyncio.gather(..., return_exceptions=False)` | Lỗi đầu tiên truyền tới caller; sibling tiếp tục |
| `gather(..., return_exceptions=True)` | Exception nằm trong list kết quả |
| `TaskGroup` | Sau cleanup, raise `ExceptionGroup`/`BaseExceptionGroup` |
| `concurrent Future.result()` | Raise lại exception của callable |
| `Executor.map()` | Raise khi lấy phần tử kết quả tương ứng |
| Task lỗi không ai chờ | Log “Task exception was never retrieved” khi được phát hiện |

### 10.2. `ExceptionGroup` và `except*` `[CORE/ADVANCED]`

`TaskGroup` có thể phải báo nhiều lỗi độc lập. Python 3.11 bổ sung `ExceptionGroup` và cú pháp `except*`:

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(job_a())
        tg.create_task(job_b())
except* OSError as group:
    ...
except* ValueError as group:
    ...
```

Phải hiểu:

- một group là cây lỗi, không chỉ list phẳng;
- mỗi `except*` xử lý subgroup theo loại;
- phần không khớp tiếp tục truyền đi;
- không trộn `except` và `except*` trong cùng một `try` statement;
- `return`, `break`, `continue` không hợp lệ trong `except*`;
- không bắt `ExceptionGroup` bằng `except* ExceptionGroup` vì semantics mơ hồ;
- thay đổi API từ một exception thành ExceptionGroup có thể là breaking change.

Nguồn: https://peps.python.org/pep-0654/

### 10.3. Phân loại lỗi ứng dụng `[APPLIED]`

Demo và báo cáo nên phân biệt:

- **lỗi lập trình:** `TypeError`, invariant sai — thường không retry;
- **lỗi input/nghiệp vụ:** dữ liệu không hợp lệ — trả kết quả lỗi có cấu trúc;
- **lỗi tạm thời:** timeout mạng, server busy — có thể retry có giới hạn;
- **lỗi vĩnh viễn:** authentication, endpoint sai — retry thường vô ích;
- **cancellation:** yêu cầu dừng từ caller/shutdown — cleanup rồi truyền tiếp;
- **partial success:** một số task thành công, một số lỗi — cần chính sách rõ, không tùy tiện che lỗi.

### 10.4. Retry, backoff và idempotency `[APPLIED/ADVANCED]`

Đây là kiến thức ứng dụng bên ngoài API cốt lõi nhưng cần để trả lời “nếu API lỗi thì sao”:

- retry phải có số lần tối đa và tổng deadline;
- exponential backoff nên có jitter trong hệ phân tán để tránh đồng loạt retry;
- chỉ retry thao tác an toàn/idempotent hoặc có idempotency key;
- semaphore/queue vẫn phải giới hạn retry như request mới;
- cancellation phải ngắt chu kỳ retry;
- log attempt và nguyên nhân cuối cùng, không log trùng vô hạn.

Không cần biến phần này thành trọng tâm Python syntax; trình bày như nguyên tắc resilience của hệ bất đồng bộ.

---

## 11. `concurrent.futures` từ cơ bản đến đầy đủ

### 11.1. Mục tiêu module `[CORE]`

`concurrent.futures` cung cấp giao diện cấp cao để thực thi callable bất đồng bộ qua các implementation chung của `Executor`:

- `ThreadPoolExecutor`;
- `ProcessPoolExecutor`;
- `InterpreterPoolExecutor` từ Python 3.14.

Tên module chính xác là **`concurrent.futures`** ở dạng số nhiều.

### 11.2. `Executor.submit()` `[CORE]`

```python
future = executor.submit(fn, arg1, arg2, keyword=value)
```

- schedule một callable;
- trả Future ngay;
- kết quả/lỗi được lấy sau;
- submit nhiều Future trước rồi mới chờ mới tạo khả năng chồng lấp;
- submit rồi lập tức `.result()` trong vòng lặp thường vô tình biến thiết kế thành gần tuần tự.

Ví dụ sai về concurrency:

```python
for item in items:
    result = executor.submit(work, item).result()
```

Mẫu đúng hơn:

```python
futures = [executor.submit(work, item) for item in items]
for future in concurrent.futures.as_completed(futures):
    result = future.result()
```

Tuy nhiên với input cực lớn, không submit vô hạn; cần batching hoặc `map(buffersize=...)` trên 3.14.

### 11.3. `Executor.map()` `[CORE/APPLIED]`

Semantics cần nhớ:

- gọi `fn` đồng thời trên nhiều input;
- iterator kết quả giữ thứ tự input;
- exception được raise khi iterator lấy tới kết quả đó;
- `timeout` được tính từ lúc gọi `map()`, không phải reset riêng cho từng phần tử;
- ProcessPool chia iterable thành chunk; tăng `chunksize` có thể cải thiện tập rất dài;
- `chunksize` không tác dụng với ThreadPool/InterpreterPool;
- `buffersize` 3.14 giới hạn số task đã submit nhưng chưa yield kết quả, giúp memory/backpressure.

### 11.4. Shutdown `[CORE]`

Ưu tiên context manager:

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    ...
```

Khi thoát `with`, executor shutdown với `wait=True`. Nếu quản lý thủ công:

- sau shutdown, submit/map mới raise `RuntimeError`;
- `wait=True` chờ pending/running hoàn tất;
- `wait=False` trả ngay nhưng chương trình Python vẫn không thoát cho đến khi pending futures hoàn tất;
- `cancel_futures=True` chỉ hủy pending chưa chạy;
- running Future không tự bị hủy.

### 11.5. `ThreadPoolExecutor` `[CORE]`

Phù hợp:

- blocking I/O;
- API sync phải tích hợp vào async system;
- C extension/native function giải phóng GIL;
- công việc cần chia sẻ memory với chi phí truyền dữ liệu thấp, nhưng phải đồng bộ đúng.

Không lý tưởng:

- pure-Python CPU-bound trên CPython có GIL thông thường;
- task chạy vô hạn/siêu dài mà không có lifecycle rõ;
- worker gọi `.result()` của Future khác trong cùng pool nhỏ và tạo vòng chờ.

Deadlock kinh điển:

- pool 1 worker;
- task A đang chiếm worker;
- A submit B vào cùng pool rồi chờ `B.result()`;
- B không thể chạy vì worker duy nhất đang chờ B.

### 11.6. `ProcessPoolExecutor` `[CORE]`

Ưu điểm:

- dùng process tách biệt;
- vượt GIL cho Python CPU-bound;
- tận dụng đa lõi.

Chi phí/hạn chế:

- process startup và memory lớn hơn thread;
- callable/argument/result phải picklable;
- dữ liệu lớn chịu serialization và IPC;
- `__main__` phải importable;
- không kỳ vọng lambda hoặc hàm định nghĩa tại REPL hoạt động;
- phải bảo vệ entry point;
- không gọi Executor/Future API từ callable trong pool;
- start method khác hệ điều hành và đã thay đổi qua phiên bản.

Python 3.14 thay default start method của `ProcessPoolExecutor` ra khỏi `fork`; nếu thật sự cần `fork`, phải truyền `mp_context` rõ. Trên POSIX, multiprocessing mặc định chung chuyển từ `fork` sang `forkserver` ở 3.14. Không viết báo cáo phụ thuộc cứng vào một start method mà không ghi platform/version.

### 11.7. `InterpreterPoolExecutor` `[ADVANCED]`

Có từ Python 3.14:

- mỗi worker chạy trong thread riêng và interpreter riêng;
- mỗi interpreter có GIL riêng, cho true multi-core parallelism;
- runtime state/module/import bị cô lập;
- mutable object không được chia sẻ trực tiếp như giữa thread thường;
- initializer, callable, argument, result thường cần serialization;
- lỗi khởi tạo hoặc thực thi có các exception chuyên biệt như `BrokenInterpreterPool`, `ExecutionFailed`.

Đây là kiến thức cập nhật giá trị nhưng không nên thay thế ThreadPool/ProcessPool trong mạch cơ bản, vì người học cần hiểu isolation và version requirement trước.

### 11.8. `wait()` và `as_completed()` của `concurrent.futures` `[CORE]`

- `wait(fs, timeout, return_when)` trả `done/not_done`.
- `as_completed(fs, timeout)` yield Future theo completion order.
- Có thể nhận Future từ các Executor khác nhau.
- Timeout của iterator `as_completed` tính từ lúc gọi; có thể raise built-in `TimeoutError`.
- Không đưa `asyncio.Future` vào hai hàm này.

### 11.9. Exception của futures `[CORE/ADVANCED]`

- `CancelledError`;
- built-in `TimeoutError` (`concurrent.futures.TimeoutError` là alias deprecated từ 3.11);
- `InvalidStateError`;
- `BrokenExecutor`;
- `BrokenThreadPool`;
- `BrokenProcessPool`;
- `BrokenInterpreterPool` 3.14+;
- `ExecutionFailed` liên quan InterpreterPool.

Nguồn chính thức:

- https://docs.python.org/3.14/library/concurrent.futures.html
- https://peps.python.org/pep-3148/

---

## 12. Bridge giữa `asyncio` và blocking/parallel work

### 12.1. `asyncio.to_thread()` `[CORE/APPLIED]`

```python
result = await asyncio.to_thread(blocking_io, arg)
```

- Có từ 3.9.
- Chạy hàm trong OS thread, tránh giữ event-loop thread.
- Truyền current `contextvars.Context` sang thread.
- Chủ yếu dành cho I/O-bound blocking trên CPython có GIL.
- Có thể hữu ích CPU-bound nếu extension giải phóng GIL hoặc implementation/build không bị GIL như thông thường.
- Không xem nó là cơ chế kill thread khi timeout/cancel.

### 12.2. `loop.run_in_executor()` `[CORE/APPLIED]`

```python
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(pool, sync_func, arg)
```

- `pool=None` dùng default ThreadPoolExecutor;
- có thể truyền ThreadPool, ProcessPool hoặc InterpreterPool;
- trả `asyncio.Future` để await trên loop;
- với ProcessPool phải dùng `if __name__ == "__main__":` theo quy tắc multiprocessing;
- để truyền keyword argument, tài liệu gợi ý `functools.partial()`.

### 12.3. Gọi từ thread khác vào loop `[ADVANCED]`

- callback: `loop.call_soon_threadsafe(callback, *args)`;
- coroutine: `asyncio.run_coroutine_threadsafe(coro, loop)`;
- hàm thứ hai trả `concurrent.futures.Future` cho thread caller chờ/lấy kết quả/hủy;
- không chạm trực tiếp Task/Future/Lock/Queue của `asyncio` từ thread khác.

### 12.4. Bảng bridge `[CORE]`

| Điểm xuất phát | Công việc đích | API | Kết quả phía caller |
|---|---|---|---|
| Coroutine trên loop | Hàm sync blocking I/O | `to_thread()` | coroutine/await result |
| Coroutine trên loop | Hàm sync trong pool tùy chọn | `run_in_executor()` | `asyncio.Future` |
| Thread khác | Callback trên loop | `call_soon_threadsafe()` | Handle/side effect |
| Thread khác | Coroutine trên loop | `run_coroutine_threadsafe()` | `concurrent.futures.Future` |
| Callback library | Async API mức thấp | `loop.create_future()` + callback set result | awaitable Future |

Nguồn:

- https://docs.python.org/3.14/library/asyncio-task.html#running-in-threads
- https://docs.python.org/3.14/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools
- https://docs.python.org/3.14/library/asyncio-dev.html#concurrency-and-multithreading

---

## 13. Đồng bộ giữa các Task

### 13.1. Vì sao async một thread vẫn có race `[CORE]`

```python
value = state["count"]
await something()
state["count"] = value + 1
```

Giữa read và write có `await`; Task khác có thể đọc cùng giá trị và cập nhật. Kết quả mất update dù hai Task cùng một event-loop thread. Cooperative scheduling giảm số điểm xen kẽ nhưng không tự tạo tính đúng đắn.

### 13.2. `asyncio.Lock` `[CORE]`

Mục tiêu: mutual exclusion cho shared resource giữa Task trong cùng loop.

```python
async with lock:
    update_shared_state()
```

- không thread-safe;
- `acquire()` là fair theo thứ tự bắt đầu chờ như tài liệu 3.14;
- release khi chưa locked raise `RuntimeError`;
- ưu tiên `async with`;
- critical section càng ngắn càng tốt;
- tránh gọi I/O không giới hạn trong lock nếu không bắt buộc.

### 13.3. `asyncio.Event` `[CORE]`

Một cờ thông báo one-to-many:

- `wait()` chờ flag true;
- `set()` đánh thức toàn bộ waiter;
- `clear()` đưa về false;
- không mang dữ liệu và không đếm số sự kiện;
- nếu cần từng item, dùng Queue thay vì Event.

### 13.4. `asyncio.Condition` `[APPLIED]`

Kết hợp Lock và khả năng chờ predicate trạng thái:

- waiter phải giữ lock rồi `wait()`; wait tạm nhả lock và reacquire trước khi trả;
- notifier phải giữ lock khi `notify/notify_all`;
- wake-up có thể spurious, luôn kiểm tra lại predicate;
- `wait_for(predicate)` lặp kiểm tra giúp biểu diễn đúng điều kiện.

### 13.5. `Semaphore` và `BoundedSemaphore` `[CORE/APPLIED]`

Semaphore đếm permit để giới hạn số Task vào khu vực:

```python
sem = asyncio.Semaphore(10)

async with sem:
    await call_remote_service()
```

- phù hợp giới hạn connection/in-flight request/tài nguyên;
- không phải rate limit theo giây;
- `Semaphore` cho phép release vượt số acquire ban đầu;
- `BoundedSemaphore` raise `ValueError` nếu release vượt giá trị khởi tạo, hữu ích phát hiện lỗi cân bằng;
- không giả định fairness nếu tài liệu không cam kết.

### 13.6. `Barrier` `[APPLIED/ADVANCED]`

- Có từ Python 3.11.
- Chặn cho đến khi đủ `parties` Task chờ rồi giải phóng cùng đợt.
- Tái sử dụng được.
- Cancellation làm giảm waiter trong trạng thái filling.
- `reset/abort` có thể làm waiter nhận `BrokenBarrierError`.
- Chỉ dùng khi bài toán thật sự có phase synchronization; không dùng để thay Queue/TaskGroup.

### 13.7. Primitive async không dành cho OS thread `[CORE]`

`asyncio.Lock/Event/Condition/Semaphore/Barrier/Queue` không thread-safe. Nếu đồng bộ OS thread, dùng primitive của `threading`; nếu trao dữ liệu giữa thread và event loop, dùng API thread-safe/queue thích hợp.

Nguồn: https://docs.python.org/3.14/library/asyncio-sync.html

---

## 14. Queue, producer–consumer và backpressure

### 14.1. `asyncio.Queue` `[CORE/APPLIED]`

```python
queue = asyncio.Queue(maxsize=100)
```

- FIFO;
- `await put()` chờ khi queue đầy;
- `await get()` chờ khi queue rỗng;
- `put_nowait()` có thể raise `QueueFull`;
- `get_nowait()` có thể raise `QueueEmpty`;
- `qsize()` trả kích thước hiện tại;
- không thread-safe;
- phương thức không có timeout parameter; dùng timeout bên ngoài.

### 14.2. Pattern worker đúng `[APPLIED]`

```python
async def worker(queue):
    while True:
        item = await queue.get()
        try:
            await process(item)
        finally:
            queue.task_done()
```

Nếu `process()` lỗi/cancel mà không `task_done()` trong `finally`, `queue.join()` có thể chờ mãi.

### 14.3. Shutdown queue `[APPLIED]`

Python 3.13+ có `queue.shutdown(immediate=False)` và `QueueShutDown`:

- không nhận item mới;
- unblock producer đang chờ và báo lỗi;
- graceful mode cho consumer rút hết item;
- khi rỗng, `get()` tiếp theo raise `QueueShutDown`;
- `immediate=True` drain ngay và có thể phá invariant thông thường của `join()`, nên phải giải thích rủi ro.

Nếu support Python <=3.12, dùng sentinel hoặc cancellation theo protocol riêng và ghi rõ khác biệt.

### 14.4. `PriorityQueue` và `LifoQueue` `[APPLIED]`

- `PriorityQueue`: lấy priority nhỏ trước, thường item là `(priority, data)`; cần tránh lỗi so sánh khi priority bằng nhau và data không comparable bằng cách thêm tie-breaker.
- `LifoQueue`: last in, first out; dùng khi việc mới quan trọng hơn theo thiết kế, nhưng phải cân nhắc starvation của item cũ.

### 14.5. Queue khác Semaphore `[CORE]`

- Queue lưu và điều tiết **đơn vị công việc** giữa producer/consumer.
- Semaphore điều tiết **số quyền truy cập đồng thời** vào khu vực/tài nguyên.
- Có thể dùng cả hai: queue bounded giới hạn backlog; semaphore giới hạn API call trong mỗi worker.

Nguồn: https://docs.python.org/3.14/library/asyncio-queue.html

---

## 15. Async I/O cấp ứng dụng

### 15.1. Streams `[APPLIED]`

Streams là API async/await cấp cao cho network connection, tránh phải dùng callback/transport trực tiếp:

- client: `asyncio.open_connection()` → `(reader, writer)`;
- server: `asyncio.start_server()`;
- đọc: `read`, `readline`, `readexactly`, `readuntil`;
- ghi: `write` rồi `await drain()`;
- đóng: `writer.close()` rồi `await writer.wait_closed()`.

Lỗi cần biết:

- `IncompleteReadError`: EOF trước khi đủ dữ liệu, có `.partial` và `.expected`;
- `LimitOverrunError`: vượt buffer limit khi tìm separator;
- protocol framing sai có thể treo hoặc tốn memory.

`drain()` là flow control. Nếu buffer dưới high watermark, nó có thể trả ngay; vòng ghi nóng vẫn có thể cần chủ động nhường theo tài liệu.

Nguồn: https://docs.python.org/3.14/library/asyncio-stream.html

### 15.2. File I/O `[CORE/APPLIED]`

Event loop không giám sát regular file I/O qua `add_reader/add_writer` trên các platform. Standard file API thường blocking; nếu demo đọc/ghi file đáng kể, dùng `to_thread()` hoặc giải pháp phù hợp, không gắn `async def` rồi cho rằng file đã non-blocking.

Nguồn: https://docs.python.org/3.14/library/asyncio-platforms.html

### 15.3. Subprocess `[ADVANCED]`

`asyncio.create_subprocess_exec()`/`create_subprocess_shell()` cho phép start và giao tiếp process bất đồng bộ.

- Ưu tiên `create_subprocess_exec` khi có thể; shell command cần quoting chống shell injection.
- `Process.wait()` với `stdout=PIPE`/`stderr=PIPE` có thể deadlock nếu child làm đầy OS pipe; dùng `communicate()`.
- `communicate()` buffer output trong memory, không phù hợp output vô hạn.
- Process async không thread-safe.
- Windows subprocess yêu cầu ProactorEventLoop; đây là default từ 3.8, nhưng vẫn phải hiểu giới hạn platform.

Nguồn: https://docs.python.org/3.14/library/asyncio-subprocess.html

### 15.4. Transports và protocols `[ADVANCED]`

Đây là API thấp dành cho library/framework author:

- transport quản lý kênh I/O và buffering;
- protocol nhận callback sự kiện;
- Future bridge callback với `await`;
- application thông thường ưu tiên Streams.

Chỉ đưa vào phụ lục nếu tài liệu gốc nhắc event loop components hoặc giáo viên hỏi mức thấp.

---

## 16. Async context manager, iterator, generator và comprehension

### 16.1. `async with` `[CORE/APPLIED]`

Đối tượng định nghĩa `__aenter__()`/`__aexit__()` trả awaitable. Dùng cho tài nguyên có bước mở/đóng async: connection, transaction, lock, timeout, TaskGroup.

Điểm cần hiểu:

- không dùng `with` cho async context manager và ngược lại;
- `__aexit__` là nơi cleanup, nhưng vẫn có thể bị cancellation; library phải thiết kế an toàn;
- nhiều cấu trúc cốt lõi (`Lock`, `Semaphore`, `TaskGroup`, `timeout`) dùng `async with` vì scope thể hiện ownership.

### 16.2. `async for` `[APPLIED]`

Async iterable có `__aiter__`; async iterator có `__anext__` trả awaitable. Mỗi vòng có thể chờ dữ liệu đến mà không chặn event-loop thread.

Không đánh đồng “async iteration” với xử lý song song từng item. `async for` mặc định lấy và xử lý theo vòng; muốn parallelize processing phải fan-out có giới hạn và giữ ordering/error policy rõ.

### 16.3. Async generator `[ADVANCED]`

```python
async def stream_items():
    while ...:
        item = await receive()
        yield item
```

- Có thể await giữa các lần yield.
- Kết thúc qua `StopAsyncIteration`.
- `return value` không được dùng như generator thường để trả giá trị cuối.
- Khi break sớm, gọi `aclose()` hoặc dùng `contextlib.aclosing()` để cleanup deterministic.
- `asyncio.run()` hỗ trợ finalization, nhưng explicit close vẫn tốt hơn khi dependency/order cleanup quan trọng.

### 16.4. Async comprehension `[ADVANCED]`

PEP 530 cho phép:

```python
values = [item async for item in source()]
results = [await transform(x) for x in values]
```

Nhấn mạnh: comprehension thứ hai await tuần tự. Nếu muốn concurrent transform, phải tạo Task/TaskGroup/gather có giới hạn phù hợp.

Nguồn:

- https://peps.python.org/pep-0492/
- https://peps.python.org/pep-0525/
- https://peps.python.org/pep-0530/
- https://docs.python.org/3.14/library/asyncio-dev.html#asynchronous-generators-best-practices

---

## 17. `contextvars` và trạng thái theo Task

### 17.1. Vấn đề `[ADVANCED]`

`threading.local()` gắn state với thread. Nhiều asyncio Task lại chia sẻ cùng event-loop thread, nên thread-local không phân biệt request/task. `ContextVar` cung cấp context-local state được `asyncio` hỗ trợ native.

Ứng dụng:

- request ID/tracing ID;
- tenant/user context;
- logging correlation;
- transaction/request-scoped settings.

### 17.2. Semantics cần biết `[ADVANCED]`

- Task sao chép current context khi được tạo nếu không truyền context riêng.
- Mỗi Task chạy trong context của nó khi được resume.
- `ContextVar.set()` trả Token để reset lại giá trị trước.
- Khai báo `ContextVar` ở module top-level, không tạo trong closure, vì Context giữ strong reference.
- `asyncio.to_thread()` truyền current context sang worker thread.
- Context không phải công cụ đồng bộ dữ liệu mutable; nó cô lập binding theo context.

Nguồn:

- https://docs.python.org/3.14/library/contextvars.html
- https://peps.python.org/pep-0567/

---

## 18. GIL, free-threaded Python và nhiều interpreter

### 18.1. GIL trên CPython thông thường `[CORE]`

GIL bảo đảm chỉ một thread thực thi Python bytecode tại một thời điểm trong interpreter. Hệ quả:

- ThreadPool không thường tăng throughput cho pure-Python CPU-bound;
- I/O vẫn phù hợp thread vì GIL được nhả quanh blocking I/O;
- một số extension giải phóng GIL khi tính toán, nên thread có thể đạt parallelism;
- GIL không thay thế lock cho invariant gồm nhiều thao tác; race logic vẫn xảy ra.

### 18.2. Free-threaded build `[ADVANCED]`

- Python 3.13 bắt đầu hỗ trợ build có thể tắt GIL; không phải cấu hình mặc định của mọi máy.
- Có thể kiểm tra support/config bằng cơ chế tài liệu chính thức, ví dụ `sysconfig.get_config_var("Py_GIL_DISABLED")`; runtime có `sys._is_gil_enabled()` theo tài liệu free-threading.
- Extension chưa tương thích có thể làm GIL được bật lại.
- Built-in có internal lock nhưng không nên dựa vào hành vi concurrent modification không được bảo đảm; dùng synchronization rõ ràng.
- Free-threaded build có overhead và hạn chế riêng; không tuyên bố “GIL đã biến mất khỏi Python”.
- Python 3.14 có hỗ trợ asyncio first-class trong môi trường free-threaded, ví dụ một event loop cho mỗi thread; vẫn không chia sẻ một loop/Task/Future qua thread tùy tiện.

### 18.3. Per-interpreter GIL `[ADVANCED]`

Subinterpreter có runtime state cô lập và GIL riêng, là nền tảng cho `InterpreterPoolExecutor`. Trade-off là isolation/communication rõ ràng. Đây không phải shared-memory thread thông thường cũng không hoàn toàn là process OS.

Nguồn:

- https://docs.python.org/3.14/library/threading.html#gil-and-performance-considerations
- https://docs.python.org/3.14/howto/free-threading-python.html
- https://docs.python.org/3.14/library/asyncio-threading.html
- https://peps.python.org/pep-0703/
- https://peps.python.org/pep-0734/

---

## 19. Hiệu năng và đo lường đúng

### 19.1. Mô hình lợi ích `[CORE]`

Với N thao tác I/O độc lập, mỗi thao tác gồm CPU ngắn + chờ dài:

- tuần tự gần tổng toàn bộ thời gian chờ;
- concurrent có thể chồng lấp phần chờ, nhưng bị giới hạn bởi service, connection, network, semaphore, overhead và tail latency;
- speedup không mặc nhiên bằng N;
- quá nhiều concurrency có thể làm chậm hơn vì contention, queueing, rate limit, memory và retry.

### 19.2. Chi phí phải tính `[CORE/APPLIED]`

- tạo/schedule Task;
- context switch hợp tác;
- memory mỗi Task và buffer;
- thread context switching/stack;
- process startup, serialization, IPC;
- interpreter isolation/serialization;
- connection limit và server rate limit;
- lock contention và queue wait;
- logging/printing trong benchmark;
- warm-up, cache, DNS, connection reuse.

### 19.3. Bounded concurrency `[CORE/APPLIED]`

Không dùng pattern không giới hạn trên input lớn:

```python
await asyncio.gather(*(call(x) for x in one_million_items))
```

Các chiến lược:

- `Semaphore` quanh operation;
- worker pool bằng `asyncio.Queue(maxsize=...)`;
- xử lý input theo batch;
- stream bằng async iterator;
- `Executor.map(buffersize=...)` trên 3.14;
- giới hạn connection pool ở client/library;
- theo dõi queue wait và in-flight count để biết bottleneck.

### 19.4. Benchmark tối thiểu `[APPLIED]`

1. Định nghĩa cùng workload và cùng dữ liệu cho tuần tự/concurrent/parallel.
2. Tách I/O simulation khỏi CPU work; ghi rõ nếu dùng `asyncio.sleep()` chỉ để mô phỏng.
3. Dùng `time.perf_counter()`/`perf_counter_ns()` cho elapsed duration.
4. Warm up nếu có cache/process startup.
5. Chạy nhiều lần; báo median và phân tán, không chỉ một con số đẹp.
6. Xác minh kết quả đúng trước khi so tốc độ.
7. Ghi Python version, OS, CPU, số worker, mức concurrency, input size.
8. Đo thêm throughput, p95/p99 latency nếu có nhiều request, CPU, memory và error count.
9. Không in/log dày trong vùng đo vì I/O console làm méo kết quả.
10. Giải thích crossover: workload quá nhỏ có thể bị overhead lấn át.

Nguồn thời gian: https://docs.python.org/3.14/library/time.html#time.perf_counter

### 19.5. Eager task factory `[ADVANCED]`

Python 3.12+ có `asyncio.eager_task_factory()`; Python 3.14 `create_task()` có `eager_start`:

- coroutine bắt đầu sync ngay khi tạo Task và chỉ schedule nếu block;
- có thể giảm overhead cho coroutine thường hoàn thành sync do cache;
- **thay đổi semantics/thứ tự thực thi**;
- nếu coroutine return/raise trước khi block, nó có thể chưa từng được đưa vào loop queue;
- chỉ dùng sau profiling và có test về ordering/reentrancy.

Không đưa eager execution vào demo nhập môn như tối ưu mặc định.

---

## 20. Deadlock, starvation, overload và các bẫy

### 20.1. Danh sách bẫy bắt buộc nhận diện `[CORE]`

1. Gọi coroutine nhưng quên `await`/schedule.
2. Dùng hai `await` tuần tự nhưng nói là chạy đồng thời.
3. Dùng `time.sleep()` trong coroutine.
4. Gọi HTTP/DB/file client blocking trực tiếp trong event loop.
5. Chạy CPU loop dài trên event-loop thread.
6. Submit Future rồi `.result()` ngay từng vòng, làm mất concurrency.
7. Nhầm `asyncio.Future` với `concurrent.futures.Future`.
8. Gọi `.result()` trên pending asyncio Task/Future và kỳ vọng nó chờ.
9. Không giữ strong reference đến background Task.
10. Không await/thu hồi exception của Task nền.
11. Cho rằng `gather()` tự cancel sibling khi một child lỗi.
12. Dùng `return_exceptions=True` rồi không kiểm tra exception.
13. Hết timeout ở `wait()` nhưng bỏ mặc pending Task.
14. Nuốt `CancelledError` và làm `TaskGroup`/timeout sai semantics.
15. Dùng `shield()` rồi bỏ ownership của task tiếp tục chạy.
16. Cho rằng cancel `to_thread` giết được thread function.
17. Không đặt timeout/deadline cho external I/O có thể treo.
18. Tạo Task không giới hạn trên input lớn.
19. Dùng Semaphore như rate limiter theo giây.
20. Quên `task_done()` khiến Queue.join treo.
21. Dùng `asyncio.Queue` giữa OS threads.
22. Giữ Lock trong lúc chờ I/O dài và gây convoy/deadlock.
23. Lock nhiều tài nguyên không theo thứ tự thống nhất.
24. ThreadPool task chờ Future khác trong pool đã cạn worker.
25. ProcessPool dùng lambda/local function/unpicklable object.
26. Quên `if __name__ == "__main__":` với multiprocessing.
27. ProcessPool worker gọi Executor/Future method và deadlock.
28. Đưa async function trực tiếp vào Executor và chỉ nhận coroutine object.
29. Ghi stream nhưng không `drain()`; đóng không `wait_closed()`.
30. Subprocess `wait()` với PIPE đầy thay vì `communicate()`.
31. Dừng async generator sớm nhưng không đóng rõ ràng.
32. Gọi `asyncio.run()` lồng trong loop đang chạy.
33. Gọi object asyncio từ thread khác mà không dùng API thread-safe.
34. Dựa vào task scheduling order không được bảo đảm.
35. Benchmark chỉ một lần, khác workload hoặc tính cả print không nhất quán.
36. Tuyên bố “async nhanh hơn X lần” mà không ghi môi trường và giới hạn.
37. Nói GIL đã bị loại bỏ hoàn toàn chỉ vì Python có free-threaded build tùy chọn.
38. Dùng API 3.13/3.14 nhưng không ghi phiên bản tối thiểu.

### 20.2. Starvation `[CORE]`

Một Task chiếm loop quá lâu không await khiến Task khác không tiến triển. Dấu hiệu:

- timer/heartbeat trễ;
- request khác latency tăng dù CPU chưa phân bố đa lõi;
- debug mode báo slow callback;
- queue tăng backlog.

Giải pháp: chia nhỏ computation có chủ đích hoặc offload; không lạm dụng `sleep(0)` trong vòng CPU như phương pháp tối ưu chính.

### 20.3. Overload `[APPLIED]`

Async làm việc tạo concurrency rất dễ, nên overload là rủi ro lớn:

- nhiều socket/file descriptor;
- memory giữ Task/buffer;
- remote rate limit;
- timeout hàng loạt;
- retry storm;
- queueing làm deadline hết trước khi task bắt đầu.

Phải có capacity limit, timeout tổng, backpressure và observability.

---

## 21. Debugging và observability

### 21.1. Bật debug mode `[CORE/APPLIED]`

Các cách chính thức:

- biến môi trường `PYTHONASYNCIODEBUG=1`;
- Python Development Mode;
- `asyncio.run(..., debug=True)`;
- `loop.set_debug(True)`.

Kết hợp:

- logger `asyncio` ở mức DEBUG khi điều tra;
- bật `ResourceWarning`, ví dụ tùy chọn `-W default`;
- điều chỉnh `loop.slow_callback_duration` nếu cần.

Debug mode hỗ trợ:

- báo API non-thread-safe gọi sai thread;
- log I/O selector chậm;
- log callback vượt ngưỡng mặc định 100 ms;
- cho traceback tốt hơn với coroutine never-awaited và Task exception never-retrieved.

### 21.2. Logging `[APPLIED]`

- Đặt tên Task có ý nghĩa.
- Log task/request ID qua ContextVar nếu có nhiều request.
- Log start/end/duration/status ở boundary, không spam mỗi vòng.
- Network logging handler có thể block event loop; xử lý log blocking ở thread hoặc non-blocking pipeline.
- Không che cancellation thành lỗi chung nếu chính sách coi đó là shutdown bình thường.

### 21.3. Introspection `[APPLIED/ADVANCED]`

Cơ bản:

- `asyncio.current_task()`;
- `asyncio.all_tasks()`;
- `task.get_name()/set_name()`;
- `task.get_stack()/print_stack()`;
- trạng thái `done/cancelled`, `result/exception` khi đã done.

Python 3.14 bổ sung call graph introspection:

- `asyncio.print_call_graph()`;
- `asyncio.format_call_graph()`;
- `asyncio.capture_call_graph()`.

Gắn nhãn 3.14, không dùng làm yêu cầu chạy trên 3.11 nếu dự án đặt baseline 3.11.

### 21.4. Cảnh báo phải biết `[CORE]`

- `RuntimeWarning: coroutine '...' was never awaited` → đã tạo coroutine nhưng không await/schedule.
- `Task exception was never retrieved` hoặc `Future exception was never retrieved` → Task/Future tương ứng bị lỗi nhưng không ai lấy exception.
- `Task was destroyed but it is pending` → lifecycle/shutdown/reference sai.
- `InvalidStateError` → lấy/set result sai trạng thái.
- `BrokenProcessPool/BrokenThreadPool/...` → worker/pool hỏng, không tiếp tục submit như bình thường.

Nguồn:

- https://docs.python.org/3.14/library/asyncio-dev.html
- https://docs.python.org/3.14/library/asyncio-task.html#introspection
- https://docs.python.org/3.14/library/asyncio-graph.html

---

## 22. Kiểm thử chương trình bất đồng bộ

### 22.1. Công cụ chuẩn `[APPLIED]`

`unittest.IsolatedAsyncioTestCase`:

- chấp nhận async test method;
- `asyncSetUp()`/`asyncTearDown()`;
- `addAsyncCleanup()`;
- `enterAsyncContext()`;
- mỗi test có loop được quản lý; cuối test các Task còn trong loop bị hủy.

`unittest.mock.AsyncMock`:

- hành xử như async function, gọi trả awaitable;
- hỗ trợ `assert_awaited`, `assert_awaited_once`, `assert_awaited_with`, `assert_has_awaits`, `assert_not_awaited`;
- `side_effect` có thể trả giá trị, raise exception hoặc cung cấp chuỗi kết quả.

Nguồn:

- https://docs.python.org/3.14/library/unittest.html#unittest.IsolatedAsyncioTestCase
- https://docs.python.org/3.14/library/unittest.mock.html#unittest.mock.AsyncMock

### 22.2. Ma trận test bắt buộc `[CORE/APPLIED]`

| Khía cạnh | Test cần có |
|---|---|
| Success | Đúng kết quả và đủ số item |
| Concurrency | In-flight không vượt giới hạn; có overlap thực sự |
| Ordering | `gather/map` giữ input order; `as_completed` không bị hiểu sai |
| Failure | Một child lỗi; xác minh policy với sibling |
| TaskGroup | Sibling bị cancel và ExceptionGroup được xử lý đúng |
| Timeout | Raise đúng loại lỗi; biết target có bị cancel hay tiếp tục |
| Cancellation | Cleanup chạy; `CancelledError` được truyền lại |
| Queue | Mỗi `get` có `task_done`; join kết thúc; shutdown đúng |
| Resource | Stream/file/client/executor đóng ngay cả khi lỗi |
| Blocking | Heartbeat/second task không bị dừng bởi operation đáng lẽ non-blocking |
| Executor | Callable exception truyền về; pending cancel đúng semantics |
| Process | Pickling/entry-point behavior được kiểm tra trên platform mục tiêu |
| Leak | Sau test không còn background task ngoài danh sách cho phép |

### 22.3. Tránh test flaky `[APPLIED]`

- Không dùng `sleep()` dài để “hy vọng” task đã chạy.
- Dùng `Event`, Future hoặc Queue để tạo synchronization point xác định.
- Khi buộc dùng timeout, đặt timeout như safety bound chứ không dùng timing làm assertion chính.
- Không assert một thứ tự scheduling mà API không bảo đảm.
- Cleanup mọi Task trong `finally` hoặc TaskGroup.
- Test cancellation ở điểm await có kiểm soát.
- Tách logic thuần thành function sync để unit test nhanh; integration test async chỉ kiểm tra orchestration.

---

## 23. Graceful shutdown

### 23.1. Quy trình chuẩn `[APPLIED]`

```text
Nhận tín hiệu dừng
   │
   ├─ Ngừng nhận công việc mới
   ├─ Báo producer dừng / shutdown queue
   ├─ Cho phép drain trong deadline nếu chính sách yêu cầu
   ├─ Cancel task còn lại
   ├─ Await task để cleanup và thu hồi exception
   ├─ Đóng stream/client/server/subprocess
   ├─ Shutdown executor
   └─ Kiểm tra không còn task/tài nguyên rò rỉ
```

### 23.2. Quy tắc `[CORE/APPLIED]`

- Cancel rồi phải await Task; chỉ gọi `.cancel()` và bỏ đi là chưa cleanup.
- Thu thập exception khi await shutdown; phân biệt cancellation bình thường và lỗi cleanup.
- Đặt deadline cho shutdown, nhưng hiểu worker thread/process có semantics dừng riêng.
- `asyncio.run()` quản lý SIGINT qua cancellation của main task rồi chuyển thành `KeyboardInterrupt`; `try/finally` cho phép cleanup.
- Signal handling yêu cầu event loop ở main thread; Windows có giới hạn khác Unix.
- TaskGroup giúp child không sống vượt scope.
- Stream dùng `close/wait_closed`; async generator dừng sớm dùng `aclose`; executor dùng context manager/shutdown.

Nguồn: https://docs.python.org/3.14/library/asyncio-runner.html#handling-keyboard-interruption

---

## 24. Ma trận phiên bản Python

> Nhóm phải chọn và ghi một baseline. Đề xuất học thuật: **Python >= 3.11** để dùng `TaskGroup`, `asyncio.timeout()` và `ExceptionGroup`; phần 3.13/3.14 đặt rõ nhãn mở rộng. Nếu máy demo là phiên bản khác, kiểm tra thực tế trước khi chốt.

| Phiên bản | Thay đổi liên quan cần biết | Ảnh hưởng đến báo cáo/demo |
|---|---|---|
| 3.7 | `asyncio.run()`, `create_task()`, contextvars support phổ biến trong Task | Nền của style asyncio hiện đại |
| 3.8 | `CancelledError` chuyển từ `Exception` sang `BaseException`; task name; `IsolatedAsyncioTestCase`, `AsyncMock` | Không dạy bắt cancellation bằng `except Exception` |
| 3.9 | `asyncio.to_thread()`; `Executor.shutdown(cancel_futures=...)` | Bridge blocking I/O thuận tiện; hủy chỉ pending Future |
| 3.10 | Nhiều tham số `loop=` bị loại; warning khi API tạo task/future không có running loop | Dùng API high-level/current loop |
| 3.11 | `TaskGroup`, `asyncio.timeout()/timeout_at()`, `Runner`, `Barrier`, `ExceptionGroup/except*`; `asyncio.TimeoutError` thành alias built-in `TimeoutError`; `wait()` cấm coroutine thô | Baseline tốt cho structured concurrency |
| 3.12 | eager task factory; Task eager start; `Task.get_context()`; `wait_for()` implementation/behavior được cập nhật; generator yield task trong wait/as_completed | Eager là advanced, có thay đổi ordering |
| 3.13 | `Queue.shutdown()/QueueShutDown`; `as_completed()` hỗ trợ async iterator; cải thiện simultaneous cancellation của TaskGroup; default worker tính qua `os.process_cpu_count`; free-threaded build khả dụng tùy chọn | Gắn nhãn; không dùng nếu baseline 3.11 mà không fallback |
| 3.14 | `InterpreterPoolExecutor`; `Executor.map(buffersize=...)`; `ProcessPoolExecutor.terminate_workers()/kill_workers()`; process start method đổi khỏi fork; `create_task(..., eager_start=...)`; `asyncio.run()` nhận any awaitable; call graph introspection; `get_event_loop()` nghiêm hơn; policy deprecated; asyncio hỗ trợ free-threaded rõ hơn | Phần cập nhật/appendix; tránh làm code baseline 3.11 hỏng |
| 3.16 dự kiến | Event-loop policy system bị loại theo docs 3.14 | Code mới dùng `loop_factory`, không đầu tư vào policy cũ |

### 24.1. Những phát biểu phiên bản dễ sai `[CORE]`

- Sai: “`CancelledError` là `Exception` bình thường.” Đúng với lịch sử cũ, sai từ 3.8.
- Sai: “Luôn bắt `asyncio.TimeoutError`.” Từ 3.11 dùng built-in `TimeoutError`; tên asyncio là alias deprecated.
- Sai: “`TaskGroup` có trong mọi Python 3.” Nó có từ 3.11.
- Sai: “Queue luôn có `shutdown()`.” Chỉ từ 3.13.
- Sai: “`as_completed()` luôn là async iterator.” Chỉ từ 3.13 mới hỗ trợ cả async/plain iterator.
- Sai: “Python đã bỏ GIL.” Free-threaded build là tùy chọn; cấu hình thông thường vẫn cần kiểm tra.
- Sai: “ProcessPool luôn fork trên Linux.” Default đã thay đổi trong 3.14.
- Sai: “Event-loop policy là hướng cấu hình tương lai.” Nó đã deprecated và dự kiến bỏ ở 3.16.

---

## 25. Khác biệt nền tảng và hệ điều hành

### `[ADVANCED]`

- Trên Windows, ProactorEventLoop là default từ 3.8 và hỗ trợ subprocess; SelectorEventLoop trên Windows không hỗ trợ subprocess và có giới hạn socket.
- `loop.add_signal_handler()` không được hỗ trợ trên Windows.
- Regular file không được theo dõi bằng `add_reader/add_writer` trên các platform.
- Clock resolution phụ thuộc OS/hardware; không viết test dựa vào timing mili-giây quá chặt.
- Process start method và yêu cầu safe import khác nhau; Windows dùng spawn-style behavior nên lỗi thiếu main guard dễ lộ rõ.
- `asyncio` và `concurrent.futures` không khả dụng trên WASI; chỉ cần nhắc trong phụ lục nếu nói tính portable.

Nguồn:

- https://docs.python.org/3.14/library/asyncio-platforms.html
- https://docs.python.org/3.14/library/multiprocessing.html#contexts-and-start-methods
- https://docs.python.org/3.14/library/concurrent.futures.html

---

## 26. Ranh giới giữa Core, Applied và Advanced

### 26.1. Core — phải nằm trong mạch báo cáo chính

1. Bài toán thời gian chờ và vì sao cần async.
2. Tuần tự/concurrency/parallelism/asynchrony.
3. Blocking/non-blocking, I/O-bound/CPU-bound.
4. Event loop và cooperative scheduling.
5. Coroutine function/object, awaitable, `async/await`.
6. Task và Future; hai loại Future.
7. `asyncio.run`, `create_task`, `gather`, `TaskGroup`.
8. `wait`, `as_completed` ở mức lựa chọn.
9. Cancellation, `CancelledError`, `try/finally`.
10. Timeout, `wait_for`, `timeout`, `shield`.
11. `concurrent.futures`: Executor/Future/submit/map/shutdown.
12. ThreadPool vs ProcessPool và GIL/pickling/main guard.
13. Race/deadlock/starvation và nhận diện blocking.
14. Bounded concurrency, Semaphore/Queue ở mức cốt lõi.
15. Xử lý lỗi và ownership/cleanup.
16. Đo hiệu năng đúng và kết luận có điều kiện.

### 26.2. Applied — phải có trong tài liệu GitHub và demo/test

1. Producer–consumer bằng bounded Queue.
2. Giới hạn in-flight bằng Semaphore.
3. Timeout/cancellation path có cleanup.
4. Bridge sync I/O bằng `to_thread` hoặc executor.
5. Benchmark sequential vs bounded async; có metadata.
6. Test success/failure/timeout/cancel/cleanup.
7. Debug mode, task naming, kiểm tra leak.
8. Graceful shutdown.
9. Flow control nếu demo có stream.
10. Error classification/retry policy nếu demo gọi service giả lập.

### 26.3. Advanced — đặt phụ lục/notes, phân công chuyên sâu

1. Low-level loop/transports/protocols.
2. Async iterator/generator/comprehension và explicit `aclose()`.
3. `contextvars`.
4. `ExceptionGroup/except*` chi tiết.
5. InterpreterPoolExecutor và multiple interpreters.
6. Free-threaded CPython/PEP 703.
7. Eager task factory/eager_start.
8. Process start methods, terminate/kill workers.
9. Async subprocess và platform caveats.
10. Call graph introspection Python 3.14.

---

## 27. Chuẩn nắm bài chung cho cả 6 thành viên

Mỗi thành viên phải tự hoàn thành checklist dưới đây. Không chỉ trưởng nhóm hoặc người thuyết trình phần đó mới biết.

### 27.1. Checklist giải thích `[CORE]`

- [ ] Định nghĩa đúng tuần tự, đồng thời, song song, bất đồng bộ.
- [ ] Vẽ được timeline tuần tự và async concurrent.
- [ ] Giải thích vì sao async không tự là parallelism.
- [ ] Phân loại được I/O-bound, CPU-bound và pipeline hỗn hợp.
- [ ] Giải thích blocking/non-blocking bằng event-loop thread.
- [ ] Phân biệt coroutine function và coroutine object.
- [ ] Nêu ba loại awaitable thường gặp.
- [ ] Giải thích lúc nào coroutine bắt đầu chạy.
- [ ] Phân biệt `await f(); await g()` và tạo hai Task.
- [ ] Mô tả cooperative scheduling và điểm nhường.
- [ ] Mô tả event loop làm gì và không làm gì.
- [ ] Phân biệt Task, `asyncio.Future`, `concurrent.futures.Future`.
- [ ] Giải thích khác biệt `.result()` của hai Future.
- [ ] Nêu lý do phải giữ strong reference cho background Task.
- [ ] Chọn được `gather`, `TaskGroup`, `wait`, `as_completed` theo yêu cầu.
- [ ] Nói đúng policy lỗi của `gather` và `TaskGroup`.
- [ ] Giải thích cancellation là request hợp tác.
- [ ] Viết/đọc được `try/finally` cleanup khi cancel.
- [ ] Giải thích vì sao không nuốt `CancelledError`.
- [ ] Phân biệt `timeout`, `wait_for`, `wait` timeout và `shield`.
- [ ] Giải thích timeout có thể không dừng worker thread.
- [ ] Nêu mục đích Lock, Event, Condition, Semaphore, Barrier.
- [ ] Giải thích vì sao async một thread vẫn có race logic.
- [ ] Giải thích Queue maxsize tạo backpressure.
- [ ] Nói đúng `task_done/join`.
- [ ] Giải thích `to_thread` và `run_in_executor`.
- [ ] Chọn ThreadPool cho blocking I/O, ProcessPool cho CPU-bound Python.
- [ ] Giải thích GIL mà không tuyệt đối hóa.
- [ ] Nêu hạn chế pickling, `__main__`, process overhead.
- [ ] Nhận diện deadlock worker chờ Future cùng pool.
- [ ] Đưa ra kế hoạch graceful shutdown.
- [ ] Nêu cách bật debug mode và hai cảnh báo phổ biến.
- [ ] Mô tả test success/failure/timeout/cancel/cleanup.
- [ ] Nêu cách benchmark công bằng bằng `perf_counter` và nhiều lần chạy.
- [ ] Ghi đúng baseline/version cho API đang trình bày.

### 27.2. Checklist đọc mã `[CORE/APPLIED]`

Mỗi người phải nhận diện được trong code:

- [ ] Coroutine bị gọi nhưng không await.
- [ ] Hai việc độc lập đang bị await tuần tự.
- [ ] Blocking call trong coroutine.
- [ ] Unbounded task creation.
- [ ] Exception bị che bởi `return_exceptions=True`.
- [ ] Pending Task từ `wait` bị bỏ quên.
- [ ] Cancellation bị nuốt.
- [ ] Lock thiếu hoặc lock giữ quá lâu.
- [ ] Queue thiếu `task_done()`.
- [ ] Executor submit rồi result ngay.
- [ ] Async Future bị dùng với concurrent wait hoặc ngược lại.
- [ ] ProcessPool dùng callable không picklable/thiếu main guard.
- [ ] Background Task không có owner.
- [ ] Resource không đóng trong đường exception/cancel.
- [ ] Benchmark không công bằng.

### 27.3. Checklist thực hành `[APPLIED]`

Mỗi người phải tự chạy hoặc walkthrough được:

- [ ] Ví dụ tuần tự hai I/O giả lập.
- [ ] Phiên bản concurrent dùng TaskGroup hoặc gather.
- [ ] Một task lỗi để quan sát propagation.
- [ ] Một task bị cancel để quan sát finally.
- [ ] Một operation timeout.
- [ ] Semaphore chứng minh in-flight không vượt giới hạn.
- [ ] Queue producer–consumer có join/shutdown.
- [ ] Blocking function được offload bằng `to_thread`.
- [ ] CPU function so sánh tuần tự/ThreadPool/ProcessPool với kết luận thận trọng.
- [ ] Debug mode phát hiện never-awaited hoặc never-retrieved.
- [ ] Unit test async kiểm tra một luồng lỗi/hủy.

---

## 28. Bộ câu hỏi phản biện bắt buộc cho từng thành viên

Mọi thành viên phải trả lời được, không chuyển câu hỏi chỉ vì “đó là phần của bạn khác”.

1. Async, concurrency và parallelism khác nhau ở điểm nào?
2. Vì sao một event loop có thể phục vụ nhiều socket trên một thread?
3. `async def` có bảo đảm hàm không blocking không?
4. Gọi coroutine function trả về gì? Khi nào code bên trong chạy?
5. Tại sao hai câu `await` liên tiếp có thể vẫn tuần tự?
6. Task khác coroutine object như thế nào?
7. Future khác Task như thế nào?
8. `asyncio.Future` khác `concurrent.futures.Future` thế nào?
9. Vì sao `.result()` của concurrent Future có thể block còn của asyncio Future pending lại lỗi?
10. Khi nào dùng `gather`, khi nào dùng `TaskGroup`?
11. Một child trong `gather` lỗi thì sibling có bị hủy không?
12. Một child trong `TaskGroup` lỗi thì chuyện gì xảy ra?
13. `ExceptionGroup` giải quyết vấn đề gì?
14. Cancellation được đưa vào coroutine khi nào?
15. Vì sao phải re-raise `CancelledError`?
16. `wait_for` có bảo đảm trả đúng lúc timeout tuyệt đối không?
17. `wait` timeout khác `wait_for` timeout ra sao?
18. `shield` bảo vệ ai và không bảo vệ ai?
19. Hủy Task đang chờ `to_thread` có giết thread function không?
20. Vì sao async code vẫn có race condition?
21. Lock, Semaphore và Queue khác nhau ở bài toán nào?
22. Semaphore 10 có nghĩa là 10 request/giây không?
23. Backpressure là gì và tại sao async cần nó?
24. Vì sao Queue.join có thể treo dù queue đã rỗng?
25. Khi nào dùng ThreadPool, ProcessPool, asyncio?
26. GIL ảnh hưởng pure-Python CPU-bound thế nào?
27. Tại sao ProcessPool cần pickling và main guard?
28. Deadlock trong ThreadPool một worker xảy ra thế nào?
29. Vì sao không submit trực tiếp `async def` vào Executor?
30. Làm sao tích hợp một thư viện blocking vào app asyncio?
31. Vì sao tạo một triệu Task cùng lúc nguy hiểm?
32. `writer.drain()` có vai trò gì?
33. Tại sao subprocess dùng PIPE nên `communicate()`?
34. Cách phát hiện coroutine never-awaited và task exception never-retrieved?
35. Một benchmark async công bằng cần công bố thông tin gì?
36. Tại sao `asyncio.sleep()` không chứng minh network library là non-blocking?
37. Graceful shutdown gồm các bước nào?
38. API nào trong báo cáo yêu cầu Python 3.11, 3.13 hoặc 3.14?
39. Free-threaded Python có làm kiến thức GIL trở nên vô nghĩa không?
40. Nếu demo nhanh hơn, làm sao chứng minh kết quả đúng chứ không chỉ nhanh?

---

## 29. Tiêu chí tuyên bố “đã nắm A–Z”

Nhóm chỉ đánh dấu hoàn thành Chương 4 khi đáp ứng đồng thời:

### 29.1. Độ phủ

- [ ] Không thiếu mục `[CORE]` trong tài liệu này.
- [ ] Mỗi mục Core có ít nhất một định nghĩa, một sơ đồ/ví dụ và một bẫy.
- [ ] Applied có bằng chứng trong kế hoạch demo/test, không chỉ liệt kê tên API.
- [ ] Advanced được đặt đúng phụ lục, không lấn át mạch cơ bản.

### 29.2. Tính đúng kỹ thuật

- [ ] Không đánh đồng async/concurrency/parallelism.
- [ ] Không nói `await` tự tạo concurrency.
- [ ] Không nói `gather` mặc định cancel sibling khi lỗi.
- [ ] Không nói timeout luôn giết công việc bên ngoài loop.
- [ ] Không nhầm hai Future.
- [ ] Không khuyên ThreadPool cho pure-Python CPU-bound mà không nói GIL.
- [ ] Không dùng API mới mà thiếu nhãn phiên bản.
- [ ] Mọi resource có ownership và cleanup path.

### 29.3. Năng lực nhóm

- [ ] 6/6 người đạt checklist giải thích Core.
- [ ] 6/6 người trả lời ngẫu nhiên ít nhất 8/10 câu phản biện.
- [ ] 6/6 người walkthrough được demo từ input đến output/error/cancel.
- [ ] Mỗi người review chéo ít nhất một phần không thuộc chuyên môn chính.
- [ ] Ít nhất hai người chạy được toàn bộ demo/test từ README sạch.

### 29.4. Bằng chứng thực nghiệm

- [ ] Có baseline tuần tự.
- [ ] Có async bounded hoặc executor tương ứng workload.
- [ ] Kết quả các phiên bản giống nhau về tính đúng.
- [ ] Có metadata môi trường và nhiều lần đo.
- [ ] Có test failure/timeout/cancel/cleanup.
- [ ] Có kết luận giới hạn, không quảng cáo speedup tuyệt đối.

---

## 30. Gợi ý ma trận chuyên sâu cho 6 thành viên

> Đây chỉ là bản đồ chuyên môn để tránh trùng và bỏ sót. **Tất cả vẫn phải học toàn bộ Core.**

| Thành viên | Chuyên sâu chính | Phần Core phải dạy lại cho nhóm | Phản biện chuyên trách |
|---|---|---|---|
| 1 | Nền tảng concurrency/asynchrony, hai trục phân loại, workload, process/thread/coroutine | Timeline, blocking và cây chọn công cụ | “Async có phải parallel không?” |
| 2 | `concurrent.futures`, Future, Executor và ThreadPool | submit/map/wait/shutdown, order/error/deadlock | “GIL và chọn ThreadPool thế nào?” |
| 3 | ProcessPool, GIL, serialization và benchmark | pickling/main guard/IPC/overhead | “CPU-bound và version/platform?” |
| 4 | Event loop, coroutine, Task và orchestration | await/create_task/gather/TaskGroup/wait | “Lỗi một task ảnh hưởng nhóm ra sao?” |
| 5 | Cancellation, error, synchronization, Queue và backpressure | timeout/shield/Lock/Semaphore/test/debug/shutdown | “Dừng đúng và tránh overload thế nào?” |
| 6 | Kiến trúc lai, demo tích hợp, decision tree và liên hệ distributed systems | bridge, correctness, giới hạn suy diễn | “Chọn mô hình và chứng minh quyết định thế nào?” |

Cách học chéo:

- Mỗi chuyên gia viết 10 câu hỏi cho 5 người còn lại.
- Reviewer của phần 1 là người 4; 2 ↔ 5; 3 ↔ 6 để kết nối lý thuyết–thực hành.
- Trước báo cáo, bốc ngẫu nhiên người giải thích slide/đoạn code của người khác.
- Không dùng câu “phần này bạn X làm” khi giáo viên hỏi Core.

---

## 31. Danh mục nguồn chính thức/primary

Chỉ dùng nguồn dưới đây làm chuẩn cho semantics kỹ thuật. Blog/video có thể giúp diễn giải nhưng không được ưu tiên hơn tài liệu chính thức khi có xung đột.

### 31.1. Tổng quan và thuật ngữ

1. Python Concurrent Execution
   https://docs.python.org/3.14/library/concurrency.html
2. Python Glossary — concurrency, coroutine, awaitable, GIL, deadlock
   https://docs.python.org/3/glossary.html
3. `asyncio` overview
   https://docs.python.org/3.14/library/asyncio.html

### 31.2. Coroutine, Task, Future và orchestration

4. Coroutines and Tasks
   https://docs.python.org/3.14/library/asyncio-task.html
5. `asyncio.Future`
   https://docs.python.org/3.14/library/asyncio-future.html
6. Runners (`asyncio.run`, `Runner`, SIGINT)
   https://docs.python.org/3.14/library/asyncio-runner.html
7. Event loop
   https://docs.python.org/3.14/library/asyncio-eventloop.html
8. `asyncio` exception classes
   https://docs.python.org/3.14/library/asyncio-exceptions.html

### 31.3. Đồng bộ, queue và I/O

9. Synchronization primitives
   https://docs.python.org/3.14/library/asyncio-sync.html
10. Async queues
    https://docs.python.org/3.14/library/asyncio-queue.html
11. Streams
    https://docs.python.org/3.14/library/asyncio-stream.html
12. Async subprocesses
    https://docs.python.org/3.14/library/asyncio-subprocess.html
13. Platform support
    https://docs.python.org/3.14/library/asyncio-platforms.html

### 31.4. Executor, thread, process và GIL

14. `concurrent.futures`
    https://docs.python.org/3.14/library/concurrent.futures.html
15. `threading` và GIL/performance
    https://docs.python.org/3.14/library/threading.html
16. `multiprocessing`
    https://docs.python.org/3.14/library/multiprocessing.html
17. Asyncio và free-threaded Python
    https://docs.python.org/3.14/library/asyncio-threading.html
18. Free-threading HOWTO
    https://docs.python.org/3.14/howto/free-threading-python.html

### 31.5. Debug, test và đo lường

19. Developing with asyncio
    https://docs.python.org/3.14/library/asyncio-dev.html
20. Call graph introspection 3.14
    https://docs.python.org/3.14/library/asyncio-graph.html
21. `unittest.IsolatedAsyncioTestCase`
    https://docs.python.org/3.14/library/unittest.html#unittest.IsolatedAsyncioTestCase
22. `unittest.mock.AsyncMock`
    https://docs.python.org/3.14/library/unittest.mock.html#unittest.mock.AsyncMock
23. `time.perf_counter()`
    https://docs.python.org/3.14/library/time.html#time.perf_counter
24. Context variables
    https://docs.python.org/3.14/library/contextvars.html

### 31.6. PEP nền tảng

25. PEP 3148 — futures
    https://peps.python.org/pep-3148/
26. PEP 3156 — asyncio/event-loop model
    https://peps.python.org/pep-3156/
27. PEP 492 — native coroutines, `async`/`await`, `async with`, `async for`
    https://peps.python.org/pep-0492/
28. PEP 525 — asynchronous generators
    https://peps.python.org/pep-0525/
29. PEP 530 — asynchronous comprehensions
    https://peps.python.org/pep-0530/
30. PEP 567 — context variables
    https://peps.python.org/pep-0567/
31. PEP 654 — Exception Groups và `except*`
    https://peps.python.org/pep-0654/
32. PEP 703 — optional GIL/free-threaded CPython
    https://peps.python.org/pep-0703/
33. PEP 734 — multiple interpreters/InterpreterPool context
    https://peps.python.org/pep-0734/

---

## 32. Tóm tắt một trang để tự kiểm tra

Một thành viên thật sự hiểu Chương 4 phải kể được chuỗi sau:

> Chúng ta dùng bất đồng bộ chủ yếu để không lãng phí thread trong lúc chờ I/O. Trong `asyncio`, gọi `async def` tạo coroutine object; event loop chỉ chạy nó khi được await hoặc schedule thành Task. Loop dùng cooperative scheduling: Task nhường ở điểm await, vì vậy blocking sync hoặc CPU dài sẽ chặn cả loop. Nhiều việc độc lập có thể được tổ chức bằng Task/`gather`, nhưng `TaskGroup` cho structured concurrency và fail-fast rõ hơn. Future biểu diễn kết quả tương lai, nhưng `asyncio.Future` khác Future của `concurrent.futures`. Cancellation là yêu cầu hợp tác thông qua `CancelledError`, nên cleanup phải nằm trong `finally`; timeout được xây trên cancellation và không phải nút cưỡng bức dừng mọi worker. Shared state qua các điểm await vẫn có race, nên dùng Lock/primitive đúng; tải phải được giới hạn bằng Semaphore, bounded Queue hoặc buffer để có backpressure. Blocking I/O cũ có thể đưa sang thread; pure-Python CPU-bound thường đưa sang process trên CPython có GIL. Chương trình đúng phải xử lý lỗi, pending task, shutdown và đóng tài nguyên; chương trình tốt còn được benchmark công bằng, test cả failure/cancel và quan sát bằng debug/log/introspection. Mọi API mới phải ghi phiên bản.

Nếu 6/6 thành viên có thể giải thích, minh họa và phản biện toàn bộ đoạn trên cùng các checklist chi tiết, nhóm mới có cơ sở tuyên bố đã nắm phương pháp tính toán bất đồng bộ từ A đến Z.
