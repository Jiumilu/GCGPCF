#!/usr/bin/env python3
"""Validate current-session mainline drift watch fixtures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/session-mainline-drift-watch-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/session-mainline-drift-watch-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-DRIFT-WATCH-003.md"
PREFLIGHT = ROOT / "docs/harness/evidence/session-mainline-preflight-enforcement-20260622.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_session_mainline_drift_watch: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    preflight = json.loads(read(PREFLIGHT))

    require(evidence["evidence_id"] == "SESSION-MAINLINE-DRIFT-WATCH-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-SESSION-MAINLINE-DRIFT-WATCH-003", "invalid scope")
    require(evidence["status"] == "drift_watch_configured", "invalid status")
    require(evidence["current_session_mainline"] == preflight["matched_session_mainline"], "mainline mismatch")
    require(evidence["watch_mode"] == "repo_recorded_governance_only", "invalid watch mode")
    require(evidence["live_codex_threads_covered"] is False, "live Codex threads must remain out of scope")

    rules = {rule["rule_id"]: rule for rule in evidence["rules"]}
    for rule_id in ["same_mainline_continue", "other_session_family", "live_thread_access", "write_or_release_action"]:
        require(rule_id in rules, f"missing rule: {rule_id}")
    require(rules["same_mainline_continue"]["decision"] == "continue_current_mainline_only", "same mainline decision mismatch")
    require(rules["same_mainline_continue"]["requires_authorization"] is False, "same mainline must not require authorization")
    for rule_id in ["other_session_family", "live_thread_access", "write_or_release_action"]:
        require(rules[rule_id]["requires_authorization"] is True, f"{rule_id} must require authorization")

    expected = {
        "下一步": ("continue_current_mainline_only", False),
        "继续": ("continue_current_mainline_only", False),
        "继续 GFIS runtime repair": ("mainline_drift_detected", True),
        "执行 CodeGraph 跨仓 recheck": ("mainline_drift_detected", True),
        "接管其它 Codex 线程": ("authorization_required", True),
        "提交并推送这些改动": ("authorization_required", True),
    }
    fixtures = {}
    for item in evidence["positive_fixtures"] + evidence["negative_fixtures"]:
        fixtures[item["request"]] = (item["expected_decision"], item["expected_authorization_required"])
    for request, expected_pair in expected.items():
        require(fixtures.get(request) == expected_pair, f"fixture mismatch: {request}")

    for phrase in [
        "auto_takeover_live_codex_threads",
        "auto_execute_other_session_task",
        "auto_cross_repo_execution",
        "auto_external_api_write",
        "auto_real_kds_api_write",
        "auto_commit",
        "auto_push",
        "auto_deploy",
        "auto_status_promotion",
    ]:
        require(phrase in evidence["forbidden_actions"], f"forbidden action missing: {phrase}")

    for phrase in [
        "Session Mainline Drift Watch 20260622",
        "repo_recorded_governance_only",
        "mainline_drift_detected",
        "authorization_required",
        "GPCF-SESSION-MAINLINE-HANDOFF-REQUEST-GATE-004",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "判断", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "session_mainline_drift_watch=pass "
        "watch_mode=repo_recorded_governance_only "
        "positive_fixtures=2 negative_fixtures=4 "
        "live_codex_threads_covered=false auto_takeover_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
