#!/usr/bin/env python3
"""Validate P0 routing package acknowledgement preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-routing-package-acknowledgement-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceReviewerAcceptanceAcknowledgementRoutingPackagePreview"])
    source = source_data["reviewerAcceptanceAcknowledgementRoutingPackagePreview"]
    acknowledgement = data["routingPackageAcknowledgementPreview"]

    if data.get("routingPackageAcknowledgementPreviewStatus") != expected["routingPackageAcknowledgementPreviewStatus"]:
        failures.append("routingPackageAcknowledgementPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRoutingPackageAcknowledgement") is not expected["notFinalRoutingPackageAcknowledgement"]:
        failures.append("acknowledgement preview must state notFinalRoutingPackageAcknowledgement=true")
    if acknowledgement.get("previewType") != expected["previewType"]:
        failures.append("routing package acknowledgement previewType mismatch")
    if acknowledgement.get("previewStatus") != expected["previewStatus"]:
        failures.append("routing package acknowledgement previewStatus must remain candidate_preview")
    if acknowledgement.get("executionMode") != expected["executionMode"]:
        failures.append("routing package acknowledgement executionMode mismatch")
    if acknowledgement.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("routing package acknowledgement must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "routingPackageAcknowledgementExecutionStatus",
        "routingPackageExecutionStatus",
        "routingPackageSubmissionStatus",
        "reviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptanceExecutionStatus",
        "reviewerNotificationExecutionStatus",
        "routingExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if acknowledgement.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus") != expected[
        "sourceRoutingPackagePreviewStatus"
    ]:
        failures.append("source routing package preview must remain candidate_preview")
    source_status_map = {
        "routingPackageExecutionStatus": "sourceRoutingPackageExecutionStatus",
        "reviewerAcceptanceAcknowledgementExecutionStatus": "sourceReviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptanceExecutionStatus": "sourceReviewerAcceptanceExecutionStatus",
        "reviewerNotificationExecutionStatus": "sourceReviewerNotificationExecutionStatus",
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
    if source.get("routingPackageExecutionStatus") != expected["sourceRoutingPackageExecutionStatus"]:
        failures.append("source routingPackageExecutionStatus must remain not_executed")
    if source.get("dryRunOnly") is not True:
        failures.append("source routing package preview must remain dryRunOnly=true")
    if acknowledgement.get("sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewId") != source.get("id"):
        failures.append("sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewId must match D65 preview id")
    if data.get("coveredReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus") != source.get("previewStatus"):
        failures.append("covered routing package preview status must match D65 preview status")
    if acknowledgement.get("routingPackageSubmissionStatus") != expected["sourceRoutingPackageSubmissionStatus"]:
        failures.append("routingPackageSubmissionStatus must remain not_executed")

    if len(set(acknowledgement.get("acknowledgementRoles", []))) != expected["acknowledgementRoleCount"]:
        failures.append("acknowledgementRoleCount mismatch")
    if not {"routing_package_owner", "routing_package_acknowledgement_owner", "waes_gate_owner"}.issubset(
        set(acknowledgement.get("acknowledgementRoles", []))
    ):
        failures.append("acknowledgementRoles must include required D66 owners")
    if len(set(acknowledgement.get("acknowledgementSections", []))) != expected["acknowledgementSectionCount"]:
        failures.append("acknowledgementSectionCount mismatch")
    if len(set(acknowledgement.get("acknowledgementEnvelopeFields", []))) != expected[
        "acknowledgementEnvelopeFieldCount"
    ]:
        failures.append("acknowledgementEnvelopeFieldCount mismatch")
    if len(set(acknowledgement.get("acknowledgementReadinessPrerequisites", []))) != expected[
        "acknowledgementReadinessPrerequisiteCount"
    ]:
        failures.append("acknowledgementReadinessPrerequisiteCount mismatch")
    if len(set(acknowledgement.get("acknowledgementDecisionConstraints", []))) != expected[
        "acknowledgementDecisionConstraintCount"
    ]:
        failures.append("acknowledgementDecisionConstraintCount mismatch")
    if len(set(acknowledgement.get("acknowledgementChecks", []))) != expected["acknowledgementCheckCount"]:
        failures.append("acknowledgementCheckCount mismatch")
    if len(set(acknowledgement.get("requiredAcknowledgementRefs", []))) != expected[
        "requiredAcknowledgementRefCount"
    ]:
        failures.append("requiredAcknowledgementRefCount mismatch")
    if len(set(acknowledgement.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(acknowledgement.get("acknowledgementSections", [])),
        {
            "candidate_acknowledgement_recipient_matrix",
            "candidate_package_to_acknowledgement_mapping",
            "candidate_acknowledgement_blocker_codes",
            "candidate_acknowledgement_hold_conditions",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "acknowledgement section",
        failures,
    )
    require_all(
        set(acknowledgement.get("acknowledgementDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "acknowledgement_not_formal_acknowledgement",
            "no_routing_package_acknowledgement_execution",
            "no_routing_package_execution",
            "no_routing_package_submission",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "acknowledgement constraint",
        failures,
    )
    require_all(
        set(acknowledgement.get("forbiddenActions", [])),
        {
            "execute_routing_package_acknowledgement",
            "execute_routing_package",
            "submit_routing_package",
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
        "executesRoutingPackageAcknowledgement",
        "executesRoutingPackage",
        "submitsRoutingPackage",
        "executesReviewerAcceptanceAcknowledgement",
        "executesReviewerAcceptance",
        "notifiesReviewer",
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
        print("gckf_p0_formal_evidence_execution_routing_package_acknowledgement_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_routing_package_acknowledgement_preview_dry_run=pass")
    print(f"status={acknowledgement['previewStatus']}")
    print(f"execution_mode={acknowledgement['executionMode']}")
    print("executes_routing_package_acknowledgement=0")
    print("executes_routing_package=0")
    print("submits_routing_package=0")
    print("executes_reviewer_acceptance_acknowledgement=0")
    print("executes_reviewer_acceptance=0")
    print("notifies_reviewer=0")
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
