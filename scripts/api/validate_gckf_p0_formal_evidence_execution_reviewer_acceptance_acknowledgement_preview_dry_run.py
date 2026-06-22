#!/usr/bin/env python3
"""Validate P0 reviewer acceptance acknowledgement preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-reviewer-acceptance-acknowledgement-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceReviewerAcceptancePrecheckPreview"])
    source = source_data["routingReceiptReviewerAcceptancePrecheckPreview"]
    ack = data["reviewerAcceptanceAcknowledgementPreview"]

    if data.get("reviewerAcceptanceAcknowledgementPreviewStatus") != expected[
        "reviewerAcceptanceAcknowledgementPreviewStatus"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalReviewerAcceptanceAcknowledgement") is not expected[
        "notFinalReviewerAcceptanceAcknowledgement"
    ]:
        failures.append("reviewer acceptance acknowledgement must state notFinalReviewerAcceptanceAcknowledgement=true")
    if ack.get("previewType") != expected["previewType"]:
        failures.append("reviewer acceptance acknowledgement previewType mismatch")
    if ack.get("previewStatus") != expected["previewStatus"]:
        failures.append("reviewer acceptance acknowledgement previewStatus must remain candidate_preview")
    if ack.get("executionMode") != expected["executionMode"]:
        failures.append("reviewer acceptance acknowledgement executionMode mismatch")
    if ack.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("reviewer acceptance acknowledgement must remain dryRunOnly=true")

    for key in (
        "executionStatus",
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
        "formalWriteExecutionStatus",
    ):
        if ack.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("routingReceiptReviewerAcceptancePrecheckPreviewStatus") != expected[
        "sourceReviewerAcceptancePrecheckPreviewStatus"
    ]:
        failures.append("source reviewer acceptance precheck preview must remain candidate_preview")
    source_status_map = {
        "reviewerAcceptancePrecheckExecutionStatus": "sourceReviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus": "sourceReviewerAcceptanceExecutionStatus",
        "routingReceiptExecutionStatus": "sourceRoutingReceiptExecutionStatus",
        "assignmentAcknowledgementExecutionStatus": "sourceAssignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus": "sourceReviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus": "sourceReviewerAssignmentExecutionStatus",
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
        failures.append("source reviewer acceptance precheck preview must remain dryRunOnly=true")
    if ack.get("sourceReviewerAcceptancePrecheckPreviewId") != source.get("id"):
        failures.append("sourceReviewerAcceptancePrecheckPreviewId must match D63 preview id")
    if data.get("coveredReviewerAcceptancePrecheckPreviewStatus") != source.get("previewStatus"):
        failures.append("covered reviewer acceptance precheck status must match D63 preview status")

    if len(set(ack.get("reviewerAcceptanceAcknowledgementRoles", []))) != expected[
        "reviewerAcceptanceAcknowledgementRoleCount"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementRoleCount mismatch")
    if not set(source.get("reviewerAcceptancePrecheckRoles", [])).issubset(
        set(ack.get("reviewerAcceptanceAcknowledgementRoles", []))
    ):
        failures.append("reviewerAcceptanceAcknowledgementRoles must include D63 reviewerAcceptancePrecheckRoles")
    if len(set(ack.get("reviewerAcceptanceAcknowledgementSections", []))) != expected[
        "reviewerAcceptanceAcknowledgementSectionCount"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementSectionCount mismatch")
    if len(set(ack.get("reviewerAcceptanceAcknowledgementEnvelopeFields", []))) != expected[
        "reviewerAcceptanceAcknowledgementEnvelopeFieldCount"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementEnvelopeFieldCount mismatch")
    if len(set(ack.get("reviewerAcceptanceAcknowledgementReadinessPrerequisites", []))) != expected[
        "reviewerAcceptanceAcknowledgementReadinessPrerequisiteCount"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementReadinessPrerequisiteCount mismatch")
    if len(set(ack.get("reviewerAcceptanceAcknowledgementDecisionConstraints", []))) != expected[
        "reviewerAcceptanceAcknowledgementDecisionConstraintCount"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementDecisionConstraintCount mismatch")
    if len(set(ack.get("reviewerAcceptanceAcknowledgementChecks", []))) != expected[
        "reviewerAcceptanceAcknowledgementCheckCount"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementCheckCount mismatch")
    if len(set(ack.get("requiredReviewerAcceptanceAcknowledgementRefs", []))) != expected[
        "requiredReviewerAcceptanceAcknowledgementRefCount"
    ]:
        failures.append("requiredReviewerAcceptanceAcknowledgementRefCount mismatch")
    if len(set(ack.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(ack.get("reviewerAcceptanceAcknowledgementSections", [])),
        {
            "candidate_acceptance_acknowledgement_fields",
            "candidate_acceptance_recipient_matrix",
            "candidate_acceptance_to_case_routing_mapping",
            "candidate_recusal_reconfirmation_snapshot",
            "candidate_acceptance_blocker_codes",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "reviewer acceptance acknowledgement section",
        failures,
    )
    require_all(
        set(ack.get("reviewerAcceptanceAcknowledgementDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "reviewer_acceptance_acknowledgement_not_formal_acknowledgement",
            "no_reviewer_acceptance_acknowledgement_execution",
            "no_reviewer_acceptance_execution",
            "no_routing_receipt_execution",
            "no_reviewer_notification",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "reviewer acceptance acknowledgement constraint",
        failures,
    )
    require_all(
        set(ack.get("forbiddenActions", [])),
        {
            "execute_reviewer_acceptance_acknowledgement",
            "execute_reviewer_acceptance_precheck",
            "accept_reviewer",
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
        "executesReviewerAcceptanceAcknowledgement",
        "executesReviewerAcceptancePrecheck",
        "executesReviewerAcceptance",
        "executesRoutingReceipt",
        "notifiesReviewer",
        "executesReviewerAssignment",
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
        print("gckf_p0_formal_evidence_execution_reviewer_acceptance_acknowledgement_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_reviewer_acceptance_acknowledgement_preview_dry_run=pass")
    print(f"status={ack['previewStatus']}")
    print(f"execution_mode={ack['executionMode']}")
    print("executes_reviewer_acceptance_acknowledgement=0")
    print("executes_reviewer_acceptance_precheck=0")
    print("executes_reviewer_acceptance=0")
    print("executes_routing_receipt=0")
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
