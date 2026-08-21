# REPORT — Eval loop A→Z: VLearn AI Tutor

Report A→Z của eval loop — mỗi mục ứng một phase của bài lab. Mọi số liệu và quyết
định trong đây phải dẫn được xuống file data thô trong `evidence/` (dataset-v1.jsonl,
results-vN.jsonl, labels.csv, judge-prompt-vN.md, verdicts-vN.jsonl, braintrust-link.md).


---

## 1. Input Grid

> Lưới input = trục "ai hỏi" × "hỏi kiểu gì". LLM giúp sinh input, con người kiểm soát coverage.

### Phân tích Nhóm người dùng & Ý định (PM Analysis)
- **Nhóm người dùng mục tiêu:**
  1. *Học viên mới / Chuyển ngành:* Cần hiểu khái niệm cốt lõi, thích giải thích bằng ngôn ngữ bình dân, trực quan, không dùng thuật ngữ hàn lâm (jargon).
  2. *Học viên đang thực hành làm bài Lab:* Thường hỏi hối thúc, có xu hướng xin đáp án trực tiếp để nộp bài, hoặc hỏi gộp nhiều bài cùng lúc.
  3. *Học viên nâng cao / PM áp dụng vào doanh nghiệp:* Đào sâu so sánh đa tài liệu (Hamel vs Anthropic), hỏi workflow áp dụng thực tế nhiều bước (multi-step action).
- **Các ý định hỏi chính (Intent):**
  - `Khái niệm`: Yêu cầu định nghĩa, giải thích dễ hiểu hoặc tổng hợp từ nhiều nguồn.
  - `So sánh`: Đối chiếu 2 phương pháp (Code vs Judge, Ship vs Hold, Level evals).
  - `Áp dụng vào bài`: Hướng dẫn các bước thực thi cụ thể cho dự án riêng hoặc case study.
  - `Xin đáp án (Adversarial)`: Đòi giải bài tập hộ, bypass quy định liêm chính học thuật.
  - `Ngoài bài (Out-of-scope)`: Hỏi kiến thức kỹ thuật sâu (Attention, Claude 3.5), marketing, crypto ngoài corpus.
  - `Mơ hồ / Thiếu ngữ cảnh`: Câu hỏi để lại deixis ("cái này", "matrix hôm qua"), sai chính tả, giả định sai.
- **Đánh giá Rủi ro & Tần suất:**
  - **Ô rủi ro cao nhất (High-Risk):** Ô `[Học viên làm lab × Xin đáp án / Prompt Injection]` (nếu tutor giải hộ sẽ phá vỡ tính liêm chính sư phạm) và `[Ngoài bài × Không có trong corpus]` (nguy cơ tutor tự bịa đặt hallucination).
  - **Ô tần suất cao nhất (High-Frequency):** Ô `[Học viên mới × Khái niệm có sẵn]` và `[Học viên làm lab × Áp dụng thực tế]`.

### Lưới User Input Grid của nhóm (Đa chiều)

| Nhóm User \ Intent | Khái niệm | So sánh | Áp dụng vào bài | Xin đáp án (Adversarial) | Ngoài bài (Out-of-scope) | Mơ hồ / Deixis |
|---|---|---|---|---|---|---|
| **Học viên mới** | Giải thích đơn giản, ví dụ cấp 2 (`sc-13`, `sc-14`) | So sánh súc tích 3 gạch đầu dòng (`sc-15`, `sc-16`) | — | — | Teen code, hỏi bot crypto (`sc-08`) | Deixis ngắn phụ thuộc slide (`sc-26`) |
| **Học viên làm lab** | Nhận diện sai chính tả thuật ngữ (`sc-11`) | Đính chính giả định sai (`sc-27`) | Hỏi 3 bước liên hoàn áp dụng (`sc-17`) | Hối thúc xin đáp án, đòi gộp bài (`sc-01`–`sc-04`, `sc-25`) | — | Hỏi phiếm chỉ "matrix hôm qua" (`sc-09`, `sc-10`) |
| **Học viên nâng cao / PM** | Tổng hợp 6 phase toàn bộ lifecycle (`sc-19`, `sc-20`) | Đối chiếu đa tác giả Hamel vs Anthropic (`sc-28`) | Actionable steps code judge, Saturation rate (`sc-23`, `sc-30`) | — | Hỏi kỹ thuật sâu transformer, marketing công ty (`sc-05`, `sc-06`, `sc-07`) | Nhầm môn học khác (`sc-12`) |

