#!/usr/bin/env python3
"""Validate D162 GCKF P0 formal evidence execution routing receipt reviewer acceptance precheck preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-routing-receipt-reviewer-acceptance-precheck-preview-current-state-d162-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-routing-receipt-reviewer-acceptance-precheck-preview-current-state-d162-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-routing-receipt-reviewer-acceptance-precheck-preview-current-state-d162-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D162-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_routing_receipt_reviewer_acceptance_precheck_preview_current_state_d162="
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d162_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_precheck = load_json(ROOT / fixture["sourceHistoricalRoutingReceiptReviewerAcceptancePrecheckPreview"])
    current_receipt = load_json(ROOT / fixture["sourceCurrentReviewerAcknowledgementRoutingReceiptPreview"])
    precheck = fixture["routingReceiptReviewerAcceptancePrecheckPreview"]
    source_historical_precheck = historical_precheck["routingReceiptReviewerAcceptancePrecheckPreview"]
    source_receipt = current_receipt["reviewerAcknowledgementRoutingReceiptPreview"]

    require(
        fixture.get("routingReceiptReviewerAcceptancePrecheckPreviewStatus")
        == expected["routingReceiptReviewerAcceptancePrecheckPreviewStatus"],
        "routing_receipt_reviewer_acceptance_precheck_preview_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalReviewerAcceptance") is expected["notFinalReviewerAcceptance"],
        "not_final_reviewer_acceptance_mismatch",
    )
    require(precheck.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(precheck.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(precheck.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(
        precheck.get("reviewerAcceptancePrecheckExecutionStatus")
        == expected["reviewerAcceptancePrecheckExecutionStatus"],
        "reviewer_acceptance_precheck_execution_status_mismatch",
    )
    require(
        precheck.get("reviewerAcceptanceExecutionStatus") == expected["reviewerAcceptanceExecutionStatus"],
        "reviewer_acceptance_execution_status_mismatch",
    )
    require(
        precheck.get("routingReceiptExecutionStatus") == expected["routingReceiptExecutionStatus"],
        "routing_receipt_execution_status_mismatch",
    )
    require(
        precheck.get("assignmentAcknowledgementExecutionStatus")
        == expected["assignmentAcknowledgementExecutionStatus"],
        "assignment_acknowledgement_execution_status_mismatch",
    )
    require(
        precheck.get("reviewerAssignmentExecutionStatus") == expected["reviewerAssignmentExecutionStatus"],
        "reviewer_assignment_execution_status_mismatch",
    )
    require(
        precheck.get("routingPrecheckExecutionStatus") == expected["routingPrecheckExecutionStatus"],
        "routing_precheck_execution_status_mismatch",
    )
    require(precheck.get("routingExecutionStatus") == expected["routingExecutionStatus"], "routing_execution_status_mismatch")
    require(
        precheck.get("acknowledgementExecutionStatus") == expected["acknowledgementExecutionStatus"],
        "acknowledgement_execution_status_mismatch",
    )
    require(
        precheck.get("repairRequestExecutionStatus") == expected["repairRequestExecutionStatus"],
        "repair_request_execution_status_mismatch",
    )
    require(
        precheck.get("supplementIntakeExecutionStatus") == expected["supplementIntakeExecutionStatus"],
        "supplement_intake_execution_status_mismatch",
    )
    require(
        precheck.get("supplementAcceptanceExecutionStatus") == expected["supplementAcceptanceExecutionStatus"],
        "supplement_acceptance_execution_status_mismatch",
    )
    require(
        precheck.get("committeeReentryExecutionStatus") == expected["committeeReentryExecutionStatus"],
        "committee_reentry_execution_status_mismatch",
    )
    require(
        precheck.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"],
        "committee_case_execution_status_mismatch",
    )
    require(
        precheck.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"],
        "committee_decision_execution_status_mismatch",
    )
    require(
        precheck.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"],
        "confirmation_execution_status_mismatch",
    )
    require(
        precheck.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"],
        "unfreeze_execution_status_mismatch",
    )
    require(precheck.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(precheck.get("executionMode") == expected["executionMode"], "precheck_execution_mode_mismatch")
    require(precheck.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(
        precheck.get("sourceReviewerAcknowledgementRoutingReceiptPreviewId") == source_receipt.get("id"),
        "source_reviewer_acknowledgement_routing_receipt_preview_id_mismatch",
    )

    require(
        historical_precheck.get("routingReceiptReviewerAcceptancePrecheckPreviewStatus") == "candidate_preview",
        "historical_reviewer_acceptance_precheck_preview_status_mismatch",
    )
    require(source_historical_precheck.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_historical_precheck.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_receipt.get("reviewerAcknowledgementRoutingReceiptPreviewStatus")
        == expected["sourceReviewerAcknowledgementRoutingReceiptPreviewStatus"],
        "source_reviewer_acknowledgement_routing_receipt_preview_status_mismatch",
    )
    require(
        source_receipt.get("routingReceiptExecutionStatus") == expected["sourceRoutingReceiptExecutionStatus"],
        "source_routing_receipt_execution_status_mismatch",
    )
    require(
        source_receipt.get("assignmentAcknowledgementExecutionStatus")
        == expected["sourceAssignmentAcknowledgementExecutionStatus"],
        "source_assignment_acknowledgement_execution_status_mismatch",
    )
    require(
        source_receipt.get("reviewerNotificationExecutionStatus") == expected["sourceReviewerNotificationExecutionStatus"],
        "source_reviewer_notification_execution_status_mismatch",
    )
    require(
        source_receipt.get("reviewerAssignmentExecutionStatus") == expected["sourceReviewerAssignmentExecutionStatus"],
        "source_reviewer_assignment_execution_status_mismatch",
    )
    require(
        source_receipt.get("routingPrecheckExecutionStatus") == expected["sourceRoutingPrecheckExecutionStatus"],
        "source_routing_precheck_execution_status_mismatch",
    )
    require(
        source_receipt.get("routingExecutionStatus") == expected["sourceRoutingExecutionStatus"],
        "source_routing_execution_status_mismatch",
    )
    require(
        source_receipt.get("acknowledgementExecutionStatus") == expected["sourceAcknowledgementExecutionStatus"],
        "source_acknowledgement_execution_status_mismatch",
    )
    require(
        source_receipt.get("repairRequestExecutionStatus") == expected["sourceRepairRequestExecutionStatus"],
        "source_repair_request_execution_status_mismatch",
    )
    require(
        source_receipt.get("supplementIntakeExecutionStatus") == expected["sourceSupplementIntakeExecutionStatus"],
        "source_supplement_intake_execution_status_mismatch",
    )
    require(
        source_receipt.get("supplementAcceptanceExecutionStatus") == expected["sourceSupplementAcceptanceExecutionStatus"],
        "source_supplement_acceptance_execution_status_mismatch",
    )
    require(
        source_receipt.get("committeeReentryExecutionStatus") == expected["sourceCommitteeReentryExecutionStatus"],
        "source_committee_reentry_execution_status_mismatch",
    )
    require(
        source_receipt.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"],
        "source_committee_case_execution_status_mismatch",
    )
    require(
        source_receipt.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"],
        "source_committee_decision_execution_status_mismatch",
    )
    require(
        source_receipt.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"],
        "source_confirmation_execution_status_mismatch",
    )
    require(
        source_receipt.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"],
        "source_unfreeze_execution_status_mismatch",
    )
    require(
        fixture.get("coveredReviewerAcknowledgementRoutingReceiptPreviewStatus")
        == expected["coveredReviewerAcknowledgementRoutingReceiptPreviewStatus"],
        "covered_reviewer_acknowledgement_routing_receipt_preview_status_mismatch",
    )
    require(
        fixture["coveredReviewerAcknowledgementRoutingReceiptPreviewStatus"] == source_receipt.get("previewStatus"),
        "covered_reviewer_acknowledgement_routing_receipt_preview_not_matched",
    )

    roles = set(precheck.get("reviewerAcceptancePrecheckRoles", []))
    require(len(roles) == expected["reviewerAcceptancePrecheckRoleCount"], "reviewer_acceptance_precheck_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "acknowledgement_owner",
            "routing_owner",
            "reviewer_assignment_owner",
            "assignment_acknowledgement_owner",
            "routing_receipt_owner",
            "reviewer_acceptance_precheck_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner",
        },
        "reviewer_acceptance_precheck_role",
    )
    require(
        set(source_receipt.get("routingReceiptRoles", [])).issubset(roles),
        "reviewer_acceptance_precheck_roles_not_covering_routing_receipt_roles",
    )

    sections = set(precheck.get("reviewerAcceptancePrecheckSections", []))
    require(len(sections) == expected["reviewerAcceptancePrecheckSectionCount"], "reviewer_acceptance_precheck_section_count_mismatch")
    require_all(
        sections,
        {
            "source_routing_receipt_lineage",
            "reviewer_acceptance_precheck_scope",
            "reviewer_acceptance_precheck_envelope_fields",
            "reviewer_acceptance_precheck_readiness_prerequisites",
            "candidate_reviewer_acceptance_matrix",
            "candidate_recusal_and_conflict_check",
            "candidate_capacity_and_sla_check",
            "candidate_access_boundary_check",
            "candidate_acceptance_blocker_codes",
            "candidate_acceptance_hold_conditions",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "reviewer_acceptance_precheck_section",
    )

    envelope_fields = set(precheck.get("reviewerAcceptancePrecheckEnvelopeFields", []))
    require(
        len(envelope_fields) == expected["reviewerAcceptancePrecheckEnvelopeFieldCount"],
        "reviewer_acceptance_precheck_envelope_field_count_mismatch",
    )
    require_all(
        envelope_fields,
        {
            "reviewer_acceptance_precheck_preview_id",
            "source_routing_receipt_preview_id",
            "candidate_reviewer_role",
            "candidate_reviewer_acceptance_ref",
            "candidate_recusal_check_ref",
            "candidate_capacity_sla_ref",
            "candidate_access_boundary_ref",
            "candidate_acceptance_blocker_code",
            "candidate_reviewer_acceptance_precheck_status",
            "no_write_attestation_ref",
        },
        "reviewer_acceptance_precheck_envelope_field",
    )

    prerequisites = set(precheck.get("reviewerAcceptancePrecheckReadinessPrerequisites", []))
    require(
        len(prerequisites) == expected["reviewerAcceptancePrecheckReadinessPrerequisiteCount"],
        "reviewer_acceptance_precheck_readiness_prerequisite_count_mismatch",
    )
    require_all(
        prerequisites,
        {
            "source_routing_receipt_candidate_preview_with_hold",
            "source_routing_receipt_not_formal_receipt",
            "source_routing_receipt_not_executed",
            "source_assignment_acknowledgement_not_executed",
            "source_reviewer_notification_not_executed",
            "source_reviewer_assignment_not_executed",
            "source_committee_case_not_opened",
            "reviewer_acceptance_precheck_not_formal_evidence",
        },
        "reviewer_acceptance_precheck_readiness_prerequisite",
    )

    decision_constraints = set(precheck.get("reviewerAcceptancePrecheckDecisionConstraints", []))
    require(
        len(decision_constraints) == expected["reviewerAcceptancePrecheckDecisionConstraintCount"],
        "reviewer_acceptance_precheck_decision_constraint_count_mismatch",
    )
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "reviewer_acceptance_precheck_not_formal_acceptance",
            "no_reviewer_acceptance_precheck_execution",
            "no_reviewer_acceptance_execution",
            "no_routing_receipt_execution",
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
        "reviewer_acceptance_precheck_decision_constraint",
    )

    checks = set(precheck.get("reviewerAcceptancePrecheckChecks", []))
    require(len(checks) == expected["reviewerAcceptancePrecheckCheckCount"], "reviewer_acceptance_precheck_check_count_mismatch")
    require_all(
        checks,
        {
            "source_routing_receipt_preview_status_is_candidate_preview_with_hold",
            "source_routing_receipt_execution_status_is_not_executed",
            "source_assignment_acknowledgement_execution_status_is_not_executed",
            "source_reviewer_notification_execution_status_is_not_executed",
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
            "source_routing_receipt_preview_is_dry_run_only",
            "reviewer_acceptance_precheck_preview_status_is_candidate_preview_with_hold",
            "all_reviewer_acceptance_precheck_roles_covered",
            "all_reviewer_acceptance_precheck_sections_covered",
            "all_reviewer_acceptance_precheck_envelope_fields_covered",
            "all_reviewer_acceptance_precheck_readiness_prerequisites_covered",
            "all_reviewer_acceptance_precheck_decision_constraints_covered",
            "candidate_reviewer_acceptance_matrix_present",
            "candidate_recusal_and_conflict_check_present",
            "candidate_capacity_and_sla_check_present",
            "candidate_access_boundary_check_present",
            "candidate_acceptance_blocker_codes_present",
            "candidate_acceptance_hold_conditions_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_reviewer_acceptance_precheck_not_formal_acceptance",
            "assert_reviewer_acceptance_precheck_not_executed",
            "assert_reviewer_acceptance_not_executed",
            "assert_routing_receipt_not_executed",
            "assert_assignment_acknowledgement_not_executed",
            "assert_reviewer_notification_not_executed",
            "assert_reviewer_assignment_not_executed",
            "assert_committee_reentry_not_executed",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "reviewer_acceptance_precheck_check",
    )

    refs = set(precheck.get("requiredReviewerAcceptancePrecheckRefs", []))
    require(
        len(refs) == expected["requiredReviewerAcceptancePrecheckRefCount"],
        "required_reviewer_acceptance_precheck_ref_count_mismatch",
    )
    require_all(
        refs,
        {
            "sourceReviewerAcknowledgementRoutingReceiptPreviewRef",
            "sourceReviewerAssignmentAcknowledgementPreviewRef",
            "reviewerAcceptancePrecheckScopeRef",
            "reviewerAcceptancePrecheckEnvelopeFieldsRef",
            "reviewerAcceptancePrecheckReadinessPrerequisitesRef",
            "candidateReviewerAcceptanceMatrixRef",
            "candidateRecusalAndConflictCheckRef",
            "candidateCapacityAndSlaCheckRef",
            "candidateAccessBoundaryCheckRef",
            "candidateAcceptanceBlockerCodesRef",
            "candidateAcceptanceHoldConditionsRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "requestOwnerRef",
            "acknowledgementOwnerRef",
            "routingOwnerRef",
            "reviewerAssignmentOwnerRef",
            "assignmentAcknowledgementOwnerRef",
            "routingReceiptOwnerRef",
            "reviewerAcceptancePrecheckOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required_reviewer_acceptance_precheck_ref",
    )

    blocking_conditions = set(precheck.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_routing_receipt_preview_not_candidate_preview_with_hold",
            "source_routing_receipt_already_executed",
            "source_assignment_acknowledgement_already_executed",
            "source_reviewer_notification_already_executed",
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
            "source_routing_receipt_preview_not_dry_run_only",
            "missing_source_routing_receipt_preview_ref",
            "missing_reviewer_acceptance_precheck_scope_ref",
            "missing_reviewer_acceptance_precheck_envelope_fields_ref",
            "missing_candidate_reviewer_acceptance_matrix_ref",
            "missing_candidate_recusal_and_conflict_check_ref",
            "missing_candidate_capacity_and_sla_check_ref",
            "missing_candidate_access_boundary_check_ref",
            "missing_candidate_acceptance_blocker_codes_ref",
            "missing_candidate_acceptance_hold_conditions_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_reviewer_acceptance_precheck_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "reviewer_acceptance_precheck_attempts_formal_acceptance",
            "reviewer_acceptance_precheck_attempts_reviewer_acceptance_execution",
            "reviewer_acceptance_precheck_attempts_routing_receipt_execution",
            "reviewer_acceptance_precheck_attempts_assignment_acknowledgement_execution",
            "reviewer_acceptance_precheck_attempts_reviewer_notification",
            "reviewer_acceptance_precheck_attempts_reviewer_assignment_execution",
            "reviewer_acceptance_precheck_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(precheck.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_reviewer_acceptance_precheck",
            "accept_reviewer",
            "execute_routing_receipt",
            "execute_assignment_acknowledgement",
            "notify_reviewer",
            "execute_reviewer_assignment",
            "execute_routing_precheck",
            "execute_routing",
            "execute_acknowledgement",
            "issue_formal_reviewer_acceptance",
            "issue_formal_routing_receipt",
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
            "record_reviewer_acceptance_precheck",
            "record_reviewer_acceptance",
            "record_routing_receipt",
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
            "convert_reviewer_acceptance_precheck_to_formal_acceptance",
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
            "reviewer_acceptance_precheck_executed",
            "reviewer_accepted",
            "routing_receipt_executed",
            "assignment_acknowledgement_executed",
            "reviewer_notified",
            "reviewer_assignment_executed",
            "routing_precheck_executed",
            "routing_executed",
            "acknowledgement_executed",
            "formal_reviewer_acceptance_issued",
            "formal_routing_receipt_issued",
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
            "reviewer_acceptance_precheck_converted_to_formal_acceptance",
            "p1_admission_granted",
            "v1_upgrade_approved",
        },
        "forbidden_output",
    )

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
        evidence.get("current_routing_receipt_reviewer_acceptance_precheck_preview_status")
        == "candidate_preview_with_hold",
        "evidence_reviewer_acceptance_precheck_preview_status_mismatch",
    )
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(
        evidence.get("package_scope", {}).get("reviewer_acceptance_precheck_roles") == 14,
        "evidence_reviewer_acceptance_precheck_role_count_mismatch",
    )
    require(
        evidence.get("hold_context", {}).get("source_reviewer_acknowledgement_routing_receipt_preview_status")
        == "candidate_preview_with_hold",
        "evidence_source_reviewer_acknowledgement_routing_receipt_preview_status_mismatch",
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

    print("gckf_p0_formal_evidence_execution_routing_receipt_reviewer_acceptance_precheck_preview_current_state_d162=pass")
    print(f"routing_receipt_reviewer_acceptance_precheck_preview_status={fixture.get('routingReceiptReviewerAcceptancePrecheckPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={precheck.get('previewStatus')}")
    print(f"execution_status={precheck.get('executionStatus')}")
    print(f"reviewer_acceptance_precheck_execution_status={precheck.get('reviewerAcceptancePrecheckExecutionStatus')}")
    print(f"reviewer_acceptance_execution_status={precheck.get('reviewerAcceptanceExecutionStatus')}")
    print(f"routing_receipt_execution_status={precheck.get('routingReceiptExecutionStatus')}")
    print(f"assignment_acknowledgement_execution_status={precheck.get('assignmentAcknowledgementExecutionStatus')}")
    print(f"reviewer_assignment_execution_status={precheck.get('reviewerAssignmentExecutionStatus')}")
    print(f"routing_precheck_execution_status={precheck.get('routingPrecheckExecutionStatus')}")
    print(f"routing_execution_status={precheck.get('routingExecutionStatus')}")
    print(f"acknowledgement_execution_status={precheck.get('acknowledgementExecutionStatus')}")
    print(f"repair_request_execution_status={precheck.get('repairRequestExecutionStatus')}")
    print(f"supplement_intake_execution_status={precheck.get('supplementIntakeExecutionStatus')}")
    print(f"supplement_acceptance_execution_status={precheck.get('supplementAcceptanceExecutionStatus')}")
    print(f"committee_reentry_execution_status={precheck.get('committeeReentryExecutionStatus')}")
    print(f"committee_case_execution_status={precheck.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={precheck.get('committeeDecisionExecutionStatus')}")
    print(f"reviewer_acceptance_precheck_roles={len(roles)}")
    print(f"reviewer_acceptance_precheck_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
