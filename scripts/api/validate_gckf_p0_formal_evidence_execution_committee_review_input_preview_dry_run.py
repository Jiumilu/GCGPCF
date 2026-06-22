#!/usr/bin/env python3
"""Validate P0 committee review input preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-review-input-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeTriggerPackagePreview"])
    source = source_data["committeeTriggerPackagePreview"]
    review = data["committeeReviewInputPreview"]

    if data.get("committeeReviewInputPreviewStatus") != expected["committeeReviewInputPreviewStatus"]:
        failures.append("committeeReviewInputPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("committee review input preview must state notFinalAcceptance=true")
    if review.get("previewType") != expected["previewType"]:
        failures.append("committee review input previewType mismatch")
    if review.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee review input previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "committeeSubmissionExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "freezeExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if review.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if review.get("executionMode") != expected["executionMode"]:
        failures.append("committee review input executionMode mismatch")
    if review.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee review input preview must remain dryRunOnly=true")

    if source_data.get("committeeTriggerPackagePreviewStatus") != expected["sourceCommitteeTriggerPackagePreviewStatus"]:
        failures.append("source committee trigger package preview must remain candidate_preview")
    source_status_map = {
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source committee trigger package must remain dryRunOnly=true")
    if review.get("sourceCommitteeTriggerPackagePreviewId") != source.get("id"):
        failures.append("sourceCommitteeTriggerPackagePreviewId must match D46 preview id")
    if data.get("coveredCommitteeTriggerPackagePreviewStatus") != expected["coveredCommitteeTriggerPackagePreviewStatus"]:
        failures.append("coveredCommitteeTriggerPackagePreviewStatus mismatch")
    if data["coveredCommitteeTriggerPackagePreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee trigger package status must match D46 preview status")

    roles = set(review.get("intakeRoles", []))
    if len(roles) != expected["intakeRoleCount"]:
        failures.append("intakeRoleCount mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner",
        },
        "intake role",
        failures,
    )
    if roles != set(source.get("committeeRoutingRoles", [])):
        failures.append("intakeRoles must mirror D46 committeeRoutingRoles")

    sections = set(review.get("reviewInputSections", []))
    if len(sections) != expected["reviewInputSectionCount"]:
        failures.append("reviewInputSectionCount mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "committee_trigger_summary",
            "case_type_summary",
            "evidence_bundle_refs",
            "dispute_questions",
            "responsibility_questions",
            "freeze_retention_statement",
            "revenue_contribution_impact_questions",
            "formal_write_risk_questions",
            "waes_negative_gate_snapshot",
            "harness_review_constraints",
            "no_write_attestation",
        },
        "review input section",
        failures,
    )

    question_groups = set(review.get("reviewQuestionGroups", []))
    if len(question_groups) != expected["reviewQuestionGroupCount"]:
        failures.append("reviewQuestionGroupCount mismatch")
    decision_constraints = set(review.get("decisionConstraints", []))
    if len(decision_constraints) != expected["decisionConstraintCount"]:
        failures.append("decisionConstraintCount mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "committee_input_not_case",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_revenue_distribution",
            "no_contribution_score",
            "no_harness_evidence_write",
            "waes_gate_not_overridden",
        },
        "decision constraint",
        failures,
    )

    checks = set(review.get("reviewChecks", []))
    if len(checks) != expected["reviewCheckCount"]:
        failures.append("reviewCheckCount mismatch")
    require_all(
        checks,
        {
            "source_committee_trigger_package_preview_status_is_candidate_preview",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_committee_trigger_package_is_dry_run_only",
            "committee_review_input_preview_status_is_candidate_preview",
            "all_intake_roles_covered",
            "all_review_input_sections_covered",
            "all_review_question_groups_covered",
            "all_decision_constraints_covered",
            "assert_committee_input_not_submitted",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
        },
        "review check",
        failures,
    )

    refs = set(review.get("requiredReviewRefs", []))
    if len(refs) != expected["requiredReviewRefCount"]:
        failures.append("requiredReviewRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeTriggerPackagePreviewRef",
            "sourceHumanConfirmationPackagePreviewRef",
            "committeeTriggerSummaryRef",
            "caseTypeSummaryRef",
            "evidenceBundleRefs",
            "waesNegativeGateSnapshotRef",
            "harnessReviewConstraintRefs",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required review ref",
        failures,
    )

    if len(set(review.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(review.get("forbiddenActions", []))
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
        print("gckf_p0_formal_evidence_execution_committee_review_input_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_review_input_preview_dry_run=pass")
    print(f"status={review['previewStatus']}")
    print(f"execution_mode={review['executionMode']}")
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
