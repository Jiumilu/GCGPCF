#!/usr/bin/env python3
"""Validate P0 repair owner notification acknowledgement receipt preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-preview-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require_all(actual: set[str], expected_values: set[str], label: str, failures: list[str]) -> None:
    for value in expected_values:
        if value not in actual:
            failures.append(f"missing {label}: {value}")


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    source_data = load_json(data["sourceRepairOwnerNotificationPreview"])
    source = source_data["repairOwnerNotificationPreview"]
    receipt = data["repairOwnerNotificationAcknowledgementReceiptPreview"]
    failures: list[str] = []

    if data.get("repairOwnerNotificationAcknowledgementReceiptPreviewStatus") != expected["repairOwnerNotificationAcknowledgementReceiptPreviewStatus"]:
        failures.append("receipt preview status must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRepairOwnerAcknowledgementReceipt") is not expected["notFinalRepairOwnerAcknowledgementReceipt"]:
        failures.append("receipt must state notFinalRepairOwnerAcknowledgementReceipt=true")
    if receipt.get("previewStatus") != expected["previewStatus"]:
        failures.append("receipt previewStatus must remain candidate_preview")
    if receipt.get("executionMode") != expected["executionMode"]:
        failures.append("receipt executionMode mismatch")
    if receipt.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("receipt preview must remain dryRunOnly=true")

    for key in (
        "acknowledgementReceiptPreviewExecutionStatus",
        "acknowledgementReceiptExecutionStatus",
        "repairOwnerNotificationExecutionStatus",
        "routingDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus",
        "recipientAcknowledgementExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "intakeAcknowledgementExecutionStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if receipt.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("repairOwnerNotificationPreviewStatus") != expected["sourceRepairOwnerNotificationPreviewStatus"]:
        failures.append("source repair owner notification preview must remain candidate_preview")
    source_status_map = {
        "repairOwnerNotificationExecutionStatus": "sourceRepairOwnerNotificationExecutionStatus",
        "routingDeliveryExecutionStatus": "sourceRoutingDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus": "sourceRecipientNotificationExecutionStatus",
        "recipientAcknowledgementExecutionStatus": "sourceRecipientAcknowledgementExecutionStatus",
        "repairRequestCreationStatus": "sourceRepairRequestCreationStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source repair owner notification preview must remain dryRunOnly=true")
    if receipt.get("sourceRepairOwnerNotificationPreviewId") != source.get("id"):
        failures.append("sourceRepairOwnerNotificationPreviewId must match D79 notification preview id")
    if data.get("coveredRepairOwnerNotificationPreviewStatus") != source.get("previewStatus"):
        failures.append("covered repair owner notification preview status must match D79 status")

    count_checks = {
        "acknowledgementReceiptRoles": "acknowledgementReceiptRoleCount",
        "acknowledgementReceiptSections": "acknowledgementReceiptSectionCount",
        "candidateAcknowledgementReceiptFields": "candidateAcknowledgementReceiptFieldCount",
        "acknowledgementReceiptPrerequisites": "acknowledgementReceiptPrerequisiteCount",
        "acknowledgementReceiptConstraints": "acknowledgementReceiptConstraintCount",
        "acknowledgementReceiptChecks": "acknowledgementReceiptCheckCount",
        "requiredAcknowledgementReceiptRefs": "requiredAcknowledgementReceiptRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(receipt.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(set(receipt.get("acknowledgementReceiptSections", [])), {
        "candidate_acknowledgement_receipt_scope",
        "candidate_receipt_channel_matrix",
        "candidate_repair_owner_identity_snapshot",
        "candidate_acknowledgement_payload_outline",
        "candidate_acl_redaction_boundary",
        "candidate_receipt_blocker_codes",
        "harness_no_write_guard",
        "no_write_attestation",
    }, "acknowledgement receipt section", failures)
    require_all(set(receipt.get("acknowledgementReceiptConstraints", [])), {
        "candidate_preview_only",
        "receipt_preview_not_formal_acknowledgement",
        "no_acknowledgement_receipt_preview_execution",
        "no_acknowledgement_receipt_execution",
        "no_repair_owner_notification_execution",
        "no_routing_delivery_execution",
        "no_recipient_notification_execution",
        "no_repair_request_creation",
        "no_committee_case_opening",
        "no_harness_evidence_write",
        "no_business_write",
    }, "acknowledgement receipt constraint", failures)
    require_all(set(receipt.get("forbiddenActions", [])), {
        "execute_acknowledgement_receipt_preview",
        "execute_acknowledgement_receipt",
        "send_repair_owner_notification",
        "execute_routing_delivery",
        "send_recipient_notification",
        "confirm_repair_owner_responsibility",
        "create_repair_request",
        "open_committee_case",
        "write_harness_evidence",
        "write_kds",
        "write_business_system",
    }, "forbidden action", failures)
    for relative_path in data.get("requiredSourceRefs", []):
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")
    for key in (
        "executesAcknowledgementReceiptPreview",
        "executesAcknowledgementReceipt",
        "sendsRepairOwnerNotification",
        "executesRoutingDelivery",
        "sendsRecipientNotification",
        "executesRecipientAcknowledgement",
        "confirmsRepairOwnerResponsibility",
        "createsRepairRequest",
        "opensCommitteeCase",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_preview_dry_run=pass")
    print(f"status={receipt['previewStatus']}")
    print(f"execution_mode={receipt['executionMode']}")
    print("executes_acknowledgement_receipt_preview=0")
    print("executes_acknowledgement_receipt=0")
    print("sends_repair_owner_notification=0")
    print("executes_routing_delivery=0")
    print("sends_recipient_notification=0")
    print("confirms_repair_owner_responsibility=0")
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
