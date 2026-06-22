#!/usr/bin/env python3
"""Validate the current GPCF session mainline declaration evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/current-session-mainline-declaration-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/current-session-mainline-declaration-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-DECLARATION-001.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_current_session_mainline_declaration: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def require_phrases(label: str, text: str, phrases: list[str]) -> None:
    for phrase in phrases:
        require(phrase in text, f"{label} missing phrase: {phrase}")


def main() -> int:
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CURRENT-SESSION-MAINLINE-DECLARATION-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-SESSION-MAINLINE-DECLARATION-001", "invalid scope")
    require(evidence["status"] == "session_mainline_declared", "invalid status")
    require(evidence["session_mainline"] == "LOOP治理主线: session-mainline-control rollout", "invalid session_mainline")
    require(evidence["owner_session"] == "current_gpcf_loop_governance_session", "invalid owner_session")
    require(evidence["loop_mode"] == "L2-governance", "invalid loop mode")
    require(evidence["status_ceiling"] == "partial", "invalid status ceiling")

    for key in [
        "scope_in",
        "scope_out",
        "allowed_actions",
        "forbidden_actions",
        "stop_conditions",
        "evidence_inputs",
        "validators",
    ]:
        require(isinstance(evidence[key], list) and evidence[key], f"{key} must be a non-empty list")

    for phrase in [
        "production write",
        "external API write",
        "real KDS API write",
        "commit",
        "push",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(phrase in evidence["forbidden_actions"], f"forbidden action missing: {phrase}")

    handoff = evidence["handoff"]
    require(handoff["handoff_required"] is False, "handoff must not be required for current continuation")
    require(handoff["handoff_source"] == "none", "handoff source must be none")
    require("no additional authorization" in handoff["authorization_delta"], "authorization delta must be explicit")

    drift = evidence["drift_check"]
    require(drift["user_request_matches_session_mainline"] is True, "user request must match session mainline")
    require(drift["worktree_in_scope"] is True, "worktree must be in scope")
    require(drift["other_session_task_takeover"] is False, "must not take over another session")
    require(drift["cross_project_execution"] is False, "must not execute cross-project work")
    require(drift["mainline_drift_detected"] is False, "mainline drift must be false")
    require(drift["authorization_required"] is False, "authorization_required must be false")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must remain false: {key}")

    require_phrases(
        "evidence markdown",
        evidence_md,
        [
            "Current Session Mainline Declaration 20260622",
            "session_mainline",
            "LOOP治理主线: session-mainline-control rollout",
            "scope_in",
            "scope_out",
            "forbidden_actions",
            "mainline_drift_detected",
            "handoff_required",
            "accepted",
            "integrated",
            "production_ready",
            "GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002",
        ],
    )
    require_phrases("loop round", loop_round, ["输入", "判断", "动作", "输出", "检查", "反馈"])

    print(
        "current_session_mainline_declaration=pass "
        "session_mainline=session-mainline-control-rollout "
        "handoff_required=false mainline_drift_detected=false "
        "status_ceiling=partial accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
