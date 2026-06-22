#!/usr/bin/env python3
"""Validate P0 committee receipt acknowledgement routing preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-receipt-acknowledgement-routing-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeCaseOpeningReceiptPreview"])
    source = source_data["committeeCaseOpeningReceiptPreview"]
    routing = data["committeeReceiptAcknowledgementRoutingPreview"]

    if (
        data.get("committeeReceiptAcknowledgementRoutingPreviewStatus")
        != expected["committeeReceiptAcknowledgementRoutingPreviewStatus"]
    ):
        failures.append("committeeReceiptAcknowledgementRoutingPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRouting") is not expected["notFinalRouting"]:
        failures.append("committee receipt acknowledgement routing preview must state notFinalRouting=true")
    if routing.get("previewType") != expected["previewType"]:
        failures.append("committee receipt acknowledgement routing previewType mismatch")
    if routing.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee receipt acknowledgement routing previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "intakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus",
        "committeeReceiptExecutionStatus",
        "committeeRoutingExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if routing.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if routing.get("executionMode") != expected["executionMode"]:
        failures.append("committee routing preview executionMode mismatch")
    if routing.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee routing preview must remain dryRunOnly=true")

    if source_data.get("committeeCaseOpeningReceiptPreviewStatus") != expected[
        "sourceCommitteeCaseOpeningReceiptPreviewStatus"
    ]:
        failures.append("source committee case opening receipt preview must remain candidate_preview")
    source_status_map = {
        "intakeAcceptanceExecutionStatus": "sourceIntakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus": "sourceCommitteeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus": "sourceCommitteeDocketExecutionStatus",
        "committeeReceiptExecutionStatus": "sourceCommitteeReceiptExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source receipt preview must remain dryRunOnly=true")
    if routing.get("sourceCommitteeCaseOpeningReceiptPreviewId") != source.get("id"):
        failures.append("sourceCommitteeCaseOpeningReceiptPreviewId must match D52 preview id")
    if data.get("coveredCommitteeCaseOpeningReceiptPreviewStatus") != expected[
        "coveredCommitteeCaseOpeningReceiptPreviewStatus"
    ]:
        failures.append("coveredCommitteeCaseOpeningReceiptPreviewStatus mismatch")
    if data["coveredCommitteeCaseOpeningReceiptPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee case opening receipt status must match D52 preview status")

    roles = set(routing.get("routingRoles", []))
    if len(roles) != expected["routingRoleCount"]:
        failures.append("routingRoleCount mismatch")
    if roles != set(source.get("receiptRoles", [])):
        failures.append("routingRoles must mirror D52 receiptRoles")

    sections = set(routing.get("routingSections", []))
    if len(sections) != expected["routingSectionCount"]:
        failures.append("routingSectionCount mismatch")
    require_all(
        sections,
        {
            "source_receipt_lineage",
            "acknowledgement_scope",
            "routing_envelope_fields",
            "routing_readiness_prerequisites",
            "recipient_role_matrix",
            "routing_path_candidates",
            "exception_return_candidates",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "routing section",
        failures,
    )

    fields = set(routing.get("routingEnvelopeFields", []))
    if len(fields) != expected["routingEnvelopeFieldCount"]:
        failures.append("routingEnvelopeFieldCount mismatch")
    prerequisites = set(routing.get("routingReadinessPrerequisites", []))
    if len(prerequisites) != expected["routingReadinessPrerequisiteCount"]:
        failures.append("routingReadinessPrerequisiteCount mismatch")
    constraints = set(routing.get("routingDecisionConstraints", []))
    if len(constraints) != expected["routingDecisionConstraintCount"]:
        failures.append("routingDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "routing_preview_not_formal_routing",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_formal_receipt_record",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_harness_evidence_write",
        },
        "routing decision constraint",
        failures,
    )

    checks = set(routing.get("routingChecks", []))
    if len(checks) != expected["routingCheckCount"]:
        failures.append("routingCheckCount mismatch")
    require_all(
        checks,
        {
            "source_receipt_preview_status_is_candidate_preview",
            "source_committee_docket_execution_status_is_not_executed",
            "source_committee_receipt_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_receipt_preview_is_dry_run_only",
            "committee_receipt_acknowledgement_routing_preview_status_is_candidate_preview",
            "all_routing_roles_covered",
            "all_routing_sections_covered",
            "all_routing_envelope_fields_covered",
            "all_routing_readiness_prerequisites_covered",
            "all_routing_decision_constraints_covered",
            "assert_routing_preview_not_formal_routing",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
        },
        "routing check",
        failures,
    )

    refs = set(routing.get("requiredRoutingRefs", []))
    if len(refs) != expected["requiredRoutingRefCount"]:
        failures.append("requiredRoutingRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseOpeningReceiptPreviewRef",
            "sourceCommitteeDocketReadinessPreviewRef",
            "acknowledgementScopeRef",
            "routingEnvelopeFieldsRef",
            "routingReadinessPrerequisitesRef",
            "recipientRoleMatrixRef",
            "routingPathCandidatesRef",
            "exceptionReturnCandidatesRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required routing ref",
        failures,
    )

    if len(set(routing.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(routing.get("forbiddenActions", []))
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
        print("gckf_p0_formal_evidence_execution_committee_receipt_acknowledgement_routing_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_receipt_acknowledgement_routing_preview_dry_run=pass")
    print(f"status={routing['previewStatus']}")
    print(f"execution_mode={routing['executionMode']}")
    print("executes_intake_acceptance=0")
    print("submits_committee_case_packet=0")
    print("submits_committee_review_input=0")
    print("creates_committee_docket=0")
    print("records_committee_receipt=0")
    print("executes_committee_routing=0")
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
