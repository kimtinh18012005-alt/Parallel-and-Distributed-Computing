# KẾ HOẠCH THỰC HIỆN 14 NGÀY VÀ WORK BREAKDOWN STRUCTURE

| Thuộc tính | Giá trị |
|---|---|
| Chu kỳ | 14 ngày chuẩn bị + ngày báo cáo |
| Đơn vị theo dõi | Work package có mã, owner, dependency, điểm và giờ |
| Baseline mỗi thành viên | 8 work package, 100 điểm, 48 giờ dự kiến |
| Công cụ kiểm soát | GitHub Issue, branch, Pull Request, review và Project board |
| Quy tắc hoàn thành | Có artifact, bằng chứng nghiệm thu và reviewer xác nhận |

---

## 1. Quy ước quản trị công việc

### 1.1. Trạng thái

| Trạng thái | Ý nghĩa | Điều kiện chuyển tiếp |
|---|---|---|
| `BACKLOG` | Chưa đủ đầu vào hoặc chưa đến lịch | Dependency đã đóng |
| `READY` | Đủ phạm vi, nguồn và acceptance criteria | Owner nhận task |
| `IN PROGRESS` | Đang thực hiện | Có commit hoặc bằng chứng tiến độ |
| `IN REVIEW` | Đã nộp artifact | PR mở, checklist hoàn chỉnh |
| `REWORK` | Có lỗi cần sửa | Comment được liên kết tới commit sửa |
| `DONE` | Qua review và nghiệm thu | Owner + reviewer cùng xác nhận |
| `BLOCKED` | Không thể tiếp tục | Ghi blocker, người xử lý và hạn phản hồi |

### 1.2. Cấu trúc mã công việc

- `M1-xx` đến `M6-xx`: work package của TV1 đến TV6.
- `SH-xx`: công việc chung có sự tham gia của cả sáu.
- `MS-xx`: milestone.
- `RISK-xx`: rủi ro cần theo dõi.

### 1.3. Cấu trúc tám work package/người

| Hậu tố | Nhóm việc | Điểm | Giờ |
|---:|---|---:|---:|
| `01` | Phạm vi và prerequisite | 8 | 4 |
| `02` | Nghiên cứu chuyên sâu và nguồn | 20 | 10 |
| `03` | Sơ đồ, bảng, ví dụ và phản ví dụ | 12 | 6 |
| `04` | Slide, speaker notes và kịch bản nói | 15 | 7 |
| `05` | Module demo, test, fault và metric | 15 | 7 |
| `06` | Ngân hàng câu hỏi và teach-back | 10 | 5 |
| `07` | Review, backup và sửa sau phản biện | 10 | 5 |
| `08` | GitHub, vai trò xuyên suốt và rehearsal | 10 | 4 |
| **Tổng/người** |  | **100** | **48** |

## 2. WBS — Thành viên 1: nền tảng và bản đồ khái niệm

| ID | Công việc | Dependency | Sản phẩm và tiêu chí nghiệm thu | Điểm | Giờ |
|---|---|---|---|---:|---:|
| M1-01 | Khóa taxonomy và prerequisite | G0 | Glossary sequential/sync/concurrent/parallel/async/blocking; ma trận prerequisite; truy vết SRC-02…SRC-08 | 8 | 4 |
| M1-02 | Viết hồ sơ nền tảng | M1-01 | 4.500–5.500 từ; tối thiểu 5 nguồn; giải thích workload, scheduling, process/thread/coroutine, Amdahl và correctness | 20 | 10 |
| M1-03 | Tạo tài sản học tập | M1-02 | Ma trận thuật ngữ, timeline so sánh, sơ đồ process/thread/coroutine; 2 ví dụ đúng và 2 phản ví dụ | 12 | 6 |
| M1-04 | Đặc tả slide 1–8 | M1-02, M1-03 | 8 slide chuẩn, mapping 6 slide rút gọn, P01–P03; notes 1/3/8 phút; timing 8–9 phút | 15 | 7 |
| M1-05 | Đặc tả data contract và baseline | M1-02 | Generator cố định seed, sequential oracle, digest, 6 loại test, 1 fault, 1 metric nền | 15 | 7 |
| M1-06 | Xây bộ câu hỏi nền tảng | M1-02 | 12 MCQ, 6 tự luận, 2 bài phân loại/debug; đáp án; teach-back 30 phút | 10 | 5 |
| M1-07 | Backup TV4 và review runtime model | M4-04, M4-05 | 5 mục review chính; review PR backup + 1 PR chéo; trình bày thay slide 25–32 một lần | 10 | 5 |
| M1-08 | Duy trì glossary/phạm vi và rehearsal | M1-04, M1-07 | Template glossary; 1 Issue, 1 branch, ≥3 commit, 1 PR; rehearsal chính + backup; workload log | 10 | 4 |
|  | **Tổng TV1** |  |  | **100** | **48** |

