#!/usr/bin/env python3
"""Validate XWAIL-WAES-AaaS contract precheck evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/XWAIL/evidence/xwail-waes-aaas-contract-precheck-20260625.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
STATUS_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
DEPENDENCY_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md"

REQUIRED_DOC_TOKENS = [
    "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001",
    "xwail_waes_aaas_contract_precheck = pass",
    "xwail_status_candidate | `integration_precheck_candidate`",
    "aaas_status_candidate | `integration_precheck_candidate`",
    "waes_status | `repair_required / authorization_boundary`",
    "commands_passed | 7",
    "commands_failed | 0",
    "WAES -> XWAIL -> AaaS",
    "gate=xwail_min_validator",
    "gate=xap_build_check",
    "gate=xap_verify",
    "gate=aaas_service_package",
    "gate=aaas_metering",
    "gate=aaas_sla",
    "gate=aaas_evidence_requirements",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "waes_publication = false",
    "aaas_real_billing = false",
    "customer_subscription = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "xwail-waes-aaas-contract-precheck-20260625.md",
    "validate_xwail_waes_aaas_contract_precheck.py",
    "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001",
    "integration_precheck_candidate",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "waes_publication = true",
    "aaas_real_billing = true",
    "customer_subscription = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join(
        [
            read(REGISTER, failures),
            read(BOARD, failures),
            read(STATUS_MATRIX, failures),
            read(DEPENDENCY_MATRIX, failures),
        ]
    )

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in contract precheck evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "xwail_waes_aaas_contract_precheck",
        "status": "pass" if not failures else "fail",
        "commands_checked": 7,
        "candidate_status": "integration_precheck_candidate" if not failures else "failed",
        "failures": failures,
        "warnings": [
            "This validates local contract precheck evidence only; it does not prove WAES publication, AaaS real billing, customer subscription, accepted, integrated, production, or customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
