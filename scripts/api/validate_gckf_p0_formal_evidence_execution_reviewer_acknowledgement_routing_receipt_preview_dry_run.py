#!/usr/bin/env python3
"""Validate P0 reviewer acknowledgement routing receipt preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-reviewer-acknowledgement-routing-receipt-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceReviewerAssignmentAcknowledgementPreview"])
    source = source_data["reviewerAssignmentAcknowledgementPreview"]
    receipt = data["reviewerAcknowledgementRoutingReceiptPreview"]

    if data.get("reviewerAcknowledgementRoutingReceiptPreviewStatus") != expected[
        "reviewerAcknowledgementRoutingReceiptPreviewStatus"
    ]:
        failures.append("reviewerAcknowledgementRoutingReceiptPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRoutingReceipt") is not expected["notFinalRoutingReceipt"]:
        failures.append("routing receipt preview must state notFinalRoutingReceipt=true")
    if receipt.get("previewType") != expected["previewType"]:
        failures.append("routing receipt previewType mismatch")
    if receipt.get("previewStatus") != expected["previewStatus"]:
        failures.append("routing receipt previewStatus must remain candidate_preview")
    if receipt.get("executionMode") != expected["executionMode"]:
        failures.append("routing receipt preview executionMode mismatch")
    if receipt.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("routing receipt preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "routingReceiptExecutionStatus",
        "assignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus",
        "routingPrecheckExecutionStatus",
        "routingExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if receipt.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("reviewerAssignmentAcknowledgementPreviewStatus") != expected[
        "sourceReviewerAssignmentAcknowledgementPreviewStatus"
    ]:
        failures.append("source reviewer assignment acknowledgement preview must remain candidate_preview")
    source_status_map = {
        "assignmentAcknowledgementExecutionStatus": "sourceAssignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus": "sourceReviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus": "sourceReviewerAssignmentExecutionStatus",
        "routingPrecheckExecutionStatus": "sourceRoutingPrecheckExecutionStatus",
        "routingExecutionStatus": "sourceRoutingExecutionStatus",
        "committeeReentryExecutionStatus": "sourceCommitteeReentryExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source assignment acknowledgement preview must remain dryRunOnly=true")
    if receipt.get("sourceReviewerAssignmentAcknowledgementPreviewId") != source.get("id"):
        failures.append("sourceReviewerAssignmentAcknowledgementPreviewId must match D61 preview id")
    if data.get("coveredReviewerAssignmentAcknowledgementPreviewStatus") != source.get("previewStatus"):
        failures.append("covered reviewer assignment acknowledgement status must match D61 preview status")

    if len(set(receipt.get("routingReceiptRoles", []))) != expected["routingReceiptRoleCount"]:
        failures.append("routingReceiptRoleCount mismatch")
    if not set(source.get("assignmentAcknowledgementRoles", [])).issubset(
        set(receipt.get("routingReceiptRoles", []))
    ):
        failures.append("routingReceiptRoles must include D61 assignmentAcknowledgementRoles")
    if len(set(receipt.get("routingReceiptSections", []))) != expected["routingReceiptSectionCount"]:
        failures.append("routingReceiptSectionCount mismatch")
    if len(set(receipt.get("routingReceiptEnvelopeFields", []))) != expected[
        "routingReceiptEnvelopeFieldCount"
    ]:
        failures.append("routingReceiptEnvelopeFieldCount mismatch")
    if len(set(receipt.get("routingReceiptReadinessPrerequisites", []))) != expected[
        "routingReceiptReadinessPrerequisiteCount"
    ]:
        failures.append("routingReceiptReadinessPrerequisiteCount mismatch")
    if len(set(receipt.get("routingReceiptDecisionConstraints", []))) != expected[
        "routingReceiptDecisionConstraintCount"
    ]:
        failures.append("routingReceiptDecisionConstraintCount mismatch")
    if len(set(receipt.get("routingReceiptChecks", []))) != expected["routingReceiptCheckCount"]:
        failures.append("routingReceiptCheckCount mismatch")
    if len(set(receipt.get("requiredRoutingReceiptRefs", []))) != expected[
        "requiredRoutingReceiptRefCount"
    ]:
        failures.append("requiredRoutingReceiptRefCount mismatch")
    if len(set(receipt.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(receipt.get("routingReceiptSections", [])),
        {
            "candidate_receipt_destination_matrix",
            "candidate_acknowledgement_to_routing_mapping",
            "candidate_receipt_blocker_codes",
            "candidate_receipt_hold_conditions",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "routing receipt section",
        failures,
    )
    require_all(
        set(receipt.get("routingReceiptDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "routing_receipt_preview_not_formal_receipt",
            "no_routing_receipt_execution",
            "no_assignment_acknowledgement_execution",
            "no_reviewer_notification",
            "no_reviewer_assignment_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "routing receipt constraint",
        failures,
    )
    require_all(
        set(receipt.get("forbiddenActions", [])),
        {
            "execute_routing_receipt",
            "execute_assignment_acknowledgement",
            "notify_reviewer",
            "execute_reviewer_assignment",
            "execute_committee_reentry",
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
        "executesRoutingReceipt",
        "executesAssignmentAcknowledgement",
        "notifiesReviewer",
        "executesReviewerAssignment",
        "executesRoutingPrecheck",
        "executesRouting",
        "executesCommitteeReentry",
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
        print("gckf_p0_formal_evidence_execution_reviewer_acknowledgement_routing_receipt_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_reviewer_acknowledgement_routing_receipt_preview_dry_run=pass")
    print(f"status={receipt['previewStatus']}")
    print(f"execution_mode={receipt['executionMode']}")
    print("executes_routing_receipt=0")
    print("executes_assignment_acknowledgement=0")
    print("notifies_reviewer=0")
    print("executes_reviewer_assignment=0")
    print("executes_routing_precheck=0")
    print("executes_routing=0")
    print("executes_committee_reentry=0")
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
