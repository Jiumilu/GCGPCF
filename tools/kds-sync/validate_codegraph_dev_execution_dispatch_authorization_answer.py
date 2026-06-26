#!/usr/bin/env python3
"""Validate CodeGraph dispatch authorization answer evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-authorization-answer-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-authorization-answer-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-022.md"
GOAL_AUDIT = ROOT / "docs/harness/evidence/codegraph-dev-execution-goal-completion-audit-20260626.json"


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
    goal_audit = load_json(GOAL_AUDIT)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-022", "invalid scope")
    require(evidence["status"] == "no_explicit_answer_default_not_authorized", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(goal_audit["completion_decision"]["goal_complete"] is False, "goal audit must remain incomplete")

    audit_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_goal_completion_audit.py"])
    require(audit_gate.returncode == 0, f"goal completion audit gate failed: {audit_gate.stdout}{audit_gate.stderr}")

    answer = evidence["answer_state"]
    require(answer["explicit_answer_received"] is False, "explicit answer must be false")
    require(answer["selected_option"] == "not_authorized_keep_prepared", "selected option must be default keep prepared")
    require(answer["selection_source"] == "default_if_no_answer", "selection source must be default")
    require(answer["effective_authorization"] == "not_authorized", "effective authorization must be not_authorized")
    require(answer["dispatch_precheck_authorized"] is False, "dispatch precheck must not be authorized")
    require(answer["actual_dispatch_authorized"] is False, "actual dispatch must not be authorized")
    require(answer["dispatch_allowed"] is False, "dispatch must not be allowed")
    require(answer["dispatch_performed"] is False, "dispatch must not be performed")

    require(set(evidence["available_user_options"]) == {
        "not_authorized_keep_prepared",
        "authorize_dispatch_precheck_only",
        "authorize_actual_dispatch_later",
    }, "available options mismatch")

    decision = evidence["current_decision"]
    require(decision["collection_pack"] == "prepared", "collection pack must remain prepared")
    require(decision["dispatch_authorization"] == "not_authorized", "dispatch authorization must be not_authorized")
    require(decision["next_action_without_user_answer"] == "hold", "next action without user answer must be hold")
    require(decision["real_business_execution"] == "blocked_until_real_source_input_arrives", "real business execution must remain blocked")
    require(decision["runtime_state"] == "not_verified", "runtime must not be verified")
    require(decision["goal_complete"] is False, "goal must not be complete")
    require(decision["status_ceiling"] == "partial", "status ceiling must be partial")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "no_explicit_answer_default_not_authorized",
        "explicit_answer_received=false",
        "selected_option=not_authorized_keep_prepared",
        "effective_authorization=not_authorized",
        "dispatch_precheck_authorized=false",
        "dispatch_performed=false",
        "goal_complete=false",
        "GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-BLOCKED-HOLD-023",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "no_explicit_answer_default_not_authorized"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_dispatch_authorization_answer=default_not_authorized "
        "explicit_answer_received=false "
        "selected_option=not_authorized_keep_prepared "
        "dispatch_allowed=false "
        "dispatch_performed=false "
        "goal_complete=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-BLOCKED-HOLD-023"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
