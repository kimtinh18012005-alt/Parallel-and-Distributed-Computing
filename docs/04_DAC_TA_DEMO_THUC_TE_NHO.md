# ĐẶC TẢ DEMO THỰC TẾ NHỎ CHO CHƯƠNG 4

| Thuộc tính | Giá trị |
|---|---|
| Vai trò | System/demo specification và verification plan |
| Trạng thái | Chờ phê duyệt triển khai |
| Điều kiện triển khai | Khóa phạm vi, Python baseline, interface contract và thời lượng báo cáo |
| Sản phẩm giai đoạn sau | Mã nguồn, test, raw benchmark và runbook |

## 1. Mục tiêu kiểm chứng

**Tên hệ thống:** Trung tâm thu thập và phân tích dữ liệu từ nhiều trạm cảm biến.

**Bài toán quyết định:** lựa chọn giữa tuần tự, thread, process, `asyncio` và mô hình lai cho pipeline có I/O trễ, lỗi, giới hạn đồng thời và bước tính toán CPU.

Demo không nhằm xây một hệ thống IoT hoàn chỉnh. Nó là một “phòng thí nghiệm thu nhỏ” để quan sát đúng những hiện tượng của Chương 4:

- thời gian bị lãng phí khi chờ I/O tuần tự;
- nhiều công việc cùng tiến triển nhưng không nhất thiết chạy song song;
- worker pool và `Future`;
- event loop, coroutine và Task;
- giới hạn concurrency và backpressure;
- timeout, cancellation, retry và cleanup;
- CPU-bound và chi phí ProcessPool;
- kiểm tra tính đúng trước khi so hiệu năng.

## 2. Phạm vi bằng chứng

### 2.1. Kết luận được phép rút ra

1. Khi nhiều thao tác độc lập chủ yếu chờ I/O, phiên bản concurrent có thể giảm tổng thời gian chờ so với tuần tự.
2. ThreadPool có thể bao bọc API I/O blocking mà không cần viết lại toàn bộ sang async.
3. `asyncio` có thể quản lý nhiều I/O in-flight trên một event-loop thread nếu các thao tác thật sự nhường quyền.
4. `time.sleep` hoặc CPU loop dài trong coroutine có thể làm đóng băng event loop.
5. Semaphore giới hạn số thao tác đồng thời; Queue hữu hạn truyền áp lực ngược tới producer.
6. Timeout/cancellation cần cleanup rõ ràng; “hủy” không có nghĩa máy lập tức dừng mọi mã đang chạy.
7. ProcessPool có thể hữu ích cho CPU-bound đủ lớn, nhưng overhead có thể khiến tác vụ nhỏ chậm hơn tuần tự.
8. Kết quả benchmark phụ thuộc cấu hình, dữ liệu, máy và phương pháp đo.

### 2.2. Giới hạn suy diễn

1. Không chứng minh `asyncio` luôn nhanh nhất.
2. Không chứng minh thread luôn là lựa chọn tốt nhất cho mọi I/O.
3. Không chứng minh process luôn tăng tốc mọi phép tính CPU.
4. Không đại diện chính xác cho độ trễ Internet nếu dữ liệu chỉ được mô phỏng bằng sleep.
5. Không biến một chương trình trên một máy thành hệ thống phân tán thực sự.
6. Không đo được khả năng mở rộng sản xuất chỉ từ laptop và vài chục trạm.
7. Không thay thế load test, profiling và kiểm thử tích hợp trong hệ thống thật.

Phần kết luận phải nhắc lại ranh giới này để tránh biến demo giáo dục thành một tuyên bố hiệu năng tuyệt đối.

## 3. Câu chuyện nghiệp vụ

Một trung tâm giám sát cần thu thập dữ liệu từ nhiều trạm:

- mã trạm;
- thời điểm đo;
- nhiệt độ;
- độ ẩm;
- chỉ số bụi hoặc chất lượng không khí;
- trạng thái nguồn;
- độ trễ mô phỏng của kết nối.

Một vòng thu thập gồm:

1. yêu cầu dữ liệu từ N trạm;
2. chờ phản hồi hoặc timeout;
3. kiểm tra dữ liệu hợp lệ;
4. đưa bản ghi hợp lệ vào hàng đợi;
5. tính chỉ số bất thường;
6. tổng hợp cảnh báo;
7. xuất báo cáo và metric.

