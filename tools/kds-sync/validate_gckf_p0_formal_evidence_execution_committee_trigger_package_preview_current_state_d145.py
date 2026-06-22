#!/usr/bin/env python3
"""Validate D145 GCKF P0 formal evidence execution committee trigger package preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-trigger-package-preview-current-state-d145-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-trigger-package-preview-current-state-d145-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-trigger-package-preview-current-state-d145-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D145-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_trigger_package_preview_current_state_d145=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d145_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_package = load_json(ROOT / fixture["sourceHistoricalCommitteeTriggerPackagePreview"])
    current_package = load_json(ROOT / fixture["sourceCurrentHumanConfirmationPackagePreview"])
    package = fixture["committeeTriggerPackagePreview"]
    source_package = historical_package["committeeTriggerPackagePreview"]
    human_confirmation_package = current_package["humanConfirmationPackagePreview"]

    require(fixture.get("committeeTriggerPackagePreviewStatus") == expected["committeeTriggerPackagePreviewStatus"], "committee_trigger_package_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(package.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(package.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(package.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(package.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(package.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(package.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(package.get("freezeExecutionStatus") == expected["freezeExecutionStatus"], "freeze_execution_status_mismatch")
    require(package.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(package.get("resendExecutionStatus") == expected["resendExecutionStatus"], "resend_execution_status_mismatch")
    require(package.get("escalationExecutionStatus") == expected["escalationExecutionStatus"], "escalation_execution_status_mismatch")
    require(package.get("approvalExecutionStatus") == expected["approvalExecutionStatus"], "approval_execution_status_mismatch")
    require(package.get("retryExecutionStatus") == expected["retryExecutionStatus"], "retry_execution_status_mismatch")
    require(package.get("executionMode") == expected["executionMode"], "package_execution_mode_mismatch")
    require(package.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(package.get("sourceHumanConfirmationPackagePreviewId") == human_confirmation_package.get("id"), "source_human_confirmation_package_preview_id_mismatch")

    require(historical_package.get("committeeTriggerPackagePreviewStatus") == "candidate_preview", "historical_committee_trigger_package_preview_status_mismatch")
    require(source_package.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_package.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_package.get("humanConfirmationPackagePreviewStatus") == expected["sourceHumanConfirmationPackagePreviewStatus"], "source_human_confirmation_package_preview_status_mismatch")
    require(human_confirmation_package.get("executionStatus") == expected["sourceHumanConfirmationExecutionStatus"], "source_human_confirmation_execution_status_mismatch")
    require(human_confirmation_package.get("committeeExecutionStatus") == expected["sourceCommitteeExecutionStatus"], "source_committee_execution_status_mismatch")
    require(human_confirmation_package.get("resendExecutionStatus") == expected["sourceResendExecutionStatus"], "source_resend_execution_status_mismatch")
    require(human_confirmation_package.get("escalationExecutionStatus") == expected["sourceEscalationExecutionStatus"], "source_escalation_execution_status_mismatch")
    require(human_confirmation_package.get("approvalExecutionStatus") == expected["sourceApprovalExecutionStatus"], "source_approval_execution_status_mismatch")
    require(human_confirmation_package.get("retryExecutionStatus") == expected["sourceRetryExecutionStatus"], "source_retry_execution_status_mismatch")
    require(human_confirmation_package.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredHumanConfirmationPackagePreviewStatus") == expected["coveredHumanConfirmationPackagePreviewStatus"], "covered_human_confirmation_package_preview_status_mismatch")
    require(fixture["coveredHumanConfirmationPackagePreviewStatus"] == human_confirmation_package.get("previewStatus"), "covered_human_confirmation_package_preview_not_matched")

    roles = set(package.get("committeeRoutingRoles", []))
    require(len(roles) == expected["committeeRoutingRoleCount"], "committee_routing_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner",
        },
        "committee_routing_role",
    )

    case_types = set(package.get("committeeCaseTypes", []))
    require(len(case_types) == expected["committeeCaseTypeCount"], "committee_case_type_count_mismatch")
    require_all(
        case_types,
        {
            "cross_unit_responsibility_dispute",
            "freeze_release_dispute",
            "formal_write_risk",
            "revenue_or_contribution_impact",
            "major_violation_suspected",
        },
        "committee_case_type",
    )
    require(case_types == set(human_confirmation_package.get("committeeTriggers", [])), "committee_case_types_not_matched_to_committee_triggers")

    sections = set(package.get("packageSections", []))
    require(len(sections) == expected["packageSectionCount"], "package_section_count_mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "human_confirmation_summary",
            "committee_trigger_summary",
            "dispute_boundary",
            "freeze_retention_boundary",
            "responsibility_boundary",
            "revenue_contribution_impact",
            "formal_write_risk_summary",
            "harness_review_input",
            "required_evidence_refs",
            "negative_gate_result",
            "no_write_attestation",
        },
        "package_section",
    )

    checks = set(package.get("triggerChecks", []))
    require(len(checks) == expected["triggerCheckCount"], "trigger_check_count_mismatch")
    require_all(
        checks,
        {
            "source_human_confirmation_package_preview_status_is_candidate_preview_with_hold",
            "source_human_confirmation_execution_status_is_not_executed",
            "source_committee_execution_status_is_not_executed",
            "source_resend_execution_status_is_not_executed",
            "source_escalation_execution_status_is_not_executed",
            "source_approval_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_human_confirmation_package_is_dry_run_only",
            "committee_trigger_package_preview_status_is_candidate_preview_with_hold",
            "all_committee_routing_roles_covered",
            "all_committee_case_types_covered",
            "source_lineage_section_present",
            "human_confirmation_summary_present",
            "committee_trigger_summary_present",
            "dispute_boundary_present",
            "freeze_retention_boundary_present",
            "responsibility_boundary_present",
            "revenue_contribution_impact_present",
            "formal_write_risk_summary_present",
            "harness_review_input_present",
            "required_evidence_refs_present",
            "negative_gate_result_present",
            "no_write_attestation_present",
            "cross_unit_responsibility_dispute_case_present",
            "freeze_release_dispute_case_present",
            "formal_write_risk_case_present",
            "revenue_or_contribution_impact_case_present",
            "major_violation_suspected_case_present",
            "preview_hold_context_refs",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "trigger_check",
    )

    refs = set(package.get("requiredTriggerRefs", []))
    require(len(refs) == expected["requiredTriggerRefCount"], "required_trigger_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceHumanConfirmationPackagePreviewRef",
            "sourceEscalationDigestPreviewRef",
            "sourceSignerReceiptPreviewRef",
            "sourceApprovalPacketPreviewRef",
            "humanConfirmationSummaryRef",
            "committeeTriggerSummaryRef",
            "disputeBoundaryRef",
            "freezeRetentionBoundaryRef",
            "responsibilityBoundaryRef",
            "revenueContributionImpactRef",
            "formalWriteRiskSummaryRef",
            "harnessReviewInputRef",
            "requiredEvidenceRefs",
            "requestOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
            "holdContextRefs",
        },
        "required_trigger_ref",
    )

    blocking_conditions = set(package.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_human_confirmation_package_not_candidate_preview_with_hold",
            "source_human_confirmation_already_executed",
            "source_committee_already_executed",
            "source_resend_already_executed",
            "source_escalation_already_executed",
            "source_approval_already_executed",
            "source_retry_already_executed",
            "source_unfreeze_already_executed",
            "source_human_confirmation_package_not_dry_run_only",
            "missing_source_human_confirmation_package_ref",
            "missing_human_confirmation_summary_ref",
            "missing_committee_trigger_summary_ref",
            "missing_dispute_boundary_ref",
            "missing_freeze_retention_boundary_ref",
            "missing_responsibility_boundary_ref",
            "missing_revenue_contribution_impact_ref",
            "missing_formal_write_risk_summary_ref",
            "missing_harness_review_input_ref",
            "missing_required_evidence_refs",
            "missing_committee_routing_role",
            "missing_negative_gate_result_ref",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "committee_trigger_package_attempts_case_opening",
            "committee_trigger_package_attempts_committee_decision",
            "committee_trigger_package_attempts_human_confirmation",
            "committee_trigger_package_attempts_freeze_release",
            "committee_trigger_package_attempts_unfreeze",
            "committee_trigger_package_attempts_approval",
            "committee_trigger_package_attempts_formal_write",
            "committee_trigger_package_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(package.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "execute_resend_dispatch",
            "execute_escalation",
            "execute_approval",
            "execute_retry",
            "execute_formal_write",
            "send_notification",
            "record_committee_case",
            "record_committee_result",
            "record_confirmation_result",
            "record_freeze_release",
            "write_harness_evidence",
            "write_formal_evidence",
            "write_kds",
            "write_business_system",
            "write_revenue_distribution",
            "write_contribution_score",
            "promote_lifecycle",
            "mark_p0_accepted",
            "convert_committee_trigger_preview_to_case",
            "convert_committee_trigger_preview_to_decision",
            "override_waes_gate",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    forbidden_outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(forbidden_outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_package.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_trigger_package_preview_status") == "candidate_preview_with_hold", "evidence_committee_trigger_package_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("committee_routing_roles") == 8, "evidence_committee_routing_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_human_confirmation_package_preview_status") == "candidate_preview_with_hold", "evidence_source_human_confirmation_package_preview_status_mismatch")

    d46_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_committee_trigger_package_preview_dry_run.py")
    require(d46_output.startswith("gckf_p0_formal_evidence_execution_committee_trigger_package_preview_dry_run=pass"), "d46_validator_not_pass")

    d144_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_current_state_d144.py")
    require(d144_output.startswith("gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_current_state_d144=pass"), "d144_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_trigger_package_preview_current_state_d145=pass")
    print(f"committee_trigger_package_preview_status={fixture.get('committeeTriggerPackagePreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={package.get('previewStatus')}")
    print(f"execution_status={package.get('executionStatus')}")
    print(f"committee_case_execution_status={package.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={package.get('committeeDecisionExecutionStatus')}")
    print(f"committee_routing_roles={len(roles)}")
    print(f"trigger_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
