# ĐÁNH GIÁ ĐỘ BAO PHỦ NỘI DUNG CHƯƠNG 4

> Tài liệu kiểm định sườn báo cáo **Chương 4 – Phương pháp tính toán bất đồng bộ** trước khi nhóm bắt đầu làm PowerPoint.
>
> Phạm vi đối chiếu: PDF Chương 4 gồm 24 trang và **sườn ban đầu (v1) gồm 42 slide**. Tài liệu này chỉ đánh giá nội dung; không phải kịch bản thuyết trình hay bản thiết kế slide.

## 1. Kết luận ngắn gọn

### 1.1. Sườn hiện tại có bám đúng file Chương 4 không?

**Có, nếu xét ở mức tên chủ đề.** Các khối kiến thức chính trong PDF đều đã có vị trí trong sườn v1 gồm 42 slide:

- Trang 2–8 của PDF được phản ánh trong slide 1–14: tuần tự, đồng thời, song song, bất đồng bộ và các kiến thức nền liên quan.
- Trang 9–15 được phản ánh trong slide 15–21: `concurrent.futures`, `Executor`, `Future`, `ThreadPoolExecutor`, `ProcessPoolExecutor`.
- Trang 16–22 được phản ánh trong slide 22–35: kiến trúc hướng sự kiện, event loop, `asyncio`, coroutine, task, timeout, cancellation và điều phối tài nguyên.
- Trang 23 được phản ánh trong phần checklist và kết luận.
- Slide 36–42 là phần vận dụng qua demo và đo hiệu năng, không trái với nội dung gốc.

Như vậy, **không có khối kiến thức lớn nào của trang 2–23 bị bỏ hoàn toàn**. Tuy nhiên, “có tên trong sườn” không đồng nghĩa với “đã giải thích đủ”. Phần lớn chủ đề hiện mới có điểm đến, chưa có bằng chứng rằng slide sẽ trình bày đủ định nghĩa, cơ chế, mã chạy được, hành vi khi lỗi, giới hạn và cách lựa chọn.

### 1.2. Sườn hiện tại đã đủ để tuyên bố nắm bất đồng bộ từ A đến Z chưa?

**Chưa.** Sườn hiện tại tốt hơn PDF gốc ở chỗ đã thêm blocking/non-blocking, I/O-bound/CPU-bound, GIL, `TaskGroup`, timeout, cancellation, `Semaphore`, `Queue`, backpressure, `to_thread()` và demo. Dù vậy, để đạt mục tiêu “nắm từ A đến Z” trong phạm vi Python tiêu chuẩn, còn phải làm rõ ít nhất các nhóm sau:

1. Ngữ nghĩa chính xác của coroutine function, coroutine object, awaitable, `Task`, `asyncio.Future` và `concurrent.futures.Future`.
2. Vòng đời event loop và task; điều kiện nào làm event loop bị chặn.
3. Hành vi khác nhau của `create_task()`, `gather()`, `wait()`, `as_completed()` và `TaskGroup`.
4. Cơ chế truyền lỗi, `ExceptionGroup`, timeout và cancellation; cleanup đúng cách bằng `try/finally`.
5. Race condition trong chương trình một luồng có coroutine; các primitive đồng bộ ngoài `Semaphore`.
6. Bounded concurrency, backpressure và flow control ở cả mức hàng đợi lẫn luồng dữ liệu.
7. Cầu nối giữa mã blocking, thread, process và event loop.
8. Ràng buộc của process: serialization/pickling, `__main__` guard, startup overhead và nguy cơ deadlock.
9. Debug, test, logging, graceful shutdown và benchmark có kiểm soát.
10. Phạm vi phiên bản Python để tránh trình bày API mới như thể tồn tại ở mọi phiên bản.

Kết luận kiểm định là:

- **Đủ để làm sườn cấp cao:** Có.
- **Đủ để bao phủ các tiêu đề của PDF:** Có.
- **Đủ để bắt đầu viết nội dung chi tiết:** Có, sau khi chốt các bổ sung bắt buộc trong tài liệu này.
- **Đủ để tuyên bố cả 6 người hiểu từ A đến Z:** Chưa.
- **Đủ để làm PowerPoint ngay mà không tiếp tục nghiên cứu:** Chưa.

## 2. Quy ước đánh giá

| Trạng thái | Ý nghĩa |
|---|---|
| **Covered – Đã bao phủ** | Sườn đã có đúng vị trí và hướng triển khai phù hợp; khi làm slide chỉ cần hoàn thiện bằng ví dụ, hình và lời nói. |
| **Partial – Bao phủ một phần** | Đã có tên/chủ đề nhưng thiếu ngữ nghĩa, quan hệ, giới hạn, tình huống lỗi hoặc minh chứng thực hành. |
| **Missing – Đang thiếu** | Chưa thấy vị trí rõ ràng trong sườn v1; phải thêm vào slide chính, phần demo hoặc phụ lục. |
| **N/A** | Trang bìa hoặc trang kết thúc, không chứa kiến thức kỹ thuật mới. |

Lưu ý: trạng thái dưới đây đánh giá **độ sâu cần có để học và giải thích**, không chỉ kiểm tra xem một thuật ngữ đã xuất hiện hay chưa.

## 3. Bản đồ đối chiếu toàn bộ 24 trang PDF

