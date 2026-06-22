#!/usr/bin/env python3
"""Validate P0 exception return supplement intake preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-exception-return-supplement-intake-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceCommitteeCaseOpeningExceptionReturnPreview"])
    source = source_data["committeeCaseOpeningExceptionReturnPreview"]
    supplement = data["exceptionReturnSupplementIntakePreview"]

    if data.get("exceptionReturnSupplementIntakePreviewStatus") != expected[
        "exceptionReturnSupplementIntakePreviewStatus"
    ]:
        failures.append("exceptionReturnSupplementIntakePreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalSupplementIntake") is not expected["notFinalSupplementIntake"]:
        failures.append("supplement intake preview must state notFinalSupplementIntake=true")
    if supplement.get("previewType") != expected["previewType"]:
        failures.append("supplement intake previewType mismatch")
    if supplement.get("previewStatus") != expected["previewStatus"]:
        failures.append("supplement intake previewStatus must remain candidate_preview")

    for key in (
        "executionStatus",
        "supplementIntakeExecutionStatus",
        "intakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus",
        "committeeReceiptExecutionStatus",
        "committeeRoutingExecutionStatus",
        "committeeExceptionReturnExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if supplement.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if supplement.get("executionMode") != expected["executionMode"]:
        failures.append("supplement intake preview executionMode mismatch")
    if supplement.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("supplement intake preview must remain dryRunOnly=true")

    if source_data.get("committeeCaseOpeningExceptionReturnPreviewStatus") != expected[
        "sourceCommitteeCaseOpeningExceptionReturnPreviewStatus"
    ]:
        failures.append("source committee case opening exception return preview must remain candidate_preview")
    source_status_map = {
        "intakeAcceptanceExecutionStatus": "sourceIntakeAcceptanceExecutionStatus",
        "committeeSubmissionExecutionStatus": "sourceCommitteeSubmissionExecutionStatus",
        "committeeDocketExecutionStatus": "sourceCommitteeDocketExecutionStatus",
        "committeeReceiptExecutionStatus": "sourceCommitteeReceiptExecutionStatus",
        "committeeRoutingExecutionStatus": "sourceCommitteeRoutingExecutionStatus",
        "committeeExceptionReturnExecutionStatus": "sourceCommitteeExceptionReturnExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source exception return preview must remain dryRunOnly=true")
    if supplement.get("sourceCommitteeCaseOpeningExceptionReturnPreviewId") != source.get("id"):
        failures.append("sourceCommitteeCaseOpeningExceptionReturnPreviewId must match D54 preview id")
    if data.get("coveredCommitteeCaseOpeningExceptionReturnPreviewStatus") != expected[
        "coveredCommitteeCaseOpeningExceptionReturnPreviewStatus"
    ]:
        failures.append("coveredCommitteeCaseOpeningExceptionReturnPreviewStatus mismatch")
    if data["coveredCommitteeCaseOpeningExceptionReturnPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered committee case opening exception return status must match D54 preview status")

    roles = set(supplement.get("supplementIntakeRoles", []))
    if len(roles) != expected["supplementIntakeRoleCount"]:
        failures.append("supplementIntakeRoleCount mismatch")
    if roles != set(source.get("returnRoles", [])):
        failures.append("supplementIntakeRoles must mirror D54 returnRoles")

    sections = set(supplement.get("supplementIntakeSections", []))
    if len(sections) != expected["supplementIntakeSectionCount"]:
        failures.append("supplementIntakeSectionCount mismatch")
    require_all(
        sections,
        {
            "source_exception_return_lineage",
            "supplement_intake_scope",
            "supplement_envelope_fields",
            "supplement_readiness_prerequisites",
            "supplement_material_candidates",
            "supplement_owner_candidates",
            "supplement_gap_resolution_candidates",
            "candidate_reentry_queue_path",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "supplement section",
        failures,
    )

    fields = set(supplement.get("supplementEnvelopeFields", []))
    if len(fields) != expected["supplementEnvelopeFieldCount"]:
        failures.append("supplementEnvelopeFieldCount mismatch")
    prerequisites = set(supplement.get("supplementReadinessPrerequisites", []))
    if len(prerequisites) != expected["supplementReadinessPrerequisiteCount"]:
        failures.append("supplementReadinessPrerequisiteCount mismatch")
    constraints = set(supplement.get("supplementDecisionConstraints", []))
    if len(constraints) != expected["supplementDecisionConstraintCount"]:
        failures.append("supplementDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "supplement_intake_preview_not_formal_intake",
            "no_supplement_acceptance",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_harness_evidence_write",
        },
        "supplement decision constraint",
        failures,
    )

    checks = set(supplement.get("supplementChecks", []))
    if len(checks) != expected["supplementCheckCount"]:
        failures.append("supplementCheckCount mismatch")
    require_all(
        checks,
        {
            "source_exception_return_preview_status_is_candidate_preview",
            "source_committee_exception_return_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_exception_return_preview_is_dry_run_only",
            "exception_return_supplement_intake_preview_status_is_candidate_preview",
            "all_supplement_intake_roles_covered",
            "all_supplement_intake_sections_covered",
            "all_supplement_envelope_fields_covered",
            "all_supplement_readiness_prerequisites_covered",
            "all_supplement_decision_constraints_covered",
            "supplement_material_candidates_present",
            "supplement_owner_candidates_present",
            "supplement_gap_resolution_candidates_present",
            "candidate_reentry_queue_path_present",
            "assert_supplement_intake_preview_not_formal_intake",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
        },
        "supplement check",
        failures,
    )

    refs = set(supplement.get("requiredSupplementRefs", []))
    if len(refs) != expected["requiredSupplementRefCount"]:
        failures.append("requiredSupplementRefCount mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseOpeningExceptionReturnPreviewRef",
            "sourceCommitteeReceiptAcknowledgementRoutingPreviewRef",
            "supplementIntakeScopeRef",
            "supplementEnvelopeFieldsRef",
            "supplementReadinessPrerequisitesRef",
            "supplementMaterialCandidatesRef",
            "supplementOwnerCandidatesRef",
            "supplementGapResolutionCandidatesRef",
            "candidateReentryQueuePathRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required supplement ref",
        failures,
    )

    if len(set(supplement.get("blockingConditions", []))) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(supplement.get("forbiddenActions", []))
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
        "executesSupplementIntake",
        "acceptsSupplementMaterial",
        "executesIntakeAcceptance",
        "submitsCommitteeCasePacket",
        "submitsCommitteeReviewInput",
        "createsCommitteeDocket",
        "recordsCommitteeReceipt",
        "executesCommitteeRouting",
        "executesCommitteeExceptionReturn",
        "executesCommitteeReentry",
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
        "execute_supplement_intake",
        "accept_supplement_material",
        "execute_intake_acceptance",
        "submit_committee_case_packet",
        "submit_committee_review_input",
        "create_committee_docket",
        "record_committee_receipt",
        "execute_committee_routing",
        "execute_committee_exception_return",
        "execute_committee_reentry",
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
        print("gckf_p0_formal_evidence_execution_exception_return_supplement_intake_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_exception_return_supplement_intake_preview_dry_run=pass")
    print(f"status={supplement['previewStatus']}")
    print(f"execution_mode={supplement['executionMode']}")
    print("executes_supplement_intake=0")
    print("accepts_supplement_material=0")
    print("executes_intake_acceptance=0")
    print("submits_committee_case_packet=0")
    print("submits_committee_review_input=0")
    print("creates_committee_docket=0")
    print("records_committee_receipt=0")
    print("executes_committee_routing=0")
    print("executes_committee_exception_return=0")
    print("executes_committee_reentry=0")
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
