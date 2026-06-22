#!/usr/bin/env python3
"""Validate KWE Promotion Request no-write dry-run boundaries.

This validator reads local OKF, shared type, and fixture files only. It does
not mutate KDS lifecycle, accepted facts, published objects, WAES gate results,
KWE work items, business systems, revenue, scores, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "kwe-promotion-request-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "kwe-promotion-request.ts"
FIXTURE = ROOT / "fixtures" / "kwe" / "promotion-request-no-write-dry-run.json"

HIGH_TRUST_TARGETS = {"verified", "accepted", "published"}
TERMINAL_STATES = {"superseded", "archived"}


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def normalized_keys(record: dict[str, Any]) -> set[str]:
    return {re.sub(r"(?<!^)([A-Z])", r"_\1", key).lower() for key in record}


def no_write_sum(request: dict[str, Any]) -> int:
    return sum(int(value) for value in request["noWrite"].values())


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    requests: list[dict[str, Any]] = fixture["requests"]
    expected = fixture["expected"]

    failures: list[str] = []
    required_fields = set(policy["required_fields"])
    hard = policy["hard_boundaries"]
    no_write_policy = policy["no_write_guards"]

    if union_literals("KwePromotionStatus") != policy["promotion_statuses"]:
        failures.append("KwePromotionStatus union does not match policy")

    for request in requests:
        missing = sorted(required_fields - normalized_keys(request))
        if missing:
            failures.append(f"{request['id']} missing required fields: {missing}")
        if no_write_sum(request) != 0:
            failures.append(f"{request['id']} has non-zero noWrite counters")
        if request["currentLifecycle"] in TERMINAL_STATES and request["promotionStatus"] != "blocked":
            failures.append(f"{request['id']} promotes from terminal state")
        if request["requestActor"] in {"ai", "loop"} and request["requestedLifecycle"] in HIGH_TRUST_TARGETS:
            if request["promotionStatus"] != "blocked":
                failures.append(f"{request['id']} allows ai/loop high-trust promotion")
        if request["requestedLifecycle"] == "accepted":
            if request["reviewerRequirement"] not in {"human_required", "committee_required"}:
                failures.append(f"{request['id']} accepted request lacks human/committee reviewer")
            if request["requestActor"] in {"ai", "loop"} and not request["blockedReasons"]:
                failures.append(f"{request['id']} blocked accepted request lacks reasons")
        if request["requestedLifecycle"] == "published":
            required_actions = set(request["requiredActions"])
            if not {"redaction_gate", "external_share_gate", "publication_approval"} <= required_actions:
                failures.append(f"{request['id']} published request lacks publication gates")
        if request["requestedLifecycle"] == "frozen" and not request["blockedReasons"]:
            failures.append(f"{request['id']} freeze request lacks freeze reason")
        if request["promotionStatus"] in {"ready_for_kwe_review", "human_required", "committee_required"}:
            if request["requestedLifecycle"] in {"verified", "accepted", "published"} and not request["harnessEvidenceRefs"]:
                failures.append(f"{request['id']} high-trust request lacks harness evidence refs")

    checks = {
        "requestCount": len(requests),
        "readyForKweReview": sum(1 for request in requests if request["promotionStatus"] == "ready_for_kwe_review"),
        "repairRequired": sum(1 for request in requests if request["promotionStatus"] == "repair_required"),
        "waesRequired": sum(1 for request in requests if request["promotionStatus"] == "waes_required"),
        "humanRequired": sum(1 for request in requests if request["promotionStatus"] == "human_required"),
        "committeeRequired": sum(1 for request in requests if request["promotionStatus"] == "committee_required"),
        "blocked": sum(1 for request in requests if request["promotionStatus"] == "blocked"),
        "freezeRequired": sum(1 for request in requests if request["promotionStatus"] == "freeze_required"),
        "aiBlockedPromotions": sum(
            1
            for request in requests
            if request["requestActor"] == "ai"
            and request["requestedLifecycle"] in HIGH_TRUST_TARGETS
            and request["promotionStatus"] == "blocked"
        ),
        "lifecycleMutations": sum(request["noWrite"]["writesKdsLifecycle"] for request in requests),
        "acceptedFactWrites": sum(request["noWrite"]["writesAcceptedFact"] for request in requests),
        "publishedObjectWrites": sum(request["noWrite"]["writesPublishedObject"] for request in requests),
        "waesGateResultWrites": sum(request["noWrite"]["writesWaesGateResult"] for request in requests),
        "kweWorkItemWrites": sum(request["noWrite"]["writesKweWorkItem"] for request in requests),
        "businessWrites": sum(request["noWrite"]["writesBusinessSystem"] for request in requests),
        "revenueOrScoreConfirmations": sum(
            request["noWrite"]["writesRevenueOrScoreConfirmation"] for request in requests
        ),
        "externalApiWrites": sum(request["noWrite"]["writesExternalApi"] for request in requests),
    }

    if not hard["promotion_request_is_not_lifecycle_mutation"]:
        failures.append("policy allows promotion request to mutate lifecycle")
    if not hard["ai_cannot_request_verified_accepted_published"]:
        failures.append("policy does not block AI high-trust promotion request")
    if not hard["loop_cannot_request_verified_accepted_published"]:
        failures.append("policy does not block LOOP high-trust promotion request")
    for key, value in no_write_policy.items():
        if value != 0:
            failures.append(f"policy no_write_guards.{key} is non-zero")

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("kwe_promotion_request_no_write=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kwe_promotion_request_no_write=pass "
        f"requests={checks['requestCount']} "
        f"ready_for_kwe_review={checks['readyForKweReview']} "
        f"repair_required={checks['repairRequired']} "
        f"waes_required={checks['waesRequired']} "
        f"human_required={checks['humanRequired']} "
        f"committee_required={checks['committeeRequired']} "
        f"blocked={checks['blocked']} "
        f"freeze_required={checks['freezeRequired']} "
        f"ai_blocked_promotions={checks['aiBlockedPromotions']} "
        "lifecycle_mutations=0 accepted_fact_writes=0 published_object_writes=0 "
        "waes_gate_result_writes=0 kwe_work_item_writes=0 business_writes=0 "
        "revenue_or_score_confirmations=0 external_api_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
