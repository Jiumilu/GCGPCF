#!/usr/bin/env python3
"""Validate the authorization-to-pre-execution total bridge audit."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-to-pre-execution-total-bridge-audit-20260627.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-AUTHORIZATION-TO-PRE-EXECUTION-TOTAL-BRIDGE-001.md"
AUTH_LAYER = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md"
HUMAN_CONFIRM = ROOT / "docs/harness/evidence/globalcloud-project-group-human-confirmation-request-20260625.md"
ROUTING = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-routing-20260625.md"
REVIEW_WAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-review-auth-pre-wave1-wave1-bridge-audit-20260627.md"
WAVE1_PRE = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-receipt-pre-execution-bridge-audit-20260627.md"
EXEC_PRE = ROOT / "docs/harness/evidence/globalcloud-project-group-execution-receipt-pre-execution-bridge-audit-20260627.md"

REQUIRED_TOKENS = [
    "project_group_authorization_to_pre_execution_total_bridge_audit_20260627 = controlled",
    "bridge_status = authorization_chain_to_pre_execution_chain_order_confirmed",
    "authorization_layer_status = prepared",
    "human_confirmation_request_status = prepared",
    "authorization_routing_status = prepared",
    "review_auth_pre_wave1_wave1_bridge_status = controlled",
    "wave1_receipt_pre_execution_bridge_status = controlled",
    "execution_receipt_pre_execution_bridge_status = controlled",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repo_count = 6",
    "noise_cleanup_repo_count = 1",
    "review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)",
    "validate_project_group_current_state_baseline_refresh_20260626.py",
    "validate_project_group_dev_task_queue_20260626.py",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc = read(DOC, failures)
    loop = read(LOOP, failures)
    refs = "\n".join(
        [
            read(AUTH_LAYER, failures),
            read(HUMAN_CONFIRM, failures),
            read(ROUTING, failures),
            read(REVIEW_WAVE1, failures),
            read(WAVE1_PRE, failures),
            read(EXEC_PRE, failures),
        ]
    )

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing total bridge token: {token}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop:
            failures.append(f"missing loop section: {section}")

    for token in [
        "authorization_layer_matrix = prepared",
        "human_confirmation_request = prepared",
        "project_group_authorization_routing = prepared",
        "project_group_review_auth_pre_wave1_wave1_bridge_audit_20260627 = controlled",
        "project_group_wave1_receipt_pre_execution_bridge_audit_20260627 = controlled",
        "project_group_execution_receipt_pre_execution_bridge_audit_20260627 = controlled",
    ]:
        if token not in refs:
            failures.append(f"missing prerequisite token: {token}")

    result = {
        "gate": "project_group_authorization_to_pre_execution_total_bridge_audit_20260627",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "This validates the total bridge audit structure only; it does not grant authorization, write receipts, execute command packs, or grant accepted/integrated/customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
