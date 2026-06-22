#!/usr/bin/env python3
"""Validate P0 acknowledgement receipt aggregation completeness precheck dry-run."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-repair-owner-notification-acknowledgement-receipt-aggregation-completeness-precheck-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require_all(actual: set[str], expected_values: set[str], label: str, failures: list[str]) -> None:
    for value in expected_values:
        if value not in actual:
            failures.append(f"missing {label}: {value}")


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    source_data = load_json(data["sourceAcknowledgementReceiptAggregationPreview"])
    source = source_data["acknowledgementReceiptAggregationPreview"]
    precheck = data["acknowledgementReceiptAggregationCompletenessPrecheck"]
    failures: list[str] = []

    if data.get("acknowledgementReceiptAggregationCompletenessPrecheckStatus") != expected["acknowledgementReceiptAggregationCompletenessPrecheckStatus"]:
        failures.append("completeness precheck status must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalCompletenessPrecheck") is not expected["notFinalCompletenessPrecheck"]:
        failures.append("precheck must state notFinalCompletenessPrecheck=true")
    if precheck.get("precheckStatus") != expected["precheckStatus"]:
        failures.append("precheckStatus must remain candidate_preview")
    if precheck.get("executionMode") != expected["executionMode"]:
        failures.append("precheck executionMode mismatch")
    if precheck.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("precheck must remain dryRunOnly=true")

    for key in (
        "completenessPrecheckExecutionStatus",
        "aggregationPreviewExecutionStatus",
        "acknowledgementReceiptAggregationExecutionStatus",
        "acknowledgementReceiptExecutionStatus",
        "repairOwnerResponsibilityConfirmationStatus",
        "repairOwnerNotificationExecutionStatus",
        "routingDeliveryExecutionStatus",
        "recipientNotificationExecutionStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if precheck.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("acknowledgementReceiptAggregationPreviewStatus") != expected["sourceAcknowledgementReceiptAggregationPreviewStatus"]:
        failures.append("source aggregation preview must remain candidate_preview")
    source_status_map = {
        "aggregationPreviewExecutionStatus": "sourceAggregationPreviewExecutionStatus",
        "acknowledgementReceiptExecutionStatus": "sourceAcknowledgementReceiptExecutionStatus",
        "repairOwnerResponsibilityConfirmationStatus": "sourceRepairOwnerResponsibilityConfirmationStatus",
        "repairRequestCreationStatus": "sourceRepairRequestCreationStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source aggregation preview must remain dryRunOnly=true")
    if precheck.get("sourceAcknowledgementReceiptAggregationPreviewId") != source.get("id"):
        failures.append("sourceAcknowledgementReceiptAggregationPreviewId must match D81 aggregation preview id")
    if data.get("coveredAcknowledgementReceiptAggregationPreviewStatus") != source.get("previewStatus"):
        failures.append("covered aggregation preview status must match D81 status")

    count_checks = {
        "precheckRoles": "precheckRoleCount",
        "completenessSections": "completenessSectionCount",
        "requiredCompletenessFields": "requiredCompletenessFieldCount",
        "precheckCriteria": "precheckCriteriaCount",
        "precheckConstraints": "precheckConstraintCount",
        "precheckChecks": "precheckCheckCount",
        "requiredCompletenessRefs": "requiredCompletenessRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(precheck.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(set(precheck.get("completenessSections", [])), {
        "candidate_aggregation_scope_completeness",
        "candidate_receipt_batch_identity_completeness",
        "candidate_receipt_deduplication_key_completeness",
        "candidate_receipt_status_matrix_completeness",
        "candidate_receipt_blocker_code_completeness",
        "waes_negative_gate_completeness",
        "harness_no_write_guard_completeness",
        "no_write_attestation",
    }, "completeness section", failures)
    require_all(set(precheck.get("precheckConstraints", [])), {
        "candidate_preview_only",
        "precheck_not_formal_completeness_result",
        "no_completeness_precheck_execution",
        "no_acknowledgement_receipt_aggregation_execution",
        "no_acknowledgement_receipt_execution",
        "no_repair_owner_responsibility_confirmation",
        "no_repair_request_creation",
        "no_committee_case_opening",
        "no_harness_evidence_write",
        "no_business_write",
    }, "precheck constraint", failures)
    require_all(set(precheck.get("forbiddenActions", [])), {
        "execute_completeness_precheck",
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
        "executesCompletenessPrecheck",
        "executesAcknowledgementReceiptAggregationPreview",
        "executesAcknowledgementReceiptAggregation",
        "executesAcknowledgementReceipt",
        "sendsRepairOwnerNotification",
        "executesRoutingDelivery",
        "sendsRecipientNotification",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_aggregation_completeness_precheck_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_repair_owner_notification_acknowledgement_receipt_aggregation_completeness_precheck_dry_run=pass")
    print(f"status={precheck['precheckStatus']}")
    print(f"execution_mode={precheck['executionMode']}")
    print("executes_completeness_precheck=0")
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
