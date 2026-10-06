# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Đình Thái | 2A202602718 | Cả bài lab |

Mô hình dự kiến dùng xuyên suốt thí nghiệm là `google_genai:gemini-3.5-flash-lite`. Kết quả Phần 1 dưới đây đã được chạy bằng chính model này.

| Thành phần | Cấu hình |
|---|---|
| Provider | Gemini Developer API, xác thực bằng `GOOGLE_API_KEY` trong `.env` |
| `LAB_MODEL` | `google_genai:gemini-3.5-flash-lite` |
| `LAB_TEMPERATURE` | `0`; SDK báo model dùng tham số lấy mẫu cố định và bỏ qua giá trị này |
| `recursion_limit` | 60 bước |
| Timeout | 60 giây/request Gemini; 120 giây/lệnh shell |
| Giới hạn request phía client | 12 request/phút, tối đa một request mỗi 5 giây, không burst |
| Retry | Tối đa 2 lần với `RemoteProtocolError`, chờ ban đầu 2 giây; SDK `max_retries=1` |
| Deep Agents / LangChain Google GenAI | `0.7.21` / `4.4.0` |
| Python / hệ điều hành | `3.11.9` / Windows build `26100` |
| Môi trường thực thi | Chạy trực tiếp trong `.venv`; backend dùng Git for Windows Bash |

Kiểm tra kết nối trả về `OK`, dùng 5 token. Các test Phần 0–3 hiện đạt tổng cộng 29 test: 12 test mô-đun có sẵn, 9 test agent/subagent, 6 test runner và 2 test curator.

Báo cáo sử dụng lần chạy hợp lệ mới nhất của `baseline/data-learn`, bắt đầu lúc `2026-10-06T04:31:30.110894+00:00` (UTC). Nguồn số liệu: [run.json](../results/baseline/data-learn/run.json) và [trace.md](../results/baseline/data-learn/trace.md).

| Chỉ số lần chạy mới nhất | Giá trị |
|---|---|
| Số lần chạy hợp lệ đưa vào báo cáo | 1 (`baseline/data-learn`) |
| Điểm | 5/8 (62,5%); 5/5 check kỹ thuật đạt, 0/3 check quy ước đạt |
| Token input / output / total | 223.249 / 6.146 / 229.395 |
| Tool call / subagent call | 23 / 0 |
| Thời gian | 127,5 giây |
| `error` | `null` |
| `skills_read` / `skills_modified` | 0 / `false` |

Ngân sách thí nghiệm chưa được cung cấp. Tag `freeze` chưa được tạo; giả thuyết và các điều kiện so sánh sẽ được hoàn thiện ở các phần tiếp theo của GUIDE.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): `baseline` sẽ đạt điểm đánh giá cao hơn hoặc tương đương `subagents`. Trên tác vụ học, subagents tốn trung bình 367.052 token/lần so với 166.252 của baseline nhưng đạt 17/27 check so với 18/27; thêm vai trò chưa cho thấy lợi ích điểm số ổn định.
- H2 (skills-auto so với baseline): `skills-auto` sẽ cải thiện các check quy ước trên tác vụ đánh giá và có thể vượt `baseline`, vì skill `adhere-to-strict-naming-and-formatting-rules` biến 9 lỗi nhóm E thành checklist tổng quát. Tuy nhiên, mức cải thiện có thể nhỏ hoặc không chuyển giao do skill được sinh từ ba tác vụ học và có nguy cơ quá khớp; `skills_read` cũng phụ thuộc mô tả skill.
- H3 (tác vụ học so với tác vụ đánh giá): mỗi điều kiện sẽ đạt điểm trung bình trên tác vụ học cao hơn tác vụ đánh giá. Tác vụ đánh giá dùng dữ liệu khác và thêm quy ước mới, nên chênh lệch sẽ đo khả năng khái quát của quy trình thay vì ghi nhớ nội dung học.

## 3. Làm quen Deep Agents (Phần 0.3)

