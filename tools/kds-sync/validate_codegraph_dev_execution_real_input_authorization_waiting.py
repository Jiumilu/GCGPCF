#!/usr/bin/env python3
"""Validate CodeGraph real-input authorization waiting evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-authorization-waiting-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-authorization-waiting-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-AUTHORIZATION-WAITING-020.md"
DISPATCH_AUTH = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-dispatch-authorization-20260626.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    dispatch = load_json(DISPATCH_AUTH)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-REAL-INPUT-AUTHORIZATION-WAITING-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-AUTHORIZATION-WAITING-020", "invalid scope")
    require(evidence["status"] == "authorization_waiting_default_not_authorized", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(dispatch["status"] == "dispatch_authorization_request_ready_not_authorized", "dispatch authorization source status mismatch")

    dispatch_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_real_input_dispatch_authorization.py"])
    require(dispatch_gate.returncode == 0, f"dispatch authorization gate failed: {dispatch_gate.stdout}{dispatch_gate.stderr}")

    state = evidence["waiting_state"]
    require(state["authorization_question_presented"] is True, "authorization question must be presented")
    require(state["authorization_received"] is False, "authorization must not be received")
    require(state["default_if_no_answer"] == "not_authorized", "default must be not_authorized")
    require(state["effective_authorization"] == "not_authorized", "effective authorization must be not_authorized")
    require(state["dispatch_allowed"] is False, "dispatch must not be allowed")
    require(state["dispatch_performed"] is False, "dispatch must not be performed")
    require(state["collection_pack_remains_prepared"] is True, "collection pack must remain prepared")
    require(state["codegraph_development_state_remains_usable"] is True, "CodeGraph development state must remain usable")

    blockers = evidence["current_blockers"]
    require(blockers["human_dispatch_authorization_missing"] is True, "human authorization blocker must be true")
    for key in [
        "recipient_identity_confirmed",
        "manual_channel_confirmed",
        "payload_reviewed",
        "evidence_destination_confirmed",
        "real_source_input_arrived",
    ]:
        require(blockers[key] is False, f"{key} must remain false")

    for phrase in ["keep collection pack prepared", "rerun read-only validators", "inspect local evidence only"]:
        require(phrase in evidence["allowed_while_waiting"], f"missing allowed action: {phrase}")
    for phrase in ["external notification dispatch", "external API write", "real KDS write", "git push", "business status upgrade"]:
        require(phrase in evidence["forbidden_while_waiting"], f"missing forbidden action: {phrase}")

    decision = evidence["decision"]
    require(decision["dispatch_authorization"] == "not_authorized", "dispatch authorization must be not_authorized")
    require(decision["next_action"] == "wait_for_human_authorization_or_keep_collection_pack_prepared", "invalid next action")
    require(decision["real_business_execution"] == "blocked_until_real_source_input_arrives", "real business execution must remain blocked")
    require(decision["runtime_state"] == "not_verified", "runtime state must not be verified")
    require(decision["status_ceiling"] == "partial", "status ceiling must be partial")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "authorization_waiting_default_not_authorized",
        "authorization_received=false",
        "effective_authorization=not_authorized",
        "dispatch_allowed=false",
        "dispatch_performed=false",
        "GPCF-CODEGRAPH-DEV-EXECUTION-GOAL-COMPLETION-AUDIT-021",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "authorization_waiting_default_not_authorized"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_real_input_authorization_waiting=pass "
        "effective_authorization=not_authorized "
        "dispatch_allowed=false "
        "dispatch_performed=false "
        "collection_pack=prepared "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-GOAL-COMPLETION-AUDIT-021"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
