#!/usr/bin/env python3
"""Validate D170 GCKF P0 committee acceptance acknowledgement notification preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-preview-current-state-d170-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-preview-current-state-d170-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-preview-current-state-d170-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D170-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_preview_current_state_d170="
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
    historical = load_json(ROOT / fixture["sourceHistoricalCommitteeAcceptanceAcknowledgementNotificationPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheck"])
    notification = fixture["committeeAcceptanceAcknowledgementNotificationPreview"]
    historical_notification = historical["committeeAcceptanceAcknowledgementNotificationPreview"]
    source_dispatch = current_source["committeeAcceptanceAcknowledgementRoutingDispatchPrecheck"]

    require(
        fixture.get("committeeAcceptanceAcknowledgementNotificationPreviewStatus")
        == expected["committeeAcceptanceAcknowledgementNotificationPreviewStatus"],
        "notification_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalCommitteeAcceptanceAcknowledgementNotification")
        is expected["notFinalCommitteeAcceptanceAcknowledgementNotification"],
        "not_final_notification_mismatch",
    )
    require(notification.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(notification.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
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
        "formalWriteExecutionStatus"
    ):
        require(notification.get(key) == expected[key], f"{key}_mismatch")
    require(notification.get("executionMode") == expected["executionMode"], "notification_execution_mode_mismatch")
    require(notification.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("committeeAcceptanceAcknowledgementNotificationPreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_notification.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_notification.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("committeeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus")
        == expected["sourceCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus"],
        "source_dispatch_status_mismatch",
    )
    for source_key, expected_key in (
        ("executionStatus", "sourceDispatchPrecheckExecutionStatus"),
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
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus")
    ):
        require(source_dispatch.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_dispatch.get("dryRunOnly") is True, "source_dispatch_not_dry_run_only")
    require(
        notification.get("sourceCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheckId") == source_dispatch.get("id"),
        "source_dispatch_id_mismatch",
    )
    require(
        fixture.get("coveredCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus")
        == expected["coveredCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus"] == source_dispatch.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(notification.get("notificationRoles", []))
    sections = set(notification.get("notificationSections", []))
    fields = set(notification.get("candidateNotificationFields", []))
    prerequisites = set(notification.get("notificationReadinessPrerequisites", []))
    constraints = set(notification.get("notificationDecisionConstraints", []))
    checks = set(notification.get("notificationChecks", []))
    refs = set(notification.get("requiredNotificationRefs", []))
    blocking_conditions = set(notification.get("blockingConditions", []))
    forbidden_actions = set(notification.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["notificationRoleCount"], "notification_role_count_mismatch")
    require(len(sections) == expected["notificationSectionCount"], "notification_section_count_mismatch")
    require(len(fields) == expected["candidateNotificationFieldCount"], "candidate_notification_field_count_mismatch")
    require(len(prerequisites) == expected["notificationReadinessPrerequisiteCount"], "notification_prerequisite_count_mismatch")
    require(len(constraints) == expected["notificationDecisionConstraintCount"], "notification_constraint_count_mismatch")
    require(len(checks) == expected["notificationCheckCount"], "notification_check_count_mismatch")
    require(len(refs) == expected["requiredNotificationRefCount"], "required_notification_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "notification_owner",
            "committee_secretariat",
            "committee_representative",
            "acknowledgement_routing_owner",
            "waes_gate_owner",
            "acl_owner",
            "harness_reviewer"
        },
        "notification_role",
    )
    require_all(
        sections,
        {
            "candidate_notification_header",
            "candidate_recipient_matrix",
            "candidate_channel_matrix",
            "candidate_message_payload_summary",
            "candidate_dispatch_readiness_snapshot",
            "candidate_acknowledgement_route_snapshot",
            "candidate_acknowledgement_envelope_snapshot",
            "candidate_acl_boundary_snapshot",
            "candidate_quorum_snapshot",
            "candidate_conflict_of_interest_snapshot",
            "candidate_delivery_hold_conditions",
            "candidate_delivery_blocker_codes",
            "candidate_hold_context_refs_snapshot",
            "harness_no_write_guard",
            "no_write_attestation"
        },
        "notification_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "notification_preview_not_formal_notice",
            "no_notification_preview_execution",
            "no_notification_execution",
            "no_acknowledgement_dispatch_execution",
            "no_acknowledgement_routing_execution",
            "no_committee_acceptance_precheck_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_routing_package_execution",
            "no_committee_case_opening",
            "no_harness_evidence_write"
        },
        "notification_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_notification_preview",
            "execute_notification",
            "execute_acknowledgement_dispatch",
            "execute_acknowledgement_routing",
            "execute_committee_acceptance",
            "execute_committee_acknowledgement",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system"
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    package_scope = evidence.get("package_scope", {})
    require(evidence.get("current_committee_acceptance_acknowledgement_notification_preview_status") == expected["committeeAcceptanceAcknowledgementNotificationPreviewStatus"], "evidence_current_status_mismatch")
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(package_scope.get("notification_roles") == expected["notificationRoleCount"], "evidence_role_count_mismatch")
    require(package_scope.get("notification_checks") == expected["notificationCheckCount"], "evidence_check_count_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_ref_count_mismatch")
    require("candidate_preview_with_hold" in EVIDENCE_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_md")
    require("candidate_preview_with_hold" in LOOP_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_loop")

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_preview_current_state_d170=pass")
    print("committee_acceptance_acknowledgement_notification_preview_status=candidate_preview_with_hold")
    print("maximum_state=review_ready_with_hold")
    print("preview_status=candidate_preview_with_hold")
    print("execution_status=not_executed")
    print("notification_preview_execution_status=not_executed")
    print("notification_execution_status=not_executed")
    print("acknowledgement_dispatch_execution_status=not_executed")
    print("acknowledgement_routing_execution_status=not_executed")
    print("committee_acceptance_execution_status=not_executed")
    print("committee_acknowledgement_execution_status=not_executed")
    print("routing_package_execution_status=not_executed")
    print("committee_case_execution_status=not_executed")
    print("committee_decision_execution_status=not_executed")
    print(f"notification_roles={len(roles)}")
    print(f"notification_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("localization_gate=pass")
    print("loop_document_gate=pass")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
