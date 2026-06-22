#!/usr/bin/env python3
"""Validate P0 formal evidence execution verification plan preview dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-verification-plan-preview-dry-run-v0.1.json"
)


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_preview = load_json(data["sourceEvidencePreview"])
    source = source_preview["evidencePreview"]
    plan = data["verificationPlanPreview"]

    if data.get("verificationPlanPreviewStatus") != expected["verificationPlanPreviewStatus"]:
        failures.append("verificationPlanPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if plan.get("previewStatus") != expected["previewStatus"]:
        failures.append("verification plan previewStatus must remain candidate_preview")
    if plan.get("executionStatus") != expected["executionStatus"]:
        failures.append("verification plan executionStatus must remain not_executed")
    if plan.get("executionMode") != expected["executionMode"]:
        failures.append("verification plan executionMode mismatch")
    if plan.get("previewType") != expected["previewType"]:
        failures.append("verification plan previewType mismatch")
    if plan.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("verification plan preview must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("verification plan preview must state notFinalAcceptance=true")

    if source_preview.get("evidencePreviewStatus") != expected["sourceEvidencePreviewStatus"]:
        failures.append("source evidence preview must remain candidate_preview")
    if source.get("executionStatus") != expected["sourceEvidencePreviewExecutionStatus"]:
        failures.append("source evidence preview executionStatus must remain not_executed")
    if source.get("dryRunOnly") is not True:
        failures.append("source evidence preview must remain dryRunOnly=true")
    if plan.get("sourceEvidencePreviewId") != source.get("id"):
        failures.append("sourceEvidencePreviewId must match D37 evidence preview id")
    if data.get("coveredEvidencePreviewStatus") != expected["coveredEvidencePreviewStatus"]:
        failures.append("coveredEvidencePreviewStatus mismatch")
    if data["coveredEvidencePreviewStatus"] != source.get("previewStatus"):
        failures.append("covered evidence preview status must match D37 preview status")

    scopes = set(plan.get("verificationScopes", []))
    if len(scopes) != expected["verificationScopeCount"]:
        failures.append("verificationScopeCount mismatch")
    for scope in {
        "source_request_integrity",
        "authority_chain_integrity",
        "execution_lock_integrity",
        "pre_write_snapshot_integrity",
        "post_write_readback_integrity",
        "harness_evidence_shape_integrity",
        "ledger_append_integrity",
        "audit_trail_integrity",
        "rollback_plan_integrity",
        "negative_no_write_boundary",
    }:
        if scope not in scopes:
            failures.append(f"missing verification scope: {scope}")

    checks = set(plan.get("verificationChecks", []))
    if len(checks) != expected["verificationCheckCount"]:
        failures.append("verificationCheckCount mismatch")
    for check in {
        "source_evidence_preview_status_is_candidate_preview",
        "source_evidence_preview_execution_status_is_not_executed",
        "source_evidence_preview_is_dry_run_only",
        "verification_plan_status_is_candidate_preview",
        "execution_mode_is_dry_run_no_write",
        "verify_source_request_ref_matches_d36_request",
        "verify_source_guard_ref_available_before_write",
        "verify_authority_refs_available_before_write",
        "verify_human_authorization_ref_available_before_write",
        "verify_committee_authorization_ref_available_before_write",
        "verify_freeze_gate_result_ref_available_before_write",
        "verify_duplicate_check_ref_available_before_write",
        "verify_idempotency_key_available_before_write",
        "verify_execution_lock_ref_available_before_write",
        "verify_pre_write_snapshot_ref_available_before_write",
        "verify_post_write_readback_plan_exists",
        "verify_harness_evidence_shape_plan_exists",
        "verify_ledger_append_plan_exists",
        "verify_audit_trail_plan_exists",
        "verify_rollback_plan_ref_available_before_write",
        "verify_negative_no_kds_write_boundary",
        "verify_negative_no_business_write_boundary",
        "verify_negative_no_accepted_lifecycle_boundary",
        "verification_requires_future_harness_execution",
    }:
        if check not in checks:
            failures.append(f"missing verification check: {check}")

    required_plan_refs = set(plan.get("requiredPlanRefs", []))
    if len(required_plan_refs) != expected["requiredPlanRefCount"]:
        failures.append("requiredPlanRefCount mismatch")
    for ref in {
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
        "postWriteReadbackPlanRef",
        "harnessEvidenceShapePlanRef",
        "ledgerAppendPlanRef",
        "auditTrailRef",
        "rollbackPlanRef",
    }:
        if ref not in required_plan_refs:
            failures.append(f"missing required plan ref: {ref}")

    blocking_conditions = set(plan.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    for blocking in {
        "source_evidence_preview_not_candidate_preview",
        "source_evidence_preview_already_executed",
        "source_evidence_preview_not_dry_run_only",
        "missing_source_request_ref",
        "missing_source_guard_ref",
        "missing_authority_refs",
        "missing_human_authorization_ref",
        "missing_committee_authorization_ref",
        "missing_freeze_gate_result_ref",
        "missing_duplicate_check_ref",
        "missing_idempotency_key",
        "missing_execution_lock_ref",
        "missing_pre_write_snapshot_ref",
        "missing_post_write_readback_plan",
        "missing_harness_evidence_shape_plan",
        "missing_ledger_append_plan",
        "missing_audit_trail_ref",
        "missing_rollback_plan_ref",
    }:
        if blocking not in blocking_conditions:
            failures.append(f"missing blocking condition: {blocking}")

    forbidden_actions = set(plan.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_verification_result",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "convert_plan_preview_to_result",
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
        "formal_write_executed",
        "formal_harness_evidence_record_written",
        "harness_evidence_record_written",
        "verification_result_written",
        "accepted",
        "integrated",
        "production_ready",
        "business_write_enabled",
        "kds_write_enabled",
        "plan_preview_converted_to_result",
        "execution_lock_released",
    ]:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")

    forbidden_terms = [
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesVerificationResult\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"dryRunOnly\": false",
        "\"verificationPlanPreviewStatus\": \"accepted\"",
        "\"previewStatus\": \"written\"",
        "\"executionStatus\": \"executed\"",
        "\"executionMode\": \"write\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
        "\"verificationResultWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden verification plan preview term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_execution_verification_plan_preview_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_execution_verification_plan_preview_dry_run=pass "
        f"status={expected['verificationPlanPreviewStatus']} "
        f"preview_type={expected['previewType']} "
        f"preview_status={expected['previewStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"execution_mode={expected['executionMode']} "
        f"source_evidence_preview_status={expected['sourceEvidencePreviewStatus']} "
        f"source_evidence_preview_execution_status={expected['sourceEvidencePreviewExecutionStatus']} "
        f"covered_evidence_preview_status={expected['coveredEvidencePreviewStatus']} "
        f"verification_scopes={expected['verificationScopeCount']} "
        f"verification_checks={expected['verificationCheckCount']} "
        f"required_plan_refs={expected['requiredPlanRefCount']} "
        f"blocking_conditions={expected['blockingConditionCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "post_write_readback_plan=covered "
        "harness_evidence_shape_plan=covered "
        "ledger_append_plan=covered "
        "negative_no_write_boundary=covered "
        "future_harness_execution=covered "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "writes_formal_evidence=0 "
        "writes_verification_result=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
