#!/usr/bin/env python3
"""Validate P0 routing reviewer assignment preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-routing-reviewer-assignment-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceAcknowledgementRoutingPrecheckPreview"])
    source = source_data["acknowledgementRoutingPrecheckPreview"]
    assignment = data["routingReviewerAssignmentPreview"]

    if data.get("routingReviewerAssignmentPreviewStatus") != expected["routingReviewerAssignmentPreviewStatus"]:
        failures.append("routingReviewerAssignmentPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalReviewerAssignment") is not expected["notFinalReviewerAssignment"]:
        failures.append("reviewer assignment preview must state notFinalReviewerAssignment=true")
    if assignment.get("previewType") != expected["previewType"]:
        failures.append("reviewer assignment previewType mismatch")
    if assignment.get("previewStatus") != expected["previewStatus"]:
        failures.append("reviewer assignment previewStatus must remain candidate_preview")
    if assignment.get("executionMode") != expected["executionMode"]:
        failures.append("reviewer assignment preview executionMode mismatch")
    if assignment.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("reviewer assignment preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
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
        if assignment.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("acknowledgementRoutingPrecheckPreviewStatus") != expected[
        "sourceAcknowledgementRoutingPrecheckPreviewStatus"
    ]:
        failures.append("source acknowledgement routing precheck preview must remain candidate_preview")
    source_status_map = {
        "routingPrecheckExecutionStatus": "sourceRoutingPrecheckExecutionStatus",
        "routingExecutionStatus": "sourceRoutingExecutionStatus",
        "acknowledgementExecutionStatus": "sourceAcknowledgementExecutionStatus",
        "repairRequestExecutionStatus": "sourceRepairRequestExecutionStatus",
        "supplementIntakeExecutionStatus": "sourceSupplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus": "sourceSupplementAcceptanceExecutionStatus",
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
        failures.append("source routing precheck preview must remain dryRunOnly=true")
    if assignment.get("sourceAcknowledgementRoutingPrecheckPreviewId") != source.get("id"):
        failures.append("sourceAcknowledgementRoutingPrecheckPreviewId must match D59 preview id")
    if data.get("coveredAcknowledgementRoutingPrecheckPreviewStatus") != source.get("previewStatus"):
        failures.append("covered acknowledgement routing precheck status must match D59 preview status")

    if len(set(assignment.get("reviewerAssignmentRoles", []))) != expected["reviewerAssignmentRoleCount"]:
        failures.append("reviewerAssignmentRoleCount mismatch")
    if not set(source.get("routingPrecheckRoles", [])).issubset(
        set(assignment.get("reviewerAssignmentRoles", []))
    ):
        failures.append("reviewerAssignmentRoles must include D59 routingPrecheckRoles")
    if len(set(assignment.get("reviewerAssignmentSections", []))) != expected["reviewerAssignmentSectionCount"]:
        failures.append("reviewerAssignmentSectionCount mismatch")
    if len(set(assignment.get("reviewerAssignmentEnvelopeFields", []))) != expected[
        "reviewerAssignmentEnvelopeFieldCount"
    ]:
        failures.append("reviewerAssignmentEnvelopeFieldCount mismatch")
    if len(set(assignment.get("reviewerAssignmentReadinessPrerequisites", []))) != expected[
        "reviewerAssignmentReadinessPrerequisiteCount"
    ]:
        failures.append("reviewerAssignmentReadinessPrerequisiteCount mismatch")
    if len(set(assignment.get("reviewerAssignmentDecisionConstraints", []))) != expected[
        "reviewerAssignmentDecisionConstraintCount"
    ]:
        failures.append("reviewerAssignmentDecisionConstraintCount mismatch")
    if len(set(assignment.get("reviewerAssignmentChecks", []))) != expected["reviewerAssignmentCheckCount"]:
        failures.append("reviewerAssignmentCheckCount mismatch")
    if len(set(assignment.get("requiredReviewerAssignmentRefs", []))) != expected[
        "requiredReviewerAssignmentRefCount"
    ]:
        failures.append("requiredReviewerAssignmentRefCount mismatch")
    if len(set(assignment.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(assignment.get("reviewerAssignmentSections", [])),
        {
            "candidate_reviewer_lane_matrix",
            "candidate_reviewer_role_matrix",
            "recusal_screen_candidates",
            "assignment_blocker_candidates",
            "candidate_assignment_path",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "reviewer assignment section",
        failures,
    )
    require_all(
        set(assignment.get("reviewerAssignmentDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "reviewer_assignment_preview_not_formal_assignment",
            "no_reviewer_assignment_execution",
            "no_routing_precheck_execution",
            "no_routing_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "reviewer assignment constraint",
        failures,
    )
    require_all(
        set(assignment.get("forbiddenActions", [])),
        {
            "execute_reviewer_assignment",
            "notify_reviewer",
            "execute_routing_precheck",
            "execute_routing",
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
        "executesReviewerAssignment",
        "notifiesReviewer",
        "executesRoutingPrecheck",
        "executesRouting",
        "executesAcknowledgement",
        "executesRepairRequest",
        "executesSupplementIntake",
        "acceptsSupplementMaterial",
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
        print("gckf_p0_formal_evidence_execution_routing_reviewer_assignment_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_routing_reviewer_assignment_preview_dry_run=pass")
    print(f"status={assignment['previewStatus']}")
    print(f"execution_mode={assignment['executionMode']}")
    print("executes_reviewer_assignment=0")
    print("notifies_reviewer=0")
    print("executes_routing_precheck=0")
    print("executes_routing=0")
    print("executes_acknowledgement=0")
    print("executes_repair_request=0")
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