Từng trạm độc lập ở bước lấy dữ liệu, vì vậy phù hợp để minh họa fan-out/fan-in. Bước tính chỉ số có thể cấu hình nhẹ hoặc nặng, giúp so sánh I/O-bound với CPU-bound trên cùng một câu chuyện.

## 4. Phạm vi tối thiểu và phạm vi mở rộng

### 4.1. Bắt buộc khi cài đặt

- Chạy offline, không cần Internet.
- Có random seed cố định để tái lập.
- Có ít nhất bốn chế độ: `sequential`, `thread`, `async`, `process`.
- Có chế độ `hybrid` nếu thời gian cho phép.
- Cùng input phải có output nghiệp vụ tương đương, trừ lỗi được tiêm có chủ đích.
- Có timeout, giới hạn concurrency và failure injection.
- Có test, log có timestamp và kết quả benchmark dạng JSON/CSV.
- Chạy được trên Windows bằng main guard cho ProcessPool.

### 4.2. Mở rộng nếu nhóm đã hoàn tất Core

- Queue producer–consumer nhiều stage.
- Retry với exponential backoff và jitter có seed.
- Graceful shutdown khi người dùng bấm Ctrl+C.
- `TaskGroup` và `ExceptionGroup` trên Python 3.11+.
- Async generator phát luồng bản ghi.
- Async context manager mô phỏng kết nối.
- Một TCP server cục bộ bằng asyncio streams.

### 4.3. Không làm ở phiên bản nhỏ

- Không cần database thật, cloud, container cluster hoặc message broker.
- Không gọi API chất lượng không khí ngoài Internet trong buổi báo cáo.
- Không xây giao diện web phức tạp.
- Không dùng framework bên thứ ba nếu thư viện chuẩn đã đủ minh họa.
- Không tối ưu vi mô trước khi test tính đúng.

## 5. Ánh xạ demo với bản đồ kiến thức

| Hiện tượng trong demo | Kiến thức quan sát được | Người giải thích chính | Người backup |
|---|---|---:|---:|
| N trạm được gọi nối tiếp | sequential, waiting time, baseline | TV1 | TV4 |
| N lời gọi blocking trong pool | Executor, Future, ThreadPool | TV2 | TV5 |
| Phân tích CPU ở process | ProcessPool, GIL, pickling, overhead | TV3 | TV6 |
| N coroutine đọc trạm | event loop, coroutine, Task | TV4 | TV1 |
| `time.sleep` làm loop đứng | blocking trong async | TV4 | TV1 |
| `TaskGroup` gom task | structured concurrency, lỗi sibling | TV4 | TV5 |
| Semaphore trước lời gọi trạm | bounded concurrency | TV5 | TV2 |
| Queue hữu hạn giữa hai stage | backpressure, producer–consumer | TV5 | TV2 |
| timeout và trạm chậm | deadline, cancellation, cleanup | TV5 | TV2 |
| hybrid async + process | chọn kiến trúc theo workload | TV6 | TV3 |
| bảng kết quả | correctness, latency, throughput | TV6 | TV3 |

Phân công cụ thể cuối cùng phải khớp với `02_PHAN_CONG_6_THANH_VIEN_A_Z.md`; bảng này mô tả ownership theo chủ đề, không giao toàn bộ demo cho một người.

## 6. Mô hình dữ liệu

### 6.1. Cấu hình trạm

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `station_id` | string | định danh ổn định |
| `base_delay_ms` | integer | độ trễ nền mô phỏng |
| `jitter_ms` | integer | dao động độ trễ |
| `failure_probability` | float | xác suất lỗi có seed |
| `malformed_probability` | float | xác suất dữ liệu không hợp lệ |
| `cpu_size` | integer | độ nặng phân tích CPU |

### 6.2. Bản ghi cảm biến

| Trường | Kiểu | Quy tắc |
|---|---|---|
| `station_id` | string | phải tồn tại trong cấu hình |
| `sequence` | integer | tăng theo vòng lấy dữ liệu |
| `observed_at` | ISO datetime | dùng UTC hoặc timezone ghi rõ |
| `temperature_c` | float | kiểm tra miền hợp lệ |
| `humidity_percent` | float | 0–100 |
| `air_quality_index` | integer | không âm |
| `payload_checksum` | string | dùng để kiểm tra tính tương đương nếu cần |