## 3. WBS — Thành viên 2: Future, Executor và ThreadPool

| ID | Công việc | Dependency | Sản phẩm và tiêu chí nghiệm thu | Điểm | Giờ |
|---|---|---|---|---:|---:|
| M2-01 | Khóa API và prerequisite | G0, M1-01 | Phạm vi `concurrent.futures`; type/API inventory; truy vết SRC-09…SRC-15; prerequisite thread/pool | 8 | 4 |
| M2-02 | Viết hồ sơ Future/Executor/ThreadPool | M2-01 | 4.500–5.500 từ; ≥5 nguồn; lifecycle, submit/map/wait/as_completed, shutdown, error/cancel/deadlock | 20 | 10 |
| M2-03 | Tạo tài sản Future/ThreadPool | M2-02 | State diagram, API matrix, collection-order timeline; 2 ví dụ đúng, 2 phản ví dụ có timeout bảo vệ | 12 | 6 |
| M2-04 | Đặc tả slide 9–16 | M2-02, M2-03 | 8 slide chuẩn, mapping 6 slide rút gọn, P04–P06; notes 1/3/8 phút; timing 8–9 phút | 15 | 7 |
| M2-05 | Đặc tả blocking adapter và thread mode | M1-05 | Future ownership, result order, exception/timeout/cancel; 6 loại test, 1 fault, latency/throughput metric | 15 | 7 |
| M2-06 | Xây bộ câu hỏi Future/ThreadPool | M2-02 | 12 MCQ, 6 tự luận, 2 bài debug; đáp án; teach-back 30 phút | 10 | 5 |
| M2-07 | Backup TV5 và review reliability | M5-04, M5-05 | 5 mục review chính; review PR backup + 1 PR chéo; trình bày thay slide 33–40 một lần | 10 | 5 |
| M2-08 | Duy trì template ví dụ/test và rehearsal | M2-04, M2-07 | Template example/test; 1 Issue, 1 branch, ≥3 commit, 1 PR; rehearsal chính + backup; workload log | 10 | 4 |
|  | **Tổng TV2** |  |  | **100** | **48** |

## 4. WBS — Thành viên 3: ProcessPool, GIL và hiệu năng