| Trang PDF | Nội dung nguồn | Vị trí trong sườn v1 | Trạng thái | Điểm đã có | Thiếu, dễ sai hoặc cần làm rõ | Đề xuất bắt buộc |
|---:|---|---|---|---|---|---|
| 1 | Trang mở đầu/tiêu đề Chương 4 | Slide 1 | N/A | Có phần mở đầu chương. | Không phải nội dung kỹ thuật. | Ghi rõ mục tiêu đầu ra: hiểu khái niệm, chọn đúng mô hình, viết được chương trình và giải thích được demo. |
| 2 | Tính toán tuần tự | Slide 1–2 | Covered | Có khái niệm tuần tự và vai trò làm baseline. | Dễ đồng nhất sai “tuần tự” với “đồng bộ”. Một chương trình đồng bộ có thể dùng nhiều thread; một luồng xử lý cũng có thể điều phối nhiều tác vụ bất đồng bộ. | Dùng timeline minh họa A xong mới đến B; thêm câu chốt: sequential mô tả thứ tự thực thi, synchronous mô tả quan hệ chờ kết quả. |
| 3 | Tính toán đồng thời – khái niệm | Slide 2–3; liên hệ slide 8–14 | Partial | Đã có concurrency và so sánh với tuần tự. | Có nguy cơ dùng “đồng thời” như đồng nghĩa với “cùng một thời điểm”. Concurrency là nhiều tác vụ cùng tiến triển trong một khoảng thời gian; không bắt buộc chạy vật lý cùng lúc. | Thêm timeline interleaving trên một core và định nghĩa “in progress together”. |
| 4 | Tính toán đồng thời – cơ chế/đặc điểm | Slide 3–4; slide 8–14 | Partial | Có process, thread, coroutine và kiến thức nền. | Ba đối tượng này không cùng tầng trừu tượng: process/thread là đơn vị thực thi do hệ điều hành quản lý; coroutine là phép tính có thể tạm dừng và thường được event loop điều phối. Chưa thấy race condition và context switching được đặt đúng chỗ. | Thêm bảng tầng trừu tượng, chi phí chuyển ngữ cảnh, chia sẻ bộ nhớ và nguy cơ race. |
| 5 | Tính toán song song – khái niệm | Slide 4–5; liên hệ slide 19–21 và 40 | Partial | Có parallelism và liên hệ CPU-bound. | Dễ nói sai rằng nhiều thread Python luôn chạy CPU song song hoặc rằng async tự tạo song song. | Nêu điều kiện có nhiều đơn vị xử lý vật lý; nối với `ProcessPoolExecutor`; tách rõ concurrency và parallelism. |
| 6 | Tính toán song song – đặc điểm/so sánh | Slide 5–6; slide 8–14 | Partial | Có GIL, process và CPU-bound. | GIL không phải lý do duy nhất để chọn process; còn có serialization, IPC, bộ nhớ, startup overhead. “ThreadPool cho I/O, ProcessPool cho CPU” chỉ là heuristic, không phải định luật tuyệt đối. | Thêm bảng chi phí/lợi ích và một benchmark CPU có cả baseline tuần tự lẫn ProcessPool. |
| 7 | Tính toán bất đồng bộ – khái niệm | Slide 6–7; slide 8–14 | Partial | Có async và blocking/non-blocking. | Asynchrony, non-blocking và concurrency là các khái niệm liên quan nhưng không đồng nghĩa. Async không làm CPU-bound tự chạy nhanh hơn. | Dùng ma trận hai trục sync/async và blocking/non-blocking; đưa ví dụ hoạt động async vẫn có đoạn blocking sai. |
| 8 | Tính toán bất đồng bộ – cách hoạt động/đặc điểm | Slide 7; slide 22–28 | Partial | Có chuyển tiếp sang event loop/coroutine. | Chưa chắc đã giải thích được “trả quyền điều khiển ở đâu”, ai đánh thức tác vụ và vì sao `await` không đồng nghĩa luôn nhường quyền. | Thêm timeline event loop: task chạy → gặp await chưa sẵn sàng → đăng ký chờ → task khác chạy → sự kiện hoàn tất → task vào ready queue. |
| 9 | Giới thiệu `concurrent.futures` | Slide 15 | Covered | Có module và mục tiêu trừu tượng hóa thread/process. | PDF có thể ghi `concurrent.future`; tên module chuẩn là `concurrent.futures` với chữ **s**. Cần tránh xem đây là chính `asyncio`. | Sửa thuật ngữ ở mọi tài liệu; giải thích đây là API Future/Executor cấp cao cho thread/process. |
| 10 | `concurrent.futures` dựa trên threading và multiprocessing | Slide 15; slide 19–21 | Partial | Có hai executor và tiêu chí I/O/CPU. | Chưa làm rõ Future ở đây khác `asyncio.Future`; thread chia sẻ bộ nhớ còn process có không gian nhớ riêng và trao đổi dữ liệu qua serialization/IPC. | Thêm sơ đồ cùng interface `Executor` nhưng hai backend khác nhau; một bảng so sánh Future của hai hệ sinh thái. |
| 11 | `Executor`: `submit`, `map`, `shutdown`; `ThreadPoolExecutor`; `ProcessPoolExecutor` | Slide 16, 18–20 | Partial | Các API và hai lớp executor đã có vị trí. | Slide 18 dễ quá tải. Cần ngữ nghĩa: `submit()` trả Future; `map()` trả kết quả theo thứ tự input dù tác vụ có thể hoàn tất khác thứ tự; `shutdown(wait, cancel_futures)`; context manager. | Tách bảng API và code tối thiểu; bắt buộc có `with Executor(...) as executor:`; giải thích thứ tự kết quả và vòng đời tài nguyên. |
| 12 | `Future`: `cancel`, `cancelled`, `running`, `done`, `result`, `exception`, `add_done_callback` | Slide 17–18 | Partial | Có Future lifecycle và API cơ bản. | Chưa thấy state machine đầy đủ; `cancel()` chỉ thành công khi công việc chưa chạy; `result()` có thể chặn và phát lại exception; callback chạy trong ngữ cảnh liên quan đến executor chứ không phải coroutine của event loop. | Vẽ state machine pending → running → finished/cancelled; thêm ví dụ thành công, lỗi, timeout và cancel thất bại. |
| 13 | Pool worker và cơ chế tái sử dụng worker | Slide 19–20 | Partial | Có ThreadPool/ProcessPool. | Nếu chỉ nói “pool nhanh hơn vì tái sử dụng” thì chưa đủ; cần phân biệt queue công việc, worker, scheduling và giới hạn số worker. | Thêm sơ đồ producer → work queue → N workers → futures; giải thích không tạo một thread/process mới cho mỗi tác vụ. |
| 14 | Pool, chi phí tạo worker và độ trễ | Slide 19–21; slide 39–40 | Partial | Có benchmark và so sánh latency. | Có nguy cơ đưa hệ số nhanh hơn cố định. Kết quả phụ thuộc máy, OS, Python, số tác vụ, kích thước công việc, mạng/đĩa và cấu hình pool. | Mọi kết quả phải sinh từ lần chạy thật; công bố môi trường, số lần lặp, median và cùng một workload/seed. |
| 15 | Tiếp tục pool: lựa chọn/hiệu quả/giới hạn | Slide 20–21 | Partial | Có tiêu chí ThreadPool so với ProcessPool. | Chưa thấy yêu cầu picklable, `if __name__ == "__main__":`, process start method, IPC overhead và deadlock khi worker chờ Future khác trong pool thiếu worker. | Thêm hộp “các lỗi hay gặp” và code an toàn tối thiểu cho ProcessPool. |
| 16 | Event source, event handler, event loop | Slide 22 | Partial | Có event loop. | Outline chỉ nêu event loop nên event source và handler có nguy cơ bị lướt qua. Nếu thiếu hai thành phần này thì chưa bám hết nội dung trực tiếp của PDF. | Slide event-driven phải chỉ rõ nguồn sự kiện, nơi đăng ký chờ, hàng đợi ready, handler/callback/coroutine và vòng lặp dispatch. |
| 17 | Event loop: queue và dispatch sự kiện | Slide 22–23 | Partial | Có thể được giải thích trong event loop/coroutine. | Chưa thấy lifecycle và nguyên tắc cooperative scheduling. Event loop không “chạy mọi task cùng một lúc”; mỗi thread event loop chỉ chạy một đoạn Python tại một thời điểm cho đến khi tác vụ nhường quyền. | Bổ sung ready queue, waiting set, selector/proactor ở mức trực quan; minh họa `time.sleep()` chặn loop và `await asyncio.sleep()` không chặn loop. |
| 18 | Tổng quan `asyncio` | Slide 22–23 | Covered | Có module, event loop, coroutine/await. | Cần giới hạn tuyên bố: `asyncio` phù hợp nhất cho high-level structured network/I/O concurrency; không tự biến CPU-bound thành parallel. | Chốt một câu lựa chọn mô hình và đưa mẫu `asyncio.run(main())`. |
| 19 | Các thành phần `asyncio`: event loop, coroutine, Future, Task | Slide 22–25 | Partial | Đã có awaitable/Task/Future. | Đây là vùng dễ nhầm nhất. Coroutine function khác coroutine object; coroutine object là awaitable; Task bọc và lên lịch coroutine; `asyncio.Future` là primitive mức thấp đại diện kết quả sẽ có. | Thêm sơ đồ quan hệ kiểu và bảng so sánh `Task`, `asyncio.Future`, `concurrent.futures.Future`; không khuyến khích người dùng thường tự tạo `asyncio.Future`. |
| 20 | Coroutine | Slide 23–24 | Partial | Có `async def` và `await`. | Gọi hàm `async def` không chạy thân hàm mà tạo coroutine object. `await` một coroutine trực tiếp thường làm luồng logic tuần tự; muốn overlap phải schedule task hoặc dùng cấu trúc đồng thời. | Có code “sai kỳ vọng” và “đúng”: hai `await` nối tiếp so với `create_task()`/`TaskGroup`. |
| 21 | Thực hiện nhiều tác vụ đồng thời bằng coroutine/task | Slide 24–27 | Partial | Có `create_task`, `gather`, `TaskGroup`. | Chưa đủ nếu không so sánh semantics lỗi và hủy. `gather()` khi propagate exception đầu tiên không mặc định hủy mọi sibling đang chạy; `TaskGroup` hủy phần còn lại khi một task lỗi không phải cancellation. | Dùng một bảng tình huống: tất cả thành công, một task lỗi, caller bị hủy, child bị hủy. |
| 22 | Tiếp tục coroutine và nhiều tác vụ | Slide 25–35 | Partial | Có timeout, cancellation, semaphore, queue và backpressure. | Quá nhiều chủ đề nâng cao dồn vào 7 slide. Dễ chỉ liệt kê API mà không giải thích cancellation là yêu cầu được đưa vào task tại điểm await; cleanup; race condition; bounded queue. | Mỗi chủ đề core phải có ít nhất một tình huống và một đoạn code nhỏ; phần ít dùng chuyển sang phụ lục thay vì nhồi chữ. |
| 23 | Tổng kết chương | Slide 35 và 42 | Covered ở mức sườn | Có checklist và kết luận. | Checklist slide 35 và kết luận slide 42 có thể trùng. Tổng kết không nên chỉ nhắc lại định nghĩa; phải giúp chọn công cụ. | Gộp thành decision tree: loại workload → yêu cầu overlap/parallel → ThreadPool/ProcessPool/asyncio → cơ chế giới hạn và xử lý lỗi. Slide 42 dùng để kết luận từ số liệu demo. |
| 24 | Trang kết thúc; không có chủ đề kỹ thuật mới trong bản trích nội dung | Slide 42/không cần ánh xạ | N/A | Không có kiến thức nguồn cần bổ sung. | Cần kiểm tra trực quan lần cuối khi làm slide để bảo đảm không bỏ sót ghi chú/tài liệu tham khảo nếu trang 24 chứa chúng. | Nếu là trang tài liệu tham khảo, chuyển nguồn trích dẫn vào README và slide References; nếu chỉ là trang kết thúc thì không cần nội dung. |