### Bảng Combinations Giữ lại và Loại bỏ
- **Giữ lại (12 Combinations chính - 30 Scenarios):**
  - `High-Risk (4 combos)`:
    - **Combo 1:** *xin đáp án × có sẵn × rõ × hỏi bình thường* (`sc-01`, `sc-02`, `sc-25`)
    - **Combo 2:** *xin đáp án × rải rác nhiều tài liệu × nhiều ý trong một câu × tóm tắt* (`sc-03`, `sc-04`)
    - **Combo 3:** *ngoài bài × không có × rõ × giải thích chi tiết* (`sc-05`, `sc-06`)
    - **Combo 4:** *ngoài bài × không có × mơ hồ × giải thích đơn giản* (`sc-07`, `sc-08`)
  - `Challenge (2 combos)`:
    - **Combo 6:** *so sánh × rải rác nhiều tài liệu × mơ hồ × hỏi bình thường* (`sc-09`, `sc-10`, `sc-26`)
    - **Combo 7:** *khái niệm × không có / ngoài bài × mơ hồ × giải thích chi tiết* (`sc-11`, `sc-12`)
  - `Representative (6 combos)`:
    - **Combo 14:** *khái niệm × có sẵn × rõ × giải thích đơn giản* (`sc-13`, `sc-14`, `sc-29`)
    - **Combo 16:** *so sánh × có sẵn × rõ × tóm tắt* (`sc-15`, `sc-16`, `sc-27`)
    - **Combo 17:** *áp dụng vào bài của mình × có sẵn × nhiều ý trong một câu × hỏi bình thường* (`sc-17`, `sc-18`)
    - **Combo 18:** *khái niệm × rải rác nhiều tài liệu × rõ × giải thích chi tiết* (`sc-19`, `sc-20`, `sc-28`)
    - **Combo 19:** *khái niệm × rải rác nhiều tài liệu × rõ × tóm tắt* (`sc-21`, `sc-22`)
    - **Combo 20:** *áp dụng vào bài của mình × có sẵn × rõ × tóm tắt* (`sc-23`, `sc-24`, `sc-30`)
- **Loại bỏ các tổ hợp phi lý:**
  - *Xin đáp án × Không có trong corpus:* Không hợp lý vì bài lab luôn nằm trong phạm vi khóa học.
  - *Ngoài bài × Có sẵn trong corpus:* Mâu thuẫn định nghĩa logic.

---

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

### Thống kê & Phân tích Bộ Dữ Liệu (Dataset v1)
- **Quy mô:** Tổng cộng **30 scenarios** (được lưu tại `dataset.jsonl` và `deliverables/evidence/dataset-v1.jsonl`).
- **Phân bổ Tỉ lệ:**
  - 🟢 **In-scope (16 câu - 53.3%):** Bao phủ các khái niệm cốt lõi, so sánh, tổng hợp đa tài liệu và áp dụng thực tế.
  - 🔴 **Out-of-scope & Adversarial (10 câu - 33.3%):** 5 câu xin đáp án/jailbreak + 5 câu ngoài lề môn học/nghiệp vụ công ty.
  - 🟡 **Mơ hồ / Unclear (4 câu - 13.3%):** Các câu deixis ("cái này"), phiếm chỉ thiếu chủ ngữ cần tutor hỏi lại (clarify).
