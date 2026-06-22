#!/usr/bin/env python3
"""Validate P0 routing package intake guard preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-routing-package-intake-guard-preview-dry-run-v0.1.json"
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
    guard = data["routingPackageIntakeGuardPreview"]

    if data.get("routingPackageIntakeGuardPreviewStatus") != expected["routingPackageIntakeGuardPreviewStatus"]:
        failures.append("routingPackageIntakeGuardPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalIntakeGuard") is not expected["notFinalIntakeGuard"]:
        failures.append("intake guard preview must state notFinalIntakeGuard=true")
    if guard.get("previewType") != expected["previewType"]:
        failures.append("intake guard previewType mismatch")
    if guard.get("previewStatus") != expected["previewStatus"]:
        failures.append("intake guard previewStatus must remain candidate_preview")
    if guard.get("executionMode") != expected["executionMode"]:
        failures.append("intake guard executionMode mismatch")
    if guard.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("intake guard preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "intakeGuardExecutionStatus",
        "routingPackageExecutionStatus",
        "routingExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if guard.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus") != expected[
        "sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus"
    ]:
        failures.append("source routing package preview must remain candidate_preview")
    source_status_map = {
        "routingPackageExecutionStatus": "sourceRoutingPackageExecutionStatus",
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
        failures.append("source routing package preview must remain dryRunOnly=true")
    if guard.get("sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewId") != source.get("id"):
        failures.append("sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewId must match D65 preview id")
    if data.get("coveredReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus") != source.get("previewStatus"):
        failures.append("covered routing package status must match D65 preview status")

    count_checks = {
        "intakeGuardRoles": "intakeGuardRoleCount",
        "intakeGuardSections": "intakeGuardSectionCount",
        "intakeGuardEnvelopeFields": "intakeGuardEnvelopeFieldCount",
        "intakeGuardReadinessPrerequisites": "intakeGuardReadinessPrerequisiteCount",
        "intakeGuardDecisionConstraints": "intakeGuardDecisionConstraintCount",
        "intakeGuardChecks": "intakeGuardCheckCount",
        "requiredIntakeGuardRefs": "requiredIntakeGuardRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(guard.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(guard.get("intakeGuardSections", [])),
        {
            "candidate_package_completeness_check",
            "candidate_acl_boundary_check",
            "candidate_committee_visibility_check",
            "candidate_intake_blocker_codes",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "intake guard section",
        failures,
    )
    require_all(
        set(guard.get("intakeGuardDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "intake_guard_preview_not_formal_intake",
            "no_intake_guard_execution",
            "no_routing_package_execution",
            "no_routing_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "intake guard constraint",
        failures,
    )
    require_all(
        set(guard.get("forbiddenActions", [])),
        {
            "execute_intake_guard",
            "execute_routing_package",
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
        "executesIntakeGuard",
        "executesRoutingPackage",
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
        print("gckf_p0_formal_evidence_execution_routing_package_intake_guard_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_routing_package_intake_guard_preview_dry_run=pass")
    print(f"status={guard['previewStatus']}")
    print(f"execution_mode={guard['executionMode']}")
    print("executes_intake_guard=0")
    print("executes_routing_package=0")
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