1. `scripts/tour.py` liệt kê các công cụ tệp `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`; công cụ shell `execute`; và công cụ giao việc `task`. `execute` chạy lệnh trong thư mục gốc của backend.
2. `task` có subagent mặc định `general-purpose` để nghiên cứu, tìm tệp/nội dung và xử lý tác vụ nhiều bước. Nó có cùng bộ công cụ với tác tử chính. Mỗi lần gọi mặc định là một phiên mới, chỉ thấy prompt được giao và trả lại một báo cáo cuối.
3. System prompt mặc định là chuỗi rỗng (`''`). Mô tả `task` ghi: “Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report.” Mô tả `execute` ghi: “You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search.”

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Số liệu lấy từ ba lần chạy học hợp lệ trong `results/baseline/`. `baseline/data-learn` được dùng lại từ Phần 1; `code-learn` và `logs-learn` được chạy ở Phần 2 với cùng model `google_genai:gemini-3.5-flash-lite`.

| Tác vụ | Điểm | Check kỹ thuật | Check quy ước | Token | Thời gian |
|---|---|---|---|---|---|
| [code-learn](../results/baseline/code-learn/run.json) | 7/10 | 7/7 | 0/3 | 197,518 | 143.8 giây |
| [data-learn](../results/baseline/data-learn/run.json) | 5/8 | 5/5 | 0/3 | 229,395 | 127.5 giây |
| [logs-learn](../results/baseline/logs-learn/run.json) | 6/9 | 6/6 | 0/3 | 71,845 | 53.3 giây |

### Check thất bại và bằng chứng

Mỗi dòng dưới đây là một check thất bại của baseline. Bằng chứng trích từ `checks[].detail` của tác vụ tương ứng.

| Tác vụ | Check thất bại | Nhóm lỗi | Bằng chứng |
|---|---|---|---|
| code-learn | `rule_type_hints` | E | `RULE: every public function ... has type annotations on all parameters and on the return value.` |
| code-learn | `rule_regression_tests` | E | `RULE: add tests/test_regressions.py ... (at least 3); the file must pass.` |
| code-learn | `rule_changelog` | E | `RULE: record each fix in CHANGELOG.md under the heading '## Unreleased'` |
| data-learn | `rule_money_in_cents` | E | `RULE: money values in answer.json are integer cents` |
| data-learn | `rule_meta_block` | E | `RULE: answer.json has an object meta`; phải có `source`, `rows_in`, `rows_used`. |
| data-learn | `rule_clean_csv` | E | `RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents` |
| logs-learn | `rule_service_names` | E | `RULE: service names in the output are lower-case with '-' replaced by '_'` |
| logs-learn | `rule_sorted_errors` | E | `RULE: errors is sorted by service, then by timestamp_utc, ascending.` |
| logs-learn | `rule_schema_header` | E | `RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage".` |

### Nhận xét

- Nhóm E chiếm 9/9 check thất bại (100%). Tác tử giải quyết được yêu cầu kỹ thuật nhưng thiếu các quy ước Acme cụ thể, vốn không được mô tả đầy đủ trong đề.
- Có 18/18 check kỹ thuật đạt. Đây là bằng chứng phủ định việc lỗi A–D chi phối kết quả cuối cùng trong ba lần chạy này; không đủ để kết luận mọi bước thực hiện đều tối ưu.
- [Trace code-learn](../results/baseline/code-learn/trace.md) cho thấy tác tử đọc README và docstring, sửa hàm dùng chung và chạy lại pytest; kết quả cuối là `7 passed`. Tác tử tạo rồi xóa test tạm, không để lại `tests/test_regressions.py` theo quy ước.
- [Trace data-learn](../results/baseline/data-learn/trace.md) cho thấy tác tử xử lý dòng trùng, giá trị thiếu và ngày giờ, ghi `answer.json` rồi đọc lại bằng shell. [Trace logs-learn](../results/baseline/logs-learn/trace.md) cho thấy tác tử đọc đặc tả và toàn bộ log, chạy parser, đọc lại `errors.json` trước khi kết thúc.
- Skill có thể phòng ngừa nhóm E bằng hướng dẫn tổng quát theo loại tác vụ: bổ sung type hint, test hồi quy và changelog cho sửa mã; chuẩn hóa tiền sang cent, metadata và CSV sạch cho báo cáo dữ liệu; chuẩn hóa tên dịch vụ, thứ tự lỗi và header schema cho log. Đây là hướng kiểm chứng ở Phần 3, chưa phải kết luận về hiệu quả skill.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa ở Phần 1.1: `explorer` đọc đặc tả và dữ liệu mà không sửa tệp; `implementer` thực hiện thay đổi và chạy kiểm tra; `reviewer` rà soát độc lập kết quả. `description` của mỗi vai trò nêu tình huống nên giao việc, còn `system_prompt` giới hạn phạm vi công việc.
- Kết quả hiện có của `subagents`:

