#!/usr/bin/env python3
"""Validate CodeGraph development-execution goal completion audit."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-goal-completion-audit-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-goal-completion-audit-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-GOAL-COMPLETION-AUDIT-021.md"


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
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-GOAL-COMPLETION-AUDIT-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-GOAL-COMPLETION-AUDIT-021", "invalid scope")
    require(evidence["status"] == "goal_partially_satisfied_development_state_proven", "invalid status")
    require(evidence["objective_under_audit"] == "从治理层推到业务执行层并证明收益", "invalid objective")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")

    for command in [
        ["python3", "tools/kds-sync/validate_codegraph_dev_execution_benefit_proof.py"],
        ["python3", "tools/kds-sync/validate_codegraph_dev_execution_benefit_regression_watch.py"],
        ["python3", "tools/kds-sync/validate_codegraph_development_state_normal_work.py"],
        ["python3", "tools/kds-sync/validate_codegraph_dev_execution_real_input_authorization_waiting.py"],
    ]:
        result = run(command)
        require(result.returncode == 0, f"gate failed: {' '.join(command)} {result.stdout}{result.stderr}")

    audits = evidence["requirement_audit"]
    require(len(audits) == 7, "expected seven audit requirements")
    status_by_requirement = {item["requirement"]: item["status"] for item in audits}
    require(status_by_requirement["CodeGraph leaves governance-only layer and becomes development task admission evidence."] == "proven", "governance-to-dev admission must be proven")
    require(status_by_requirement["CodeGraph constrains business development scope before implementation."] == "proven_for_development_state", "scope control must be proven for development state")
    require(status_by_requirement["CodeGraph contributes to test selection and fallback reasoning."] == "proven_for_current_sample", "test fallback must be proven")
    require(status_by_requirement["CodeGraph benefit is quantified."] == "proven_for_current_sample", "benefit must be quantified")
    require(status_by_requirement["CodeGraph is guarded against regression."] == "proven_for_current_sample", "regression guard must be proven")
    require(status_by_requirement["Real business source inputs are ready for runtime business execution."] == "not_proven_blocked", "real input must remain blocked")
    require(status_by_requirement["Dispatch authorization exists to request real source inputs."] == "not_proven_waiting", "dispatch authorization must remain waiting")

    decision = evidence["completion_decision"]
    require(decision["goal_complete"] is False, "goal must not be complete")
    require(decision["current_status"] == "development_state_proven_real_input_blocked", "invalid current status")
    require(decision["status_ceiling"] == "partial", "status ceiling must be partial")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "goal_partially_satisfied_development_state_proven",
        "goal_complete=false",
        "manual_scan_reduction_percent=97.5",
        "valid_source_records=0",
        "authorization_received=false",
        "effective_authorization=not_authorized",
        "development_state_proven_real_input_blocked",
        "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-022",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "goal_partially_satisfied_development_state_proven"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_goal_completion_audit=partial "
        "goal_complete=false "
        "development_state_proven=true "
        "benefit_quantified=true "
        "real_input_blocked=true "
        "dispatch_authorization=not_authorized "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-AUTHORIZATION-ANSWER-022"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