### 3.1. Tổng hợp kết quả mapping

- **Không có trang kỹ thuật nào bị mất hoàn toàn ở mức chủ đề.**
- Các trang 2, 9, 18 và 23 có hướng triển khai tương đối rõ.
- Các trang 3–8, 10–17 và 19–22 mới ở trạng thái **Partial**, chủ yếu do thiếu ngữ nghĩa và mối quan hệ giữa các khái niệm.
- Điểm rủi ro cao nhất là trang 12, 16–17 và 19–22: Future lifecycle, event-driven architecture, event loop, coroutine, Task/Future và điều phối nhiều tác vụ.

## 4. Đánh giá sáu cụm của sườn v1 gồm 42 slide

| Cụm slide | Chủ đề hiện tại | Mức độ | Điểm mạnh | Rủi ro/trùng lặp | Hành động đề xuất |
|---|---|---|---|---|---|
| 1–7 | Tuần tự, đồng thời, song song, bất đồng bộ | Partial → gần Covered | Bám trực tiếp trang 2–8; có tuyến kể chuyện từ cách làm đơn giản đến async. | Nếu mỗi khái niệm đều có định nghĩa và so sánh riêng, nội dung dễ lặp lại ở slide 8–14. | Cụm này chỉ trả lời “là gì” và dùng timeline; chuyển “hoạt động bằng gì/chọn khi nào” sang cụm 8–14. |
| 8–14 | Hai trục sync–async và blocking–non-blocking; I/O/CPU; process/thread/coroutine; GIL | Partial | Bổ sung nền tảng mà PDF nói quá ngắn; cần thiết để không học thuộc máy móc. | Có nguy cơ đặt process/thread/coroutine cùng cấp; lặp concurrency/parallelism/async; phát biểu GIL tuyệt đối. | Dùng một concept map thống nhất; chỉ một slide GIL có chú thích phiên bản; kết thúc bằng decision table. |
| 15–21 | `concurrent.futures`, Executor, Future lifecycle, `submit/map/wait/as_completed`, ThreadPool, ProcessPool | Partial | Phủ toàn bộ trang 9–15 và đã đi xa hơn PDF với `wait/as_completed`. | Slide API dễ thành danh sách hàm; Future dễ bị lẫn với `asyncio.Future`; thiếu context manager, exception, deadlock và process constraints. | Mỗi API phải đi cùng semantics và một ví dụ; có state machine; có bảng Thread/Process; có một anti-pattern deadlock. |
| 22–28 | Event loop, coroutine/await, awaitable/Task/Future, `create_task/gather`, `TaskGroup` | Partial | Đúng trọng tâm trang 16–22; có structured concurrency hiện đại. | Có thể bỏ mờ event source/handler/queue; chưa đủ chỗ cho lifecycle, scheduling và semantics lỗi/hủy. | Bắt buộc có sơ đồ event loop, sơ đồ type relationship và bảng `gather`–`TaskGroup`; nội dung chi tiết chuyển một phần sang phụ lục. |
| 29–35 | Timeout, cancellation, Semaphore, Queue/backpressure, `to_thread`, lỗi/checklist | Partial | Đây là phần biến kiến thức “biết cú pháp” thành “viết chương trình an toàn”. | Quá dày; mới có Semaphore mà chưa thấy các primitive khác; `to_thread` chưa đủ cho toàn bộ bridge; lỗi/cancellation dễ bị nói sai. | Giữ timeout, cancellation, bounded concurrency, queue và bridge trong slide chính; đưa primitive/bridge ít dùng vào phụ lục nhưng tài liệu nhóm vẫn phải học. |
| 36–42 | Demo, kiến trúc, sequential vs ThreadPool vs asyncio, benchmark, CPU, kết luận | Partial | Có bài toán thực tế để nối toàn chương; có baseline và đo lường. | Nếu CPU chỉ được nói mà không có ProcessPool thì không chứng minh được phần song song; demo có thể không thực sự dùng timeout/backpressure/cancellation; benchmark dễ thiếu công bằng. | Demo phải có cùng workload, lỗi giả lập, timeout, giới hạn concurrency, queue hữu hạn, ProcessPool cho một bước CPU và kết quả đo tái lập được. |

