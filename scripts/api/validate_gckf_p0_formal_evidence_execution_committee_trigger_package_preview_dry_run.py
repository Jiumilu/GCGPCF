#!/usr/bin/env python3
"""Validate P0 committee trigger package preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-trigger-package-preview-dry-run-v0.1.json"
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

    source_package_data = load_json(data["sourceHumanConfirmationPackagePreview"])
    source = source_package_data["humanConfirmationPackagePreview"]
    package = data["committeeTriggerPackagePreview"]

    if data.get("committeeTriggerPackagePreviewStatus") != expected["committeeTriggerPackagePreviewStatus"]:
        failures.append("committeeTriggerPackagePreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("committee trigger package preview must state notFinalAcceptance=true")
    if package.get("previewType") != expected["previewType"]:
        failures.append("committee trigger package previewType mismatch")
    if package.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee trigger package previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "freezeExecutionStatus",
        "unfreezeExecutionStatus",
        "resendExecutionStatus",
        "escalationExecutionStatus",
        "approvalExecutionStatus",
        "retryExecutionStatus",
    ):
        if package.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if package.get("executionMode") != expected["executionMode"]:
        failures.append("committee trigger package executionMode mismatch")
    if package.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee trigger package preview must remain dryRunOnly=true")

    if source_package_data.get("humanConfirmationPackagePreviewStatus") != expected["sourceHumanConfirmationPackagePreviewStatus"]:
        failures.append("source human confirmation package preview must remain candidate_preview")
    source_status_map = {
        "executionStatus": "sourceHumanConfirmationExecutionStatus",
        "committeeExecutionStatus": "sourceCommitteeExecutionStatus",
        "resendExecutionStatus": "sourceResendExecutionStatus",
        "escalationExecutionStatus": "sourceEscalationExecutionStatus",
        "approvalExecutionStatus": "sourceApprovalExecutionStatus",
        "retryExecutionStatus": "sourceRetryExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source human confirmation package must remain dryRunOnly=true")
    if package.get("sourceHumanConfirmationPackagePreviewId") != source.get("id"):
        failures.append("sourceHumanConfirmationPackagePreviewId must match D45 human confirmation package preview id")
    if data.get("coveredHumanConfirmationPackagePreviewStatus") != expected["coveredHumanConfirmationPackagePreviewStatus"]:
        failures.append("coveredHumanConfirmationPackagePreviewStatus mismatch")
    if data["coveredHumanConfirmationPackagePreviewStatus"] != source.get("previewStatus"):
        failures.append("covered human confirmation package preview status must match D45 preview status")

    roles = set(package.get("committeeRoutingRoles", []))
    if len(roles) != expected["committeeRoutingRoleCount"]:
        failures.append("committeeRoutingRoleCount mismatch")
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
        "committee routing role",
        failures,
    )

    case_types = set(package.get("committeeCaseTypes", []))
    if len(case_types) != expected["committeeCaseTypeCount"]:
        failures.append("committeeCaseTypeCount mismatch")
    require_all(
        case_types,
        {
            "cross_unit_responsibility_dispute",
            "freeze_release_dispute",
            "formal_write_risk",
            "revenue_or_contribution_impact",
            "major_violation_suspected",
        },
        "committee case type",
        failures,
    )
    if case_types != set(source.get("committeeTriggers", [])):
        failures.append("committeeCaseTypes must mirror D45 committeeTriggers")

    sections = set(package.get("packageSections", []))
    if len(sections) != expected["packageSectionCount"]:
        failures.append("packageSectionCount mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "human_confirmation_summary",
            "committee_trigger_summary",
            "dispute_boundary",
            "freeze_retention_boundary",
            "responsibility_boundary",
            "revenue_contribution_impact",
            "formal_write_risk_summary",
            "harness_review_input",
            "required_evidence_refs",
            "negative_gate_result",
            "no_write_attestation",
        },
        "package section",
        failures,
    )

    checks = set(package.get("triggerChecks", []))
    if len(checks) != expected["triggerCheckCount"]:
        failures.append("triggerCheckCount mismatch")
    require_all(
        checks,
        {
            "source_human_confirmation_package_preview_status_is_candidate_preview",
            "source_human_confirmation_execution_status_is_not_executed",
            "source_committee_execution_status_is_not_executed",
            "source_human_confirmation_package_is_dry_run_only",
            "committee_trigger_package_preview_status_is_candidate_preview",
            "all_committee_routing_roles_covered",
            "all_committee_case_types_covered",
            "harness_review_input_present",
            "major_violation_suspected_case_present",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
        },
        "trigger check",
        failures,
    )

    refs = set(package.get("requiredTriggerRefs", []))
    if len(refs) != expected["requiredTriggerRefCount"]:
        failures.append("requiredTriggerRefCount mismatch")
    require_all(
        refs,
        {
            "sourceHumanConfirmationPackagePreviewRef",
            "humanConfirmationSummaryRef",
            "committeeTriggerSummaryRef",
            "disputeBoundaryRef",
            "freezeRetentionBoundaryRef",
            "responsibilityBoundaryRef",
            "revenueContributionImpactRef",
            "formalWriteRiskSummaryRef",
            "harnessReviewInputRef",
            "requiredEvidenceRefs",
            "committeeRepresentativeRef",
            "governanceOwnerRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
        },
        "required trigger ref",
        failures,
    )

    blocking_conditions = set(package.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(package.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    forbidden_outputs = set(data.get("forbiddenOutputs", []))
    if len(forbidden_outputs) != expected["forbiddenOutputCount"]:
        failures.append("forbiddenOutputCount mismatch")
    required_sources = set(data.get("requiredSourceRefs", []))
    if len(required_sources) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for relative_path in required_sources:
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")

    for key in (
        "opensCommitteeCase",
        "executesCommitteeDecision",
        "executesHumanConfirmation",
        "releasesFreeze",
        "executesUnfreeze",
        "executesResend",
        "executesEscalation",
        "executesApproval",
        "executesRetry",
        "writesKds",
        "writesBusinessSystem",
        "writesHarnessEvidence",
        "writesFormalEvidence",
        "writesRevenueDistribution",
        "writesContributionScore",
    ):
        if expected[key] is not False:
            failures.append(f"{key} must be false in expectedSummary")

    forbidden_token_map = {
        "open_committee_case": "opensCommitteeCase",
        "execute_committee_decision": "executesCommitteeDecision",
        "execute_human_confirmation": "executesHumanConfirmation",
        "execute_freeze_release": "releasesFreeze",
        "execute_unfreeze": "executesUnfreeze",
        "execute_resend_dispatch": "executesResend",
        "execute_escalation": "executesEscalation",
        "execute_approval": "executesApproval",
        "execute_retry": "executesRetry",
        "write_kds": "writesKds",
        "write_business_system": "writesBusinessSystem",
        "write_harness_evidence": "writesHarnessEvidence",
        "write_formal_evidence": "writesFormalEvidence",
        "write_revenue_distribution": "writesRevenueDistribution",
        "write_contribution_score": "writesContributionScore",
    }
    for token in forbidden_token_map:
        if token not in forbidden_actions:
            failures.append(f"missing forbidden action token: {token}")

    if failures:
        print("gckf_p0_formal_evidence_execution_committee_trigger_package_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_trigger_package_preview_dry_run=pass")
    print(f"status={package['previewStatus']}")
    print(f"execution_mode={package['executionMode']}")
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
