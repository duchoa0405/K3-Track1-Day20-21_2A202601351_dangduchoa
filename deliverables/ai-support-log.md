# AI Support Log

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

## Nguyễn Đặng Kỳ Anh

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | Phase 1 — paraphrase | Sinh 2 biến thể câu hỏi tự nhiên cho mỗi combination đã khoá sẵn (dimensions/values/combinations do người tự chọn trước, AI chỉ diễn đạt lại thành câu hỏi) | Lọc tay từng câu theo Keep/Rewrite/Reject; loại 4 câu AI tự thêm ngữ cảnh làm bài test dễ đi, sửa lại 3 câu để giữ tính cộc lốc/thiếu ngữ cảnh |
| 2 | Phase 2 — sửa lỗi kỹ thuật | Chẩn đoán và vá lỗi mojibake (thiếu BOM UTF-8) trong `exportCsv()` của `report.py`; đọc lại 10 note tiếng Việt bị vỡ dấu bằng phân tích byte-level | Tự chạy lại `tests/test_eval_kit.py` (44 pass) sau mỗi lần vá; đối chiếu file khôi phục với chính nội dung đã chấm để không đổi nghĩa |
| 3 | Phase 2 — tính agreement | Chạy `agreement.py`, tổng hợp bảng 18 case bất đồng, rút 3 pattern từ cột note | Đối chiếu số liệu bằng cách chạy lại `agreement.py` nhiều lần với các tổ hợp rater khác nhau (3 người, rồi 2 người sau khi loại 1 vòng chấm) — số khớp cả 2 lần chạy |
| 4 | Phase 3 — soạn nháp Rubric v1 & Routing Map | Viết 6 tiêu chí rubric bám theo 3 pattern bất đồng thật; đề xuất routing 4 làn kèm lý do | Đối chiếu từng tiêu chí với `code_checks.py`/`judge_prompt.md` thật đang có trong repo, không bịa tiêu chí không kiểm chứng được |
| 5 | Phase 4 — code checks & calibrate judge | Viết thêm 2 code check (`scope_matches_expected`, `followup_count`); soạn 2 vòng judge prompt cho groundedness và follow-up quality | Chạy thật `code_checks.py`/`judge.py` trên `results.jsonl` + `labels.csv`, đọc tay `raw_content` của từng case lệch trước khi kết luận nguyên nhân (vd phân biệt "slide nhiều cột" với "gắn nhầm section") |
| 6 | Phase 5–6 — đọc slice, viết verdict | Tổng hợp scorecard, đọc 3 trace fail, soạn nháp report 5 phần | Xác minh lại bằng script riêng (đếm chính xác 7/9 case `high_risk` pass trước khi ghi vào report) thay vì tin số AI tóm tắt |

### AI sai, hời hợt hoặc làm mất coverage ở đâu?
- Ở Phase 4, AI ban đầu định gộp nhiều thay đổi vào 1 vòng sửa judge prompt (vi phạm "sửa 1 thứ
  mỗi vòng") — đã tự nhận và ghi rõ trong REPORT.md mục 5 thay vì che giấu.
- Nhận diện sai một chỗ: từng cho rằng "cả 6 tiêu chí đều đã có trong system prompt" (spec không
  thiếu) trước khi grep thật vào `tutor.py` — sau khi kiểm chứng mới phát hiện tiêu chí 3 (xử lý
  câu mơ hồ) thực ra là spec gap thật, phải sửa lại kết luận trong REPORT.md mục 4.

### Tôi đã tự sửa hoặc quyết định lại điều gì?
- Quyết định loại vòng chấm nhãn của Đặng Đức Hòa khỏi cơ sở tính nhãn vàng vì đánh giá chất
  lượng chấm chưa đạt (nhiều note không khớp label, xem `evidence/labels-dangduchoa.csv`) —
  quyết định này của người, không phải AI đề xuất; AI chỉ tính lại agreement trên 2 người còn lại
  sau khi có quyết định.
- Quyết định threshold "0 case out-of-scope bị trả lời như in-scope" là zero-tolerance, không cho
  trade-off dù các gate khác đều đạt — dẫn tới verdict HOLD dù phần lớn chỉ số khác đều xanh.
