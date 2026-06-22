#!/usr/bin/env python3
"""Validate P0 committee case review packet preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-case-review-packet-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeReviewInputPreview"])
    source = source_data["committeeReviewInputPreview"]
    packet = data["committeeCaseReviewPacketPreview"]

    if data.get("committeeCaseReviewPacketPreviewStatus") != expected["committeeCaseReviewPacketPreviewStatus"]:
        failures.append("committeeCaseReviewPacketPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("committee case review packet preview must state notFinalAcceptance=true")
    if packet.get("previewType") != expected["previewType"]:
        failures.append("committee case review packet previewType mismatch")
    if packet.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee case review packet previewStatus must remain candidate_preview")
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
        if packet.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if packet.get("executionMode") != expected["executionMode"]:
        failures.append("committee case review packet executionMode mismatch")
    if packet.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee case review packet preview must remain dryRunOnly=true")

    if source_data.get("committeeReviewInputPreviewStatus") != expected["sourceCommitteeReviewInputPreviewStatus"]:
        failures.append("source committee review input preview must remain candidate_preview")
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
        failures.append("source committee review input must remain dryRunOnly=true")
    if packet.get("sourceCommitteeReviewInputPreviewId") != source.get("id"):
        failures.append("sourceCommitteeReviewInputPreviewId must match D47 preview id")
    if data.get("coveredCommitteeReviewInputPreviewStatus") != expected["coveredCommitteeReviewInputPreviewStatus"]:
        failures.append("coveredCommitteeReviewInputPreviewStatus mismatch")
    if data["coveredCommitteeReviewInputPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee review input status must match D47 preview status")

    roles = set(packet.get("casePacketRoles", []))
    if len(roles) != expected["casePacketRoleCount"]:
        failures.append("casePacketRoleCount mismatch")
    if roles != set(source.get("intakeRoles", [])):
        failures.append("casePacketRoles must mirror D47 intakeRoles")

    sections = set(packet.get("casePacketSections", []))
    if len(sections) != expected["casePacketSectionCount"]:
        failures.append("casePacketSectionCount mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "committee_review_input_summary",
            "case_scope_summary",
            "case_type_matrix",
            "evidence_bundle_index",
            "reviewer_question_matrix",
            "responsibility_boundary",
            "freeze_retention_statement",
            "revenue_contribution_impact_summary",
            "formal_write_risk_summary",
            "waes_negative_gate_snapshot",
            "no_write_attestation",
        },
        "case packet section",
        failures,
    )

    question_groups = set(packet.get("casePacketQuestionGroups", []))
    if len(question_groups) != expected["casePacketQuestionGroupCount"]:
        failures.append("casePacketQuestionGroupCount mismatch")
    if question_groups != set(source.get("reviewQuestionGroups", [])):
        failures.append("casePacketQuestionGroups must mirror D47 reviewQuestionGroups")

    constraints = set(packet.get("casePacketDecisionConstraints", []))
    if len(constraints) != expected["casePacketDecisionConstraintCount"]:
        failures.append("casePacketDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "case_packet_not_case",
            "no_committee_submission",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_revenue_distribution",
            "no_contribution_score",
            "no_harness_evidence_write",
        },
        "case packet decision constraint",
        failures,
    )

    checks = set(packet.get("casePacketChecks", []))
    if len(checks) != expected["casePacketCheckCount"]:
        failures.append("casePacketCheckCount mismatch")
    require_all(
        checks,
        {
            "source_committee_review_input_preview_status_is_candidate_preview",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_committee_review_input_is_dry_run_only",
            "committee_case_review_packet_preview_status_is_candidate_preview",
            "all_case_packet_roles_covered",
            "all_case_packet_sections_covered",
            "all_case_packet_question_groups_covered",
            "all_case_packet_decision_constraints_covered",
            "assert_case_packet_not_submitted",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
        },
        "case packet check",
        failures,
    )

    refs = set(packet.get("requiredCasePacketRefs", []))
    if len(refs) != expected["requiredCasePacketRefCount"]:
        failures.append("requiredCasePacketRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeReviewInputPreviewRef",
            "sourceCommitteeTriggerPackagePreviewRef",
            "committeeReviewInputSummaryRef",
            "caseScopeSummaryRef",
            "caseTypeMatrixRef",
            "evidenceBundleIndexRef",
            "reviewerQuestionMatrixRef",
            "waesNegativeGateSnapshotRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required case packet ref",
        failures,
    )

    if len(set(packet.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(packet.get("forbiddenActions", []))
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
        print("gckf_p0_formal_evidence_execution_committee_case_review_packet_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_case_review_packet_preview_dry_run=pass")
    print(f"status={packet['previewStatus']}")
    print(f"execution_mode={packet['executionMode']}")
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
