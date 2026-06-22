#!/usr/bin/env python3
"""Validate D174 GCKF P0 repair request intake preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-precheck-repair-request-intake-preview-current-state-d174-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-precheck-repair-request-intake-preview-current-state-d174-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-precheck-repair-request-intake-preview-current-state-d174-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D174-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_precheck_repair_request_intake_preview_current_state_d174="
        f"fail reason={message}"
    )
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_all(actual: set[str], expected_values: set[str], label: str) -> None:
    for value in expected_values:
        require(value in actual, f"missing_{label}:{value}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    expected = fixture["expectedSummary"]
    historical = load_json(ROOT / fixture["sourceHistoricalRepairRequestIntakePreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentAggregationCompletenessPrecheck"])
    intake = fixture["repairRequestIntakePreview"]
    historical_intake = historical["repairRequestIntakePreview"]
    source_precheck = current_source["aggregationCompletenessPrecheck"]

    require(
        fixture.get("repairRequestIntakePreviewStatus") == expected["repairRequestIntakePreviewStatus"],
        "intake_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalRepairRequestIntake") is expected["notFinalRepairRequestIntake"],
        "not_final_intake_mismatch",
    )
    require(intake.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(intake.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "repairIntakePreviewExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "aggregationCompletenessPrecheckPreviewExecutionStatus",
        "aggregationCompletenessPrecheckExecutionStatus",
        "notificationReceiptAggregationPreviewExecutionStatus",
        "notificationReceiptAggregationExecutionStatus",
        "notificationReceiptPreviewExecutionStatus",
        "notificationReceiptExecutionStatus",
        "notificationPreviewExecutionStatus",
        "notificationExecutionStatus",
        "acknowledgementDispatchExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "envelopeAssemblyExecutionStatus",
        "committeeAcceptancePrecheckExecutionStatus",
        "committeeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus",
        "intakeGuardExecutionStatus",
        "routingPackageExecutionStatus",
        "reviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus",
        "routingReceiptExecutionStatus",
        "assignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus",
        "routingExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        require(intake.get(key) == "not_executed", f"{key}_mismatch")

    require(intake.get("executionMode") == expected["executionMode"], "intake_execution_mode_mismatch")
    require(intake.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("repairRequestIntakePreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_intake.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_intake.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("aggregationCompletenessPrecheckStatus")
        == expected["sourceAggregationCompletenessPrecheckStatus"],
        "source_precheck_status_mismatch",
    )
    for source_key, expected_key in (
        ("aggregationCompletenessPrecheckPreviewExecutionStatus", "sourcePrecheckPreviewExecutionStatus"),
        ("aggregationCompletenessPrecheckExecutionStatus", "sourcePrecheckExecutionStatus"),
        ("notificationReceiptAggregationPreviewExecutionStatus", "sourceAggregationPreviewExecutionStatus"),
        ("notificationReceiptAggregationExecutionStatus", "sourceAggregationExecutionStatus"),
        ("notificationReceiptPreviewExecutionStatus", "sourceReceiptPreviewExecutionStatus"),
        ("notificationReceiptExecutionStatus", "sourceReceiptExecutionStatus"),
        ("notificationPreviewExecutionStatus", "sourceNotificationPreviewExecutionStatus"),
        ("notificationExecutionStatus", "sourceNotificationExecutionStatus"),
        ("acknowledgementDispatchExecutionStatus", "sourceAcknowledgementDispatchExecutionStatus"),
        ("acknowledgementRoutingExecutionStatus", "sourceAcknowledgementRoutingExecutionStatus"),
        ("envelopeAssemblyExecutionStatus", "sourceEnvelopeAssemblyExecutionStatus"),
        ("committeeAcceptancePrecheckExecutionStatus", "sourceCommitteeAcceptancePrecheckExecutionStatus"),
        ("committeeAcceptanceExecutionStatus", "sourceCommitteeAcceptanceExecutionStatus"),
        ("committeeAcknowledgementExecutionStatus", "sourceCommitteeAcknowledgementExecutionStatus"),
        ("intakeGuardExecutionStatus", "sourceIntakeGuardExecutionStatus"),
        ("routingPackageExecutionStatus", "sourceRoutingPackageExecutionStatus"),
        ("reviewerAcceptanceAcknowledgementExecutionStatus", "sourceReviewerAcceptanceAcknowledgementExecutionStatus"),
        ("reviewerAcceptancePrecheckExecutionStatus", "sourceReviewerAcceptancePrecheckExecutionStatus"),
        ("reviewerAcceptanceExecutionStatus", "sourceReviewerAcceptanceExecutionStatus"),
        ("routingReceiptExecutionStatus", "sourceRoutingReceiptExecutionStatus"),
        ("assignmentAcknowledgementExecutionStatus", "sourceAssignmentAcknowledgementExecutionStatus"),
        ("reviewerNotificationExecutionStatus", "sourceReviewerNotificationExecutionStatus"),
        ("reviewerAssignmentExecutionStatus", "sourceReviewerAssignmentExecutionStatus"),
        ("routingExecutionStatus", "sourceRoutingExecutionStatus"),
        ("committeeReentryExecutionStatus", "sourceCommitteeReentryExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_precheck.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_precheck.get("dryRunOnly") is True, "source_precheck_not_dry_run_only")
    require(
        intake.get("sourceAggregationCompletenessPrecheckId") == source_precheck.get("id"),
        "source_precheck_id_mismatch",
    )
    require(
        fixture.get("coveredAggregationCompletenessPrecheckStatus") == expected["coveredAggregationCompletenessPrecheckStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredAggregationCompletenessPrecheckStatus"] == source_precheck.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(intake.get("repairIntakeRoles", []))
    sections = set(intake.get("repairIntakeSections", []))
    fields = set(intake.get("candidateRepairIntakeFields", []))
    prerequisites = set(intake.get("repairIntakeReadinessPrerequisites", []))
    constraints = set(intake.get("repairIntakeDecisionConstraints", []))
    checks = set(intake.get("repairIntakeChecks", []))
    refs = set(intake.get("requiredRepairIntakeRefs", []))
    blocking_conditions = set(intake.get("blockingConditions", []))
    forbidden_actions = set(intake.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["repairIntakeRoleCount"], "repair_intake_role_count_mismatch")
    require(len(sections) == expected["repairIntakeSectionCount"], "repair_intake_section_count_mismatch")
    require(len(fields) == expected["candidateRepairIntakeFieldCount"], "candidate_repair_intake_field_count_mismatch")
    require(len(prerequisites) == expected["repairIntakeReadinessPrerequisiteCount"], "repair_intake_prerequisite_count_mismatch")
    require(len(constraints) == expected["repairIntakeDecisionConstraintCount"], "repair_intake_constraint_count_mismatch")
    require(len(checks) == expected["repairIntakeCheckCount"], "repair_intake_check_count_mismatch")
    require(len(refs) == expected["requiredRepairIntakeRefCount"], "required_repair_intake_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "aggregation_owner",
            "precheck_owner",
            "repair_intake_owner",
            "receipt_owner",
            "committee_secretariat",
            "waes_gate_owner",
            "harness_reviewer",
            "acl_owner",
        },
        "repair_intake_role",
    )
    require_all(
        sections,
        {
            "candidate_precheck_gap_reason_matrix",
            "candidate_required_receipt_material_matrix",
            "candidate_submitter_boundary",
            "candidate_intake_channel_matrix",
            "candidate_acl_boundary_snapshot",
            "candidate_intake_hold_conditions",
            "candidate_intake_blocker_codes",
            "candidate_hold_context_refs_snapshot",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "repair_intake_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_with_hold_only",
            "repair_intake_preview_not_formal_intake",
            "no_repair_intake_preview_execution",
            "no_repair_intake_execution",
            "no_repair_request_creation",
            "no_completeness_precheck_execution",
            "no_notification_receipt_aggregation_execution",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "repair_intake_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_repair_intake_preview",
            "execute_repair_intake",
            "create_repair_request",
            "execute_aggregation_completeness_precheck",
            "execute_notification_receipt_aggregation",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    package_scope = evidence.get("package_scope", {})
    require(
        evidence.get("current_repair_request_intake_preview_status") == expected["repairRequestIntakePreviewStatus"],
        "evidence_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(evidence.get("execution_mode") == "local_evidence_no_write", "evidence_execution_mode_mismatch")
    require(evidence.get("execution_status") == "not_executed", "evidence_execution_status_mismatch")
    require(package_scope.get("repair_intake_roles") == expected["repairIntakeRoleCount"], "evidence_repair_intake_roles_mismatch")
    require(package_scope.get("repair_intake_sections") == expected["repairIntakeSectionCount"], "evidence_repair_intake_sections_mismatch")
    require(package_scope.get("candidate_repair_intake_fields") == expected["candidateRepairIntakeFieldCount"], "evidence_candidate_repair_intake_fields_mismatch")
    require(package_scope.get("repair_intake_readiness_prerequisites") == expected["repairIntakeReadinessPrerequisiteCount"], "evidence_prerequisites_mismatch")
    require(package_scope.get("repair_intake_decision_constraints") == expected["repairIntakeDecisionConstraintCount"], "evidence_constraints_mismatch")
    require(package_scope.get("repair_intake_checks") == expected["repairIntakeCheckCount"], "evidence_checks_mismatch")
    require(package_scope.get("required_repair_intake_refs") == expected["requiredRepairIntakeRefCount"], "evidence_required_refs_mismatch")
    require(package_scope.get("blocking_conditions") == expected["blockingConditionCount"], "evidence_blocking_conditions_mismatch")
    require(package_scope.get("forbidden_actions") == expected["forbiddenActionCount"], "evidence_forbidden_actions_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_context_refs_mismatch")

    gate_assertions = evidence.get("gateAssertions", {})
    for key in (
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ):
        require(gate_assertions.get(key) is False, f"gate_assertion_not_false:{key}")

    evidence_md = EVIDENCE_MD.read_text(encoding="utf-8")
    loop_md = LOOP_MD.read_text(encoding="utf-8")
    require("candidate_preview_with_hold" in evidence_md, "evidence_md_missing_hold_status")
    require("review_ready_with_hold" in evidence_md, "evidence_md_missing_maximum_state")
    require("Hold 上下文" in evidence_md, "evidence_md_missing_hold_section")
    require("candidate_preview_with_hold" in loop_md, "loop_md_missing_hold_status")
    require("继续保持 no-write" in loop_md, "loop_md_missing_next_round_guidance")

    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_precheck_repair_request_intake_preview_current_state_d174=pass"
    )
    print(f"repair_request_intake_preview_status={fixture['repairRequestIntakePreviewStatus']}")
    print(f"maximum_state={fixture['maximumState']}")
    print(f"preview_status={intake['previewStatus']}")
    print(f"execution_status={intake['executionStatus']}")
    print(f"repair_intake_roles={len(roles)}")
    print(f"repair_intake_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
