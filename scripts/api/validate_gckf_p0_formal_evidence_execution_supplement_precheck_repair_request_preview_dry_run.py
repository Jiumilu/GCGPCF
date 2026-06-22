#!/usr/bin/env python3
"""Validate P0 supplement precheck repair request preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-supplement-precheck-repair-request-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceSupplementCompletenessPrecheckPreview"])
    source = source_data["supplementCompletenessPrecheckPreview"]
    repair = data["supplementPrecheckRepairRequestPreview"]

    if data.get("supplementPrecheckRepairRequestPreviewStatus") != expected[
        "supplementPrecheckRepairRequestPreviewStatus"
    ]:
        failures.append("supplementPrecheckRepairRequestPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRepairRequest") is not expected["notFinalRepairRequest"]:
        failures.append("repair request preview must state notFinalRepairRequest=true")
    if repair.get("previewType") != expected["previewType"]:
        failures.append("repair request previewType mismatch")
    if repair.get("previewStatus") != expected["previewStatus"]:
        failures.append("repair request previewStatus must remain candidate_preview")
    if repair.get("executionMode") != expected["executionMode"]:
        failures.append("repair request preview executionMode mismatch")
    if repair.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("repair request preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "repairRequestExecutionStatus",
        "completenessPrecheckExecutionStatus",
        "supplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if repair.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("supplementCompletenessPrecheckPreviewStatus") != expected[
        "sourceSupplementCompletenessPrecheckPreviewStatus"
    ]:
        failures.append("source supplement completeness precheck preview must remain candidate_preview")
    source_status_map = {
        "completenessPrecheckExecutionStatus": "sourceCompletenessPrecheckExecutionStatus",
        "supplementIntakeExecutionStatus": "sourceSupplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus": "sourceSupplementAcceptanceExecutionStatus",
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
        failures.append("source precheck preview must remain dryRunOnly=true")
    if repair.get("sourceSupplementCompletenessPrecheckPreviewId") != source.get("id"):
        failures.append("sourceSupplementCompletenessPrecheckPreviewId must match D56 preview id")
    if data.get("coveredSupplementCompletenessPrecheckPreviewStatus") != source.get("previewStatus"):
        failures.append("covered supplement completeness precheck status must match D56 preview status")

    if len(set(repair.get("repairRequestRoles", []))) != expected["repairRequestRoleCount"]:
        failures.append("repairRequestRoleCount mismatch")
    if set(repair.get("repairRequestRoles", [])) != set(source.get("precheckRoles", [])):
        failures.append("repairRequestRoles must mirror D56 precheckRoles")
    if len(set(repair.get("repairRequestSections", []))) != expected["repairRequestSectionCount"]:
        failures.append("repairRequestSectionCount mismatch")
    if len(set(repair.get("repairRequestEnvelopeFields", []))) != expected["repairRequestEnvelopeFieldCount"]:
        failures.append("repairRequestEnvelopeFieldCount mismatch")
    if len(set(repair.get("repairRequestReadinessPrerequisites", []))) != expected[
        "repairRequestReadinessPrerequisiteCount"
    ]:
        failures.append("repairRequestReadinessPrerequisiteCount mismatch")
    if len(set(repair.get("repairRequestDecisionConstraints", []))) != expected["repairRequestDecisionConstraintCount"]:
        failures.append("repairRequestDecisionConstraintCount mismatch")
    if len(set(repair.get("repairRequestChecks", []))) != expected["repairRequestCheckCount"]:
        failures.append("repairRequestCheckCount mismatch")
    if len(set(repair.get("requiredRepairRequestRefs", []))) != expected["requiredRepairRequestRefCount"]:
        failures.append("requiredRepairRequestRefCount mismatch")
    if len(set(repair.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(repair.get("repairRequestSections", [])),
        {
            "gap_reference_candidates",
            "repair_reason_candidates",
            "responsible_role_candidates",
            "required_supplement_candidates",
            "candidate_recheck_path",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "repair request section",
        failures,
    )
    require_all(
        set(repair.get("repairRequestDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "repair_request_preview_not_formal_repair_request",
            "no_repair_request_execution",
            "no_supplement_acceptance",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "repair request constraint",
        failures,
    )
    require_all(
        set(repair.get("forbiddenActions", [])),
        {
            "execute_repair_request",
            "execute_completeness_precheck",
            "execute_supplement_intake",
            "accept_supplement_material",
            "execute_committee_reentry",
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
        "executesRepairRequest",
        "executesCompletenessPrecheck",
        "executesSupplementIntake",
        "acceptsSupplementMaterial",
        "executesCommitteeReentry",
        "opensCommitteeCase",
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
        print("gckf_p0_formal_evidence_execution_supplement_precheck_repair_request_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_supplement_precheck_repair_request_preview_dry_run=pass")
    print(f"status={repair['previewStatus']}")
    print(f"execution_mode={repair['executionMode']}")
    print("executes_repair_request=0")
    print("executes_completeness_precheck=0")
    print("executes_supplement_intake=0")
    print("accepts_supplement_material=0")
    print("executes_committee_reentry=0")
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
