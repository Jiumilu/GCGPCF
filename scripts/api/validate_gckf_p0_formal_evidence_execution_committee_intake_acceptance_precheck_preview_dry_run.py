#!/usr/bin/env python3
"""Validate P0 committee intake acceptance precheck preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-intake-acceptance-precheck-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeCaseReviewPacketPreview"])
    source = source_data["committeeCaseReviewPacketPreview"]
    precheck = data["committeeIntakeAcceptancePrecheckPreview"]

    if data.get("committeeIntakeAcceptancePrecheckPreviewStatus") != expected["committeeIntakeAcceptancePrecheckPreviewStatus"]:
        failures.append("committeeIntakeAcceptancePrecheckPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("committee intake acceptance precheck preview must state notFinalAcceptance=true")
    if precheck.get("previewType") != expected["previewType"]:
        failures.append("committee intake acceptance precheck previewType mismatch")
    if precheck.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee intake acceptance precheck previewStatus must remain candidate_preview")
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
        if precheck.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if precheck.get("executionMode") != expected["executionMode"]:
        failures.append("committee intake precheck executionMode mismatch")
    if precheck.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee intake precheck preview must remain dryRunOnly=true")

    if source_data.get("committeeCaseReviewPacketPreviewStatus") != expected["sourceCommitteeCaseReviewPacketPreviewStatus"]:
        failures.append("source committee case review packet preview must remain candidate_preview")
    source_status_map = {
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
        failures.append("source committee case review packet must remain dryRunOnly=true")
    if precheck.get("sourceCommitteeCaseReviewPacketPreviewId") != source.get("id"):
        failures.append("sourceCommitteeCaseReviewPacketPreviewId must match D48 preview id")
    if data.get("coveredCommitteeCaseReviewPacketPreviewStatus") != expected["coveredCommitteeCaseReviewPacketPreviewStatus"]:
        failures.append("coveredCommitteeCaseReviewPacketPreviewStatus mismatch")
    if data["coveredCommitteeCaseReviewPacketPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee case review packet status must match D48 preview status")

    roles = set(precheck.get("precheckRoles", []))
    if len(roles) != expected["precheckRoleCount"]:
        failures.append("precheckRoleCount mismatch")
    if roles != set(source.get("casePacketRoles", [])):
        failures.append("precheckRoles must mirror D48 casePacketRoles")

    sections = set(precheck.get("precheckSections", []))
    if len(sections) != expected["precheckSectionCount"]:
        failures.append("precheckSectionCount mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "case_packet_summary",
            "intake_acceptance_criteria",
            "routing_readiness",
            "evidence_completeness",
            "case_scope_boundary",
            "freeze_retention_statement",
            "decision_constraint_snapshot",
            "waes_negative_gate_snapshot",
            "harness_review_readiness",
            "exception_return_path",
            "no_write_attestation",
        },
        "precheck section",
        failures,
    )

    criteria = set(precheck.get("acceptanceCriteria", []))
    if len(criteria) != expected["acceptanceCriteriaCount"]:
        failures.append("acceptanceCriteriaCount mismatch")
    constraints = set(precheck.get("precheckDecisionConstraints", []))
    if len(constraints) != expected["precheckDecisionConstraintCount"]:
        failures.append("precheckDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "precheck_not_acceptance",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "precheck decision constraint",
        failures,
    )

    checks = set(precheck.get("precheckChecks", []))
    if len(checks) != expected["precheckCheckCount"]:
        failures.append("precheckCheckCount mismatch")
    require_all(
        checks,
        {
            "source_committee_case_review_packet_preview_status_is_candidate_preview",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_case_review_packet_is_dry_run_only",
            "committee_intake_acceptance_precheck_preview_status_is_candidate_preview",
            "all_precheck_roles_covered",
            "all_precheck_sections_covered",
            "all_acceptance_criteria_covered",
            "all_precheck_decision_constraints_covered",
            "assert_precheck_not_acceptance",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
        },
        "precheck check",
        failures,
    )

    refs = set(precheck.get("requiredPrecheckRefs", []))
    if len(refs) != expected["requiredPrecheckRefCount"]:
        failures.append("requiredPrecheckRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseReviewPacketPreviewRef",
            "sourceCommitteeReviewInputPreviewRef",
            "casePacketSummaryRef",
            "intakeAcceptanceCriteriaRef",
            "routingReadinessRef",
            "evidenceCompletenessRef",
            "waesNegativeGateSnapshotRef",
            "harnessReviewReadinessRef",
            "exceptionReturnPathRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required precheck ref",
        failures,
    )

    if len(set(precheck.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(precheck.get("forbiddenActions", []))
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
        print("gckf_p0_formal_evidence_execution_committee_intake_acceptance_precheck_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_intake_acceptance_precheck_preview_dry_run=pass")
    print(f"status={precheck['previewStatus']}")
    print(f"execution_mode={precheck['executionMode']}")
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
