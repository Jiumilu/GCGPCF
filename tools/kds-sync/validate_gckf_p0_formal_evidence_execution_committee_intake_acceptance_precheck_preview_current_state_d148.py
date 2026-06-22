#!/usr/bin/env python3
"""Validate D148 GCKF P0 formal evidence execution committee intake acceptance precheck preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-intake-acceptance-precheck-preview-current-state-d148-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-intake-acceptance-precheck-preview-current-state-d148-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-intake-acceptance-precheck-preview-current-state-d148-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D148-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_intake_acceptance_precheck_preview_current_state_d148=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d148_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_precheck = load_json(ROOT / fixture["sourceHistoricalCommitteeIntakeAcceptancePrecheckPreview"])
    current_packet = load_json(ROOT / fixture["sourceCurrentCommitteeCaseReviewPacketPreview"])
    precheck = fixture["committeeIntakeAcceptancePrecheckPreview"]
    source_precheck = historical_precheck["committeeIntakeAcceptancePrecheckPreview"]
    packet = current_packet["committeeCaseReviewPacketPreview"]

    require(fixture.get("committeeIntakeAcceptancePrecheckPreviewStatus") == expected["committeeIntakeAcceptancePrecheckPreviewStatus"], "committee_intake_acceptance_precheck_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(precheck.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(precheck.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(precheck.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(precheck.get("intakeAcceptanceExecutionStatus") == expected["intakeAcceptanceExecutionStatus"], "intake_acceptance_execution_status_mismatch")
    require(precheck.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(precheck.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(precheck.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(precheck.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(precheck.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(precheck.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(precheck.get("executionMode") == expected["executionMode"], "precheck_execution_mode_mismatch")
    require(precheck.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(precheck.get("sourceCommitteeCaseReviewPacketPreviewId") == packet.get("id"), "source_committee_case_review_packet_preview_id_mismatch")

    require(historical_precheck.get("committeeIntakeAcceptancePrecheckPreviewStatus") == "candidate_preview", "historical_committee_intake_acceptance_precheck_preview_status_mismatch")
    require(source_precheck.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_precheck.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_packet.get("committeeCaseReviewPacketPreviewStatus") == expected["sourceCommitteeCaseReviewPacketPreviewStatus"], "source_committee_case_review_packet_preview_status_mismatch")
    require(packet.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(packet.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(packet.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(packet.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(packet.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeCaseReviewPacketPreviewStatus") == expected["coveredCommitteeCaseReviewPacketPreviewStatus"], "covered_committee_case_review_packet_preview_status_mismatch")
    require(fixture["coveredCommitteeCaseReviewPacketPreviewStatus"] == packet.get("previewStatus"), "covered_committee_case_review_packet_preview_not_matched")

    roles = set(precheck.get("precheckRoles", []))
    require(len(roles) == expected["precheckRoleCount"], "precheck_role_count_mismatch")
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
        "precheck_role",
    )
    require(roles == set(packet.get("casePacketRoles", [])), "precheck_roles_not_matched_to_case_packet_roles")

    sections = set(precheck.get("precheckSections", []))
    require(len(sections) == expected["precheckSectionCount"], "precheck_section_count_mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "case_packet_summary",
            "intake_acceptance_criteria",
            "routing_readiness",
            "evidence_completeness",
            "case_scope_boundary",
            "freeze_retention_statement",
            "decision_constraint_snapshot",
            "waes_negative_gate_snapshot",
            "harness_review_readiness",
            "exception_return_path",
            "no_write_attestation",
        },
        "precheck_section",
    )

    acceptance_criteria = set(precheck.get("acceptanceCriteria", []))
    require(len(acceptance_criteria) == expected["acceptanceCriteriaCount"], "acceptance_criteria_count_mismatch")
    require_all(
        acceptance_criteria,
        {
            "source_case_packet_candidate_preview",
            "evidence_bundle_index_present",
            "case_type_matrix_present",
            "reviewer_question_matrix_present",
            "responsibility_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "no_write_attestation_present",
        },
        "acceptance_criteria",
    )

    decision_constraints = set(precheck.get("precheckDecisionConstraints", []))
    require(len(decision_constraints) == expected["precheckDecisionConstraintCount"], "precheck_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "precheck_not_acceptance",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "precheck_decision_constraint",
    )

    checks = set(precheck.get("precheckChecks", []))
    require(len(checks) == expected["precheckCheckCount"], "precheck_check_count_mismatch")
    require_all(
        checks,
        {
            "source_committee_case_review_packet_preview_status_is_candidate_preview_with_hold",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_case_review_packet_is_dry_run_only",
            "committee_intake_acceptance_precheck_preview_status_is_candidate_preview_with_hold",
            "all_precheck_roles_covered",
            "all_precheck_sections_covered",
            "all_acceptance_criteria_covered",
            "all_precheck_decision_constraints_covered",
            "source_lineage_section_present",
            "case_packet_summary_present",
            "intake_acceptance_criteria_present",
            "routing_readiness_present",
            "evidence_completeness_present",
            "case_scope_boundary_present",
            "freeze_retention_statement_present",
            "decision_constraint_snapshot_present",
            "waes_negative_gate_snapshot_present",
            "harness_review_readiness_present",
            "exception_return_path_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_precheck_not_acceptance",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "precheck_check",
    )

    refs = set(precheck.get("requiredPrecheckRefs", []))
    require(len(refs) == expected["requiredPrecheckRefCount"], "required_precheck_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseReviewPacketPreviewRef",
            "sourceCommitteeReviewInputPreviewRef",
            "sourceCommitteeTriggerPackagePreviewRef",
            "casePacketSummaryRef",
            "intakeAcceptanceCriteriaRef",
            "routingReadinessRef",
            "evidenceCompletenessRef",
            "caseScopeBoundaryRef",
            "freezeRetentionStatementRef",
            "decisionConstraintSnapshotRef",
            "waesNegativeGateSnapshotRef",
            "harnessReviewReadinessRef",
            "exceptionReturnPathRef",
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
        "required_precheck_ref",
    )

    blocking_conditions = set(precheck.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_committee_case_review_packet_not_candidate_preview_with_hold",
            "source_committee_packet_already_submitted",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_case_review_packet_not_dry_run_only",
            "missing_source_committee_case_packet_ref",
            "missing_case_packet_summary_ref",
            "missing_intake_acceptance_criteria_ref",
            "missing_routing_readiness_ref",
            "missing_evidence_completeness_ref",
            "missing_case_scope_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_decision_constraint_snapshot_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_review_readiness_ref",
            "missing_exception_return_path_ref",
            "missing_required_precheck_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "precheck_attempts_intake_acceptance",
            "precheck_attempts_committee_submission",
            "precheck_attempts_case_opening",
            "precheck_attempts_committee_decision",
            "precheck_attempts_formal_write",
            "precheck_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(precheck.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "execute_formal_write",
            "record_intake_acceptance",
            "record_committee_case",
            "record_committee_result",
            "write_harness_evidence",
            "write_formal_evidence",
            "write_kds",
            "write_business_system",
            "write_revenue_distribution",
            "write_contribution_score",
            "promote_lifecycle",
            "mark_p0_accepted",
            "convert_precheck_preview_to_acceptance",
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
    source_hold_refs = set(current_packet.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_intake_acceptance_precheck_preview_status") == "candidate_preview_with_hold", "evidence_committee_intake_acceptance_precheck_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("precheck_roles") == 8, "evidence_precheck_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_case_review_packet_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_case_review_packet_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_intake_acceptance_precheck_preview_current_state_d148=pass")
    print(f"committee_intake_acceptance_precheck_preview_status={fixture.get('committeeIntakeAcceptancePrecheckPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={precheck.get('previewStatus')}")
    print(f"execution_status={precheck.get('executionStatus')}")
    print(f"intake_acceptance_execution_status={precheck.get('intakeAcceptanceExecutionStatus')}")
    print(f"committee_submission_execution_status={precheck.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_case_execution_status={precheck.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={precheck.get('committeeDecisionExecutionStatus')}")
    print(f"precheck_roles={len(roles)}")
    print(f"precheck_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
