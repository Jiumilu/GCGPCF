#!/usr/bin/env python3
"""Validate P0 routing receipt reviewer acceptance precheck preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-routing-receipt-reviewer-acceptance-precheck-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceReviewerAcknowledgementRoutingReceiptPreview"])
    source = source_data["reviewerAcknowledgementRoutingReceiptPreview"]
    precheck = data["routingReceiptReviewerAcceptancePrecheckPreview"]

    if data.get("routingReceiptReviewerAcceptancePrecheckPreviewStatus") != expected[
        "routingReceiptReviewerAcceptancePrecheckPreviewStatus"
    ]:
        failures.append("routingReceiptReviewerAcceptancePrecheckPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalReviewerAcceptance") is not expected["notFinalReviewerAcceptance"]:
        failures.append("reviewer acceptance precheck must state notFinalReviewerAcceptance=true")
    if precheck.get("previewType") != expected["previewType"]:
        failures.append("reviewer acceptance precheck previewType mismatch")
    if precheck.get("previewStatus") != expected["previewStatus"]:
        failures.append("reviewer acceptance precheck previewStatus must remain candidate_preview")
    if precheck.get("executionMode") != expected["executionMode"]:
        failures.append("reviewer acceptance precheck executionMode mismatch")
    if precheck.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("reviewer acceptance precheck must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "reviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus",
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
        if precheck.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("reviewerAcknowledgementRoutingReceiptPreviewStatus") != expected[
        "sourceReviewerAcknowledgementRoutingReceiptPreviewStatus"
    ]:
        failures.append("source reviewer acknowledgement routing receipt preview must remain candidate_preview")
    source_status_map = {
        "routingReceiptExecutionStatus": "sourceRoutingReceiptExecutionStatus",
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
        failures.append("source routing receipt preview must remain dryRunOnly=true")
    if precheck.get("sourceReviewerAcknowledgementRoutingReceiptPreviewId") != source.get("id"):
        failures.append("sourceReviewerAcknowledgementRoutingReceiptPreviewId must match D62 preview id")
    if data.get("coveredReviewerAcknowledgementRoutingReceiptPreviewStatus") != source.get("previewStatus"):
        failures.append("covered reviewer acknowledgement routing receipt status must match D62 preview status")

    if len(set(precheck.get("reviewerAcceptancePrecheckRoles", []))) != expected[
        "reviewerAcceptancePrecheckRoleCount"
    ]:
        failures.append("reviewerAcceptancePrecheckRoleCount mismatch")
    if not set(source.get("routingReceiptRoles", [])).issubset(
        set(precheck.get("reviewerAcceptancePrecheckRoles", []))
    ):
        failures.append("reviewerAcceptancePrecheckRoles must include D62 routingReceiptRoles")
    if len(set(precheck.get("reviewerAcceptancePrecheckSections", []))) != expected[
        "reviewerAcceptancePrecheckSectionCount"
    ]:
        failures.append("reviewerAcceptancePrecheckSectionCount mismatch")
    if len(set(precheck.get("reviewerAcceptancePrecheckEnvelopeFields", []))) != expected[
        "reviewerAcceptancePrecheckEnvelopeFieldCount"
    ]:
        failures.append("reviewerAcceptancePrecheckEnvelopeFieldCount mismatch")
    if len(set(precheck.get("reviewerAcceptancePrecheckReadinessPrerequisites", []))) != expected[
        "reviewerAcceptancePrecheckReadinessPrerequisiteCount"
    ]:
        failures.append("reviewerAcceptancePrecheckReadinessPrerequisiteCount mismatch")
    if len(set(precheck.get("reviewerAcceptancePrecheckDecisionConstraints", []))) != expected[
        "reviewerAcceptancePrecheckDecisionConstraintCount"
    ]:
        failures.append("reviewerAcceptancePrecheckDecisionConstraintCount mismatch")
    if len(set(precheck.get("reviewerAcceptancePrecheckChecks", []))) != expected[
        "reviewerAcceptancePrecheckCheckCount"
    ]:
        failures.append("reviewerAcceptancePrecheckCheckCount mismatch")
    if len(set(precheck.get("requiredReviewerAcceptancePrecheckRefs", []))) != expected[
        "requiredReviewerAcceptancePrecheckRefCount"
    ]:
        failures.append("requiredReviewerAcceptancePrecheckRefCount mismatch")
    if len(set(precheck.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(precheck.get("reviewerAcceptancePrecheckSections", [])),
        {
            "candidate_reviewer_acceptance_matrix",
            "candidate_recusal_and_conflict_check",
            "candidate_capacity_and_sla_check",
            "candidate_access_boundary_check",
            "candidate_acceptance_blocker_codes",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "reviewer acceptance precheck section",
        failures,
    )
    require_all(
        set(precheck.get("reviewerAcceptancePrecheckDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "reviewer_acceptance_precheck_not_formal_acceptance",
            "no_reviewer_acceptance_precheck_execution",
            "no_reviewer_acceptance_execution",
            "no_routing_receipt_execution",
            "no_reviewer_notification",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "reviewer acceptance precheck constraint",
        failures,
    )
    require_all(
        set(precheck.get("forbiddenActions", [])),
        {
            "execute_reviewer_acceptance_precheck",
            "accept_reviewer",
            "execute_routing_receipt",
            "notify_reviewer",
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
        "executesReviewerAcceptancePrecheck",
        "executesReviewerAcceptance",
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
        print(
            "gckf_p0_formal_evidence_execution_routing_receipt_reviewer_acceptance_precheck_preview_dry_run=fail"
        )
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "gckf_p0_formal_evidence_execution_routing_receipt_reviewer_acceptance_precheck_preview_dry_run=pass"
    )
    print(f"status={precheck['previewStatus']}")
    print(f"execution_mode={precheck['executionMode']}")
    print("executes_reviewer_acceptance_precheck=0")
    print("executes_reviewer_acceptance=0")
    print("executes_routing_receipt=0")
    print("executes_assignment_acknowledgement=0")
    print("notifies_reviewer=0")
    print("executes_reviewer_assignment=0")
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
