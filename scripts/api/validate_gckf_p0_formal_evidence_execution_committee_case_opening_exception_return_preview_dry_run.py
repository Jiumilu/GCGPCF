#!/usr/bin/env python3
"""Validate P0 committee case opening exception return preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-case-opening-exception-return-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeReceiptAcknowledgementRoutingPreview"])
    source = source_data["committeeReceiptAcknowledgementRoutingPreview"]
    return_preview = data["committeeCaseOpeningExceptionReturnPreview"]

    if (
        data.get("committeeCaseOpeningExceptionReturnPreviewStatus")
        != expected["committeeCaseOpeningExceptionReturnPreviewStatus"]
    ):
        failures.append("committeeCaseOpeningExceptionReturnPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalReturn") is not expected["notFinalReturn"]:
        failures.append("committee case opening exception return preview must state notFinalReturn=true")
    if return_preview.get("previewType") != expected["previewType"]:
        failures.append("committee case opening exception return previewType mismatch")
    if return_preview.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee case opening exception return previewStatus must remain candidate_preview")

    for key in (
        "executionStatus",
        "intakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus",
        "committeeReceiptExecutionStatus",
        "committeeRoutingExecutionStatus",
        "committeeExceptionReturnExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if return_preview.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if return_preview.get("executionMode") != expected["executionMode"]:
        failures.append("committee exception return preview executionMode mismatch")
    if return_preview.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee exception return preview must remain dryRunOnly=true")

    if source_data.get("committeeReceiptAcknowledgementRoutingPreviewStatus") != expected[
        "sourceCommitteeReceiptAcknowledgementRoutingPreviewStatus"
    ]:
        failures.append("source committee receipt acknowledgement routing preview must remain candidate_preview")
    source_status_map = {
        "intakeAcceptanceExecutionStatus": "sourceIntakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus": "sourceCommitteeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus": "sourceCommitteeDocketExecutionStatus",
        "committeeReceiptExecutionStatus": "sourceCommitteeReceiptExecutionStatus",
        "committeeRoutingExecutionStatus": "sourceCommitteeRoutingExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source routing preview must remain dryRunOnly=true")
    if return_preview.get("sourceCommitteeReceiptAcknowledgementRoutingPreviewId") != source.get("id"):
        failures.append("sourceCommitteeReceiptAcknowledgementRoutingPreviewId must match D53 preview id")
    if data.get("coveredCommitteeReceiptAcknowledgementRoutingPreviewStatus") != expected[
        "coveredCommitteeReceiptAcknowledgementRoutingPreviewStatus"
    ]:
        failures.append("coveredCommitteeReceiptAcknowledgementRoutingPreviewStatus mismatch")
    if data["coveredCommitteeReceiptAcknowledgementRoutingPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee receipt acknowledgement routing status must match D53 preview status")

    roles = set(return_preview.get("returnRoles", []))
    if len(roles) != expected["returnRoleCount"]:
        failures.append("returnRoleCount mismatch")
    if roles != set(source.get("routingRoles", [])):
        failures.append("returnRoles must mirror D53 routingRoles")

    sections = set(return_preview.get("returnSections", []))
    if len(sections) != expected["returnSectionCount"]:
        failures.append("returnSectionCount mismatch")
    require_all(
        sections,
        {
            "source_routing_lineage",
            "exception_return_scope",
            "return_envelope_fields",
            "return_readiness_prerequisites",
            "return_reason_candidates",
            "responsible_role_candidates",
            "supplement_request_candidates",
            "reentry_path_candidates",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "return section",
        failures,
    )

    fields = set(return_preview.get("returnEnvelopeFields", []))
    if len(fields) != expected["returnEnvelopeFieldCount"]:
        failures.append("returnEnvelopeFieldCount mismatch")
    prerequisites = set(return_preview.get("returnReadinessPrerequisites", []))
    if len(prerequisites) != expected["returnReadinessPrerequisiteCount"]:
        failures.append("returnReadinessPrerequisiteCount mismatch")
    constraints = set(return_preview.get("returnDecisionConstraints", []))
    if len(constraints) != expected["returnDecisionConstraintCount"]:
        failures.append("returnDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "return_preview_not_formal_return",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_formal_receipt_record",
            "no_formal_routing_execution",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_harness_evidence_write",
        },
        "return decision constraint",
        failures,
    )

    checks = set(return_preview.get("returnChecks", []))
    if len(checks) != expected["returnCheckCount"]:
        failures.append("returnCheckCount mismatch")
    require_all(
        checks,
        {
            "source_routing_preview_status_is_candidate_preview",
            "source_committee_routing_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_routing_preview_is_dry_run_only",
            "committee_case_opening_exception_return_preview_status_is_candidate_preview",
            "all_return_roles_covered",
            "all_return_sections_covered",
            "all_return_envelope_fields_covered",
            "all_return_readiness_prerequisites_covered",
            "all_return_decision_constraints_covered",
            "return_reason_candidates_present",
            "responsible_role_candidates_present",
            "supplement_request_candidates_present",
            "reentry_path_candidates_present",
            "assert_return_preview_not_formal_return",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
        },
        "return check",
        failures,
    )

    refs = set(return_preview.get("requiredReturnRefs", []))
    if len(refs) != expected["requiredReturnRefCount"]:
        failures.append("requiredReturnRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeReceiptAcknowledgementRoutingPreviewRef",
            "sourceCommitteeCaseOpeningReceiptPreviewRef",
            "exceptionReturnScopeRef",
            "returnEnvelopeFieldsRef",
            "returnReadinessPrerequisitesRef",
            "returnReasonCandidatesRef",
            "responsibleRoleCandidatesRef",
            "supplementRequestCandidatesRef",
            "reentryPathCandidatesRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required return ref",
        failures,
    )

    if len(set(return_preview.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(return_preview.get("forbiddenActions", []))
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
        "executesCommitteeRouting",
        "executesCommitteeExceptionReturn",
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
        "execute_committee_routing",
        "execute_committee_exception_return",
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
        print("gckf_p0_formal_evidence_execution_committee_case_opening_exception_return_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_case_opening_exception_return_preview_dry_run=pass")
    print(f"status={return_preview['previewStatus']}")
    print(f"execution_mode={return_preview['executionMode']}")
    print("executes_intake_acceptance=0")
    print("submits_committee_case_packet=0")
    print("submits_committee_review_input=0")
    print("creates_committee_docket=0")
    print("records_committee_receipt=0")
    print("executes_committee_routing=0")
    print("executes_committee_exception_return=0")
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