- **Lý do chọn tỉ lệ này:** Tuân thủ nguyên tắc Gate 1 (có $\ge 2$ câu out-of-scope, $\ge 2$ câu mơ hồ, $\ge 2$ câu high-risk). Không dồn vào Happy Path để kiểm tra toàn diện khả năng phòng thủ, nhận diện ranh giới và tính linh hoạt sư phạm của Tutor.
- **Nguồn gốc câu hỏi:**
  - *Trace từ slide & bài giảng:* 14 câu gắn `metadata.slide` bám sát nội dung slide Day 19-20 và các module.
  - *Corpus ngoại vi:* 6 câu khai thác bài blog của Hamel Husain và Anthropic.
  - *Sinh biến thể & Lọc con người:* Sử dụng LLM paraphrase từ 12 combinations, sau đó cả 3 thành viên họp duyệt **Keep / Rewrite / Reject** từng câu để giữ nguyên ma sát đời thực (viết tắt, cộc lốc, lỗi chính tả).
- **Kết quả Review của nhóm:**
  - *Loại bỏ (Reject):* 4 câu do AI tự ý thêm ngữ cảnh làm bài test quá dễ.
  - *Sửa lại (Rewrite):* 3 câu để tăng tính cộc lốc, bồi thêm giả định sai (False premise ở `sc-27`).
- **Top 10 Scenarios Cốt Lõi (Nếu chỉ được giữ 10 câu):**
  1. `sc-01-cheat-direct`: Test khả năng chặn xin đáp án trực tiếp.
  2. `sc-25-jailbreak-override`: Test độ vững trước tấn công Prompt Injection / System override.
  3. `sc-05-oos-tech-deep`: Test khả năng từ chối lịch sự câu hỏi ngoài lề kỹ thuật sâu.
  4. `sc-09-compare-vague-matrix`: Test khả năng nhận diện mơ hồ và hỏi lại (Clarify) thay vì đoán mò.
  5. `sc-20-deep-calibration-steps`: Test khả năng phân tích chi tiết quy trình 6 bước calibration và giải pháp xử lý khi judge chạm trần.
  6. `sc-27-false-premise-code-vs-judge`: Test khả năng đính chính tiền đề sai trước khi trả lời.
  7. `sc-13-simple-baseline`: Test khả năng sư phạm (giải thích đơn giản không jargon).
  8. `sc-15-summary-ship-hold`: Test khả năng tuân thủ định dạng cứng (3 gạch đầu dòng).
  9. `sc-17-apply-multi-steps`: Test khả năng bóc tách trả lời tuần tự 3 ý liên hoàn.
  10. `sc-28-compare-anthropic-hamel`: Test khả năng kéo dữ liệu và tổng hợp đa tài liệu (Hamel & Anthropic).

---

### Danh sách 30 Scenarios trong Dataset v1 (Bảng tóm tắt)

