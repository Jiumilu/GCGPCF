#!/usr/bin/env python3
"""Validate resumed CodeGraph dispatch authorization answer evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-authorization-answer-resumed-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-authorization-answer-resumed-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-RESUMED-024.md"
BLOCKED_HOLD = ROOT / "docs/harness/evidence/codegraph-dev-execution-authorization-blocked-hold-20260626.json"


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
    blocked = load_json(BLOCKED_HOLD)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-RESUMED-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-RESUMED-024", "invalid scope")
    require(evidence["status"] == "actual_dispatch_later_intent_recorded_details_missing", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(blocked["status"] == "blocked_hold_requires_user_authorization_or_real_input", "blocked hold source mismatch")

    blocked_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_authorization_blocked_hold.py"])
    require(blocked_gate.returncode == 0, f"blocked hold gate failed: {blocked_gate.stdout}{blocked_gate.stderr}")

    answer = evidence["user_answer"]
    require(answer["raw_input"] == "3", "raw input must be 3")
    require(answer["interpreted_option"] == "authorize_actual_dispatch_later", "option interpretation mismatch")
    require(answer["explicit_answer_received"] is True, "explicit answer must be recorded")
    require(answer["selection_source"] == "user_message", "selection source must be user message")
    require(answer["answer_recorded"] is True, "answer must be recorded")

    effect = evidence["authorization_effect"]
    require(effect["dispatch_direction_authorized"] is True, "dispatch direction must be authorized")
    require(effect["dispatch_precheck_authorized"] is True, "dispatch precheck must be authorized")
    require(effect["actual_dispatch_authorized"] is False, "actual dispatch must not be authorized yet")
    require(effect["dispatch_allowed"] is False, "dispatch must not be allowed")
    require(effect["dispatch_performed"] is False, "dispatch must not be performed")
    require("recipient, channel, payload, and evidence destination" in effect["reason_actual_dispatch_not_authorized"], "missing reason for no actual dispatch")

    missing = evidence["missing_actual_dispatch_details"]
    for key in ["recipient", "channel", "payload", "evidence_destination", "rollback_or_cancellation_path"]:
        require(missing[key] == "", f"{key} must remain empty")
    require(missing["sensitive_data_review"] is False, "sensitive review must be false")

    for field in ["recipient", "channel", "payload", "evidence_destination", "sensitive_data_review", "rollback_or_cancellation_path"]:
        require(field in evidence["next_intake_required_fields"], f"missing required intake field: {field}")

    for phrase in ["dispatch precheck", "payload preview", "no-send dry run"]:
        require(phrase in evidence["allowed_next_scope"], f"missing allowed next scope: {phrase}")
    for phrase in ["actual dispatch", "external API write", "real KDS write", "git push", "business status upgrade"]:
        require(phrase in evidence["forbidden_until_details_complete"], f"missing forbidden action: {phrase}")

    decision = evidence["decision"]
    require(decision["resume_status"] == "resumed_by_user_answer_3", "invalid resume status")
    require(decision["next_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-PRECHECK-DETAIL-INTAKE-025", "invalid next round")
    require(decision["goal_complete"] is False, "goal must not be complete")
    require(decision["status_ceiling"] == "partial", "status ceiling must be partial")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "actual_dispatch_later_intent_recorded_details_missing",
        "interpreted_option=authorize_actual_dispatch_later",
        "actual_dispatch_authorized=false",
        "dispatch_performed=false",
        "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-PRECHECK-DETAIL-INTAKE-025",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "actual_dispatch_later_intent_recorded_details_missing"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_dispatch_authorization_answer_resumed=pass "
        "selected_option=authorize_actual_dispatch_later "
        "dispatch_precheck_authorized=true "
        "actual_dispatch_authorized=false "
        "dispatch_performed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-PRECHECK-DETAIL-INTAKE-025"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