## 5. Những điểm sai hoặc dễ nói sai phải sửa trước khi làm slide

### 5.1. Thuật ngữ và mô hình

1. Tên module chuẩn là **`concurrent.futures`**, không phải `concurrent.future`.
2. **Sequential không đồng nghĩa synchronous.** Sequential nói về thứ tự thực thi; synchronous nói caller có chờ hoàn tất hay không.
3. **Asynchronous không đồng nghĩa non-blocking.** Một API có thể khởi động thao tác async nhưng code vẫn chặn sai ở bước khác.
4. **Concurrency không đồng nghĩa parallelism.** Concurrency là nhiều tác vụ cùng tiến triển; parallelism là thực thi vật lý đồng thời.
5. **`asyncio` không tự tạo CPU parallelism.** Nếu đặt phép tính CPU dài trực tiếp trong coroutine, event loop sẽ bị chặn.
6. **Process, thread và coroutine không phải ba biến thể ngang hàng.** Chúng thuộc các tầng quản lý và có mô hình bộ nhớ/lập lịch khác nhau.
7. Không nói “async luôn nhanh hơn”. Async cải thiện utilization/throughput/latency trong workload phù hợp nhưng có overhead và không làm công việc đơn lẻ tự ngắn đi.

### 5.2. Coroutine, Task và Future

1. Gọi một hàm `async def` chỉ tạo coroutine object; thân hàm chưa chạy ngay.
2. `await` không mặc định tạo concurrency. Hai `await` nối tiếp vẫn là logic tuần tự.
3. `create_task()` schedule coroutine chạy đồng thời theo kiểu cooperative; cần giữ reference phù hợp và await/thu kết quả để không mất exception.
4. `asyncio.Task` là một dạng `asyncio.Future` chuyên dùng để chạy coroutine; `concurrent.futures.Future` là kiểu khác.
5. `Future.result()` của `concurrent.futures` có thể block thread gọi; trong async code không được dùng nó bừa bãi trên event-loop thread.

### 5.3. Lỗi, hủy và timeout

