#!/usr/bin/env python3
"""Validate the project-group operational blocker resolution matrix."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-operational-blocker-resolution-matrix-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

BLOCKER_IDS = [
    "DEP-WAES-XWAIL-AAAS-001",
    "DEP-KDS-BRAIN-001",
    "DEP-GFIS-GPC-PVAOS-SCAAS-001",
    "DEP-GPCF-ALL-PROJECTS-001",
    "CS-GPCF-USER-FEEDBACK-001",
    "CS-SCAAS-UAT-READINESS-001",
]

REQUIRED_TOKENS = [
    "GPCF-OPERATIONAL-BLOCKER-RESOLUTION-MATRIX-20260626-001",
    "project_group_operational_blocker_resolution_matrix_20260626 = controlled",
    "blocker_count = 6",
    "dependency_blocker_count = 4",
    "customer_satisfaction_blocker_count = 2",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "operational_gate_after_this_doc = blocked",
    "WAES lint/runtime",
    "XWAIL/AaaS",
    "KDS RAG",
    "Brain review",
    "GFIS",
    "GPC",
    "PVAOS",
    "SCaaS",
    "post-scheme 17 仓",
    "用户反馈记录",
    "SCaaS UAT readiness record",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

GOVERNANCE_TOKENS = [
    "globalcloud-project-group-operational-blocker-resolution-matrix-20260626.md",
    "validate_project_group_operational_blocker_resolution_matrix_20260626.py",
    "project_group_operational_blocker_resolution_matrix_20260626 = controlled",
    "operational_blocker_resolution_matrix_controlled",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
    "operational_gate_after_this_doc = pass",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc = read(DOC, failures)
    governance = read(BOARD, failures) + "\n" + read(CORE_REGISTER, failures)

    for blocker_id in BLOCKER_IDS:
        if blocker_id not in doc:
            failures.append(f"missing blocker id: {blocker_id}")

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing matrix token: {token}")

    for token in GOVERNANCE_TOKENS:
        if token not in governance:
            failures.append(f"missing governance token: {token}")

    matrix_rows = [line for line in doc.splitlines() if line.startswith("| `DEP-") or line.startswith("| `CS-")]
    if len(matrix_rows) != 6:
        failures.append(f"expected 6 blocker matrix rows, found {len(matrix_rows)}")

    combined = doc + "\n" + governance
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_operational_blocker_resolution_matrix_20260626",
        "status": "pass" if not failures else "fail",
        "blocker_count": 6,
        "dependency_blocker_count": 4,
        "customer_satisfaction_blocker_count": 2,
        "failures": failures,
        "warnings": [
            "This validates blocker resolution structure only; it does not clear dependency/customer gates, execute tasks, grant authorization, or approve accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
