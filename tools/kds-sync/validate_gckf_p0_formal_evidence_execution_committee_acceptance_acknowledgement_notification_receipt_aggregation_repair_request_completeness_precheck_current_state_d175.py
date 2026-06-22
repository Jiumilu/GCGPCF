#!/usr/bin/env python3
"""Validate D175 GCKF P0 repair request completeness precheck current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-completeness-precheck-current-state-d175-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-completeness-precheck-current-state-d175-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-completeness-precheck-current-state-d175-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D175-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_completeness_precheck_current_state_d175="
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
    historical = load_json(ROOT / fixture["sourceHistoricalRepairRequestCompletenessPrecheck"])
    current_source = load_json(ROOT / fixture["sourceCurrentRepairRequestIntakePreview"])
    precheck = fixture["repairRequestCompletenessPrecheck"]
    historical_precheck = historical["repairRequestCompletenessPrecheck"]
    source_intake = current_source["repairRequestIntakePreview"]

    require(
        fixture.get("repairRequestCompletenessPrecheckStatus") == expected["repairRequestCompletenessPrecheckStatus"],
        "precheck_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalRepairRequestCompletenessPrecheck") is expected["notFinalRepairRequestCompletenessPrecheck"],
        "not_final_precheck_mismatch",
    )
    require(precheck.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(precheck.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "repairRequestCompletenessPrecheckPreviewExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus",
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
        require(precheck.get(key) == "not_executed", f"{key}_mismatch")

    require(precheck.get("executionMode") == expected["executionMode"], "precheck_execution_mode_mismatch")
    require(precheck.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("repairRequestCompletenessPrecheckStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_precheck.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_precheck.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("repairRequestIntakePreviewStatus") == expected["sourceRepairRequestIntakePreviewStatus"],
        "source_intake_status_mismatch",
    )
    for source_key, expected_key in (
        ("repairIntakePreviewExecutionStatus", "sourceRepairIntakePreviewExecutionStatus"),
        ("repairIntakeExecutionStatus", "sourceRepairIntakeExecutionStatus"),
        ("repairRequestCreationStatus", "sourceRepairRequestCreationStatus"),
        ("aggregationCompletenessPrecheckPreviewExecutionStatus", "sourceAggregationCompletenessPrecheckPreviewExecutionStatus"),
        ("aggregationCompletenessPrecheckExecutionStatus", "sourceAggregationCompletenessPrecheckExecutionStatus"),
        ("notificationReceiptAggregationPreviewExecutionStatus", "sourceNotificationReceiptAggregationPreviewExecutionStatus"),
        ("notificationReceiptAggregationExecutionStatus", "sourceNotificationReceiptAggregationExecutionStatus"),
        ("notificationReceiptPreviewExecutionStatus", "sourceNotificationReceiptPreviewExecutionStatus"),
        ("notificationReceiptExecutionStatus", "sourceNotificationReceiptExecutionStatus"),
        ("notificationPreviewExecutionStatus", "sourceNotificationPreviewExecutionStatus"),
        ("notificationExecutionStatus", "sourceNotificationExecutionStatus"),
        ("acknowledgementDispatchExecutionStatus", "sourceAcknowledgementDispatchExecutionStatus"),
        ("acknowledgementRoutingExecutionStatus", "sourceAcknowledgementRoutingExecutionStatus"),
        ("committeeAcceptanceExecutionStatus", "sourceCommitteeAcceptanceExecutionStatus"),
        ("committeeAcknowledgementExecutionStatus", "sourceCommitteeAcknowledgementExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_intake.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_intake.get("dryRunOnly") is True, "source_intake_not_dry_run_only")
    require(
        precheck.get("sourceRepairRequestIntakePreviewId") == source_intake.get("id"),
        "source_intake_id_mismatch",
    )
    require(
        fixture.get("coveredRepairRequestIntakePreviewStatus") == expected["coveredRepairRequestIntakePreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredRepairRequestIntakePreviewStatus"] == source_intake.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(precheck.get("precheckRoles", []))
    sections = set(precheck.get("precheckSections", []))
    fields = set(precheck.get("candidatePrecheckFields", []))
    prerequisites = set(precheck.get("precheckReadinessPrerequisites", []))
    constraints = set(precheck.get("precheckDecisionConstraints", []))
    checks = set(precheck.get("precheckChecks", []))
    refs = set(precheck.get("requiredPrecheckRefs", []))
    blocking_conditions = set(precheck.get("blockingConditions", []))
    forbidden_actions = set(precheck.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["precheckRoleCount"], "precheck_role_count_mismatch")
    require(len(sections) == expected["precheckSectionCount"], "precheck_section_count_mismatch")
    require(len(fields) == expected["candidatePrecheckFieldCount"], "candidate_precheck_field_count_mismatch")
    require(len(prerequisites) == expected["precheckReadinessPrerequisiteCount"], "precheck_prerequisite_count_mismatch")
    require(len(constraints) == expected["precheckDecisionConstraintCount"], "precheck_constraint_count_mismatch")
    require(len(checks) == expected["precheckCheckCount"], "precheck_check_count_mismatch")
    require(len(refs) == expected["requiredPrecheckRefCount"], "required_precheck_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "repair_intake_owner",
            "precheck_owner",
            "aggregation_owner",
            "committee_secretariat",
            "waes_gate_owner",
            "harness_reviewer",
            "acl_owner",
        },
        "precheck_role",
    )
    require_all(
        sections,
        {
            "candidate_required_receipt_material_matrix",
            "candidate_submitted_material_snapshot",
            "candidate_missing_material_gap_list",
            "candidate_submitter_boundary_snapshot",
            "candidate_acl_boundary_snapshot",
            "candidate_precheck_hold_conditions",
            "candidate_precheck_blocker_codes",
            "candidate_hold_context_refs_snapshot",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "precheck_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_with_hold_only",
            "precheck_not_formal_acceptance",
            "no_repair_request_completeness_precheck_execution",
            "no_repair_intake_execution",
            "no_repair_request_creation",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "precheck_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_repair_request_completeness_precheck",
            "execute_repair_intake",
            "create_repair_request",
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
        evidence.get("current_repair_request_completeness_precheck_status") == expected["repairRequestCompletenessPrecheckStatus"],
        "evidence_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(evidence.get("execution_mode") == "local_evidence_no_write", "evidence_execution_mode_mismatch")
    require(evidence.get("execution_status") == "not_executed", "evidence_execution_status_mismatch")
    require(package_scope.get("precheck_roles") == expected["precheckRoleCount"], "evidence_precheck_roles_mismatch")
    require(package_scope.get("precheck_sections") == expected["precheckSectionCount"], "evidence_precheck_sections_mismatch")
    require(package_scope.get("candidate_precheck_fields") == expected["candidatePrecheckFieldCount"], "evidence_candidate_precheck_fields_mismatch")
    require(package_scope.get("precheck_readiness_prerequisites") == expected["precheckReadinessPrerequisiteCount"], "evidence_prerequisites_mismatch")
    require(package_scope.get("precheck_decision_constraints") == expected["precheckDecisionConstraintCount"], "evidence_constraints_mismatch")
    require(package_scope.get("precheck_checks") == expected["precheckCheckCount"], "evidence_checks_mismatch")
    require(package_scope.get("required_precheck_refs") == expected["requiredPrecheckRefCount"], "evidence_required_refs_mismatch")
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
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_completeness_precheck_current_state_d175=pass"
    )
    print(f"repair_request_completeness_precheck_status={fixture['repairRequestCompletenessPrecheckStatus']}")
    print(f"maximum_state={fixture['maximumState']}")
    print(f"preview_status={precheck['previewStatus']}")
    print(f"execution_status={precheck['executionStatus']}")
    print(f"precheck_roles={len(roles)}")
    print(f"precheck_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
