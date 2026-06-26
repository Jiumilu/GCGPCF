#!/usr/bin/env python3
"""Validate CodeGraph development-execution benefit proof evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-benefit-proof-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-benefit-proof-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-PROOF-015.md"
TASK_INTAKE = ROOT / "docs/harness/evidence/codegraph-dev-execution-business-task-intake-008.json"
AUTHORIZED = ROOT / "docs/harness/evidence/codegraph-dev-execution-first-real-candidate-authorized-20260622.json"


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
    task = load_json(TASK_INTAKE)
    authorized = load_json(AUTHORIZED)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-BENEFIT-PROOF-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-PROOF-015", "invalid scope")
    require(evidence["status"] == "development_state_benefit_proof_ready", "invalid status")

    task_gate = run([
        "python3",
        "tools/kds-sync/validate_codegraph_task_intake_gate.py",
        "--task-file",
        "docs/harness/evidence/codegraph-dev-execution-business-task-intake-008.json",
    ])
    require(task_gate.returncode == 0, f"task intake gate failed: {task_gate.stdout}{task_gate.stderr}")

    authorized_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_first_real_candidate_authorized.py"])
    require(authorized_gate.returncode == 0, f"authorized candidate gate failed: {authorized_gate.stdout}{authorized_gate.stderr}")

    proof = evidence["business_execution_layer_proof"]
    require(proof["codegraph_required"] is True, "CodeGraph must be required")
    require(proof["task_intake_gate_passed"] is True, "task intake gate must be recorded as passed")
    require(proof["authorized_minimal_execution_validator_passed"] is True, "authorized candidate validator must be recorded as passed")
    for key in [
        "pre_change_analysis_present",
        "target_nodes_present",
        "files_allowed_to_change_present",
        "files_not_to_touch_present",
        "expected_tests_present",
        "affected_tests_empty_with_fallback_reason",
    ]:
        require(proof[key] is True, f"{key} must be true")

    metrics = evidence["benefit_metrics"]
    require(metrics["manual_scan_files_before"] == task["efficiency_metrics"]["manual_scan_files"], "manual scan baseline mismatch")
    require(metrics["codegraph_candidate_files_after"] == task["efficiency_metrics"]["codegraph_candidate_files"], "candidate files mismatch")
    require(metrics["manual_scan_reduction_files"] == 78, "manual scan reduction files mismatch")
    require(metrics["manual_scan_reduction_percent"] == 97.5, "manual scan reduction percent mismatch")
    require(metrics["affected_tests"] == [], "affected_tests must remain empty")
    require(metrics["fallback_tests_recorded"] is True, "fallback tests must be recorded")
    require(metrics["missed_impact_count"] == 0, "missed impact count must be zero")
    require(metrics["review_rework_count"] == 0, "review rework count must be zero")

    allowed = set(authorized["implementation_boundary"]["files_allowed_to_change"])
    changed = set(authorized["implementation_boundary"]["actual_changed_files"])
    require(len(changed) == metrics["actual_changed_files_authorized_candidate"], "actual changed file count mismatch")
    require(changed.issubset(allowed), "authorized changed files must stay inside allowed scope")
    require(metrics["actual_changed_files_outside_allowed_scope"] == 0, "outside allowed scope must be zero")

    selection = task["test_selection"]
    require(selection["affected_tests"] == [], "task affected_tests must be empty")
    require(selection["fallback_tests"], "task fallback_tests must be present")
    require(selection["fallback_reason"], "task fallback_reason must be present")
    require(authorized["codegraph_evidence_added_to_gfis"]["fallback_reason"], "authorized fallback_reason must be present")
    require(authorized["validation_results"]["gfis_runtime_sop_e2e"] == "failed_existing_kds_coverage_missing_controlled_sources", "GFIS runtime SOP blocker mismatch")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "development_state_benefit_proof_ready",
        "manual_scan_files_before",
        "codegraph_candidate_files_after",
        "97.5",
        "actual_changed_files_outside_allowed_scope=0",
        "FAIL: KDS coverage must not have missing controlled sources",
        "GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_benefit_proof=pass "
        "manual_scan_files=80 "
        "codegraph_candidate_files=2 "
        "manual_scan_reduction_percent=97.5 "
        "changed_files_outside_allowed_scope=0 "
        "affected_tests=0 fallback_tests=recorded "
        "business_implementation_completed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
