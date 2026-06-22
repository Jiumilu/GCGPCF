#!/usr/bin/env python3
"""Validate P0 formal evidence execution signer receipt escalation digest preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-signer-receipt-escalation-digest-preview-dry-run-v0.1.json"
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

    source_receipt = load_json(data["sourceSignerReceiptPreview"])
    source = source_receipt["signerReceiptPreview"]
    digest = data["escalationDigestPreview"]

    if data.get("escalationDigestPreviewStatus") != expected["escalationDigestPreviewStatus"]:
        failures.append("escalationDigestPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("escalation digest preview must state notFinalAcceptance=true")
    if digest.get("previewType") != expected["previewType"]:
        failures.append("escalation digest previewType mismatch")
    if digest.get("previewStatus") != expected["previewStatus"]:
        failures.append("escalation digest previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "receiptExecutionStatus",
        "resendExecutionStatus",
        "escalationExecutionStatus",
        "approvalExecutionStatus",
        "retryExecutionStatus",
        "unfreezeExecutionStatus",
    ):
        if digest.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if digest.get("executionMode") != expected["executionMode"]:
        failures.append("escalation digest executionMode mismatch")
    if digest.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("escalation digest preview must remain dryRunOnly=true")

    if source_receipt.get("signerReceiptPreviewStatus") != expected["sourceSignerReceiptPreviewStatus"]:
        failures.append("source signer receipt preview must remain candidate_preview")
    source_status_map = {
        "receiptExecutionStatus": "sourceReceiptExecutionStatus",
        "resendExecutionStatus": "sourceResendExecutionStatus",
        "escalationExecutionStatus": "sourceEscalationExecutionStatus",
        "approvalExecutionStatus": "sourceApprovalExecutionStatus",
        "retryExecutionStatus": "sourceRetryExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source signer receipt must remain dryRunOnly=true")
    if digest.get("sourceSignerReceiptPreviewId") != source.get("id"):
        failures.append("sourceSignerReceiptPreviewId must match D43 signer receipt preview id")
    if data.get("coveredSignerReceiptPreviewStatus") != expected["coveredSignerReceiptPreviewStatus"]:
        failures.append("coveredSignerReceiptPreviewStatus mismatch")
    if data["coveredSignerReceiptPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered signer receipt preview status must match D43 preview status")

    roles = set(digest.get("digestAudienceRoles", []))
    if len(roles) != expected["digestAudienceRoleCount"]:
        failures.append("digestAudienceRoleCount mismatch")
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
        "digest audience role",
        failures,
    )
    if roles != set(source.get("signerRoles", [])):
        failures.append("digestAudienceRoles must mirror D43 signerRoles")

    sections = set(digest.get("digestSections", []))
    if len(sections) != expected["digestSectionCount"]:
        failures.append("digestSectionCount mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "receipt_state_summary",
            "pending_signer_summary",
            "refusal_summary",
            "timeout_summary",
            "needs_repair_summary",
            "resend_candidate_batch",
            "escalation_candidate_batch",
            "human_confirmation_boundary",
            "committee_trigger_boundary",
            "negative_gate_result",
            "no_write_attestation",
        },
        "digest section",
        failures,
    )

    triggers = set(digest.get("escalationTriggers", []))
    if len(triggers) != expected["escalationTriggerCount"]:
        failures.append("escalationTriggerCount mismatch")
    require_all(
        triggers,
        {
            "required_signer_refused",
            "required_signer_timed_out",
            "receipt_needs_repair",
            "stop_authority_not_acknowledged",
            "business_owner_not_acknowledged",
        },
        "escalation trigger",
        failures,
    )

    checks = set(digest.get("digestChecks", []))
    if len(checks) != expected["digestCheckCount"]:
        failures.append("digestCheckCount mismatch")
    require_all(
        checks,
        {
            "source_signer_receipt_preview_status_is_candidate_preview",
            "source_receipt_execution_status_is_not_executed",
            "source_resend_execution_status_is_not_executed",
            "source_escalation_execution_status_is_not_executed",
            "source_approval_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_signer_receipt_is_dry_run_only",
            "escalation_digest_preview_status_is_candidate_preview",
            "all_digest_audience_roles_covered",
            "source_lineage_section_present",
            "receipt_state_summary_present",
            "pending_signer_summary_present",
            "refusal_summary_present",
            "timeout_summary_present",
            "needs_repair_summary_present",
            "resend_candidate_batch_present",
            "escalation_candidate_batch_present",
            "human_confirmation_boundary_present",
            "committee_trigger_boundary_present",
            "negative_gate_result_present",
            "no_write_attestation_present",
            "required_signer_refused_trigger_present",
            "required_signer_timed_out_trigger_present",
            "receipt_needs_repair_trigger_present",
            "stop_authority_not_acknowledged_trigger_present",
            "business_owner_not_acknowledged_trigger_present",
            "assert_digest_not_sent",
            "assert_escalation_not_executed",
            "assert_no_write_boundary",
        },
        "digest check",
        failures,
    )

    refs = set(digest.get("requiredDigestRefs", []))
    if len(refs) != expected["requiredDigestRefCount"]:
        failures.append("requiredDigestRefCount mismatch")
    require_all(
        refs,
        {
            "sourceSignerReceiptPreviewRef",
            "sourceApprovalPacketPreviewRef",
            "sourceReentryPreflightPreviewRef",
            "receiptStateSummaryRef",
            "pendingSignerSummaryRef",
            "refusalSummaryRef",
            "timeoutSummaryRef",
            "needsRepairSummaryRef",
            "resendCandidateBatchRef",
            "escalationCandidateBatchRef",
            "humanConfirmationBoundaryRef",
            "committeeTriggerBoundaryRef",
            "controlledRegisterAckRef",
            "harnessReviewQueueAckRef",
            "committeeQueueAckRef",
            "businessOwnerAckRef",
            "requestOwnerDigestRef",
            "repairReviewerDigestRef",
            "waesGateOwnerDigestRef",
            "kweWorkflowOwnerDigestRef",
            "harnessReviewerDigestRef",
            "committeeRepresentativeDigestRef",
            "stopAuthorityOwnerDigestRef",
            "businessSystemOwnerDigestRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
        },
        "required digest ref",
        failures,
    )

    blocking_conditions = set(digest.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    require_all(
        blocking_conditions,
        {
            "source_signer_receipt_not_candidate_preview",
            "source_receipt_already_executed",
            "source_resend_already_executed",
            "source_escalation_already_executed",
            "source_approval_already_executed",
            "source_retry_already_executed",
            "source_unfreeze_already_executed",
            "source_signer_receipt_not_dry_run_only",
            "missing_source_signer_receipt_ref",
            "missing_receipt_state_summary_ref",
            "missing_pending_signer_summary_ref",
            "missing_refusal_summary_ref",
            "missing_timeout_summary_ref",
            "missing_needs_repair_summary_ref",
            "missing_resend_candidate_batch_ref",
            "missing_escalation_candidate_batch_ref",
            "missing_human_confirmation_boundary_ref",
            "missing_committee_trigger_boundary_ref",
            "missing_controlled_register_ack_ref",
            "missing_harness_review_queue_ack_ref",
            "missing_committee_queue_ack_ref",
            "missing_business_owner_ack_ref",
            "missing_required_digest_audience",
            "missing_negative_gate_result_ref",
            "missing_no_write_attestation_ref",
            "digest_preview_attempts_notification_send",
            "digest_preview_attempts_resend",
            "digest_preview_attempts_escalation",
            "digest_preview_attempts_approval",
            "digest_preview_attempts_formal_write",
        },
        "blocking condition",
        failures,
    )

    forbidden_actions = set(digest.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    require_all(
        forbidden_actions,
        {
            "send_escalation_digest",
            "send_notification",
            "execute_resend_dispatch",
            "execute_escalation",
            "execute_approval",
            "execute_formal_write",
            "execute_retry",
            "execute_unfreeze",
            "release_freeze",
            "release_execution_lock",
            "record_digest_delivery",
            "write_receipt_result",
            "write_escalation_result",
            "write_resend_result",
            "write_approval_result",
            "write_reentry_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "mark_production_ready",
            "convert_digest_preview_to_result",
        },
        "forbidden action",
        failures,
    )

    forbidden_outputs = set(data.get("forbiddenOutputs", []))
    if len(forbidden_outputs) != expected["forbiddenOutputCount"]:
        failures.append("forbiddenOutputCount mismatch")
    require_all(
        forbidden_outputs,
        {
            "escalation_digest_sent",
            "notification_sent",
            "resend_dispatch_executed",
            "escalation_executed",
            "approval_executed",
            "formal_write_executed",
            "retry_executed",
            "unfreeze_executed",
            "freeze_released",
            "execution_lock_released",
            "digest_delivery_recorded",
            "receipt_result_written",
            "escalation_result_written",
            "resend_result_written",
            "approval_result_written",
            "reentry_result_written",
            "formal_harness_evidence_record_written",
            "harness_evidence_record_written",
            "accepted",
            "integrated",
            "production_ready",
            "business_write_enabled",
            "kds_write_enabled",
            "digest_preview_converted_to_result",
        },
        "forbidden output marker",
        failures,
    )

    required_sources = set(data.get("requiredSourceRefs", []))
    if len(required_sources) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for relative_path in required_sources:
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")

    for key in (
        "sendsEscalationDigest",
        "sendsNotification",
        "recordsDigestDelivery",
        "executesResend",
        "executesEscalation",
        "executesApproval",
        "executesRetry",
        "executesUnfreeze",
        "writesFormalEvidence",
        "writesHarnessEvidence",
        "writesReceiptResult",
        "writesEscalationResult",
        "writesResendResult",
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
        print("gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_dry_run=pass "
        f"status={data['escalationDigestPreviewStatus']} "
        f"preview_type={digest['previewType']} "
        f"preview_status={digest['previewStatus']} "
        f"execution_status={digest['executionStatus']} "
        f"receipt_execution_status={digest['receiptExecutionStatus']} "
        f"resend_execution_status={digest['resendExecutionStatus']} "
        f"escalation_execution_status={digest['escalationExecutionStatus']} "
        f"approval_execution_status={digest['approvalExecutionStatus']} "
        f"retry_execution_status={digest['retryExecutionStatus']} "
        f"unfreeze_execution_status={digest['unfreezeExecutionStatus']} "
        f"execution_mode={data['executionMode']} "
        f"source_signer_receipt_status={source_receipt['signerReceiptPreviewStatus']} "
        f"source_receipt_execution_status={source['receiptExecutionStatus']} "
        f"source_resend_execution_status={source['resendExecutionStatus']} "
        f"source_escalation_execution_status={source['escalationExecutionStatus']} "
        f"source_approval_execution_status={source['approvalExecutionStatus']} "
        f"source_retry_execution_status={source['retryExecutionStatus']} "
        f"source_unfreeze_execution_status={source['unfreezeExecutionStatus']} "
        f"covered_signer_receipt_status={data['coveredSignerReceiptPreviewStatus']} "
        f"digest_audience_roles={len(roles)} "
        f"digest_sections={len(sections)} "
        f"escalation_triggers={len(triggers)} "
        f"digest_checks={len(checks)} "
        f"required_digest_refs={len(refs)} "
        f"blocking_conditions={len(blocking_conditions)} "
        f"forbidden_actions={len(forbidden_actions)} "
        f"forbidden_outputs={len(forbidden_outputs)} "
        f"required_sources={len(required_sources)} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "receipt_state_summary=covered "
        "refusal_timeout_summary=covered "
        "resend_candidate_batch=covered "
        "escalation_candidate_batch=covered "
        "human_confirmation_boundary=covered "
        "committee_trigger_boundary=covered "
        "negative_gate_result=covered "
        "no_write_attestation=covered "
        "starts_server=0 connects_database=0 calls_external_api=0 "
        "sends_escalation_digest=0 sends_notification=0 records_digest_delivery=0 "
        "executes_resend=0 executes_escalation=0 executes_approval=0 "
        "executes_retry=0 executes_unfreeze=0 "
        "writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 writes_formal_evidence=0 "
        "writes_receipt_result=0 writes_escalation_result=0 writes_resend_result=0 "
        "writes_approval_result=0 writes_reentry_result=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