| ID | Công việc | Dependency | Sản phẩm và tiêu chí nghiệm thu | Điểm | Giờ |
|---|---|---|---|---:|---:|
| M3-01 | Khóa môi trường và prerequisite | G0, M1-01 | Python/OS baseline; GIL scope; pickling/main-guard checklist; truy vết SRC-05, SRC-06, SRC-10, SRC-14, SRC-15 | 8 | 4 |
| M3-02 | Viết hồ sơ ProcessPool/GIL/benchmark | M3-01 | 4.500–5.500 từ; ≥5 nguồn; isolation, IPC, serialization, startup, granularity, speedup/efficiency | 20 | 10 |
| M3-03 | Tạo tài sản process/benchmark | M3-02 | Sơ đồ IPC, bảng pickling/platform, benchmark chart schema; 2 ví dụ đúng, 2 phản ví dụ | 12 | 6 |
| M3-04 | Đặc tả slide 17–24 | M3-02, M3-03 | 8 slide chuẩn, mapping 6 slide rút gọn, P07–P09; notes 1/3/8 phút; timing 8–9 phút | 15 | 7 |
| M3-05 | Đặc tả CPU stage và process mode | M1-05 | CPU workload điều chỉnh được, ProcessPool/main guard, digest, 6 loại test, 1 fault, speedup/efficiency metric | 15 | 7 |
| M3-06 | Xây bộ câu hỏi process/hiệu năng | M3-02 | 12 MCQ, 6 tự luận, 2 bài debug/benchmark; đáp án; teach-back 30 phút | 10 | 5 |
| M3-07 | Backup TV6 và review hybrid claims | M6-04, M6-05 | 5 mục review chính; review PR backup + 1 PR chéo; trình bày thay slide 41–48 một lần | 10 | 5 |
| M3-08 | Duy trì citation/benchmark template | M3-04, M3-07 | Source log + benchmark schema; 1 Issue, 1 branch, ≥3 commit, 1 PR; rehearsal chính + backup | 10 | 4 |
|  | **Tổng TV3** |  |  | **100** | **48** |

## 5. WBS — Thành viên 4: event loop, coroutine và Task

| ID | Công việc | Dependency | Sản phẩm và tiêu chí nghiệm thu | Điểm | Giờ |
|---|---|---|---|---:|---:|
| M4-01 | Khóa runtime model và prerequisite | G0, M1-01 | Event source/handler/queue/loop; coroutine/awaitable/Task/Future type map; truy vết SRC-16…SRC-21 | 8 | 4 |
| M4-02 | Viết hồ sơ `asyncio` cốt lõi | M4-01 | 4.500–5.500 từ; ≥5 nguồn; loop lifecycle, scheduling, orchestration, structured concurrency, async iteration/context | 20 | 10 |
| M4-03 | Tạo tài sản runtime | M4-02 | Event-loop diagram, scheduling trace, type comparison; 2 ví dụ đúng, 2 phản ví dụ blocking/never-awaited | 12 | 6 |
| M4-04 | Đặc tả slide 25–32 | M4-02, M4-03 | 8 slide chuẩn, mapping 6 slide rút gọn, P10–P12; notes 1/3/8 phút; timing 8–9 phút | 15 | 7 |
| M4-05 | Đặc tả async adapter và async mode | M1-05 | Coroutine/Task ownership, TaskGroup trace, CPU bridge; 6 loại test, 1 fault, responsiveness/in-flight metric | 15 | 7 |
| M4-06 | Xây bộ câu hỏi event loop/Task | M4-02 | 12 MCQ, 6 tự luận, 2 bài dự đoán trace/debug; đáp án; teach-back 30 phút | 10 | 5 |
| M4-07 | Backup TV1 và review nền tảng | M1-04, M1-05 | 5 mục review chính; review PR backup + 1 PR chéo; trình bày thay slide 1–8 một lần | 10 | 5 |
| M4-08 | Duy trì diagram/story template | M4-04, M4-07 | Template diagram/notes/transition; 1 Issue, 1 branch, ≥3 commit, 1 PR; rehearsal chính + backup | 10 | 4 |
|  | **Tổng TV4** |  |  | **100** | **48** |

## 6. WBS — Thành viên 5: điều phối, lỗi và độ tin cậy

