#!/usr/bin/env python3
"""Validate P0 repair response deadline monitor preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-repair-response-deadline-monitor-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceRepairRequestAcknowledgementPreview"])
    source = source_data["repairRequestAcknowledgementPreview"]
    monitor = data["repairResponseDeadlineMonitorPreview"]

    if data.get("repairResponseDeadlineMonitorPreviewStatus") != expected[
        "repairResponseDeadlineMonitorPreviewStatus"
    ]:
        failures.append("repairResponseDeadlineMonitorPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalDeadlineMonitor") is not expected["notFinalDeadlineMonitor"]:
        failures.append("deadline monitor preview must state notFinalDeadlineMonitor=true")
    if monitor.get("previewType") != expected["previewType"]:
        failures.append("deadline monitor previewType mismatch")
    if monitor.get("previewStatus") != expected["previewStatus"]:
        failures.append("deadline monitor previewStatus must remain candidate_preview")
    if monitor.get("executionMode") != expected["executionMode"]:
        failures.append("deadline monitor preview executionMode mismatch")
    if monitor.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("deadline monitor preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "deadlineMonitorExecutionStatus",
        "acknowledgementExecutionStatus",
        "reminderExecutionStatus",
        "escalationExecutionStatus",
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
        if monitor.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("repairRequestAcknowledgementPreviewStatus") != expected[
        "sourceRepairRequestAcknowledgementPreviewStatus"
    ]:
        failures.append("source repair request acknowledgement preview must remain candidate_preview")
    source_status_map = {
        "acknowledgementExecutionStatus": "sourceAcknowledgementExecutionStatus",
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
        failures.append("source acknowledgement preview must remain dryRunOnly=true")
    if monitor.get("sourceAcknowledgementPreviewId") != source.get("id"):
        failures.append("sourceAcknowledgementPreviewId must match D58 preview id")
    if data.get("coveredRepairRequestAcknowledgementPreviewStatus") != source.get("previewStatus"):
        failures.append("covered acknowledgement preview status must match D58 preview status")

    if len(set(monitor.get("deadlineMonitorRoles", []))) != expected["deadlineMonitorRoleCount"]:
        failures.append("deadlineMonitorRoleCount mismatch")
    if "deadline_monitor_owner" not in set(monitor.get("deadlineMonitorRoles", [])):
        failures.append("deadline_monitor_owner must be present")
    if not set(source.get("acknowledgementRoles", [])).issubset(set(monitor.get("deadlineMonitorRoles", []))):
        failures.append("deadlineMonitorRoles must include D58 acknowledgementRoles")
    if len(set(monitor.get("deadlineMonitorSections", []))) != expected["deadlineMonitorSectionCount"]:
        failures.append("deadlineMonitorSectionCount mismatch")
    if len(set(monitor.get("deadlineMonitorEnvelopeFields", []))) != expected["deadlineMonitorEnvelopeFieldCount"]:
        failures.append("deadlineMonitorEnvelopeFieldCount mismatch")
    if len(set(monitor.get("deadlineMonitorReadinessPrerequisites", []))) != expected[
        "deadlineMonitorReadinessPrerequisiteCount"
    ]:
        failures.append("deadlineMonitorReadinessPrerequisiteCount mismatch")
    if len(set(monitor.get("deadlineMonitorDecisionConstraints", []))) != expected[
        "deadlineMonitorDecisionConstraintCount"
    ]:
        failures.append("deadlineMonitorDecisionConstraintCount mismatch")
    if len(set(monitor.get("deadlineMonitorChecks", []))) != expected["deadlineMonitorCheckCount"]:
        failures.append("deadlineMonitorCheckCount mismatch")
    if len(set(monitor.get("requiredDeadlineMonitorRefs", []))) != expected["requiredDeadlineMonitorRefCount"]:
        failures.append("requiredDeadlineMonitorRefCount mismatch")
    if len(set(monitor.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(monitor.get("deadlineMonitorSections", [])),
        {
            "response_due_window_candidates",
            "watch_window_candidates",
            "reminder_candidate_matrix",
            "escalation_candidate_matrix",
            "candidate_follow_up_path",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "deadline monitor section",
        failures,
    )
    require_all(
        set(monitor.get("deadlineMonitorDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "deadline_monitor_preview_not_formal_monitor",
            "no_deadline_monitor_execution",
            "no_reminder_execution",
            "no_escalation_execution",
            "no_acknowledgement_execution",
            "no_harness_evidence_write",
        },
        "deadline monitor constraint",
        failures,
    )
    require_all(
        set(monitor.get("forbiddenActions", [])),
        {
            "execute_deadline_monitor",
            "send_reminder",
            "execute_escalation",
            "execute_acknowledgement",
            "execute_repair_request",
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
        "executesDeadlineMonitor",
        "sendsReminder",
        "executesEscalation",
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
        print("gckf_p0_formal_evidence_execution_repair_response_deadline_monitor_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_repair_response_deadline_monitor_preview_dry_run=pass")
    print(f"status={monitor['previewStatus']}")
    print(f"execution_mode={monitor['executionMode']}")
    print("executes_deadline_monitor=0")
    print("sends_reminder=0")
    print("executes_escalation=0")
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
