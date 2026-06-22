#!/usr/bin/env python3
"""Validate P0 reviewer acceptance acknowledgement routing package preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-reviewer-acceptance-acknowledgement-routing-package-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceReviewerAcceptanceAcknowledgementPreview"])
    source = source_data["reviewerAcceptanceAcknowledgementPreview"]
    package = data["reviewerAcceptanceAcknowledgementRoutingPackagePreview"]

    if data.get("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus") != expected[
        "reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus"
    ]:
        failures.append("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRoutingPackage") is not expected["notFinalRoutingPackage"]:
        failures.append("routing package preview must state notFinalRoutingPackage=true")
    if package.get("previewType") != expected["previewType"]:
        failures.append("routing package previewType mismatch")
    if package.get("previewStatus") != expected["previewStatus"]:
        failures.append("routing package previewStatus must remain candidate_preview")
    if package.get("executionMode") != expected["executionMode"]:
        failures.append("routing package executionMode mismatch")
    if package.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("routing package must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "routingPackageExecutionStatus",
        "reviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus",
        "routingReceiptExecutionStatus",
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
        if package.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("reviewerAcceptanceAcknowledgementPreviewStatus") != expected[
        "sourceReviewerAcceptanceAcknowledgementPreviewStatus"
    ]:
        failures.append("source reviewer acceptance acknowledgement must remain candidate_preview")
    source_status_map = {
        "reviewerAcceptanceAcknowledgementExecutionStatus": "sourceReviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptancePrecheckExecutionStatus": "sourceReviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus": "sourceReviewerAcceptanceExecutionStatus",
        "routingReceiptExecutionStatus": "sourceRoutingReceiptExecutionStatus",
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
    if source.get("dryRunOnly") is not True:
        failures.append("source reviewer acceptance acknowledgement must remain dryRunOnly=true")
    if package.get("sourceReviewerAcceptanceAcknowledgementPreviewId") != source.get("id"):
        failures.append("sourceReviewerAcceptanceAcknowledgementPreviewId must match D64 preview id")
    if data.get("coveredReviewerAcceptanceAcknowledgementPreviewStatus") != source.get("previewStatus"):
        failures.append("covered reviewer acceptance acknowledgement status must match D64 preview status")

    if len(set(package.get("routingPackageRoles", []))) != expected["routingPackageRoleCount"]:
        failures.append("routingPackageRoleCount mismatch")
    if not {"reviewer_acceptance_acknowledgement_owner", "routing_package_owner", "waes_gate_owner"}.issubset(
        set(package.get("routingPackageRoles", []))
    ):
        failures.append("routingPackageRoles must include required D65 owners")
    if len(set(package.get("routingPackageSections", []))) != expected["routingPackageSectionCount"]:
        failures.append("routingPackageSectionCount mismatch")
    if len(set(package.get("routingPackageEnvelopeFields", []))) != expected["routingPackageEnvelopeFieldCount"]:
        failures.append("routingPackageEnvelopeFieldCount mismatch")
    if len(set(package.get("routingPackageReadinessPrerequisites", []))) != expected[
        "routingPackageReadinessPrerequisiteCount"
    ]:
        failures.append("routingPackageReadinessPrerequisiteCount mismatch")
    if len(set(package.get("routingPackageDecisionConstraints", []))) != expected[
        "routingPackageDecisionConstraintCount"
    ]:
        failures.append("routingPackageDecisionConstraintCount mismatch")
    if len(set(package.get("routingPackageChecks", []))) != expected["routingPackageCheckCount"]:
        failures.append("routingPackageCheckCount mismatch")
    if len(set(package.get("requiredRoutingPackageRefs", []))) != expected["requiredRoutingPackageRefCount"]:
        failures.append("requiredRoutingPackageRefCount mismatch")
    if len(set(package.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(package.get("routingPackageSections", [])),
        {
            "candidate_package_destination_matrix",
            "candidate_acknowledgement_to_package_mapping",
            "candidate_package_blocker_codes",
            "candidate_package_hold_conditions",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "routing package section",
        failures,
    )
    require_all(
        set(package.get("routingPackageDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "routing_package_not_formal_package",
            "no_routing_package_execution",
            "no_reviewer_acceptance_acknowledgement_execution",
            "no_reviewer_acceptance_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "routing package constraint",
        failures,
    )
    require_all(
        set(package.get("forbiddenActions", [])),
        {
            "execute_routing_package",
            "submit_routing_package",
            "execute_reviewer_acceptance_acknowledgement",
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
        "executesRoutingPackage",
        "submitsRoutingPackage",
        "executesReviewerAcceptanceAcknowledgement",
        "executesReviewerAcceptancePrecheck",
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
        print("gckf_p0_formal_evidence_execution_reviewer_acceptance_acknowledgement_routing_package_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_reviewer_acceptance_acknowledgement_routing_package_preview_dry_run=pass")
    print(f"status={package['previewStatus']}")
    print(f"execution_mode={package['executionMode']}")
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
