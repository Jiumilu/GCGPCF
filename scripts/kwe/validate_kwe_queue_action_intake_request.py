#!/usr/bin/env python3
"""Validate KWE queue action intake request dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "kwe-queue-action-intake-request-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "kwe-queue-action-intake-request.ts"
FIXTURE = ROOT / "fixtures" / "kwe" / "queue-action-intake-request-dry-run.json"

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
    requests: list[dict[str, Any]] = fixture["requests"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "KweQueueActionType": policy["action_types"],
        "KweQueueActionStatus": policy["action_statuses"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "submitEvidence": 0,
        "metadataOnlyReview": 0,
        "committeeCandidates": 0,
        "freezeCandidates": 0,
        "blocked": 0,
        "createsKweWorkItems": 0,
        "requestsWithPayloadOrEvidence": 0,
    }

    for request in requests:
        request_id = request["requestId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in request})
        if missing:
            failures.append(f"{request_id} missing required fields: {missing}")
        if request["createsKweWorkItem"] is not False:
            failures.append(f"{request_id}: createsKweWorkItem must be false")
        counts["createsKweWorkItems"] += int(request["createsKweWorkItem"] is True)

        for key in NO_WRITE_KEYS:
            value = request["noWrite"].get(key)
            if value != 0:
                failures.append(f"{request_id}: {key} must be 0")
            totals[key] += value

        has_payload_or_evidence = bool(request["payloadRefs"] or request["evidenceRefs"])
        counts["requestsWithPayloadOrEvidence"] += int(has_payload_or_evidence)

        if request["actionType"] == "submit_evidence":
            counts["submitEvidence"] += 1
            if not has_payload_or_evidence:
                failures.append(f"{request_id}: submit_evidence requires payloadRefs or evidenceRefs")
        if request["actionType"] == "metadata_only_review":
            counts["metadataOnlyReview"] += 1
            raw_tokens = " ".join(request["payloadRefs"] + request["evidenceRefs"])
            if "raw" in raw_tokens or "原文" in raw_tokens:
                failures.append(f"{request_id}: metadata_only_review must not include raw content refs")
        if request["actionType"] == "escalate_committee":
            if request["actionStatus"] != "committee_request_candidate":
                failures.append(f"{request_id}: escalate_committee must remain committee_request_candidate")
            counts["committeeCandidates"] += 1
        if request["actionType"] == "request_freeze":
            if request["actionStatus"] != "freeze_request_candidate":
                failures.append(f"{request_id}: request_freeze must remain freeze_request_candidate")
            counts["freezeCandidates"] += 1
        if request["actionStatus"] == "blocked":
            counts["blocked"] += 1
            if not request["blockedReasons"]:
                failures.append(f"{request_id}: blocked request requires blockedReasons")

    actual = {
        "requestCount": len(requests),
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
        print("kwe_queue_action_intake_request=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kwe_queue_action_intake_request=pass "
        f"requests={actual['requestCount']} submit_evidence={actual['submitEvidence']} "
        f"metadata_only_review={actual['metadataOnlyReview']} committee_candidates={actual['committeeCandidates']} "
        f"freeze_candidates={actual['freezeCandidates']} blocked={actual['blocked']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"requests_with_payload_or_evidence={actual['requestsWithPayloadOrEvidence']} "
        "writes_kwe_work_item=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_waes_gate_result=0 writes_business_system=0 "
        "writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
