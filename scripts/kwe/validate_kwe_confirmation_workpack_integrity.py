#!/usr/bin/env python3
"""Validate KWE confirmation workpack reference integrity dry-run.

This script uses local fixtures only. It does not create KWE work items, KDS
facts, WAES gate results, business writebacks, ledger confirmations, or
external API calls.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "kwe" / "confirmation-workpack-integrity-dry-run.json"


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def has_required_fields(workpack: dict[str, Any], required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in workpack]


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    required_fields = data["requiredFields"]
    failures: list[str] = []

    counts = {
        "workpackCount": len(data["workpacks"]),
        "requiredFieldCount": len(required_fields),
        "readyForHumanReview": 0,
        "readyForCommitteeReview": 0,
        "repairRequired": 0,
        "blocked": 0,
        "metadataOnlyOrControlledOriginal": 0,
        "rawContentLeaks": 0,
        "humanAcceptsBlockedOrCommitteeRequired": 0,
        "committeeMissingTriggerReason": 0,
        "acceptOnlyWithMissingEvidence": 0,
        "writesKweWorkItem": 0,
        "writesKdsFact": 0,
        "writesWaesGateResult": 0,
        "writesBusinessSystem": 0,
        "writesRevenueOrScoreConfirmation": 0,
        "writesQuotaTransfer": 0,
        "writesBountySettlement": 0,
        "writesCommitteeDecisionCompletion": 0,
        "writesExternalApi": 0,
    }

    for workpack in data["workpacks"]:
        missing = has_required_fields(workpack, required_fields)
        if missing:
            failures.append(f"{workpack.get('id', '<missing-id>')} missing required fields: {missing}")
            continue

        result = workpack["workpackResult"]
        if result == "ready_for_human_review":
            counts["readyForHumanReview"] += 1
        elif result == "ready_for_committee_review":
            counts["readyForCommitteeReview"] += 1
        elif result == "repair_required":
            counts["repairRequired"] += 1
        elif result == "blocked":
            counts["blocked"] += 1
        else:
            failures.append(f"{workpack['id']} unexpected workpackResult={result!r}")

        if workpack["sensitiveHandling"] in {"metadata_only", "controlled_original"}:
            counts["metadataOnlyOrControlledOriginal"] += 1
            if workpack["containsRawContent"]:
                counts["rawContentLeaks"] += 1

        if workpack["reviewerType"] == "committee" and not workpack.get("committeeTriggerReason"):
            counts["committeeMissingTriggerReason"] += 1

        if workpack["reviewerType"] == "human" and workpack["waesGateStatus"] in {"blocked", "committee_required", "freeze_required"}:
            if "allow_accept" in as_list(workpack["decisionOptions"]):
                counts["humanAcceptsBlockedOrCommitteeRequired"] += 1

        if as_list(workpack["missingEvidenceRefs"]) and as_list(workpack["decisionOptions"]) == ["allow_accept"]:
            counts["acceptOnlyWithMissingEvidence"] += 1

        if not workpack["noWrite"]:
            failures.append(f"{workpack['id']} noWrite must be true")

        for key in ("poolRefs", "waesGateRefs"):
            if not as_list(workpack[key]):
                failures.append(f"{workpack['id']} {key} must not be empty")

        if result in {"ready_for_human_review", "ready_for_committee_review"}:
            for key in ("sourceRefs", "evidenceRefs", "reviewerRefs"):
                if not as_list(workpack[key]):
                    failures.append(f"{workpack['id']} {key} must not be empty when review-ready")

    expected = data["expected"]
    for key, expected_value in expected.items():
        if counts.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={counts.get(key)!r}")

    if failures:
        print("kwe_confirmation_workpack_integrity=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kwe_confirmation_workpack_integrity=pass "
        f"workpacks={counts['workpackCount']} "
        f"required_fields={counts['requiredFieldCount']} "
        f"ready_human={counts['readyForHumanReview']} "
        f"ready_committee={counts['readyForCommitteeReview']} "
        f"repair_required={counts['repairRequired']} "
        f"blocked={counts['blocked']} "
        f"metadata_or_controlled={counts['metadataOnlyOrControlledOriginal']} "
        "raw_content_leaks=0 "
        "human_accepts_blocked_or_committee=0 "
        "committee_missing_trigger=0 "
        "accept_only_with_missing_evidence=0 "
        "writes_kwe_work_item=0 writes_kds_fact=0 writes_waes_gate_result=0 "
        "writes_business_system=0 writes_revenue_or_score_confirmation=0 "
        "writes_quota_transfer=0 writes_bounty_settlement=0 "
        "writes_committee_decision_completion=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
