# AI Support Log

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

## Đặng Đức Hòa

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | Phase 1 — Sinh biến thể câu hỏi (Paraphrase) | Dùng AI sinh biến thể câu hỏi tự nhiên cho 12 combinations đã chọn sẵn từ User Input Grid (giữ nguyên intent và coverage). | Cả nhóm họp duyệt thủ công từng câu theo nguyên tắc Keep/Rewrite/Reject; loại bỏ 4 câu AI tự ý thêm ngữ cảnh, viết lại 3 câu cộc lốc/gài giả định sai để tăng ma sát thực tế. |
| 2 | Phase 2 — Hỗ trợ kỹ thuật xuất nhãn (Export CSV) | Nhờ AI chẩn đoán và sửa lỗi encode UTF-8 BOM (`Uint8Array([0xEF, 0xBB, 0xBF])`) trong `eval/report.py` để file CSV mở trên Excel không bị lỗi font tiếng Việt. | Tải lại trang `report.html`, bấm Export `labels.csv` và mở trực tiếp trên Excel kiểm tra 30 dòng hiển thị tiếng Việt chuẩn xác 100%. |
| 3 | Phase 2 — Đo Agreement & Phân tích Disagreement | Nhờ AI chạy `eval/agreement.py` đo độ đồng thuận giữa 3 thành viên và tổng hợp danh sách các ca lệch ý kiến. | Đối chiếu trực tiếp các ca lệch trên giao diện web, cùng nhóm thảo luận nguyên nhân bất đồng (mơ hồ, groundedness, liệt kê thiếu ý). |
| 4 | Phase 3 — Thảo luận Rubric & Routing Map | Nhờ AI hỗ trợ format bảng Rubric 6 tiêu chí dựa trên 3 pattern bất đồng thực tế và lập bảng Routing 4 làn. | Kiểm tra đối chiếu xem từng tiêu chí có thể tự động hóa bằng Code/Judge hay phải giữ lại cho Expert review. |
| 5 | Phase 5 — Phân tích Slice & 3 Trace Fail | Nhờ AI tổng hợp scorecard theo từng slice (đặc biệt là slice `high_risk`) và bóc tách root cause của 3 trace fail (`sc-02`, `sc-04`, `sc-30`). | Đọc trực tiếp trường `raw_content` trong `results-v1.jsonl` để xác minh lỗi tutor bị lừa xin đáp án là có thật. |
| 6 | Phase 6 — Đề xuất đòn bẩy & Verdict | Nhờ AI gợi ý các đòn bẩy cải tiến theo thứ tự chi phí từ thấp đến cao (Prompt → Model → Architecture). | Cùng nhóm thống nhất chốt Verdict **HOLD** dựa trên bằng chứng vi phạm gate cứng liêm chính học thuật (không thỏa hiệp hạ threshold). |

### AI sai, hời hợt hoặc làm mất coverage ở đâu?
- Ở Phase 1, khi được yêu cầu sinh câu hỏi tự nhiên, AI có xu hướng tự ý bổ sung thêm thông tin bối cảnh giải thích, làm mất đi tính "cộc lốc, mơ hồ" của đời thực. Tôi và nhóm đã phải Reject 4 câu và Rewrite 3 câu để giữ nguyên tính thử thách cho bộ test.
- Khi phân tích câu mơ hồ (`sc-09`), AI Tutor tự suy diễn câu trả lời thay vì hỏi lại để làm rõ (Clarify) — bộc lộ rõ spec gap trong system prompt hiện tại.

### Tôi đã tự sửa hoặc quyết định lại điều gì?
- Tự nhận diện và đồng thuận cùng nhóm loại bỏ vòng chấm cá nhân ban đầu (`evidence/labels-dangduchoa.csv`) khỏi cơ sở tính nhãn vàng chung nhằm đảm bảo tính chuẩn xác và chất lượng cao nhất cho ground truth.
- Quyết định bảo vệ nguyên tắc Gate cứng: Không hạ threshold của tiêu chí `scope_matches_expected` xuống dưới 100% để "cho qua", kiên quyết giữ verdict HOLD vì an toàn sư phạm và liêm chính học thuật.
