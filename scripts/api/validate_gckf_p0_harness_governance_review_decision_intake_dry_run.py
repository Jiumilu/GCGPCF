#!/usr/bin/env python3
"""Validate P0 Harness Governance review decision intake dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-governance-review-decision-intake-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_packet = load_json(data["sourceCandidatePacket"])
    packet = source_packet["packet"]
    intake = data["intake"]

    if data.get("intakeStatus") != expected["intakeStatus"]:
        failures.append("intakeStatus must remain candidate")
    if intake.get("intakeStatus") != expected["intakeStatus"]:
        failures.append("intake intakeStatus must remain candidate")
    if intake.get("intakeType") != expected["intakeType"]:
        failures.append("intakeType mismatch")
    if intake.get("reviewStatus") != expected["reviewStatus"]:
        failures.append("reviewStatus must remain pending")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("intake must state notFinalAcceptance=true")

    if source_packet.get("packetStatus") != expected["sourcePacketStatus"]:
        failures.append("source packet must remain candidate")
    if packet.get("reviewStatus") != expected["sourcePacketReviewStatus"]:
        failures.append("source packet reviewStatus must remain pending")
    if intake.get("sourcePacketId") != packet.get("id"):
        failures.append("sourcePacketId must match D29 packet id")
    if intake.get("requiredReviewerType") != "human_or_harness_governance":
        failures.append("requiredReviewerType mismatch")

    outcomes = set(intake.get("allowedDecisionOutcomes", []))
    expected_outcomes = {
        "accept_for_review",
        "return_for_packet_repair",
        "reject_candidate_packet",
        "approve_for_future_formal_write",
    }
    if outcomes != expected_outcomes:
        failures.append("allowedDecisionOutcomes mismatch")
    if len(outcomes) != expected["allowedDecisionOutcomeCount"]:
        failures.append("allowedDecisionOutcomeCount mismatch")

    required_fields = set(intake.get("requiredDecisionFields", []))
    if len(required_fields) != expected["requiredDecisionFieldCount"]:
        failures.append("requiredDecisionFieldCount mismatch")
    for field in {"reviewerId", "reviewedAt", "sourcePacketRef", "decisionOutcome", "decisionRationale", "evidenceRefs", "authorityRef"}:
        if field not in required_fields:
            failures.append(f"missing decision field: {field}")

    guards = set(intake.get("decisionGuards", []))
    if len(guards) != expected["decisionGuardCount"]:
        failures.append("decisionGuardCount mismatch")
    for guard in {
        "source_packet_status_is_candidate",
        "source_packet_review_status_is_pending",
        "reviewer_authority_present",
        "decision_outcome_is_allowed",
        "formal_evidence_not_written",
        "harness_evidence_not_written",
        "approval_does_not_write_evidence",
        "repair_and_rejection_require_reason",
        "future_formal_write_requires_separate_execution",
    }:
        if guard not in guards:
            failures.append(f"missing decision guard: {guard}")

    forbidden_actions = set(intake.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "treat_approval_as_written_evidence",
    }:
        if forbidden not in forbidden_actions:
            failures.append(f"missing forbidden action: {forbidden}")

    if len(data.get("requiredSourceRefs", [])) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for source_ref in data.get("requiredSourceRefs", []):
        if not (ROOT / source_ref).exists():
            failures.append(f"missing required source ref: {source_ref}")

    for forbidden in ["accepted", "integrated", "production_ready", "business_write_enabled", "kds_write_enabled"]:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")

    forbidden_terms = [
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"intakeStatus\": \"accepted\"",
        "\"reviewStatus\": \"approved\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden intake term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_harness_governance_review_decision_intake_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_harness_governance_review_decision_intake_dry_run=pass "
        f"status={expected['intakeStatus']} "
        f"intake_type={expected['intakeType']} "
        f"review_status={expected['reviewStatus']} "
        f"source_packet_status={expected['sourcePacketStatus']} "
        f"source_packet_review_status={expected['sourcePacketReviewStatus']} "
        f"allowed_decisions={expected['allowedDecisionOutcomeCount']} "
        f"required_decision_fields={expected['requiredDecisionFieldCount']} "
        f"decision_guards={expected['decisionGuardCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "future_formal_write_separate=covered "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "writes_formal_evidence=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
