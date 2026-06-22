#!/usr/bin/env python3
"""Validate P0 committee acceptance acknowledgement notification receipt aggregation preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-preview-dry-run-v0.1.json"
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
    failures: list[str] = []
    source_data = load_json(data["sourceCommitteeAcceptanceAcknowledgementNotificationReceiptPreview"])
    source = source_data["committeeAcceptanceAcknowledgementNotificationReceiptPreview"]
    aggregation = data["committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreview"]

    if data.get("committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus") != expected[
        "committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus"
    ]:
        failures.append("committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalCommitteeAcceptanceAcknowledgementNotificationReceiptAggregation") is not expected[
        "notFinalCommitteeAcceptanceAcknowledgementNotificationReceiptAggregation"
    ]:
        failures.append("receipt aggregation preview must state notFinalCommitteeAcceptanceAcknowledgementNotificationReceiptAggregation=true")
    if aggregation.get("previewType") != expected["previewType"]:
        failures.append("committee acceptance acknowledgement notification receipt aggregation previewType mismatch")
    if aggregation.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee acceptance acknowledgement notification receipt aggregation previewStatus must remain candidate_preview")
    if aggregation.get("executionMode") != expected["executionMode"]:
        failures.append("committee acceptance acknowledgement notification receipt aggregation executionMode mismatch")
    if aggregation.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee acceptance acknowledgement notification receipt aggregation must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "notificationReceiptAggregationPreviewExecutionStatus",
        "notificationReceiptAggregationExecutionStatus",
        "notificationReceiptExecutionStatus",
        "notificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "envelopeAssemblyExecutionStatus",
        "committeeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if aggregation.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("committeeAcceptanceAcknowledgementNotificationReceiptPreviewStatus") != expected[
        "sourceCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewStatus"
    ]:
        failures.append("source notification receipt preview must remain candidate_preview")
    source_status_map = {
        "notificationReceiptPreviewExecutionStatus": "sourceNotificationReceiptPreviewExecutionStatus",
        "notificationReceiptExecutionStatus": "sourceNotificationReceiptExecutionStatus",
        "notificationExecutionStatus": "sourceNotificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus": "sourceAcknowledgementRoutingExecutionStatus",
        "committeeAcceptanceExecutionStatus": "sourceCommitteeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus": "sourceCommitteeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source notification receipt preview must remain dryRunOnly=true")
    if aggregation.get("sourceCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewId") != source.get("id"):
        failures.append("sourceCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewId must match D71 preview id")
    if data.get("coveredCommitteeAcceptanceAcknowledgementNotificationReceiptPreviewStatus") != source.get("previewStatus"):
        failures.append("covered receipt status must match D71 preview status")

    count_checks = {
        "aggregationRoles": "aggregationRoleCount",
        "aggregationSections": "aggregationSectionCount",
        "candidateAggregationFields": "candidateAggregationFieldCount",
        "aggregationReadinessPrerequisites": "aggregationReadinessPrerequisiteCount",
        "aggregationDecisionConstraints": "aggregationDecisionConstraintCount",
        "aggregationChecks": "aggregationCheckCount",
        "requiredAggregationRefs": "requiredAggregationRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(aggregation.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(aggregation.get("aggregationSections", [])),
        {
            "candidate_aggregation_header",
            "candidate_receipt_set_summary",
            "candidate_recipient_acknowledgement_rollup",
            "candidate_channel_receipt_rollup",
            "candidate_missing_receipt_snapshot",
            "candidate_acl_boundary_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "committee acceptance acknowledgement notification receipt aggregation section",
        failures,
    )
    require_all(
        set(aggregation.get("aggregationDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "aggregation_preview_not_formal_receipt",
            "no_notification_receipt_aggregation_preview_execution",
            "no_notification_receipt_aggregation_execution",
            "no_notification_receipt_execution",
            "no_notification_execution",
            "no_committee_acceptance_execution",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "committee acceptance acknowledgement notification receipt aggregation constraint",
        failures,
    )
    require_all(
        set(aggregation.get("forbiddenActions", [])),
        {
            "execute_notification_receipt_aggregation_preview",
            "execute_notification_receipt_aggregation",
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
        "forbidden action",
        failures,
    )
    for relative_path in data.get("requiredSourceRefs", []):
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")
    for key in (
        "executesNotificationReceiptAggregationPreview",
        "executesNotificationReceiptAggregation",
        "executesNotificationReceipt",
        "executesNotification",
        "executesAcknowledgementRouting",
        "executesEnvelopeAssembly",
        "executesCommitteeAcceptancePrecheck",
        "executesCommitteeAcceptance",
        "executesCommitteeAcknowledgement",
        "opensCommitteeCase",
        "executesCommitteeDecision",
        "executesHumanConfirmation",
        "releasesFreeze",
        "executesUnfreeze",
        "executesIntakeGuard",
        "executesRoutingPackage",
        "executesRouting",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_preview_dry_run=pass")
    print(f"status={aggregation['previewStatus']}")
    print(f"execution_mode={aggregation['executionMode']}")
    print("executes_notification_receipt_aggregation_preview=0")
    print("executes_notification_receipt_aggregation=0")
    print("executes_notification_receipt=0")
    print("executes_notification=0")
    print("executes_acknowledgement_routing=0")
    print("executes_committee_acceptance=0")
    print("executes_committee_acknowledgement=0")
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
