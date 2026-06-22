#!/usr/bin/env python3
"""Validate current-session mainline preflight enforcement evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/session-mainline-preflight-enforcement-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/session-mainline-preflight-enforcement-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002.md"
SESSION_REGISTRY = ROOT / "02-governance/loop/LOOP_SESSION_REGISTRY.md"
CURRENT_DECLARATION = ROOT / "docs/harness/evidence/current-session-mainline-declaration-20260622.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_session_mainline_preflight_enforcement: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    registry = read(SESSION_REGISTRY)
    current_declaration = json.loads(read(CURRENT_DECLARATION))

    require(evidence["evidence_id"] == "SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002", "invalid scope")
    require(evidence["status"] == "preflight_enforced", "invalid status")
    require(evidence["input_request"] == "下一步", "invalid input request")
    require(evidence["matched_session_mainline"] == current_declaration["session_mainline"], "session mainline mismatch")
    require(evidence["preflight_decision"] == "continue_current_mainline_only", "invalid preflight decision")

    checks = evidence["checks"]
    expected_true = [
        "registry_present",
        "current_declaration_present",
        "request_matches_current_mainline",
    ]
    expected_false = [
        "other_session_takeover_requested",
        "cross_repo_execution_requested",
        "external_api_requested",
        "real_kds_api_write_requested",
        "commit_requested",
        "push_requested",
        "deploy_requested",
        "status_promotion_requested",
        "handoff_required",
        "mainline_drift_detected",
        "authorization_required",
    ]
    for key in expected_true:
        require(checks.get(key) is True, f"check must be true: {key}")
    for key in expected_false:
        require(checks.get(key) is False, f"check must be false: {key}")

    gate = evidence["session_family_gate"]
    require(gate["repo_recorded_loop_rounds"] >= 876, "repo recorded loop round count regressed")
    require(gate["orphan_session_family"] == 0, "orphan session family must be zero")
    require(gate["live_codex_threads_covered"] is False, "live Codex threads must remain out of scope")
    require(gate["auto_takeover_allowed"] is False, "auto takeover must be false")
    require(gate["write_without_handoff_allowed"] is False, "write without handoff must be false")

    for phrase in [
        "take over live Codex threads",
        "execute another session task",
        "cross repo execution",
        "external API write",
        "real KDS API write",
        "commit",
        "push",
        "deploy",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(phrase in evidence["forbidden_actions"], f"forbidden action missing: {phrase}")

    for phrase in [
        "Session Mainline Preflight Enforcement 20260622",
        "continue_current_mainline_only",
        "mainline_drift_detected",
        "handoff_required",
        "authorization_required",
        "live_codex_threads_covered",
        "auto_takeover_allowed",
        "GPCF-SESSION-MAINLINE-DRIFT-WATCH-003",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "判断", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")
    require("LOOP 会话总账" in registry, "session registry missing")

    print(
        "session_mainline_preflight_enforcement=pass "
        "preflight_decision=continue_current_mainline_only "
        "mainline_drift_detected=false handoff_required=false authorization_required=false "
        "live_codex_threads_covered=false auto_takeover_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
