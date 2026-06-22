#!/usr/bin/env python3
"""Validate D144 GCKF P0 formal evidence execution escalation digest human confirmation package preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-escalation-digest-human-confirmation-package-preview-current-state-d144-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-escalation-digest-human-confirmation-package-preview-current-state-d144-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-escalation-digest-human-confirmation-package-preview-current-state-d144-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D144-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_current_state_d144=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d144_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_package = load_json(ROOT / fixture["sourceHistoricalHumanConfirmationPackagePreview"])
    current_digest = load_json(ROOT / fixture["sourceCurrentEscalationDigestPreview"])
    package = fixture["humanConfirmationPackagePreview"]
    source_package = historical_package["humanConfirmationPackagePreview"]
    digest = current_digest["escalationDigestPreview"]

    require(fixture.get("humanConfirmationPackagePreviewStatus") == expected["humanConfirmationPackagePreviewStatus"], "human_confirmation_package_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(package.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(package.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(package.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(package.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(package.get("committeeExecutionStatus") == expected["committeeExecutionStatus"], "committee_execution_status_mismatch")
    require(package.get("resendExecutionStatus") == expected["resendExecutionStatus"], "resend_execution_status_mismatch")
    require(package.get("escalationExecutionStatus") == expected["escalationExecutionStatus"], "escalation_execution_status_mismatch")
    require(package.get("approvalExecutionStatus") == expected["approvalExecutionStatus"], "approval_execution_status_mismatch")
    require(package.get("retryExecutionStatus") == expected["retryExecutionStatus"], "retry_execution_status_mismatch")
    require(package.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(package.get("executionMode") == expected["executionMode"], "package_execution_mode_mismatch")
    require(package.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(package.get("sourceEscalationDigestPreviewId") == digest.get("id"), "source_escalation_digest_preview_id_mismatch")

    require(historical_package.get("humanConfirmationPackagePreviewStatus") == "candidate_preview", "historical_human_confirmation_package_preview_status_mismatch")
    require(source_package.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_package.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_digest.get("escalationDigestPreviewStatus") == expected["sourceEscalationDigestPreviewStatus"], "source_escalation_digest_preview_status_mismatch")
    require(digest.get("executionStatus") == expected["sourceDigestExecutionStatus"], "source_digest_execution_status_mismatch")
    require(digest.get("resendExecutionStatus") == expected["sourceResendExecutionStatus"], "source_resend_execution_status_mismatch")
    require(digest.get("escalationExecutionStatus") == expected["sourceEscalationExecutionStatus"], "source_escalation_execution_status_mismatch")
    require(digest.get("approvalExecutionStatus") == expected["sourceApprovalExecutionStatus"], "source_approval_execution_status_mismatch")
    require(digest.get("retryExecutionStatus") == expected["sourceRetryExecutionStatus"], "source_retry_execution_status_mismatch")
    require(digest.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredEscalationDigestPreviewStatus") == expected["coveredEscalationDigestPreviewStatus"], "covered_escalation_digest_preview_status_mismatch")
    require(fixture["coveredEscalationDigestPreviewStatus"] == digest.get("previewStatus"), "covered_escalation_digest_preview_not_matched")

    roles = set(package.get("reviewerRoles", []))
    require(len(roles) == expected["reviewerRoleCount"], "reviewer_role_count_mismatch")
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
        "reviewer_role",
    )
    require(roles == set(digest.get("digestAudienceRoles", [])), "reviewer_roles_not_matched_to_digest_audience_roles")

    sections = set(package.get("packageSections", []))
    require(len(sections) == expected["packageSectionCount"], "package_section_count_mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "escalation_digest_summary",
            "receipt_exception_summary",
            "resend_candidate_review",
            "escalation_candidate_review",
            "human_decision_options",
            "committee_trigger_review",
            "responsibility_boundary",
            "required_evidence_refs",
            "negative_gate_result",
            "no_write_attestation",
        },
        "package_section",
    )

    decision_options = set(package.get("decisionOptions", []))
    require(len(decision_options) == expected["decisionOptionCount"], "decision_option_count_mismatch")
    require_all(
        decision_options,
        {
            "approve_resend_candidate",
            "approve_escalation_candidate",
            "request_repair",
            "send_to_committee",
            "reject_candidate",
            "keep_frozen",
        },
        "decision_option",
    )

    committee_triggers = set(package.get("committeeTriggers", []))
    require(len(committee_triggers) == expected["committeeTriggerCount"], "committee_trigger_count_mismatch")
    require_all(
        committee_triggers,
        {
            "cross_unit_responsibility_dispute",
            "freeze_release_dispute",
            "formal_write_risk",
            "revenue_or_contribution_impact",
            "major_violation_suspected",
        },
        "committee_trigger",
    )

    checks = set(package.get("confirmationChecks", []))
    require(len(checks) == expected["confirmationCheckCount"], "confirmation_check_count_mismatch")
    require_all(
        checks,
        {
            "source_escalation_digest_preview_status_is_candidate_preview_with_hold",
            "source_digest_execution_status_is_not_executed",
            "source_resend_execution_status_is_not_executed",
            "source_escalation_execution_status_is_not_executed",
            "source_approval_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_escalation_digest_is_dry_run_only",
            "human_confirmation_package_preview_status_is_candidate_preview_with_hold",
            "all_reviewer_roles_covered",
            "source_lineage_section_present",
            "escalation_digest_summary_present",
            "receipt_exception_summary_present",
            "resend_candidate_review_present",
            "escalation_candidate_review_present",
            "human_decision_options_present",
            "committee_trigger_review_present",
            "responsibility_boundary_present",
            "required_evidence_refs_present",
            "negative_gate_result_present",
            "no_write_attestation_present",
            "approve_resend_candidate_option_present",
            "approve_escalation_candidate_option_present",
            "request_repair_option_present",
            "send_to_committee_option_present",
            "reject_candidate_option_present",
            "keep_frozen_option_present",
            "major_violation_trigger_present",
            "preview_hold_context_refs",
            "assert_confirmation_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "confirmation_check",
    )

    refs = set(package.get("requiredConfirmationRefs", []))
    require(len(refs) == expected["requiredConfirmationRefCount"], "required_confirmation_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceEscalationDigestPreviewRef",
            "sourceSignerReceiptPreviewRef",
            "sourceApprovalPacketPreviewRef",
            "escalationDigestSummaryRef",
            "receiptExceptionSummaryRef",
            "resendCandidateReviewRef",
            "escalationCandidateReviewRef",
            "humanDecisionOptionsRef",
            "committeeTriggerReviewRef",
            "responsibilityBoundaryRef",
            "requiredEvidenceRefs",
            "requestOwnerReviewerRef",
            "repairReviewerRef",
            "waesGateOwnerReviewerRef",
            "kweWorkflowOwnerReviewerRef",
            "harnessReviewerRef",
            "committeeRepresentativeReviewerRef",
            "stopAuthorityOwnerReviewerRef",
            "businessSystemOwnerReviewerRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
            "holdContextRefs",
        },
        "required_confirmation_ref",
    )

    blocking_conditions = set(package.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_escalation_digest_not_candidate_preview_with_hold",
            "source_digest_already_executed",
            "source_resend_already_executed",
            "source_escalation_already_executed",
            "source_approval_already_executed",
            "source_retry_already_executed",
            "source_unfreeze_already_executed",
            "source_escalation_digest_not_dry_run_only",
            "missing_source_escalation_digest_ref",
            "missing_escalation_digest_summary_ref",
            "missing_receipt_exception_summary_ref",
            "missing_resend_candidate_review_ref",
            "missing_escalation_candidate_review_ref",
            "missing_human_decision_options_ref",
            "missing_committee_trigger_review_ref",
            "missing_responsibility_boundary_ref",
            "missing_required_evidence_refs",
            "missing_required_reviewer",
            "missing_negative_gate_result_ref",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "confirmation_package_attempts_human_confirmation",
            "confirmation_package_attempts_committee_decision",
            "confirmation_package_attempts_resend",
            "confirmation_package_attempts_escalation",
            "confirmation_package_attempts_approval",
            "confirmation_package_attempts_formal_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(package.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_human_confirmation",
            "execute_committee_decision",
            "send_escalation_digest",
            "send_notification",
            "execute_resend_dispatch",
            "execute_escalation",
            "execute_approval",
            "execute_formal_write",
            "execute_retry",
            "execute_unfreeze",
            "release_freeze",
            "record_confirmation_result",
            "record_committee_result",
            "write_receipt_result",
            "write_escalation_result",
            "write_resend_result",
            "write_approval_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "convert_confirmation_package_preview_to_result",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    forbidden_outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(forbidden_outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_digest.get("holdContextRefs", []))
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

    require(evidence.get("current_human_confirmation_package_preview_status") == "candidate_preview_with_hold", "evidence_human_confirmation_package_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("reviewer_roles") == 8, "evidence_reviewer_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_escalation_digest_preview_status") == "candidate_preview_with_hold", "evidence_source_escalation_digest_preview_status_mismatch")

    d45_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_dry_run.py")
    require(d45_output.startswith("gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_dry_run=pass"), "d45_validator_not_pass")

    d143_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_current_state_d143.py")
    require(d143_output.startswith("gckf_p0_formal_evidence_execution_signer_receipt_escalation_digest_preview_current_state_d143=pass"), "d143_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_current_state_d144=pass")
    print(f"human_confirmation_package_preview_status={fixture.get('humanConfirmationPackagePreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={package.get('previewStatus')}")
    print(f"execution_status={package.get('executionStatus')}")
    print(f"confirmation_execution_status={package.get('confirmationExecutionStatus')}")
    print(f"committee_execution_status={package.get('committeeExecutionStatus')}")
    print(f"reviewer_roles={len(roles)}")
    print(f"confirmation_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
