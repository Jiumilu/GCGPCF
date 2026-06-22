#!/usr/bin/env python3
"""Validate P0 reviewer assignment acknowledgement preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-reviewer-assignment-acknowledgement-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceRoutingReviewerAssignmentPreview"])
    source = source_data["routingReviewerAssignmentPreview"]
    ack = data["reviewerAssignmentAcknowledgementPreview"]

    if data.get("reviewerAssignmentAcknowledgementPreviewStatus") != expected[
        "reviewerAssignmentAcknowledgementPreviewStatus"
    ]:
        failures.append("reviewerAssignmentAcknowledgementPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAssignmentAcknowledgement") is not expected["notFinalAssignmentAcknowledgement"]:
        failures.append("assignment acknowledgement preview must state notFinalAssignmentAcknowledgement=true")
    if ack.get("previewType") != expected["previewType"]:
        failures.append("assignment acknowledgement previewType mismatch")
    if ack.get("previewStatus") != expected["previewStatus"]:
        failures.append("assignment acknowledgement previewStatus must remain candidate_preview")
    if ack.get("executionMode") != expected["executionMode"]:
        failures.append("assignment acknowledgement preview executionMode mismatch")
    if ack.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("assignment acknowledgement preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "assignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus",
        "routingPrecheckExecutionStatus",
        "routingExecutionStatus",
        "acknowledgementExecutionStatus",
        "repairRequestExecutionStatus",
        "supplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if ack.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("routingReviewerAssignmentPreviewStatus") != expected[
        "sourceRoutingReviewerAssignmentPreviewStatus"
    ]:
        failures.append("source routing reviewer assignment preview must remain candidate_preview")
    source_status_map = {
        "reviewerAssignmentExecutionStatus": "sourceReviewerAssignmentExecutionStatus",
        "routingPrecheckExecutionStatus": "sourceRoutingPrecheckExecutionStatus",
        "routingExecutionStatus": "sourceRoutingExecutionStatus",
        "acknowledgementExecutionStatus": "sourceAcknowledgementExecutionStatus",
        "repairRequestExecutionStatus": "sourceRepairRequestExecutionStatus",
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
        failures.append("source reviewer assignment preview must remain dryRunOnly=true")
    if ack.get("sourceRoutingReviewerAssignmentPreviewId") != source.get("id"):
        failures.append("sourceRoutingReviewerAssignmentPreviewId must match D60 preview id")
    if data.get("coveredRoutingReviewerAssignmentPreviewStatus") != source.get("previewStatus"):
        failures.append("covered routing reviewer assignment status must match D60 preview status")

    if len(set(ack.get("assignmentAcknowledgementRoles", []))) != expected[
        "assignmentAcknowledgementRoleCount"
    ]:
        failures.append("assignmentAcknowledgementRoleCount mismatch")
    if not set(source.get("reviewerAssignmentRoles", [])).issubset(
        set(ack.get("assignmentAcknowledgementRoles", []))
    ):
        failures.append("assignmentAcknowledgementRoles must include D60 reviewerAssignmentRoles")
    if len(set(ack.get("assignmentAcknowledgementSections", []))) != expected[
        "assignmentAcknowledgementSectionCount"
    ]:
        failures.append("assignmentAcknowledgementSectionCount mismatch")
    if len(set(ack.get("assignmentAcknowledgementEnvelopeFields", []))) != expected[
        "assignmentAcknowledgementEnvelopeFieldCount"
    ]:
        failures.append("assignmentAcknowledgementEnvelopeFieldCount mismatch")
    if len(set(ack.get("assignmentAcknowledgementReadinessPrerequisites", []))) != expected[
        "assignmentAcknowledgementReadinessPrerequisiteCount"
    ]:
        failures.append("assignmentAcknowledgementReadinessPrerequisiteCount mismatch")
    if len(set(ack.get("assignmentAcknowledgementDecisionConstraints", []))) != expected[
        "assignmentAcknowledgementDecisionConstraintCount"
    ]:
        failures.append("assignmentAcknowledgementDecisionConstraintCount mismatch")
    if len(set(ack.get("assignmentAcknowledgementChecks", []))) != expected[
        "assignmentAcknowledgementCheckCount"
    ]:
        failures.append("assignmentAcknowledgementCheckCount mismatch")
    if len(set(ack.get("requiredAssignmentAcknowledgementRefs", []))) != expected[
        "requiredAssignmentAcknowledgementRefCount"
    ]:
        failures.append("requiredAssignmentAcknowledgementRefCount mismatch")
    if len(set(ack.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(ack.get("assignmentAcknowledgementSections", [])),
        {
            "candidate_assignment_receipt_fields",
            "candidate_acknowledgement_recipient_matrix",
            "recusal_screen_snapshot",
            "acknowledgement_blocker_candidates",
            "candidate_assignment_acknowledgement_path",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "assignment acknowledgement section",
        failures,
    )
    require_all(
        set(ack.get("assignmentAcknowledgementDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "assignment_acknowledgement_preview_not_formal_acknowledgement",
            "no_assignment_acknowledgement_execution",
            "no_reviewer_notification",
            "no_reviewer_assignment_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "assignment acknowledgement constraint",
        failures,
    )
    require_all(
        set(ack.get("forbiddenActions", [])),
        {
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
        "executesAssignmentAcknowledgement",
        "notifiesReviewer",
        "executesReviewerAssignment",
        "executesRoutingPrecheck",
        "executesRouting",
        "executesAcknowledgement",
        "executesRepairRequest",
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
        print("gckf_p0_formal_evidence_execution_reviewer_assignment_acknowledgement_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_reviewer_assignment_acknowledgement_preview_dry_run=pass")
    print(f"status={ack['previewStatus']}")
    print(f"execution_mode={ack['executionMode']}")
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
