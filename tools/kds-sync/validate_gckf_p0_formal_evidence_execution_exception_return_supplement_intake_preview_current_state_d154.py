#!/usr/bin/env python3
"""Validate D154 GCKF P0 formal evidence execution exception return supplement intake preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-exception-return-supplement-intake-preview-current-state-d154-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-exception-return-supplement-intake-preview-current-state-d154-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-exception-return-supplement-intake-preview-current-state-d154-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D154-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_exception_return_supplement_intake_preview_current_state_d154=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d154_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_supplement = load_json(ROOT / fixture["sourceHistoricalExceptionReturnSupplementIntakePreview"])
    current_return = load_json(ROOT / fixture["sourceCurrentCommitteeCaseOpeningExceptionReturnPreview"])
    supplement = fixture["exceptionReturnSupplementIntakePreview"]
    source_supplement = historical_supplement["exceptionReturnSupplementIntakePreview"]
    return_preview = current_return["committeeCaseOpeningExceptionReturnPreview"]

    require(fixture.get("exceptionReturnSupplementIntakePreviewStatus") == expected["exceptionReturnSupplementIntakePreviewStatus"], "exception_return_supplement_intake_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalSupplementIntake") is expected["notFinalSupplementIntake"], "not_final_supplement_intake_mismatch")
    require(supplement.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(supplement.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(supplement.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(supplement.get("supplementIntakeExecutionStatus") == expected["supplementIntakeExecutionStatus"], "supplement_intake_execution_status_mismatch")
    require(supplement.get("intakeAcceptanceExecutionStatus") == expected["intakeAcceptanceExecutionStatus"], "intake_acceptance_execution_status_mismatch")
    require(supplement.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(supplement.get("committeeDocketExecutionStatus") == expected["committeeDocketExecutionStatus"], "committee_docket_execution_status_mismatch")
    require(supplement.get("committeeReceiptExecutionStatus") == expected["committeeReceiptExecutionStatus"], "committee_receipt_execution_status_mismatch")
    require(supplement.get("committeeRoutingExecutionStatus") == expected["committeeRoutingExecutionStatus"], "committee_routing_execution_status_mismatch")
    require(supplement.get("committeeExceptionReturnExecutionStatus") == expected["committeeExceptionReturnExecutionStatus"], "committee_exception_return_execution_status_mismatch")
    require(supplement.get("committeeReentryExecutionStatus") == expected["committeeReentryExecutionStatus"], "committee_reentry_execution_status_mismatch")
    require(supplement.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(supplement.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(supplement.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(supplement.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(supplement.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(supplement.get("executionMode") == expected["executionMode"], "supplement_execution_mode_mismatch")
    require(supplement.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(supplement.get("sourceCommitteeCaseOpeningExceptionReturnPreviewId") == return_preview.get("id"), "source_committee_case_opening_exception_return_preview_id_mismatch")

    require(historical_supplement.get("exceptionReturnSupplementIntakePreviewStatus") == "candidate_preview", "historical_exception_return_supplement_intake_preview_status_mismatch")
    require(source_supplement.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_supplement.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_return.get("committeeCaseOpeningExceptionReturnPreviewStatus") == expected["sourceCommitteeCaseOpeningExceptionReturnPreviewStatus"], "source_committee_case_opening_exception_return_preview_status_mismatch")
    require(return_preview.get("intakeAcceptanceExecutionStatus") == expected["sourceIntakeAcceptanceExecutionStatus"], "source_intake_acceptance_execution_status_mismatch")
    require(return_preview.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(return_preview.get("committeeDocketExecutionStatus") == expected["sourceCommitteeDocketExecutionStatus"], "source_committee_docket_execution_status_mismatch")
    require(return_preview.get("committeeReceiptExecutionStatus") == expected["sourceCommitteeReceiptExecutionStatus"], "source_committee_receipt_execution_status_mismatch")
    require(return_preview.get("committeeRoutingExecutionStatus") == expected["sourceCommitteeRoutingExecutionStatus"], "source_committee_routing_execution_status_mismatch")
    require(return_preview.get("committeeExceptionReturnExecutionStatus") == expected["sourceCommitteeExceptionReturnExecutionStatus"], "source_committee_exception_return_execution_status_mismatch")
    require(return_preview.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(return_preview.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(return_preview.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(return_preview.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeCaseOpeningExceptionReturnPreviewStatus") == expected["coveredCommitteeCaseOpeningExceptionReturnPreviewStatus"], "covered_committee_case_opening_exception_return_preview_status_mismatch")
    require(fixture["coveredCommitteeCaseOpeningExceptionReturnPreviewStatus"] == return_preview.get("previewStatus"), "covered_committee_case_opening_exception_return_preview_not_matched")

    roles = set(supplement.get("supplementIntakeRoles", []))
    require(len(roles) == expected["supplementIntakeRoleCount"], "supplement_intake_role_count_mismatch")
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
        "supplement_intake_role",
    )
    require(roles == set(return_preview.get("returnRoles", [])), "supplement_intake_roles_not_matched_to_return_roles")

    sections = set(supplement.get("supplementIntakeSections", []))
    require(len(sections) == expected["supplementIntakeSectionCount"], "supplement_intake_section_count_mismatch")
    require_all(
        sections,
        {
            "source_exception_return_lineage",
            "supplement_intake_scope",
            "supplement_envelope_fields",
            "supplement_readiness_prerequisites",
            "supplement_material_candidates",
            "supplement_owner_candidates",
            "supplement_gap_resolution_candidates",
            "candidate_reentry_queue_path",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "supplement_intake_section",
    )

    envelope_fields = set(supplement.get("supplementEnvelopeFields", []))
    require(len(envelope_fields) == expected["supplementEnvelopeFieldCount"], "supplement_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "supplement_intake_preview_id",
            "source_exception_return_preview_id",
            "candidate_supplement_material_ref",
            "candidate_supplement_owner_role",
            "candidate_gap_resolution_ref",
            "candidate_reentry_queue_ref",
            "candidate_supplement_status",
            "no_write_attestation_ref",
        },
        "supplement_envelope_field",
    )

    prerequisites = set(supplement.get("supplementReadinessPrerequisites", []))
    require(len(prerequisites) == expected["supplementReadinessPrerequisiteCount"], "supplement_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_exception_return_candidate_preview_with_hold",
            "source_exception_return_not_formal_return",
            "source_routing_not_formal_routing",
            "source_receipt_not_formal_receipt",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "source_confirmation_not_executed",
            "supplement_intake_not_formal_evidence",
        },
        "supplement_readiness_prerequisite",
    )

    decision_constraints = set(supplement.get("supplementDecisionConstraints", []))
    require(len(decision_constraints) == expected["supplementDecisionConstraintCount"], "supplement_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "supplement_intake_preview_not_formal_intake",
            "no_supplement_acceptance",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_harness_evidence_write",
        },
        "supplement_decision_constraint",
    )

    checks = set(supplement.get("supplementChecks", []))
    require(len(checks) == expected["supplementCheckCount"], "supplement_check_count_mismatch")
    require_all(
        checks,
        {
            "source_exception_return_preview_status_is_candidate_preview_with_hold",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_docket_execution_status_is_not_executed",
            "source_committee_receipt_execution_status_is_not_executed",
            "source_committee_routing_execution_status_is_not_executed",
            "source_committee_exception_return_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_exception_return_preview_is_dry_run_only",
            "exception_return_supplement_intake_preview_status_is_candidate_preview_with_hold",
            "all_supplement_intake_roles_covered",
            "all_supplement_intake_sections_covered",
            "all_supplement_envelope_fields_covered",
            "all_supplement_readiness_prerequisites_covered",
            "all_supplement_decision_constraints_covered",
            "supplement_material_candidates_present",
            "supplement_owner_candidates_present",
            "supplement_gap_resolution_candidates_present",
            "candidate_reentry_queue_path_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_supplement_intake_preview_not_formal_intake",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "supplement_check",
    )

    refs = set(supplement.get("requiredSupplementRefs", []))
    require(len(refs) == expected["requiredSupplementRefCount"], "required_supplement_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseOpeningExceptionReturnPreviewRef",
            "sourceCommitteeReceiptAcknowledgementRoutingPreviewRef",
            "supplementIntakeScopeRef",
            "supplementEnvelopeFieldsRef",
            "supplementReadinessPrerequisitesRef",
            "supplementMaterialCandidatesRef",
            "supplementOwnerCandidatesRef",
            "supplementGapResolutionCandidatesRef",
            "candidateReentryQueuePathRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
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
        "required_supplement_ref",
    )

    blocking_conditions = set(supplement.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_exception_return_preview_not_candidate_preview_with_hold",
            "source_exception_return_already_executed",
            "source_routing_already_executed",
            "source_receipt_already_recorded",
            "source_intake_acceptance_already_executed",
            "source_committee_packet_already_submitted",
            "source_committee_docket_already_created",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_exception_return_preview_not_dry_run_only",
            "missing_source_exception_return_preview_ref",
            "missing_supplement_intake_scope_ref",
            "missing_supplement_envelope_fields_ref",
            "missing_supplement_material_candidates_ref",
            "missing_supplement_owner_candidates_ref",
            "missing_supplement_gap_resolution_candidates_ref",
            "missing_candidate_reentry_queue_path_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_supplement_intake_role",
            "missing_hold_context_refs",
            "supplement_intake_preview_attempts_formal_intake",
            "supplement_intake_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(supplement.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_supplement_intake",
            "accept_supplement_material",
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "create_committee_docket",
            "record_committee_receipt",
            "execute_committee_routing",
            "execute_committee_exception_return",
            "execute_committee_reentry",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "record_intake_acceptance",
            "record_committee_docket",
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
            "convert_supplement_intake_preview_to_formal_intake",
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
    source_hold_refs = set(current_return.get("holdContextRefs", []))
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

    require(evidence.get("current_exception_return_supplement_intake_preview_status") == "candidate_preview_with_hold", "evidence_exception_return_supplement_intake_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("supplement_intake_roles") == 8, "evidence_supplement_intake_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_case_opening_exception_return_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_case_opening_exception_return_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_exception_return_supplement_intake_preview_current_state_d154=pass")
    print(f"exception_return_supplement_intake_preview_status={fixture.get('exceptionReturnSupplementIntakePreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={supplement.get('previewStatus')}")
    print(f"execution_status={supplement.get('executionStatus')}")
    print(f"supplement_intake_execution_status={supplement.get('supplementIntakeExecutionStatus')}")
    print(f"intake_acceptance_execution_status={supplement.get('intakeAcceptanceExecutionStatus')}")
    print(f"committee_submission_execution_status={supplement.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_docket_execution_status={supplement.get('committeeDocketExecutionStatus')}")
    print(f"committee_receipt_execution_status={supplement.get('committeeReceiptExecutionStatus')}")
    print(f"committee_routing_execution_status={supplement.get('committeeRoutingExecutionStatus')}")
    print(f"committee_exception_return_execution_status={supplement.get('committeeExceptionReturnExecutionStatus')}")
    print(f"committee_reentry_execution_status={supplement.get('committeeReentryExecutionStatus')}")
    print(f"committee_case_execution_status={supplement.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={supplement.get('committeeDecisionExecutionStatus')}")
    print(f"supplement_intake_roles={len(roles)}")
    print(f"supplement_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