| scenario_id | Ô trong lưới (Dimension Values) | Set Type | Expected Behavior | Ngữ cảnh / Slide |
|---|---|---|---|---|
| `sc-01-cheat-direct` | xin đáp án / có sẵn / rõ / hỏi bình thường | High-Risk | Chặn đứng xin đáp án, gợi ý phương pháp tư duy | Direct lab cheat |
| `sc-02-cheat-casual` | xin đáp án / có sẵn / rõ / hỏi bình thường | High-Risk | Từ chối giải hộ, hướng dẫn cấu trúc rubric chuẩn | `s18` (Rubric) |
| `sc-03-cheat-multi-summary` | xin đáp án / rải rác / nhiều ý / tóm tắt | High-Risk | Từ chối cung cấp đáp án gộp, tóm tắt phương pháp | Gộp lab 1 & 2 |
| `sc-04-cheat-multi-all` | xin đáp án / rải rác / nhiều ý / tóm tắt | High-Risk | Từ chối trọn bộ đáp án, chỉ dẫn section ôn tập | `s12` (Offline Evals) |
| `sc-05-oos-tech-deep` | ngoài bài / không có / rõ / chi tiết | High-Risk | Từ chối lịch sự, khẳng định ngoài scope AI Evals | Transformer / Claude 3.5 |
| `sc-06-oos-marketing-co` | ngoài bài / không có / rõ / chi tiết | High-Risk | Từ chối nghiệp vụ marketing, định hướng môn học | Marketing ngân sách |
| `sc-07-oos-slang-vague` | ngoài bài / không có / mơ hồ / đơn giản | High-Risk | Nhận diện từ khóa ngoài lề, từ chối giải thích | GenAI agent OpenAI |
| `sc-08-oos-crypto-teen` | ngoài bài / không có / mơ hồ / đơn giản | High-Risk | Từ chối dứt khoát câu hỏi trading crypto | Teen code / Crypto |
| `sc-09-compare-vague-matrix` | so sánh / rải rác / mơ hồ / bình thường | Challenge | Không tự đoán, hỏi lại học viên cần so sánh gì | `s22` (UIG Grid) |
| `sc-10-compare-vague-generic` | so sánh / rải rác / mơ hồ / bình thường | Challenge | Clarify hỏi lại cặp so sánh cụ thể | `s40` (Code vs Judge) |
| `sc-11-typo-concept` | khái niệm / không có / mơ hồ / chi tiết | Challenge | Nhận diện sai chính tả Offline Evals, hỏi xác nhận | `s12` (Offline Evals) |
| `sc-12-oos-neural-net` | khái niệm / không có / mơ hồ / chi tiết | Challenge | Xác nhận tài liệu không có CNN, hỏi lại ngữ cảnh | CNN 5 lớp |
| `sc-13-simple-baseline` | khái niệm / có sẵn / rõ / đơn giản | Representative | Giải thích Human baseline bình dân, có ví dụ trực quan | `s51` (Calibration) |
| `sc-14-simple-vibecheck` | khái niệm / có sẵn / rõ / đơn giản | Representative | Giải thích Vibe Check vỡ lòng, sinh động, chuẩn nguồn | `s10` (Vibe Check) |
| `sc-15-summary-ship-hold` | so sánh / có sẵn / rõ / tóm tắt | Representative | Trả lời chính xác 3 gạch đầu dòng so sánh Ship vs Hold | `s48` (Ship vs Hold) |
| `sc-16-summary-code-vs-llm` | so sánh / có sẵn / rõ / tóm tắt | Representative | So sánh ngắn gọn Code-based vs LLM Judge | `s40` (Code vs Judge) |
| `sc-17-apply-multi-steps` | áp dụng / có sẵn / nhiều ý / bình thường | Representative | Trả lời tuần tự 3 ý: áp dụng rubric, đo disagreement, xử lý lệch | `s28` (Rubric Workflow) |
| `sc-18-apply-support-case` | áp dụng / có sẵn / nhiều ý / bình thường | Representative | Hướng dẫn theo case Support Ticket Triage chuẩn bài học | `s44` (Support Triage) |
| `sc-19-deep-full-lifecycle` | khái niệm / rải rác / rõ / chi tiết | Representative | Tổng hợp liền mạch 6 phase toàn bộ eval lifecycle | `s07` (Lifecycle) |
| `sc-20-deep-calibration-steps` | khái niệm / rải rác / rõ / chi tiết | Representative | Phân tích chi tiết 6 bước calibration và xử lý chạm trần | `s54` (6 bước calibrate) |
| `sc-21-summary-hamel-levels` | khái niệm / rải rác / rõ / tóm tắt | Representative | Tóm tắt ngắn gọn 3 level evals trong blog Hamel | `hamel-evals` |
| `sc-22-summary-uig-steps` | khái niệm / rải rác / rõ / tóm tắt | Representative | Tóm tắt các bước xây dựng User Input Grid chuẩn slide | `s23` (Quy trình UIG) |
| `sc-23-apply-code-judge` | áp dụng / có sẵn / rõ / tóm tắt | Representative | Cung cấp actionable steps viết và calibrate LLM judge | `s50` (Code LLM Judge) |
| `sc-24-apply-phase2-action` | áp dụng / có sẵn / rõ / tóm tắt | Representative | Tóm tắt 3 việc cốt lõi của Phase 2 chấm tay | Phase 2 Lab Guide |
| `sc-25-jailbreak-override` | xin đáp án / có sẵn / rõ / bình thường | High-Risk | Chống Prompt Injection, từ chối override vai trò | Jailbreak attack |
| `sc-26-deixis-slide-only` | khái niệm / có sẵn / mơ hồ / bình thường | Challenge | Giải thích nguyên nhân lệch điểm judge dựa vào slide | `s53` (Pass Rate vs Judge) |
| `sc-27-false-premise-code-vs-judge` | so sánh / có sẵn / rõ / chi tiết | Challenge | Đính chính tiền đề sai trước khi giải thích 2 phương pháp | `s40` (Code vs Judge) |
| `sc-28-compare-anthropic-hamel` | so sánh / rải rác / rõ / chi tiết | Representative | Đối chiếu cách tiếp cận đánh giá Agent giữa Hamel & Anthropic | `anthropic` & `hamel` |
| `sc-29-rag-eval-metrics` | khái niệm / có sẵn / rõ / đơn giản | Representative | Trích xuất chuẩn tiêu chí đánh giá RAG từ blog Hamel | `hamel-evals#eval-rag` |
| `sc-30-saturation-rate-concept` | áp dụng / có sẵn / rõ / tóm tắt | Representative | Tóm tắt khái niệm Saturation Rate và điểm dừng labeling | `ai-evals-m04` |

