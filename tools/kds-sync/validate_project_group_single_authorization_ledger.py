#!/usr/bin/env python3
"""Validate the project-group single authorization ledger (PG-03)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "09-status/globalcloud-project-group-single-authorization-ledger-v1.0.md"
TEMPLATE = ROOT / "templates/authorization-batch-request.md"
RECEIPTS = ROOT / "runtime/authorization-receipts.yaml"

AUTH_IDS = [
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-WAVE1-WAME-LINT-RUNTIME-20260626",
    "AUTH-WAVE1-GFIS-REAL-SOR-20260626",
    "AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626",
    "AUTH-WAVE1-BRAIN-HUMAN-REVIEW-20260626",
    "AUTH-WAVE1-GPCF-POST-SCHEME-REVIEW-20260626",
    "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
    "AUTH-WAS-DELETE-DS-STORE-20260626",
    "AUTH-KDS-OWNER-DECISION-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
]

GRANTED_IDS = [
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-WAVE1-WAME-LINT-RUNTIME-20260626",
    "AUTH-WAVE1-BRAIN-HUMAN-REVIEW-20260626",
    "AUTH-WAVE1-GPCF-POST-SCHEME-REVIEW-20260626",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-KDS-DIFFCHECK-CLEANUP-20260626",
    "AUTH-WAS-DELETE-DS-STORE-20260626",
]

REQUIRED_TOKENS = [
    "project_group_single_authorization_ledger_v1_0 = controlled",
    "auth_item_count = 14",
    "pending_confirmation_count = 2",
    "authorized_review_only_count = 3",
    "blocked_by_pre_wave1_count = 0",
    "historical_verify_count = 2",
    "authorization_granted_count = 10",
    "action_executed_count = 10",
    "review_conclusion_count = 8",
    "wave1_review_conclusion_count = 5",
    "authorized_pending_execution_count = 0",
    "executed_cleanup_count = 2",
    "pre_wave1_concluded = true",
    "first_batch_recommended = 3",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]


def fail(msg: str) -> int:
    print("project_group_single_authorization_ledger = fail")
    print(f"reason = {msg}")
    return 1


def main() -> int:
    for path in (DOC, TEMPLATE, RECEIPTS):
        if not path.exists():
            return fail(f"missing file: {path}")

    doc = DOC.read_text(encoding="utf-8")
    missing = [t for t in REQUIRED_TOKENS if t not in doc]
    if missing:
        return fail("ledger missing tokens: " + "; ".join(missing))

    missing_ids = [a for a in AUTH_IDS if a not in doc]
    if missing_ids:
        return fail("ledger missing auth ids: " + ", ".join(missing_ids))

    import re
    receipts = RECEIPTS.read_text(encoding="utf-8")
    executed_m = re.search(r"action_executed_count:\s*(\d+)", receipts)
    granted_m = re.search(r"authorization_granted_count:\s*(\d+)", receipts)
    if not executed_m or not granted_m:
        return fail("receipts missing action_executed_count / authorization_granted_count")
    executed, granted = int(executed_m.group(1)), int(granted_m.group(1))
    auth_id_count = receipts.count("auth_id: AUTH-")
    if executed > granted:
        return fail(f"executed({executed}) exceeds granted({granted})")
    if granted > auth_id_count:
        return fail(f"granted({granted}) exceeds receipt entries({auth_id_count})")
    for a in GRANTED_IDS:
        if a not in receipts:
            return fail(f"receipt missing for {a}")
    if "revoked_at: null" not in receipts:
        return fail("receipts must keep explicit revocation field")
    if "expires_at:" not in receipts:
        return fail("receipts must carry expiry")

    if "授权 <AUTH-ID>" not in TEMPLATE.read_text(encoding="utf-8"):
        return fail("batch request template missing single-auth template")

    print("project_group_single_authorization_ledger = pass")
    print("auth_item_count = 14")
    print("pending_confirmation_count = 2")
    print("blocked_by_pre_wave1_count = 0")
    print("historical_verify_count = 2")
    print("first_batch_recommended = 3")
    print(f"authorization_granted_count = {granted}")
    print(f"action_executed_count = {executed}")
    print("accepted = false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
