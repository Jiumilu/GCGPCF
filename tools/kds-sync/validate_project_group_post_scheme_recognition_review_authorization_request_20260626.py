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
EXTERNAL_DELEGATE_BASELINE = ROOT / "docs/harness/evidence/globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md"

AUTH_ITEMS = [
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "project_group_post_scheme_recognition_review_authorization_request_20260626 = prepared",
    "post_scheme_recognition_review_authorization_request_prepared",
    "recheck_date | `2026-06-27`",
    "live_dirty_repo_count | `7`",
    "review_boundary_repo_count | `6`",
    "noise_cleanup_repo_count | `1`",
    "request_item_count | `6`",
    "live_dirty_review_items | `6`",
    "excluded_noise_cleanup_items | `1`",
    "scheme_recognition_replay_items | `1`",
    "delegate_wrapper_review_items | `3`",
    "globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repos_current | `GlobalCloud AAAS`、`GlobalCoud GPCF`、`GlobalCloud XWAIL`、`GlobalCloud GFIS`、`GlobalCloud KDS`、`GlobalCloud SOP`",
    "noise_cleanup_repo_current | `WAS世界资产体系(.DS_Store)`",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
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
    "validate_project_group_external_loop_gate_delegate_baseline_20260627.py",
    "5.3 KDS 单仓核对卡",
    "5.4 KDS 确认后状态传导摘要",
    "5.5.1 AAAS delegated wrapper 单仓核对卡",
    "5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡",
    "5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡",
    "5.6.3 SOP delegated wrapper 确认后状态传导摘要",
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
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(POST_SCHEME_QUEUE, failures), read(EXTERNAL_DELEGATE_BASELINE, failures)])

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
