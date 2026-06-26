#!/usr/bin/env python3
"""Validate the post-scheme-recognition review authorization request."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
POST_SCHEME_QUEUE = ROOT / "docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md"

AUTH_ITEMS = [
    "AUTH-AAAS-SCHEME-REVIEW-20260626",
    "AUTH-BRAIN-SCHEME-REVIEW-20260626",
    "AUTH-WAS-SCHEME-REVIEW-20260626",
    "AUTH-XIAOC-SCHEME-REVIEW-20260626",
    "AUTH-WAES-SCHEME-REVIEW-20260626",
    "AUTH-GPC-SCHEME-REVIEW-20260626",
    "AUTH-STUDIO-SCHEME-REVIEW-20260626",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-XWAIL-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-MMC-SCHEME-REVIEW-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-XIAOG-SCHEME-REVIEW-20260626",
    "AUTH-PVAOS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-SCHEME-REVIEW-20260626",
    "AUTH-PKC-SCHEME-REVIEW-20260626",
    "AUTH-XGD-SCHEME-REVIEW-20260626",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "project_group_post_scheme_recognition_review_authorization_request_20260626 = prepared",
    "post_scheme_recognition_review_authorization_request_prepared",
    "request_item_count | `17`",
    "scheme_review_items | `17`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "cleanup_allowed | `false`",
    "owner_decision_confirmed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "review_allowed=false",
    "stage_allowed=false",
    "commit_allowed=false",
    "push_allowed=false",
    "delete_allowed=false",
    "cleanup_allowed=false",
    "owner_decision_confirmed=false",
    "repo_specific_scheme_review_allowed",
    "authorization_boundary",
]

REFERENCE_TOKENS = [
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md",
    "validate_project_group_post_scheme_recognition_review_authorization_request_20260626.py",
    "post_scheme_recognition_review_authorization_request_prepared",
]

FORBIDDEN_CLAIMS = [
    "review_allowed | `true`",
    "stage_allowed | `true`",
    "commit_allowed | `true`",
    "push_allowed | `true`",
    "delete_allowed | `true`",
    "cleanup_allowed | `true`",
    "owner_decision_confirmed | `true`",
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
    "review_allowed=true",
    "stage_allowed=true",
    "commit_allowed=true",
    "push_allowed=true",
    "delete_allowed=true",
    "cleanup_allowed=true",
    "accepted=true",
    "integrated=true",
    "production_ready=true",
    "customer_accepted=true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(POST_SCHEME_QUEUE, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in post-scheme review authorization request: {token}")

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
        "gate": "project_group_post_scheme_recognition_review_authorization_request_20260626",
        "status": "pass" if not failures else "fail",
        "request_item_count": len(AUTH_ITEMS),
        "failures": failures,
        "warnings": [
            "This validates the post-scheme review authorization request only; it grants no review, stage, commit, push, cleanup, owner decision, accepted, integrated, production, or customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
