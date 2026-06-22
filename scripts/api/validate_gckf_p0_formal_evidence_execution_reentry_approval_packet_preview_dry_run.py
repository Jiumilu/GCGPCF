#!/usr/bin/env python3
"""Validate P0 formal evidence execution re-entry approval packet preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-reentry-approval-packet-preview-dry-run-v0.1.json"
)


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require_all(actual: set[str], expected_values: set[str], label: str, failures: list[str]) -> None:
    for value in expected_values:
        if value not in actual:
            failures.append(f"missing {label}: {value}")


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_preflight = load_json(data["sourceReentryPreflightPreview"])
    source = source_preflight["reentryPreflightPreview"]
    approval = data["approvalPacketPreview"]

    if data.get("approvalPacketPreviewStatus") != expected["approvalPacketPreviewStatus"]:
        failures.append("approvalPacketPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("approval packet preview must state notFinalAcceptance=true")
    if approval.get("previewType") != expected["previewType"]:
        failures.append("approval packet previewType mismatch")
    if approval.get("previewStatus") != expected["previewStatus"]:
        failures.append("approval packet previewStatus must remain candidate_preview")
    if approval.get("executionStatus") != expected["executionStatus"]:
        failures.append("approval packet executionStatus must remain not_executed")
    if approval.get("approvalExecutionStatus") != expected["approvalExecutionStatus"]:
        failures.append("approvalExecutionStatus must remain not_executed")
    if approval.get("retryExecutionStatus") != expected["retryExecutionStatus"]:
        failures.append("retryExecutionStatus must remain not_executed")
    if approval.get("unfreezeExecutionStatus") != expected["unfreezeExecutionStatus"]:
        failures.append("unfreezeExecutionStatus must remain not_executed")
    if approval.get("executionMode") != expected["executionMode"]:
        failures.append("approval packet executionMode mismatch")
    if approval.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("approval packet preview must remain dryRunOnly=true")

    if source_preflight.get("reentryPreflightPreviewStatus") != expected["sourceReentryPreflightPreviewStatus"]:
        failures.append("source reentry preflight preview must remain candidate_preview")
    if source.get("reentryExecutionStatus") != expected["sourceReentryExecutionStatus"]:
        failures.append("source reentryExecutionStatus must remain not_executed")
    if source.get("unfreezeExecutionStatus") != expected["sourceUnfreezeExecutionStatus"]:
        failures.append("source unfreezeExecutionStatus must remain not_executed")
    if source.get("retryExecutionStatus") != expected["sourceRetryExecutionStatus"]:
        failures.append("source retryExecutionStatus must remain not_executed")
    if source.get("dryRunOnly") is not True:
        failures.append("source reentry preflight must remain dryRunOnly=true")
    if approval.get("sourceReentryPreflightPreviewId") != source.get("id"):
        failures.append("sourceReentryPreflightPreviewId must match D41 preflight preview id")
    if data.get("coveredReentryPreflightPreviewStatus") != expected["coveredReentryPreflightPreviewStatus"]:
        failures.append("coveredReentryPreflightPreviewStatus mismatch")
    if data["coveredReentryPreflightPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered reentry preflight preview status must match D41 preview status")

    roles = set(approval.get("approvalRoles", []))
    if len(roles) != expected["approvalRoleCount"]:
        failures.append("approvalRoleCount mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "repair_reviewer",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
        },
        "approval role",
        failures,
    )

    sections = set(approval.get("approvalPacketSections", []))
    if len(sections) != expected["approvalPacketSectionCount"]:
        failures.append("approvalPacketSectionCount mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "incident_summary",
            "repair_summary",
            "reentry_preflight_summary",
            "freeze_release_candidate",
            "execution_lock_renewal",
            "approval_refresh",
            "verification_plan_refresh",
            "rollback_drill_refresh",
            "waes_reentry_gate",
            "kwe_reentry_work_item",
            "harness_review_input",
            "responsibility_boundary",
            "negative_gate_result",
            "no_write_attestation",
        },
        "approval packet section",
        failures,
    )

    checks = set(approval.get("approvalChecks", []))
    if len(checks) != expected["approvalCheckCount"]:
        failures.append("approvalCheckCount mismatch")
    require_all(
        checks,
        {
            "source_reentry_preflight_preview_status_is_candidate_preview",
            "source_reentry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_reentry_preflight_is_dry_run_only",
            "approval_packet_preview_status_is_candidate_preview",
            "request_owner_signer_present",
            "repair_reviewer_signer_present",
            "waes_gate_owner_signer_present",
            "kwe_workflow_owner_signer_present",
            "harness_reviewer_signer_present",
            "committee_representative_signer_present",
            "stop_authority_owner_signer_present",
            "business_system_owner_signer_present",
            "responsibility_boundary_present",
            "approval_sequence_present",
            "harness_review_input_present",
            "negative_gate_result_present",
            "no_write_attestation_present",
            "assert_approval_not_executed",
            "assert_retry_not_executed",
            "assert_unfreeze_not_executed",
            "assert_no_write_boundary",
            "approval_requires_future_harness_execution",
        },
        "approval check",
        failures,
    )

    refs = set(approval.get("requiredApprovalRefs", []))
    if len(refs) != expected["requiredApprovalRefCount"]:
        failures.append("requiredApprovalRefCount mismatch")
    require_all(
        refs,
        {
            "sourceReentryPreflightPreviewRef",
            "sourceIncidentEscalationPreviewRef",
            "repairEvidencePacketRef",
            "freezeReleaseCandidateRef",
            "executionLockRenewalCandidateRef",
            "approvalRefreshCandidateRef",
            "verificationPlanRefreshCandidateRef",
            "rollbackDrillRefreshCandidateRef",
            "waesReentryGateCandidateRef",
            "kweReentryWorkItemCandidateRef",
            "harnessReviewInputRef",
            "responsibilityBoundaryRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
            "requestOwnerSignerRef",
            "repairReviewerSignerRef",
            "waesGateOwnerSignerRef",
            "kweWorkflowOwnerSignerRef",
            "harnessReviewerSignerRef",
            "committeeRepresentativeSignerRef",
            "stopAuthorityOwnerSignerRef",
            "businessSystemOwnerSignerRef",
        },
        "required approval ref",
        failures,
    )

    blocking_conditions = set(approval.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    require_all(
        blocking_conditions,
        {
            "source_reentry_preflight_not_candidate_preview",
            "source_reentry_already_executed",
            "source_unfreeze_already_executed",
            "source_retry_already_executed",
            "source_reentry_preflight_not_dry_run_only",
            "missing_source_reentry_preflight_ref",
            "missing_repair_evidence_packet_ref",
            "missing_freeze_release_candidate_ref",
            "missing_execution_lock_renewal_candidate_ref",
            "missing_approval_refresh_candidate_ref",
            "missing_verification_plan_refresh_candidate_ref",
            "missing_rollback_drill_refresh_candidate_ref",
            "missing_waes_reentry_gate_candidate_ref",
            "missing_kwe_reentry_work_item_candidate_ref",
            "missing_harness_review_input_ref",
            "missing_responsibility_boundary_ref",
            "missing_negative_gate_result_ref",
            "missing_no_write_attestation_ref",
            "missing_required_signer",
            "approval_preview_attempts_approval",
            "approval_preview_attempts_retry",
            "approval_preview_attempts_unfreeze",
            "approval_preview_attempts_write",
        },
        "blocking condition",
        failures,
    )

    forbidden_actions = set(approval.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_approval",
            "execute_formal_write",
            "execute_retry",
            "execute_unfreeze",
            "release_freeze",
            "release_execution_lock",
            "write_approval_result",
            "write_reentry_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_verification_result",
            "write_rollback_result",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "mark_production_ready",
            "convert_approval_preview_to_result",
        },
        "forbidden action",
        failures,
    )

    required_sources = set(data.get("requiredSourceRefs", []))
    if len(required_sources) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for relative_path in required_sources:
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")

    forbidden_outputs = set(data.get("forbiddenOutputs", []))
    forbidden_markers = {
        "approval_executed",
        "formal_write_executed",
        "retry_executed",
        "unfreeze_executed",
        "freeze_released",
        "execution_lock_released",
        "approval_result_written",
        "reentry_result_written",
        "formal_harness_evidence_record_written",
        "harness_evidence_record_written",
        "verification_result_written",
        "rollback_result_written",
        "accepted",
        "integrated",
        "production_ready",
        "business_write_enabled",
        "kds_write_enabled",
        "approval_preview_converted_to_result",
    }
    require_all(forbidden_outputs, forbidden_markers, "forbidden output marker", failures)

    for key in (
        "writesFormalEvidence",
        "writesHarnessEvidence",
        "writesVerificationResult",
        "writesRollbackResult",
        "writesApprovalResult",
        "writesReentryResult",
        "writesAcceptedLifecycle",
        "startsServer",
        "connectsDatabase",
        "callsExternalApi",
        "writesKds",
        "writesBusinessSystem",
    ):
        if expected[key] is not False:
            failures.append(f"expectedSummary.{key} must be false")
    if expected["noWrite"] is not True:
        failures.append("expectedSummary.noWrite must be true")

    if failures:
        print("gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_dry_run=pass "
        f"status={data['approvalPacketPreviewStatus']} "
        f"preview_type={approval['previewType']} "
        f"preview_status={approval['previewStatus']} "
        f"execution_status={approval['executionStatus']} "
        f"approval_execution_status={approval['approvalExecutionStatus']} "
        f"retry_execution_status={approval['retryExecutionStatus']} "
        f"unfreeze_execution_status={approval['unfreezeExecutionStatus']} "
        f"execution_mode={data['executionMode']} "
        f"source_reentry_preflight_status={source_preflight['reentryPreflightPreviewStatus']} "
        f"source_reentry_execution_status={source['reentryExecutionStatus']} "
        f"source_unfreeze_execution_status={source['unfreezeExecutionStatus']} "
        f"source_retry_execution_status={source['retryExecutionStatus']} "
        f"covered_reentry_preflight_status={data['coveredReentryPreflightPreviewStatus']} "
        f"approval_roles={len(roles)} "
        f"approval_packet_sections={len(sections)} "
        f"approval_checks={len(checks)} "
        f"required_approval_refs={len(refs)} "
        f"blocking_conditions={len(blocking_conditions)} "
        f"forbidden_actions={len(forbidden_actions)} "
        f"required_sources={len(required_sources)} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "signer_responsibilities=covered "
        "responsibility_boundary=covered "
        "harness_review_input=covered "
        "negative_gate_result=covered "
        "no_write_attestation=covered "
        "starts_server=0 connects_database=0 calls_external_api=0 "
        "writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 writes_formal_evidence=0 "
        "writes_verification_result=0 writes_rollback_result=0 "
        "writes_approval_result=0 writes_reentry_result=0 "
        "executes_approval=0 executes_retry=0 executes_unfreeze=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