| ID | Công việc | Dependency | Sản phẩm và tiêu chí nghiệm thu | Điểm | Giờ |
|---|---|---|---|---:|---:|
| M5-01 | Khóa failure model và prerequisite | G0, M2-01, M4-01 | Error taxonomy, ownership, timeout/cancel boundary, primitive inventory; truy vết SRC-21, SRC-22 | 8 | 4 |
| M5-02 | Viết hồ sơ reliability/coordination | M5-01 | 4.500–5.500 từ; ≥5 nguồn; error propagation, retry/idempotency, sync primitives, Queue, shutdown | 20 | 10 |
| M5-03 | Tạo tài sản reliability | M5-02 | Primitive matrix, cancellation state diagram, shutdown sequence; 2 ví dụ đúng, 2 phản ví dụ race/leak | 12 | 6 |
| M5-04 | Đặc tả slide 33–40 | M5-02, M5-03 | 8 slide chuẩn, mapping 6 slide rút gọn, P13–P15; notes 1/3/8 phút; timing 8–9 phút | 15 | 7 |
| M5-05 | Đặc tả Queue/Semaphore/failure policy | M2-05, M4-05 | Bounded queue, concurrency limit, retry/cancel/shutdown; 6 loại test, 1 fault, queue/in-flight/error metric | 15 | 7 |
| M5-06 | Xây bộ câu hỏi reliability | M5-02 | 12 MCQ, 6 tự luận, 2 bài debug/thiết kế; đáp án; teach-back 30 phút | 10 | 5 |
| M5-07 | Backup TV2 và review executor lifecycle | M2-04, M2-05 | 5 mục review chính; review PR backup + 1 PR chéo; trình bày thay slide 9–16 một lần | 10 | 5 |
| M5-08 | Duy trì rubric/fault matrix | M5-04, M5-07 | Template QA/fault; 1 Issue, 1 branch, ≥3 commit, 1 PR; rehearsal chính + backup; workload log | 10 | 4 |
|  | **Tổng TV5** |  |  | **100** | **48** |

## 7. WBS — Thành viên 6: kiến trúc lai, quyết định và liên hệ phân tán

| ID | Công việc | Dependency | Sản phẩm và tiêu chí nghiệm thu | Điểm | Giờ |
|---|---|---|---|---:|---:|
| M6-01 | Khóa decision criteria và interface | G0, M1-01 | Cây chọn tuần tự/thread/process/async/hybrid; integration contract; truy vết SRC-23, SRC-24 | 8 | 4 |
| M6-02 | Viết hồ sơ decision/hybrid/distributed | M6-01 | 4.500–5.500 từ; ≥5 nguồn; resource budget, boundary, failure model và giới hạn suy diễn | 20 | 10 |
| M6-03 | Tạo tài sản kiến trúc | M6-02 | Decision tree, hybrid architecture, resource-budget matrix; 2 ví dụ đúng, 2 phản ví dụ | 12 | 6 |
| M6-04 | Đặc tả slide 41–48 | M6-02, M6-03 | 8 slide chuẩn, mapping 6 slide rút gọn, P16–P18; notes 1/3/8 phút; timing 8–9 phút | 15 | 7 |
| M6-05 | Đặc tả hybrid mode và integration contract | M1-05, M2-05, M3-05, M4-05, M5-05 | CLI/report schema, interface validation, 6 loại test, 1 fault, end-to-end metric; không viết thay module khác | 15 | 7 |
| M6-06 | Xây bộ câu hỏi kiến trúc | M6-02 | 12 MCQ, 6 tự luận, 2 bài lựa chọn kiến trúc; đáp án; teach-back 30 phút | 10 | 5 |
| M6-07 | Backup TV3 và review process claims | M3-04, M3-05 | 5 mục review chính; review PR backup + 1 PR chéo; trình bày thay slide 17–24 một lần | 10 | 5 |
| M6-08 | Duy trì template Issue/PR/runbook | M6-04, M6-07 | Template quản trị; 1 Issue, 1 branch, ≥3 commit, 1 PR; rehearsal chính + backup; workload log | 10 | 4 |
|  | **Tổng TV6** |  |  | **100** | **48** |

## 8. Công việc chung

