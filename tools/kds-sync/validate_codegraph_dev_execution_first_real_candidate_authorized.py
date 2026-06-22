#!/usr/bin/env python3
"""Validate the authorized first real CodeGraph development candidate evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-first-real-candidate-authorized-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-first-real-candidate-authorized-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZED-006.md"
GFIS_REGISTER = GFIS_ROOT / "docs/harness/sop-e2e/evidence/liaoning-yuanhang-contract-chain-real-receipt-empty-directory-hold-register.json"
GFIS_DOC = GFIS_ROOT / "docs/harness/sop-e2e/liaoning-yuanhang-contract-chain-real-receipt-empty-directory-hold-register.md"
GFIS_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_liaoning_yuanhang_contract_chain_real_receipt_empty_directory_hold_register.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    gfis_register = load_json(GFIS_REGISTER)
    gfis_doc = read(GFIS_DOC)
    gfis_validator = read(GFIS_VALIDATOR)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZED-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZED-006", "invalid scope")
    require(evidence["status"] == "authorized_minimal_execution_completed_with_residual_gfis_drift", "invalid status")
    require(evidence["source_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-WAITING-006", "invalid source round")

    auth = evidence["authorization"]
    require(auth["received_authorization_phrase"] == "全部授权", "authorization phrase mismatch")
    for key in [
        "commit_authorized",
        "push_authorized",
        "deployment_authorized",
        "production_write_authorized",
        "external_api_write_authorized",
        "real_kds_write_authorized",
        "real_waes_write_authorized",
    ]:
        require(auth[key] is False, f"{key} must remain false")

    candidate = evidence["candidate_task"]
    require(candidate["project"] == "GFIS", "candidate project must be GFIS")
    require(candidate["business_implementation_authorized"] is True, "candidate must be authorized")
    require(candidate["runtime_sop_e2e"] == "repair_required", "runtime SOP must remain repair_required")

    implementation = evidence["implementation_boundary"]
    require(implementation["business_status_changed"] is False, "business status must not be changed")
    require(implementation["post_change_status"] == "repair_required", "post change status must remain repair_required")
    require(len(implementation["actual_changed_files"]) == 4, "actual changed files must stay scoped to four files")

    gfis_codegraph = gfis_register.get("codegraph_evidence")
    require(isinstance(gfis_codegraph, dict), "GFIS register must contain codegraph_evidence")
    require(gfis_codegraph.get("affected_tests") == [], "GFIS codegraph affected_tests must be []")
    require(gfis_codegraph.get("fallback_reason"), "GFIS codegraph fallback_reason must be present")
    require(gfis_codegraph.get("post_change_status") == "repair_required", "GFIS post_change_status must remain repair_required")
    require("## CodeGraph Evidence" in gfis_doc, "GFIS Markdown must include CodeGraph Evidence section")
    require("codegraph_evidence must be present" in gfis_validator, "GFIS validator must enforce codegraph_evidence")

    validation = evidence["validation_results"]
    require(validation["candidate_validator"] == "pass", "candidate validator must pass")
    require(validation["gfis_runtime_sop_e2e"] == "failed_existing_kds_coverage_missing_controlled_sources", "GFIS runtime SOP failure must be recorded")

    sync = evidence["gfis_codegraph_sync"]
    require(sync["sync_performed"] is True, "GFIS CodeGraph sync must be recorded as performed")
    require(sync["status_after_sync"]["pendingChanges"] == {"added": 1, "modified": 0, "removed": 0}, "GFIS residual drift mismatch")
    require(sync["dot_codegraph_git_isolated"] is True, "GFIS .codegraph isolation must be recorded")
    require(sync["closure_status"] == "not_closed_due_residual_pending_added_1", "GFIS closure status mismatch")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "全部授权",
        "pendingChanges.added=1",
        "not_closed_due_residual_pending_added_1",
        "FAIL: KDS coverage must not have missing controlled sources",
        "不能声明业务完成",
        "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    gpcf_dot_codegraph = run(["git", "status", "--short", "--", ".codegraph"], ROOT)
    require(gpcf_dot_codegraph.returncode == 0, f"GPCF .codegraph status failed: {gpcf_dot_codegraph.stderr}")
    require(gpcf_dot_codegraph.stdout.strip() == "", "GPCF .codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_first_real_candidate_authorized=pass "
        "candidate=GFIS "
        "candidate_validator=pass "
        "runtime_sop_e2e=failed_existing_kds_coverage_missing_controlled_sources "
        "gfis_codegraph_sync=performed "
        "gfis_residual_pending_added=1 "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