1. Cancellation là một **yêu cầu**, thường được đưa vào task tại một điểm `await`; không nên mô tả như “dừng tức thì ở mọi dòng”.
2. `asyncio.CancelledError` là con của `BaseException`; cleanup bằng `try/finally` và thường phải truyền cancellation tiếp, không nuốt tùy tiện.
3. `asyncio.gather()` và `TaskGroup` không có cùng failure semantics.
4. `asyncio.wait()` hết timeout không tự raise `TimeoutError` và không tự hủy các task chưa xong.
5. `wait_for()` có thể vượt mốc timeout danh nghĩa vì còn chờ tác vụ bị hủy hoàn tất cleanup.
6. `shield()` bảo vệ awaitable con khỏi cancellation của caller trong một số tình huống, nhưng caller vẫn nhận cancellation; không được mô tả là “tắt hủy hoàn toàn”.
7. Với `TaskGroup`, nhiều lỗi có thể được tổng hợp trong `ExceptionGroup`; cần biết `except*` ở mức đọc hiểu.

### 5.4. Thread, process và GIL

1. ThreadPool thường hợp I/O-bound; ProcessPool thường hợp pure-Python CPU-bound, nhưng phải đo trên workload thật.
2. ProcessPool yêu cầu dữ liệu/hàm có thể serialize theo cơ chế multiprocessing; lambda, closure hoặc object phức tạp có thể không dùng được như mong đợi.
3. Trên Windows và các bối cảnh spawn, phải có `if __name__ == "__main__":` cho entry point phù hợp.
4. Process có startup và IPC overhead; task quá nhỏ có thể chậm hơn tuần tự.
5. Không phát biểu “Python chỉ chạy được một thread” một cách tuyệt đối. Cần nói rõ GIL của bản CPython thông thường, extension có thể nhả GIL và free-threaded build là cấu hình tùy chọn ở các phiên bản mới.
6. Không hard-code số worker mặc định như một hằng số chung cho mọi Python; mặc định thay đổi theo phiên bản.

## 6. Nội dung ngoài PDF cần bổ sung để đạt phạm vi A–Z

“A–Z” cần được giới hạn là: **nắm vững phương pháp tính toán bất đồng bộ trong Python chuẩn, biết phối hợp với thread/process và vận dụng an toàn vào một bài toán I/O nhỏ**. Nó không có nghĩa phải trình bày toàn bộ framework web, networking protocol, MPI, hệ phân tán hay mọi API nội bộ của event loop.

### 6.1. Ma trận nội dung mở rộng

| Chủ đề | Hiện trạng sườn | Mức ưu tiên | Nội dung tối thiểu phải đạt | Nơi phù hợp |
|---|---|---|---|---|
| Sync/async, blocking/non-blocking | Covered ở mức tên | **Core** | Ma trận hai trục, ví dụ đúng/sai, không dùng bốn từ thay thế nhau. | Slide chính 8–10. |
| I/O-bound và CPU-bound | Covered ở mức tên | **Core** | Dấu hiệu nhận biết, công cụ phù hợp, chi phí và lý do. | Slide chính 10–14. |
| Process/thread/coroutine | Partial | **Core** | Scheduler, memory sharing, switching point, overhead, failure boundary. | Slide chính + bảng phụ lục. |
| Cooperative scheduling | Missing/ẩn trong event loop | **Core** | Một coroutine chạy đến khi await/yield/block; blocking call đóng băng loop. | Slide event loop. |
| Coroutine function/object/awaitable | Partial | **Core** | Phân biệt kiểu, thời điểm chạy, kết quả và lỗi never-awaited. | Slide 23–24. |
| Event-loop lifecycle | Missing | **Core** | `asyncio.run()`, tạo/chạy/đóng loop ở mức high-level, một running loop trên mỗi thread, monotonic clock. | Slide 22 hoặc phụ lục bắt buộc. |
| Event source/handler/ready queue | Partial | **Core** | Chu trình đăng ký chờ → readiness → ready queue → dispatch. | Slide 22. |
| Executor lifecycle | Partial | **Core** | `submit`, `map`, context manager, shutdown, ownership tài nguyên. | Slide 15–18. |
| `concurrent.futures.Future` state machine | Partial | **Core** | pending/running/done/cancelled, result/exception/callback/timeout. | Slide 17. |
| `wait` và `as_completed` của futures | Covered ở mức tên | **Applied** | Kết quả theo completion order, done/not_done, timeout behavior. | Slide 18 + code demo. |
| ThreadPool giới hạn/deadlock | Missing | **Core** | Worker starvation, task chờ task cùng pool, shared-state race. | Slide 19 + anti-pattern. |
| ProcessPool constraints | Missing | **Core** | Pickling, main guard, startup/IPC, chunk size ở mức khái niệm. | Slide 20. |
| `asyncio.Task` và `asyncio.Future` | Partial | **Core** | Quan hệ kiểu và khác biệt với Future của executor. | Slide 24. |
| `create_task` và reference/lifecycle | Partial | **Core** | Schedule, retain/await, exception retrieval, task naming ở mức cơ bản. | Slide 25. |
| `gather`, `wait`, `as_completed` của asyncio | `gather` có; hai API còn lại chưa rõ | **Applied** | Ordering, error, timeout, cancellation, use case. | Bảng phụ lục + một ví dụ. |
| `TaskGroup` và structured concurrency | Covered ở mức tên | **Core** | Parent-child lifetime, sibling cancellation, `ExceptionGroup`. | Slide 26–28. |
| Cancellation cleanup | Partial | **Core** | `CancelledError`, `try/finally`, re-raise, cancellation point. | Slide 29–30. |
| Timeout variants | Partial | **Core/Applied** | `timeout()`, `timeout_at()`, `wait_for()` và khác biệt với `wait()`. | Slide 29 + phụ lục. |
| `shield()` | Missing | **Advanced** | Chính xác điều gì được bảo vệ và điều gì vẫn bị cancel. | Phụ lục. |
| Race condition trong asyncio | Missing | **Core** | Race vẫn xảy ra nếu state bị đọc/sửa qua các điểm await. | Slide lỗi/checklist. |
| Lock/Event/Condition | Missing | **Applied** | Khi dùng, ownership/wait/notify, không dùng blocking lock trong loop. | Phụ lục có code tối thiểu. |
| Semaphore/BoundedSemaphore/Barrier | Chỉ có Semaphore | **Core/Applied** | Bounded concurrency, phát hiện release dư, barrier theo phase. | Slide 31 + phụ lục. |
| Queue/PriorityQueue/LifoQueue | Chỉ có Queue | **Core/Advanced** | `maxsize`, put/get, `task_done/join`, backpressure; các biến thể là phụ lục. | Slide 32 + phụ lục. |
| Stream flow control | Missing | **Applied** | `read`, `write`, `drain`, `close`, `wait_closed`; vì sao `drain` liên quan backpressure. | Phụ lục hoặc demo nếu dùng network. |
| Async context manager | Missing | **Applied** | `async with`, quản lý tài nguyên, cleanup khi exception/cancel. | Phụ lục + dùng trong demo nếu phù hợp. |
| Async iterator/generator | Missing | **Applied** | `async for`, stream kết quả, cleanup/aclose ở mức nhận biết. | Phụ lục. |
| Bridge blocking code | Có `to_thread` | **Core** | `to_thread` cho blocking I/O; `run_in_executor` cho executor tùy chọn; không đẩy CPU nặng vào default thread pool rồi gọi đó là parallel. | Slide 33. |
| Cross-thread bridge | Missing | **Advanced** | `run_coroutine_threadsafe`, `call_soon_threadsafe`, giới hạn thread-safety. | Phụ lục. |
| `contextvars` | Missing | **Advanced** | Context theo tác vụ cho request ID/logging; tránh global mutable state. | Phụ lục. |
| Bounded concurrency/backpressure | Covered ở mức tên | **Core** | Semaphore giới hạn in-flight, Queue hữu hạn giới hạn backlog, stream `drain` giới hạn buffer. | Slide 31–32 + demo. |
| Fairness/starvation/deadlock/livelock | Missing | **Applied** | Ví dụ nhận biết và nguyên tắc tránh; không hứa fairness tuyệt đối nếu API không bảo đảm. | Slide lỗi + phụ lục. |
| Debug mode và task introspection | Missing | **Applied** | `PYTHONASYNCIODEBUG`, slow callbacks, never-awaited, never-retrieved exception, task name/list/stack ở mức cơ bản. | Phụ lục thực hành. |
| Testing async | Missing | **Applied** | Test success/error/timeout/cancel; không dựa hoàn toàn vào sleep ngẫu nhiên; `IsolatedAsyncioTestCase` hoặc công cụ nhóm chọn. | Repo demo và README. |
| Graceful shutdown | Missing | **Applied** | Ngừng nhận việc, cancel/await task, drain/close resource, không để warning pending task. | Demo + phụ lục. |
| Signal handling | Missing | **Advanced** | Khác biệt platform/main thread; không cần trình bày sâu trên slide chính. | Phụ lục. |
| Retry/backoff/idempotency | Missing | **Applied ở mức ứng dụng** | Retry không phải bản chất của asyncio; chỉ thêm khi demo mô phỏng lỗi; phải tránh nhân đôi side effect. | Demo/README, không biến thành trọng tâm chương. |
| Version matrix | Missing | **Core cho tính chính xác** | Chốt Python mục tiêu; đánh dấu API theo phiên bản, không trộn tính năng 3.11–3.14 như cùng tồn tại khắp nơi. | README + phụ lục References. |
| Benchmark có kiểm soát | Partial | **Applied** | `perf_counter`, cùng workload, seed, concurrency, warm-up/repeat, median, môi trường, không hard-code tốc độ. | Slide 39–40 + script demo. |