| ID | Công việc | Thành phần tham gia | Đầu ra | Điều kiện hoàn thành |
|---|---|---|---|---|
| SH-01 | Kickoff và gán danh tính TV1–TV6 | 6/6 | Danh sách tên, MSSV, liên hệ, owner/backup | Tất cả xác nhận |
| SH-02 | Khóa data/interface contract từ M1-05 | 6/6 | Schema input/output, seed, error model, metric | Sáu module dùng được cùng contract |
| SH-03 | Diagnostic và glossary | 6/6 | Điểm đầu vào và thuật ngữ thống nhất | Không còn định nghĩa mâu thuẫn |
| SH-04 | Teach-back vòng 1 | TV1–TV3 dạy; 6/6 học | Biên bản, câu hỏi và lỗ hổng | Mỗi phiên đủ 30 phút |
| SH-05 | Teach-back vòng 2 | TV4–TV6 dạy; 6/6 học | Biên bản, câu hỏi và lỗ hổng | Mỗi phiên đủ 30 phút |
| SH-06 | Lab và fault drill | 6/6 | Kết quả 8 lab chung | Mỗi người sửa một lỗi ngoài chuyên môn |
| SH-07 | Quiz và oral defense | 6/6 | Điểm, câu hỏi ngẫu nhiên, kế hoạch học bù | ≥85% tổng; không cụm nào <70% |
| SH-08 | Integration rehearsal | 6/6 | Checklist năm mode và timing | Mỗi owner chạy segment của mình |
| SH-09 | Backup rehearsal | 3 cặp backup | Video/phiếu nhận xét | Backup trình bày trọn cụm |
| SH-10 | Content freeze | 6/6 | Release candidate tài liệu | Không còn blocker mức nghiêm trọng |

## 9. Lịch 14 ngày

| Mốc | Trọng tâm | Work package chính | Artifact cuối ngày | Gate |
|---|---|---|---|---|
| D−14 | Kickoff và diagnostic | SH-01, SH-03, M1-01…M6-01 | Danh tính, baseline điểm, prerequisite map | G0 |
| D−13 | Truy vết nguồn và khóa scope | M1-01…M6-01 | Requirement mapping và source log | G1 |
| D−12 | Nghiên cứu chuyên sâu | M1-02…M6-02 | Outline hồ sơ + danh mục nguồn |  |
| D−11 | Hoàn thiện hồ sơ chuyên môn | M1-02…M6-02 | Sáu hồ sơ bản review | G2 |
| D−10 | Tài sản trực quan và ví dụ | M1-03…M6-03 | 18 tài sản chính + 24 ví dụ |  |
| D−9 | Outline slide và speaker notes | M1-04…M6-04 | 48/36/18 outline | G3 |
| D−8 | Teach-back TV1–TV3 | SH-04, M1-06…M3-06 | Biên bản, câu hỏi, action item |  |
| D−7 | Teach-back TV4–TV6 | SH-05, M4-06…M6-06 | Biên bản, câu hỏi, action item |  |
| D−6 | Đặc tả module demo | SH-02, M1-05…M6-05 | Interface, test, fault và metric | G5-ready |
| D−5 | Review backup và review chéo | M1-07…M6-07 | PR comment, rework list |  |
| D−4 | Lab, quiz và oral defense | SH-06, SH-07 | Điểm và kế hoạch học bù | G4 |
| D−3 | Rehearsal nội dung chuẩn | M1-08…M6-08 | Timing, transition, Q&A log |  |
| D−2 | Integration và backup rehearsal | SH-08, SH-09 | Runbook, fallback, backup sign-off | G6-ready |
| D−1 | Content freeze | SH-10 | Release candidate, checksum/commit | G6 |
| D0 | Báo cáo | 6/6 | Bản phát hành và biên bản Q&A | G7 |

## 10. Ma trận dependency trọng yếu

| Đầu ra | Phụ thuộc | Tác động nếu trễ | Phương án xử lý |
|---|---|---|---|
| Glossary/taxonomy TV1 | SRC mapping | Sáu hồ sơ dùng thuật ngữ khác nhau | Freeze glossary D−13; thay đổi qua Issue |
| Data contract TV1 | Thống nhất demo | Năm mode không so sánh được | Review 6/6 trước khi làm module |
| Thread mode TV2 | Data contract | Reliability test thiếu backend | Dùng stub theo contract |
| Process mode TV3 | CPU stage + main guard | Hybrid thiếu bước CPU | Chuẩn bị saved result và mode giảm tải |
| Async mode TV4 | Async adapter | TV5 không test cancel/Queue được | Mock async adapter có kiểm soát |
| Reliability TV5 | Thread + async interface | Failure scenario không tích hợp | Test policy độc lập bằng fake adapter |
| Hybrid contract TV6 | Interface của năm owner | Runbook và report trễ | Chỉ tích hợp contract đã ký; owner tự sửa module |
| Quiz/oral | Sáu hồ sơ chuyên môn | Không chứng minh hiểu chung | Không mở content freeze khi chưa đạt |

