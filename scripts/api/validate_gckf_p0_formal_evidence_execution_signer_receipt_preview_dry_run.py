#!/usr/bin/env python3
"""Validate P0 formal evidence execution signer receipt preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-signer-receipt-preview-dry-run-v0.1.json"
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

    source_approval_packet = load_json(data["sourceApprovalPacketPreview"])
    source = source_approval_packet["approvalPacketPreview"]
    receipt = data["signerReceiptPreview"]

    if data.get("signerReceiptPreviewStatus") != expected["signerReceiptPreviewStatus"]:
        failures.append("signerReceiptPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("signer receipt preview must state notFinalAcceptance=true")
    if receipt.get("previewType") != expected["previewType"]:
        failures.append("signer receipt previewType mismatch")
    if receipt.get("previewStatus") != expected["previewStatus"]:
        failures.append("signer receipt previewStatus must remain candidate_preview")
    if receipt.get("executionStatus") != expected["executionStatus"]:
        failures.append("signer receipt executionStatus must remain not_executed")
    if receipt.get("approvalExecutionStatus") != expected["approvalExecutionStatus"]:
        failures.append("approvalExecutionStatus must remain not_executed")
    if receipt.get("receiptExecutionStatus") != expected["receiptExecutionStatus"]:
        failures.append("receiptExecutionStatus must remain not_executed")
    if receipt.get("resendExecutionStatus") != expected["resendExecutionStatus"]:
        failures.append("resendExecutionStatus must remain not_executed")
    if receipt.get("escalationExecutionStatus") != expected["escalationExecutionStatus"]:
        failures.append("escalationExecutionStatus must remain not_executed")
    if receipt.get("retryExecutionStatus") != expected["retryExecutionStatus"]:
        failures.append("retryExecutionStatus must remain not_executed")
    if receipt.get("unfreezeExecutionStatus") != expected["unfreezeExecutionStatus"]:
        failures.append("unfreezeExecutionStatus must remain not_executed")
    if receipt.get("executionMode") != expected["executionMode"]:
        failures.append("signer receipt executionMode mismatch")
    if receipt.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("signer receipt preview must remain dryRunOnly=true")

    if source_approval_packet.get("approvalPacketPreviewStatus") != expected["sourceApprovalPacketPreviewStatus"]:
        failures.append("source approval packet preview must remain candidate_preview")
    if source.get("executionStatus") != expected["sourceApprovalPacketExecutionStatus"]:
        failures.append("source approval packet executionStatus must remain not_executed")
    if source.get("approvalExecutionStatus") != expected["sourceApprovalExecutionStatus"]:
        failures.append("source approvalExecutionStatus must remain not_executed")
    if source.get("retryExecutionStatus") != expected["sourceRetryExecutionStatus"]:
        failures.append("source retryExecutionStatus must remain not_executed")
    if source.get("unfreezeExecutionStatus") != expected["sourceUnfreezeExecutionStatus"]:
        failures.append("source unfreezeExecutionStatus must remain not_executed")
    if source.get("dryRunOnly") is not True:
        failures.append("source approval packet must remain dryRunOnly=true")
    if receipt.get("sourceApprovalPacketPreviewId") != source.get("id"):
        failures.append("sourceApprovalPacketPreviewId must match D42 approval packet preview id")
    if data.get("coveredApprovalPacketPreviewStatus") != expected["coveredApprovalPacketPreviewStatus"]:
        failures.append("coveredApprovalPacketPreviewStatus mismatch")
    if data["coveredApprovalPacketPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered approval packet preview status must match D42 preview status")

    signer_roles = set(receipt.get("signerRoles", []))
    if len(signer_roles) != expected["signerRoleCount"]:
        failures.append("signerRoleCount mismatch")
    require_all(
        signer_roles,
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
        "signer role",
        failures,
    )
    if signer_roles != set(source.get("approvalRoles", [])):
        failures.append("signerRoles must mirror D42 approvalRoles")

    channels = set(receipt.get("receiptChannels", []))
    if len(channels) != expected["receiptChannelCount"]:
        failures.append("receiptChannelCount mismatch")
    require_all(
        channels,
        {
            "controlled_register_ack",
            "harness_review_queue_ack",
            "committee_queue_ack",
            "business_owner_ack",
        },
        "receipt channel",
        failures,
    )

    states = set(receipt.get("receiptStates", []))
    if len(states) != expected["receiptStateCount"]:
        failures.append("receiptStateCount mismatch")
    require_all(
        states,
        {
            "pending",
            "acknowledged",
            "refused",
            "needs_repair",
            "timed_out",
            "escalation_required",
            "voided",
        },
        "receipt state",
        failures,
    )

    checks = set(receipt.get("receiptChecks", []))
    if len(checks) != expected["receiptCheckCount"]:
        failures.append("receiptCheckCount mismatch")
    require_all(
        checks,
        {
            "source_approval_packet_preview_status_is_candidate_preview",
            "source_approval_packet_execution_status_is_not_executed",
            "source_approval_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_approval_packet_is_dry_run_only",
            "signer_receipt_preview_status_is_candidate_preview",
            "all_required_signer_roles_covered",
            "controlled_register_ack_channel_present",
            "harness_review_queue_ack_channel_present",
            "committee_queue_ack_channel_present",
            "business_owner_ack_channel_present",
            "pending_state_present",
            "acknowledged_state_present",
            "refused_state_present",
            "needs_repair_state_present",
            "timed_out_state_present",
            "escalation_required_state_present",
            "voided_state_present",
            "refusal_reason_required",
            "timeout_escalation_path_present",
            "resend_dispatch_candidate_present",
            "receipt_audit_snapshot_present",
            "negative_gate_result_present",
            "no_write_attestation_present",
            "assert_receipt_not_executed",
            "assert_resend_not_executed",
            "assert_no_write_boundary",
        },
        "receipt check",
        failures,
    )

    refs = set(receipt.get("requiredReceiptRefs", []))
    if len(refs) != expected["requiredReceiptRefCount"]:
        failures.append("requiredReceiptRefCount mismatch")
    require_all(
        refs,
        {
            "sourceApprovalPacketPreviewRef",
            "sourceReentryPreflightPreviewRef",
            "sourceIncidentEscalationPreviewRef",
            "approvalPacketRef",
            "approvalRoleRosterRef",
            "requestOwnerReceiptRef",
            "repairReviewerReceiptRef",
            "waesGateOwnerReceiptRef",
            "kweWorkflowOwnerReceiptRef",
            "harnessReviewerReceiptRef",
            "committeeRepresentativeReceiptRef",
            "stopAuthorityOwnerReceiptRef",
            "businessSystemOwnerReceiptRef",
            "controlledRegisterAckRef",
            "harnessReviewQueueAckRef",
            "committeeQueueAckRef",
            "businessOwnerAckRef",
            "refusalReasonPolicyRef",
            "timeoutEscalationPolicyRef",
            "resendDispatchCandidateRef",
            "receiptAuditSnapshotRef",
            "responsibilityBoundaryRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
            "futureHarnessExecutionApprovalRef",
        },
        "required receipt ref",
        failures,
    )

    blocking_conditions = set(receipt.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    require_all(
        blocking_conditions,
        {
            "source_approval_packet_not_candidate_preview",
            "source_approval_packet_already_executed",
            "source_approval_already_executed",
            "source_retry_already_executed",
            "source_unfreeze_already_executed",
            "source_approval_packet_not_dry_run_only",
            "missing_source_approval_packet_ref",
            "missing_approval_role_roster_ref",
            "missing_required_signer_receipt_ref",
            "missing_controlled_register_ack_ref",
            "missing_harness_review_queue_ack_ref",
            "missing_committee_queue_ack_ref",
            "missing_business_owner_ack_ref",
            "missing_refusal_reason_policy_ref",
            "missing_timeout_escalation_policy_ref",
            "missing_resend_dispatch_candidate_ref",
            "missing_receipt_audit_snapshot_ref",
            "missing_responsibility_boundary_ref",
            "missing_negative_gate_result_ref",
            "missing_no_write_attestation_ref",
            "receipt_preview_attempts_notification_send",
            "receipt_preview_attempts_receipt_write",
            "receipt_preview_attempts_resend",
            "receipt_preview_attempts_escalation",
            "receipt_preview_attempts_approval",
            "receipt_preview_attempts_unfreeze",
            "receipt_preview_attempts_formal_write",
        },
        "blocking condition",
        failures,
    )

    forbidden_actions = set(receipt.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    require_all(
        forbidden_actions,
        {
            "send_notification",
            "record_signer_receipt",
            "execute_resend_dispatch",
            "execute_escalation",
            "execute_approval",
            "execute_formal_write",
            "execute_retry",
            "execute_unfreeze",
            "release_freeze",
            "release_execution_lock",
            "write_receipt_result",
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
            "convert_receipt_preview_to_result",
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
            "notification_sent",
            "signer_receipt_recorded",
            "resend_dispatch_executed",
            "escalation_executed",
            "approval_executed",
            "formal_write_executed",
            "retry_executed",
            "unfreeze_executed",
            "freeze_released",
            "execution_lock_released",
            "receipt_result_written",
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
            "receipt_preview_converted_to_result",
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
        "sendsNotification",
        "recordsSignerReceipt",
        "executesResend",
        "executesEscalation",
        "executesApproval",
        "executesRetry",
        "executesUnfreeze",
        "writesFormalEvidence",
        "writesHarnessEvidence",
        "writesVerificationResult",
        "writesRollbackResult",
        "writesApprovalResult",
        "writesReentryResult",
        "writesReceiptResult",
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
        print("gckf_p0_formal_evidence_execution_signer_receipt_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "gckf_p0_formal_evidence_execution_signer_receipt_preview_dry_run=pass "
        f"status={data['signerReceiptPreviewStatus']} "
        f"preview_type={receipt['previewType']} "
        f"preview_status={receipt['previewStatus']} "
        f"execution_status={receipt['executionStatus']} "
        f"approval_execution_status={receipt['approvalExecutionStatus']} "
        f"receipt_execution_status={receipt['receiptExecutionStatus']} "
        f"resend_execution_status={receipt['resendExecutionStatus']} "
        f"escalation_execution_status={receipt['escalationExecutionStatus']} "
        f"retry_execution_status={receipt['retryExecutionStatus']} "
        f"unfreeze_execution_status={receipt['unfreezeExecutionStatus']} "
        f"execution_mode={data['executionMode']} "
        f"source_approval_packet_status={source_approval_packet['approvalPacketPreviewStatus']} "
        f"source_approval_packet_execution_status={source['executionStatus']} "
        f"source_approval_execution_status={source['approvalExecutionStatus']} "
        f"source_retry_execution_status={source['retryExecutionStatus']} "
        f"source_unfreeze_execution_status={source['unfreezeExecutionStatus']} "
        f"covered_approval_packet_status={data['coveredApprovalPacketPreviewStatus']} "
        f"signer_roles={len(signer_roles)} "
        f"receipt_channels={len(channels)} "
        f"receipt_states={len(states)} "
        f"receipt_checks={len(checks)} "
        f"required_receipt_refs={len(refs)} "
        f"blocking_conditions={len(blocking_conditions)} "
        f"forbidden_actions={len(forbidden_actions)} "
        f"forbidden_outputs={len(forbidden_outputs)} "
        f"required_sources={len(required_sources)} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "signer_receipt=covered "
        "refusal_path=covered "
        "timeout_escalation=covered "
        "resend_dispatch_candidate=covered "
        "receipt_audit_snapshot=covered "
        "negative_gate_result=covered "
        "no_write_attestation=covered "
        "starts_server=0 connects_database=0 calls_external_api=0 "
        "sends_notification=0 records_signer_receipt=0 executes_resend=0 "
        "executes_escalation=0 executes_approval=0 executes_retry=0 executes_unfreeze=0 "
        "writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 writes_formal_evidence=0 "
        "writes_verification_result=0 writes_rollback_result=0 "
        "writes_approval_result=0 writes_reentry_result=0 writes_receipt_result=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
