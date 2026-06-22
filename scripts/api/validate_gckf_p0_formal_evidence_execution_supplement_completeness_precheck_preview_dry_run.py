#!/usr/bin/env python3
"""Validate P0 supplement completeness precheck preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-supplement-completeness-precheck-preview-dry-run-v0.1.json"
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

    source_data = load_json(data["sourceExceptionReturnSupplementIntakePreview"])
    source = source_data["exceptionReturnSupplementIntakePreview"]
    precheck = data["supplementCompletenessPrecheckPreview"]

    if data.get("supplementCompletenessPrecheckPreviewStatus") != expected[
        "supplementCompletenessPrecheckPreviewStatus"
    ]:
        failures.append("supplementCompletenessPrecheckPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalCompletenessCheck") is not expected["notFinalCompletenessCheck"]:
        failures.append("precheck preview must state notFinalCompletenessCheck=true")
    if precheck.get("previewType") != expected["previewType"]:
        failures.append("precheck previewType mismatch")
    if precheck.get("previewStatus") != expected["previewStatus"]:
        failures.append("precheck previewStatus must remain candidate_preview")

    for key in (
        "executionStatus",
        "supplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus",
        "completenessPrecheckExecutionStatus",
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
        if precheck.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if precheck.get("executionMode") != expected["executionMode"]:
        failures.append("precheck preview executionMode mismatch")
    if precheck.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("precheck preview must remain dryRunOnly=true")

    if source_data.get("exceptionReturnSupplementIntakePreviewStatus") != expected[
        "sourceExceptionReturnSupplementIntakePreviewStatus"
    ]:
        failures.append("source supplement intake preview must remain candidate_preview")
    source_status_map = {
        "supplementIntakeExecutionStatus": "sourceSupplementIntakeExecutionStatus",
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
        failures.append("source supplement intake preview must remain dryRunOnly=true")
    if precheck.get("sourceExceptionReturnSupplementIntakePreviewId") != source.get("id"):
        failures.append("sourceExceptionReturnSupplementIntakePreviewId must match D55 preview id")
    if data.get("coveredExceptionReturnSupplementIntakePreviewStatus") != expected[
        "coveredExceptionReturnSupplementIntakePreviewStatus"
    ]:
        failures.append("coveredExceptionReturnSupplementIntakePreviewStatus mismatch")
    if data["coveredExceptionReturnSupplementIntakePreviewStatus"] != source.get("previewStatus"):
        failures.append("covered supplement intake status must match D55 preview status")

    roles = set(precheck.get("precheckRoles", []))
    if len(roles) != expected["precheckRoleCount"]:
        failures.append("precheckRoleCount mismatch")
    if roles != set(source.get("supplementIntakeRoles", [])):
        failures.append("precheckRoles must mirror D55 supplementIntakeRoles")

    sections = set(precheck.get("precheckSections", []))
    if len(sections) != expected["precheckSectionCount"]:
        failures.append("precheckSectionCount mismatch")
    require_all(
        sections,
        {
            "source_supplement_intake_lineage",
            "completeness_precheck_scope",
            "precheck_envelope_fields",
            "precheck_readiness_prerequisites",
            "required_material_candidate_matrix",
            "submitted_material_candidate_matrix",
            "gap_resolution_candidate_matrix",
            "candidate_reentry_eligibility_snapshot",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "precheck section",
        failures,
    )

    fields = set(precheck.get("precheckEnvelopeFields", []))
    if len(fields) != expected["precheckEnvelopeFieldCount"]:
        failures.append("precheckEnvelopeFieldCount mismatch")
    prerequisites = set(precheck.get("precheckReadinessPrerequisites", []))
    if len(prerequisites) != expected["precheckReadinessPrerequisiteCount"]:
        failures.append("precheckReadinessPrerequisiteCount mismatch")
    constraints = set(precheck.get("precheckDecisionConstraints", []))
    if len(constraints) != expected["precheckDecisionConstraintCount"]:
        failures.append("precheckDecisionConstraintCount mismatch")
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "precheck_preview_not_formal_completeness_check",
            "no_supplement_acceptance",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
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
            "source_supplement_intake_preview_status_is_candidate_preview",
            "source_supplement_intake_execution_status_is_not_executed",
            "source_committee_reentry_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_supplement_intake_preview_is_dry_run_only",
            "supplement_completeness_precheck_preview_status_is_candidate_preview",
            "all_precheck_roles_covered",
            "all_precheck_sections_covered",
            "all_precheck_envelope_fields_covered",
            "all_precheck_readiness_prerequisites_covered",
            "all_precheck_decision_constraints_covered",
            "required_material_candidate_matrix_present",
            "submitted_material_candidate_matrix_present",
            "gap_resolution_candidate_matrix_present",
            "candidate_reentry_eligibility_snapshot_present",
            "assert_precheck_preview_not_formal_completeness_check",
            "assert_committee_reentry_not_executed",
            "assert_committee_case_not_opened",
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
            "sourceExceptionReturnSupplementIntakePreviewRef",
            "sourceCommitteeCaseOpeningExceptionReturnPreviewRef",
            "completenessPrecheckScopeRef",
            "precheckEnvelopeFieldsRef",
            "precheckReadinessPrerequisitesRef",
            "requiredMaterialCandidateMatrixRef",
            "submittedMaterialCandidateMatrixRef",
            "gapResolutionCandidateMatrixRef",
            "candidateReentryEligibilitySnapshotRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
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
        "executesCompletenessPrecheck",
        "executesSupplementIntake",
        "acceptsSupplementMaterial",
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
        "execute_completeness_precheck",
        "execute_supplement_intake",
        "accept_supplement_material",
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
        print("gckf_p0_formal_evidence_execution_supplement_completeness_precheck_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_supplement_completeness_precheck_preview_dry_run=pass")
    print(f"status={precheck['previewStatus']}")
    print(f"execution_mode={precheck['executionMode']}")
    print("executes_completeness_precheck=0")
    print("executes_supplement_intake=0")
    print("accepts_supplement_material=0")
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
