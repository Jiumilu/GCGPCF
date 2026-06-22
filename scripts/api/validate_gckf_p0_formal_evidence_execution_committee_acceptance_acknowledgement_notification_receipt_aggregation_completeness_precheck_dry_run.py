#!/usr/bin/env python3
"""Validate P0 notification receipt aggregation completeness precheck dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-completeness-precheck-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceAggregationPreview"])
    source = source_data["committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreview"]
    precheck = data["aggregationCompletenessPrecheck"]
    failures: list[str] = []

    if data.get("aggregationCompletenessPrecheckStatus") != expected["aggregationCompletenessPrecheckStatus"]:
        failures.append("aggregationCompletenessPrecheckStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAggregationCompletenessPrecheck") is not expected["notFinalAggregationCompletenessPrecheck"]:
        failures.append("precheck must state notFinalAggregationCompletenessPrecheck=true")
    if precheck.get("previewType") != expected["previewType"]:
        failures.append("aggregation completeness precheck previewType mismatch")
    if precheck.get("previewStatus") != expected["previewStatus"]:
        failures.append("aggregation completeness precheck previewStatus must remain candidate_preview")
    if precheck.get("executionMode") != expected["executionMode"]:
        failures.append("aggregation completeness precheck executionMode mismatch")
    if precheck.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("aggregation completeness precheck must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "aggregationCompletenessPrecheckPreviewExecutionStatus",
        "aggregationCompletenessPrecheckExecutionStatus",
        "notificationReceiptAggregationPreviewExecutionStatus",
        "notificationReceiptAggregationExecutionStatus",
        "notificationReceiptExecutionStatus",
        "notificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "committeeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if precheck.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("committeeAcceptanceAcknowledgementNotificationReceiptAggregationPreviewStatus") != expected[
        "sourceAggregationPreviewStatus"
    ]:
        failures.append("source aggregation preview must remain candidate_preview")
    source_status_map = {
        "notificationReceiptAggregationPreviewExecutionStatus": "sourceAggregationPreviewExecutionStatus",
        "notificationReceiptAggregationExecutionStatus": "sourceAggregationExecutionStatus",
        "notificationReceiptExecutionStatus": "sourceReceiptExecutionStatus",
        "notificationExecutionStatus": "sourceNotificationExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source aggregation preview must remain dryRunOnly=true")
    if precheck.get("sourceAggregationPreviewId") != source.get("id"):
        failures.append("sourceAggregationPreviewId must match D72 aggregation preview id")
    if data.get("coveredAggregationPreviewStatus") != source.get("previewStatus"):
        failures.append("covered aggregation status must match D72 preview status")

    count_checks = {
        "precheckRoles": "precheckRoleCount",
        "precheckSections": "precheckSectionCount",
        "candidatePrecheckFields": "candidatePrecheckFieldCount",
        "precheckReadinessPrerequisites": "precheckReadinessPrerequisiteCount",
        "precheckDecisionConstraints": "precheckDecisionConstraintCount",
        "precheckChecks": "precheckCheckCount",
        "requiredPrecheckRefs": "requiredPrecheckRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(precheck.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(precheck.get("precheckSections", [])),
        {
            "candidate_receipt_set_completeness_matrix",
            "candidate_required_recipient_coverage",
            "candidate_channel_receipt_coverage",
            "candidate_missing_receipt_exception_list",
            "candidate_acl_boundary_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "aggregation completeness precheck section",
        failures,
    )
    require_all(
        set(precheck.get("precheckDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "precheck_not_formal_acceptance",
            "no_completeness_precheck_preview_execution",
            "no_completeness_precheck_execution",
            "no_notification_receipt_aggregation_execution",
            "no_notification_receipt_execution",
            "no_notification_execution",
            "no_committee_acceptance_execution",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "aggregation completeness precheck constraint",
        failures,
    )
    require_all(
        set(precheck.get("forbiddenActions", [])),
        {
            "execute_aggregation_completeness_precheck_preview",
            "execute_aggregation_completeness_precheck",
            "execute_notification_receipt_aggregation",
            "execute_notification_receipt",
            "execute_notification",
            "execute_committee_acceptance",
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
        "executesAggregationCompletenessPrecheckPreview",
        "executesAggregationCompletenessPrecheck",
        "executesNotificationReceiptAggregationPreview",
        "executesNotificationReceiptAggregation",
        "executesNotificationReceipt",
        "executesNotification",
        "executesAcknowledgementRouting",
        "executesCommitteeAcceptance",
        "executesCommitteeAcknowledgement",
        "opensCommitteeCase",
        "executesCommitteeDecision",
        "executesHumanConfirmation",
        "releasesFreeze",
        "executesUnfreeze",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_completeness_precheck_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_completeness_precheck_dry_run=pass")
    print(f"status={precheck['previewStatus']}")
    print(f"execution_mode={precheck['executionMode']}")
    print("executes_aggregation_completeness_precheck_preview=0")
    print("executes_aggregation_completeness_precheck=0")
    print("executes_notification_receipt_aggregation=0")
    print("executes_notification_receipt=0")
    print("executes_notification=0")
    print("executes_committee_acceptance=0")
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