### 6.3. Kết quả một trạm

```text
station_id
status: success | timeout | failed | invalid | cancelled
attempts
elapsed_ms
record hoặc null
error_type hoặc null
error_message hoặc null
```

### 6.4. Báo cáo một lần chạy

```text
run_id
mode
python_version
platform
parameters
seed
started_at
elapsed_ms
success_count
timeout_count
failure_count
cancelled_count
max_in_flight
throughput_items_per_second
result_digest
station_results
```

Không dùng nội dung `error_message` làm oracle vì thông điệp có thể khác phiên bản; dùng loại lỗi, trạng thái và dữ liệu chuẩn hóa.

## 7. Mô phỏng I/O sao cho có ý nghĩa

Mô phỏng nên có hai adapter cùng giao kèo:

1. **Blocking adapter** dùng thao tác chờ đồng bộ để phiên bản tuần tự/ThreadPool gọi.
2. **Async adapter** dùng thao tác chờ bất đồng bộ để event loop có thể làm việc khác.

Cả hai adapter nhận cùng `station_id`, seed và attempt, rồi trả cùng payload hoặc cùng lỗi logic. Như vậy so sánh không bị sai vì mỗi phiên bản thực hiện một bài toán khác.

Độ trễ nên được tính xác định từ `(seed, station_id, attempt)` thay vì gọi random toàn cục không kiểm soát. Khi retry, attempt thay đổi nhưng quy luật vẫn tái lập.

Kịch bản mặc định gợi ý:

- 8 hoặc 12 trạm;
- delay 200–800 ms;
- concurrency limit 3 hoặc 4;
- timeout 600 ms để cố ý có vài timeout;
- failure rate 10%;
- Queue `maxsize` nhỏ hơn số trạm;
- CPU size có hai mức nhỏ/lớn.

Thông số chỉ là điểm bắt đầu; trước báo cáo phải chạy thử trên đúng máy trình chiếu.

## 8. Năm chế độ thực thi

### 8.1. `sequential` — mốc tính đúng và thời gian

Luồng:

```text
for từng trạm
  gọi blocking adapter
  kiểm tra dữ liệu
  phân tích
  lưu kết quả
tổng hợp
```

Điểm phải giải thích:

- CPU phần lớn rảnh khi từng trạm đang chờ;
- lỗi được xử lý từng trạm;
- đơn giản, dễ debug, có thể là lựa chọn đúng khi N nhỏ;
- dùng làm oracle chứ không mặc định gọi là “tệ”.

### 8.2. `thread` — bọc I/O blocking bằng ThreadPool

Luồng:

```text
submit một callable cho mỗi trạm
nhận Future
thu kết quả theo completion order hoặc input order
xử lý lỗi/timeout
shutdown pool
```

Hai biến thể minh họa:

- `executor.map`: kết quả được quan sát theo thứ tự input;
- `submit` + `as_completed`: xử lý trạm hoàn thành trước ngay khi có kết quả.

Điểm phải giải thích:

- số worker là giới hạn tài nguyên, không phải càng nhiều càng tốt;
- callable chia sẻ memory của process nên dữ liệu dùng chung cần thread safety;
- timeout của `future.result` không nhất thiết dừng callable đã running;
- context manager bảo đảm shutdown có cấu trúc.

### 8.3. `async` — concurrent I/O trên event loop

Luồng chuẩn:

```text
asyncio.run(main())
main tạo phạm vi task có cấu trúc
mỗi task lấy Semaphore rồi await adapter
kết quả đi qua Queue hoặc được gom trực tiếp
timeout/cancellation chạy cleanup
tổng hợp sau khi task kết thúc
```

Điểm phải giải thích:

- tạo coroutine object khác tạo Task;
- `await` một coroutine sau một coroutine có thể vẫn tuần tự;
- `create_task`, `TaskGroup` và các API phối hợp có khả năng schedule coroutine như `gather`/`as_completed` có thể làm nhiều công việc cùng tiến triển; hai `await` trực tiếp nối tiếp thì vẫn có thể tuần tự;
- event loop không được gọi `time.sleep` hay tính CPU dài;
- mọi task phải có ownership và kết quả/ngoại lệ phải được quan sát.

