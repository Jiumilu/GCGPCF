#!/usr/bin/env python3
"""Validate P0 repair request acknowledgement preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-repair-request-acknowledgement-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceSupplementPrecheckRepairRequestPreview"])
    source = source_data["supplementPrecheckRepairRequestPreview"]
    ack = data["repairRequestAcknowledgementPreview"]

    if data.get("repairRequestAcknowledgementPreviewStatus") != expected[
        "repairRequestAcknowledgementPreviewStatus"
    ]:
        failures.append("repairRequestAcknowledgementPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcknowledgement") is not expected["notFinalAcknowledgement"]:
        failures.append("acknowledgement preview must state notFinalAcknowledgement=true")
    if ack.get("previewType") != expected["previewType"]:
        failures.append("acknowledgement previewType mismatch")
    if ack.get("previewStatus") != expected["previewStatus"]:
        failures.append("acknowledgement previewStatus must remain candidate_preview")
    if ack.get("executionMode") != expected["executionMode"]:
        failures.append("acknowledgement preview executionMode mismatch")
    if ack.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("acknowledgement preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "acknowledgementExecutionStatus",
        "repairRequestExecutionStatus",
        "supplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if ack.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("supplementPrecheckRepairRequestPreviewStatus") != expected[
        "sourceSupplementPrecheckRepairRequestPreviewStatus"
    ]:
        failures.append("source supplement precheck repair request preview must remain candidate_preview")
    source_status_map = {
        "repairRequestExecutionStatus": "sourceRepairRequestExecutionStatus",
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
        failures.append("source repair request preview must remain dryRunOnly=true")
    if ack.get("sourceSupplementPrecheckRepairRequestPreviewId") != source.get("id"):
        failures.append("sourceSupplementPrecheckRepairRequestPreviewId must match D57 preview id")
    if data.get("coveredSupplementPrecheckRepairRequestPreviewStatus") != source.get("previewStatus"):
        failures.append("covered supplement precheck repair request status must match D57 preview status")

    if len(set(ack.get("acknowledgementRoles", []))) != expected["acknowledgementRoleCount"]:
        failures.append("acknowledgementRoleCount mismatch")
    if not set(source.get("repairRequestRoles", [])).issubset(set(ack.get("acknowledgementRoles", []))):
        failures.append("acknowledgementRoles must include D57 repairRequestRoles")
    if len(set(ack.get("acknowledgementSections", []))) != expected["acknowledgementSectionCount"]:
        failures.append("acknowledgementSectionCount mismatch")
    if len(set(ack.get("acknowledgementEnvelopeFields", []))) != expected["acknowledgementEnvelopeFieldCount"]:
        failures.append("acknowledgementEnvelopeFieldCount mismatch")
    if len(set(ack.get("acknowledgementReadinessPrerequisites", []))) != expected[
        "acknowledgementReadinessPrerequisiteCount"
    ]:
        failures.append("acknowledgementReadinessPrerequisiteCount mismatch")
    if len(set(ack.get("acknowledgementDecisionConstraints", []))) != expected[
        "acknowledgementDecisionConstraintCount"
    ]:
        failures.append("acknowledgementDecisionConstraintCount mismatch")
    if len(set(ack.get("acknowledgementChecks", []))) != expected["acknowledgementCheckCount"]:
        failures.append("acknowledgementCheckCount mismatch")
    if len(set(ack.get("requiredAcknowledgementRefs", []))) != expected["requiredAcknowledgementRefCount"]:
        failures.append("requiredAcknowledgementRefCount mismatch")
    if len(set(ack.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(ack.get("acknowledgementSections", [])),
        {
            "receipt_identifier_candidates",
            "acknowledgement_channel_candidates",
            "recipient_role_candidates",
            "response_due_window_candidates",
            "candidate_follow_up_path",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "acknowledgement section",
        failures,
    )
    require_all(
        set(ack.get("acknowledgementDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "acknowledgement_preview_not_formal_acknowledgement",
            "no_acknowledgement_execution",
            "no_repair_request_execution",
            "no_supplement_acceptance",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "acknowledgement constraint",
        failures,
    )
    require_all(
        set(ack.get("forbiddenActions", [])),
        {
            "execute_acknowledgement",
            "issue_formal_acknowledgement",
            "execute_repair_request",
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
        "executesAcknowledgement",
        "executesRepairRequest",
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
        print("gckf_p0_formal_evidence_execution_repair_request_acknowledgement_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_repair_request_acknowledgement_preview_dry_run=pass")
    print(f"status={ack['previewStatus']}")
    print(f"execution_mode={ack['executionMode']}")
    print("executes_acknowledgement=0")
    print("executes_repair_request=0")
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
