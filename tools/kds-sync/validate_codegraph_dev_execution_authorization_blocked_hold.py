#!/usr/bin/env python3
"""Validate CodeGraph authorization blocked-hold evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-authorization-blocked-hold-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-authorization-blocked-hold-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-BLOCKED-HOLD-023.md"
ANSWER = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-authorization-answer-20260626.json"


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
    answer = load_json(ANSWER)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-BLOCKED-HOLD-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-BLOCKED-HOLD-023", "invalid scope")
    require(evidence["status"] == "blocked_hold_requires_user_authorization_or_real_input", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(answer["status"] == "no_explicit_answer_default_not_authorized", "answer source status mismatch")

    answer_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_dispatch_authorization_answer.py"])
    require(answer_gate.returncode == 0, f"answer gate failed: {answer_gate.stdout}{answer_gate.stderr}")

    blocked = evidence["blocked_audit"]
    require(blocked["same_blocker_repeated"] is True, "same blocker must be repeated")
    require(blocked["consecutive_goal_turns_observed"] >= 3, "blocked audit requires at least 3 turns")
    require(blocked["meaningful_progress_without_user_input_remaining"] is False, "must require user input for further progress")
    for phrase in [
        "dispatch_authorization_not_received",
        "effective_authorization_not_authorized",
        "real_source_input_not_arrived",
        "goal_complete_false",
    ]:
        require(phrase in blocked["blocking_conditions"], f"missing blocking condition: {phrase}")

    state = evidence["current_state"]
    require(state["development_state_proven"] is True, "development state must be proven")
    require(state["benefit_quantified"] is True, "benefit must be quantified")
    require(state["goal_complete"] is False, "goal must not be complete")
    require(state["effective_authorization"] == "not_authorized", "authorization must be not_authorized")
    require(state["dispatch_allowed"] is False, "dispatch must not be allowed")
    require(state["dispatch_performed"] is False, "dispatch must not be performed")
    require(state["real_input_blocked"] is True, "real input must be blocked")
    require(state["runtime_state"] == "not_verified", "runtime state must not be verified")

    require(len(evidence["resume_conditions"]) == 4, "expected four resume conditions")
    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "blocked_hold_requires_user_authorization_or_real_input",
        "same_blocker_repeated=true",
        "consecutive_goal_turns_observed=3",
        "meaningful_progress_without_user_input_remaining=false",
        "effective_authorization=not_authorized",
        "goal_complete=false",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "blocked_hold_requires_user_authorization_or_real_input"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_authorization_blocked_hold=blocked "
        "goal_complete=false "
        "development_state_proven=true "
        "benefit_quantified=true "
        "effective_authorization=not_authorized "
        "resume_requires=user_authorization_or_real_input"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
