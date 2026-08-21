"""Code checks — kiểm tra results.jsonl bằng rule thuần Python (không tốn API).

Đây là làn "Code check" của bài lab: những tiêu chí viết được thành rule thì kiểm
bằng code — nhanh, rẻ, khách quan, chạy lại bao nhiêu lần cũng được.

Chạy:  python3 eval/code_checks.py            # in bảng pass/fail từng check từng row
Mở rộng: thêm hàm check_* mới của riêng nhóm (xem 3 hàm mẫu dưới).
"""
import json
import os
import re
import sys
from pathlib import Path

# tutor.py nằm ở tutor/ (khu vực sản phẩm) — thêm vào sys.path để import được
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tutor"))

import tutor  # dùng lại load_corpus

EXPECTED_FIELDS = {"scope", "answer", "sources", "followup_questions"}


def check_schema(rec):
    """Output parse được và đủ 4 field đúng contract."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return False, "JSON không parse được (xem raw_content)"
    missing = EXPECTED_FIELDS - set(out)
    if missing:
        return False, "thiếu field: " + ", ".join(sorted(missing))
    return True, None


def check_citation_exists(rec, valid_ids):
    """Mọi doc_id/section_id trong sources phải tồn tại thật trong corpus."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    for s in out.get("sources") or []:
        key = (s.get("doc_id"), s.get("section_id"))
        if key not in valid_ids:
            return False, f'nguồn không tồn tại: {key[0]}#{key[1]}'
    return True, None


def _token_subsequence(needle, haystack):
    """True nếu chuỗi token của needle xuất hiện liên tiếp trong haystack."""
    if not needle:
        return True
    n = len(needle)
    return any(haystack[i:i + n] == needle for i in range(len(haystack) - n + 1))


def check_quote_verbatim(rec, section_tokens):
    """Quote phải nằm trong section đã cite — so theo chuỗi token (bỏ dấu, lowercase,
    bỏ mọi dấu câu/khoảng trắng) nên khác biệt gạch ngang/ngoặc kép không tính là sai."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    for s in out.get("sources") or []:
        tokens = section_tokens.get((s.get("doc_id"), s.get("section_id")), [])
        quote_tokens = tutor.tokens(s.get("quote") or "")
        if quote_tokens and not _token_subsequence(quote_tokens, tokens):
            return False, f'quote không khớp section {s.get("section_id")}: "{(s.get("quote") or "")[:40]}..."'
    return True, None


def check_scope_matches_expected(rec, dataset_by_id):
    """scope output của tutor chỉ có 2 giá trị (in_scope/out_of_scope — xem SYSTEM_PROMPT),
    nên chỉ so được với dataset khi expected_scope cũng là 1 trong 2 giá trị đó. Row
    expected_scope="unclear" bị bỏ qua (skip) vì tutor không có cách diễn đạt "mơ hồ" trong
    schema hiện tại — đây chính là spec gap ghi trong REPORT.md mục 4, không phải lỗi tutor."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    expected = (dataset_by_id.get(rec.get("scenario_id"), {}) or {}).get("expected_scope")
    if expected not in ("in_scope", "out_of_scope"):
        return None, "bỏ qua (expected_scope=unclear, ngoài enum scope của tutor)"
    got = out.get("scope")
    if got != expected:
        return False, f"expected {expected}, tutor trả {got}"
    return True, None


def check_followup_count(rec, *_):
    """System prompt yêu cầu followup_questions luôn đúng 3 câu (cả in-scope lẫn out-of-scope)."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    fu = out.get("followup_questions") or []
    if len(fu) != 3 or any(not (q or "").strip() for q in fu):
        return False, f"có {len(fu)} câu (cần đúng 3, không rỗng)"
    return True, None


CHECKS = [  # thêm check của nhóm vào đây
    ("schema_valid", check_schema),
    ("citation_exists", check_citation_exists),
    ("quote_verbatim", check_quote_verbatim),
    ("scope_matches_expected", check_scope_matches_expected),
    ("followup_count", check_followup_count),
]


def main(path="results.jsonl", dataset_path="dataset.jsonl"):
    if not os.path.exists(path):
        raise SystemExit("Không thấy %s — chạy python3 eval/run_eval.py trước." % path)
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]

    sections = tutor.load_corpus()
    valid_ids = {(s["doc_id"], s["section_id"]) for s in sections}
    section_tokens = {(s["doc_id"], s["section_id"]): tutor.tokens(s["text"]) for s in sections}
    dataset_by_id = {}
    if os.path.exists(dataset_path):
        for l in open(dataset_path, encoding="utf-8"):
            if l.strip():
                d = json.loads(l)
                dataset_by_id[d.get("scenario_id") or d.get("id")] = d

    totals = {name: [0, 0] for name, _ in CHECKS}  # [pass, fail] (skip không đếm)
    for rec in rows:
        sid = rec.get("scenario_id", "?")
        line = [sid]
        for name, fn in CHECKS:
            if fn is check_schema:
                ok, reason = fn(rec)
            elif fn is check_citation_exists:
                ok, reason = fn(rec, valid_ids)
            elif fn is check_scope_matches_expected:
                ok, reason = fn(rec, dataset_by_id)
            elif fn is check_followup_count:
                ok, reason = fn(rec)
            else:
                ok, reason = fn(rec, section_tokens)
            if ok is None:
                line.append(f"{name}: skip")
                continue
            totals[name][0 if ok else 1] += 1
            line.append(f"{name}: {'pass' if ok else 'FAIL — ' + str(reason)}")
        print(" | ".join(line))

    print("\nTổng kết:")
    for name, (p, f) in totals.items():
        print(f"  {name}: {p} pass / {f} fail")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "results.jsonl")
