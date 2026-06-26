#!/usr/bin/env python3
"""Validate CodeGraph development-state normal-work evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / "09-status/codegraph-development-state-control-memory-20260626.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-development-state-normal-work-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-development-state-normal-work-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEVELOPMENT-STATE-NORMAL-WORK-017.md"
BENEFIT_PROOF = ROOT / "docs/harness/evidence/codegraph-dev-execution-benefit-proof-20260626.json"
REGRESSION_WATCH = ROOT / "docs/harness/evidence/codegraph-dev-execution-benefit-regression-watch-20260626.json"
GITIGNORE = ROOT / ".gitignore"


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
    proof = load_json(BENEFIT_PROOF)
    regression = load_json(REGRESSION_WATCH)
    memory = read(MEMORY)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    gitignore = read(GITIGNORE)

    require(evidence["evidence_id"] == "CODEGRAPH-DEVELOPMENT-STATE-NORMAL-WORK-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEVELOPMENT-STATE-NORMAL-WORK-017", "invalid scope")
    require(evidence["status"] == "development_state_normal_work_verified", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")

    proof_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_benefit_proof.py"])
    require(proof_gate.returncode == 0, f"benefit proof gate failed: {proof_gate.stdout}{proof_gate.stderr}")
    regression_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_benefit_regression_watch.py"])
    require(regression_gate.returncode == 0, f"regression watch gate failed: {regression_gate.stdout}{regression_gate.stderr}")

    checks = evidence["development_state_checks"]
    require(checks["benefit_proof_validator_passed"] is True, "benefit proof validator must be recorded as passed")
    require(checks["benefit_regression_watch_validator_passed"] is True, "regression watch validator must be recorded as passed")
    require(checks["task_intake_gate_required"] is True, "task intake gate must be required")
    require(checks["fallback_required_when_affected_tests_empty"] is True, "fallback must be required")
    require(checks["codegraph_git_isolation_required"] is True, "CodeGraph Git isolation must be required")
    require(checks["dirty_worktree_allowed_as_development_state"] is True, "dirty worktree must be explicitly development-state only")
    require(checks["git_clean_required"] is False, "git clean must not be required by this development-state evidence")

    metrics = evidence["current_metrics"]
    proof_metrics = proof["benefit_metrics"]
    regression_sample = regression["current_sample"]
    require(metrics["manual_scan_files_before"] == proof_metrics["manual_scan_files_before"], "manual scan baseline mismatch")
    require(metrics["codegraph_candidate_files_after"] == proof_metrics["codegraph_candidate_files_after"], "candidate files mismatch")
    require(metrics["manual_scan_reduction_percent"] == regression_sample["manual_scan_reduction_percent"], "reduction percent mismatch")
    require(metrics["manual_scan_reduction_percent"] >= 80.0, "manual scan reduction below development-state threshold")
    require(metrics["actual_changed_files_outside_allowed_scope"] == 0, "outside allowed scope must be zero")
    require(metrics["missed_impact_count"] == 0, "missed impact count must be zero")
    require(metrics["review_rework_count"] == 0, "review rework count must be zero")
    require(metrics["affected_tests"] == [], "affected_tests must remain empty in current sample")
    require(metrics["fallback_tests_recorded"] is True, "fallback tests must be recorded")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "当前会话按开发态处理，不按运行态、部署态或生产态处理。",
        "development_state_benefit_proof_ready",
        "benefit_regression_watch_active",
        "97.5%",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017",
    ]:
        require(phrase in memory, f"memory missing phrase: {phrase}")

    for phrase in [
        "development_state_normal_work_verified",
        "当前只按开发态处理，不按运行态处理",
        "dirty_worktree_allowed_as_development_state=true",
        "git_clean_required=false",
        "manual_scan_reduction_percent",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "runtime_mode=false"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    require(".codegraph/" in gitignore, ".gitignore must keep .codegraph/ isolated")
    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_development_state_normal_work=pass "
        "operation_mode=development_state "
        "runtime_mode=false "
        "manual_scan_reduction_percent=97.5 "
        "changed_files_outside_allowed_scope=0 "
        "missed_impact_count=0 "
        "review_rework_count=0 "
        "git_clean_required=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
