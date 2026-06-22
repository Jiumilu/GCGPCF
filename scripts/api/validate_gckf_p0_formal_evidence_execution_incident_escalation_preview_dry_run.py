#!/usr/bin/env python3
"""Validate P0 formal evidence execution incident escalation preview dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-incident-escalation-preview-dry-run-v0.1.json"
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

    source_drill = load_json(data["sourceRollbackDrillPreview"])
    source = source_drill["rollbackDrillPreview"]
    escalation = data["incidentEscalationPreview"]

    if data.get("incidentEscalationPreviewStatus") != expected["incidentEscalationPreviewStatus"]:
        failures.append("incidentEscalationPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if escalation.get("previewStatus") != expected["previewStatus"]:
        failures.append("incident escalation previewStatus must remain candidate_preview")
    if escalation.get("executionStatus") != expected["executionStatus"]:
        failures.append("incident escalation executionStatus must remain not_executed")
    if escalation.get("incidentExecutionStatus") != expected["incidentExecutionStatus"]:
        failures.append("incidentExecutionStatus must remain not_executed")
    if escalation.get("freezeExecutionStatus") != expected["freezeExecutionStatus"]:
        failures.append("freezeExecutionStatus must remain not_executed")
    if escalation.get("executionMode") != expected["executionMode"]:
        failures.append("incident escalation executionMode mismatch")
    if escalation.get("previewType") != expected["previewType"]:
        failures.append("incident escalation previewType mismatch")
    if escalation.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("incident escalation preview must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("incident escalation preview must state notFinalAcceptance=true")

    if source_drill.get("rollbackDrillPreviewStatus") != expected["sourceRollbackDrillPreviewStatus"]:
        failures.append("source rollback drill preview must remain candidate_preview")
    if source.get("executionStatus") != expected["sourceRollbackDrillExecutionStatus"]:
        failures.append("source rollback drill executionStatus must remain not_executed")
    if source.get("rollbackExecutionStatus") != expected["sourceRollbackExecutionStatus"]:
        failures.append("source rollbackExecutionStatus must remain not_executed")
    if source.get("dryRunOnly") is not True:
        failures.append("source rollback drill must remain dryRunOnly=true")
    if escalation.get("sourceRollbackDrillPreviewId") != source.get("id"):
        failures.append("sourceRollbackDrillPreviewId must match D39 rollback drill preview id")
    if data.get("coveredRollbackDrillPreviewStatus") != expected["coveredRollbackDrillPreviewStatus"]:
        failures.append("coveredRollbackDrillPreviewStatus mismatch")
    if data["coveredRollbackDrillPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered rollback drill preview status must match D39 preview status")

    incident_classes = set(escalation.get("incidentClasses", []))
    if len(incident_classes) != expected["incidentClassCount"]:
        failures.append("incidentClassCount mismatch")
    require_all(
        incident_classes,
        {
            "formal_write_failure",
            "verification_failure",
            "rollback_failure",
            "unexpected_kds_write",
            "unexpected_business_write",
            "unexpected_lifecycle_promotion",
            "evidence_shape_violation",
            "audit_trail_violation",
        },
        "incident class",
        failures,
    )

    severity_levels = set(escalation.get("severityLevels", []))
    if len(severity_levels) != expected["severityLevelCount"]:
        failures.append("severityLevelCount mismatch")
    require_all(
        severity_levels,
        {"S0_info", "S1_minor", "S2_major", "S3_critical", "S4_stop_authority_required"},
        "severity level",
        failures,
    )

    freeze_scopes = set(escalation.get("freezeScopes", []))
    if len(freeze_scopes) != expected["freezeScopeCount"]:
        failures.append("freezeScopeCount mismatch")
    require_all(
        freeze_scopes,
        {
            "source_request",
            "candidate_evidence",
            "execution_lock",
            "kds_object",
            "writeback_candidate",
            "rag_admission",
            "contribution_revenue_effects",
            "external_share",
        },
        "freeze scope",
        failures,
    )

    checks = set(escalation.get("escalationChecks", []))
    if len(checks) != expected["escalationCheckCount"]:
        failures.append("escalationCheckCount mismatch")
    require_all(
        checks,
        {
            "source_rollback_drill_preview_status_is_candidate_preview",
            "source_rollback_drill_execution_status_is_not_executed",
            "source_rollback_execution_status_is_not_executed",
            "source_rollback_drill_is_dry_run_only",
            "incident_preview_status_is_candidate_preview",
            "execution_mode_is_dry_run_no_write",
            "classify_incident_from_execution_or_verification_or_rollback_failure",
            "map_incident_class_to_severity",
            "map_severity_to_freeze_scope",
            "map_severity_to_human_review_required",
            "map_severity_to_committee_review_required",
            "map_severity_to_stop_authority_required",
            "preview_freeze_request_packet",
            "preview_human_review_packet",
            "preview_committee_review_packet",
            "preview_stop_authority_packet",
            "preview_notification_targets",
            "preview_audit_trail_entry",
            "preview_harness_evidence_candidate_link",
            "preview_repair_or_reopen_work_item",
            "assert_incident_not_written",
            "assert_freeze_not_executed",
            "assert_no_write_boundary",
            "incident_escalation_requires_future_harness_execution",
        },
        "escalation check",
        failures,
    )

    refs = set(escalation.get("requiredEscalationRefs", []))
    if len(refs) != expected["requiredEscalationRefCount"]:
        failures.append("requiredEscalationRefCount mismatch")
    require_all(
        refs,
        {
            "sourceRollbackDrillPreviewRef",
            "sourceVerificationPlanPreviewRef",
            "sourceEvidencePreviewRef",
            "sourceRequestRef",
            "executionLockRef",
            "freezeGateRef",
            "humanEscalationRef",
            "committeeEscalationRef",
            "stopAuthorityRef",
            "notificationTargetRefs",
            "incidentAuditTrailRef",
            "harnessEvidenceCandidateRef",
            "repairOrReopenWorkItemRef",
        },
        "required escalation ref",
        failures,
    )

    blocking_conditions = set(escalation.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    require_all(
        blocking_conditions,
        {
            "source_rollback_drill_not_candidate_preview",
            "source_rollback_drill_already_executed",
            "source_rollback_already_executed",
            "source_rollback_drill_not_dry_run_only",
            "missing_source_rollback_drill_ref",
            "missing_source_verification_plan_ref",
            "missing_source_evidence_preview_ref",
            "missing_source_request_ref",
            "missing_execution_lock_ref",
            "missing_freeze_gate_ref",
            "missing_human_escalation_ref",
            "missing_committee_escalation_ref",
            "missing_stop_authority_ref",
            "missing_notification_targets",
            "missing_incident_audit_trail_ref",
            "missing_harness_evidence_candidate_ref",
            "missing_repair_or_reopen_work_item_ref",
            "incident_preview_attempts_write",
            "freeze_preview_attempts_execution",
        },
        "blocking condition",
        failures,
    )

    forbidden_actions = set(escalation.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_formal_write",
            "execute_rollback",
            "execute_freeze",
            "write_incident_result",
            "write_freeze_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_verification_result",
            "write_rollback_result",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "mark_production_ready",
            "convert_escalation_preview_to_result",
            "release_execution_lock",
        },
        "forbidden action",
        failures,
    )

    if len(data.get("requiredSourceRefs", [])) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for source_ref in data.get("requiredSourceRefs", []):
        if not (ROOT / source_ref).exists():
            failures.append(f"missing required source ref: {source_ref}")

    for forbidden in [
        "formal_write_executed",
        "rollback_executed",
        "freeze_executed",
        "incident_result_written",
        "freeze_result_written",
        "formal_harness_evidence_record_written",
        "harness_evidence_record_written",
        "verification_result_written",
        "rollback_result_written",
        "accepted",
        "integrated",
        "production_ready",
        "business_write_enabled",
        "kds_write_enabled",
        "escalation_preview_converted_to_result",
        "execution_lock_released",
    ]:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")

    forbidden_terms = [
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesVerificationResult\": true",
        "\"writesRollbackResult\": true",
        "\"writesIncidentResult\": true",
        "\"writesFreezeResult\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"dryRunOnly\": false",
        "\"incidentEscalationPreviewStatus\": \"accepted\"",
        "\"previewStatus\": \"written\"",
        "\"executionStatus\": \"executed\"",
        "\"incidentExecutionStatus\": \"executed\"",
        "\"freezeExecutionStatus\": \"executed\"",
        "\"executionMode\": \"write\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
        "\"incidentResultWritten\": true",
        "\"freezeResultWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden incident escalation preview term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_execution_incident_escalation_preview_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_execution_incident_escalation_preview_dry_run=pass "
        f"status={expected['incidentEscalationPreviewStatus']} "
        f"preview_type={expected['previewType']} "
        f"preview_status={expected['previewStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"incident_execution_status={expected['incidentExecutionStatus']} "
        f"freeze_execution_status={expected['freezeExecutionStatus']} "
        f"execution_mode={expected['executionMode']} "
        f"source_rollback_drill_status={expected['sourceRollbackDrillPreviewStatus']} "
        f"source_rollback_drill_execution_status={expected['sourceRollbackDrillExecutionStatus']} "
        f"source_rollback_execution_status={expected['sourceRollbackExecutionStatus']} "
        f"covered_rollback_drill_status={expected['coveredRollbackDrillPreviewStatus']} "
        f"incident_classes={expected['incidentClassCount']} "
        f"severity_levels={expected['severityLevelCount']} "
        f"freeze_scopes={expected['freezeScopeCount']} "
        f"escalation_checks={expected['escalationCheckCount']} "
        f"required_escalation_refs={expected['requiredEscalationRefCount']} "
        f"blocking_conditions={expected['blockingConditionCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "incident_classes=covered "
        "severity_mapping=covered "
        "freeze_scope_preview=covered "
        "human_committee_stop_authority=covered "
        "notification_targets=covered "
        "repair_reopen_work_item=covered "
        "negative_no_write_boundary=covered "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "writes_formal_evidence=0 "
        "writes_verification_result=0 "
        "writes_rollback_result=0 "
        "writes_incident_result=0 "
        "writes_freeze_result=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
