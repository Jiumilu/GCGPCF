#!/usr/bin/env python3
"""Validate P0 formal evidence final execution request dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-final-execution-request-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_guard = load_json(data["sourceFinalExecutionGuard"])
    guard = source_guard["finalExecutionGuard"]
    request = data["finalExecutionRequest"]

    if data.get("finalExecutionRequestStatus") != expected["finalExecutionRequestStatus"]:
        failures.append("finalExecutionRequestStatus must remain candidate_request")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if request.get("requestStatus") != expected["requestStatus"]:
        failures.append("requestStatus must remain candidate_request")
    if request.get("executionStatus") != expected["executionStatus"]:
        failures.append("executionStatus must remain not_executed")
    if request.get("executionMode") != expected["executionMode"]:
        failures.append("request executionMode mismatch")
    if request.get("requestType") != expected["requestType"]:
        failures.append("requestType mismatch")
    if request.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("final execution request must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("final execution request must state notFinalAcceptance=true")

    if source_guard.get("finalExecutionGuardStatus") != expected["sourceFinalExecutionGuardStatus"]:
        failures.append("source final execution guard must remain candidate_guard")
    if guard.get("executionStatus") != expected["sourceFinalExecutionGuardExecutionStatus"]:
        failures.append("source final execution guard executionStatus must remain not_executed")
    if guard.get("dryRunOnly") is not True:
        failures.append("source final execution guard must remain dryRunOnly=true")
    if request.get("sourceFinalExecutionGuardId") != guard.get("id"):
        failures.append("sourceFinalExecutionGuardId must match D35 guard id")
    if data.get("coveredGuardStatus") != expected["coveredGuardStatus"]:
        failures.append("coveredGuardStatus mismatch")
    if data["coveredGuardStatus"] != guard.get("guardStatus"):
        failures.append("covered guard status must match D35 guard status")

    required_inputs = set(request.get("requiredInputs", []))
    if len(required_inputs) != expected["requiredInputCount"]:
        failures.append("requiredInputCount mismatch")
    for required in {
        "finalExecutionGuardRef",
        "executionStepRef",
        "executionApprovalRef",
        "executorId",
        "requesterId",
        "humanAuthorizationRef",
        "committeeAuthorizationRef",
        "freezeGateResultRef",
        "duplicateCheckRef",
        "idempotencyKey",
        "executionLockRef",
        "preWriteSnapshotRef",
        "postWriteVerificationPlanRef",
        "rollbackPlanRef",
        "auditTrailRef",
        "harnessEvidenceTargetRef",
        "formalEvidenceTargetRef",
        "noWriteBoundaryRef",
    }:
        if required not in required_inputs:
            failures.append(f"missing required input: {required}")

    checks = set(request.get("requestChecks", []))
    if len(checks) != expected["requestCheckCount"]:
        failures.append("requestCheckCount mismatch")
    for check in {
        "source_final_execution_guard_status_is_candidate_guard",
        "source_final_execution_guard_execution_status_is_not_executed",
        "source_final_execution_guard_is_dry_run_only",
        "execution_mode_is_dry_run_no_write",
        "request_status_is_candidate_request",
        "human_authorization_ref_present",
        "committee_authorization_ref_present",
        "freeze_gate_result_ref_present",
        "duplicate_check_ref_present",
        "idempotency_key_present",
        "execution_lock_ref_present",
        "pre_write_snapshot_ref_present",
        "post_write_verification_plan_ref_present",
        "rollback_plan_ref_present",
        "audit_trail_ref_present",
        "harness_evidence_target_ref_present",
        "formal_evidence_target_ref_present",
        "no_write_boundary_ref_present",
        "request_does_not_execute_formal_evidence",
        "formal_write_requires_separate_harness_execution",
    }:
        if check not in checks:
            failures.append(f"missing request check: {check}")

    blocking_conditions = set(request.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    for blocking in {
        "source_guard_not_candidate_guard",
        "source_guard_already_executed",
        "source_guard_not_dry_run_only",
        "missing_requester",
        "missing_human_authorization",
        "missing_committee_authorization",
        "freeze_gate_blocked",
        "duplicate_formal_evidence_found",
        "idempotency_key_missing",
        "execution_lock_missing",
        "pre_write_snapshot_missing",
        "post_write_verification_plan_missing",
        "rollback_plan_missing",
        "audit_trail_missing",
        "formal_evidence_target_missing",
        "no_write_boundary_missing",
    }:
        if blocking not in blocking_conditions:
            failures.append(f"missing blocking condition: {blocking}")

    forbidden_actions = set(request.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "convert_candidate_guard_to_passed",
        "bypass_freeze_gate",
        "bypass_human_authorization",
        "bypass_committee_authorization",
        "release_execution_lock",
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
        "candidate_guard_promoted_to_passed",
        "freeze_gate_bypassed",
        "human_authorization_bypassed",
        "committee_authorization_bypassed",
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
        "\"finalExecutionRequestStatus\": \"accepted\"",
        "\"requestStatus\": \"approved\"",
        "\"executionStatus\": \"executed\"",
        "\"executionMode\": \"write\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden final execution request term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_final_execution_request_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_final_execution_request_dry_run=pass "
        f"status={expected['finalExecutionRequestStatus']} "
        f"request_type={expected['requestType']} "
        f"request_status={expected['requestStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"execution_mode={expected['executionMode']} "
        f"source_guard_status={expected['sourceFinalExecutionGuardStatus']} "
        f"source_guard_execution_status={expected['sourceFinalExecutionGuardExecutionStatus']} "
        f"covered_guard_status={expected['coveredGuardStatus']} "
        f"required_inputs={expected['requiredInputCount']} "
        f"request_checks={expected['requestCheckCount']} "
        f"blocking_conditions={expected['blockingConditionCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "human_authorization=covered "
        "committee_authorization=covered "
        "freeze_gate=covered "
        "duplicate_guard=covered "
        "no_guard_promotion=covered "
        "separate_harness_execution=covered "
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
