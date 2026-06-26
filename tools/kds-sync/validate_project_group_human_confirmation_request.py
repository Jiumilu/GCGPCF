#!/usr/bin/env python3
"""Validate project-group human confirmation request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-human-confirmation-request-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_DOC_TOKENS = [
    "GlobalCloud 项目群提交前人工确认请求包 2026-06-25",
    "GPCF-HUMAN-CONFIRMATION-REQUEST-001",
    "human_confirmation_request = prepared",
    "PKG-GPC-EVIDENCE-BROWSER-20260625",
    "PKG-PVAOS-RELEASE-GATE-20260625",
    "PKG-GPCF-GOVERNANCE-EVIDENCE-20260625",
    "PKG-GPCF-KDS-MIRROR-20260625",
    "HOLD-WAS-SYSTEM-NOISE-20260625",
    "HOLD-KDS-FUNDING-REPORT-20260625",
    "HOLD-SOP-WUHAN-SCENARIO-20260625",
    "allow_review = true/false",
    "allow_stage = true/false",
    "allow_commit = true/false",
    "allow_push = true/false",
    "allow_delete_ds_store = true/false",
    "business_owner_confirmed = true/false",
    "scenario_owner_confirmed = true/false",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "confirmation_item_count = 7",
    "review_packages = 4",
    "hold_packages = 3",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-HUMAN-CONFIRMATION-REQUEST-001",
    "globalcloud-project-group-human-confirmation-request-20260625.md",
    "validate_project_group_human_confirmation_request.py",
    "project_group_human_confirmation_request = prepared",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
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
    doc_text = read(EVIDENCE_DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in human confirmation request: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive authorization claim: {token}")

    result = {
        "gate": "project_group_human_confirmation_request",
        "status": "pass" if not failures else "fail",
        "confirmation_request": "prepared",
        "failures": failures,
        "warnings": [
            "This validates a confirmation request only; it does not grant review, stage, commit, push, delete, accepted, integrated, or customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
