#!/usr/bin/env python3
"""Validate P0 repair request intake acknowledgement preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-intake-acknowledgement-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceRepairRequestCompletenessPrecheck"])
    source = source_data["repairRequestCompletenessPrecheck"]
    acknowledgement = data["repairRequestIntakeAcknowledgementPreview"]
    failures: list[str] = []

    if data.get("repairRequestIntakeAcknowledgementPreviewStatus") != expected["repairRequestIntakeAcknowledgementPreviewStatus"]:
        failures.append("repairRequestIntakeAcknowledgementPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRepairRequestIntakeAcknowledgement") is not expected["notFinalRepairRequestIntakeAcknowledgement"]:
        failures.append("acknowledgement must state notFinalRepairRequestIntakeAcknowledgement=true")
    if acknowledgement.get("previewType") != expected["previewType"]:
        failures.append("repair request intake acknowledgement previewType mismatch")
    if acknowledgement.get("previewStatus") != expected["previewStatus"]:
        failures.append("repair request intake acknowledgement previewStatus must remain candidate_preview")
    if acknowledgement.get("executionMode") != expected["executionMode"]:
        failures.append("repair request intake acknowledgement executionMode mismatch")
    if acknowledgement.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("repair request intake acknowledgement must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "intakeAcknowledgementPreviewExecutionStatus",
        "intakeAcknowledgementExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if acknowledgement.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("repairRequestCompletenessPrecheckStatus") != expected["sourceRepairRequestCompletenessPrecheckStatus"]:
        failures.append("source repair request completeness precheck must remain candidate_preview")
    source_status_map = {
        "repairRequestCompletenessPrecheckPreviewExecutionStatus": "sourceRepairRequestCompletenessPrecheckPreviewExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus": "sourceRepairRequestCompletenessPrecheckExecutionStatus",
        "repairIntakeExecutionStatus": "sourceRepairIntakeExecutionStatus",
        "repairRequestCreationStatus": "sourceRepairRequestCreationStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source repair request completeness precheck must remain dryRunOnly=true")
    if acknowledgement.get("sourceRepairRequestCompletenessPrecheckId") != source.get("id"):
        failures.append("sourceRepairRequestCompletenessPrecheckId must match D75 precheck id")
    if data.get("coveredRepairRequestCompletenessPrecheckStatus") != source.get("previewStatus"):
        failures.append("covered completeness precheck status must match D75 precheck status")

    count_checks = {
        "acknowledgementRoles": "acknowledgementRoleCount",
        "acknowledgementSections": "acknowledgementSectionCount",
        "candidateAcknowledgementFields": "candidateAcknowledgementFieldCount",
        "acknowledgementReadinessPrerequisites": "acknowledgementReadinessPrerequisiteCount",
        "acknowledgementDecisionConstraints": "acknowledgementDecisionConstraintCount",
        "acknowledgementChecks": "acknowledgementCheckCount",
        "requiredAcknowledgementRefs": "requiredAcknowledgementRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(acknowledgement.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(acknowledgement.get("acknowledgementSections", [])),
        {
            "candidate_receipt_acknowledgement_summary",
            "candidate_precheck_result_snapshot",
            "candidate_missing_material_gap_snapshot",
            "candidate_submitter_notification_boundary",
            "candidate_acl_visibility_boundary",
            "candidate_next_action_hint",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "repair request intake acknowledgement section",
        failures,
    )
    require_all(
        set(acknowledgement.get("acknowledgementDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "acknowledgement_not_formal_acceptance",
            "no_intake_acknowledgement_preview_execution",
            "no_intake_acknowledgement_execution",
            "no_repair_request_completeness_precheck_execution",
            "no_repair_intake_execution",
            "no_repair_request_creation",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "repair request intake acknowledgement constraint",
        failures,
    )
    require_all(
        set(acknowledgement.get("forbiddenActions", [])),
        {
            "execute_intake_acknowledgement",
            "execute_repair_request_completeness_precheck",
            "execute_repair_intake",
            "create_repair_request",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
        },
        "forbidden action",
        failures,
    )
    for relative_path in data.get("requiredSourceRefs", []):
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")
    for key in (
        "executesIntakeAcknowledgementPreview",
        "executesIntakeAcknowledgement",
        "executesRepairRequestCompletenessPrecheck",
        "executesRepairIntake",
        "createsRepairRequest",
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

    if failures:
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_intake_acknowledgement_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_intake_acknowledgement_preview_dry_run=pass")
    print(f"status={acknowledgement['previewStatus']}")
    print(f"execution_mode={acknowledgement['executionMode']}")
    print("executes_intake_acknowledgement_preview=0")
    print("executes_intake_acknowledgement=0")
    print("executes_repair_request_completeness_precheck=0")
    print("executes_repair_intake=0")
    print("creates_repair_request=0")
    print("opens_committee_case=0")
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
