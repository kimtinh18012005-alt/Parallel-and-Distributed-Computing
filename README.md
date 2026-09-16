# Parallel and Distributed Computing

## Chương 4 — Phương pháp tính toán bất đồng bộ trong Python

> **Trạng thái hiện tại:** đang ở giai đoạn kiểm định phạm vi, xây sườn và chia việc. Repository **chưa tạo PPTX/PDF và chưa cài đặt demo**. Nhóm chỉ làm các bước đó sau khi duyệt sườn, thời lượng và phiên bản Python.

Repository này là kế hoạch học–báo cáo Chương 4 cho nhóm **6 thành viên**. Mục tiêu không phải chia sáu đoạn để mỗi người học thuộc phần mình, mà xây một hệ thống trong đó:

- mỗi người là chuyên gia chính của một cụm kiến thức;
- mỗi cụm có một người backup có thể trình bày thay;
- cả sáu người đều phải vượt chuẩn kiến thức chung, quiz, bảo vệ miệng và lab;
- nội dung gốc của giảng viên được bao phủ đầy đủ;
- các khoảng trống thực hành được bổ sung bằng tài liệu Python chính thức;
- demo nhỏ nối lý thuyết với một bài toán có I/O, CPU, lỗi, timeout và quá tải.

## Trả lời thẳng: nội dung cũ đã đủ Chương 4 chưa?

**Đúng chủ đề nhưng chưa đủ A–Z.**

Sườn cũ đã chạm đủ các cụm chính trong PDF 24 trang: tuần tự/đồng thời/song song/bất đồng bộ, `concurrent.futures`, Executor/Future, worker pool, event loop, coroutine, Task và `asyncio`. Vì vậy nó **không lệch Chương 4**.

Tuy nhiên, phần lớn mới ở mức tiêu đề hoặc giới thiệu. Để cả nhóm thật sự nắm phương pháp tính toán bất đồng bộ và bảo vệ được câu hỏi sâu, phải bổ sung:

- semantics chính xác của coroutine, Task và hai loại Future;
- `gather`, `wait`, `as_completed`, `TaskGroup`, `ExceptionGroup` và thứ tự/lỗi/hủy;
- timeout, cancellation, `shield`, cleanup và graceful shutdown;
- race condition, Lock, Event, Condition, Semaphore, BoundedSemaphore, Barrier;
- Queue, producer–consumer, backpressure và giới hạn tải;
- cầu nối giữa async với code blocking, thread và process;
- pickling, main guard, khác biệt hệ điều hành và GIL;
- async iterator/generator/context manager, streams và subprocess ở tầng phù hợp;
- test, debug, logging, task introspection và benchmark công bằng;
- các lưu ý phiên bản Python thay vì phát biểu API như thể không bao giờ thay đổi.

Bằng chứng đối chiếu từng trang và mức `Covered/Partial/Missing` nằm trong [báo cáo kiểm định](docs/00_DANH_GIA_DO_BAO_PHU_CHUONG_4.md).

## Phân công chính thức mới

| Thành viên | Chuyên môn chính | Người backup | Trách nhiệm xuyên suốt |
|---|---|---|---|
| TV1 | Nền tảng: sequential/concurrency/parallel/async, hai trục sync–async và blocking–non-blocking, workload, process/thread/coroutine | TV4 | scope, mapping tài liệu gốc, glossary và baseline |
| TV2 | `concurrent.futures`, `Future`, `Executor`, `ThreadPoolExecutor`, order/error/cancel/deadlock | TV5 | bảng API, ví dụ Future, review lifecycle và shutdown |
| TV3 | `ProcessPoolExecutor`, GIL, serialization/pickling, platform caveat và benchmark | TV6 | protocol đo, raw data và kiểm tra claim hiệu năng |
| TV4 | event loop, coroutine/awaitable, Task/Future, orchestration và structured concurrency | TV1 | timeline/sơ đồ runtime và kiểm citation `asyncio` |
| TV5 | timeout, cancellation, error, synchronization, Queue, backpressure, test/debug/shutdown | TV2 | fault injection, test matrix và checklist độ tin cậy |
| TV6 | kiến trúc lai, cây chọn công cụ, demo tích hợp, giới hạn suy diễn và liên hệ distributed systems | TV3 | tích hợp, runbook, phương án offline và rehearsal |

Đây là **phân công trách nhiệm sâu**, không phải ranh giới được phép học. Mọi người vẫn phải nắm 40 năng lực chung trong tài liệu học chéo.

