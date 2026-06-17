#!/usr/bin/env python3
"""Validate the Loop governance efficiency debt locator evidence."""

from __future__ import annotations

import difflib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOOP_DIR = ROOT / "docs/harness/loops"
BACKLOG_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.md"
EVIDENCE_README = ROOT / "docs/harness/evidence/README.md"
EVIDENCE_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"
AUDIT_LIMIT = 30
HARD_LIMIT = 5

TRUTH_FIELDS = [
    "declared_rounds",
    "substantive_rounds",
    "generated_items",
    "batch_generated",
    "substance_gate",
    "stop_type",
]

FIVE_SEGMENT_MARKERS = {
    "input": ["## 输入", "| 输入 |", "- 输入：", "## 3. 输入文档"],
    "action": ["## 执行动作", "## 实施动作", "## 实施", "| 动作 |", "- 动作：", "本轮执行", "本轮将", "## 总控回写"],
    "output": ["## 产出", "## 结果", "| 输出 |", "- 输出：", "## 关键事实", "## 输出摘要", "## GFIS 验证摘要"],
    "check": ["## 验证", "## 结果", "## GFIS 验证摘要", "| 检查 |", "- 检查：", "主 SOP validator"],
    "feedback": ["## 下一步", "## 下一轮", "| 反馈 |", "- 反馈："],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def round_sort_key(path: Path) -> tuple[str, int, str]:
    name = path.stem
    match = re.search(r"(.+?)-(\d+)$", name)
    if match:
        return match.group(1), int(match.group(2)), name
    return name, -1, name


def table_value(text: str, key: str) -> str | None:
    patterns = [
        rf"^\|\s*{re.escape(key)}\s*\|\s*(.*?)\s*\|$",
        rf"^\s*[-*]\s*`?{re.escape(key)}`?\s*:\s*`?([^`\n]+)`?\s*$",
        rf"^\s*[-*]\s*`?{re.escape(key)}\s*=\s*([^`\n]+)`?\s*$",
        rf"^\s*`?{re.escape(key)}`?\s*[:=]\s*`?([^`\n]+)`?\s*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            return match.group(1).strip().strip("`").strip()
    return None


def has_any(text: str, markers: list[str]) -> bool:
    return any(marker in text for marker in markers)


def normalize_for_similarity(text: str) -> str:
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    text = re.sub(r"GPCF-[A-Z0-9-]+-\d+", "ROUND_ID", text)
    text = re.sub(r"GFIS-[A-Z0-9-]+-\d+", "GFIS_ROUND_ID", text)
    text = re.sub(r"\b20\d{2}-\d{2}-\d{2}\b", "DATE", text)
    text = re.sub(r"\b\d+\b", "N", text)
    text = re.sub(r"`[^`]+`", "`CODE`", text)
    text = re.sub(r"/Users/[^\s|]+", "ABS_PATH", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def max_consecutive_sequence(paths: list[Path]) -> int:
    by_prefix: dict[str, list[int]] = defaultdict(list)
    for path in paths:
        match = re.search(r"loop-round-(.+?)-(\d+)\.md$", path.name)
        if match:
            by_prefix[match.group(1)].append(int(match.group(2)))

    max_run = 0
    for numbers in by_prefix.values():
        current = 0
        previous: int | None = None
        for number in sorted(set(numbers)):
            if previous is None or number == previous + 1:
                current += 1
            else:
                current = 1
            previous = number
            max_run = max(max_run, current)
    return max_run


def locate_debt() -> dict:
    require(LOOP_DIR.exists(), f"missing loop directory: {LOOP_DIR.relative_to(ROOT)}")
    paths = sorted(LOOP_DIR.glob("loop-round-*.md"), key=round_sort_key)
    require(paths, "no Loop round records found")

    recent = paths[-AUDIT_LIMIT:]
    hard_recent_names = {path.name for path in paths[-HARD_LIMIT:]}
    truth_records = []
    segment_records = []
    hard_truth = []
    hard_segments = []

    recent_texts = [(path, read(path)) for path in recent]
    for path, text in recent_texts:
        missing_fields = [field for field in TRUTH_FIELDS if table_value(text, field) is None]
        if missing_fields:
            record = {
                "round": path.name,
                "path": str(path.relative_to(ROOT)),
                "missing_fields": missing_fields,
            }
            truth_records.append(record)
            if path.name in hard_recent_names:
                hard_truth.append(record)

        missing_segments = [
            segment for segment, markers in FIVE_SEGMENT_MARKERS.items() if not has_any(text, markers)
        ]
        if missing_segments:
            record = {
                "round": path.name,
                "path": str(path.relative_to(ROOT)),
                "missing_segments": missing_segments,
            }
            segment_records.append(record)
            if path.name in hard_recent_names:
                hard_segments.append(record)

    duplicate_fingerprints: dict[str, list[str]] = defaultdict(list)
    normalized_recent = []
    for path, text in recent_texts:
        normalized = normalize_for_similarity(text)
        normalized_recent.append((path, normalized))
        duplicate_fingerprints[normalized].append(path.name)

    duplicate_groups = [names for names in duplicate_fingerprints.values() if len(names) > 1]
    high_similarity_pairs = 0
    for index in range(1, len(normalized_recent)):
        previous_path, previous_text = normalized_recent[index - 1]
        current_path, current_text = normalized_recent[index]
        ratio = difflib.SequenceMatcher(None, previous_text, current_text).ratio()
        if ratio >= 0.92 and read(previous_path) != read(current_path):
            high_similarity_pairs += 1

    return {
        "total_rounds": len(paths),
        "audit_checked": len(recent),
        "hard_checked": HARD_LIMIT,
        "truth_records": truth_records,
        "segment_records": segment_records,
        "hard_truth": hard_truth,
        "hard_segments": hard_segments,
        "duplicate_fingerprint_groups": len(duplicate_groups),
        "high_similarity_adjacent_pairs": high_similarity_pairs,
        "max_consecutive_sequence": max_consecutive_sequence(paths),
    }


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    backlog = read(BACKLOG_DOC)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)
    located = locate_debt()

    require(evidence.get("evidence_id") == "LOOP-GOV-EFF-DEBT-LOCATOR-20260617", "invalid locator evidence id")
    require(evidence.get("status") == "review_required", "locator evidence must remain review_required")
    require(evidence.get("scope", {}).get("no_bulk_rewrite") is True, "locator must forbid bulk rewrite")
    require(evidence.get("scope", {}).get("business_status_impact") == "none", "locator must have no business impact")
    require(not located["hard_truth"], "hard window truth-field debt must remain zero")
    require(not located["hard_segments"], "hard window five-segment debt must remain zero")

    signal = evidence.get("source_signal", {})
    baseline_total_rounds = signal.get("total_rounds")
    require(isinstance(baseline_total_rounds, int), "total round baseline must be numeric")
    require(
        baseline_total_rounds <= located["total_rounds"],
        "total round baseline must not be ahead of current scan",
    )
    require(signal.get("audit_checked") == located["audit_checked"], "audit window mismatch")
    require(signal.get("hard_checked") == located["hard_checked"], "hard window mismatch")
    require(
        signal.get("audit_missing_truth_fields") == len(evidence.get("affected_truth_field_records", [])),
        "baseline truth locator count mismatch",
    )
    require(
        signal.get("audit_missing_five_segment") == len(evidence.get("affected_five_segment_records", [])),
        "baseline five-segment locator count mismatch",
    )
    require(
        signal.get("audit_missing_truth_fields", 0) <= len(located["truth_records"]),
        "current truth locator count must not be below baseline",
    )
    require(
        signal.get("audit_missing_five_segment", 0) <= len(located["segment_records"]),
        "current five-segment locator count must not be below baseline",
    )
    require(signal.get("hard_missing_truth_fields") == 0, "hard truth count must be zero")
    require(signal.get("hard_missing_five_segment") == 0, "hard five-segment count must be zero")
    require(signal.get("duplicate_fingerprint_groups", 0) >= 0, "duplicate group baseline must be non-negative")
    require(signal.get("high_similarity_adjacent_pairs", 0) >= 0, "high similarity baseline must be non-negative")
    require(
        signal.get("max_consecutive_sequence", 0) <= located["max_consecutive_sequence"],
        "max sequence baseline must not exceed current scan",
    )

    for record in evidence.get("affected_truth_field_records", []):
        require((ROOT / record.get("path", "")).exists(), f"truth record path missing: {record.get('path')}")
    for record in evidence.get("affected_five_segment_records", []):
        require((ROOT / record.get("path", "")).exists(), f"five-segment record path missing: {record.get('path')}")

    require("Loop Governance Efficiency Debt Locator Evidence" in evidence_md, "locator markdown missing title")
    require(
        f"LEDB-001 | {len(located['truth_records'])}" in evidence_md,
        "locator markdown missing LEDB-001 count",
    )
    require(
        f"LEDB-002 | {len(located['segment_records'])}" in evidence_md,
        "locator markdown missing LEDB-002 count",
    )
    require("This locator does not rewrite historical round records" in evidence_md, "locator non-claim missing")
    require("LOOP-GOV-EFF-DEBT-LOCATOR-20260617" in backlog, "backlog missing locator evidence link")
    require(
        "Loop Governance Efficiency Debt Locator Evidence | docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.md"
        in evidence_readme,
        "evidence README missing locator entry",
    )
    require("LOOP-GOV-EFF-DEBT-LOCATOR-20260617" in evidence_index, "evidence index missing locator section")

    print(
        "loop_governance_efficiency_debt_locator=pass "
        "evidence=LOOP-GOV-EFF-DEBT-LOCATOR-20260617 "
        f"total_rounds={located['total_rounds']} baseline_total_rounds={baseline_total_rounds} "
        f"truth_records={len(located['truth_records'])} five_segment_records={len(located['segment_records'])} "
        "hard_missing_truth_fields=0 hard_missing_five_segment=0 "
        "no_bulk_rewrite=true business_status_impact=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
