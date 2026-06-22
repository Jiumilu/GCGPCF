#!/usr/bin/env python3
"""Validate P0 aggregation precheck repair request intake preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-precheck-repair-request-intake-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceAggregationCompletenessPrecheck"])
    source = source_data["aggregationCompletenessPrecheck"]
    intake = data["repairRequestIntakePreview"]

    if data.get("repairRequestIntakePreviewStatus") != expected["repairRequestIntakePreviewStatus"]:
        failures.append("repairRequestIntakePreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRepairRequestIntake") is not expected["notFinalRepairRequestIntake"]:
        failures.append("repair intake preview must state notFinalRepairRequestIntake=true")
    if intake.get("previewType") != expected["previewType"]:
        failures.append("repair intake previewType mismatch")
    if intake.get("previewStatus") != expected["previewStatus"]:
        failures.append("repair intake previewStatus must remain candidate_preview")
    if intake.get("executionMode") != expected["executionMode"]:
        failures.append("repair intake executionMode mismatch")
    if intake.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("repair intake must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "repairIntakePreviewExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "aggregationCompletenessPrecheckPreviewExecutionStatus",
        "aggregationCompletenessPrecheckExecutionStatus",
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
        if intake.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("aggregationCompletenessPrecheckStatus") != expected["sourceAggregationCompletenessPrecheckStatus"]:
        failures.append("source aggregation completeness precheck must remain candidate_preview")
    source_status_map = {
        "aggregationCompletenessPrecheckPreviewExecutionStatus": "sourcePrecheckPreviewExecutionStatus",
        "aggregationCompletenessPrecheckExecutionStatus": "sourcePrecheckExecutionStatus",
        "notificationReceiptAggregationExecutionStatus": "sourceAggregationExecutionStatus",
        "notificationReceiptExecutionStatus": "sourceReceiptExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source aggregation completeness precheck must remain dryRunOnly=true")
    if intake.get("sourceAggregationCompletenessPrecheckId") != source.get("id"):
        failures.append("sourceAggregationCompletenessPrecheckId must match D73 preview id")
    if data.get("coveredAggregationCompletenessPrecheckStatus") != source.get("previewStatus"):
        failures.append("covered aggregation completeness status must match D73 preview status")

    count_checks = {
        "repairIntakeRoles": "repairIntakeRoleCount",
        "repairIntakeSections": "repairIntakeSectionCount",
        "candidateRepairIntakeFields": "candidateRepairIntakeFieldCount",
        "repairIntakeReadinessPrerequisites": "repairIntakeReadinessPrerequisiteCount",
        "repairIntakeDecisionConstraints": "repairIntakeDecisionConstraintCount",
        "repairIntakeChecks": "repairIntakeCheckCount",
        "requiredRepairIntakeRefs": "requiredRepairIntakeRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(intake.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(intake.get("repairIntakeSections", [])),
        {
            "candidate_precheck_gap_reason_matrix",
            "candidate_required_receipt_material_matrix",
            "candidate_submitter_boundary",
            "candidate_intake_channel_matrix",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "repair intake section",
        failures,
    )
    require_all(
        set(intake.get("repairIntakeDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "repair_intake_preview_not_formal_intake",
            "no_repair_intake_preview_execution",
            "no_repair_intake_execution",
            "no_repair_request_creation",
            "no_completeness_precheck_execution",
            "no_notification_receipt_aggregation_execution",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "repair intake constraint",
        failures,
    )
    require_all(
        set(intake.get("forbiddenActions", [])),
        {
            "execute_repair_intake_preview",
            "execute_repair_intake",
            "create_repair_request",
            "execute_aggregation_completeness_precheck",
            "execute_notification_receipt_aggregation",
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
        "executesRepairIntakePreview",
        "executesRepairIntake",
        "createsRepairRequest",
        "executesAggregationCompletenessPrecheckPreview",
        "executesAggregationCompletenessPrecheck",
        "executesNotificationReceiptAggregation",
        "executesNotificationReceipt",
        "executesNotification",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_precheck_repair_request_intake_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_precheck_repair_request_intake_preview_dry_run=pass")
    print(f"status={intake['previewStatus']}")
    print(f"execution_mode={intake['executionMode']}")
    print("executes_repair_intake_preview=0")
    print("executes_repair_intake=0")
    print("creates_repair_request=0")
    print("executes_aggregation_completeness_precheck=0")
    print("executes_notification_receipt_aggregation=0")
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
