#!/usr/bin/env python3
"""Validate P0 Harness evidence candidate record dry-run without formal evidence writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-evidence-candidate-record-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_packet = load_json(data["sourceHarnessInputPacket"])
    candidate_record = data["candidateRecord"]

    if data.get("candidateRecordStatus") != expected["candidateRecordStatus"]:
        failures.append("candidateRecordStatus must remain candidate")
    if candidate_record.get("recordType") != expected["recordType"]:
        failures.append("recordType mismatch")
    if source_packet.get("packetStatus") != expected["sourceHarnessInputPacketStatus"]:
        failures.append("source Harness input packet status mismatch")
    if candidate_record.get("reviewStatus") != expected["reviewStatus"]:
        failures.append("candidate reviewStatus must remain pending")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("candidate record must state notFinalAcceptance=true")

    if len(candidate_record["allowedDecisionOutcomes"]) != expected["allowedDecisionOutcomeCount"]:
        failures.append("allowedDecisionOutcomeCount mismatch")
    if len(data["sourceReviewInputs"]) != expected["sourceReviewInputCount"]:
        failures.append("sourceReviewInputCount mismatch")
    if len(data["sourceRiskRefs"]) != expected["sourceRiskRefCount"]:
        failures.append("sourceRiskRefCount mismatch")
    if len(data["requiredSourceRefs"]) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    if candidate_record.get("defaultDecisionOutcome") != "pending":
        failures.append("defaultDecisionOutcome must be pending")
    if "pending" in candidate_record.get("allowedDecisionOutcomes", []):
        failures.append("pending must not be a final allowed decision outcome")
    if candidate_record.get("requiresHumanReview") is not expected["requiresHumanReview"]:
        failures.append("requiresHumanReview mismatch")
    if candidate_record.get("requiresHarnessGovernance") is not expected["requiresHarnessGovernance"]:
        failures.append("requiresHarnessGovernance mismatch")
    if candidate_record.get("writesFormalEvidence") is not expected["writesFormalEvidence"]:
        failures.append("writesFormalEvidence must remain false")
    if candidate_record.get("writesAcceptedLifecycle") is not expected["writesAcceptedLifecycle"]:
        failures.append("writesAcceptedLifecycle must remain false")

    source_input_ids = {item["id"] for item in source_packet.get("harnessInputs", [])}
    for input_ref in data["sourceReviewInputs"]:
        if input_ref not in source_input_ids:
            failures.append(f"sourceReviewInput missing from D22 packet: {input_ref}")

    source_risk_refs = set(source_packet.get("riskRefs", []))
    for risk_ref in data["sourceRiskRefs"]:
        if risk_ref not in source_risk_refs:
            failures.append(f"sourceRiskRef missing from D22 packet: {risk_ref}")

    for source_ref in data["requiredSourceRefs"]:
        if not (ROOT / source_ref).exists():
            failures.append(f"required source ref missing: {source_ref}")

    forbidden_final_statuses = {"accepted", "integrated", "production_ready", "business_write_enabled"}
    if data["candidateRecordStatus"] in forbidden_final_statuses:
        failures.append("candidateRecordStatus must not be final")
    if candidate_record["reviewStatus"] in forbidden_final_statuses:
        failures.append("reviewStatus must not be final")

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
        "\"candidateRecordStatus\": \"accepted\"",
        "\"candidateRecordStatus\": \"integrated\"",
        "\"reviewStatus\": \"approved\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden candidate record term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_harness_evidence_candidate_record_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_harness_evidence_candidate_record_dry_run=pass "
        f"status={expected['candidateRecordStatus']} "
        f"record_type={expected['recordType']} "
        f"source_packet_status={expected['sourceHarnessInputPacketStatus']} "
        f"review_status={expected['reviewStatus']} "
        f"decision_outcomes={expected['allowedDecisionOutcomeCount']} "
        f"source_inputs={expected['sourceReviewInputCount']} "
        f"risk_refs={expected['sourceRiskRefCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "requires_human_review=covered "
        "requires_harness_governance=covered "
        "not_final_acceptance=covered "
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