| Tác vụ | Điểm | Token | Tool call luồng chính | `subagent_calls` | Thời gian | Lỗi |
|---|---:|---:|---:|---:|---:|---|
| `code-learn` | 7/10 | 322.654 | 8 | 4 | 300,3 giây | không |
| `data-learn` | 4/8 | 519.626 | 23 | 1 | 290,6 giây | không |
| `logs-learn` (chạy lại) | 6/9 | 258.876 | 10 | 2 | 207,7 giây | không |

Lần chạy `logs-learn` đầu tiên bị 504 được lưu riêng ở `results/_failed/subagents-logs-learn-504/`; bản ghi 0/9 đó là lỗi hạ tầng và không được diễn giải như lỗi nội dung. Lần chạy lại hoàn tất với 6/9.

- `code-learn` gọi `explorer` hai lần và `implementer` hai lần. Trace cho thấy lời giao việc có đường dẫn, yêu cầu đọc docstring, chạy test và giữ nguyên test gốc; tác tử chính đọc báo cáo rồi tự sửa và kiểm chứng. `data-learn` gọi một `implementer` với các quy tắc dữ liệu chính; kết quả thiếu 4 check (một check kỹ thuật về số order và ba quy ước). `logs-learn` gọi `implementer` hai lần; sau lần đầu 504, lần chạy lại tạo cấu trúc log hợp lệ và đạt cả 6 check kỹ thuật, còn thiếu ba quy ước E.
- Khi subagent được gọi, `UsageMetadataCallbackHandler` cộng token của cả luồng chính và subagent. So với baseline cùng tác vụ, chi phí tăng rõ: code 322.654 so với 197.518 (+63,4%); data 519.626 so với 229.395 (+126,5%). Điểm code giữ nguyên 7/10; điểm data giảm từ 5/8 xuống 4/8. Vì vậy trong mẫu nhỏ này đa tác tử chưa chứng minh được lợi ích điểm số tương xứng với chi phí.
- `skills_read=0` và `skills_modified=false` ở cả ba lần subagents; điều kiện này không nạp skill. Trace chính chỉ hiển thị call `task` và báo cáo cuối, không hiển thị toàn bộ thao tác bên trong subagent. Trung bình subagents đạt 17/27 check (63,0%) và 367.052 token/lần; baseline đạt 18/27 (66,7%) và 166.252 token/lần. Trong dữ liệu học hiện có, subagents tốn khoảng 2,21 lần token nhưng thấp hơn một check kỹ thuật so với baseline.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator chạy 1 lần trên đúng ba run `baseline` có `role=learn`; không đọc dữ liệu eval. Không có skill nào bị xóa vì cả ba đều vượt `validate_skill`, không chứa marker eval và có thân 8 dòng.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `adhere-to-strict-naming-and-formatting-rules` | Tổng quát cho output có schema, metadata, tên và định dạng; không nêu task hoặc dữ liệu riêng. | Đúng với 9 feedback nhóm E về cent, metadata, CSV, service name, sort và schema. Cần đối chiếu đề trước khi áp dụng vì ví dụ trong skill chỉ minh họa quy tắc. | 8 dòng; description bắt đầu `Use when generating structured output files...`; `skills_read`: 3 ở code-learn, 1 ở data-learn, 0 ở logs-learn. |
| `comprehensive-regression-testing` | Tổng quát cho sửa code; yêu cầu test hồi quy và changelog. | Đúng với `rule_regression_tests` và `rule_changelog`; không giải quyết type hints nếu tác tử không tự kiểm tra annotation. | 8 dòng; description nêu rõ tình huống sửa bug; `skills_read`: code-learn đọc skill này. |
| `verify-rfc4180-csv-quoting` | Hẹp hơn, chỉ áp dụng cho CSV có ký tự đặc biệt; vẫn là quy trình theo loại dữ liệu, không lộ dữ liệu eval. | Đúng với lỗi quoting của `code-learn`; không liên quan trực tiếp đến các lỗi còn lại. | 8 dòng; description nêu CSV comma/quote/newline và RFC 4180; `skills_read`: code-learn đọc skill này. |

