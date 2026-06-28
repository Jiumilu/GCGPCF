#!/usr/bin/env python3
"""Validate GFIS development-ready authorization request boundary."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/gfis-development-ready-for-real-business-validation-authorization-request-20260628.md"

REQUIRED_TOKENS = [
    "gfis_development_ready_for_real_business_validation_authorization_request_20260628 = prepared",
    "mainline = GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001",
    "request_item_count = 2",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "development_lane = continue_allowed",
    "development_ready_for_real_business_validation = candidate",
    "real_business_validation_lane = pending_source_of_record",
    "acceptance_lane = not_started",
    "production_lane = not_started",
    "gfis_git_dirty = true",
    "gfis_dirty_count = 91",
    "gfis_untracked_count = 38",
    "project_group_git_gate = partial",
    "AUTH-GFIS-DEV-READY-CANDIDATE-20260628",
    "AUTH-GFIS-DIRTY-EVIDENCE-REVIEW-20260628",
    "validate_loop_v11_slimming_delivery_recovery.py",
    "validate_loop_v11_delivery_boundary.py",
    "validate_gfis_real_fact_entry_gate.py",
    "validate_loop_v11_gfis_authorization_boundary.py",
    "project_group_git_clean_gate.py --allow-non-pass-exit-zero",
    "loop_document_gate.py --check-only",
    "validate_gfis_runtime_sop_e2e_min_001.py",
    "authorization_granted = false",
    "action_executed = false",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "cleanup_allowed = false",
    "real_business_verified = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "overall_status = partial_repair",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "cleanup_allowed = true",
    "real_business_verified = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "真实 KDS API 已同步",
    "真实业务验证已完成",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_gfis_development_ready_authorization_request_20260628: {message}")


def main() -> int:
    if not DOC.exists():
        fail(f"missing file: {DOC.relative_to(ROOT)}")
    text = DOC.read_text(encoding="utf-8", errors="ignore")

    for token in REQUIRED_TOKENS:
        if token not in text:
            fail(f"missing token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            fail(f"forbidden token: {token}")

    print(
        "gfis_development_ready_authorization_request_20260628=pass "
        "status=prepared request_item_count=2 authorization_granted_count=0 "
        "action_executed_count=0 development_ready_for_real_business_validation=candidate "
        "real_business_validation_lane=pending_source_of_record stage_allowed=false "
        "commit_allowed=false push_allowed=false accepted=false integrated=false "
        "production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