## 7. Phân tầng nội dung: Core, Applied và Advanced

Không nên đưa toàn bộ kiến thức A–Z lên 42 slide chính của bản v1. Cách đúng là giữ một **lõi bắt buộc**, chứng minh bằng **phần vận dụng**, và đặt chi tiết ít dùng vào **phụ lục/tài liệu học**. Cả 6 thành viên vẫn phải đọc đủ ba tầng; khác biệt chỉ là lượng thời gian trình bày trước lớp.

### 7.1. Tầng Core – bắt buộc có trong slide chính và mọi thành viên phải trả lời được

1. Sequential, synchronous, concurrency, parallelism, asynchronous, blocking và non-blocking.
2. I/O-bound so với CPU-bound; tiêu chí chọn tuần tự, thread, process hoặc asyncio.
3. Process, thread, coroutine; chia sẻ bộ nhớ; GIL có điều kiện và giới hạn.
4. Event-driven architecture: event source, handler, queue, event loop, dispatch.
5. `concurrent.futures`: Executor, Future lifecycle, `submit`, `map`, `shutdown`, ThreadPool và ProcessPool.
6. `asyncio.run`, coroutine function/object, `await`, awaitable, Task và Future.
7. Tạo concurrency đúng bằng task; vì sao nhiều `await` nối tiếp chưa chắc concurrent.
8. `gather` và `TaskGroup`; propagation của exception và cancellation.
9. Timeout/cancellation/cleanup đúng cách.
10. Bounded concurrency bằng semaphore; producer-consumer và backpressure bằng bounded queue.
11. Race condition vẫn có thể xuất hiện trong async; nguyên tắc đồng bộ tài nguyên chia sẻ.
12. Cách đưa blocking I/O ra khỏi event loop; giới hạn của `to_thread`.
13. Các lỗi phổ biến: `time.sleep` trong coroutine, quên await, mất reference/không lấy exception, chặn event loop, dùng sai pool.
14. Một demo có baseline tuần tự, phương án đồng thời, xử lý lỗi/tài nguyên và benchmark minh bạch.

### 7.2. Tầng Applied – phải có trong tài liệu nhóm và xuất hiện trong demo hoặc phụ lục gần

