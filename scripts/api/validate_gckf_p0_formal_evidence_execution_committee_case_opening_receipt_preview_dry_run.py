#!/usr/bin/env python3
"""Validate P0 committee case opening receipt preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-case-opening-receipt-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeDocketReadinessPreview"])
    source = source_data["committeeDocketReadinessPreview"]
    receipt = data["committeeCaseOpeningReceiptPreview"]

    if data.get("committeeCaseOpeningReceiptPreviewStatus") != expected["committeeCaseOpeningReceiptPreviewStatus"]:
        failures.append("committeeCaseOpeningReceiptPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalReceipt") is not expected["notFinalReceipt"]:
        failures.append("committee case opening receipt preview must state notFinalReceipt=true")
    if receipt.get("previewType") != expected["previewType"]:
        failures.append("committee case opening receipt previewType mismatch")
    if receipt.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee case opening receipt previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "intakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus",
        "committeeReceiptExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if receipt.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if receipt.get("executionMode") != expected["executionMode"]:
        failures.append("committee receipt preview executionMode mismatch")
    if receipt.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee receipt preview must remain dryRunOnly=true")

    if source_data.get("committeeDocketReadinessPreviewStatus") != expected["sourceCommitteeDocketReadinessPreviewStatus"]:
        failures.append("source committee docket readiness preview must remain candidate_preview")
    source_status_map = {
        "intakeAcceptanceExecutionStatus": "sourceIntakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus": "sourceCommitteeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus": "sourceCommitteeDocketExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source docket readiness preview must remain dryRunOnly=true")
    if receipt.get("sourceCommitteeDocketReadinessPreviewId") != source.get("id"):
        failures.append("sourceCommitteeDocketReadinessPreviewId must match D51 preview id")
    if data.get("coveredCommitteeDocketReadinessPreviewStatus") != expected[
        "coveredCommitteeDocketReadinessPreviewStatus"
    ]:
        failures.append("coveredCommitteeDocketReadinessPreviewStatus mismatch")
    if data["coveredCommitteeDocketReadinessPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee docket readiness status must match D51 preview status")

    roles = set(receipt.get("receiptRoles", []))
    if len(roles) != expected["receiptRoleCount"]:
        failures.append("receiptRoleCount mismatch")
    if roles != set(source.get("docketRoles", [])):
        failures.append("receiptRoles must mirror D51 docketRoles")

    sections = set(receipt.get("receiptSections", []))
    if len(sections) != expected["receiptSectionCount"]:
        failures.append("receiptSectionCount mismatch")
    require_all(
        sections,
        {
            "source_docket_readiness_lineage",
            "receipt_scope",
            "receipt_envelope_fields",
            "receipt_readiness_prerequisites",
            "material_index_acknowledgement",
            "reviewer_assignment_acknowledgement",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "return_to_docket_readiness_path",
            "no_write_attestation",
        },
        "receipt section",
        failures,
    )

    fields = set(receipt.get("receiptEnvelopeFields", []))
    if len(fields) != expected["receiptEnvelopeFieldCount"]:
        failures.append("receiptEnvelopeFieldCount mismatch")
    prerequisites = set(receipt.get("receiptReadinessPrerequisites", []))
    if len(prerequisites) != expected["receiptReadinessPrerequisiteCount"]:
        failures.append("receiptReadinessPrerequisiteCount mismatch")
    constraints = set(receipt.get("receiptDecisionConstraints", []))
    if len(constraints) != expected["receiptDecisionConstraintCount"]:
        failures.append("receiptDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "receipt_preview_not_formal_receipt",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_harness_evidence_write",
        },
        "receipt decision constraint",
        failures,
    )

    checks = set(receipt.get("receiptChecks", []))
    if len(checks) != expected["receiptCheckCount"]:
        failures.append("receiptCheckCount mismatch")
    require_all(
        checks,
        {
            "source_docket_readiness_preview_status_is_candidate_preview",
            "source_committee_docket_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_docket_readiness_is_dry_run_only",
            "committee_case_opening_receipt_preview_status_is_candidate_preview",
            "all_receipt_roles_covered",
            "all_receipt_sections_covered",
            "all_receipt_envelope_fields_covered",
            "all_receipt_readiness_prerequisites_covered",
            "all_receipt_decision_constraints_covered",
            "assert_receipt_preview_not_formal_receipt",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
        },
        "receipt check",
        failures,
    )

    refs = set(receipt.get("requiredReceiptRefs", []))
    if len(refs) != expected["requiredReceiptRefCount"]:
        failures.append("requiredReceiptRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeDocketReadinessPreviewRef",
            "sourceCommitteeCaseOpeningGuardPreviewRef",
            "receiptScopeRef",
            "receiptEnvelopeFieldsRef",
            "receiptReadinessPrerequisitesRef",
            "materialIndexAcknowledgementRef",
            "reviewerAssignmentAcknowledgementRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "returnToDocketReadinessPathRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required receipt ref",
        failures,
    )

    if len(set(receipt.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(receipt.get("forbiddenActions", []))
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
        "recordsCommitteeReceipt",
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
        "record_committee_receipt",
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
        print("gckf_p0_formal_evidence_execution_committee_case_opening_receipt_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_case_opening_receipt_preview_dry_run=pass")
    print(f"status={receipt['previewStatus']}")
    print(f"execution_mode={receipt['executionMode']}")
    print("executes_intake_acceptance=0")
    print("submits_committee_case_packet=0")
    print("submits_committee_review_input=0")
    print("creates_committee_docket=0")
    print("records_committee_receipt=0")
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
