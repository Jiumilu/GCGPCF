#!/usr/bin/env python3
"""Validate P0 formal evidence execution evidence preview dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-evidence-preview-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_request = load_json(data["sourceFinalExecutionRequest"])
    request = source_request["finalExecutionRequest"]
    preview = data["evidencePreview"]

    if data.get("evidencePreviewStatus") != expected["evidencePreviewStatus"]:
        failures.append("evidencePreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if preview.get("previewStatus") != expected["previewStatus"]:
        failures.append("previewStatus must remain candidate_preview")
    if preview.get("executionStatus") != expected["executionStatus"]:
        failures.append("executionStatus must remain not_executed")
    if preview.get("executionMode") != expected["executionMode"]:
        failures.append("preview executionMode mismatch")
    if preview.get("previewType") != expected["previewType"]:
        failures.append("previewType mismatch")
    if preview.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("evidence preview must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("evidence preview must state notFinalAcceptance=true")

    if source_request.get("finalExecutionRequestStatus") != expected["sourceFinalExecutionRequestStatus"]:
        failures.append("source final execution request must remain candidate_request")
    if request.get("executionStatus") != expected["sourceFinalExecutionRequestExecutionStatus"]:
        failures.append("source final execution request executionStatus must remain not_executed")
    if request.get("dryRunOnly") is not True:
        failures.append("source final execution request must remain dryRunOnly=true")
    if preview.get("sourceFinalExecutionRequestId") != request.get("id"):
        failures.append("sourceFinalExecutionRequestId must match D36 request id")
    if data.get("coveredRequestStatus") != expected["coveredRequestStatus"]:
        failures.append("coveredRequestStatus mismatch")
    if data["coveredRequestStatus"] != request.get("requestStatus"):
        failures.append("covered request status must match D36 request status")

    fields = set(preview.get("previewFields", []))
    if len(fields) != expected["previewFieldCount"]:
        failures.append("previewFieldCount mismatch")
    for field in {
        "evidenceId",
        "evidenceType",
        "tenantId",
        "projectId",
        "sourceRequestRef",
        "sourceGuardRef",
        "sourceStepRef",
        "authorityRefs",
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
        "createdBy",
        "createdAt",
        "status",
    }:
        if field not in fields:
            failures.append(f"missing preview field: {field}")

    checks = set(preview.get("previewChecks", []))
    if len(checks) != expected["previewCheckCount"]:
        failures.append("previewCheckCount mismatch")
    for check in {
        "source_final_execution_request_status_is_candidate_request",
        "source_final_execution_request_execution_status_is_not_executed",
        "source_final_execution_request_is_dry_run_only",
        "execution_mode_is_dry_run_no_write",
        "preview_status_is_candidate_preview",
        "preview_contains_source_request_ref",
        "preview_contains_source_guard_ref",
        "preview_contains_source_step_ref",
        "preview_contains_authority_refs",
        "preview_contains_human_authorization_ref",
        "preview_contains_committee_authorization_ref",
        "preview_contains_freeze_gate_result_ref",
        "preview_contains_duplicate_check_ref",
        "preview_contains_idempotency_key",
        "preview_contains_execution_lock_ref",
        "preview_contains_pre_write_snapshot_ref",
        "preview_contains_post_write_verification_plan_ref",
        "preview_contains_rollback_plan_ref",
        "preview_contains_audit_trail_ref",
        "preview_does_not_write_harness_evidence",
        "preview_does_not_write_formal_evidence",
        "preview_requires_future_harness_execution",
    }:
        if check not in checks:
            failures.append(f"missing preview check: {check}")

    blocking_conditions = set(preview.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    for blocking in {
        "source_request_not_candidate_request",
        "source_request_already_executed",
        "source_request_not_dry_run_only",
        "missing_source_request_ref",
        "missing_authority_refs",
        "missing_human_authorization",
        "missing_committee_authorization",
        "missing_freeze_gate_result",
        "missing_duplicate_check",
        "missing_idempotency_key",
        "missing_execution_lock",
        "missing_pre_write_snapshot",
        "missing_post_write_verification_plan",
        "missing_rollback_plan",
        "missing_audit_trail",
    }:
        if blocking not in blocking_conditions:
            failures.append(f"missing blocking condition: {blocking}")

    forbidden_actions = set(preview.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "write_formal_evidence",
        "write_harness_evidence",
        "execute_formal_write",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "convert_preview_to_evidence",
        "convert_request_to_approved",
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
        "preview_converted_to_evidence",
        "request_promoted_to_approved",
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
        "\"evidencePreviewStatus\": \"accepted\"",
        "\"previewStatus\": \"written\"",
        "\"executionStatus\": \"executed\"",
        "\"executionMode\": \"write\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden evidence preview term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_execution_evidence_preview_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_execution_evidence_preview_dry_run=pass "
        f"status={expected['evidencePreviewStatus']} "
        f"preview_type={expected['previewType']} "
        f"preview_status={expected['previewStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"execution_mode={expected['executionMode']} "
        f"source_request_status={expected['sourceFinalExecutionRequestStatus']} "
        f"source_request_execution_status={expected['sourceFinalExecutionRequestExecutionStatus']} "
        f"covered_request_status={expected['coveredRequestStatus']} "
        f"preview_fields={expected['previewFieldCount']} "
        f"preview_checks={expected['previewCheckCount']} "
        f"blocking_conditions={expected['blockingConditionCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "authority_refs=covered "
        "future_harness_execution=covered "
        "preview_not_evidence=covered "
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
