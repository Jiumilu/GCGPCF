#!/usr/bin/env python3
"""Validate P0 repair owner notification preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-preview-dry-run-v0.1.json"
)


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require_all(actual: set[str], expected_values: set[str], label: str, failures: list[str]) -> None:
    for value in expected_values:
        if value not in actual:
            failures.append(f"missing {label}: {value}")


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    source_data = load_json(data["sourceRoutingDeliveryPrecheck"])
    source = source_data["routingDeliveryPrecheck"]
    notification = data["repairOwnerNotificationPreview"]
    failures: list[str] = []

    if data.get("repairOwnerNotificationPreviewStatus") != expected["repairOwnerNotificationPreviewStatus"]:
        failures.append("repairOwnerNotificationPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRepairOwnerNotification") is not expected["notFinalRepairOwnerNotification"]:
        failures.append("notification must state notFinalRepairOwnerNotification=true")
    if notification.get("previewType") != expected["previewType"]:
        failures.append("repair owner notification previewType mismatch")
    if notification.get("previewStatus") != expected["previewStatus"]:
        failures.append("repair owner notification previewStatus must remain candidate_preview")
    if notification.get("executionMode") != expected["executionMode"]:
        failures.append("repair owner notification executionMode mismatch")
    if notification.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("repair owner notification must remain dryRunOnly=true")

    for key in (
        "repairOwnerNotificationPreviewExecutionStatus",
        "repairOwnerNotificationExecutionStatus",
        "routingDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus",
        "recipientAcknowledgementExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "intakeAcknowledgementExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if notification.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("routingDeliveryPrecheckStatus") != expected["sourceRoutingDeliveryPrecheckStatus"]:
        failures.append("source routing delivery precheck must remain candidate_preview")
    source_status_map = {
        "deliveryExecutionStatus": "sourceDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus": "sourceRecipientNotificationExecutionStatus",
        "recipientAcknowledgementExecutionStatus": "sourceRecipientAcknowledgementExecutionStatus",
        "repairOwnerNotificationExecutionStatus": "sourceRepairOwnerNotificationExecutionStatus",
        "repairRequestCreationStatus": "sourceRepairRequestCreationStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source routing delivery precheck must remain dryRunOnly=true")
    if notification.get("sourceRoutingDeliveryPrecheckId") != source.get("id"):
        failures.append("sourceRoutingDeliveryPrecheckId must match D78 delivery precheck id")
    if data.get("coveredRoutingDeliveryPrecheckStatus") != source.get("precheckStatus"):
        failures.append("covered routing delivery precheck status must match D78 status")

    count_checks = {
        "notificationPreviewRoles": "notificationPreviewRoleCount",
        "notificationPreviewSections": "notificationPreviewSectionCount",
        "candidateNotificationFields": "candidateNotificationFieldCount",
        "notificationReadinessPrerequisites": "notificationReadinessPrerequisiteCount",
        "notificationDecisionConstraints": "notificationDecisionConstraintCount",
        "notificationPreviewChecks": "notificationPreviewCheckCount",
        "requiredNotificationRefs": "requiredNotificationRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(notification.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(notification.get("notificationPreviewSections", [])),
        {
            "candidate_repair_owner_identity_scope",
            "candidate_notification_channel_matrix",
            "candidate_notification_payload_outline",
            "candidate_acl_redaction_boundary",
            "candidate_sla_window_hint",
            "candidate_response_requirement_hint",
            "candidate_notification_blocker_codes",
            "harness_no_write_guard",
            "no_notification_attestation",
            "no_write_attestation",
        },
        "repair owner notification section",
        failures,
    )
    require_all(
        set(notification.get("notificationDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "notification_preview_not_formal_notification",
            "no_repair_owner_notification_preview_execution",
            "no_repair_owner_notification_execution",
            "no_routing_delivery_execution",
            "no_recipient_notification_execution",
            "no_recipient_acknowledgement_execution",
            "no_repair_request_creation",
            "no_committee_case_opening",
            "no_harness_evidence_write",
            "no_business_write",
        },
        "repair owner notification constraint",
        failures,
    )
    require_all(
        set(notification.get("forbiddenActions", [])),
        {
            "execute_repair_owner_notification_preview",
            "send_repair_owner_notification",
            "execute_routing_delivery",
            "send_recipient_notification",
            "execute_recipient_acknowledgement",
            "create_repair_request",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
        },
        "forbidden action",
        failures,
    )
    for relative_path in data.get("requiredSourceRefs", []):
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")
    for key in (
        "executesRepairOwnerNotificationPreview",
        "sendsRepairOwnerNotification",
        "executesRoutingDelivery",
        "sendsRecipientNotification",
        "executesRecipientAcknowledgement",
        "executesAcknowledgementRouting",
        "executesIntakeAcknowledgement",
        "executesRepairRequestCompletenessPrecheck",
        "executesRepairIntake",
        "createsRepairRequest",
        "opensCommitteeCase",
        "executesCommitteeDecision",
        "executesHumanConfirmation",
        "writesKds",
        "writesBusinessSystem",
        "writesHarnessEvidence",
        "writesFormalEvidence",
        "writesRevenueDistribution",
        "writesContributionScore",
    ):
        if expected[key] is not False:
            failures.append(f"{key} must be false in expectedSummary")

    if failures:
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_preview_dry_run=pass")
    print(f"status={notification['previewStatus']}")
    print(f"execution_mode={notification['executionMode']}")
    print("executes_repair_owner_notification_preview=0")
    print("sends_repair_owner_notification=0")
    print("executes_routing_delivery=0")
    print("sends_recipient_notification=0")
    print("executes_recipient_acknowledgement=0")
    print("executes_acknowledgement_routing=0")
    print("executes_intake_acknowledgement=0")
    print("creates_repair_request=0")
    print("opens_committee_case=0")
    print("writes_kds=0")
    print("writes_business_system=0")
    print("writes_harness_evidence=0")
    print("writes_formal_evidence=0")
    print("writes_revenue_distribution=0")
    print("writes_contribution_score=0")
    print("no_write=covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
