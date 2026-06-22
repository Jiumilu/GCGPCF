#!/usr/bin/env python3
"""Validate D172 GCKF P0 committee acceptance acknowledgement notification receipt aggregation preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-preview-current-state-d172-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-preview-current-state-d172-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-preview-current-state-d172-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D172-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_preview_current_state_d172="
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
    historical = load_json(ROOT / fixture["sourceHistoricalCommitteeAcceptanceAcknowledgementNotificationReceiptAggregationPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentCommitteeAcceptanceAcknowledgementNotificationReceiptPreview"])
    aggregation = fixture["committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreview"]
    historical_aggregation = historical["committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreview"]
    source_receipt = current_source["committeeAcceptanceAcknowledgementNotificationReceiptPreview"]

    require(
        fixture.get("committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus")
        == expected["committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus"],
        "aggregation_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalCommitteeAcceptanceAcknowledgementNotificationReceiptAggregation")
        is expected["notFinalCommitteeAcceptanceAcknowledgementNotificationReceiptAggregation"],
        "not_final_aggregation_mismatch",
    )
    require(aggregation.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(aggregation.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
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
        require(aggregation.get(key) == expected[key], f"{key}_mismatch")

    require(aggregation.get("executionMode") == expected["executionMode"], "aggregation_execution_mode_mismatch")
    require(aggregation.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_aggregation.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_aggregation.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("committeeAcceptanceAcknowledgementNotificationReceiptPreviewStatus")
        == expected["sourceCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewStatus"],
        "source_receipt_status_mismatch",
    )
    for source_key, expected_key in (
        ("notificationReceiptPreviewExecutionStatus", "sourceNotificationReceiptPreviewExecutionStatus"),
        ("notificationReceiptExecutionStatus", "sourceNotificationReceiptExecutionStatus"),
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
        require(source_receipt.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_receipt.get("dryRunOnly") is True, "source_receipt_not_dry_run_only")
    require(
        aggregation.get("sourceCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewId") == source_receipt.get("id"),
        "source_receipt_id_mismatch",
    )
    require(
        fixture.get("coveredCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewStatus")
        == expected["coveredCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewStatus"] == source_receipt.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(aggregation.get("aggregationRoles", []))
    sections = set(aggregation.get("aggregationSections", []))
    fields = set(aggregation.get("candidateAggregationFields", []))
    prerequisites = set(aggregation.get("aggregationReadinessPrerequisites", []))
    constraints = set(aggregation.get("aggregationDecisionConstraints", []))
    checks = set(aggregation.get("aggregationChecks", []))
    refs = set(aggregation.get("requiredAggregationRefs", []))
    blocking_conditions = set(aggregation.get("blockingConditions", []))
    forbidden_actions = set(aggregation.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["aggregationRoleCount"], "aggregation_role_count_mismatch")
    require(len(sections) == expected["aggregationSectionCount"], "aggregation_section_count_mismatch")
    require(len(fields) == expected["candidateAggregationFieldCount"], "candidate_aggregation_field_count_mismatch")
    require(len(prerequisites) == expected["aggregationReadinessPrerequisiteCount"], "aggregation_prerequisite_count_mismatch")
    require(len(constraints) == expected["aggregationDecisionConstraintCount"], "aggregation_constraint_count_mismatch")
    require(len(checks) == expected["aggregationCheckCount"], "aggregation_check_count_mismatch")
    require(len(refs) == expected["requiredAggregationRefCount"], "required_aggregation_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "request_owner",
            "notification_owner",
            "receipt_owner",
            "receipt_aggregation_owner",
            "committee_secretariat",
            "committee_representative",
            "waes_gate_owner",
            "harness_reviewer",
            "acl_owner",
        },
        "aggregation_role",
    )
    require_all(
        sections,
        {
            "candidate_aggregation_header",
            "candidate_receipt_set_summary",
            "candidate_recipient_acknowledgement_rollup",
            "candidate_channel_receipt_rollup",
            "candidate_missing_receipt_snapshot",
            "candidate_dispatch_readiness_snapshot",
            "candidate_acknowledgement_route_snapshot",
            "candidate_acl_boundary_snapshot",
            "candidate_delivery_hold_conditions",
            "candidate_delivery_blocker_codes",
            "candidate_hold_context_refs_snapshot",
            "candidate_aggregation_integrity_check",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "aggregation_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "aggregation_preview_not_formal_receipt",
            "no_notification_receipt_aggregation_preview_execution",
            "no_notification_receipt_aggregation_execution",
            "no_notification_receipt_preview_execution",
            "no_notification_receipt_execution",
            "no_notification_execution",
            "no_acknowledgement_routing_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_harness_evidence_write",
        },
        "aggregation_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_notification_receipt_aggregation_preview",
            "execute_notification_receipt_aggregation",
            "execute_notification_receipt_preview",
            "execute_notification_receipt",
            "execute_notification",
            "execute_acknowledgement_routing",
            "execute_committee_acceptance",
            "execute_committee_acknowledgement",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    package_scope = evidence.get("package_scope", {})
    require(
        evidence.get("current_committee_acceptance_acknowledgement_notification_receipt_aggregation_preview_status")
        == expected["committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus"],
        "evidence_current_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(package_scope.get("aggregation_roles") == expected["aggregationRoleCount"], "evidence_role_count_mismatch")
    require(package_scope.get("aggregation_checks") == expected["aggregationCheckCount"], "evidence_check_count_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_ref_count_mismatch")
    require("candidate_preview_with_hold" in EVIDENCE_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_md")
    require("candidate_preview_with_hold" in LOOP_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_loop")

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_preview_current_state_d172=pass")
    print("committee_acceptance_acknowledgement_notification_receipt_aggregation_preview_status=candidate_preview_with_hold")
    print("maximum_state=review_ready_with_hold")
    print("preview_status=candidate_preview_with_hold")
    print("execution_status=not_executed")
    print("notification_receipt_aggregation_preview_execution_status=not_executed")
    print("notification_receipt_aggregation_execution_status=not_executed")
    print("notification_receipt_execution_status=not_executed")
    print(f"aggregation_roles={expected['aggregationRoleCount']}")
    print(f"aggregation_checks={expected['aggregationCheckCount']}")
    print(f"hold_context_refs={expected['holdContextRefCount']}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
