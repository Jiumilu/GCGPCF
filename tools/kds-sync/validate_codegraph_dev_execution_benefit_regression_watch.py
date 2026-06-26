#!/usr/bin/env python3
"""Validate CodeGraph development-execution benefit regression watch evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-benefit-regression-watch-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-benefit-regression-watch-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016.md"
BENEFIT_PROOF = ROOT / "docs/harness/evidence/codegraph-dev-execution-benefit-proof-20260626.json"


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
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-BENEFIT-REGRESSION-WATCH-016", "invalid scope")
    require(evidence["status"] == "benefit_regression_watch_active", "invalid status")
    require(proof["status"] == "development_state_benefit_proof_ready", "benefit proof status mismatch")

    proof_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_benefit_proof.py"])
    require(proof_gate.returncode == 0, f"benefit proof gate failed: {proof_gate.stdout}{proof_gate.stderr}")

    thresholds = evidence["regression_thresholds"]
    sample = evidence["current_sample"]
    proof_metrics = proof["benefit_metrics"]

    require(sample["manual_scan_reduction_percent"] == proof_metrics["manual_scan_reduction_percent"], "manual scan percent mismatch")
    require(sample["manual_scan_reduction_files"] == proof_metrics["manual_scan_reduction_files"], "manual scan reduction file mismatch")
    require(sample["manual_scan_reduction_percent"] >= thresholds["minimum_manual_scan_reduction_percent"], "manual scan reduction regressed")
    require(sample["changed_files_outside_allowed_scope"] <= thresholds["maximum_changed_files_outside_allowed_scope"], "scope control regressed")
    require(sample["missed_impact_count"] <= thresholds["maximum_missed_impact_count"], "missed impact regressed")
    require(sample["review_rework_count"] <= thresholds["maximum_review_rework_count"], "review rework regressed")
    require(sample["affected_tests"] == [], "affected_tests sample must remain empty")
    require(sample["fallback_tests_recorded"] is True, "fallback tests must be recorded")
    require(sample["business_implementation_completed"] is False, "business implementation must not be completed")

    for key, value in evidence["regression_results"].items():
        require(value is False, f"{key} must be false")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    stop = evidence["stop_boundary"]
    require(stop["stop_type"] == "benefit_regression_watch_active", "invalid stop type")
    require(stop["status_ceiling"] == "partial", "status ceiling must be partial")

    for phrase in [
        "benefit_regression_watch_active",
        "minimum_manual_scan_reduction_percent",
        "97.5",
        "manual_scan_reduction_regression=false",
        "scope_control_regression=false",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_benefit_regression_watch=pass "
        "manual_scan_reduction_percent=97.5 "
        "minimum_threshold=80.0 "
        "scope_control_regression=false "
        "missed_impact_regression=false "
        "review_rework_regression=false "
        "business_implementation_completed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
