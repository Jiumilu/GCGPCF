#!/usr/bin/env python3
"""Validate D142 GCKF P0 formal evidence execution signer receipt preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-signer-receipt-preview-current-state-d142-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-signer-receipt-preview-current-state-d142-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-signer-receipt-preview-current-state-d142-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D142-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_signer_receipt_preview_current_state_d142=fail reason={message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run_command(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        fail(f"command_failed:{' '.join(args)}:{stderr}")
    return result.stdout.strip()


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_all(actual: set[str], expected_values: set[str], label: str) -> None:
    for value in expected_values:
        require(value in actual, f"missing_{label}:{value}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d142_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_receipt = load_json(ROOT / fixture["sourceHistoricalSignerReceiptPreview"])
    current_approval = load_json(ROOT / fixture["sourceCurrentApprovalPacketPreview"])
    receipt = fixture["signerReceiptPreview"]
    source_receipt = historical_receipt["signerReceiptPreview"]
    approval = current_approval["approvalPacketPreview"]

    require(fixture.get("signerReceiptPreviewStatus") == expected["signerReceiptPreviewStatus"], "signer_receipt_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(receipt.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(receipt.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(receipt.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(receipt.get("approvalExecutionStatus") == expected["approvalExecutionStatus"], "approval_execution_status_mismatch")
    require(receipt.get("receiptExecutionStatus") == expected["receiptExecutionStatus"], "receipt_execution_status_mismatch")
    require(receipt.get("resendExecutionStatus") == expected["resendExecutionStatus"], "resend_execution_status_mismatch")
    require(receipt.get("escalationExecutionStatus") == expected["escalationExecutionStatus"], "escalation_execution_status_mismatch")
    require(receipt.get("retryExecutionStatus") == expected["retryExecutionStatus"], "retry_execution_status_mismatch")
    require(receipt.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(receipt.get("executionMode") == expected["executionMode"], "receipt_execution_mode_mismatch")
    require(receipt.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(receipt.get("sourceApprovalPacketPreviewId") == approval.get("id"), "source_approval_packet_preview_id_mismatch")

    require(historical_receipt.get("signerReceiptPreviewStatus") == "candidate_preview", "historical_signer_receipt_preview_status_mismatch")
    require(source_receipt.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_receipt.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_approval.get("approvalPacketPreviewStatus") == expected["sourceApprovalPacketPreviewStatus"], "source_approval_packet_preview_status_mismatch")
    require(approval.get("executionStatus") == expected["sourceApprovalPacketExecutionStatus"], "source_approval_packet_execution_status_mismatch")
    require(approval.get("approvalExecutionStatus") == expected["sourceApprovalExecutionStatus"], "source_approval_execution_status_mismatch")
    require(approval.get("retryExecutionStatus") == expected["sourceRetryExecutionStatus"], "source_retry_execution_status_mismatch")
    require(approval.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredApprovalPacketPreviewStatus") == expected["coveredApprovalPacketPreviewStatus"], "covered_approval_packet_preview_status_mismatch")
    require(fixture["coveredApprovalPacketPreviewStatus"] == approval.get("previewStatus"), "covered_approval_packet_preview_not_matched")

    signer_roles = set(receipt.get("signerRoles", []))
    require(len(signer_roles) == expected["signerRoleCount"], "signer_role_count_mismatch")
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
        "signer_role",
    )
    require(signer_roles == set(approval.get("approvalRoles", [])), "signer_roles_not_matched_to_approval_roles")

    channels = set(receipt.get("receiptChannels", []))
    require(len(channels) == expected["receiptChannelCount"], "receipt_channel_count_mismatch")
    require_all(
        channels,
        {
            "controlled_register_ack",
            "harness_review_queue_ack",
            "committee_queue_ack",
            "business_owner_ack",
        },
        "receipt_channel",
    )

    states = set(receipt.get("receiptStates", []))
    require(len(states) == expected["receiptStateCount"], "receipt_state_count_mismatch")
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
        "receipt_state",
    )

    checks = set(receipt.get("receiptChecks", []))
    require(len(checks) == expected["receiptCheckCount"], "receipt_check_count_mismatch")
    require_all(
        checks,
        {
            "source_approval_packet_preview_status_is_candidate_preview_with_hold",
            "source_approval_packet_execution_status_is_not_executed",
            "source_approval_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_approval_packet_is_dry_run_only",
            "signer_receipt_preview_status_is_candidate_preview_with_hold",
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
            "preview_hold_context_refs",
            "assert_receipt_not_executed",
            "assert_resend_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "receipt_check",
    )

    refs = set(receipt.get("requiredReceiptRefs", []))
    require(len(refs) == expected["requiredReceiptRefCount"], "required_receipt_ref_count_mismatch")
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
            "holdContextRefs",
        },
        "required_receipt_ref",
    )

    blocking_conditions = set(receipt.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_approval_packet_not_candidate_preview_with_hold",
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
            "missing_hold_context_refs",
            "receipt_preview_attempts_notification_send",
            "receipt_preview_attempts_receipt_write",
            "receipt_preview_attempts_resend",
            "receipt_preview_attempts_escalation",
            "receipt_preview_attempts_approval",
            "receipt_preview_attempts_unfreeze",
            "receipt_preview_attempts_formal_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(receipt.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
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
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_approval.get("holdContextRefs", []))
    for hold_ref in hold_refs:
        require(hold_ref in source_hold_refs, f"missing_hold_context_ref:{hold_ref}")

    for key in [
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ]:
        require(fixture["currentGateAssertions"].get(key) is False, f"current_gate_assertion_not_false:{key}")

    require(len(fixture.get("requiredSourceRefs", [])) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")

    require(evidence.get("current_signer_receipt_preview_status") == "candidate_preview_with_hold", "evidence_signer_receipt_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("receipt_scope", {}).get("signer_roles") == 8, "evidence_signer_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_approval_packet_preview_status") == "candidate_preview_with_hold", "evidence_source_approval_packet_preview_status_mismatch")

    d43_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_signer_receipt_preview_dry_run.py")
    require(d43_output.startswith("gckf_p0_formal_evidence_execution_signer_receipt_preview_dry_run=pass"), "d43_validator_not_pass")

    d141_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_current_state_d141.py")
    require(d141_output.startswith("gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_current_state_d141=pass"), "d141_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_signer_receipt_preview_current_state_d142=pass")
    print(f"signer_receipt_preview_status={fixture.get('signerReceiptPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={receipt.get('previewStatus')}")
    print(f"execution_status={receipt.get('executionStatus')}")
    print(f"approval_execution_status={receipt.get('approvalExecutionStatus')}")
    print(f"receipt_execution_status={receipt.get('receiptExecutionStatus')}")
    print(f"resend_execution_status={receipt.get('resendExecutionStatus')}")
    print(f"escalation_execution_status={receipt.get('escalationExecutionStatus')}")
    print(f"signer_roles={len(signer_roles)}")
    print(f"receipt_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
