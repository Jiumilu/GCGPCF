#!/usr/bin/env python3
"""Validate P0 formal evidence candidate packet assembly dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-candidate-packet-assembly-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_guard = load_json(data["sourceWriteActionGuard"])
    guarded_action = source_guard["guardedAction"]
    candidate_request = source_guard["candidateWriteRequest"]
    packet = data["packet"]

    if data.get("packetStatus") != expected["packetStatus"]:
        failures.append("packetStatus must remain candidate")
    if packet.get("packetStatus") != expected["packetStatus"]:
        failures.append("packet packetStatus must remain candidate")
    if packet.get("packetType") != expected["packetType"]:
        failures.append("packetType mismatch")
    if packet.get("reviewStatus") != expected["reviewStatus"]:
        failures.append("reviewStatus must remain pending")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("packet must state notFinalAcceptance=true")

    if source_guard.get("guardStatus") != expected["sourceGuardStatus"]:
        failures.append("source guard must remain candidate")
    if guarded_action.get("outputType") != expected["sourceGuardOutputType"]:
        failures.append("source guard outputType mismatch")
    if packet.get("sourceGuardId") != guarded_action.get("id"):
        failures.append("packet sourceGuardId must match D28 guard id")
    if candidate_request.get("requestStatus") != "candidate":
        failures.append("source candidate write request must remain candidate")
    if candidate_request.get("formalEvidenceWritten") is not expected["formalEvidenceWritten"]:
        failures.append("source formalEvidenceWritten must remain false")
    if candidate_request.get("harnessEvidenceWritten") is not expected["harnessEvidenceWritten"]:
        failures.append("source harnessEvidenceWritten must remain false")

    required_sections = set(packet.get("requiredSections", []))
    if len(required_sections) != expected["requiredSectionCount"]:
        failures.append("requiredSectionCount mismatch")
    for section in {
        "sourceCandidateRecord",
        "approvalPreflight",
        "writeActionGuard",
        "reviewRoute",
        "idempotencyPlan",
        "duplicateCheck",
        "rollbackPlan",
        "forbiddenActionAcknowledgement",
    }:
        if section not in required_sections:
            failures.append(f"missing required packet section: {section}")

    assembly_checks = set(packet.get("assemblyChecks", []))
    if len(assembly_checks) != expected["assemblyCheckCount"]:
        failures.append("assemblyCheckCount mismatch")
    for check in {
        "source_write_guard_status_is_candidate",
        "source_write_guard_output_is_candidate_write_request",
        "candidate_write_request_status_is_candidate",
        "formal_evidence_not_written",
        "harness_evidence_not_written",
        "review_route_present",
        "idempotency_plan_present",
        "duplicate_check_present",
        "rollback_plan_present",
        "forbidden_actions_acknowledged",
    }:
        if check not in assembly_checks:
            failures.append(f"missing assembly check: {check}")

    allowed_next = set(packet.get("allowedNextActions", []))
    if len(allowed_next) != expected["allowedNextActionCount"]:
        failures.append("allowedNextActionCount mismatch")
    if "submit_to_harness_governance_review" not in allowed_next:
        failures.append("packet must only proceed through Harness Governance review")

    forbidden_actions = set(packet.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "skip_harness_review",
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
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"packetStatus\": \"accepted\"",
        "\"reviewStatus\": \"approved\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden packet term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_candidate_packet_assembly_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_candidate_packet_assembly_dry_run=pass "
        f"status={expected['packetStatus']} "
        f"packet_type={expected['packetType']} "
        f"review_status={expected['reviewStatus']} "
        f"source_guard_status={expected['sourceGuardStatus']} "
        f"source_guard_output_type={expected['sourceGuardOutputType']} "
        f"required_sections={expected['requiredSectionCount']} "
        f"assembly_checks={expected['assemblyCheckCount']} "
        f"allowed_next_actions={expected['allowedNextActionCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "review_route=covered "
        "idempotency=covered "
        "rollback=covered "
        "duplicate_guard=covered "
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