## Quy mô slide dạng mô-đun — chưa tạo PowerPoint

Không khóa cứng một số slide trước khi biết thời lượng giảng viên cho phép. Sườn mới chuẩn bị ba cấu hình:

| Cấu hình | Quy mô | Thời lượng nội dung | Tổng với demo và Q&A | Nguyên tắc |
|---|---:|---:|---:|---|
| Rút gọn | 36 slide chính, 6/người | khoảng 30–36 phút | khoảng 46–56 phút | giữ mạch Core, chuyển chi tiết sang notes/phụ lục |
| Chuẩn | 48 slide chính, 8/người | khoảng 48–55 phút | khoảng 66–75 phút | đủ nền tảng, cơ chế, reliability, demo và kết luận |
| Phụ lục A–Z | 18 slide, 3/người | không tính vào mạch chính | dùng theo Q&A | version caveat, API matrix, phản ví dụ và câu khó |

Số cuối cùng phải được chốt theo thời lượng thực tế. Tài liệu kiến thức có thể rất dài, nhưng mặt slide không được nhồi nguyên đoạn văn; lời giải thích chi tiết sau này nằm ở speaker notes, tài liệu GitHub và phụ lục.

## Đọc repository theo thứ tự này

1. [`00_DANH_GIA_DO_BAO_PHU_CHUONG_4.md`](docs/00_DANH_GIA_DO_BAO_PHU_CHUONG_4.md) — audit PDF 24 trang, kết luận đủ/thiếu, điểm dễ nói sai, Core/Applied/Advanced và cổng nghiệm thu.
2. [`01_BAN_DO_KIEN_THUC_A_Z.md`](docs/01_BAN_DO_KIEN_THUC_A_Z.md) — bản đồ kiến thức rất chi tiết từ A–Z, semantics, bẫy, phiên bản và 33 nguồn chính thức.
3. [`02_PHAN_CONG_6_THANH_VIEN_A_Z.md`](docs/02_PHAN_CONG_6_THANH_VIEN_A_Z.md) — nhiệm vụ cực chi tiết cho từng người, cấu hình slide mô-đun, đầu ra, câu hỏi, review và Definition of Done.
4. [`03_CHUONG_TRINH_HOC_CHUNG_VA_KIEM_TRA_CHEO.md`](docs/03_CHUONG_TRINH_HOC_CHUNG_VA_KIEM_TRA_CHEO.md) — 40 năng lực chung, lộ trình 8 buổi, lab, quiz 60 câu, bảo vệ miệng và quality gates.
5. [`04_DAC_TA_DEMO_THUC_TE_NHO.md`](docs/04_DAC_TA_DEMO_THUC_TE_NHO.md) — đặc tả demo cảm biến, năm mode, dữ liệu, fault injection, test oracle, benchmark và kịch bản live.

Các tài liệu cũ được giữ để truy vết phiên bản ban đầu:

- [`SUON_BAO_CAO_CHUONG_4.md`](docs/SUON_BAO_CAO_CHUONG_4.md) — sườn 42 slide ban đầu;
- [`PHAN_CONG_6_THANH_VIEN.md`](docs/PHAN_CONG_6_THANH_VIEN.md) — phân công tóm tắt ban đầu;
- [`PHAN_CONG_CHI_TIET_6_THANH_VIEN.md`](docs/PHAN_CONG_CHI_TIET_6_THANH_VIEN.md) — bản chi tiết v1.

Khi có khác biệt, bộ tài liệu đánh số `00`–`04` là phương án mới được ưu tiên.

## Hợp đồng kiến thức của cả nhóm

Mỗi thành viên phải làm được cả bốn mức:

1. **Nhận biết:** định nghĩa đúng, không trộn thuật ngữ.
2. **Giải thích:** tự vẽ timeline/state/flow và nói được cơ chế.
3. **Áp dụng:** đọc, chạy, sửa và dự đoán mã.
4. **Phân tích:** chọn mô hình, nêu overhead, giới hạn và phản biện số liệu.

Điều kiện đề xuất trước khi làm PPTX:

- đạt ít nhất 85% quiz chung và không có cụm Core nào dưới 70%;
- trả lời câu ngẫu nhiên ngoài chuyên môn chính;
- backup trình bày thay owner được;
- cả sáu chạy/trace được mọi mode của demo;
- mỗi người sửa được ít nhất một lỗi async không thuộc module mình;
- mọi claim kỹ thuật có nguồn và đúng phiên bản;
- không còn mục Core ở trạng thái thiếu trong coverage matrix.

