#!/usr/bin/env python3
"""Validate the Wave1 receipt-to-pre-execution bridge audit."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-receipt-pre-execution-bridge-audit-20260627.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-WAVE1-RECEIPT-PRE-EXECUTION-BRIDGE-001.md"
REQUEST = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-authorization-request-20260626.md"
LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-authorization-receipt-ledger-20260626.md"
COMMAND_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-execution-command-pack-20260626.md"
ENV_READINESS = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-pre-execution-environment-readiness-20260626.md"

REQUIRED_TOKENS = [
    "project_group_wave1_receipt_pre_execution_bridge_audit_20260627 = controlled",
    "bridge_status = wave1_request_to_receipt_ledger_to_command_pack_to_environment_order_confirmed",
    "wave1_authorization_request_status = prepared",
    "wave1_authorization_receipt_ledger_status = controlled",
    "wave1_execution_command_pack_status = controlled",
    "wave1_pre_execution_environment_status = controlled",
    "wave1_entry_blocked_by_pre_review = true",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repo_count = 6",
    "noise_cleanup_repo_count = 1",
    "review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)",
    "GPCF-WAVE1-AUTHORIZATION-REQUEST-20260626-001",
    "GPCF-WAVE1-AUTHORIZATION-RECEIPT-LEDGER-20260626-001",
    "GPCF-WAVE1-EXECUTION-COMMAND-PACK-20260626-001",
    "GPCF-WAVE1-PRE-EXECUTION-ENVIRONMENT-READINESS-20260626-001",
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
            read(REQUEST, failures),
            read(LEDGER, failures),
            read(COMMAND_PACK, failures),
            read(ENV_READINESS, failures),
        ]
    )

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing wave1 bridge token: {token}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop:
            failures.append(f"missing loop section: {section}")

    for token in [
        "project_group_wave1_authorization_request_20260626 = prepared",
        "project_group_wave1_authorization_receipt_ledger_20260626 = controlled",
        "project_group_wave1_execution_command_pack_20260626 = controlled",
        "project_group_wave1_pre_execution_environment_readiness_20260626 = controlled",
    ]:
        if token not in refs:
            failures.append(f"missing prerequisite token: {token}")

    result = {
        "gate": "project_group_wave1_receipt_pre_execution_bridge_audit_20260627",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "This validates Wave1 bridge audit structure only; it does not grant authorization, write receipts, execute command packs, or grant accepted/integrated/customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
