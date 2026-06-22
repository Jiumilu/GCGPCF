#!/usr/bin/env python3
"""Validate current-session summary and declaration control boundary."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/session-main-task-summary-declaration-boundary-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/session-main-task-summary-declaration-boundary-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-SESSION-DECLARATION-CONTROL-BOUNDARY-001.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "SESSION-MAIN-TASK-SUMMARY-DECLARATION-BOUNDARY-20260622", "invalid evidence id")
    require(evidence["status"] == "declaration_boundary_controlled", "invalid status")
    require(evidence["scope"] == "GPCF-SESSION-DECLARATION-CONTROL-BOUNDARY-001", "invalid scope")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004", "invalid next round")
    require(len(evidence["main_task_summary"]) >= 4, "main task summary is incomplete")
    require(len(evidence["allowed_declarations"]) >= 6, "allowed declarations are incomplete")
    require(len(evidence["forbidden_declarations"]) >= 6, "forbidden declarations are incomplete")
    observation = evidence["post_boundary_revalidation_observation"]
    require(observation["result"] == "failed_after_boundary_generation", "post-boundary observation must record live drift")
    require("Brain" in observation["observed_failure"], "post-boundary observation must mention Brain drift")

    for source in evidence["source_evidence"]:
        require((ROOT / source).exists(), f"missing source evidence: {source}")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must remain false: {key}")

    required_md_phrases = [
        "允许声明",
        "禁止声明",
        "声明控制边界",
        "Agent-Reach accepted",
        "Agent-Reach integrated",
        "Agent-Reach production_ready",
        "GFIS policy exception repaired",
        "Brain/Studio business code changed",
        "Post-boundary Live Revalidation Observation",
        "GlobalCloud Brain live pending must be zero",
        "截至本轮证据生成时",
        "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004",
    ]
    for phrase in required_md_phrases:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "session_declaration_control_boundary=pass "
        "status=declaration_boundary_controlled "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
