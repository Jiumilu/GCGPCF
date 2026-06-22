#!/usr/bin/env python3
"""Validate project-group closure for CodeGraph dev execution chain."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-project-group-closure-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-project-group-closure-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-PROJECT-GROUP-CLOSURE-010.md"


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

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-PROJECT-GROUP-CLOSURE-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-PROJECT-GROUP-CLOSURE-010", "invalid scope")
    require(evidence["status"] == "project_group_codegraph_dev_execution_chain_validated_with_document_localization_debt", "invalid status")
    require(len(evidence["evidence_chain"]) == 10, "evidence chain must contain ten rounds")

    for item in evidence["evidence_chain"]:
        require((ROOT / item["evidence"]).exists(), f"missing evidence: {item['evidence']}")
        require((ROOT / item["validator"]).exists(), f"missing validator: {item['validator']}")
        require(item["result"] == "pass", f"chain result must be pass: {item['round']}")

    for claim in [
        "business implementation completed",
        "accepted",
        "integrated",
        "production_ready",
        "GFIS CodeGraph sync-only closure completed",
        "git commit performed",
        "git push performed",
        "deployment performed",
    ]:
        require(claim in evidence["closure_claims_forbidden"], f"missing forbidden claim: {claim}")

    gfis = evidence["gfis_open_items"]
    require(gfis["codegraph_pending_added"] == 1, "GFIS pending added must remain 1")
    require(gfis["clean_reindex_authorized"] is False, "clean reindex must not be authorized")
    require(gfis["runtime_sop_e2e"] == "failed_existing_kds_coverage_missing_controlled_sources", "GFIS runtime SOP status mismatch")

    project = evidence["project_group_state"]
    require(project["gpcf_codegraph_pending_changes"] == {"added": 0, "modified": 0, "removed": 0}, "GPCF pending changes mismatch")
    require(project["document_pollution"] == "pass", "document pollution must pass")
    require(project["kds_token"] == "pass", "KDS token must pass")
    require(project["loop_document_gate"] == "rework_required", "Loop document gate must record rework")
    require(project["loop_document_gate_reason"] == "localization_debt", "Loop document gate reason mismatch")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    validators = [
        "tools/kds-sync/validate_codegraph_dev_execution_admission.py",
        "tools/kds-sync/validate_codegraph_dev_execution_pilot_pack.py",
        "tools/kds-sync/validate_codegraph_dev_execution_harness_gate.py",
        "tools/kds-sync/validate_codegraph_dev_execution_first_real_candidate.py",
        "tools/kds-sync/validate_codegraph_dev_execution_first_real_candidate_authorization.py",
        "tools/kds-sync/validate_codegraph_dev_execution_authorization_waiting.py",
        "tools/kds-sync/validate_codegraph_dev_execution_first_real_candidate_authorized.py",
        "tools/kds-sync/validate_codegraph_dev_execution_gfis_residual_drift.py",
        "tools/kds-sync/validate_codegraph_dev_execution_gfis_residual_locator.py",
        "tools/kds-sync/validate_codegraph_dev_execution_gfis_tool_state_audit_blocked.py",
    ]
    for validator in validators:
        result = run(["python3", validator])
        require(result.returncode == 0, f"validator failed: {validator}: {result.stdout}{result.stderr}")

    for phrase in [
        "CodeGraph 已经从工具层推进到开发执行层治理链",
        "codegraph_pending_added=1",
        "clean_reindex_authorized=false",
        "loop_document_gate=rework_required",
        "loop_document_gate_reason=localization_debt",
        "不声明 accepted",
        "GPCF-CODEGRAPH-DEV-EXECUTION-DOCUMENT-LOCALIZATION-DEBT-011",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"GPCF .codegraph status failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", "GPCF .codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_project_group_closure=pass "
        "evidence_chain=10 "
        "loop_document_gate=rework_required "
        "gpcf_codegraph_pending=0 "
        "gfis_pending_added=1 "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-DOCUMENT-LOCALIZATION-DEBT-011"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