Kết quả `skills-auto --tasks learn`: `code-learn` 8/10, `data-learn` 5/8, `logs-learn` 6/9. `skills_read` lần lượt là 3, 1, 0; cả ba có `skills_modified=false`. `code-learn` đạt 8/10 nhưng kết thúc bằng `GraphRecursionError` ở giới hạn 60 sau khi đã ghi thay đổi; `data-learn` và `logs-learn` không có lỗi hạ tầng. So với baseline tương ứng, code tăng từ 7/10 lên 8/10, data giữ 5/8, logs giữ 6/9. Hai check quy ước của code còn lại là `rule_type_hints` và `rule_changelog`; đây là bằng chứng skill được đọc nhưng không bảo đảm tác tử làm theo toàn bộ checklist.

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

Phần 4 đã tạo commit `hypotheses` (`b9318d8`) và tag `freeze` (`15f9687`). Sau khi thay API key Gemini, sáu lần chạy `skills-auto` sau freeze đã hoàn tất.

| Tác vụ | baseline | subagents | skills-auto |
|---|---:|---:|---:|
| `code-learn` | 7/10 | 7/10 | 8/10* |
| `data-learn` | 5/8 | 4/8 | 5/8 |
| `logs-learn` | 6/9 | 6/9 | 6/9 |
| `code-eval` | 7/11 | 7/11 | 8/11* |
| `data-eval` | 5/9 | 5/9 | 5/9 |
| `logs-eval` | 6/10 | 6/10 | 6/10 |
| **Mean learning** | 0.66 | 0.62 | 0.70 |
| **Mean evaluation** | 0.60 | 0.60 | 0.63 |
| **Mean tokens/run** | 136,103 | 269,517 | 165,220 |

`skills-auto` đọc skill ở 5/6 lần chạy và không sửa skill. `code-learn` (208.895 token) và `code-eval` (205.425 token) đạt điểm tương ứng 8/10 và 8/11 nhưng kết thúc bằng `GraphRecursionError` ở giới hạn 60; đây là lỗi dừng của graph sau khi đã ghi kết quả, không phải quota. Bốn lần chạy còn lại không có lỗi. Không có lần chạy nào sau khi đổi key bị 429. Kết quả trước freeze được lưu tại `results/skills-auto-dev/` và không dùng thay cho sáu bản ghi chính thức.

