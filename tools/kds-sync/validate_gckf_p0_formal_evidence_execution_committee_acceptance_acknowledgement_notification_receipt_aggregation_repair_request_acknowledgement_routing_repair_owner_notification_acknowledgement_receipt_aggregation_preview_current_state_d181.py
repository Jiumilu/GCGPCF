#!/usr/bin/env python3
"""Validate D181 GCKF P0 acknowledgement receipt aggregation preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-preview-current-state-d181-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-preview-current-state-d181-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-preview-current-state-d181-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D181-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_aggregation_preview_current_state_d181="
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
    historical = load_json(ROOT / fixture["sourceHistoricalAcknowledgementReceiptAggregationPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentAcknowledgementReceiptPreview"])
    preview = fixture["acknowledgementReceiptAggregationPreview"]
    historical_preview = historical["acknowledgementReceiptAggregationPreview"]
    source_preview = current_source["repairOwnerNotificationAcknowledgementReceiptPreview"]

    require(
        fixture.get("acknowledgementReceiptAggregationPreviewStatus")
        == expected["acknowledgementReceiptAggregationPreviewStatus"],
        "aggregation_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalAcknowledgementReceiptAggregation")
        is expected["notFinalAcknowledgementReceiptAggregation"],
        "not_final_aggregation_mismatch",
    )
    require(preview.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(preview.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "aggregationPreviewExecutionStatus",
        "aggregationExecutionStatus",
        "acknowledgementReceiptPreviewExecutionStatus",
        "acknowledgementReceiptExecutionStatus",
        "repairOwnerResponsibilityConfirmationExecutionStatus",
        "repairOwnerNotificationPreviewExecutionStatus",
        "repairOwnerNotificationExecutionStatus",
        "routingDeliveryPrecheckExecutionStatus",
        "routingDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus",
        "recipientAcknowledgementExecutionStatus",
        "acknowledgementRoutingPreviewExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "intakeAcknowledgementExecutionStatus",
        "repairRequestCompletenessPrecheckPreviewExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus",
        "repairIntakePreviewExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        require(preview.get(key) == "not_executed", f"{key}_mismatch")

    require(preview.get("executionMode") == expected["executionMode"], "preview_execution_mode_mismatch")
    require(preview.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("acknowledgementReceiptAggregationPreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_preview.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(
        historical_preview.get("aggregationPreviewExecutionStatus") == "not_executed",
        "historical_execution_status_mismatch",
    )

    require(
        current_source.get("repairOwnerNotificationAcknowledgementReceiptPreviewStatus")
        == expected["sourceAcknowledgementReceiptPreviewStatus"],
        "source_preview_status_mismatch",
    )
    for source_key, expected_key in (
        ("acknowledgementReceiptPreviewExecutionStatus", "sourceAcknowledgementReceiptPreviewExecutionStatus"),
        ("acknowledgementReceiptExecutionStatus", "sourceAcknowledgementReceiptExecutionStatus"),
        ("repairOwnerResponsibilityConfirmationExecutionStatus", "sourceRepairOwnerResponsibilityConfirmationExecutionStatus"),
        ("repairOwnerNotificationPreviewExecutionStatus", "sourceRepairOwnerNotificationPreviewExecutionStatus"),
        ("repairOwnerNotificationExecutionStatus", "sourceRepairOwnerNotificationExecutionStatus"),
        ("routingDeliveryPrecheckExecutionStatus", "sourceRoutingDeliveryPrecheckExecutionStatus"),
        ("routingDeliveryExecutionStatus", "sourceRoutingDeliveryExecutionStatus"),
        ("recipientNotificationExecutionStatus", "sourceRecipientNotificationExecutionStatus"),
        ("recipientAcknowledgementExecutionStatus", "sourceRecipientAcknowledgementExecutionStatus"),
        ("acknowledgementRoutingPreviewExecutionStatus", "sourceAcknowledgementRoutingPreviewExecutionStatus"),
        ("acknowledgementRoutingExecutionStatus", "sourceAcknowledgementRoutingExecutionStatus"),
        ("intakeAcknowledgementExecutionStatus", "sourceIntakeAcknowledgementExecutionStatus"),
        (
            "repairRequestCompletenessPrecheckPreviewExecutionStatus",
            "sourceRepairRequestCompletenessPrecheckPreviewExecutionStatus",
        ),
        (
            "repairRequestCompletenessPrecheckExecutionStatus",
            "sourceRepairRequestCompletenessPrecheckExecutionStatus",
        ),
        ("repairIntakePreviewExecutionStatus", "sourceRepairIntakePreviewExecutionStatus"),
        ("repairIntakeExecutionStatus", "sourceRepairIntakeExecutionStatus"),
        ("repairRequestCreationStatus", "sourceRepairRequestCreationStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_preview.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_preview.get("dryRunOnly") is True, "source_preview_not_dry_run_only")
    require(
        preview.get("sourceAcknowledgementReceiptPreviewId") == source_preview.get("id"),
        "source_preview_id_mismatch",
    )
    require(
        fixture.get("coveredAcknowledgementReceiptPreviewStatus")
        == expected["coveredAcknowledgementReceiptPreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredAcknowledgementReceiptPreviewStatus"] == source_preview.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(preview.get("aggregationRoles", []))
    sections = set(preview.get("aggregationSections", []))
    fields = set(preview.get("candidateAggregationFields", []))
    prerequisites = set(preview.get("aggregationPrerequisites", []))
    constraints = set(preview.get("aggregationConstraints", []))
    checks = set(preview.get("aggregationChecks", []))
    refs = set(preview.get("requiredAggregationRefs", []))
    blocking_conditions = set(preview.get("blockingConditions", []))
    forbidden_actions = set(preview.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["aggregationRoleCount"], "aggregation_role_count_mismatch")
    require(len(sections) == expected["aggregationSectionCount"], "aggregation_section_count_mismatch")
    require(len(fields) == expected["candidateAggregationFieldCount"], "aggregation_field_count_mismatch")
    require(len(prerequisites) == expected["aggregationPrerequisiteCount"], "aggregation_prerequisite_count_mismatch")
    require(len(constraints) == expected["aggregationConstraintCount"], "aggregation_constraint_count_mismatch")
    require(len(checks) == expected["aggregationCheckCount"], "aggregation_check_count_mismatch")
    require(len(refs) == expected["requiredAggregationRefCount"], "aggregation_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(
        len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"],
        "required_source_ref_count_mismatch",
    )
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "repair_owner",
            "receipt_owner",
            "aggregation_owner",
            "routing_owner",
            "recipient_acl_owner",
            "sla_owner",
            "waes_gate_owner",
            "harness_reviewer",
            "governance_owner",
            "audit_owner",
        },
        "aggregation_role",
    )
    require_all(
        sections,
        {
            "candidate_receipt_aggregation_scope",
            "candidate_receipt_batch_identity",
            "candidate_receipt_deduplication_key",
            "candidate_receipt_channel_matrix",
            "candidate_repair_owner_identity_snapshot",
            "candidate_receipt_status_matrix",
            "candidate_hold_reason_snapshot",
            "candidate_hold_context_refs_snapshot",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
        },
        "aggregation_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_with_hold_only",
            "aggregation_preview_not_formal_receipt_aggregation",
            "no_aggregation_preview_execution",
            "no_aggregation_execution",
            "no_acknowledgement_receipt_preview_execution",
            "no_acknowledgement_receipt_execution",
            "no_repair_owner_responsibility_confirmation",
            "no_repair_request_creation",
            "no_committee_case_opening",
            "no_harness_evidence_write",
            "no_business_write",
        },
        "aggregation_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_acknowledgement_receipt_aggregation_preview",
            "execute_acknowledgement_receipt_aggregation",
            "execute_acknowledgement_receipt_preview",
            "execute_acknowledgement_receipt",
            "confirm_repair_owner_responsibility",
            "create_repair_request",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    require(
        evidence.get("current_acknowledgement_receipt_aggregation_preview_status")
        == expected["acknowledgementReceiptAggregationPreviewStatus"],
        "evidence_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(evidence.get("execution_mode") == "local_evidence_no_write", "evidence_execution_mode_mismatch")
    require(evidence.get("execution_status") == "not_executed", "evidence_execution_status_mismatch")

    package_scope = evidence.get("package_scope", {})
    require(package_scope.get("aggregation_roles") == expected["aggregationRoleCount"], "evidence_roles_mismatch")
    require(package_scope.get("aggregation_sections") == expected["aggregationSectionCount"], "evidence_sections_mismatch")
    require(
        package_scope.get("candidate_aggregation_fields") == expected["candidateAggregationFieldCount"],
        "evidence_fields_mismatch",
    )
    require(
        package_scope.get("aggregation_prerequisites") == expected["aggregationPrerequisiteCount"],
        "evidence_prerequisites_mismatch",
    )
    require(
        package_scope.get("aggregation_constraints") == expected["aggregationConstraintCount"],
        "evidence_constraints_mismatch",
    )
    require(package_scope.get("aggregation_checks") == expected["aggregationCheckCount"], "evidence_checks_mismatch")
    require(
        package_scope.get("required_aggregation_refs") == expected["requiredAggregationRefCount"],
        "evidence_refs_mismatch",
    )
    require(
        package_scope.get("blocking_conditions") == expected["blockingConditionCount"],
        "evidence_blocks_mismatch",
    )
    require(
        package_scope.get("forbidden_actions") == expected["forbiddenActionCount"],
        "evidence_forbidden_actions_mismatch",
    )
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_refs_mismatch")

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
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_aggregation_preview_current_state_d181=pass"
    )
    print(f"acknowledgement_receipt_aggregation_preview_status={fixture['acknowledgementReceiptAggregationPreviewStatus']}")
    print(f"maximum_state={fixture['maximumState']}")
    print(f"preview_status={preview['previewStatus']}")
    print(f"execution_status={preview['executionStatus']}")
    print(f"aggregation_roles={len(roles)}")
    print(f"aggregation_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
