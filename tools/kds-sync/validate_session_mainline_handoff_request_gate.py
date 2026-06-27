#!/usr/bin/env python3
"""Validate current-session handoff request gate fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/session-mainline-handoff-request-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/session-mainline-handoff-request-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-HANDOFF-REQUEST-GATE-004.md"
DRIFT_WATCH = ROOT / "docs/harness/evidence/session-mainline-drift-watch-20260622.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_session_mainline_handoff_request_gate: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    drift_watch = json.loads(read(DRIFT_WATCH))

    require(evidence["evidence_id"] == "SESSION-MAINLINE-HANDOFF-REQUEST-GATE-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-SESSION-MAINLINE-HANDOFF-REQUEST-GATE-004", "invalid scope")
    require(evidence["status"] == "handoff_request_gate_configured", "invalid status")
    require(evidence["derived_from"] == drift_watch["evidence_id"], "invalid drift watch linkage")
    require(evidence["current_session_mainline"] == drift_watch["current_session_mainline"], "mainline mismatch")
    require(evidence["gate_mode"] == "explicit_user_confirmation_required", "invalid gate mode")
    require(evidence["live_codex_threads_covered"] is False, "live Codex threads must remain out of scope")
    require(evidence["auto_takeover_allowed"] is False, "auto takeover must be false")

    rules = {rule["rule_id"]: rule for rule in evidence["request_handling_rules"]}
    for rule_id in [
        "same_mainline_next_step",
        "other_session_or_project_family",
        "live_codex_thread_operation",
        "cross_repo_or_external_execution",
        "release_or_status_promotion",
    ]:
        require(rule_id in rules, f"missing rule: {rule_id}")
    require(rules["same_mainline_next_step"]["decision"] == "continue_current_mainline_only", "same mainline decision mismatch")
    require(rules["same_mainline_next_step"]["requires_user_confirmation"] is False, "same mainline must not require confirmation")
    for rule_id in [
        "other_session_or_project_family",
        "live_codex_thread_operation",
        "cross_repo_or_external_execution",
        "release_or_status_promotion",
    ]:
        require(rules[rule_id]["decision"] == "answer_with_handoff_proposal_only", f"{rule_id} decision mismatch")
        require(rules[rule_id]["requires_handoff_proposal"] is True, f"{rule_id} must require handoff proposal")
        require(rules[rule_id]["requires_user_confirmation"] is True, f"{rule_id} must require confirmation")

    required_fields = {
        "requested_action",
        "target_session_or_project",
        "scope",
        "expected_effect",
        "risk",
        "validation_plan",
        "stop_condition",
        "confirmation_required_before_execution",
    }
    require(required_fields.issubset(set(evidence["handoff_proposal_required_fields"])), "handoff proposal fields incomplete")

    for phrase in [
        "take_over_other_live_codex_threads",
        "execute_other_session_work",
        "write_other_project_repos",
        "call_external_write_api",
        "call_real_kds_api_write",
        "commit",
        "push",
        "deploy",
        "promote_status_to_accepted_integrated_or_production_ready",
    ]:
        require(phrase in evidence["forbidden_without_confirmation"], f"forbidden action missing: {phrase}")

    expected = {
        "下一步": ("continue_current_mainline_only", False),
        "其它所有会话呢": ("answer_with_handoff_proposal_only", True),
        "接管 GFIS 会话并继续执行": ("answer_with_handoff_proposal_only", True),
        "提交并推送这些改动": ("answer_with_handoff_proposal_only", True),
    }
    fixtures = {
        item["request"]: (item["expected_decision"], item["expected_confirmation_required"])
        for item in evidence["fixtures"]
    }
    for request, expected_pair in expected.items():
        require(fixtures.get(request) == expected_pair, f"fixture mismatch: {request}")

    for phrase in [
        "Session Mainline Handoff Request Gate 20260622",
        "explicit_user_confirmation_required",
        "answer_with_handoff_proposal_only",
        "其它所有会话呢",
        "GPCF-SESSION-MAINLINE-CROSS-THREAD-LEDGER-005",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "判断", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "session_mainline_handoff_request_gate=pass "
        "gate_mode=explicit_user_confirmation_required "
        "proposal_only_for_other_sessions=true "
        "live_codex_threads_covered=false auto_takeover_allowed=false "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
