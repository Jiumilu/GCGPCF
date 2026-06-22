#!/usr/bin/env python3
"""Validate D143 GCKF P0 formal evidence execution signer receipt escalation digest preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-signer-receipt-escalation-digest-preview-current-state-d143-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-signer-receipt-escalation-digest-preview-current-state-d143-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-signer-receipt-escalation-digest-preview-current-state-d143-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D143-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_current_state_d143=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d143_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_digest = load_json(ROOT / fixture["sourceHistoricalEscalationDigestPreview"])
    current_receipt = load_json(ROOT / fixture["sourceCurrentSignerReceiptPreview"])
    digest = fixture["escalationDigestPreview"]
    source_digest = historical_digest["escalationDigestPreview"]
    receipt = current_receipt["signerReceiptPreview"]

    require(fixture.get("escalationDigestPreviewStatus") == expected["escalationDigestPreviewStatus"], "escalation_digest_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(digest.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(digest.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(digest.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(digest.get("receiptExecutionStatus") == expected["receiptExecutionStatus"], "receipt_execution_status_mismatch")
    require(digest.get("resendExecutionStatus") == expected["resendExecutionStatus"], "resend_execution_status_mismatch")
    require(digest.get("escalationExecutionStatus") == expected["escalationExecutionStatus"], "escalation_execution_status_mismatch")
    require(digest.get("approvalExecutionStatus") == expected["approvalExecutionStatus"], "approval_execution_status_mismatch")
    require(digest.get("retryExecutionStatus") == expected["retryExecutionStatus"], "retry_execution_status_mismatch")
    require(digest.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(digest.get("executionMode") == expected["executionMode"], "digest_execution_mode_mismatch")
    require(digest.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(digest.get("sourceSignerReceiptPreviewId") == receipt.get("id"), "source_signer_receipt_preview_id_mismatch")

    require(historical_digest.get("escalationDigestPreviewStatus") == "candidate_preview", "historical_escalation_digest_preview_status_mismatch")
    require(source_digest.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_digest.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_receipt.get("signerReceiptPreviewStatus") == expected["sourceSignerReceiptPreviewStatus"], "source_signer_receipt_preview_status_mismatch")
    require(receipt.get("receiptExecutionStatus") == expected["sourceReceiptExecutionStatus"], "source_receipt_execution_status_mismatch")
    require(receipt.get("resendExecutionStatus") == expected["sourceResendExecutionStatus"], "source_resend_execution_status_mismatch")
    require(receipt.get("escalationExecutionStatus") == expected["sourceEscalationExecutionStatus"], "source_escalation_execution_status_mismatch")
    require(receipt.get("approvalExecutionStatus") == expected["sourceApprovalExecutionStatus"], "source_approval_execution_status_mismatch")
    require(receipt.get("retryExecutionStatus") == expected["sourceRetryExecutionStatus"], "source_retry_execution_status_mismatch")
    require(receipt.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredSignerReceiptPreviewStatus") == expected["coveredSignerReceiptPreviewStatus"], "covered_signer_receipt_preview_status_mismatch")
    require(fixture["coveredSignerReceiptPreviewStatus"] == receipt.get("previewStatus"), "covered_signer_receipt_preview_not_matched")

    roles = set(digest.get("digestAudienceRoles", []))
    require(len(roles) == expected["digestAudienceRoleCount"], "digest_audience_role_count_mismatch")
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
        "digest_audience_role",
    )
    require(roles == set(receipt.get("signerRoles", [])), "digest_audience_roles_not_matched_to_signer_roles")

    sections = set(digest.get("digestSections", []))
    require(len(sections) == expected["digestSectionCount"], "digest_section_count_mismatch")
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
        "digest_section",
    )

    triggers = set(digest.get("escalationTriggers", []))
    require(len(triggers) == expected["escalationTriggerCount"], "escalation_trigger_count_mismatch")
    require_all(
        triggers,
        {
            "required_signer_refused",
            "required_signer_timed_out",
            "receipt_needs_repair",
            "stop_authority_not_acknowledged",
            "business_owner_not_acknowledged",
        },
        "escalation_trigger",
    )

    checks = set(digest.get("digestChecks", []))
    require(len(checks) == expected["digestCheckCount"], "digest_check_count_mismatch")
    require_all(
        checks,
        {
            "source_signer_receipt_preview_status_is_candidate_preview_with_hold",
            "source_receipt_execution_status_is_not_executed",
            "source_resend_execution_status_is_not_executed",
            "source_escalation_execution_status_is_not_executed",
            "source_approval_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_signer_receipt_is_dry_run_only",
            "escalation_digest_preview_status_is_candidate_preview_with_hold",
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
            "preview_hold_context_refs",
            "assert_digest_not_sent",
            "assert_escalation_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "digest_check",
    )

    refs = set(digest.get("requiredDigestRefs", []))
    require(len(refs) == expected["requiredDigestRefCount"], "required_digest_ref_count_mismatch")
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
            "holdContextRefs",
        },
        "required_digest_ref",
    )

    blocking_conditions = set(digest.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_signer_receipt_not_candidate_preview_with_hold",
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
            "missing_hold_context_refs",
            "digest_preview_attempts_notification_send",
            "digest_preview_attempts_resend",
            "digest_preview_attempts_escalation",
            "digest_preview_attempts_approval",
            "digest_preview_attempts_formal_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(digest.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
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
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    forbidden_outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(forbidden_outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_receipt.get("holdContextRefs", []))
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

    require(evidence.get("current_escalation_digest_preview_status") == "candidate_preview_with_hold", "evidence_escalation_digest_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("digest_scope", {}).get("digest_audience_roles") == 8, "evidence_digest_audience_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_signer_receipt_preview_status") == "candidate_preview_with_hold", "evidence_source_signer_receipt_preview_status_mismatch")

    d44_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_dry_run.py")
    require(d44_output.startswith("gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_dry_run=pass"), "d44_validator_not_pass")

    d142_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_signer_receipt_preview_current_state_d142.py")
    require(d142_output.startswith("gckf_p0_formal_evidence_execution_signer_receipt_preview_current_state_d142=pass"), "d142_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_current_state_d143=pass")
    print(f"escalation_digest_preview_status={fixture.get('escalationDigestPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={digest.get('previewStatus')}")
    print(f"execution_status={digest.get('executionStatus')}")
    print(f"receipt_execution_status={digest.get('receiptExecutionStatus')}")
    print(f"resend_execution_status={digest.get('resendExecutionStatus')}")
    print(f"escalation_execution_status={digest.get('escalationExecutionStatus')}")
    print(f"digest_audience_roles={len(roles)}")
    print(f"digest_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