### 8.4. `process` — phân tích CPU bằng ProcessPool

Chỉ tách bước CPU đủ lớn sang worker process. Không giả vờ rằng `sleep` là CPU-bound.

Điểm phải giải thích:

- hàm worker đặt ở top level và dữ liệu phải pickle được;
- dùng `if __name__ == "__main__":`;
- truyền dữ liệu qua process có overhead;
- tác vụ nhỏ có thể chậm hơn;
- phép tính và result digest phải giống baseline.

### 8.5. `hybrid` — async I/O kết hợp ProcessPool CPU

Pipeline:

```text
async producers lấy dữ liệu
bounded Queue điều tiết
async coordinator chuyển batch CPU đủ lớn sang ProcessPool
nhận Future qua event loop
aggregate và ghi metric
```

Đây là chế độ tổng hợp, không phải mặc định tốt nhất. Nhóm phải giải thích chi phí tăng độ phức tạp, serialization, shutdown hai loại tài nguyên và luồng cancellation qua ranh giới process.

## 9. Ba sơ đồ bắt buộc phải chuẩn bị

### 9.1. Timeline

Vẽ cùng ba trạm A/B/C cho tuần tự, ThreadPool và asyncio. Màu tách:

- CPU chạy;
- chờ I/O;
- ready nhưng chưa được chạy;
- hoàn thành/lỗi.

Không vẽ các coroutine như ba lõi CPU chạy thật cùng lúc nếu demo chỉ dùng một event-loop thread.

### 9.2. Sơ đồ state/task ownership

```text
main scope
├─ station task A
├─ station task B
├─ station task C
└─ aggregator task
```

Trên mỗi nhánh ghi điều gì xảy ra khi child lỗi, timeout hoặc parent bị cancel. Nếu dùng task “fire-and-forget”, phải có nơi giữ tham chiếu và thu exception.

### 9.3. Pipeline/backpressure

```text
N producers → Semaphore → Queue(maxsize=k) → M consumers → aggregator
```

Minh họa producer phải đợi ở `put` khi queue đầy. Phân biệt rõ:

- Semaphore giới hạn số thao tác trong critical/expensive section;
- Queue hữu hạn giới hạn backlog giữa các stage;
- rate limiter giới hạn số thao tác trong một khoảng thời gian và không tự có chỉ vì dùng Semaphore.

## 10. Failure injection

Mỗi loại lỗi phải bật/tắt được bằng tham số và có kết quả kỳ vọng.

| Mã | Lỗi | Cách tiêm | Điều cần quan sát |
|---|---|---|---|
| F1 | trạm chậm | delay lớn hơn timeout | timeout, cleanup, kết quả partial |
| F2 | kết nối lỗi | raise exception xác định | propagation và status failed |
| F3 | payload hỏng | giá trị ngoài miền | validation, không đưa vào CPU stage |
| F4 | queue đầy | producer nhanh/consumer chậm | producer chờ, backlog bị chặn |
| F5 | worker CPU lỗi | input đặc biệt | Future chứa exception/BrokenPool nếu mô phỏng crash |
| F6 | người dùng hủy | cancel parent giữa pipeline | child cleanup, queue/pool shutdown |
| F7 | blocking trong coroutine | cố ý gọi blocking sleep | heartbeat dừng/callback chậm |
| F8 | race | read–await–write counter | số đếm sai rồi sửa bằng Lock |
| F9 | task bị bỏ quên | tạo task lỗi không await | debug warning/never-retrieved exception |
| F10 | quên `task_done` | consumer bỏ gọi | `join` treo, test timeout phát hiện |

Mỗi lỗi có hai phiên bản: `broken` để dạy và `fixed` để chứng minh cách sửa. Không đưa lỗi cố ý vào đường chạy mặc định mà không gắn nhãn.

## 11. Chính sách timeout, retry và cancellation

### 11.1. Timeout

Phân biệt ba lớp:

- per-attempt timeout: giới hạn một lần gọi trạm;
- per-station deadline: bao gồm mọi lần retry;
- whole-run deadline: ngân sách cả vòng thu thập.

