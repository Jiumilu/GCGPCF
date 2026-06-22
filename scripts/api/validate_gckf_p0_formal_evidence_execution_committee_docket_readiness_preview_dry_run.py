#!/usr/bin/env python3
"""Validate P0 committee docket readiness preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-docket-readiness-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeCaseOpeningGuardPreview"])
    source = source_data["committeeCaseOpeningGuardPreview"]
    docket = data["committeeDocketReadinessPreview"]

    if data.get("committeeDocketReadinessPreviewStatus") != expected["committeeDocketReadinessPreviewStatus"]:
        failures.append("committeeDocketReadinessPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalDocket") is not expected["notFinalDocket"]:
        failures.append("committee docket readiness preview must state notFinalDocket=true")
    if docket.get("previewType") != expected["previewType"]:
        failures.append("committee docket readiness previewType mismatch")
    if docket.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee docket readiness previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "intakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if docket.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if docket.get("executionMode") != expected["executionMode"]:
        failures.append("committee docket readiness executionMode mismatch")
    if docket.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee docket readiness preview must remain dryRunOnly=true")

    if source_data.get("committeeCaseOpeningGuardPreviewStatus") != expected[
        "sourceCommitteeCaseOpeningGuardPreviewStatus"
    ]:
        failures.append("source committee case opening guard preview must remain candidate_preview")
    source_status_map = {
        "intakeAcceptanceExecutionStatus": "sourceIntakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus": "sourceCommitteeSubmissionExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source committee case opening guard must remain dryRunOnly=true")
    if docket.get("sourceCommitteeCaseOpeningGuardPreviewId") != source.get("id"):
        failures.append("sourceCommitteeCaseOpeningGuardPreviewId must match D50 preview id")
    if data.get("coveredCommitteeCaseOpeningGuardPreviewStatus") != expected[
        "coveredCommitteeCaseOpeningGuardPreviewStatus"
    ]:
        failures.append("coveredCommitteeCaseOpeningGuardPreviewStatus mismatch")
    if data["coveredCommitteeCaseOpeningGuardPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee case opening guard status must match D50 preview status")

    roles = set(docket.get("docketRoles", []))
    if len(roles) != expected["docketRoleCount"]:
        failures.append("docketRoleCount mismatch")
    if roles != set(source.get("guardRoles", [])):
        failures.append("docketRoles must mirror D50 guardRoles")

    sections = set(docket.get("docketSections", []))
    if len(sections) != expected["docketSectionCount"]:
        failures.append("docketSectionCount mismatch")
    require_all(
        sections,
        {
            "source_case_opening_guard_lineage",
            "docket_scope",
            "docket_readiness_prerequisites",
            "committee_material_index",
            "reviewer_assignment_readiness",
            "authority_and_recusal_boundary",
            "freeze_retention_guard",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "business_system_no_write_guard",
            "return_to_case_opening_guard_path",
            "no_write_attestation",
        },
        "docket section",
        failures,
    )

    prerequisites = set(docket.get("docketReadinessPrerequisites", []))
    if len(prerequisites) != expected["docketReadinessPrerequisiteCount"]:
        failures.append("docketReadinessPrerequisiteCount mismatch")
    constraints = set(docket.get("docketDecisionConstraints", []))
    if len(constraints) != expected["docketDecisionConstraintCount"]:
        failures.append("docketDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "docket_readiness_not_docket_creation",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_harness_evidence_write",
        },
        "docket decision constraint",
        failures,
    )

    checks = set(docket.get("docketChecks", []))
    if len(checks) != expected["docketCheckCount"]:
        failures.append("docketCheckCount mismatch")
    require_all(
        checks,
        {
            "source_case_opening_guard_preview_status_is_candidate_preview",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_guard_is_dry_run_only",
            "committee_docket_readiness_preview_status_is_candidate_preview",
            "all_docket_roles_covered",
            "all_docket_sections_covered",
            "all_docket_readiness_prerequisites_covered",
            "all_docket_decision_constraints_covered",
            "assert_docket_readiness_not_docket_creation",
            "assert_committee_docket_not_created",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
        },
        "docket check",
        failures,
    )

    refs = set(docket.get("requiredDocketRefs", []))
    if len(refs) != expected["requiredDocketRefCount"]:
        failures.append("requiredDocketRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseOpeningGuardPreviewRef",
            "sourceCommitteeIntakeAcceptancePrecheckPreviewRef",
            "docketScopeRef",
            "docketReadinessPrerequisitesRef",
            "committeeMaterialIndexRef",
            "reviewerAssignmentReadinessRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionGuardRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "businessSystemNoWriteGuardRef",
            "returnToCaseOpeningGuardPathRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required docket ref",
        failures,
    )

    if len(set(docket.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(docket.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("forbiddenOutputs", []))) != expected["forbiddenOutputCount"]:
        failures.append("forbiddenOutputCount mismatch")
    required_sources = set(data.get("requiredSourceRefs", []))
    if len(required_sources) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for relative_path in required_sources:
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")

    for key in (
        "executesIntakeAcceptance",
        "submitsCommitteeCasePacket",
        "submitsCommitteeReviewInput",
        "createsCommitteeDocket",
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

    for token in (
        "execute_intake_acceptance",
        "submit_committee_case_packet",
        "submit_committee_review_input",
        "create_committee_docket",
        "open_committee_case",
        "execute_committee_decision",
        "execute_human_confirmation",
        "execute_freeze_release",
        "execute_unfreeze",
        "write_kds",
        "write_business_system",
        "write_harness_evidence",
        "write_formal_evidence",
        "write_revenue_distribution",
        "write_contribution_score",
    ):
        if token not in forbidden_actions:
            failures.append(f"missing forbidden action token: {token}")

    if failures:
        print("gckf_p0_formal_evidence_execution_committee_docket_readiness_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_docket_readiness_preview_dry_run=pass")
    print(f"status={docket['previewStatus']}")
    print(f"execution_mode={docket['executionMode']}")
    print("executes_intake_acceptance=0")
    print("submits_committee_case_packet=0")
    print("submits_committee_review_input=0")
    print("creates_committee_docket=0")
    print("opens_committee_case=0")
    print("executes_committee_decision=0")
    print("executes_human_confirmation=0")
    print("releases_freeze=0")
    print("executes_unfreeze=0")
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
