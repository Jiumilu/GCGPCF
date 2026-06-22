#!/usr/bin/env python3
"""Validate D146 GCKF P0 formal evidence execution committee review input preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-review-input-preview-current-state-d146-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-review-input-preview-current-state-d146-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-review-input-preview-current-state-d146-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D146-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_review_input_preview_current_state_d146=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d146_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_review = load_json(ROOT / fixture["sourceHistoricalCommitteeReviewInputPreview"])
    current_trigger = load_json(ROOT / fixture["sourceCurrentCommitteeTriggerPackagePreview"])
    review = fixture["committeeReviewInputPreview"]
    source_review = historical_review["committeeReviewInputPreview"]
    trigger = current_trigger["committeeTriggerPackagePreview"]

    require(fixture.get("committeeReviewInputPreviewStatus") == expected["committeeReviewInputPreviewStatus"], "committee_review_input_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(review.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(review.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(review.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(review.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(review.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(review.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(review.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(review.get("freezeExecutionStatus") == expected["freezeExecutionStatus"], "freeze_execution_status_mismatch")
    require(review.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(review.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(review.get("executionMode") == expected["executionMode"], "review_execution_mode_mismatch")
    require(review.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(review.get("sourceCommitteeTriggerPackagePreviewId") == trigger.get("id"), "source_committee_trigger_package_preview_id_mismatch")

    require(historical_review.get("committeeReviewInputPreviewStatus") == "candidate_preview", "historical_committee_review_input_preview_status_mismatch")
    require(source_review.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_review.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_trigger.get("committeeTriggerPackagePreviewStatus") == expected["sourceCommitteeTriggerPackagePreviewStatus"], "source_committee_trigger_package_preview_status_mismatch")
    require(trigger.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(trigger.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(trigger.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(trigger.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeTriggerPackagePreviewStatus") == expected["coveredCommitteeTriggerPackagePreviewStatus"], "covered_committee_trigger_package_preview_status_mismatch")
    require(fixture["coveredCommitteeTriggerPackagePreviewStatus"] == trigger.get("previewStatus"), "covered_committee_trigger_package_preview_not_matched")

    roles = set(review.get("intakeRoles", []))
    require(len(roles) == expected["intakeRoleCount"], "intake_role_count_mismatch")
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
        "intake_role",
    )
    require(roles == set(trigger.get("committeeRoutingRoles", [])), "intake_roles_not_matched_to_committee_routing_roles")

    sections = set(review.get("reviewInputSections", []))
    require(len(sections) == expected["reviewInputSectionCount"], "review_input_section_count_mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "committee_trigger_summary",
            "case_type_summary",
            "evidence_bundle_refs",
            "dispute_questions",
            "responsibility_questions",
            "freeze_retention_statement",
            "revenue_contribution_impact_questions",
            "formal_write_risk_questions",
            "waes_negative_gate_snapshot",
            "harness_review_constraints",
            "no_write_attestation",
        },
        "review_input_section",
    )

    question_groups = set(review.get("reviewQuestionGroups", []))
    require(len(question_groups) == expected["reviewQuestionGroupCount"], "review_question_group_count_mismatch")
    require_all(
        question_groups,
        {
            "source_and_lineage_questions",
            "evidence_sufficiency_questions",
            "cross_unit_responsibility_questions",
            "freeze_release_questions",
            "formal_write_risk_questions",
            "revenue_contribution_impact_questions",
            "major_violation_questions",
            "decision_constraint_questions",
        },
        "review_question_group",
    )

    decision_constraints = set(review.get("decisionConstraints", []))
    require(len(decision_constraints) == expected["decisionConstraintCount"], "decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "committee_input_not_case",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_revenue_distribution",
            "no_contribution_score",
            "no_harness_evidence_write",
            "waes_gate_not_overridden",
        },
        "decision_constraint",
    )

    checks = set(review.get("reviewChecks", []))
    require(len(checks) == expected["reviewCheckCount"], "review_check_count_mismatch")
    require_all(
        checks,
        {
            "source_committee_trigger_package_preview_status_is_candidate_preview_with_hold",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_committee_trigger_package_is_dry_run_only",
            "committee_review_input_preview_status_is_candidate_preview_with_hold",
            "all_intake_roles_covered",
            "all_review_input_sections_covered",
            "all_review_question_groups_covered",
            "all_decision_constraints_covered",
            "source_lineage_section_present",
            "committee_trigger_summary_present",
            "case_type_summary_present",
            "evidence_bundle_refs_present",
            "dispute_questions_present",
            "responsibility_questions_present",
            "freeze_retention_statement_present",
            "revenue_contribution_impact_questions_present",
            "formal_write_risk_questions_present",
            "waes_negative_gate_snapshot_present",
            "harness_review_constraints_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_committee_input_not_submitted",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "review_check",
    )

    refs = set(review.get("requiredReviewRefs", []))
    require(len(refs) == expected["requiredReviewRefCount"], "required_review_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeTriggerPackagePreviewRef",
            "sourceHumanConfirmationPackagePreviewRef",
            "sourceEscalationDigestPreviewRef",
            "committeeTriggerSummaryRef",
            "caseTypeSummaryRef",
            "evidenceBundleRefs",
            "disputeQuestionRefs",
            "responsibilityQuestionRefs",
            "freezeRetentionStatementRef",
            "revenueContributionImpactQuestionRefs",
            "formalWriteRiskQuestionRefs",
            "waesNegativeGateSnapshotRef",
            "harnessReviewConstraintRefs",
            "requestOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
            "holdContextRefs",
        },
        "required_review_ref",
    )

    blocking_conditions = set(review.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_committee_trigger_package_not_candidate_preview_with_hold",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_committee_trigger_package_not_dry_run_only",
            "missing_source_committee_trigger_package_ref",
            "missing_committee_trigger_summary_ref",
            "missing_case_type_summary_ref",
            "missing_evidence_bundle_refs",
            "missing_dispute_question_refs",
            "missing_responsibility_question_refs",
            "missing_freeze_retention_statement_ref",
            "missing_revenue_contribution_impact_question_refs",
            "missing_formal_write_risk_question_refs",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_review_constraint_refs",
            "missing_required_intake_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "committee_review_input_attempts_submission",
            "committee_review_input_attempts_case_opening",
            "committee_review_input_attempts_committee_decision",
            "committee_review_input_attempts_human_confirmation",
            "committee_review_input_attempts_freeze_release",
            "committee_review_input_attempts_formal_write",
            "committee_review_input_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(review.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "submit_committee_review_input",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "execute_formal_write",
            "record_committee_input",
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
            "convert_committee_review_input_preview_to_submission",
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
    source_hold_refs = set(current_trigger.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_review_input_preview_status") == "candidate_preview_with_hold", "evidence_committee_review_input_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("intake_roles") == 8, "evidence_intake_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_trigger_package_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_trigger_package_preview_status_mismatch")

    d47_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_committee_review_input_preview_dry_run.py")
    require(d47_output.startswith("gckf_p0_formal_evidence_execution_committee_review_input_preview_dry_run=pass"), "d47_validator_not_pass")

    d145_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_committee_trigger_package_preview_current_state_d145.py")
    require(d145_output.startswith("gckf_p0_formal_evidence_execution_committee_trigger_package_preview_current_state_d145=pass"), "d145_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_review_input_preview_current_state_d146=pass")
    print(f"committee_review_input_preview_status={fixture.get('committeeReviewInputPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={review.get('previewStatus')}")
    print(f"execution_status={review.get('executionStatus')}")
    print(f"committee_submission_execution_status={review.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_case_execution_status={review.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={review.get('committeeDecisionExecutionStatus')}")
    print(f"intake_roles={len(roles)}")
    print(f"review_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