Chi tiết máy sinh nằm tại [table.md](table.md); kiểm tra `verify_freeze.py` báo `checked 6 runs of skill conditions: OK`. Kết quả breakdown xác nhận cả ba điều kiện đạt 18/18 check kỹ thuật ở eval; khác biệt nằm ở check `rule_`.

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, `skills-auto` tăng học từ 18/27 lên 19/27 check (mean 0,66 lên 0,70) và tăng eval từ 18/30 lên 19/30 (0,60 lên 0,63). `subagents` giảm học xuống 17/27 và không đổi eval. Skill giúp học và chuyển giao một phần sang eval; mức tăng nhỏ và code có lỗi recursion nên không nên xem là thắng tuyệt đối.
2. Cả ba điều kiện đạt 18/18 check kỹ thuật ở eval. Chênh lệch đều nằm ở `rule_`: skills-auto đạt 1/12 eval, baseline/subagents 0/12. Skill tổng quát về naming/formatting giúp một quy ước, nhưng quy ước mới của eval phần lớn không xuất hiện trong dữ liệu học nên không thể bảo đảm bao phủ.
3. `code-eval` đạt `rule_regression_tests` sau khi đọc ba skill (`skills_read=3`), nhưng vẫn trượt `rule_type_hints` và `rule_changelog`; đọc skill không đồng nghĩa làm đủ checklist. `logs-learn` không đọc skill (`skills_read=0`) và giữ 6/9, cho thấy việc nạp skill phụ thuộc mô tả tác vụ.
4. Token trung bình: baseline 136.103, subagents 269.517, skills-auto 165.220. Baseline có điểm/token tốt nhất; skills-auto mua thêm khoảng 3 điểm phần trăm mean eval với khoảng 21% token, còn subagents tăng gần gấp đôi token mà không tăng eval. Trong mẫu này đa tác tử chưa đáng chi phí.
5. Không có dấu hiệu rò rỉ dữ liệu: curator chỉ đọc ba run `role=learn`, chặn marker eval và kiểm tra skill bằng validator trước khi ghi. Các skill không chứa tên task hay dữ liệu cụ thể; nguy cơ còn lại là quá khớp quy ước học.
6. So với bản sao trước freeze (code 8/10, data 5/8, logs 6/9), sau freeze là code 8/10, data 5/8, logs 6/9: chênh lệch 0 ở cả ba. Điều này hỗ trợ độ ổn định của chênh lệch chính, nhưng mỗi cấu hình chỉ chạy một lần và code vẫn có lỗi recursion.

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1. Mỗi task/điều kiện chỉ chạy một lần, nên nhiễu sampling và trạng thái dịch vụ có thể lớn hơn chênh lệch 0,03–0,04 điểm.
2. Chỉ dùng một model Gemini và ba task mỗi vai trò; kết luận chưa khái quát sang model, quota hoặc bộ task khác.
3. `code-learn` và `code-eval` dừng ở recursion limit sau khi ghi điểm; điểm một phần hữu ích để quan sát nhưng không tương đương một lần chạy sạch.
4. Các quy ước Acme được ẩn trong grader, nên skill có thể cải thiện checklist đã thấy mà bỏ sót quy ước mới.

## 10. Kết luận

`skills-auto` đạt mean 0,70 ở học và 0,63 ở eval, cao hơn baseline 0,66 và 0,60 trong mẫu này. `subagents` tăng chi phí lên 269.517 token/lần nhưng không tăng điểm eval. Lợi ích của skill chủ yếu nằm ở check quy ước, còn 18/18 check kỹ thuật đạt ở cả ba điều kiện eval. Hai lần chạy code gặp `GraphRecursionError`, nên cần tăng giới hạn hoặc bổ sung điều kiện dừng trước khi kết luận chắc chắn. Bước tiếp theo là lặp mỗi task nhiều lần với cùng freeze và ghi khoảng tin cậy.

## Phụ lục

### Cài đặt harness (Phần 1)

| Bước | Nội dung đã cài đặt | Kiểm tra |
|---|---|---|
| 1.1 | `get_subagents()` trả về `explorer`, `implementer`, `reviewer`; mỗi vai trò có tên duy nhất, mô tả tình huống giao việc và system prompt xác định phạm vi. | Test cấu trúc và hai test tích hợp subagent đều đạt trong `test_02_agent.py`. |
| 1.2 | `make_backend()` dùng `LocalShellBackend` với đường dẫn ảo, không kế thừa biến môi trường, đặt PATH chứa Python và timeout 120 giây. `build_agent()` hỗ trợ `single`, `subagents`, nạp skill theo yêu cầu và nối `PATHS_NOTE` vào prompt của subagent. | `python -m pytest tests/test_02_agent.py` → `9 passed`. |
| 1.3 | `run_task()` tạo và xóa sandbox tạm, cộng token bằng callback, chấm điểm, đếm tool/subagent/skill, so hash skill và ghi `run.json`, `trace.md`. | `test_03_runner.py`: 6 test đạt; chạy cùng `test_01_provided.py` cho kết quả `18 passed`. |