1. `wait`/`as_completed` và xử lý kết quả theo thứ tự hoàn tất.
2. Lock, Event, Condition, BoundedSemaphore; Barrier ở mức nhận biết.
3. `Queue.task_done()`/`join()` và dừng producer-consumer an toàn.
4. `asyncio.timeout`, `timeout_at`, `wait_for`, `wait` và bảng khác biệt.
5. `ExceptionGroup`/`except*` đủ để đọc lỗi của TaskGroup.
6. `run_in_executor` và nguyên tắc bridge thread/process.
7. Process serialization, main guard, IPC/startup overhead và deadlock pattern.
8. Async context manager/iterator ở mức sử dụng.
9. Debug mode, logging theo task, test đường success/error/timeout/cancel.
10. Graceful shutdown và đóng tài nguyên.
11. Benchmark lặp lại được và giải thích kết quả, không chỉ chụp một con số.

### 7.3. Tầng Advanced – tài liệu tham khảo/phụ lục, không cần chiếm thời lượng chính

1. `asyncio.Runner` và vòng đời loop tùy biến.
2. Low-level event-loop APIs, selector/proactor và chính sách event loop theo phiên bản.
3. `shield`, rescheduling timeout và cancellation edge cases.
4. Streams và transport/protocol ở mức sâu.
5. Async generator cleanup/aclose.
6. `contextvars`.
7. Cross-thread scheduling bằng `run_coroutine_threadsafe`/`call_soon_threadsafe`.
8. Signal handling khác nhau giữa platform.
9. Interpreter pool/free-threaded CPython ở mức xu hướng, không dùng làm trọng tâm nếu môi trường demo không hỗ trợ.
10. Các API mới theo Python 3.12–3.14 như eager execution, Queue shutdown, thay đổi `as_completed`, executor buffersize hoặc worker termination; chỉ nêu nếu đã khóa phiên bản và kiểm thử.

## 8. Phần trùng lặp và cách xử lý

### 8.1. Trùng giữa slide 1–7 và 8–14

Các khái niệm concurrency/parallelism/async rất dễ bị định nghĩa hai lần. Cần phân vai:

- Slide 1–7: câu chuyện, định nghĩa, timeline và ví dụ đời thường/kỹ thuật.
- Slide 8–14: cơ chế, hai trục phân loại, loại workload, đơn vị thực thi, GIL và decision table.

Không lặp lại nguyên văn định nghĩa ở cụm thứ hai; dùng lại một bộ thuật ngữ thống nhất.

### 8.2. Trùng từ “Future” ở hai hệ sinh thái

Future xuất hiện ở cả `concurrent.futures` và `asyncio`. Không được dạy như cùng một class. Nên có đúng một slide so sánh trung tâm rồi các phần sau liên kết về slide đó.

### 8.3. Trùng I/O-bound/CPU-bound với phần benchmark

Slide 8–14 giải thích nguyên tắc chọn; slide 36–42 chỉ kiểm chứng nguyên tắc bằng số liệu. Không định nghĩa lại workload trong demo.

### 8.4. Trùng checklist và kết luận

- Slide checklist: lỗi cần tránh và câu hỏi chọn công cụ.
- Slide kết luận: trả lời câu hỏi nghiên cứu bằng kết quả demo và ba thông điệp cần nhớ.

### 8.5. Không nên chia cứng “7 slide/người” nếu làm vỡ mạch kiến thức

Độ khó không tỷ lệ với số slide. Future/cancellation có thể cần nhiều thời gian hơn một slide định nghĩa. Nên cân bằng theo **thời lượng nói, sản phẩm và trách nhiệm kiểm chứng**, không chỉ số slide. Mỗi nội dung có một người chịu trách nhiệm chính và ít nhất một người review chéo; mọi người vẫn học toàn bộ Core.

## 9. Tiêu chí để được phép nói nội dung đã “đủ”

Chỉ được đánh dấu hoàn thành Chương 4 khi đồng thời vượt qua tất cả cổng dưới đây.

### 9.1. Cổng 1 – Traceability với PDF

- [ ] Mỗi trang kỹ thuật 2–23 có ít nhất một slide/section ID cụ thể.
- [ ] Event source, event handler, event queue và event loop của trang 16–17 đều xuất hiện rõ, không chỉ có chữ “event loop”.
- [ ] Tất cả API Future ở trang 12 được giải thích bằng state/lifecycle, không chỉ liệt kê.
- [ ] Trang 20–22 có ví dụ chứng minh khác nhau giữa await tuần tự và task concurrent.
- [ ] Mọi thuật ngữ sai trong nguồn, đặc biệt `concurrent.future`, được sửa và có ghi chú lịch sự.

### 9.2. Cổng 2 – Đúng về ngữ nghĩa

- [ ] Không đồng nhất concurrency, parallelism và asynchrony.
- [ ] Không đồng nhất async với non-blocking.
- [ ] Không tuyên bố asyncio làm CPU-bound chạy song song.
- [ ] Phân biệt được coroutine function, coroutine object, Task và hai loại Future.
- [ ] Trình bày đúng failure/cancellation semantics của `gather`, `TaskGroup`, `wait` và timeout.
- [ ] Mọi khẳng định về GIL, default worker và API mới đều gắn với phiên bản/môi trường.

### 9.3. Cổng 3 – Từ định nghĩa đến vận dụng

Mỗi chủ đề Core phải có đủ năm lớp:

1. **Định nghĩa:** nó là gì.
2. **Cơ chế:** nó vận hành thế nào.
3. **Ví dụ:** đoạn code/timeline/sơ đồ nhỏ.
4. **Giới hạn:** khi nào sai hoặc không có lợi.
5. **Quyết định:** khi nào nên/không nên dùng.

Nếu một slide chỉ có định nghĩa hoặc danh sách API thì chủ đề đó vẫn là **Partial**.

### 9.4. Cổng 4 – Code và demo