Nhóm phải quyết định khi timeout sẽ:

- trả partial result;
- đánh dấu trạm timeout;
- retry nếu còn ngân sách;
- hay hủy cả scope nếu đây là dữ liệu bắt buộc.

### 11.2. Retry

Chỉ retry lỗi tạm thời đã phân loại. Không retry payload invalid hoặc lỗi lập trình. Cấu hình:

- `max_attempts` nhỏ;
- exponential backoff;
- jitter xác định trong demo;
- deadline tổng;
- metric số attempt.

Giải thích idempotency: nếu thao tác thực tế có side effect, retry có thể tạo bản ghi/đơn hàng trùng. Demo đọc cảm biến gần như read-only nhưng phải nêu giới hạn khi liên hệ hệ thống phân tán.

### 11.3. Cancellation

Khi parent bị hủy:

1. ngừng tạo công việc mới;
2. báo cancellation cho child trong phạm vi;
3. child chạy `finally`/thoát context manager;
4. xử lý item còn trong queue theo chính sách;
5. shutdown executor;
6. ghi báo cáo cancelled;
7. không nuốt `CancelledError` vô điều kiện.

Nếu có ProcessPool task đã chạy, phải nói rõ cancellation Future không bảo đảm dừng ngay mã CPU đang thực thi.

## 12. Oracle tính đúng

Trước benchmark phải định nghĩa “kết quả giống nhau”:

- cùng tập trạm được xem xét;
- cùng payload từ seed;
- cùng validation rules;
- cùng anomaly algorithm;
- cùng status theo fault policy;
- cùng aggregate sau khi chuẩn hóa thứ tự;
- cùng digest của bản ghi thành công.

Do concurrent completion order không ổn định, không so trực tiếp thứ tự danh sách nếu thứ tự không phải yêu cầu nghiệp vụ. Sắp theo `station_id` trước khi tính digest, hoặc so mapping/set phù hợp.

## 13. Kế hoạch kiểm thử

### 13.1. Unit tests

- sinh payload xác định từ seed;
- validation biên;
- anomaly calculation;
- retry classifier;
- backoff calculation;
- result normalization/digest.

### 13.2. Async tests

- coroutine thành công;
- timeout đúng loại trạng thái;
- cancellation chạy cleanup;
- Semaphore không vượt max in-flight;
- Queue `join` kết thúc khi đủ `task_done`;
- không còn pending task sau main;
- TaskGroup xử lý sibling failure theo thiết kế.

### 13.3. Executor tests

- ThreadPool output tương đương baseline;
- exception từ callable xuất hiện khi lấy Future;
- pending Future có thể cancel trong kịch bản kiểm soát;
- ProcessPool worker import/pickle được;
- process output tương đương baseline;
- shutdown không để worker sống ngoài ý muốn.

### 13.4. Integration tests

| Test | Input | Kỳ vọng |
|---|---|---|
| I1 happy path | 8 trạm, không lỗi | mọi mode cùng digest |
| I2 partial failure | 2 trạm lỗi | số success/fail đúng, run vẫn kết thúc |
| I3 timeout | vài delay vượt ngưỡng | đúng trạm timeout, elapsed có giới hạn |
| I4 overload | Queue nhỏ, consumer chậm | max queue không vượt cấu hình |
| I5 cancellation | hủy giữa run | cleanup hoàn tất, không task treo |
| I6 CPU small | phép tính nhẹ | process có thể không nhanh hơn |
| I7 CPU large | phép tính đủ nặng | so speedup có điều kiện |
| I8 deterministic | chạy cùng seed | cùng normalized result |

Test thời gian cần ngưỡng rộng và không dùng equality tuyệt đối vì scheduler/máy khác nhau. Test correctness tách khỏi benchmark.

## 14. Giao thức benchmark

### 14.1. Thông tin môi trường phải lưu

- phiên bản Python đầy đủ;
- hệ điều hành;
- CPU logic/physical nếu lấy được;
- RAM nếu liên quan;
- chế độ nguồn của laptop;
- số worker/concurrency limit;
- seed, số trạm, delay, failure rate, CPU size;
- commit hash.

### 14.2. Quy trình