Tổng cộng 29 test Phần 0 đến Phần 3 đạt. Các hằng số prompt, `render_trace`, `main` và các tệp có sẵn được giữ nguyên. Backend trên Windows dùng Git for Windows Bash (`--noprofile --norc`) qua một script tạm được xóa sau mỗi lệnh; không kế thừa môi trường của tiến trình cha. Alias hàm `python3` dùng Python của `.venv`. Đã kiểm tra ngoại tuyến cả lệnh Python nhiều dòng và heredoc: đều in đúng kết quả, exit code 0. Với cấu hình backend cuối cùng, 15 test `test_02_agent.py` và `test_03_runner.py` đều đạt; `test_04_curator.py` có 2 test đạt.

Runner dùng `agent.stream(..., stream_mode="values")` theo mở rộng được nêu trong pseudo-code để giữ trace khi API lỗi. Với model Gemini thực, `ModelRetryMiddleware` thử lại tối đa hai lần đối với `RemoteProtocolError` (chờ ban đầu 2 giây); SDK được đặt `max_retries=1` để tránh hai tầng retry. `InMemoryRateLimiter` cấp tối đa một request mỗi 5 giây (12/phút), dùng chung đối tượng model giữa tác tử chính và subagent. Lỗi quota không được thử lại bằng middleware này; timeout chỉ giới hạn thời gian chờ, không ngăn vượt hạn mức. Các cấu hình này cần giữ giống nhau giữa các điều kiện thí nghiệm và chạy các tác vụ tuần tự; limiter không phối hợp giữa các tiến trình riêng.

### Mốc chạy thật cuối Phần 1

Lệnh: `python -m lab.runner --condition baseline --tasks data-learn`.

Lần chạy hợp lệ mới nhất bắt đầu lúc `2026-10-06T04:31:30.110894+00:00` (UTC), dùng `google_genai:gemini-3.5-flash-lite` với cấu hình ở mục 1:

| Chỉ số | Kết quả |
|---|---|
| Điểm | 5/8 (62,5%) |
| Check kỹ thuật | 5/5 đạt |
| Check quy ước tổ chức | 0/3 đạt |
| Token input / output / total | 223.249 / 6.146 / 229.395 |
| Tool call / subagent call | 23 / 0 |
| Thời gian | 127,5 giây |
| `error` | `null` |
| `skills_read` / `skills_modified` | 0 / `false` |

Đã xác nhận `results/baseline/data-learn/run.json` và `trace.md` tồn tại; trace có 31.257 byte; `tokens.total>0`; mọi check thất bại có `detail`. Sandbox của lần chạy đã được xóa. Trace cho thấy tác tử đọc `workspace/README.md`, chuyển sang thư viện chuẩn `csv` sau khi gặp lỗi thiếu `pandas`, xử lý dữ liệu, ghi `workspace/answer.json` và đọc lại JSON bằng shell trước khi kết thúc.

Ba check chưa đạt là `rule_money_in_cents` (tiền phải là số nguyên cent), `rule_meta_block` (thiếu đối tượng `meta`) và `rule_clean_csv` (thiếu `workspace/clean.csv`). Đây là nhóm E theo GUIDE, với `detail` bắt đầu bằng `RULE:`; quy ước không có trong đề. Giữ nguyên kết quả baseline để dùng tiếp ở Phần 2 và làm dữ liệu đầu vào cho curator ở Phần 3.

**Checkpoint Phần 1 đã đạt:** cài đặt đủ 1.1–1.3, các test đạt, có một baseline thật hợp lệ. Theo GUIDE, không cần chạy lại `baseline/data-learn` ở Phần 2.

- Thử thách mở rộng: chưa thực hiện.