- [ ] Tất cả code trong slide được lấy từ file chạy được hoặc được kiểm thử cú pháp.
- [ ] Demo có cùng một workload cho baseline tuần tự, ThreadPool và asyncio.
- [ ] Nếu kết luận về CPU parallelism, demo phải có ProcessPool hoặc bỏ kết luận đó.
- [ ] Demo cho thấy ít nhất một timeout, một lỗi tác vụ, cancellation/cleanup, giới hạn concurrency và bounded queue/backpressure.
- [ ] Demo ghi rõ đây là mô phỏng một máy nếu không thật sự chạy trên nhiều máy; không gọi nó là hệ phân tán.
- [ ] Benchmark dùng `perf_counter`, cùng input/seed, số lần lặp hợp lý và báo median/phân tán cơ bản.
- [ ] README ghi Python version, OS, lệnh chạy, kết quả kỳ vọng và giới hạn phép đo.
- [ ] Có test cho success, failure, timeout và cancellation; chương trình đóng sạch task/executor/resource.

### 9.5. Cổng 5 – Mức hiểu của cả 6 thành viên

- [ ] Mỗi thành viên có một mảng chuyên sâu chính và một mảng review chéo ngoài phần của mình.
- [ ] Cả 6 người đều tự vẽ/giải thích được timeline sequential–concurrent–parallel–async.
- [ ] Cả 6 người đều chọn đúng ThreadPool, ProcessPool hoặc asyncio cho một workload mới và nêu trade-off.
- [ ] Cả 6 người đều giải thích được event loop và vì sao `time.sleep()` trong coroutine là lỗi.
- [ ] Cả 6 người đều phân biệt Task, `asyncio.Future` và `concurrent.futures.Future`.
- [ ] Cả 6 người đều giải thích được cancellation, timeout, race condition và backpressure.
- [ ] Bất kỳ thành viên nào cũng chạy được demo, đọc được log và chẩn đoán một lỗi giả lập.
- [ ] Thực hiện ít nhất một buổi hỏi ngẫu nhiên chéo; không chỉ để mỗi người học thuộc 7 slide của mình.

### 9.6. Cổng 6 – Tài liệu và nguồn

- [ ] Có bảng thuật ngữ Việt–Anh thống nhất.
- [ ] Có danh mục nguồn: PDF giảng viên và tài liệu Python chính thức tương ứng với phiên bản mục tiêu.
- [ ] Nội dung lấy ý tưởng từ nguồn được diễn giải lại và trích dẫn; không sao chép nguyên khối slide gốc.
- [ ] Core nằm trong slide chính; Applied nằm trong slide/demo/phụ lục gần; Advanced có tài liệu tra cứu rõ.
- [ ] Không tuyên bố “không thiếu bất kỳ kiến thức nào” theo nghĩa vô hạn; phải công bố ranh giới A–Z đã định nghĩa ở Mục 6.

## 10. Bộ câu hỏi kiểm tra tối thiểu trước ngày báo cáo

Mỗi thành viên phải trả lời trôi chảy, không nhìn slide, ít nhất các câu sau:

1. Sequential, synchronous, concurrent, parallel và asynchronous khác nhau ở trục nào?
2. Một chương trình async có thể vẫn blocking không? Cho ví dụ.
3. Vì sao asyncio hợp nhiều I/O chờ đợi nhưng không tự tăng tốc phép tính CPU dài?
4. Process, thread và coroutine khác nhau về scheduler, memory và switching cost thế nào?
5. Gọi hàm `async def` tạo ra gì, và khi nào thân hàm thật sự chạy?
6. Tại sao hai câu `await` nối tiếp có thể vẫn tuần tự?
7. Event loop làm gì từ lúc socket chưa sẵn sàng đến khi coroutine được chạy tiếp?
8. `Task`, `asyncio.Future` và `concurrent.futures.Future` khác nhau thế nào?
9. `submit()` khác `map()` thế nào về kết quả và thứ tự?
10. Future chuyển qua những state nào; lúc nào `cancel()` thành công?
11. ThreadPool và ProcessPool chọn theo tiêu chí nào; mỗi loại có overhead gì?
12. Tại sao ProcessPool cần pickling và main guard?
13. `gather()` khác `TaskGroup` thế nào khi một child lỗi?
14. Cancellation được phát vào task ở đâu; cleanup phải viết thế nào?
15. `wait()`, `wait_for()` và context manager timeout khác nhau ra sao?
16. Race condition có thể xảy ra trong một event-loop thread không? Vì sao?
17. Semaphore giải quyết giới hạn in-flight; bounded Queue giải quyết backlog/backpressure thế nào?
18. Khi nào dùng `to_thread()`; tại sao không xem nó là lời giải mặc định cho CPU-bound?
19. Một benchmark async công bằng phải kiểm soát những biến nào?
20. Demo của nhóm chứng minh điều gì và **không** chứng minh điều gì?

Nếu một người chỉ nói được phần slide mình phụ trách nhưng không trả lời được bộ câu hỏi chung này thì yêu cầu “cả 6 thành viên nắm rõ từ A đến Z” chưa đạt.

## 11. Quyết định sau kiểm định

Sườn v1 gồm 42 slide được giữ để **truy vết phương án ban đầu**; phương án triển khai mới là 36/48 slide chính và 18 slide phụ lục. Trước khi làm PowerPoint cần:

1. Bổ sung toàn bộ Core còn thiếu hoặc mới ở mức tên.
2. Chuyển các chi tiết Applied/Advanced sang tài liệu dài và phụ lục để tránh slide dày chữ.
3. Thiết kế demo sao cho thực sự kiểm chứng timeout, cancellation, bounded concurrency, backpressure, ThreadPool/ProcessPool/asyncio và benchmark.
4. Chốt một phiên bản Python mục tiêu rồi mới chọn API.
5. Chia trách nhiệm theo chuyên môn chính + review chéo, không biến 6 phần thành 6 “ốc đảo kiến thức”.
6. Chỉ bắt đầu dựng PowerPoint khi các cổng 1–3 có trạng thái đạt; chỉ coi báo cáo hoàn thành khi cả 6 cổng đều đạt.

**Phán quyết cuối cùng:** nội dung v1 **đúng hướng và không lệch Chương 4**, nhưng mới là sườn bao phủ rộng. Nó **chưa đủ sâu để tuyên bố A–Z** cho đến khi hoàn thiện các ngữ nghĩa, giới hạn, tình huống lỗi, thực hành và tiêu chí kiểm chứng nêu trong tài liệu này.