1. Chạy correctness suite.
2. Warm-up ít nhất một lần nếu có cache/process startup effects.
3. Chạy mỗi cấu hình nhiều lần, thứ tự có thể luân phiên để giảm thiên lệch nhiệt/tải nền.
4. Dùng monotonic high-resolution timer như `perf_counter`.
5. Không tính thời gian tạo dữ liệu vào một mode nhưng lại tính vào mode khác.
6. Lưu raw result từng run; chỉ sau đó tính summary.
7. Báo median và khoảng phân tán; có thể thêm p95 nếu số mẫu đủ.
8. Kiểm tra digest sau mỗi run.
9. Ghi mọi run lỗi; không xóa run xấu mà không giải thích.

### 14.3. Metric

- total elapsed time;
- per-station latency;
- throughput;
- success/timeout/failure/cancel count;
- attempts/retries;
- maximum in-flight;
- maximum queue depth;
- worker count;
- CPU stage time;
- speedup so với baseline;
- efficiency khi phân tích process nếu có ý nghĩa.

### 14.4. Ma trận thí nghiệm tối thiểu

| Thí nghiệm | Biến thay đổi | Điều muốn thấy |
|---|---|---|
| E1 | mode, I/O nhiều | concurrent giảm idle waiting |
| E2 | worker/concurrency 1,2,4,8 | lợi ích bão hòa/overhead |
| E3 | CPU size nhỏ/lớn | ngưỡng ProcessPool hữu ích |
| E4 | Queue maxsize | latency/backlog/backpressure |
| E5 | timeout | trade-off hoàn tất vs thời gian |
| E6 | failure rate | độ bền và chi phí retry |
| E7 | blocking call trong loop | event-loop responsiveness |

## 15. Kịch bản live demo 8–10 phút

### Phút 0–1 — Bài toán và oracle

- Hiện sơ đồ pipeline.
- Cho xem input seed/cấu hình.
- Nêu mọi mode phải cho cùng digest trên happy path.

### Phút 1–2 — Tuần tự

- Chạy 8 trạm.
- Chỉ timeline: từng khoảng chờ nối đuôi.
- Không chê mô hình; nêu nó là baseline đơn giản.

### Phút 2–4 — Thread và asyncio

- Chạy cùng input bằng ThreadPool và asyncio.
- Hiện timestamp/interleaving/max in-flight.
- Phân biệt worker thread với coroutine trên event loop.
- Nếu thời gian cho phép, bật bản `time.sleep` sai để heartbeat dừng.

### Phút 4–6 — Timeout và backpressure

- Bật một trạm chậm và Queue nhỏ.
- Hiện timeout, retry giới hạn, producer chờ ở queue.
- Hủy một run và cho thấy cleanup.

### Phút 6–8 — CPU/process

- So CPU nhỏ: overhead có thể làm process chậm.
- So CPU lớn: process có cơ hội tăng tốc.
- Nhắc main guard/pickling và môi trường máy.

### Phút 8–10 — Kết luận

- Hiện decision table.
- Nêu ba kết luận có điều kiện.
- Nêu hai điều demo không chứng minh.
- Mời giảng viên chọn một fault/mode để nhóm giải thích.

## 16. Phương án dự phòng

Demo trực tiếp có thể thất bại vì Python, quyền process, antivirus hoặc máy chiếu. Chuẩn bị:

- một lệnh smoke test chạy trước giờ học;
- môi trường đã ghim phiên bản;
- raw JSON/CSV của lần chạy hợp lệ;
- ảnh timeline và bảng benchmark;
- video ngắn không phụ thuộc mạng;
- chế độ giảm CPU size để không quá giờ;
- phương án bỏ ProcessPool live nhưng vẫn giải thích bằng dữ liệu đã lưu;
- checksum/commit hash chứng minh dữ liệu dự phòng thuộc bản nào.

Không chỉnh tay số liệu để “đẹp”. Nếu live result khác dữ liệu chuẩn bị, đó là cơ hội giải thích biến thiên benchmark.

## 17. Phân công demo cho sáu người

