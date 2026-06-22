#!/usr/bin/env python3
"""Validate P0 committee case opening guard preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-case-opening-guard-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeIntakeAcceptancePrecheckPreview"])
    source = source_data["committeeIntakeAcceptancePrecheckPreview"]
    guard = data["committeeCaseOpeningGuardPreview"]

    if data.get("committeeCaseOpeningGuardPreviewStatus") != expected["committeeCaseOpeningGuardPreviewStatus"]:
        failures.append("committeeCaseOpeningGuardPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalCaseOpening") is not expected["notFinalCaseOpening"]:
        failures.append("committee case opening guard preview must state notFinalCaseOpening=true")
    if guard.get("previewType") != expected["previewType"]:
        failures.append("committee case opening guard previewType mismatch")
    if guard.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee case opening guard previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "intakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if guard.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if guard.get("executionMode") != expected["executionMode"]:
        failures.append("committee case opening guard executionMode mismatch")
    if guard.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee case opening guard preview must remain dryRunOnly=true")

    if source_data.get("committeeIntakeAcceptancePrecheckPreviewStatus") != expected[
        "sourceCommitteeIntakeAcceptancePrecheckPreviewStatus"
    ]:
        failures.append("source committee intake acceptance precheck preview must remain candidate_preview")
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
        failures.append("source committee intake acceptance precheck must remain dryRunOnly=true")
    if guard.get("sourceCommitteeIntakeAcceptancePrecheckPreviewId") != source.get("id"):
        failures.append("sourceCommitteeIntakeAcceptancePrecheckPreviewId must match D49 preview id")
    if data.get("coveredCommitteeIntakeAcceptancePrecheckPreviewStatus") != expected[
        "coveredCommitteeIntakeAcceptancePrecheckPreviewStatus"
    ]:
        failures.append("coveredCommitteeIntakeAcceptancePrecheckPreviewStatus mismatch")
    if data["coveredCommitteeIntakeAcceptancePrecheckPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee intake precheck status must match D49 preview status")

    roles = set(guard.get("guardRoles", []))
    if len(roles) != expected["guardRoleCount"]:
        failures.append("guardRoleCount mismatch")
    if roles != set(source.get("precheckRoles", [])):
        failures.append("guardRoles must mirror D49 precheckRoles")

    sections = set(guard.get("guardSections", []))
    if len(sections) != expected["guardSectionCount"]:
        failures.append("guardSectionCount mismatch")
    require_all(
        sections,
        {
            "source_intake_precheck_lineage",
            "case_opening_scope",
            "case_opening_prerequisites",
            "committee_submission_readiness",
            "committee_authority_boundary",
            "freeze_retention_guard",
            "waes_negative_gate_guard",
            "harness_no_write_guard",
            "business_system_no_write_guard",
            "revenue_contribution_no_write_guard",
            "return_to_intake_precheck_path",
            "no_write_attestation",
        },
        "guard section",
        failures,
    )

    prerequisites = set(guard.get("caseOpeningPrerequisites", []))
    if len(prerequisites) != expected["caseOpeningPrerequisiteCount"]:
        failures.append("caseOpeningPrerequisiteCount mismatch")
    constraints = set(guard.get("guardDecisionConstraints", []))
    if len(constraints) != expected["guardDecisionConstraintCount"]:
        failures.append("guardDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "guard_not_case_opening",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "guard decision constraint",
        failures,
    )

    checks = set(guard.get("guardChecks", []))
    if len(checks) != expected["guardCheckCount"]:
        failures.append("guardCheckCount mismatch")
    require_all(
        checks,
        {
            "source_intake_precheck_preview_status_is_candidate_preview",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_precheck_is_dry_run_only",
            "committee_case_opening_guard_preview_status_is_candidate_preview",
            "all_guard_roles_covered",
            "all_guard_sections_covered",
            "all_case_opening_prerequisites_covered",
            "all_guard_decision_constraints_covered",
            "assert_guard_not_case_opening",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
        },
        "guard check",
        failures,
    )

    refs = set(guard.get("requiredGuardRefs", []))
    if len(refs) != expected["requiredGuardRefCount"]:
        failures.append("requiredGuardRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeIntakeAcceptancePrecheckPreviewRef",
            "sourceCommitteeCaseReviewPacketPreviewRef",
            "caseOpeningScopeRef",
            "caseOpeningPrerequisitesRef",
            "committeeSubmissionReadinessRef",
            "committeeAuthorityBoundaryRef",
            "freezeRetentionGuardRef",
            "waesNegativeGateGuardRef",
            "harnessNoWriteGuardRef",
            "businessSystemNoWriteGuardRef",
            "revenueContributionNoWriteGuardRef",
            "returnToIntakePrecheckPathRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required guard ref",
        failures,
    )

    if len(set(guard.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(guard.get("forbiddenActions", []))
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
        print("gckf_p0_formal_evidence_execution_committee_case_opening_guard_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_case_opening_guard_preview_dry_run=pass")
    print(f"status={guard['previewStatus']}")
    print(f"execution_mode={guard['executionMode']}")
    print("executes_intake_acceptance=0")
    print("submits_committee_case_packet=0")
    print("submits_committee_review_input=0")
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
