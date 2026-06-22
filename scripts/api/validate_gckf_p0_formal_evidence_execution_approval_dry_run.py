#!/usr/bin/env python3
"""Validate P0 formal evidence execution approval dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-approval-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_request = load_json(data["sourceExecutionRequest"])
    request = source_request["executionRequest"]
    approval = data["approvalCandidate"]

    if data.get("executionApprovalStatus") != expected["executionApprovalStatus"]:
        failures.append("executionApprovalStatus must remain candidate_approval")
    if approval.get("approvalStatus") != expected["approvalStatus"]:
        failures.append("approvalStatus must remain candidate_approval")
    if approval.get("approvalOutcome") != expected["approvalOutcome"]:
        failures.append("approvalOutcome mismatch")
    if approval.get("executionStatus") != expected["executionStatus"]:
        failures.append("executionStatus must remain not_executed")
    if approval.get("approvalType") != expected["approvalType"]:
        failures.append("approvalType mismatch")
    if approval.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("execution approval must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("execution approval must state notFinalAcceptance=true")

    if source_request.get("executionRequestStatus") != expected["sourceExecutionRequestStatus"]:
        failures.append("source execution request must remain candidate")
    if request.get("executionStatus") != expected["sourceExecutionRequestExecutionStatus"]:
        failures.append("source execution request executionStatus must remain not_executed")
    if request.get("dryRunOnly") is not True:
        failures.append("source execution request must remain dryRunOnly=true")
    if approval.get("sourceExecutionRequestId") != request.get("id"):
        failures.append("sourceExecutionRequestId must match D32 request id")
    if data.get("coveredRequestType") != expected["coveredRequestType"]:
        failures.append("coveredRequestType mismatch")
    if data["coveredRequestType"] != request.get("requestType"):
        failures.append("covered request type must match D32 request type")

    required_inputs = set(approval.get("requiredInputs", []))
    if len(required_inputs) != expected["requiredInputCount"]:
        failures.append("requiredInputCount mismatch")
    for required in {
        "executionRequestRef",
        "reviewerId",
        "reviewedAt",
        "authorityRef",
        "approvalOutcome",
        "approvalScope",
        "evidenceRefs",
        "idempotencyKey",
        "duplicateCheckRef",
        "rollbackPlanRef",
        "executionLockRef",
        "auditTrailRef",
        "nextExecutionStepRef",
        "harnessDecisionRecordRef",
    }:
        if required not in required_inputs:
            failures.append(f"missing required input: {required}")

    checks = set(approval.get("approvalChecks", []))
    if len(checks) != expected["approvalCheckCount"]:
        failures.append("approvalCheckCount mismatch")
    for check in {
        "source_execution_request_status_is_candidate",
        "source_execution_request_execution_status_is_not_executed",
        "source_execution_request_is_dry_run_only",
        "request_type_is_formal_evidence_execution_request",
        "approval_scope_present",
        "authority_ref_present",
        "evidence_refs_present",
        "idempotency_key_present",
        "duplicate_formal_evidence_absent",
        "rollback_plan_present",
        "execution_lock_present",
        "audit_trail_ref_present",
        "harness_decision_record_ref_present",
        "approval_requires_separate_execution_step",
        "approval_does_not_execute_formal_write",
    }:
        if check not in checks:
            failures.append(f"missing approval check: {check}")

    forbidden_actions = set(approval.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "bypass_execution_step",
        "bypass_duplicate_guard",
    }:
        if forbidden not in forbidden_actions:
            failures.append(f"missing forbidden action: {forbidden}")

    if len(data.get("requiredSourceRefs", [])) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for source_ref in data.get("requiredSourceRefs", []):
        if not (ROOT / source_ref).exists():
            failures.append(f"missing required source ref: {source_ref}")

    for forbidden in [
        "formal_harness_evidence_record_written",
        "harness_evidence_record_written",
        "formal_write_executed",
        "accepted",
        "integrated",
        "production_ready",
        "business_write_enabled",
        "kds_write_enabled",
    ]:
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
        "\"dryRunOnly\": false",
        "\"executionApprovalStatus\": \"accepted\"",
        "\"approvalStatus\": \"approved\"",
        "\"executionStatus\": \"executed\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden execution approval term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_execution_approval_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_execution_approval_dry_run=pass "
        f"status={expected['executionApprovalStatus']} "
        f"approval_type={expected['approvalType']} "
        f"approval_status={expected['approvalStatus']} "
        f"approval_outcome={expected['approvalOutcome']} "
        f"execution_status={expected['executionStatus']} "
        f"source_request_status={expected['sourceExecutionRequestStatus']} "
        f"source_request_execution_status={expected['sourceExecutionRequestExecutionStatus']} "
        f"covered_request_type={expected['coveredRequestType']} "
        f"required_inputs={expected['requiredInputCount']} "
        f"approval_checks={expected['approvalCheckCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "harness_decision_record=covered "
        "separate_execution_step=covered "
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
