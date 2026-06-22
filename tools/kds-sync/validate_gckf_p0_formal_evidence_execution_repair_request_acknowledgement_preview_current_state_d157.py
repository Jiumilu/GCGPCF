#!/usr/bin/env python3
"""Validate D157 GCKF P0 formal evidence execution repair request acknowledgement preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-repair-request-acknowledgement-preview-current-state-d157-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-repair-request-acknowledgement-preview-current-state-d157-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-repair-request-acknowledgement-preview-current-state-d157-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D157-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_repair_request_acknowledgement_preview_current_state_d157=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d157_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_ack = load_json(ROOT / fixture["sourceHistoricalRepairRequestAcknowledgementPreview"])
    current_repair = load_json(ROOT / fixture["sourceCurrentSupplementPrecheckRepairRequestPreview"])
    acknowledgement = fixture["repairRequestAcknowledgementPreview"]
    source_ack = historical_ack["repairRequestAcknowledgementPreview"]
    repair_request = current_repair["supplementPrecheckRepairRequestPreview"]

    require(fixture.get("repairRequestAcknowledgementPreviewStatus") == expected["repairRequestAcknowledgementPreviewStatus"], "repair_request_acknowledgement_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcknowledgement") is expected["notFinalAcknowledgement"], "not_final_acknowledgement_mismatch")
    require(acknowledgement.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(acknowledgement.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(acknowledgement.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(acknowledgement.get("acknowledgementExecutionStatus") == expected["acknowledgementExecutionStatus"], "acknowledgement_execution_status_mismatch")
    require(acknowledgement.get("repairRequestExecutionStatus") == expected["repairRequestExecutionStatus"], "repair_request_execution_status_mismatch")
    require(acknowledgement.get("supplementIntakeExecutionStatus") == expected["supplementIntakeExecutionStatus"], "supplement_intake_execution_status_mismatch")
    require(acknowledgement.get("supplementAcceptanceExecutionStatus") == expected["supplementAcceptanceExecutionStatus"], "supplement_acceptance_execution_status_mismatch")
    require(acknowledgement.get("committeeReentryExecutionStatus") == expected["committeeReentryExecutionStatus"], "committee_reentry_execution_status_mismatch")
    require(acknowledgement.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(acknowledgement.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(acknowledgement.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(acknowledgement.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(acknowledgement.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(acknowledgement.get("executionMode") == expected["executionMode"], "acknowledgement_execution_mode_mismatch")
    require(acknowledgement.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(acknowledgement.get("sourceSupplementPrecheckRepairRequestPreviewId") == repair_request.get("id"), "source_supplement_precheck_repair_request_preview_id_mismatch")

    require(historical_ack.get("repairRequestAcknowledgementPreviewStatus") == "candidate_preview", "historical_acknowledgement_preview_status_mismatch")
    require(source_ack.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_ack.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_repair.get("supplementPrecheckRepairRequestPreviewStatus") == expected["sourceSupplementPrecheckRepairRequestPreviewStatus"], "source_repair_request_preview_status_mismatch")
    require(repair_request.get("repairRequestExecutionStatus") == expected["sourceRepairRequestExecutionStatus"], "source_repair_request_execution_status_mismatch")
    require(repair_request.get("completenessPrecheckExecutionStatus") == expected["sourceCompletenessPrecheckExecutionStatus"], "source_completeness_precheck_execution_status_mismatch")
    require(repair_request.get("supplementIntakeExecutionStatus") == expected["sourceSupplementIntakeExecutionStatus"], "source_supplement_intake_execution_status_mismatch")
    require(repair_request.get("supplementAcceptanceExecutionStatus") == expected["sourceSupplementAcceptanceExecutionStatus"], "source_supplement_acceptance_execution_status_mismatch")
    require(repair_request.get("committeeReentryExecutionStatus") == expected["sourceCommitteeReentryExecutionStatus"], "source_committee_reentry_execution_status_mismatch")
    require(repair_request.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(repair_request.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(repair_request.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(repair_request.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredSupplementPrecheckRepairRequestPreviewStatus") == expected["coveredSupplementPrecheckRepairRequestPreviewStatus"], "covered_supplement_precheck_repair_request_preview_status_mismatch")
    require(fixture["coveredSupplementPrecheckRepairRequestPreviewStatus"] == repair_request.get("previewStatus"), "covered_supplement_precheck_repair_request_preview_not_matched")

    roles = set(acknowledgement.get("acknowledgementRoles", []))
    require(len(roles) == expected["acknowledgementRoleCount"], "acknowledgement_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "acknowledgement_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner",
        },
        "acknowledgement_role",
    )
    require(set(repair_request.get("repairRequestRoles", [])).issubset(roles), "acknowledgement_roles_not_covering_repair_request_roles")

    sections = set(acknowledgement.get("acknowledgementSections", []))
    require(len(sections) == expected["acknowledgementSectionCount"], "acknowledgement_section_count_mismatch")
    require_all(
        sections,
        {
            "source_repair_request_lineage",
            "acknowledgement_scope",
            "acknowledgement_envelope_fields",
            "acknowledgement_readiness_prerequisites",
            "receipt_identifier_candidates",
            "acknowledgement_channel_candidates",
            "recipient_role_candidates",
            "response_due_window_candidates",
            "candidate_follow_up_path",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "acknowledgement_section",
    )

    envelope_fields = set(acknowledgement.get("acknowledgementEnvelopeFields", []))
    require(len(envelope_fields) == expected["acknowledgementEnvelopeFieldCount"], "acknowledgement_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "acknowledgement_preview_id",
            "source_repair_request_preview_id",
            "candidate_receipt_ref",
            "candidate_acknowledgement_channel",
            "candidate_recipient_role",
            "candidate_response_due_window",
            "candidate_follow_up_path_ref",
            "candidate_acknowledgement_status",
            "no_write_attestation_ref",
        },
        "acknowledgement_envelope_field",
    )

    prerequisites = set(acknowledgement.get("acknowledgementReadinessPrerequisites", []))
    require(len(prerequisites) == expected["acknowledgementReadinessPrerequisiteCount"], "acknowledgement_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_repair_request_candidate_preview_with_hold",
            "source_repair_request_not_formal_request",
            "source_repair_request_not_executed",
            "source_supplement_material_not_accepted",
            "source_committee_reentry_not_executed",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "acknowledgement_not_formal_evidence",
        },
        "acknowledgement_readiness_prerequisite",
    )

    decision_constraints = set(acknowledgement.get("acknowledgementDecisionConstraints", []))
    require(len(decision_constraints) == expected["acknowledgementDecisionConstraintCount"], "acknowledgement_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "acknowledgement_preview_not_formal_acknowledgement",
            "no_acknowledgement_execution",
            "no_repair_request_execution",
            "no_supplement_acceptance",
            "no_intake_acceptance",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_harness_evidence_write",
        },
        "acknowledgement_decision_constraint",
    )

    checks = set(acknowledgement.get("acknowledgementChecks", []))
    require(len(checks) == expected["acknowledgementCheckCount"], "acknowledgement_check_count_mismatch")
    require_all(
        checks,
        {
            "source_repair_request_preview_status_is_candidate_preview_with_hold",
            "source_repair_request_execution_status_is_not_executed",
            "source_completeness_precheck_execution_status_is_not_executed",
            "source_supplement_intake_execution_status_is_not_executed",
            "source_supplement_acceptance_execution_status_is_not_executed",
            "source_committee_reentry_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_repair_request_preview_is_dry_run_only",
            "repair_request_acknowledgement_preview_status_is_candidate_preview_with_hold",
            "all_acknowledgement_roles_covered",
            "all_acknowledgement_sections_covered",
            "all_acknowledgement_envelope_fields_covered",
            "all_acknowledgement_readiness_prerequisites_covered",
            "all_acknowledgement_decision_constraints_covered",
            "receipt_identifier_candidates_present",
            "acknowledgement_channel_candidates_present",
            "recipient_role_candidates_present",
            "response_due_window_candidates_present",
            "candidate_follow_up_path_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_acknowledgement_preview_not_formal_acknowledgement",
            "assert_acknowledgement_not_executed",
            "assert_repair_request_not_executed",
            "assert_committee_reentry_not_executed",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "acknowledgement_check",
    )

    refs = set(acknowledgement.get("requiredAcknowledgementRefs", []))
    require(len(refs) == expected["requiredAcknowledgementRefCount"], "required_acknowledgement_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceSupplementPrecheckRepairRequestPreviewRef",
            "sourceSupplementCompletenessPrecheckPreviewRef",
            "acknowledgementScopeRef",
            "acknowledgementEnvelopeFieldsRef",
            "acknowledgementReadinessPrerequisitesRef",
            "receiptIdentifierCandidatesRef",
            "acknowledgementChannelCandidatesRef",
            "recipientRoleCandidatesRef",
            "responseDueWindowCandidatesRef",
            "candidateFollowUpPathRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "requestOwnerRef",
            "acknowledgementOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required_acknowledgement_ref",
    )

    blocking_conditions = set(acknowledgement.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_repair_request_preview_not_candidate_preview_with_hold",
            "source_repair_request_already_executed",
            "source_completeness_precheck_already_executed",
            "source_supplement_intake_already_executed",
            "source_supplement_material_already_accepted",
            "source_committee_reentry_already_executed",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_repair_request_preview_not_dry_run_only",
            "missing_source_repair_request_preview_ref",
            "missing_acknowledgement_scope_ref",
            "missing_acknowledgement_envelope_fields_ref",
            "missing_receipt_identifier_candidates_ref",
            "missing_acknowledgement_channel_candidates_ref",
            "missing_recipient_role_candidates_ref",
            "missing_response_due_window_candidates_ref",
            "missing_candidate_follow_up_path_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_acknowledgement_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "acknowledgement_preview_attempts_formal_acknowledgement",
            "acknowledgement_preview_attempts_repair_request_execution",
            "acknowledgement_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(acknowledgement.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_acknowledgement",
            "issue_formal_acknowledgement",
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
            "record_acknowledgement",
            "record_repair_request",
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
            "convert_acknowledgement_preview_to_formal_acknowledgement",
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
            "acknowledgement_executed",
            "formal_acknowledgement_issued",
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
            "acknowledgement_preview_converted_to_formal_acknowledgement",
            "p1_admission_granted",
            "v1_upgrade_approved",
        },
        "forbidden_output",
    )

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_repair.get("holdContextRefs", []))
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

    require(evidence.get("current_repair_request_acknowledgement_preview_status") == "candidate_preview_with_hold", "evidence_acknowledgement_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("acknowledgement_roles") == 9, "evidence_acknowledgement_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_supplement_precheck_repair_request_preview_status") == "candidate_preview_with_hold", "evidence_source_repair_request_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_repair_request_acknowledgement_preview_current_state_d157=pass")
    print(f"repair_request_acknowledgement_preview_status={fixture.get('repairRequestAcknowledgementPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={acknowledgement.get('previewStatus')}")
    print(f"execution_status={acknowledgement.get('executionStatus')}")
    print(f"acknowledgement_execution_status={acknowledgement.get('acknowledgementExecutionStatus')}")
    print(f"repair_request_execution_status={acknowledgement.get('repairRequestExecutionStatus')}")
    print(f"supplement_intake_execution_status={acknowledgement.get('supplementIntakeExecutionStatus')}")
    print(f"supplement_acceptance_execution_status={acknowledgement.get('supplementAcceptanceExecutionStatus')}")
    print(f"committee_reentry_execution_status={acknowledgement.get('committeeReentryExecutionStatus')}")
    print(f"committee_case_execution_status={acknowledgement.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={acknowledgement.get('committeeDecisionExecutionStatus')}")
    print(f"acknowledgement_roles={len(roles)}")
    print(f"acknowledgement_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
