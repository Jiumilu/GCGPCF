#!/usr/bin/env python3
"""Validate KDS lifecycle transition audit packet dry-run boundary.

The validator checks local policy, shared type text, and fixture declarations
only. It does not mutate KDS lifecycle, WAES gate results, KWE work items,
business systems, revenue, scores, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "kds-lifecycle-transition-audit-packet-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "kds-lifecycle-transition-audit-packet.ts"
FIXTURE = ROOT / "fixtures" / "kds" / "lifecycle-transition-audit-packet-dry-run.json"

NO_WRITE_KEYS = (
    "writesKdsLifecycle",
    "writesAcceptedFact",
    "writesPublishedObject",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesBusinessSystem",
    "writesRevenueOrScoreConfirmation",
    "writesExternalApi",
)

HIGH_TRUST_TARGETS = {"verified", "accepted", "published"}
TERMINAL_STATES = {"archived", "superseded"}


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def extract_union_literals(text: str, type_name: str) -> set[str]:
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise AssertionError(f"missing union type: {type_name}")
    return set(re.findall(r'"([^"]+)"', match.group("body")))


def fail(failures: list[str], message: str) -> None:
    failures.append(message)


def main() -> int:
    policy = yaml.safe_load(POLICY.read_text())
    type_text = TYPE_FILE.read_text()
    fixture = json.loads(FIXTURE.read_text())
    packets: list[dict[str, Any]] = fixture["auditPackets"]
    expected = fixture["expected"]
    failures: list[str] = []

    policy_statuses = set(policy["audit_statuses"])
    type_statuses = extract_union_literals(type_text, "KdsLifecycleTransitionAuditStatus")
    if policy_statuses != type_statuses:
        fail(failures, f"audit status mismatch policy={sorted(policy_statuses)} type={sorted(type_statuses)}")

    required_fields = set(policy["required_fields"])
    packet_fields = {camel_to_snake(key) for key in packets[0].keys()}
    missing_required = sorted(required_fields - packet_fields)
    if missing_required:
        fail(failures, f"missing required fixture fields: {missing_required}")

    hard_boundaries = policy["hard_boundaries"]
    for key in (
        "audit_packet_is_not_lifecycle_mutation",
        "ai_and_loop_cannot_audit_high_trust_as_approved",
        "accepted_requires_human_or_committee",
        "published_requires_publication_controls",
        "frozen_requires_freeze_reason",
        "terminal_states_block_transition",
        "harness_evidence_is_required_for_high_trust",
        "audit_pass_is_not_business_completion",
    ):
        if hard_boundaries.get(key) is not True:
            fail(failures, f"hard boundary must be true: {key}")

    if any(value != 0 for value in policy["no_write_guards"].values()):
        fail(failures, "policy no_write_guards must all be zero")

    status_counts = {
        "readyForReview": 0,
        "repairRequired": 0,
        "waesRequired": 0,
        "humanRequired": 0,
        "publicationRequired": 0,
        "freezeRequired": 0,
        "blocked": 0,
    }
    status_key = {
        "ready_for_review": "readyForReview",
        "repair_required": "repairRequired",
        "waes_required": "waesRequired",
        "human_required": "humanRequired",
        "publication_required": "publicationRequired",
        "freeze_required": "freezeRequired",
        "blocked": "blocked",
    }

    totals = {key: 0 for key in NO_WRITE_KEYS}
    high_trust_audits = 0
    terminal_blocked = 0
    ai_blocked_high_trust = 0

    for packet in packets:
        audit_id = packet["auditId"]
        audit_status = packet["auditStatus"]
        from_lifecycle = packet["fromLifecycle"]
        to_lifecycle = packet["toLifecycle"]
        actor = packet["transitionActor"]

        if audit_status not in policy_statuses:
            fail(failures, f"{audit_id}: unknown auditStatus {audit_status}")
        else:
            key = status_key.get(audit_status)
            if key:
                status_counts[key] += 1

        for key in NO_WRITE_KEYS:
            value = packet["noWrite"].get(key)
            if value != 0:
                fail(failures, f"{audit_id}: {key} must be 0")
            totals[key] += value

        if to_lifecycle in HIGH_TRUST_TARGETS and audit_status != "blocked":
            high_trust_audits += 1
            if not packet["harnessEvidenceRefs"]:
                fail(failures, f"{audit_id}: high-trust audit requires harnessEvidenceRefs")

        if to_lifecycle == "accepted":
            if packet["reviewerRequirement"] not in {"human_required", "committee_required"}:
                fail(failures, f"{audit_id}: accepted audit requires human or committee reviewer")
            if audit_status not in {"human_required", "committee_required", "blocked"}:
                fail(failures, f"{audit_id}: accepted audit cannot be {audit_status}")

        if to_lifecycle == "published":
            required = {"redaction_gate", "external_share_gate", "publication_approval"}
            if not required.issubset(set(packet["requiredActions"])):
                fail(failures, f"{audit_id}: published audit missing publication controls")
            if audit_status not in {"publication_required", "blocked"}:
                fail(failures, f"{audit_id}: published audit cannot be {audit_status}")

        if to_lifecycle == "frozen":
            freeze_tokens = " ".join(packet["blockedReasons"] + packet["requiredActions"])
            if "freeze" not in freeze_tokens and "冻结" not in freeze_tokens:
                fail(failures, f"{audit_id}: frozen audit requires freeze reason or action")

        if from_lifecycle in TERMINAL_STATES:
            if audit_status != "blocked":
                fail(failures, f"{audit_id}: terminal state transition must be blocked")
            terminal_blocked += 1

        if actor in {"ai", "loop"} and to_lifecycle in HIGH_TRUST_TARGETS:
            if audit_status != "blocked":
                fail(failures, f"{audit_id}: {actor} high-trust audit must be blocked")
            if actor == "ai":
                ai_blocked_high_trust += 1

    actual = {
        "auditCount": len(packets),
        **status_counts,
        "highTrustAudits": high_trust_audits,
        "terminalBlocked": terminal_blocked,
        "aiBlockedHighTrust": ai_blocked_high_trust,
        "lifecycleMutations": totals["writesKdsLifecycle"],
        "acceptedFactWrites": totals["writesAcceptedFact"],
        "publishedObjectWrites": totals["writesPublishedObject"],
        "waesGateResultWrites": totals["writesWaesGateResult"],
        "kweWorkItemWrites": totals["writesKweWorkItem"],
        "businessWrites": totals["writesBusinessSystem"],
        "revenueOrScoreConfirmations": totals["writesRevenueOrScoreConfirmation"],
        "externalApiWrites": totals["writesExternalApi"],
    }

    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            fail(failures, f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("kds_lifecycle_transition_audit_packet=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kds_lifecycle_transition_audit_packet=pass "
        f"audits={actual['auditCount']} "
        f"ready_for_review={actual['readyForReview']} "
        f"repair_required={actual['repairRequired']} "
        f"waes_required={actual['waesRequired']} "
        f"human_required={actual['humanRequired']} "
        f"publication_required={actual['publicationRequired']} "
        f"freeze_required={actual['freezeRequired']} "
        f"blocked={actual['blocked']} "
        f"high_trust_audits={actual['highTrustAudits']} "
        f"terminal_blocked={actual['terminalBlocked']} "
        f"ai_blocked_high_trust={actual['aiBlockedHighTrust']} "
        f"lifecycle_mutations={actual['lifecycleMutations']} "
        f"accepted_fact_writes={actual['acceptedFactWrites']} "
        f"published_object_writes={actual['publishedObjectWrites']} "
        f"waes_gate_result_writes={actual['waesGateResultWrites']} "
        f"kwe_work_item_writes={actual['kweWorkItemWrites']} "
        f"business_writes={actual['businessWrites']} "
        f"revenue_or_score_confirmations={actual['revenueOrScoreConfirmations']} "
        f"external_api_writes={actual['externalApiWrites']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
