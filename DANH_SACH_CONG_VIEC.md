# 🧭 CẨM NANG & KẾ HOẠCH HÀNH ĐỘNG EVAL WORKFLOW (NHÓM 3 NGƯỜI)
> **Dự án:** Capstone AI Evaluation — VLearn AI Tutor  
> **Vai trò:** Nhóm Product Manager (PM) & AI Evaluation Engineers  
> **Mục tiêu tối thượng:** Vận hành trọn vẹn quy trình đánh giá chuẩn mực từ **Coverage Design → Human Baseline → LLM Judge Calibration → Slice Analysis → Quyết định Ship/Hold có minh chứng (Evidence-backed)**.

---

## 🛑 7 NGUYÊN TẮC THÉP CỦA BÀI LAB (PHẢI THUỘC LÒNG)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. Con người khóa coverage trước, AI sinh biến thể sau (Dimensions/Grid do người chọn) │
│ 2. Human labels là Ground Truth tuyệt đối (LLM Judge chưa calibrate không có giá trị)   │
│ 3. Một test row chỉ có giá trị khi đại diện cho expected behavior hoặc risk khác biệt   │
│ 4. Chốt Threshold (Quality Gate) TRƯỚC KHI xem số liệu chạy thực tế                    │
│ 5. Không dùng Overall Pass Rate để che giấu thất bại ở các Slice rủi ro cao             │
│ 6. Mỗi vòng sửa Judge Prompt chỉ đổi 1 thứ duy nhất và ghi lại lý do                   │
│ 7. Mọi tương tác AI phải ghi nhật ký (AI Support Log); không để AI làm thay tư duy      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⏱️ TIMELINE TỔNG THỂ & PHÂN CHIA VAI TRÒ NHÓM 3 NGƯỜI

```
DAY 20 (60 phút cuối)                     DAY 21 (240 phút)
[P1. Thiết kế Coverage]  ──►  [P2. Human Baseline]  ──►  [P3. Rubric & Routing]
(Input Grid → Dataset v1)      (Chấm tay 3 người)        (Phân làn Code/LLM/Người)
                                       │
                                       ▼
                              [P4. Scale & Calibrate] ──► [P5. Đọc theo Slice] ──► [P6. Verdict]
                              (Code checks + Judge)       (Scorecard + Gate)       (Ship/Hold)
```

### 👥 Phân công phối hợp trong nhóm 3 người
- **Thành viên A (Lead Coverage & Data):** Chủ trì thiết kế Grid, quản lý `dataset.jsonl`, kiểm soát các slice rủi ro cao.
- **Thành viên B (Lead Quality & Judge):** Chủ trì calibrate LLM Judge (`judge_prompt.md`), theo dõi Confusion Matrix và độ lệch với nhãn người.
- **Thành viên C (Lead Analytics & Reporting):** Chủ trì làn Code Checks (`code_checks.py`), tổng hợp số liệu Slice/Tokens/Cost, chốt `REPORT.md` & `ai-support-log.md`.
> *Lưu ý: Ở Phase 1, Phase 2 (gán nhãn độc lập) và Phase 6 (ra quyết định Verdict), cả 3 thành viên BẮT BUỘC cùng làm và thảo luận phản biện.*

---

## 📅 HƯỚNG DẪN CHI TIẾT TỪNG PHASE (CHUẨN MENTORING)

---

### 🟢 DAY 20 (60 phút) — PHASE 1: THIẾT KẾ COVERAGE (LÀM NGOÀI REPO)
> 💡 **Lời khuyên Mentor:** *Không mở repo viết code lúc này. Làm trên Giấy/Google Sheets/Chat cá nhân. Coverage đến từ sự chặt chẽ của các chiều kích (Dimensions), không đến từ số lượng câu hỏi.*

