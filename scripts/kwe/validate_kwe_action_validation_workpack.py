#!/usr/bin/env python3
"""Validate KWE action validation workpack dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "kwe-action-validation-workpack-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "kwe-action-validation-workpack.ts"
FIXTURE = ROOT / "fixtures" / "kwe" / "action-validation-workpack-dry-run.json"

NO_WRITE_KEYS = (
    "writesKweWorkItem",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
    "writesWaesGateResult",
    "writesBusinessSystem",
    "writesTargetReceipt",
    "writesCommitteeDecisionCompletion",
    "writesRevenueOrScoreConfirmation",
    "writesQuotaTransfer",
    "writesBountySettlement",
    "writesExternalApi",
)


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    workpacks: list[dict[str, Any]] = fixture["workpacks"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "KweActionValidationCheck": policy["validation_checks"],
        "KweActionValidationStatus": policy["validation_statuses"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    required_checks = set(policy["validation_checks"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "validationPassed": 0,
        "repairRequired": 0,
        "committeeReviewCandidates": 0,
        "freezeReviewCandidates": 0,
        "blocked": 0,
        "createsKweWorkItems": 0,
        "promotesLifecycle": 0,
        "workpacksWithFollowups": 0,
    }

    for workpack in workpacks:
        workpack_id = workpack["workpackId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in workpack})
        if missing:
            failures.append(f"{workpack_id} missing required fields: {missing}")
        if workpack["createsKweWorkItem"] is not False:
            failures.append(f"{workpack_id}: createsKweWorkItem must be false")
        if workpack["promotesLifecycle"] is not False:
            failures.append(f"{workpack_id}: promotesLifecycle must be false")
        counts["createsKweWorkItems"] += int(workpack["createsKweWorkItem"] is True)
        counts["promotesLifecycle"] += int(workpack["promotesLifecycle"] is True)
        counts["workpacksWithFollowups"] += int(bool(workpack["requiredFollowups"]))

        check_names = {item["check"] for item in workpack["validationChecks"]}
        unknown_checks = sorted(check_names - required_checks)
        if unknown_checks:
            failures.append(f"{workpack_id}: unknown validation checks {unknown_checks}")
        if "no_write_guard" not in check_names:
            failures.append(f"{workpack_id}: missing no_write_guard")

        for check in workpack["validationChecks"]:
            if check["status"] not in {"passed", "repair_required", "blocked"}:
                failures.append(f"{workpack_id}: invalid check status {check['status']}")
            if check["status"] != "passed" and not check["reasonCodes"]:
                failures.append(f"{workpack_id}: non-passed check requires reasonCodes")

        raw_tokens = " ".join(
            workpack["acceptedPayloadRefs"]
            + workpack["acceptedEvidenceRefs"]
            + workpack["rejectedRefs"]
            + workpack["validationNotes"]
        )
        if workpack["actionType"] == "metadata_only_review":
            if "raw" in raw_tokens or "原文" in raw_tokens:
                failures.append(f"{workpack_id}: metadata_only_review must not include raw content refs")
            if "metadata_only_boundary" not in check_names:
                failures.append(f"{workpack_id}: metadata_only_review requires metadata_only_boundary check")
        if workpack["validationStatus"] == "committee_review_candidate":
            counts["committeeReviewCandidates"] += 1
            if workpack["actionType"] != "escalate_committee":
                failures.append(f"{workpack_id}: committee candidate must come from escalate_committee")
        if workpack["validationStatus"] == "freeze_review_candidate":
            counts["freezeReviewCandidates"] += 1
            if workpack["actionType"] != "request_freeze":
                failures.append(f"{workpack_id}: freeze candidate must come from request_freeze")
            if "blocked_reason_presence" not in check_names:
                failures.append(f"{workpack_id}: freeze candidate requires blocked_reason_presence")
        if workpack["validationStatus"] == "blocked":
            counts["blocked"] += 1
            if "blocked_reason_presence" not in check_names:
                failures.append(f"{workpack_id}: blocked workpack requires blocked_reason_presence")
        if workpack["validationStatus"] == "validation_passed":
            counts["validationPassed"] += 1
            if not workpack["acceptedPayloadRefs"] and not workpack["acceptedEvidenceRefs"]:
                failures.append(f"{workpack_id}: validation_passed requires accepted payload or evidence")
        if workpack["validationStatus"] == "repair_required":
            counts["repairRequired"] += 1
            if not any(check["status"] == "repair_required" for check in workpack["validationChecks"]):
                failures.append(f"{workpack_id}: repair_required requires a repair_required check")

        for key in NO_WRITE_KEYS:
            value = workpack["noWrite"].get(key)
            if value != 0:
                failures.append(f"{workpack_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "workpackCount": len(workpacks),
        **counts,
        **totals,
    }

    for key, value in policy["hard_boundaries"].items():
        if value is not True:
            failures.append(f"policy hard_boundaries.{key} is not true")
    for key, value in policy["no_write_guards"].items():
        if value != 0:
            failures.append(f"policy no_write_guards.{key} is non-zero")
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("kwe_action_validation_workpack=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kwe_action_validation_workpack=pass "
        f"workpacks={actual['workpackCount']} validation_passed={actual['validationPassed']} "
        f"repair_required={actual['repairRequired']} committee_review_candidates={actual['committeeReviewCandidates']} "
        f"freeze_review_candidates={actual['freezeReviewCandidates']} blocked={actual['blocked']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} promotes_lifecycle={actual['promotesLifecycle']} "
        f"workpacks_with_followups={actual['workpacksWithFollowups']} "
        "writes_kwe_work_item=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_waes_gate_result=0 writes_business_system=0 "
        "writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