| Thành viên | Hạng mục cài đặt sau khi sườn được duyệt | Test/đầu ra | Review chéo |
|---|---|---|---|
| TV1 | domain model, deterministic generator, sequential baseline | oracle/digest tests | review async timeline |
| TV2 | blocking adapter, ThreadPool/Future mode | Future error/cancel/order tests | review reliability semantics |
| TV3 | CPU function, ProcessPool mode, raw benchmark protocol | pickle/main-guard/equivalence tests | review hybrid performance claims |
| TV4 | async adapter, event-loop/Task/TaskGroup mode | scheduling/blocking-call tests | review baseline semantics |
| TV5 | timeout, cancellation, Queue, Semaphore, retry và debug | overload/leak/graceful-shutdown tests | review executor lifecycle |
| TV6 | hybrid integration, CLI, result report và runbook | cross-mode equivalence/release tests | review asyncio–process bridge |

TV6 duy trì integration contract và hybrid mode nhưng không viết thay năm module. Mỗi owner phải tự đưa module của mình qua interface chung, sửa lỗi tích hợp thuộc module đó và nộp cùng định mức: 6 test gồm happy path, boundary, failure, timeout/cancellation, resource/cleanup và integration; 1 fault injection; 1 metric; review module của backup pair.

Mọi thành viên phải:

- clone và chạy cả năm mode;
- đọc được cấu hình/output;
- giải thích một trace không thuộc module mình;
- sửa được ít nhất một fault;
- trình bày kết luận benchmark có điều kiện.

Khối lượng demo được tính 15/100 điểm và khoảng 7/48 giờ cho từng người như nhau. Nếu một module vượt định mức vì phát sinh kỹ thuật, tách phần độc lập thành issue chung và giao cho người còn tải; không mặc định dồn cho TV6.

## 18. Cấu trúc thư mục triển khai

```text
demo/
├── README.md
├── pyproject.toml hoặc requirements-dev.txt
├── src/
│   └── sensor_demo/
│       ├── models.py
│       ├── config.py
│       ├── simulator.py
│       ├── sequential_mode.py
│       ├── thread_mode.py
│       ├── async_mode.py
│       ├── process_mode.py
│       ├── hybrid_mode.py
│       ├── resilience.py
│       ├── metrics.py
│       └── cli.py
├── tests/
│   ├── test_correctness.py
│   ├── test_thread_mode.py
│   ├── test_async_mode.py
│   ├── test_process_mode.py
│   └── test_failures.py
└── results/
    ├── raw/
    └── summaries/
```

Tên file có thể thay đổi khi cài đặt; trách nhiệm và test oracle không được mất.

## 19. Cổng phê duyệt triển khai

- [ ] Giảng viên/nhóm chấp nhận bài toán cảm biến.
- [ ] Chốt phiên bản Python mục tiêu.
- [ ] Chốt bốn mode bắt buộc và mode hybrid tùy chọn/bắt buộc.
- [ ] Chốt input schema, result schema và oracle.
- [ ] Chốt fault policy, timeout policy, retry policy.
- [ ] Chốt giới hạn concurrency và Queue.
- [ ] Chốt CPU function không quá chậm trên máy trình chiếu.
- [ ] Chốt metric và benchmark protocol.
- [ ] Chốt ai làm module, ai review.
- [ ] Chốt phương án offline và dữ liệu dự phòng.
- [ ] Không bắt đầu tối ưu khi correctness tests chưa có.

## 20. Tiêu chí hoàn thành demo

Demo chỉ được xem là hoàn tất nếu:

1. Mọi mode bắt buộc chạy cùng input và pass oracle.
2. Các lỗi F1–F10 có test hoặc kịch bản minh họa rõ.
3. Không có unbounded task creation ở đường chạy chuẩn.
4. Event loop không chứa blocking sleep/CPU dài ở bản đúng.
5. Cancellation chạy cleanup và không để pending task ngoài ý muốn.
6. Executor được shutdown rõ ràng.
7. Process mode chạy trên Windows với main guard và dữ liệu pickle được.
8. Queue/Semaphore thực sự đo được max depth/max in-flight.
9. Raw benchmark, cấu hình, môi trường và commit hash được lưu.
10. Kết luận nêu cả lợi ích, overhead và giới hạn suy diễn.
11. Mỗi thành viên giải thích được toàn pipeline và một lỗi ngoài phần mình.
12. Có runbook 8–10 phút và phương án B không phụ thuộc Internet.