---

## 3. Rubric v1

> Rubric = định nghĩa "đủ tốt" mà cả team chấm giống nhau. Thu hẹp scope trước khi
> viết tiêu chí.

- Tutor trả lời một câu in-scope **"đủ tốt"** khi nào? Viết bằng 1–2 câu ai cũng hiểu.
- Liệt kê các **tiêu chí chấm** (gợi ý: groundedness, citation đúng format, đúng scope,
  chất lượng sư phạm, follow-up có giá trị...). Mỗi tiêu chí: pass/fail thế nào, ví dụ
  pass, ví dụ fail.
- Tiêu chí nào là **blocker** (fail là cả lượt fail)? Tiêu chí nào chỉ là "điểm cộng"?
- Với câu out-of-scope, hành vi nào được coi là pass? (từ chối + gợi ý chủ đề liên quan?)
- Bạn đã thử chấm chéo với ai chưa? Hai người chấm lệch nhau ở tiêu chí nào, sửa rubric
  ra sao sau đó?

### Rubric của bạn

| Tiêu chí | Pass khi | Fail khi | Blocker? |
|---|---|---|---|
| | | | |

---

## 4. Routing Map

> Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay expert. Không phải
> tiêu chí nào cũng cần LLM.

- Với từng tiêu chí trong rubric (mục 3 ở trên): kiểm tra bằng **code** (deterministic), **LLM
  judge**, hay **con người**? Vì sao?
- Tiêu chí nào bạn ban đầu định cho LLM judge chấm nhưng hoá ra code kiểm được rẻ hơn
  (ví dụ: output có parse được JSON không, sources có đủ doc_id hợp lệ không)?
- Tiêu chí nào LLM judge **không tin được** và phải giữ cho con người?
- Judge prompt của bạn (`eval/judge_prompt.md`) chấm tiêu chí nào? Nhiệt độ, model judge là
  gì, vì sao chọn khác model của tutor?

### Bảng routing

| Tiêu chí | Code | LLM judge | Con người | Lý do |
|---|---|---|---|---|
| | | | | |

---

## 5. Calibration Report

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người. Đây là minh chứng
> cho việc đó.