## Demo dự kiến

**Trung tâm thu thập và phân tích dữ liệu từ nhiều trạm cảm biến**:

```text
trạm cảm biến
→ lấy dữ liệu có độ trễ/lỗi
→ giới hạn concurrency
→ bounded Queue tạo backpressure
→ validation
→ phân tích CPU
→ tổng hợp cảnh báo
→ metric và báo cáo
```

Năm chế độ để so sánh:

1. `sequential` — baseline và oracle tính đúng;
2. `thread` — blocking I/O qua `ThreadPoolExecutor`;
3. `process` — CPU-bound đủ lớn qua `ProcessPoolExecutor`;
4. `async` — concurrent I/O bằng event loop/Task;
5. `hybrid` — `asyncio` cho I/O và process pool cho CPU.

Demo phải chạy offline, cùng seed/input, kiểm tra output tương đương trước benchmark, có timeout/cancellation/Queue/Semaphore/failure injection và lưu raw result. Hiện tại repository chỉ chứa **đặc tả**; theo đúng yêu cầu, chưa viết code và chưa tạo PPTX/PDF.

## Các mốc thực hiện

- [x] Đọc và mapping PDF Chương 4.
- [x] Audit sườn cũ: đúng file gốc nhưng chưa đủ A–Z.
- [x] Xây bản đồ kiến thức A–Z từ nguồn Python chính thức.
- [x] Chia lại sáu chuyên môn cùng owner/backup.
- [x] Đặc tả chương trình học chung và demo nhỏ.
- [ ] Điền họ tên/MSSV vào TV1–TV6.
- [ ] Hỏi giảng viên thời lượng; chốt 36 hay 48 slide chính.
- [ ] Chốt phiên bản Python mục tiêu; khuyến nghị tối thiểu 3.11 nếu dùng `TaskGroup`/`asyncio.timeout` trong Core.
- [ ] Tạo Issues và giao deadline nghiên cứu.
- [ ] Sáu owner viết hồ sơ kiến thức; backup review.
- [ ] Tổ chức quiz, oral defense và lab chung.
- [ ] Chốt bài toán demo rồi mới viết/test/benchmark code.
- [ ] Duyệt nội dung và speaker notes rồi mới thiết kế PPTX/PDF.
- [ ] Rehearsal, chạy offline và chuẩn bị phương án B.

## Quy trình GitHub

1. Mỗi cụm kiến thức có Issue và acceptance criteria.
2. Dùng nhánh `tvN/ten-cong-viec`, không sửa trực tiếp `main` trong giai đoạn nhóm làm việc.
3. Commit nhỏ, mô tả nội dung thực: `docs: clarify TaskGroup failure semantics`.
4. Mỗi Pull Request phải có owner khác review, liên kết nguồn và nêu cách kiểm chứng.
5. Claim hiệu năng phải kèm input, môi trường, tham số, raw result và kiểm tra tính đúng.
6. Nội dung ngoài PDF phải gắn nhãn Nền tảng, Applied hoặc Advanced để không làm loãng mạch chính.
7. Mọi thay đổi API theo phiên bản phải vào version matrix.

## Nguồn chính

- Tài liệu Chương 4 do giảng viên cung cấp — chỉ dùng để mapping nội bộ, không đăng lại PDF nếu chưa được phép.
- [`asyncio` — Python documentation](https://docs.python.org/3/library/asyncio.html)
- [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
- [Runners](https://docs.python.org/3/library/asyncio-runner.html)
- [Synchronization Primitives](https://docs.python.org/3/library/asyncio-sync.html)
- [Queues](https://docs.python.org/3/library/asyncio-queue.html)
- [Developing with asyncio](https://docs.python.org/3/library/asyncio-dev.html)
- [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html)
- [`threading`](https://docs.python.org/3/library/threading.html)
- [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
- [PEP 492 — Coroutines with async and await syntax](https://peps.python.org/pep-0492/)
- [PEP 654 — Exception Groups and `except*`](https://peps.python.org/pep-0654/)

Danh mục đầy đủ 33 nguồn primary nằm cuối bản đồ A–Z.

## Nguyên tắc bản quyền và chất lượng

Repository công khai chỉ lưu nội dung nhóm tự xây dựng và liên kết nguồn. Không đăng lại nguyên PDF/slide của giảng viên khi chưa có quyền. Các ví dụ phải được nhóm tự chạy và tự giải thích; không sao chép một đoạn mã mà không hiểu semantics, lỗi, giới hạn và phiên bản.
