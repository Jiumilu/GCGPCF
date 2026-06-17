#!/usr/bin/env python3
"""Audit Loop round efficiency and substance signals from round records."""

from __future__ import annotations

import difflib
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOOP_DIR = ROOT / "docs/harness/loops"
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


def explicit_batch_generated(text: str) -> bool:
    value = table_value(text, "batch_generated")
    if value is None:
        return False
    return value.lower() == "true"


def is_counted_substantive(text: str) -> bool:
    value = table_value(text, "substantive_round")
    if value is not None:
        return value.lower() == "true"
    ratio = table_value(text, "substantive_rounds")
    if ratio:
        match = re.search(r"(\d+)\s*/", ratio)
        return bool(match and int(match.group(1)) > 0)
    return False


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


def main() -> int:
    require(LOOP_DIR.exists(), f"missing loop directory: {LOOP_DIR.relative_to(ROOT)}")
    paths = sorted(LOOP_DIR.glob("loop-round-*.md"), key=round_sort_key)
    require(paths, "no Loop round records found")

    recent = paths[-AUDIT_LIMIT:]
    hard_recent = paths[-HARD_LIMIT:]
    recent_texts = [(path, read(path)) for path in recent]
    hard_recent_names = {path.name for path in hard_recent}

    missing_truth: list[str] = []
    missing_five_segment: list[str] = []
    hard_missing_truth: list[str] = []
    hard_missing_five_segment: list[str] = []
    explicit_batch_counted: list[str] = []
    hard_explicit_batch_counted: list[str] = []

    for path, text in recent_texts:
        missing_fields = [field for field in TRUTH_FIELDS if table_value(text, field) is None]
        if missing_fields:
            missing_truth.append(f"{path.name}:{','.join(missing_fields)}")
            if path.name in hard_recent_names:
                hard_missing_truth.append(f"{path.name}:{','.join(missing_fields)}")

        missing_segments = [
            segment for segment, markers in FIVE_SEGMENT_MARKERS.items() if not has_any(text, markers)
        ]
        if missing_segments:
            missing_five_segment.append(f"{path.name}:{','.join(missing_segments)}")
            if path.name in hard_recent_names:
                hard_missing_five_segment.append(f"{path.name}:{','.join(missing_segments)}")

        if explicit_batch_generated(text) and is_counted_substantive(text):
            explicit_batch_counted.append(path.name)
            if path.name in hard_recent_names:
                hard_explicit_batch_counted.append(path.name)

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
        if ratio >= 0.92 and previous_path.read_text(encoding="utf-8", errors="ignore") != current_path.read_text(
            encoding="utf-8", errors="ignore"
        ):
            high_similarity_pairs += 1

    max_sequence = max_consecutive_sequence(paths)
    risk = "pass"
    if max_sequence >= 30 or high_similarity_pairs >= 10:
        risk = "watch"
    if missing_truth or missing_five_segment or explicit_batch_counted or duplicate_groups:
        risk = "review_required"

    require(
        not hard_missing_truth,
        "hard-window Loop rounds missing truth fields: " + "; ".join(hard_missing_truth[:10]),
    )
    require(
        not hard_missing_five_segment,
        "hard-window Loop rounds missing five-segment markers: " + "; ".join(hard_missing_five_segment[:10]),
    )
    require(
        not hard_explicit_batch_counted,
        "batch_generated=true rounds counted as substantive: " + ", ".join(hard_explicit_batch_counted[:10]),
    )

    print(
        "loop_round_efficiency_audit=pass "
        f"total_rounds={len(paths)} audit_checked={len(recent)} hard_checked={len(hard_recent)} "
        f"audit_missing_truth_fields={len(missing_truth)} audit_missing_five_segment={len(missing_five_segment)} "
        f"audit_batch_generated_counted={len(explicit_batch_counted)} "
        "hard_missing_truth_fields=0 hard_missing_five_segment=0 hard_batch_generated_counted=0 "
        f"duplicate_fingerprint_groups={len(duplicate_groups)} "
        f"high_similarity_adjacent_pairs={high_similarity_pairs} "
        f"max_consecutive_sequence={max_sequence} risk={risk}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