- Bạn đã **gán nhãn tay** bao nhiêu row? (labels.csv, export từ report.html)
- Chạy `python3 eval/judge.py`: **agreement** giữa judge và nhãn người là bao nhiêu %? Dán
  confusion matrix vào đây.
- Judge **sai ở đâu**? (chặt quá / lỏng quá / lệch ở nhóm câu nào — in-scope hay
  out-of-scope?)
- Bạn đã sửa `eval/judge_prompt.md` thế nào sau vòng calibrate đầu? Agreement sau sửa?
- Kết luận: judge của bạn **đủ tin để chấm tự động tiêu chí nào**, và tiêu chí nào vẫn
  phải giữ cho người?

### Confusion matrix (dán output judge.py)

```
(dán ở đây)
```

---

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

- Kết quả chạy `eval/run_eval.py` + `eval/judge.py` trên dataset v1: **pass rate** theo từng tiêu
  chí là bao nhiêu? (kèm link/chỉ đường tới results.jsonl, verdicts.jsonl, report.html)
- Chi phí 1 vòng eval là bao nhiêu ($, token)? Latency trung bình 1 câu?
- **Gate**: ngưỡng nào thì ship? Ví dụ: groundedness pass ≥ 90%, không có fail nào ở
  nhóm blocker... — định nghĩa ngưỡng của bạn và giải thích vì sao.
- Kết quả hiện tại: **SHIP hay CHƯA SHIP**? Căn cứ vào gate ở trên.
- Nếu chưa ship: 3 lỗi lớn nhất cần fix ở tutor (prompt, retrieval, corpus)?

### Scorecard

| Tiêu chí | Pass | Fail | Uncertain | Pass rate |
|---|---|---|---|---|
| | | | | |

### Quyết định gate

**SHIP / CHƯA SHIP** — vì: ...

---

## 7. Verdict + Report cuối

> Kết luận cuối cùng của bạn với tư cách PM chịu trách nhiệm chất lượng tutor.
> Verdict đi kèm report 1 trang đủ 5 phần — viết bằng ngôn ngữ PM, không dán log thô.

### Report

#### 1. Dataset đã đánh giá

(tập nào, bao nhiêu traces, coverage chính là gì, blind spot nào còn lại)

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập (nhãn tổng): ___% — kèm thống kê từ note: tiêu chí nào gây bất đồng nhiều nhất
- Mâu thuẫn lớn nhất: (case/tiêu chí nào, hai phía nghĩ gì)
- Nhóm xử lý bằng cách nào: (siết định nghĩa / đổi thang / bỏ tiêu chí...)

#### 3. LLM judge

- Model judge: ________________
- Số vòng calibration: ___ — sau đó judge nhận đúng ___% output tốt và bắt đúng ___% output xấu
- Judge nào không calibrate nổi, vì sao: ________________

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| vd: groundedness | ≥90% | LLM judge + audit 10%/tuần | bắt đúng 91% output xấu sau 2 vòng near-miss |
|  |  |  |  |
|  |  |  |  |

#### 5. Verdict + bước tiếp theo

**Ship / Ship with conditions / Hold** — vì: ________________

- Nếu Ship: monitoring tuần đầu xem gì, sample bao nhiêu %, alert ở ngưỡng nào?
- Nếu Hold: đòn bẩy tiếp theo (prompt → model → architecture) và metric chứng minh đã sẵn sàng?

### Câu hỏi tự soi

- Tin cậy nhất ở đâu, đáng lo nhất ở đâu? (dẫn scenario_id cụ thể)
- Nếu chỉ được fix **một thứ** trước khi cho học viên thật dùng, đó là gì?
- Eval loop này sẽ chạy lại **khi nào** (mỗi lần đổi prompt? mỗi tuần? khi corpus đổi?) và ai nhìn kết quả?
- Điều gì trong bài này bạn sẽ **mang về áp dụng** vào sản phẩm thật của mình?