## 11. Bảng kiểm soát khối lượng hằng ngày

| Thành viên | Baseline điểm | Baseline giờ | Giờ thực tế | Chênh lệch | Blocker | Hành động tái phân bổ |
|---|---:|---:|---:|---:|---|---|
| TV1 | 100 | 48 |  |  |  |  |
| TV2 | 100 | 48 |  |  |  |  |
| TV3 | 100 | 48 |  |  |  |  |
| TV4 | 100 | 48 |  |  |  |  |
| TV5 | 100 | 48 |  |  |  |  |
| TV6 | 100 | 48 |  |  |  |  |

Chênh lệch dự kiến trên 5% phải được giải thích. Chênh lệch thực tế trên 10% kích hoạt tái phân bổ task độc lập; không chuyển ownership chuyên môn nếu chưa bàn giao prerequisite và acceptance criteria.

## 12. Risk register

| ID | Rủi ro | Xác suất | Tác động | Chủ trì | Biện pháp |
|---|---|---|---|---:|---|
| RISK-01 | Chưa biết thời lượng báo cáo | Trung bình | Cao | TV4 | Duy trì đồng thời cấu hình 36 và 48 slide |
| RISK-02 | Nội dung quá rộng | Cao | Cao | TV1 | Giữ Core ở mạch chính; Applied/Advanced vào phụ lục |
| RISK-03 | Claim API sai phiên bản | Trung bình | Cao | TV3 | Version matrix, source log và review claim |
| RISK-04 | Chỉ owner hiểu phần chuyên môn | Trung bình | Cao | TV5 | Teach-back, oral defense và backup rehearsal |
| RISK-05 | TV6 bị dồn tích hợp | Cao | Cao | TV6 | Integration contract; owner tự sửa module mình |
| RISK-06 | Demo live thất bại | Trung bình | Cao | TV2 | Smoke test, saved result, video và offline mode |
| RISK-07 | Benchmark không công bằng | Trung bình | Cao | TV3 | Fixed seed, oracle, repeats, median và metadata |
| RISK-08 | Slide dày chữ | Cao | Trung bình | TV4 | Một thông điệp/slide; chi tiết vào notes/phụ lục |
| RISK-09 | Thành viên trễ task | Trung bình | Cao | TV6 | Daily board, blocker SLA 24 giờ và tái phân bổ |
| RISK-10 | Upload tài liệu không có quyền | Thấp | Cao | TV1 | Chỉ lưu nội dung tự viết và liên kết nguồn |
| RISK-11 | Test của module không đủ sáu nhóm | Trung bình | Cao | TV2 | Dùng test template; Gate G5 không đóng khi thiếu case |
| RISK-12 | Failure path và cleanup bị bỏ sót | Trung bình | Cao | TV5 | Fault matrix, resource check và shutdown rehearsal |

## 13. Quy tắc bàn giao

Một work package chỉ chuyển sang `DONE` khi có đủ:

1. Artifact đúng tên và đúng thư mục.
2. Requirement ID hoặc Issue liên kết rõ.
3. Nguồn và phiên bản cho claim kỹ thuật.
4. Acceptance criteria đã tự kiểm.
5. Pull Request không còn comment nghiêm trọng.
6. Reviewer xác nhận và owner sửa rework.
7. Workload log đã cập nhật.
8. Dependency downstream được thông báo.

Không dùng tin nhắn riêng làm bằng chứng hoàn thành. Quyết định kỹ thuật, thay đổi phạm vi và kết quả review phải được truy vết trên GitHub.
