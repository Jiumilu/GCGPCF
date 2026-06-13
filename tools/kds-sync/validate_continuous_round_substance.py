#!/usr/bin/env python3
"""Validate substance accounting for continuous Loop modes L3/L3.5/L4/L5."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
AUTONOMY_POLICY = ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md"
ROUND_TEMPLATE = ROOT / "templates/LOOP_ROUND_TEMPLATE.md"
ORCHESTRATOR_SKILL = ROOT / ".codex/skills/globalcloud-loop-orchestrator/SKILL.md"

ALLOWED_MODES = {"L3", "L3.5", "L4", "L5"}
ALLOWED_GATES = {"pass", "partial", "fail"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def table_value(text: str, key: str) -> str:
    pattern = re.compile(rf"^\|\s*{re.escape(key)}\s*\|\s*(.*?)\s*\|$", re.MULTILINE)
    match = pattern.search(text)
    require(match is not None, f"LOOP_CONTROL_BOARD.md missing table field: {key}")
    return match.group(1).strip()


def parse_ratio(value: str, field: str) -> tuple[int, int]:
    match = re.search(r"(\d+)\s*/\s*(\d+)", value)
    require(match is not None, f"invalid ratio for {field}: {value}")
    return int(match.group(1)), int(match.group(2))


def main() -> int:
    control = read(CONTROL_BOARD)
    policy = read(AUTONOMY_POLICY)
    template = read(ROUND_TEMPLATE)
    skill = read(ORCHESTRATOR_SKILL)

    required_phrases = [
        "substantive_rounds",
        "generated_items",
        "batch_generated",
        "substance_gate",
        "批量生成",
        "authorization_boundary",
    ]
    for phrase in required_phrases:
        require(phrase in policy, f"LOOP_AUTONOMY_POLICY.md missing substance phrase: {phrase}")
        require(phrase in template, f"LOOP_ROUND_TEMPLATE.md missing substance phrase: {phrase}")
        require(phrase in skill, f"loop orchestrator skill missing substance phrase: {phrase}")

    mode_line = table_value(control, "当前 Loop 模式")
    detected_modes = {mode for mode in ALLOWED_MODES if mode in mode_line}
    require(detected_modes, f"unable to detect continuous mode from: {mode_line}")

    declared_value = table_value(control, "continuous declared_rounds")
    substantive_value = table_value(control, "continuous substantive_rounds")
    generated_items = table_value(control, "continuous generated_items")
    batch_generated = table_value(control, "continuous batch_generated")
    substance_gate = table_value(control, "continuous substance_gate")
    corrected_stop_type = table_value(control, "corrected stop_type")
    current_stop_type = table_value(control, "L3 stop_type")

    declared_done, declared_limit = parse_ratio(declared_value, "continuous declared_rounds")
    substantive_done, substantive_limit = parse_ratio(substantive_value, "continuous substantive_rounds")
    require(declared_limit == substantive_limit, "declared and substantive limits must match")
    require(generated_items.isdigit(), f"generated_items must be numeric: {generated_items}")
    require(batch_generated in {"true", "false"}, f"batch_generated must be true/false: {batch_generated}")
    require(substance_gate in ALLOWED_GATES, f"invalid substance_gate: {substance_gate}")

    if batch_generated == "true":
        require(substantive_done <= declared_done, "batch-generated substantive rounds cannot exceed declared rounds")

    if declared_done >= declared_limit and substantive_done < substantive_limit:
        require(
            corrected_stop_type == "authorization_boundary",
            "declared budget exhausted but substantive rounds incomplete must correct stop_type to authorization_boundary",
        )
        require(
            current_stop_type != "budget_exhausted" or substance_gate != "pass",
            "budget_exhausted cannot be accepted when substance_gate is not pass",
        )

    if corrected_stop_type == "budget_exhausted":
        require(
            substantive_done >= substantive_limit and substance_gate == "pass",
            "budget_exhausted requires substantive_rounds to reach limit and substance_gate=pass",
        )

    print("continuous round substance validation passed")
    print(
        "declared="
        f"{declared_done}/{declared_limit} substantive={substantive_done}/{substantive_limit} "
        f"generated_items={generated_items} batch_generated={batch_generated} "
        f"substance_gate={substance_gate} corrected_stop_type={corrected_stop_type}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