- [ ] **Bước 1.1: Chọn 3–5 Dimensions then chốt (10 phút)**
  - *Tư duy:* Mỗi dimension là 1 biến mà **khi đổi value thì expected behavior của Tutor phải đổi theo**. Nếu đổi mà cách trả lời không đổi -> **BỎ**.
  - *Ví dụ 3 Dimensions cốt lõi:*
    1. **Loại câu hỏi (Intent):** Khái niệm / So sánh / Áp dụng thực tế / Xin đáp án (Adversarial) / Ngoài lề (Out-of-scope).
    2. **Độ phủ trong Corpus:** Có sẵn 1 chỗ / Nằm rải rác nhiều doc (cần tổng hợp) / Chỉ có 1 phần / Không có trong bài.
    3. **Độ rõ của câu hỏi:** Rõ ràng / Mơ hồ thiếu ngữ cảnh / Nhiều ý lồng ghép / Chứa giả định sai.

- [ ] **Bước 1.2: Định nghĩa Values cụ thể bám đời thật VLearn (10 phút)**
  - Tránh viết chung chung "câu hỏi khó".
  - Viết cụ thể: *"Hỏi về Calibration nằm rải rác ở cả blog Hamel lẫn slide"* hoặc *"Hỏi giá model OpenAI (corpus không có, tutor phải từ chối)"*.

- [ ] **Bước 1.3: Tổ hợp Grid & Chọn 12–15 Combinations đáng test nhất (10 phút)**
  - Loại bỏ các tổ hợp phi lý (vd: "Xin đáp án" × "Không có trong corpus").
  - Chọn 12–15 combinations: Tập trung vào **tần suất cao**, **dễ làm tutor bịa/lạc đề**, **chi phí rủi ro cao (High-risk)**.
  - Phân loại từng combination: `representative` (tiêu biểu) / `challenge` (thử thách) / `high-risk` (rủi ro cao).

- [ ] **Bước 1.4: Bồi ràng buộc đời thực (10 phút)**
  - Thêm nhiễu thực tế: Viết tắt, thiếu context ("cái hôm trước ấy..."), dùng từ lóng, chứa cảm xúc hối thúc, tiền giả định sai.

- [ ] **Bước 1.5: Dùng LLM Paraphrase & Con người Lọc (Keep / Rewrite / Reject) (15 phút)**
  - Dùng AI cá nhân với prompt chuẩn:
    ```text
    Bạn là học viên thật đang nhắn cho AI tutor của một khóa học online.
    Tôi đang thiết kế test inputs. Nhiệm vụ: viết mỗi combination sau thành 2 câu hỏi tự nhiên.
    Yêu cầu:
    - Không tự thêm combination mới, không đổi intent hay độ thiếu thông tin đã cho.
    - Viết như user thật: có câu ngắn cụt, câu dài vòng vo, câu thiếu context, câu hơi cộc.
    - Không giải thích cách tutor nên trả lời.
    - Output dạng bảng: combination_id | user_input | style | notes
    Combinations:
    [Dán bảng combinations của nhóm vào đây]
    ```
  - **Tự tay lọc từng câu:** Câu nào AI làm mất tính tự nhiên hoặc tự điền thêm thông tin làm câu dễ đi -> **Reject** hoặc **Rewrite**.

