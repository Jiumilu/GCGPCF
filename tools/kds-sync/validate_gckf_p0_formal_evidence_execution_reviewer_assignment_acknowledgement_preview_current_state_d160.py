#!/usr/bin/env python3
"""Validate D160 GCKF P0 formal evidence execution reviewer assignment acknowledgement preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-reviewer-assignment-acknowledgement-preview-current-state-d160-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-reviewer-assignment-acknowledgement-preview-current-state-d160-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-reviewer-assignment-acknowledgement-preview-current-state-d160-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D160-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_reviewer_assignment_acknowledgement_preview_current_state_d160="
        f"fail reason={message}"
    )
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d160_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_ack = load_json(ROOT / fixture["sourceHistoricalReviewerAssignmentAcknowledgementPreview"])
    current_assignment = load_json(ROOT / fixture["sourceCurrentRoutingReviewerAssignmentPreview"])
    acknowledgement = fixture["reviewerAssignmentAcknowledgementPreview"]
    source_historical_ack = historical_ack["reviewerAssignmentAcknowledgementPreview"]
    source_assignment = current_assignment["routingReviewerAssignmentPreview"]

    require(
        fixture.get("reviewerAssignmentAcknowledgementPreviewStatus")
        == expected["reviewerAssignmentAcknowledgementPreviewStatus"],
        "reviewer_assignment_acknowledgement_preview_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalAssignmentAcknowledgement") is expected["notFinalAssignmentAcknowledgement"],
        "not_final_assignment_acknowledgement_mismatch",
    )
    require(acknowledgement.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(acknowledgement.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(acknowledgement.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(
        acknowledgement.get("assignmentAcknowledgementExecutionStatus")
        == expected["assignmentAcknowledgementExecutionStatus"],
        "assignment_acknowledgement_execution_status_mismatch",
    )
    require(
        acknowledgement.get("reviewerAssignmentExecutionStatus")
        == expected["reviewerAssignmentExecutionStatus"],
        "reviewer_assignment_execution_status_mismatch",
    )
    require(
        acknowledgement.get("routingPrecheckExecutionStatus") == expected["routingPrecheckExecutionStatus"],
        "routing_precheck_execution_status_mismatch",
    )
    require(
        acknowledgement.get("routingExecutionStatus") == expected["routingExecutionStatus"],
        "routing_execution_status_mismatch",
    )
    require(
        acknowledgement.get("acknowledgementExecutionStatus") == expected["acknowledgementExecutionStatus"],
        "acknowledgement_execution_status_mismatch",
    )
    require(
        acknowledgement.get("repairRequestExecutionStatus") == expected["repairRequestExecutionStatus"],
        "repair_request_execution_status_mismatch",
    )
    require(
        acknowledgement.get("supplementIntakeExecutionStatus") == expected["supplementIntakeExecutionStatus"],
        "supplement_intake_execution_status_mismatch",
    )
    require(
        acknowledgement.get("supplementAcceptanceExecutionStatus")
        == expected["supplementAcceptanceExecutionStatus"],
        "supplement_acceptance_execution_status_mismatch",
    )
    require(
        acknowledgement.get("committeeReentryExecutionStatus")
        == expected["committeeReentryExecutionStatus"],
        "committee_reentry_execution_status_mismatch",
    )
    require(
        acknowledgement.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"],
        "committee_case_execution_status_mismatch",
    )
    require(
        acknowledgement.get("committeeDecisionExecutionStatus")
        == expected["committeeDecisionExecutionStatus"],
        "committee_decision_execution_status_mismatch",
    )
    require(
        acknowledgement.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"],
        "confirmation_execution_status_mismatch",
    )
    require(
        acknowledgement.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"],
        "unfreeze_execution_status_mismatch",
    )
    require(
        acknowledgement.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"],
        "formal_write_execution_status_mismatch",
    )
    require(
        acknowledgement.get("executionMode") == expected["executionMode"],
        "acknowledgement_execution_mode_mismatch",
    )
    require(acknowledgement.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(
        acknowledgement.get("sourceRoutingReviewerAssignmentPreviewId") == source_assignment.get("id"),
        "source_routing_reviewer_assignment_preview_id_mismatch",
    )

    require(
        historical_ack.get("reviewerAssignmentAcknowledgementPreviewStatus") == "candidate_preview",
        "historical_assignment_acknowledgement_preview_status_mismatch",
    )
    require(
        source_historical_ack.get("previewStatus") == "candidate_preview",
        "historical_preview_status_mismatch",
    )
    require(
        source_historical_ack.get("executionStatus") == "not_executed",
        "historical_execution_status_mismatch",
    )

    require(
        current_assignment.get("routingReviewerAssignmentPreviewStatus")
        == expected["sourceRoutingReviewerAssignmentPreviewStatus"],
        "source_routing_reviewer_assignment_preview_status_mismatch",
    )
    require(
        source_assignment.get("reviewerAssignmentExecutionStatus")
        == expected["sourceReviewerAssignmentExecutionStatus"],
        "source_reviewer_assignment_execution_status_mismatch",
    )
    require(
        source_assignment.get("routingPrecheckExecutionStatus")
        == expected["sourceRoutingPrecheckExecutionStatus"],
        "source_routing_precheck_execution_status_mismatch",
    )
    require(
        source_assignment.get("routingExecutionStatus") == expected["sourceRoutingExecutionStatus"],
        "source_routing_execution_status_mismatch",
    )
    require(
        source_assignment.get("acknowledgementExecutionStatus")
        == expected["sourceAcknowledgementExecutionStatus"],
        "source_acknowledgement_execution_status_mismatch",
    )
    require(
        source_assignment.get("repairRequestExecutionStatus")
        == expected["sourceRepairRequestExecutionStatus"],
        "source_repair_request_execution_status_mismatch",
    )
    require(
        source_assignment.get("supplementIntakeExecutionStatus")
        == expected["sourceSupplementIntakeExecutionStatus"],
        "source_supplement_intake_execution_status_mismatch",
    )
    require(
        source_assignment.get("supplementAcceptanceExecutionStatus")
        == expected["sourceSupplementAcceptanceExecutionStatus"],
        "source_supplement_acceptance_execution_status_mismatch",
    )
    require(
        source_assignment.get("committeeReentryExecutionStatus")
        == expected["sourceCommitteeReentryExecutionStatus"],
        "source_committee_reentry_execution_status_mismatch",
    )
    require(
        source_assignment.get("committeeCaseExecutionStatus")
        == expected["sourceCommitteeCaseExecutionStatus"],
        "source_committee_case_execution_status_mismatch",
    )
    require(
        source_assignment.get("committeeDecisionExecutionStatus")
        == expected["sourceCommitteeDecisionExecutionStatus"],
        "source_committee_decision_execution_status_mismatch",
    )
    require(
        source_assignment.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"],
        "source_confirmation_execution_status_mismatch",
    )
    require(
        source_assignment.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"],
        "source_unfreeze_execution_status_mismatch",
    )
    require(
        fixture.get("coveredRoutingReviewerAssignmentPreviewStatus")
        == expected["coveredRoutingReviewerAssignmentPreviewStatus"],
        "covered_routing_reviewer_assignment_preview_status_mismatch",
    )
    require(
        fixture["coveredRoutingReviewerAssignmentPreviewStatus"] == source_assignment.get("previewStatus"),
        "covered_routing_reviewer_assignment_preview_not_matched",
    )

    roles = set(acknowledgement.get("assignmentAcknowledgementRoles", []))
    require(
        len(roles) == expected["assignmentAcknowledgementRoleCount"],
        "assignment_acknowledgement_role_count_mismatch",
    )
    require_all(
        roles,
        {
            "request_owner",
            "acknowledgement_owner",
            "routing_owner",
            "reviewer_assignment_owner",
            "assignment_acknowledgement_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner",
        },
        "assignment_acknowledgement_role",
    )
    require(
        set(source_assignment.get("reviewerAssignmentRoles", [])).issubset(roles),
        "assignment_acknowledgement_roles_not_covering_reviewer_assignment_roles",
    )

    sections = set(acknowledgement.get("assignmentAcknowledgementSections", []))
    require(
        len(sections) == expected["assignmentAcknowledgementSectionCount"],
        "assignment_acknowledgement_section_count_mismatch",
    )
    require_all(
        sections,
        {
            "source_reviewer_assignment_lineage",
            "assignment_acknowledgement_scope",
            "assignment_acknowledgement_envelope_fields",
            "assignment_acknowledgement_readiness_prerequisites",
            "candidate_assignment_receipt_fields",
            "candidate_acknowledgement_recipient_matrix",
            "recusal_screen_snapshot",
            "acknowledgement_blocker_candidates",
            "candidate_assignment_acknowledgement_path",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "assignment_acknowledgement_section",
    )

    envelope_fields = set(acknowledgement.get("assignmentAcknowledgementEnvelopeFields", []))
    require(
        len(envelope_fields) == expected["assignmentAcknowledgementEnvelopeFieldCount"],
        "assignment_acknowledgement_envelope_field_count_mismatch",
    )
    require_all(
        envelope_fields,
        {
            "assignment_acknowledgement_preview_id",
            "source_reviewer_assignment_preview_id",
            "candidate_assignment_receipt_ref",
            "candidate_acknowledgement_recipient_role",
            "candidate_recusal_screen_ref",
            "candidate_acknowledgement_blocker_code",
            "candidate_assignment_acknowledgement_path_ref",
            "candidate_assignment_acknowledgement_status",
            "no_write_attestation_ref",
        },
        "assignment_acknowledgement_envelope_field",
    )

    prerequisites = set(acknowledgement.get("assignmentAcknowledgementReadinessPrerequisites", []))
    require(
        len(prerequisites) == expected["assignmentAcknowledgementReadinessPrerequisiteCount"],
        "assignment_acknowledgement_readiness_prerequisite_count_mismatch",
    )
    require_all(
        prerequisites,
        {
            "source_reviewer_assignment_candidate_preview_with_hold",
            "source_reviewer_assignment_not_formal_assignment",
            "source_reviewer_assignment_not_executed",
            "source_reviewer_notification_not_executed",
            "source_routing_not_executed",
            "source_committee_reentry_not_executed",
            "source_committee_case_not_opened",
            "assignment_acknowledgement_not_formal_evidence",
        },
        "assignment_acknowledgement_readiness_prerequisite",
    )

    decision_constraints = set(acknowledgement.get("assignmentAcknowledgementDecisionConstraints", []))
    require(
        len(decision_constraints) == expected["assignmentAcknowledgementDecisionConstraintCount"],
        "assignment_acknowledgement_decision_constraint_count_mismatch",
    )
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "assignment_acknowledgement_preview_not_formal_acknowledgement",
            "no_assignment_acknowledgement_execution",
            "no_reviewer_notification",
            "no_reviewer_assignment_execution",
            "no_routing_precheck_execution",
            "no_routing_execution",
            "no_acknowledgement_execution",
            "no_repair_request_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_harness_evidence_write",
        },
        "assignment_acknowledgement_decision_constraint",
    )

    checks = set(acknowledgement.get("assignmentAcknowledgementChecks", []))
    require(
        len(checks) == expected["assignmentAcknowledgementCheckCount"],
        "assignment_acknowledgement_check_count_mismatch",
    )
    require_all(
        checks,
        {
            "source_reviewer_assignment_preview_status_is_candidate_preview_with_hold",
            "source_reviewer_assignment_execution_status_is_not_executed",
            "source_routing_precheck_execution_status_is_not_executed",
            "source_routing_execution_status_is_not_executed",
            "source_acknowledgement_execution_status_is_not_executed",
            "source_repair_request_execution_status_is_not_executed",
            "source_supplement_intake_execution_status_is_not_executed",
            "source_supplement_acceptance_execution_status_is_not_executed",
            "source_committee_reentry_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_reviewer_assignment_preview_is_dry_run_only",
            "reviewer_assignment_acknowledgement_preview_status_is_candidate_preview_with_hold",
            "all_assignment_acknowledgement_roles_covered",
            "all_assignment_acknowledgement_sections_covered",
            "all_assignment_acknowledgement_envelope_fields_covered",
            "all_assignment_acknowledgement_readiness_prerequisites_covered",
            "all_assignment_acknowledgement_decision_constraints_covered",
            "candidate_assignment_receipt_fields_present",
            "candidate_acknowledgement_recipient_matrix_present",
            "recusal_screen_snapshot_present",
            "acknowledgement_blocker_candidates_present",
            "candidate_assignment_acknowledgement_path_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_assignment_acknowledgement_preview_not_formal_acknowledgement",
            "assert_assignment_acknowledgement_not_executed",
            "assert_reviewer_notification_not_executed",
            "assert_reviewer_assignment_not_executed",
            "assert_routing_precheck_not_executed",
            "assert_routing_not_executed",
            "assert_acknowledgement_not_executed",
            "assert_repair_request_not_executed",
            "assert_committee_reentry_not_executed",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "assignment_acknowledgement_check",
    )

    refs = set(acknowledgement.get("requiredAssignmentAcknowledgementRefs", []))
    require(
        len(refs) == expected["requiredAssignmentAcknowledgementRefCount"],
        "required_assignment_acknowledgement_ref_count_mismatch",
    )
    require_all(
        refs,
        {
            "sourceRoutingReviewerAssignmentPreviewRef",
            "sourceAcknowledgementRoutingPrecheckPreviewRef",
            "assignmentAcknowledgementScopeRef",
            "assignmentAcknowledgementEnvelopeFieldsRef",
            "assignmentAcknowledgementReadinessPrerequisitesRef",
            "candidateAssignmentReceiptFieldsRef",
            "candidateAcknowledgementRecipientMatrixRef",
            "recusalScreenSnapshotRef",
            "acknowledgementBlockerCandidatesRef",
            "candidateAssignmentAcknowledgementPathRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "requestOwnerRef",
            "acknowledgementOwnerRef",
            "routingOwnerRef",
            "reviewerAssignmentOwnerRef",
            "assignmentAcknowledgementOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required_assignment_acknowledgement_ref",
    )

    blocking_conditions = set(acknowledgement.get("blockingConditions", []))
    require(
        len(blocking_conditions) == expected["blockingConditionCount"],
        "blocking_condition_count_mismatch",
    )
    require_all(
        blocking_conditions,
        {
            "source_reviewer_assignment_preview_not_candidate_preview_with_hold",
            "source_reviewer_assignment_already_executed",
            "source_routing_precheck_already_executed",
            "source_routing_already_executed",
            "source_acknowledgement_already_executed",
            "source_repair_request_already_executed",
            "source_supplement_intake_already_executed",
            "source_supplement_material_already_accepted",
            "source_committee_reentry_already_executed",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_reviewer_assignment_preview_not_dry_run_only",
            "missing_source_reviewer_assignment_preview_ref",
            "missing_assignment_acknowledgement_scope_ref",
            "missing_assignment_acknowledgement_envelope_fields_ref",
            "missing_candidate_assignment_receipt_fields_ref",
            "missing_candidate_acknowledgement_recipient_matrix_ref",
            "missing_recusal_screen_snapshot_ref",
            "missing_acknowledgement_blocker_candidates_ref",
            "missing_candidate_assignment_acknowledgement_path_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_assignment_acknowledgement_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "assignment_acknowledgement_preview_attempts_formal_acknowledgement",
            "assignment_acknowledgement_preview_attempts_reviewer_notification",
            "assignment_acknowledgement_preview_attempts_reviewer_assignment_execution",
            "assignment_acknowledgement_preview_attempts_routing_precheck_execution",
            "assignment_acknowledgement_preview_attempts_routing_execution",
            "assignment_acknowledgement_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(acknowledgement.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_assignment_acknowledgement",
            "notify_reviewer",
            "execute_reviewer_assignment",
            "execute_routing_precheck",
            "execute_routing",
            "execute_acknowledgement",
            "issue_formal_acknowledgement",
            "execute_repair_request",
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
            "record_assignment_acknowledgement",
            "record_reviewer_notification",
            "record_reviewer_assignment",
            "record_routing_precheck",
            "record_routing",
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
            "convert_assignment_acknowledgement_preview_to_formal_acknowledgement",
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
            "assignment_acknowledgement_executed",
            "reviewer_notified",
            "reviewer_assignment_executed",
            "routing_precheck_executed",
            "routing_executed",
            "acknowledgement_executed",
            "formal_acknowledgement_issued",
            "repair_request_executed",
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
            "assignment_acknowledgement_preview_converted_to_formal_acknowledgement",
            "p1_admission_granted",
            "v1_upgrade_approved",
        },
        "forbidden_output",
    )

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_assignment.get("holdContextRefs", []))
    for hold_ref in hold_refs:
        require(hold_ref in source_hold_refs, f"missing_hold_context_ref:{hold_ref}")

    for key in [
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ]:
        require(
            fixture["currentGateAssertions"].get(key) is False,
            f"current_gate_assertion_not_false:{key}",
        )

    require(
        len(fixture.get("requiredSourceRefs", [])) == expected["requiredSourceRefCount"],
        "required_source_ref_count_mismatch",
    )
    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")

    require(
        evidence.get("current_reviewer_assignment_acknowledgement_preview_status")
        == "candidate_preview_with_hold",
        "evidence_assignment_acknowledgement_preview_status_mismatch",
    )
    require(
        evidence.get("maximum_state") == "review_ready_with_hold",
        "evidence_maximum_state_mismatch",
    )
    require(
        evidence.get("package_scope", {}).get("assignment_acknowledgement_roles") == 12,
        "evidence_assignment_acknowledgement_role_count_mismatch",
    )
    require(
        evidence.get("hold_context", {}).get("source_routing_reviewer_assignment_preview_status")
        == "candidate_preview_with_hold",
        "evidence_source_routing_reviewer_assignment_preview_status_mismatch",
    )

    localization = json.loads(
        run_command(
            "python3",
            "tools/kds-sync/check_chinese_localization_gate.py",
            "--json",
            "--max-findings",
            "10000",
        )
    )
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print(
        "gckf_p0_formal_evidence_execution_reviewer_assignment_acknowledgement_preview_current_state_d160=pass"
    )
    print(
        "reviewer_assignment_acknowledgement_preview_status="
        f"{fixture.get('reviewerAssignmentAcknowledgementPreviewStatus')}"
    )
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={acknowledgement.get('previewStatus')}")
    print(f"execution_status={acknowledgement.get('executionStatus')}")
    print(
        "assignment_acknowledgement_execution_status="
        f"{acknowledgement.get('assignmentAcknowledgementExecutionStatus')}"
    )
    print(f"reviewer_assignment_execution_status={acknowledgement.get('reviewerAssignmentExecutionStatus')}")
    print(f"routing_precheck_execution_status={acknowledgement.get('routingPrecheckExecutionStatus')}")
    print(f"routing_execution_status={acknowledgement.get('routingExecutionStatus')}")
    print(f"acknowledgement_execution_status={acknowledgement.get('acknowledgementExecutionStatus')}")
    print(f"repair_request_execution_status={acknowledgement.get('repairRequestExecutionStatus')}")
    print(f"supplement_intake_execution_status={acknowledgement.get('supplementIntakeExecutionStatus')}")
    print(
        f"supplement_acceptance_execution_status={acknowledgement.get('supplementAcceptanceExecutionStatus')}"
    )
    print(f"committee_reentry_execution_status={acknowledgement.get('committeeReentryExecutionStatus')}")
    print(f"committee_case_execution_status={acknowledgement.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={acknowledgement.get('committeeDecisionExecutionStatus')}")
    print(f"assignment_acknowledgement_roles={len(roles)}")
    print(f"assignment_acknowledgement_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
