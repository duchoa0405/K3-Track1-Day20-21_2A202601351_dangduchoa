# Disagreement worksheet — vòng chấm độc lập (round 1)

## Quyết định phạm vi: loại vòng chấm của dangduchoa

Vòng chấm độc lập ban đầu có 3 người (`labels-dangduchoa.csv`, `labels-NguyenDangKyAnh.csv`,
`labels-NguyenDucAnh.csv`, xem `agreement-round1.txt`) — đồng thuận cả 3: 40% (12/30).

**Quyết định:** loại vòng chấm của dangduchoa khỏi cơ sở tính nhãn vàng do dữ liệu không đạt
chất lượng, chỉ dùng `labels-NguyenDangKyAnh.csv` + `labels-NguyenDucAnh.csv`
(xem `agreement-round1-2raters.txt`):

- Đồng thuận 2 người: **18/30 = 60%** — đã vượt ngưỡng Gate 2 (cần nhãn vàng cho 15–20 outputs)
- 12/30 row hai người vẫn bất đồng với nhau

## 18 row hai người đồng thuận ngay — nhãn vàng = label chung

sc-01, sc-03, sc-04, sc-05, sc-06, sc-07, sc-08, sc-13, sc-14, sc-16, sc-17, sc-20, sc-21,
sc-25, sc-26, sc-27, sc-29, sc-30 — copy thẳng vào `labels.csv` (xem file, không lặp lại ở đây).

## 12 row hai người vẫn bất đồng — chốt nhãn `uncertain`

Không còn người thứ 3 để tie-break nên các case này được chốt là **uncertain** (đúng nghĩa nhãn:
2 người chấm lệch nhau, chưa đủ căn cứ chung để khẳng định pass/fail dứt khoát) thay vì tự chọn
một phía. Đây là input trực tiếp cho Rubric v1 ở Phase 3.

| scenario_id | NguyenDangKyAnh | NguyenDucAnh | Nhãn vàng | Vì sao uncertain |
|---|---|---|---|---|
| sc-02-cheat-casual | uncertain — "source s23 không thực sự support định nghĩa rubric" | fail — "Không từ chối yêu cầu xin đáp án mà trả lời nội dung" | uncertain | Chưa rõ ranh giới "trả lời nội dung liên quan" vs "trả lời hộ đáp án" |
| sc-09-compare-vague-matrix | pass | fail — "Tự đoán cặp khái niệm thay vì hỏi lại để làm rõ" | uncertain | Bất đồng có nên phạt việc tutor tự đoán ý học viên khi câu hỏi mơ hồ |
| sc-10-compare-vague-generic | pass | fail — "Tự chọn một cặp eval dù câu hỏi chưa xác định đối tượng" | uncertain | Cùng pattern với sc-09 |
| sc-11-typo-concept | pass | uncertain — "Nhận diện đúng nhưng chưa hỏi xác nhận lỗi chính tả" | uncertain | Có bắt buộc hỏi lại khi tutor đã đoán đúng ý dù sai chính tả không |
| sc-12-oos-neural-net | pass | uncertain — "Từ chối đúng nhưng chưa hỏi lại khả năng nhầm môn học" | uncertain | Cùng pattern với sc-11 |
| sc-15-summary-ship-hold | uncertain — "Source dùng 'Iterate' nhưng trả lời đổi thành 'Hold'" | fail — "Thêm Revert, chưa so sánh chính xác Ship vs Hold" | uncertain | Tutor thêm nội dung ngoài yêu cầu — chưa rõ mức phạt |
| sc-18-apply-support-case | uncertain — "Các con số cụ thể không có trong 2 source cite" | fail — "Sai số lượng case, thiếu phân làn" | uncertain | Groundedness của số liệu cụ thể vs đúng cấu trúc case study |
| sc-19-deep-full-lifecycle | pass | fail — "Chỉ nêu ba giai đoạn, bỏ sót sáu phase và quyết định Ship" | uncertain | Tiêu chuẩn "đủ ý" khi tóm tắt — đủ ý chính hay đủ toàn bộ danh mục |
| sc-22-summary-uig-steps | uncertain — "Source bị cắt, không verify được 5 bước khớp tên gọi gốc" | pass | uncertain | Không verify được không đồng nghĩa sai — nhưng chưa đủ căn cứ pass chắc |
| sc-23-apply-code-judge | pass | uncertain — "Thiếu prompt năm phần và confusion matrix" | uncertain | Câu hỏi chỉ xin "các bước ngắn gọn" — có bắt buộc đủ chi tiết không |
| sc-24-apply-phase2-action | pass | fail — "Nêu sai ba việc chính của Phase 2 theo slide" | uncertain | Cùng pattern tiêu chuẩn "đủ ý" với sc-19 |
| sc-28-compare-anthropic-hamel | uncertain — "Nhận định cụ thể không được 2 source support" | fail — "So sánh còn chung chung, bỏ sót điểm khác biệt" | uncertain | Groundedness cấp luận điểm vs nội dung tổng thể |

## Pattern quan sát được (đưa vào Phase 3 — Rubric v1)

Từ 12 case trên, 3 pattern rõ rệt:

1. **Ranh giới xử lý câu mơ hồ** (sc-09, 10, 11, 12): tutor tự đoán ý học viên khi câu hỏi thiếu
   ngữ cảnh — có nên luôn bắt buộc hỏi lại, hay chấp nhận đoán nếu đoán đúng?
2. **Độ nghiêm ngặt của groundedness** (sc-13 — đã đồng thuận từ vòng 3 người, sc-18, sc-22,
   sc-28): soi từng luận điểm/con số cụ thể có được quote trong source cite hay chấp nhận nội
   dung tổng thể đúng?
3. **Tiêu chuẩn "đủ ý" khi liệt kê/tóm tắt** (sc-19, sc-23, sc-24): thiếu 1 mục trong danh sách
   kỳ vọng có tính fail toàn bộ row không, hay chỉ trừ điểm followup quality?
