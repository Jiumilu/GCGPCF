#!/usr/bin/env python3
"""Validate the first project-group execution authorization request."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-first-execution-authorization-request-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

AUTH_ITEMS = [
    "AUTH-WAS-DELETE-DS-STORE-20260626",
    "AUTH-GPC-REVIEW-20260626",
    "AUTH-PVAOS-REVIEW-20260626",
    "AUTH-STUDIO-REVIEW-20260626",
    "AUTH-GPCF-GOVERNANCE-REVIEW-20260626",
    "AUTH-KDS-OWNER-DECISION-20260626",
    "AUTH-SOP-OWNER-DECISION-20260626",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-FIRST-EXECUTION-AUTHORIZATION-REQUEST-20260626-001",
    "project_group_first_execution_authorization_request_20260626 = prepared",
    "first_execution_authorization_request_prepared",
    "request_item_count | `7`",
    "noise_cleanup_items | `1`",
    "review_candidate_items | `4`",
    "owner_decision_items | `2`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "owner_decision_confirmed=false",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
]

REFERENCE_TOKENS = [
    "GPCF-FIRST-EXECUTION-AUTHORIZATION-REQUEST-20260626-001",
    "globalcloud-project-group-first-execution-authorization-request-20260626.md",
    "validate_project_group_first_execution_authorization_request_20260626.py",
    "first_execution_authorization_request_prepared",
]

FORBIDDEN_CLAIMS = [
    "review_allowed | `true`",
    "stage_allowed | `true`",
    "commit_allowed | `true`",
    "push_allowed | `true`",
    "delete_allowed | `true`",
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(STATUS, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in authorization request: {token}")

    for item in AUTH_ITEMS:
        if item not in doc_text:
            failures.append(f"missing authorization item: {item}")

    for token in REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive claim: {token}")

    result = {
        "gate": "project_group_first_execution_authorization_request_20260626",
        "status": "pass" if not failures else "fail",
        "request_item_count": len(AUTH_ITEMS),
        "failures": failures,
        "warnings": [
            "This validates the authorization request only; it grants no review, delete, stage, commit, push, owner decision, accepted, integrated, production, or customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