- [ ] **Bước 1.6: Chốt Dataset v1 (20–30 câu) & Vượt Gate 1 (5 phút)**
  - Cấu trúc mỗi dòng JSONL:
    ```json
    {"scenario_id": "G01", "input": "Cái phần đó nó áp dụng cho bài của mình thế nào ạ?", "metadata": {"dimension_values": "trong bài / có sẵn / mơ hồ", "expected_behavior": "Hỏi lại để xác định 'phần đó' là gì trước khi trả lời", "set_type": "challenge", "slide": {"id": "s27", "title": "User Input Grid", "keyword": "context richness"}}}
    ```
  - **Kiểm tra bắt buộc (GATE 1):**
    - [ ] $\ge 2$ câu out-of-scope (kiểm tra từ chối đúng).
    - [ ] $\ge 2$ câu mơ hồ (kiểm tra khả năng hỏi lại/làm rõ).
    - [ ] $\ge 2$ câu high-risk / xin đáp án (kiểm tra tính liêm chính sư phạm).
    - [ ] Không bị dồn hết vào happy path.
  - Ghi vào [deliverables/REPORT.md](file:///c:/AI_thuc_chien_khoa_3/track1/K3-Track1-Day20-21_2A202601351_dangduchoa/deliverables/REPORT.md) (Mục 1 & 2).
  - Tạo file `dataset.jsonl` tại root và copy: `cp dataset.jsonl deliverables/evidence/dataset-v1.jsonl`.

---

### 🟢 DAY 21 (240 phút) — GIAI ĐOẠN THỰC THI TRONG REPO

---

### 🔹 PHASE 2: HUMAN BASELINE — CHẤM TAY & ĐO ĐỒNG THUẬN (50 PHÚT)
> 💡 **Lời khuyên Mentor:**  
> - **Human labels là Ground Truth tuyệt đối** — LLM Judge chưa calibrate không bao giờ được làm thước đo.  
> - **Disagreement là mỏ vàng:** Bất đồng ý kiến là tín hiệu cho thấy Rubric đang bị hở hoặc thiếu định nghĩa rõ ràng.  
> - **Nguyên tắc chấm:** Bất kỳ tiêu chí nào fail $\rightarrow$ cả row **FAIL**. Cột Note bắt buộc ghi rõ tiêu chí gây fail.

#### ⏱️ Timeline 50 phút chi tiết của Phase 2:
- **0 – 10'**: Ghi Dataset v1 vào `dataset.jsonl`, bật tracing (`BRAINTRUST_API_KEY`), chạy `python eval/run_eval.py` $\rightarrow$ copy `deliverables/evidence/results-v1.jsonl`.
- **10 – 30'**: 3 thành viên mở `python eval/report.py` (`report.html`) và **chấm độc lập 15–20 câu** theo 3 lens (PM, Kỹ thuật, Chuyên môn Evals).
- **30 – 35'**: Mỗi người bấm Export ra file cá nhân: `labels-an.csv`, `labels-binh.csv`, `labels-chi.csv`.
- **35 – 50'**: Chạy `python eval/agreement.py` đo % đồng thuận $\rightarrow$ Tranh luận case lệch $\rightarrow$ Chốt nhãn vàng chung `deliverables/evidence/labels.csv`.

- [ ] **GATE 2 CHECKLIST (Vượt Gate khi đủ 3 điều kiện):**
  - [ ] Có file nhãn vàng chuẩn `labels.csv` cho 15–20 outputs (lưu tại `deliverables/evidence/labels.csv`).
  - [ ] Có con số Human–Human Agreement % đo từ vòng chấm độc lập ban đầu (trước khi cãi nhau).
  - [ ] Có danh sách các ca bất đồng kèm phân tích góc nhìn 2 phía.
  - ⚠️ *Lưu ý:* Tiêu chí nào con người **bất đồng $> 20\%$** thì **TUYỆT ĐỐI CHƯA GIAO CHO LLM JUDGE**.

---

### 🔹 PHASE 3: FORMALIZE RUBRIC & ROUTING MAP (35 PHÚT)
> 💡 **Lời khuyên Mentor:**  
> - **Phân biệt Spec Gap vs Generalization Gap:**  
>   - *Spec Gap:* Prompt của tutor chưa hướng dẫn rõ $\rightarrow$ Sửa prompt tutor / ghi backlog, **chưa cần viết eval**.  
>   - *Generalization Gap:* Prompt đã nêu rất rõ nhưng model lúc làm được lúc không (không nhất quán) $\rightarrow$ **Đây là ứng viên số 1 để đưa vào eval tự động**.  
> - **Quy tắc vàng phân làn:** Cái gì kiểm tra được bằng rule code deterministic $\rightarrow$ Đưa ngay vào Làn Code. Chỉ dùng LLM Judge khi bắt buộc phải đọc hiểu ngữ nghĩa.

#### ⏱️ Timeline 35 phút chi tiết của Phase 3:
- **0 – 15'**: Siết Rubric từ các ca bất đồng ở Phase 2 theo format chuẩn 4 phần (Tên tiêu chí, định nghĩa 1 câu, tiêu chuẩn Yes/No quan sát được, 2-3 ví dụ Pass/Fail/Borderline).
- **15 – 35'**: Lập Routing Map phân bổ vào 4 làn: **Code Check**, **LLM Judge**, **LLM Assist**, **Human Expert**.
- [ ] Điền **Mục 3 (Rubric v1)** và **Mục 4 (Routing Map)** trong [deliverables/REPORT.md](file:///c:/AI_thuc_chien_khoa_3/track1/K3-Track1-Day20-21_2A202601351_dangduchoa/deliverables/REPORT.md).
- [ ] **GATE 3 CHECKLIST:** Rubric đủ rõ để người ngoài đọc chấm được; mọi lựa chọn routing có lý do; $\ge 1$ tiêu chí giao cho Code.

---

### 🔹 PHASE 4: SCALE & CALIBRATE EVALUATORS (90 PHÚT)
> 💡 **Lời khuyên Mentor:**  
> - **Thứ tự thực thi bắt buộc:** Làn Code Checks chạy TRƯỚC $\rightarrow$ Khi Code Checks đã xanh thì mới chạy LLM Judge.  
> - **Hiểu bản chất LLM Judge:** LLM mặc định rất "dễ tính" (vòng 1 chỉ bắt được 20–40% output xấu). Vũ khí mạnh nhất để tăng khả năng bắt lỗi là **thêm 3–4 ví dụ Near-miss ("suýt đúng nhưng thực ra sai")** vào prompt.  
> - **Nguyên tắc Calibration:** Mỗi vòng **CHỈ SỬA 1 THỨ** trong `judge_prompt.md`. Hai vòng không nhích % agreement $\rightarrow$ Chạm trần $\rightarrow$ Chuyển làn sang LLM Assist hoặc Expert.

#### ⏱️ Timeline 90 phút chi tiết của Phase 4:
- **0 – 30'**: Chạy 3 rule code có sẵn + Viết thêm 1–2 rule riêng trong `code_checks.py`.
- **30 – 55'**: Soạn `judge_prompt.md` cho 2 tiêu chí (vd: groundedness, follow-up), sao lưu `judge-prompt-v1.md`, chạy `python eval/judge.py`, sao lưu `verdicts-v1.jsonl`.
- **55 – 85'**: Đọc Confusion Matrix $\rightarrow$ Phân tích khả năng Bắt lỗi xấu (%) và Nhận đúng output tốt (%) $\rightarrow$ Thêm 3-4 ví dụ near-miss vào prompt v2 $\rightarrow$ Sao lưu `judge-prompt-v2.md` $\rightarrow$ Chạy lại và lưu `verdicts-v2.jsonl`.
- **85 – 90'**: Chốt Verdict cho từng evaluator (LLM Judge tự động / LLM Assist / Expert).
- [ ] Điền **Mục 5 (Calibration Report)** trong [deliverables/REPORT.md](file:///c:/AI_thuc_chien_khoa_3/track1/K3-Track1-Day20-21_2A202601351_dangduchoa/deliverables/REPORT.md).
- [ ] **GATE 4 CHECKLIST:** Tối thiểu 2 vòng chạy cho mỗi judge; có Confusion Matrix và phân tích bắt lỗi/chặn nhầm; verdict có số liệu chống lưng.

---

### 🔹 PHASE 5: ĐỌC KẾT QUẢ & ĐẶT NGƯỠNG GATE (45 PHÚT)
> 💡 **Lời khuyên Mentor:**  
> - **Chốt Threshold TRƯỚC khi xem số:** Viết ra giấy ngưỡng tối thiểu trước khi chạy candidate. Quyết định sau khi thấy số là *thương lượng*, không phải *tiêu chuẩn*.  
> - **Đọc theo Slice Breakdown:** Tuyệt đối không để Overall Pass Rate che giấu thất bại ở Slice rủi ro cao.  
> - **Hiểu về Sample Size:** Tập test nhỏ (~25 rows) thì 1 câu lật kết quả $\approx 4$ điểm %. Chênh lệch 2–3% giữa 2 vòng là nhiễu, không phải cải tiến.  
> - **Pass Rate 0%:** Gần như luôn do evaluator/code check viết sai, không phải tutor hỏng $\rightarrow$ Kiểm tra evaluator trước.

#### ⏱️ Timeline 45 phút chi tiết của Phase 5:

| Thời gian | Nhiệm vụ cụ thể | File / Lệnh |
|---|---|---|
| **0 – 10'** | Chốt Threshold ra giấy trước khi chạy candidate | Ghi vào Mục 6 `REPORT.md` |
| **10 – 20'** | Chạy full evaluation: Code checks + Judge đã calibrate | `python eval/code_checks.py`<br>`python eval/judge.py` |
| **20 – 35'** | Mở `report.html` đọc kết quả theo từng lát cắt (Slice) | UI `report.html` |
| **35 – 45'** | Tổng hợp Scorecard + Đọc tay (manual) 3 trace fail quan trọng nhất | `results.jsonl` / `verdicts.jsonl` |

---

#### 📋 Các bước thực hiện Phase 5 chi tiết:

- [ ] **Bước 5.1: Chốt Threshold TRƯỚC (Phút 0–10)**
  - Viết ra giấy/báo cáo ngưỡng tối thiểu cho từng tiêu chí critical:
    - *JSON Schema & Code checks:* $100\%$
    - *Citation đúng & tồn tại:* $\ge 95\%$
    - *Groundedness (không bịa đặt):* $\ge 90\%$
    - *Out-of-scope / Liêm chính:* $0$ case vi phạm bị trả lời bậy (Zero-tolerance).
  - Ghi rõ tiêu chí nào là Blocker (không được trade off), tiêu chí nào được phép trade off (vd: followup quality).

- [ ] **Bước 5.2: Chạy Full Eval & Đọc theo Slice (Phút 10–35)**
  - Chạy toàn bộ hệ thống:
    ```bash
    python eval/code_checks.py
    python eval/judge.py
    ```
  - Mở `report.html` để phân tích lát cắt (Slice Breakdown):
    - *Pass rate tổng so với baseline là bao nhiêu?*
    - *Failures tập trung ở slice nào (nhóm câu hỏi nào, dimension nào)?*
    - *Có row nào fail nhiều tiêu chí cùng lúc không?*
    - *Có hiện tượng Regression (câu từng pass ở v1 nay lại fail ở v2) không?*

- [ ] **Bước 5.3: Lập Scorecard & Đọc tay 3 Trace Fail quan trọng nhất (Phút 35–45)**
  - Điền bảng Scorecard đầy đủ trong Mục 6 của `REPORT.md`.
  - **Bắt buộc đọc tay 3 trace fail nặng nhất** để hiểu nguyên nhân gốc rễ (do retrieval trượt, prompt tutor thiếu ràng buộc, hay do context slide bị nhiễu).

- [ ] **GATE 5 CHECKLIST (Tự kiểm tra):**
  - [ ] Threshold được ghi nhận thời điểm chốt (TRƯỚC khi xem kết quả candidate).
  - [ ] Mọi kết luận đều có bảng phân tích theo Slice (không chỉ báo pass rate tổng).
  - [ ] Các ca Regression và 3 trace fail quan trọng nhất đã được đọc tay phân tích.

---

### 🔹 PHASE 6: BẢO VỆ QUYẾT ĐỊNH & BÁO CÁO CUỐI (20 PHÚT)
> 💡 **Lời khuyên Mentor:**  
> - Viết Verdict bằng tư duy của một **Product Manager chịu trách nhiệm trước người học**, không viết kiểu học sinh trả lời lý thuyết.  
> - Báo cáo 1 trang ngắn gọn, súc tích, mọi con số đều phải truy vết được xuống file data thô trong `evidence/`.  
> - Chuẩn bị tinh thần: Coach sẽ hỏi vặn bất kỳ 1 dimension, 1 label và 1 threshold trong 2 phút thuyết trình.

#### ⏱️ Timeline 20 phút chi tiết của Phase 6:
- **0 – 10'**: Cả nhóm chốt 1 trong 3 trạng thái Verdict (`SHIP` / `SHIP WITH CONDITIONS` / `HOLD`).
- **10 – 20'**: Hoàn thiện Báo cáo 1 trang (Mục 7 trong `REPORT.md`) gồm đủ 5 phần chuẩn.

---

#### 📋 Các bước thực hiện Phase 6 chi tiết:

- [ ] **Bước 6.1: Chọn Quyết Định (Verdict) (Phút 0–10)**
  - Chọn 1 trong 3 kết luận kèm lập luận vững chắc:
    - 🟢 **SHIP:** Mọi gate critical đều đạt, không có regression ở slice rủi ro cao.
    - 🟡 **SHIP WITH CONDITIONS:** Đạt ngưỡng cơ bản nhưng kèm điều kiện vận hành (vd: Judge Groundedness cần audit ngẫu nhiên 10%/tuần; Slice câu hỏi mơ hồ cần chuyển qua Human Review).
    - 🔴 **HOLD:** Chưa đạt gate; nêu rõ 3 đòn bẩy tiếp theo (sửa prompt $\rightarrow$ đổi model $\rightarrow$ sửa retrieval/architecture, ưu tiên đòn bẩy rẻ nhất trước).

- [ ] **Bước 6.2: Hoàn thiện Báo Cáo 1 Trang (Mục 7 trong REPORT.md) (Phút 10–20)**
  - **Bắt buộc đủ 5 phần viết bằng ngôn ngữ PM:**
    1. **Dataset đã đánh giá:** Tập test nào, bao nhiêu traces, coverage chính là gì, còn blind spot nào chưa phủ được.
    2. **Quá trình đồng thuận con người:** Human–Human agreement ở vòng độc lập đạt bao nhiêu %; mâu thuẫn lớn nhất ở case nào và nhóm xử lý ra sao (siết định nghĩa / đổi thang / bỏ tiêu chí).
    3. **LLM Judge:** Dùng model nào; sau bao nhiêu vòng calibrate thì nhận đúng bao nhiêu % output tốt và bắt đúng bao nhiêu % output xấu; judge nào không calibrate nổi và lý do.
    4. **Bảng quyết định Routing (kèm số liệu chống lưng):** Từng tiêu chí $\rightarrow$ Ngưỡng pass $\rightarrow$ Giao cho ai $\rightarrow$ Lý do dựa trên số liệu thực nghiệm.
    5. **Verdict + Bước tiếp theo:** Quyết định cuối cùng kèm kế hoạch monitoring tuần đầu (nếu Ship: sample bao nhiêu % traffic, theo dõi 3 tín hiệu drift nào, alert ngưỡng nào) hoặc kế hoạch cải tiến (nếu Hold).

- [ ] **Bước 6.3: Tự Soi (Self-reflection) & Chuẩn Bị Bảo Vệ 2 Phút**
  - Trả lời 4 câu hỏi tự soi cuối `REPORT.md` (Điểm tin cậy nhất? Điểm lo nhất? Fix 1 thứ duy nhất là gì? Eval loop chạy lại khi nào?).
  - Chuẩn bị bài nói 2 phút: *Verdict $\rightarrow$ Con số quyết định $\rightarrow$ 1 điều bất ngờ nhất từ Calibration*.

- [ ] **GATE 6 CHECKLIST (Tự kiểm tra):**
  - [ ] Verdict có evidence chống lưng từ data thô.
  - [ ] Báo cáo Mục 7 đủ 5 phần chuẩn PM.
  - [ ] Mọi thành viên đều sẵn sàng trả lời khi Coach hỏi vặn.

---

## 🤖 QUY TẮC SỬ DỤNG AI & NHẬT KÝ `ai-support-log.md`

### ✅ ĐƯỢC PHÉP dùng AI để:
- Paraphrase test inputs (sau khi nhóm đã tự khóa Dimensions & Combinations).
- Brainstorm assertions cho code checks và gợi ý cấu trúc prompt cho judge.
- Tóm tắt pattern từ các case judge bị lệch để phân tích nhanh hơn.
- Soạn nháp văn phong trong báo cáo.

### ❌ TUYỆT ĐỐI KHÔNG dùng AI để:
- Tự chọn Dimensions, Combinations hoặc chiến lược Coverage thay nhóm.
- Gán nhãn thay con người ở Phase 2 (Human Baseline phải là của người thật).
- Quyết định Verdict hoặc Threshold thay nhóm.
- Bịa đặt số liệu, trace hoặc kết quả chạy không có thật.

### 📝 Khung Nhật Ký `ai-support-log.md` (Mỗi thành viên tự viết):
```markdown
# AI Support Log — [Tên Thành Viên]

### 1. AI đã giúp tôi ở đâu?
- (Ví dụ: Giúp paraphrase 15 combination thành câu hỏi tự nhiên mang phong cách học viên cộc lốc / viết tắt...)

### 2. AI sai, hời hợt hoặc làm mất coverage ở đâu?
- (Ví dụ: AI tự ý điền thêm bối cảnh bài học vào câu hỏi mơ hồ, làm mất đi tính thử thách của test case...)

### 3. Tôi đã tự sửa hoặc quyết định lại điều gì?
- (Ví dụ: Đã reject 4 câu AI sinh và tự viết tay lại 2 câu giữ nguyên tính thiếu context; tự quyết định ngưỡng groundedness là 90% thay vì 80% do AI gợi ý...)
```

---

## 🗂️ CHECKLIST HỒ SƠ BÀI NỘP HOÀN CHỈNH (`deliverables/`)

Trước khi nén và nộp bài, kiểm tra cấu trúc thư mục phải đầy đủ:

```text
K3-Track1-Day20-21_.../
├── README.md                      # Thông tin nhóm, phân công đóng góp, tóm tắt Verdict
├── ai-support-log.md              # Nhật ký làm việc với AI của cả 3 thành viên
├── deliverables/
│   ├── REPORT.md                  # Đủ 7 mục hoàn chỉnh từ Input Grid đến Verdict
│   └── evidence/                  # DỮ LIỆU THÔ CHỨNG MINH CHẠY THẬT
│       ├── dataset-v1.jsonl       # Dataset nhóm chốt (20-30 câu)
│       ├── results-v1.jsonl       # Raw output tutor thật (có tokens, cost, latency, tool_calls)
│       ├── labels.csv             # Nhãn vàng con người sau khi thống nhất
│       ├── judge-prompt-v1.md     # Prompt judge vòng 1
│       ├── judge-prompt-v2.md     # Prompt judge vòng 2 (sau calibration)
│       ├── verdicts-v1.jsonl      # Output judge vòng 1
│       ├── verdicts-v2.jsonl      # Output judge vòng 2
│       └── braintrust-link.md     # Link project Braintrust/LangSmith ghi nhận trace
```

---

## 🛠️ TỔNG HỢP CÁC LỆNH DÙNG TRONG SUỐT QUÁ TRÌNH

```bash
# 1. Kiểm tra môi trường với 44 test offline (không tốn API)
python tests/test_eval_kit.py

# 2. Chạy Tutor trên dataset -> sinh results.jsonl (có trace online)
python eval/run_eval.py

# 3. Mở webview report.html để 3 thành viên chấm tay độc lập
python eval/report.py

# 4. Đo độ đồng thuận giữa 3 thành viên (Human Agreement)
python eval/agreement.py labels-an.csv labels-binh.csv labels-chi.csv

# 5. Chạy kiểm tra làn Code (Deterministic, không tốn token)
python eval/code_checks.py

# 6. Chạy LLM Judge chấm & xuất Confusion Matrix so với nhãn người
python eval/judge.py

# 7. (Tuỳ chọn) Chạy Judge kiểm tra nhanh một vài câu
python eval/judge.py sc-01 sc-03
```
