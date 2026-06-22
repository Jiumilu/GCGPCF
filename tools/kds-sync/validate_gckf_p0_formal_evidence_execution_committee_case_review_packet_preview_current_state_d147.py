#!/usr/bin/env python3
"""Validate D147 GCKF P0 formal evidence execution committee case review packet preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-case-review-packet-preview-current-state-d147-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-case-review-packet-preview-current-state-d147-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-case-review-packet-preview-current-state-d147-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D147-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_case_review_packet_preview_current_state_d147=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d147_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_packet = load_json(ROOT / fixture["sourceHistoricalCommitteeCaseReviewPacketPreview"])
    current_review_input = load_json(ROOT / fixture["sourceCurrentCommitteeReviewInputPreview"])
    packet = fixture["committeeCaseReviewPacketPreview"]
    source_packet = historical_packet["committeeCaseReviewPacketPreview"]
    review_input = current_review_input["committeeReviewInputPreview"]

    require(fixture.get("committeeCaseReviewPacketPreviewStatus") == expected["committeeCaseReviewPacketPreviewStatus"], "committee_case_review_packet_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(packet.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(packet.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(packet.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(packet.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(packet.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(packet.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(packet.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(packet.get("freezeExecutionStatus") == expected["freezeExecutionStatus"], "freeze_execution_status_mismatch")
    require(packet.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(packet.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(packet.get("executionMode") == expected["executionMode"], "packet_execution_mode_mismatch")
    require(packet.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(packet.get("sourceCommitteeReviewInputPreviewId") == review_input.get("id"), "source_committee_review_input_preview_id_mismatch")

    require(historical_packet.get("committeeCaseReviewPacketPreviewStatus") == "candidate_preview", "historical_committee_case_review_packet_preview_status_mismatch")
    require(source_packet.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_packet.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_review_input.get("committeeReviewInputPreviewStatus") == expected["sourceCommitteeReviewInputPreviewStatus"], "source_committee_review_input_preview_status_mismatch")
    require(review_input.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(review_input.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(review_input.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(review_input.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(review_input.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeReviewInputPreviewStatus") == expected["coveredCommitteeReviewInputPreviewStatus"], "covered_committee_review_input_preview_status_mismatch")
    require(fixture["coveredCommitteeReviewInputPreviewStatus"] == review_input.get("previewStatus"), "covered_committee_review_input_preview_not_matched")

    roles = set(packet.get("casePacketRoles", []))
    require(len(roles) == expected["casePacketRoleCount"], "case_packet_role_count_mismatch")
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
        "case_packet_role",
    )
    require(roles == set(review_input.get("intakeRoles", [])), "case_packet_roles_not_matched_to_review_input_roles")

    sections = set(packet.get("casePacketSections", []))
    require(len(sections) == expected["casePacketSectionCount"], "case_packet_section_count_mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "committee_review_input_summary",
            "case_scope_summary",
            "case_type_matrix",
            "evidence_bundle_index",
            "reviewer_question_matrix",
            "responsibility_boundary",
            "freeze_retention_statement",
            "revenue_contribution_impact_summary",
            "formal_write_risk_summary",
            "waes_negative_gate_snapshot",
            "no_write_attestation",
        },
        "case_packet_section",
    )

    question_groups = set(packet.get("casePacketQuestionGroups", []))
    require(len(question_groups) == expected["casePacketQuestionGroupCount"], "case_packet_question_group_count_mismatch")
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
        "case_packet_question_group",
    )

    decision_constraints = set(packet.get("casePacketDecisionConstraints", []))
    require(len(decision_constraints) == expected["casePacketDecisionConstraintCount"], "case_packet_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "case_packet_not_case",
            "no_committee_submission",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_revenue_distribution",
            "no_contribution_score",
            "no_harness_evidence_write",
        },
        "case_packet_decision_constraint",
    )

    checks = set(packet.get("casePacketChecks", []))
    require(len(checks) == expected["casePacketCheckCount"], "case_packet_check_count_mismatch")
    require_all(
        checks,
        {
            "source_committee_review_input_preview_status_is_candidate_preview_with_hold",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_committee_review_input_is_dry_run_only",
            "committee_case_review_packet_preview_status_is_candidate_preview_with_hold",
            "all_case_packet_roles_covered",
            "all_case_packet_sections_covered",
            "all_case_packet_question_groups_covered",
            "all_case_packet_decision_constraints_covered",
            "source_lineage_section_present",
            "committee_review_input_summary_present",
            "case_scope_summary_present",
            "case_type_matrix_present",
            "evidence_bundle_index_present",
            "reviewer_question_matrix_present",
            "responsibility_boundary_present",
            "freeze_retention_statement_present",
            "revenue_contribution_impact_summary_present",
            "formal_write_risk_summary_present",
            "waes_negative_gate_snapshot_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_case_packet_not_submitted",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "case_packet_check",
    )

    refs = set(packet.get("requiredCasePacketRefs", []))
    require(len(refs) == expected["requiredCasePacketRefCount"], "required_case_packet_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeReviewInputPreviewRef",
            "sourceCommitteeTriggerPackagePreviewRef",
            "sourceHumanConfirmationPackagePreviewRef",
            "committeeReviewInputSummaryRef",
            "caseScopeSummaryRef",
            "caseTypeMatrixRef",
            "evidenceBundleIndexRef",
            "reviewerQuestionMatrixRef",
            "responsibilityBoundaryRef",
            "freezeRetentionStatementRef",
            "revenueContributionImpactSummaryRef",
            "formalWriteRiskSummaryRef",
            "waesNegativeGateSnapshotRef",
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
        "required_case_packet_ref",
    )

    blocking_conditions = set(packet.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_committee_review_input_not_candidate_preview_with_hold",
            "source_committee_input_already_submitted",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_committee_review_input_not_dry_run_only",
            "missing_source_committee_review_input_ref",
            "missing_committee_review_input_summary_ref",
            "missing_case_scope_summary_ref",
            "missing_case_type_matrix_ref",
            "missing_evidence_bundle_index_ref",
            "missing_reviewer_question_matrix_ref",
            "missing_responsibility_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_revenue_contribution_impact_summary_ref",
            "missing_formal_write_risk_summary_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_required_case_packet_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "case_packet_attempts_submission",
            "case_packet_attempts_case_opening",
            "case_packet_attempts_committee_decision",
            "case_packet_attempts_human_confirmation",
            "case_packet_attempts_formal_write",
            "case_packet_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(packet.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "execute_formal_write",
            "record_committee_case_packet",
            "record_committee_case",
            "record_committee_result",
            "record_confirmation_result",
            "write_harness_evidence",
            "write_formal_evidence",
            "write_kds",
            "write_business_system",
            "write_revenue_distribution",
            "write_contribution_score",
            "promote_lifecycle",
            "mark_p0_accepted",
            "convert_case_packet_preview_to_case",
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
    source_hold_refs = set(current_review_input.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_case_review_packet_preview_status") == "candidate_preview_with_hold", "evidence_committee_case_review_packet_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("case_packet_roles") == 8, "evidence_case_packet_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_review_input_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_review_input_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_case_review_packet_preview_current_state_d147=pass")
    print(f"committee_case_review_packet_preview_status={fixture.get('committeeCaseReviewPacketPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={packet.get('previewStatus')}")
    print(f"execution_status={packet.get('executionStatus')}")
    print(f"committee_submission_execution_status={packet.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_case_execution_status={packet.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={packet.get('committeeDecisionExecutionStatus')}")
    print(f"case_packet_roles={len(roles)}")
    print(f"case_packet_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
