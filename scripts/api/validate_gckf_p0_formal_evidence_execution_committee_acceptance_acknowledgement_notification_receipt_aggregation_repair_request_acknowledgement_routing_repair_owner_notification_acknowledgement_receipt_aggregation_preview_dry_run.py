#!/usr/bin/env python3
"""Validate P0 repair owner notification acknowledgement receipt aggregation preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-preview-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require_all(actual: set[str], expected_values: set[str], label: str, failures: list[str]) -> None:
    for value in expected_values:
        if value not in actual:
            failures.append(f"missing {label}: {value}")


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    source_data = load_json(data["sourceAcknowledgementReceiptPreview"])
    source = source_data["repairOwnerNotificationAcknowledgementReceiptPreview"]
    aggregation = data["acknowledgementReceiptAggregationPreview"]
    failures: list[str] = []

    if data.get("acknowledgementReceiptAggregationPreviewStatus") != expected["acknowledgementReceiptAggregationPreviewStatus"]:
        failures.append("aggregation preview status must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcknowledgementReceiptAggregation") is not expected["notFinalAcknowledgementReceiptAggregation"]:
        failures.append("aggregation must state notFinalAcknowledgementReceiptAggregation=true")
    if aggregation.get("previewStatus") != expected["previewStatus"]:
        failures.append("aggregation previewStatus must remain candidate_preview")
    if aggregation.get("executionMode") != expected["executionMode"]:
        failures.append("aggregation executionMode mismatch")
    if aggregation.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("aggregation preview must remain dryRunOnly=true")

    for key in (
        "aggregationPreviewExecutionStatus",
        "acknowledgementReceiptPreviewExecutionStatus",
        "acknowledgementReceiptExecutionStatus",
        "repairOwnerNotificationExecutionStatus",
        "routingDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus",
        "repairOwnerResponsibilityConfirmationStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if aggregation.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("repairOwnerNotificationAcknowledgementReceiptPreviewStatus") != expected["sourceAcknowledgementReceiptPreviewStatus"]:
        failures.append("source acknowledgement receipt preview must remain candidate_preview")
    source_status_map = {
        "acknowledgementReceiptPreviewExecutionStatus": "sourceAcknowledgementReceiptPreviewExecutionStatus",
        "acknowledgementReceiptExecutionStatus": "sourceAcknowledgementReceiptExecutionStatus",
        "repairOwnerNotificationExecutionStatus": "sourceRepairOwnerNotificationExecutionStatus",
        "routingDeliveryExecutionStatus": "sourceRoutingDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus": "sourceRecipientNotificationExecutionStatus",
        "repairRequestCreationStatus": "sourceRepairRequestCreationStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source acknowledgement receipt preview must remain dryRunOnly=true")
    if aggregation.get("sourceAcknowledgementReceiptPreviewId") != source.get("id"):
        failures.append("sourceAcknowledgementReceiptPreviewId must match D80 receipt preview id")
    if data.get("coveredAcknowledgementReceiptPreviewStatus") != source.get("previewStatus"):
        failures.append("covered acknowledgement receipt preview status must match D80 status")

    count_checks = {
        "aggregationRoles": "aggregationRoleCount",
        "aggregationSections": "aggregationSectionCount",
        "candidateAggregationFields": "candidateAggregationFieldCount",
        "aggregationPrerequisites": "aggregationPrerequisiteCount",
        "aggregationConstraints": "aggregationConstraintCount",
        "aggregationChecks": "aggregationCheckCount",
        "requiredAggregationRefs": "requiredAggregationRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(aggregation.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(set(aggregation.get("aggregationSections", [])), {
        "candidate_receipt_aggregation_scope",
        "candidate_receipt_batch_identity",
        "candidate_receipt_deduplication_key",
        "candidate_receipt_status_matrix",
        "candidate_receipt_blocker_codes",
        "waes_negative_gate_snapshot",
        "harness_no_write_guard",
        "no_write_attestation",
    }, "aggregation section", failures)
    require_all(set(aggregation.get("aggregationConstraints", [])), {
        "candidate_preview_only",
        "aggregation_preview_not_formal_receipt_aggregation",
        "no_aggregation_preview_execution",
        "no_acknowledgement_receipt_execution",
        "no_repair_owner_responsibility_confirmation",
        "no_repair_request_creation",
        "no_committee_case_opening",
        "no_harness_evidence_write",
        "no_business_write",
    }, "aggregation constraint", failures)
    require_all(set(aggregation.get("forbiddenActions", [])), {
        "execute_acknowledgement_receipt_aggregation_preview",
        "execute_acknowledgement_receipt_aggregation",
        "execute_acknowledgement_receipt",
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
        "executesAcknowledgementReceiptAggregationPreview",
        "executesAcknowledgementReceiptAggregation",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_aggregation_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_aggregation_preview_dry_run=pass")
    print(f"status={aggregation['previewStatus']}")
    print(f"execution_mode={aggregation['executionMode']}")
    print("executes_acknowledgement_receipt_aggregation_preview=0")
    print("executes_acknowledgement_receipt_aggregation=0")
    print("executes_acknowledgement_receipt=0")
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
