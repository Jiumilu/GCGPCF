#!/usr/bin/env python3
"""Validate the first real candidate dry-run for CodeGraph development execution."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-first-real-candidate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-first-real-candidate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004", "invalid scope")
    require(evidence["status"] == "first_real_candidate_dry_run_ready", "invalid status")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005", "invalid next round")

    candidate = evidence["candidate_task"]
    require(candidate["project"] == "GFIS", "candidate project must be GFIS")
    require(candidate["business_implementation_authorized"] is False, "business implementation must not be authorized")
    require(candidate["business_files_changed"] == [], "business files must not change")

    repo = evidence["codegraph_source_repo"]
    require(repo["name"] == "GlobalCloud GFIS", "source repo mismatch")
    require(repo["initialized"] is True, "source repo CodeGraph must be initialized")
    require(repo["pending_changes"]["added"] == 1, "GFIS pending added drift must be recorded")
    require(repo["git_isolated_codegraph"] is True, "GFIS .codegraph isolation must be recorded")

    target = "scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py"
    pre_change = evidence["pre_change_analysis"]
    require(pre_change["target_nodes"] == [target], "target node mismatch")
    require(pre_change["node_inspection"]["lines"] == 211, "node line count mismatch")
    require(pre_change["node_inspection"]["symbol_count"] == 20, "symbol count mismatch")
    require(pre_change["node_inspection"]["indexed_dependents"] == 0, "indexed dependents must be zero")
    require(pre_change["affected"]["changedFiles"] == [target], "affected changed file mismatch")
    require(pre_change["affected"]["affectedTests"] == [], "affected tests must be empty")
    require(pre_change["affected"]["totalDependentsTraversed"] == 0, "dependent traversal must be zero")

    constraints = evidence["implementation_constraints"]
    require(constraints["files_allowed_to_change"] == [], "files_allowed_to_change must stay empty")
    require("GFIS real receipt intake directories" in constraints["files_not_to_touch"], "GFIS intake directories must be protected")
    require(".codegraph/**" in constraints["files_not_to_touch"], ".codegraph must be protected")

    selection = evidence["test_selection"]
    require(selection["affected_tests"] == [], "affected_tests must remain empty")
    require(selection["fallback_tests"], "fallback tests must be recorded")
    require("affectedTests=[]" in selection["fallback_reason"], "fallback reason must cite affectedTests=[]")

    codegraph = evidence["codegraph_evidence"]
    require(codegraph["changed_files"] == [], "changed_files must stay empty")
    require(codegraph["post_change_status"] == "first_real_candidate_dry_run_recorded", "post_change_status mismatch")

    dry_run = evidence["harness_gate_dry_run"]
    require(dry_run["gate"] == "pass", "Harness dry-run gate must pass")
    require(dry_run["business_implementation_blocked_until_authorized"] is True, "implementation must remain blocked until authorized")

    observation = evidence["candidate_runtime_observation"]
    require(observation["runtime_sop_e2e"] == "repair_required", "GFIS runtime SOP must remain repair_required")
    for key in ["review_queue", "runtime_intake", "waes_review", "verified"]:
        require(observation[key] == 0, f"{key} must remain zero")

    metrics = evidence["efficiency_metrics"]
    require(metrics["manual_scan_files"] == 80, "manual scan baseline mismatch")
    require(metrics["codegraph_candidate_files"] == 2, "CodeGraph candidate count mismatch")
    require(metrics["actual_changed_files"] == 0, "actual changed files must be zero")
    require(metrics["missed_impact_count"] == 0, "missed impact must be zero")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004",
        "不进入业务实现",
        "affectedTests=[]",
        "fallback_reason",
        "runtime_sop_e2e=repair_required",
        "未运行 GFIS sync",
        "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_first_real_candidate=pass "
        "candidate=GFIS "
        "target_nodes=1 "
        "affected_tests=0 "
        "business_implementation=false "
        "runtime_sop_e2e=repair_required "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
