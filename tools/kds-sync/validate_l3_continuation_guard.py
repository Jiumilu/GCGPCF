#!/usr/bin/env python3
"""Validate that active L3 sessions cannot stop after a stage summary."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
AUTONOMY_POLICY = ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md"
ORCHESTRATOR_SKILL = ROOT / ".codex/skills/globalcloud-loop-orchestrator/SKILL.md"

ALLOWED_STOP_TYPES = {
    "hard_stop",
    "user_stop",
    "budget_exhausted",
    "time_exhausted",
    "task_queue_empty",
    "authorization_boundary",
}


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


def parse_completed_rounds(value: str) -> tuple[int, int]:
    match = re.search(r"(\d+)\s*/\s*(\d+)", value)
    require(match is not None, f"invalid L3 completed rounds value: {value}")
    return int(match.group(1)), int(match.group(2))


def main() -> int:
    control = read(CONTROL_BOARD)
    policy = read(AUTONOMY_POLICY)
    skill = read(ORCHESTRATOR_SKILL)

    for phrase in [
        "L3 final answer guard",
        "3 轮不是停止条件",
        "阶段性汇报只能是 progress update",
        "stop_type=none",
    ]:
        require(phrase in policy, f"LOOP_AUTONOMY_POLICY.md missing guard phrase: {phrase}")

    for phrase in [
        "L3 final answer guard",
        "停止类型为 `none`",
        "必须继续下一轮",
        "validate_l3_continuation_guard.py",
    ]:
        require(phrase in skill, f"loop orchestrator skill missing guard phrase: {phrase}")

    session = table_value(control, "L3 session")
    completed_value = table_value(control, "L3 已完成轮次")
    remaining_value = table_value(control, "L3 剩余轮次")
    stop_type = table_value(control, "L3 stop_type")
    stop_evidence = table_value(control, "L3 stop_evidence")
    final_guard = table_value(control, "L3 final answer guard")
    next_round = table_value(control, "当前轮次")

    completed, limit = parse_completed_rounds(completed_value)
    require(limit == 15, f"L3 limit must be 15, got {limit}")
    require(remaining_value.isdigit(), f"L3 remaining rounds must be numeric: {remaining_value}")
    remaining = int(remaining_value)
    require(remaining == limit - completed, "L3 remaining rounds must equal 15 - completed")

    if session == "active" and completed < limit:
        require(stop_type == "none", "active L3 below 15 rounds must use stop_type=none unless it is actually stopping")
        require(stop_evidence == "无", "active L3 with stop_type=none must use stop_evidence=无")
        require("不得 final 收口" in final_guard, "final answer guard must forbid final closure")
        require("下一轮候选" in next_round, "active L3 must expose next round candidate")
    elif session == "stopped":
        require(stop_type in ALLOWED_STOP_TYPES, f"invalid L3 stopped stop_type: {stop_type}")
    else:
        require(session in {"active", "stopped"}, f"invalid L3 session: {session}")

    for anti_pattern in ["3/15", "5/15", "10/15"]:
        require(anti_pattern in policy, f"policy must explicitly mention anti-pattern {anti_pattern}")

    print("L3 continuation guard validation passed")
    print(f"session={session} completed={completed}/{limit} remaining={remaining} stop_type={stop_type}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
