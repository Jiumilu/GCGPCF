#!/usr/bin/env python3
"""Validate D156 GCKF P0 formal evidence execution supplement precheck repair request preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-supplement-precheck-repair-request-preview-current-state-d156-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-supplement-precheck-repair-request-preview-current-state-d156-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-supplement-precheck-repair-request-preview-current-state-d156-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D156-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_supplement_precheck_repair_request_preview_current_state_d156=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d156_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_repair = load_json(ROOT / fixture["sourceHistoricalSupplementPrecheckRepairRequestPreview"])
    current_precheck = load_json(ROOT / fixture["sourceCurrentSupplementCompletenessPrecheckPreview"])
    repair_request = fixture["supplementPrecheckRepairRequestPreview"]
    source_repair = historical_repair["supplementPrecheckRepairRequestPreview"]
    precheck = current_precheck["supplementCompletenessPrecheckPreview"]

    require(fixture.get("supplementPrecheckRepairRequestPreviewStatus") == expected["supplementPrecheckRepairRequestPreviewStatus"], "supplement_precheck_repair_request_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalRepairRequest") is expected["notFinalRepairRequest"], "not_final_repair_request_mismatch")
    require(repair_request.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(repair_request.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(repair_request.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(repair_request.get("repairRequestExecutionStatus") == expected["repairRequestExecutionStatus"], "repair_request_execution_status_mismatch")
    require(repair_request.get("completenessPrecheckExecutionStatus") == expected["completenessPrecheckExecutionStatus"], "completeness_precheck_execution_status_mismatch")
    require(repair_request.get("supplementIntakeExecutionStatus") == expected["supplementIntakeExecutionStatus"], "supplement_intake_execution_status_mismatch")
    require(repair_request.get("supplementAcceptanceExecutionStatus") == expected["supplementAcceptanceExecutionStatus"], "supplement_acceptance_execution_status_mismatch")
    require(repair_request.get("committeeReentryExecutionStatus") == expected["committeeReentryExecutionStatus"], "committee_reentry_execution_status_mismatch")
    require(repair_request.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(repair_request.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(repair_request.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(repair_request.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(repair_request.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(repair_request.get("executionMode") == expected["executionMode"], "repair_request_execution_mode_mismatch")
    require(repair_request.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(repair_request.get("sourceSupplementCompletenessPrecheckPreviewId") == precheck.get("id"), "source_supplement_completeness_precheck_preview_id_mismatch")

    require(historical_repair.get("supplementPrecheckRepairRequestPreviewStatus") == "candidate_preview", "historical_repair_request_preview_status_mismatch")
    require(source_repair.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_repair.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_precheck.get("supplementCompletenessPrecheckPreviewStatus") == expected["sourceSupplementCompletenessPrecheckPreviewStatus"], "source_supplement_completeness_precheck_preview_status_mismatch")
    require(precheck.get("completenessPrecheckExecutionStatus") == expected["sourceCompletenessPrecheckExecutionStatus"], "source_completeness_precheck_execution_status_mismatch")
    require(precheck.get("supplementIntakeExecutionStatus") == expected["sourceSupplementIntakeExecutionStatus"], "source_supplement_intake_execution_status_mismatch")
    require(precheck.get("supplementAcceptanceExecutionStatus") == expected["sourceSupplementAcceptanceExecutionStatus"], "source_supplement_acceptance_execution_status_mismatch")
    require(precheck.get("committeeReentryExecutionStatus") == expected["sourceCommitteeReentryExecutionStatus"], "source_committee_reentry_execution_status_mismatch")
    require(precheck.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(precheck.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(precheck.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(precheck.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredSupplementCompletenessPrecheckPreviewStatus") == expected["coveredSupplementCompletenessPrecheckPreviewStatus"], "covered_supplement_completeness_precheck_preview_status_mismatch")
    require(fixture["coveredSupplementCompletenessPrecheckPreviewStatus"] == precheck.get("previewStatus"), "covered_supplement_completeness_precheck_preview_not_matched")

    roles = set(repair_request.get("repairRequestRoles", []))
    require(len(roles) == expected["repairRequestRoleCount"], "repair_request_role_count_mismatch")
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
        "repair_request_role",
    )
    require(roles == set(precheck.get("precheckRoles", [])), "repair_request_roles_not_matched_to_precheck_roles")

    sections = set(repair_request.get("repairRequestSections", []))
    require(len(sections) == expected["repairRequestSectionCount"], "repair_request_section_count_mismatch")
    require_all(
        sections,
        {
            "source_precheck_lineage",
            "repair_request_scope",
            "repair_request_envelope_fields",
            "repair_request_readiness_prerequisites",
            "gap_reference_candidates",
            "repair_reason_candidates",
            "responsible_role_candidates",
            "required_supplement_candidates",
            "candidate_recheck_path",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "repair_request_section",
    )

    envelope_fields = set(repair_request.get("repairRequestEnvelopeFields", []))
    require(len(envelope_fields) == expected["repairRequestEnvelopeFieldCount"], "repair_request_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "repair_request_preview_id",
            "source_precheck_preview_id",
            "candidate_gap_ref",
            "candidate_repair_reason_code",
            "candidate_responsible_role",
            "candidate_required_supplement_ref",
            "candidate_recheck_path_ref",
            "candidate_repair_status",
            "no_write_attestation_ref",
        },
        "repair_request_envelope_field",
    )

    prerequisites = set(repair_request.get("repairRequestReadinessPrerequisites", []))
    require(len(prerequisites) == expected["repairRequestReadinessPrerequisiteCount"], "repair_request_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_precheck_candidate_preview_with_hold",
            "source_precheck_not_formal_completeness_check",
            "source_supplement_material_not_accepted",
            "source_committee_reentry_not_executed",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "source_confirmation_not_executed",
            "repair_request_not_formal_evidence",
        },
        "repair_request_readiness_prerequisite",
    )

    decision_constraints = set(repair_request.get("repairRequestDecisionConstraints", []))
    require(len(decision_constraints) == expected["repairRequestDecisionConstraintCount"], "repair_request_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "repair_request_preview_not_formal_repair_request",
            "no_repair_request_execution",
            "no_supplement_acceptance",
            "no_intake_acceptance",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_harness_evidence_write",
        },
        "repair_request_decision_constraint",
    )

    checks = set(repair_request.get("repairRequestChecks", []))
    require(len(checks) == expected["repairRequestCheckCount"], "repair_request_check_count_mismatch")
    require_all(
        checks,
        {
            "source_precheck_preview_status_is_candidate_preview_with_hold",
            "source_completeness_precheck_execution_status_is_not_executed",
            "source_supplement_intake_execution_status_is_not_executed",
            "source_supplement_acceptance_execution_status_is_not_executed",
            "source_committee_reentry_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_precheck_preview_is_dry_run_only",
            "supplement_precheck_repair_request_preview_status_is_candidate_preview_with_hold",
            "all_repair_request_roles_covered",
            "all_repair_request_sections_covered",
            "all_repair_request_envelope_fields_covered",
            "all_repair_request_readiness_prerequisites_covered",
            "all_repair_request_decision_constraints_covered",
            "gap_reference_candidates_present",
            "repair_reason_candidates_present",
            "responsible_role_candidates_present",
            "required_supplement_candidates_present",
            "candidate_recheck_path_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_repair_request_preview_not_formal_repair_request",
            "assert_repair_request_not_executed",
            "assert_completeness_precheck_not_executed",
            "assert_supplement_intake_not_executed",
            "assert_committee_reentry_not_executed",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "repair_request_check",
    )

    refs = set(repair_request.get("requiredRepairRequestRefs", []))
    require(len(refs) == expected["requiredRepairRequestRefCount"], "required_repair_request_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceSupplementCompletenessPrecheckPreviewRef",
            "sourceExceptionReturnSupplementIntakePreviewRef",
            "repairRequestScopeRef",
            "repairRequestEnvelopeFieldsRef",
            "repairRequestReadinessPrerequisitesRef",
            "gapReferenceCandidatesRef",
            "repairReasonCandidatesRef",
            "responsibleRoleCandidatesRef",
            "requiredSupplementCandidatesRef",
            "candidateRecheckPathRef",
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
        },
        "required_repair_request_ref",
    )

    blocking_conditions = set(repair_request.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_precheck_preview_not_candidate_preview_with_hold",
            "source_completeness_precheck_already_executed",
            "source_supplement_intake_already_executed",
            "source_supplement_material_already_accepted",
            "source_committee_reentry_already_executed",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_precheck_preview_not_dry_run_only",
            "missing_source_precheck_preview_ref",
            "missing_repair_request_scope_ref",
            "missing_repair_request_envelope_fields_ref",
            "missing_gap_reference_candidates_ref",
            "missing_repair_reason_candidates_ref",
            "missing_responsible_role_candidates_ref",
            "missing_required_supplement_candidates_ref",
            "missing_candidate_recheck_path_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_repair_request_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "repair_request_preview_attempts_formal_repair_request",
            "repair_request_preview_attempts_supplement_intake",
            "repair_request_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(repair_request.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_repair_request",
            "execute_completeness_precheck",
            "execute_supplement_intake",
            "accept_supplement_material",
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "execute_committee_reentry",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "record_repair_request",
            "record_completeness_precheck",
            "record_supplement_intake",
            "record_supplement_acceptance",
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
            "convert_repair_request_preview_to_formal_repair_request",
            "override_waes_gate",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    forbidden_outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(forbidden_outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")
    require_all(
        forbidden_outputs,
        {
            "repair_request_executed",
            "completeness_precheck_executed",
            "supplement_intake_executed",
            "supplement_material_accepted",
            "intake_acceptance_executed",
            "committee_case_packet_submitted",
            "committee_review_input_submitted",
            "committee_reentry_executed",
            "committee_case_opened",
            "committee_decision_executed",
            "human_confirmation_executed",
            "freeze_released",
            "unfreeze_executed",
            "formal_write_executed",
            "formal_harness_evidence_record_written",
            "harness_evidence_record_written",
            "kds_write_enabled",
            "business_write_enabled",
            "revenue_distribution_written",
            "contribution_score_written",
            "accepted",
            "integrated",
            "production_ready",
            "waes_gate_overridden",
            "repair_request_preview_converted_to_formal_repair_request",
            "p1_admission_granted",
            "v1_upgrade_approved",
        },
        "forbidden_output",
    )

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_precheck.get("holdContextRefs", []))
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

    require(evidence.get("current_supplement_precheck_repair_request_preview_status") == "candidate_preview_with_hold", "evidence_repair_request_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("repair_request_roles") == 8, "evidence_repair_request_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_supplement_completeness_precheck_preview_status") == "candidate_preview_with_hold", "evidence_source_precheck_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_supplement_precheck_repair_request_preview_current_state_d156=pass")
    print(f"supplement_precheck_repair_request_preview_status={fixture.get('supplementPrecheckRepairRequestPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={repair_request.get('previewStatus')}")
    print(f"execution_status={repair_request.get('executionStatus')}")
    print(f"repair_request_execution_status={repair_request.get('repairRequestExecutionStatus')}")
    print(f"completeness_precheck_execution_status={repair_request.get('completenessPrecheckExecutionStatus')}")
    print(f"supplement_intake_execution_status={repair_request.get('supplementIntakeExecutionStatus')}")
    print(f"supplement_acceptance_execution_status={repair_request.get('supplementAcceptanceExecutionStatus')}")
    print(f"committee_reentry_execution_status={repair_request.get('committeeReentryExecutionStatus')}")
    print(f"committee_case_execution_status={repair_request.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={repair_request.get('committeeDecisionExecutionStatus')}")
    print(f"repair_request_roles={len(roles)}")
    print(f"repair_request_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
