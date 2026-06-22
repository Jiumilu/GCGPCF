#!/usr/bin/env python3
"""Validate P0 formal evidence execution re-entry preflight preview dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-reentry-preflight-preview-dry-run-v0.1.json"
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

    source_escalation = load_json(data["sourceIncidentEscalationPreview"])
    source = source_escalation["incidentEscalationPreview"]
    reentry = data["reentryPreflightPreview"]

    if data.get("reentryPreflightPreviewStatus") != expected["reentryPreflightPreviewStatus"]:
        failures.append("reentryPreflightPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("reentry preflight preview must state notFinalAcceptance=true")
    if reentry.get("previewType") != expected["previewType"]:
        failures.append("reentry preflight previewType mismatch")
    if reentry.get("previewStatus") != expected["previewStatus"]:
        failures.append("reentry preflight previewStatus must remain candidate_preview")
    if reentry.get("executionStatus") != expected["executionStatus"]:
        failures.append("reentry preflight executionStatus must remain not_executed")
    if reentry.get("reentryExecutionStatus") != expected["reentryExecutionStatus"]:
        failures.append("reentryExecutionStatus must remain not_executed")
    if reentry.get("unfreezeExecutionStatus") != expected["unfreezeExecutionStatus"]:
        failures.append("unfreezeExecutionStatus must remain not_executed")
    if reentry.get("retryExecutionStatus") != expected["retryExecutionStatus"]:
        failures.append("retryExecutionStatus must remain not_executed")
    if reentry.get("executionMode") != expected["executionMode"]:
        failures.append("reentry preflight executionMode mismatch")
    if reentry.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("reentry preflight preview must remain dryRunOnly=true")

    if source_escalation.get("incidentEscalationPreviewStatus") != expected["sourceIncidentEscalationPreviewStatus"]:
        failures.append("source incident escalation preview must remain candidate_preview")
    if source.get("incidentExecutionStatus") != expected["sourceIncidentExecutionStatus"]:
        failures.append("source incidentExecutionStatus must remain not_executed")
    if source.get("freezeExecutionStatus") != expected["sourceFreezeExecutionStatus"]:
        failures.append("source freezeExecutionStatus must remain not_executed")
    if source.get("dryRunOnly") is not True:
        failures.append("source incident escalation must remain dryRunOnly=true")
    if reentry.get("sourceIncidentEscalationPreviewId") != source.get("id"):
        failures.append("sourceIncidentEscalationPreviewId must match D40 incident escalation preview id")
    if data.get("coveredIncidentEscalationPreviewStatus") != expected["coveredIncidentEscalationPreviewStatus"]:
        failures.append("coveredIncidentEscalationPreviewStatus mismatch")
    if data["coveredIncidentEscalationPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered incident escalation preview status must match D40 preview status")

    states = set(reentry.get("reentryAdmissionStates", []))
    if len(states) != expected["reentryAdmissionStateCount"]:
        failures.append("reentryAdmissionStateCount mismatch")
    require_all(
        states,
        {
            "repair_required",
            "repair_submitted",
            "repair_human_review_required",
            "repair_committee_review_required",
            "ready_for_reentry_candidate",
            "reentry_blocked",
        },
        "reentry admission state",
        failures,
    )

    checks = set(reentry.get("reentryPreflightChecks", []))
    if len(checks) != expected["reentryPreflightCheckCount"]:
        failures.append("reentryPreflightCheckCount mismatch")
    require_all(
        checks,
        {
            "source_incident_escalation_preview_status_is_candidate_preview",
            "source_incident_execution_status_is_not_executed",
            "source_freeze_execution_status_is_not_executed",
            "source_incident_escalation_is_dry_run_only",
            "repair_or_reopen_work_item_present",
            "repair_evidence_packet_present",
            "repair_evidence_shape_valid",
            "human_repair_review_packet_present",
            "committee_repair_review_packet_present",
            "stop_authority_release_packet_present",
            "freeze_release_candidate_packet_present",
            "execution_lock_renewal_candidate_present",
            "approval_refresh_candidate_present",
            "verification_plan_refresh_candidate_present",
            "rollback_drill_refresh_candidate_present",
            "incident_audit_trail_link_present",
            "harness_evidence_candidate_link_present",
            "waes_reentry_gate_candidate_present",
            "kwe_reentry_work_item_candidate_present",
            "notify_original_approvers_candidate_present",
            "assert_unfreeze_not_executed",
            "assert_retry_not_executed",
            "assert_no_write_boundary",
            "reentry_requires_future_harness_execution",
        },
        "reentry preflight check",
        failures,
    )

    refs = set(reentry.get("requiredReentryRefs", []))
    if len(refs) != expected["requiredReentryRefCount"]:
        failures.append("requiredReentryRefCount mismatch")
    require_all(
        refs,
        {
            "sourceIncidentEscalationPreviewRef",
            "sourceRollbackDrillPreviewRef",
            "sourceVerificationPlanPreviewRef",
            "repairOrReopenWorkItemRef",
            "repairEvidencePacketRef",
            "humanRepairReviewPacketRef",
            "committeeRepairReviewPacketRef",
            "stopAuthorityReleasePacketRef",
            "freezeReleaseCandidateRef",
            "executionLockRenewalCandidateRef",
            "approvalRefreshCandidateRef",
            "verificationPlanRefreshCandidateRef",
            "rollbackDrillRefreshCandidateRef",
            "incidentAuditTrailRef",
            "harnessEvidenceCandidateRef",
            "waesReentryGateCandidateRef",
            "kweReentryWorkItemCandidateRef",
        },
        "required reentry ref",
        failures,
    )

    blocking_conditions = set(reentry.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    require_all(
        blocking_conditions,
        {
            "source_incident_escalation_not_candidate_preview",
            "source_incident_already_executed",
            "source_freeze_already_executed",
            "source_incident_escalation_not_dry_run_only",
            "missing_source_incident_escalation_ref",
            "missing_repair_or_reopen_work_item_ref",
            "missing_repair_evidence_packet_ref",
            "missing_human_repair_review_packet_ref",
            "missing_committee_repair_review_packet_ref",
            "missing_stop_authority_release_packet_ref",
            "missing_freeze_release_candidate_ref",
            "missing_execution_lock_renewal_candidate_ref",
            "missing_approval_refresh_candidate_ref",
            "missing_verification_plan_refresh_candidate_ref",
            "missing_rollback_drill_refresh_candidate_ref",
            "missing_incident_audit_trail_ref",
            "missing_harness_evidence_candidate_ref",
            "missing_waes_reentry_gate_candidate_ref",
            "missing_kwe_reentry_work_item_candidate_ref",
            "reentry_preview_attempts_unfreeze",
            "reentry_preview_attempts_retry",
            "reentry_preview_attempts_write",
        },
        "blocking condition",
        failures,
    )

    forbidden_actions = set(reentry.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_formal_write",
            "execute_retry",
            "execute_unfreeze",
            "release_freeze",
            "release_execution_lock",
            "write_reentry_result",
            "write_repair_result",
            "write_freeze_release_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_verification_result",
            "write_rollback_result",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "mark_production_ready",
            "convert_reentry_preview_to_result",
        },
        "forbidden action",
        failures,
    )

    required_sources = set(data.get("requiredSourceRefs", []))
    if len(required_sources) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for relative_path in required_sources:
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")

    forbidden_outputs = set(data.get("forbiddenOutputs", []))
    forbidden_markers = {
        "formal_write_executed",
        "retry_executed",
        "unfreeze_executed",
        "freeze_released",
        "execution_lock_released",
        "reentry_result_written",
        "repair_result_written",
        "freeze_release_result_written",
        "formal_harness_evidence_record_written",
        "harness_evidence_record_written",
        "verification_result_written",
        "rollback_result_written",
        "accepted",
        "integrated",
        "production_ready",
        "business_write_enabled",
        "kds_write_enabled",
        "reentry_preview_converted_to_result",
    }
    require_all(forbidden_outputs, forbidden_markers, "forbidden output marker", failures)

    for key in (
        "writesFormalEvidence",
        "writesHarnessEvidence",
        "writesVerificationResult",
        "writesRollbackResult",
        "writesReentryResult",
        "writesRepairResult",
        "writesFreezeReleaseResult",
        "writesAcceptedLifecycle",
        "startsServer",
        "connectsDatabase",
        "callsExternalApi",
        "writesKds",
        "writesBusinessSystem",
    ):
        if expected[key] is not False:
            failures.append(f"expectedSummary.{key} must be false")
    if expected["noWrite"] is not True:
        failures.append("expectedSummary.noWrite must be true")

    if failures:
        print("gckf_p0_formal_evidence_execution_reentry_preflight_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "gckf_p0_formal_evidence_execution_reentry_preflight_preview_dry_run=pass "
        f"status={data['reentryPreflightPreviewStatus']} "
        f"preview_type={reentry['previewType']} "
        f"preview_status={reentry['previewStatus']} "
        f"execution_status={reentry['executionStatus']} "
        f"reentry_execution_status={reentry['reentryExecutionStatus']} "
        f"unfreeze_execution_status={reentry['unfreezeExecutionStatus']} "
        f"retry_execution_status={reentry['retryExecutionStatus']} "
        f"execution_mode={data['executionMode']} "
        f"source_incident_escalation_status={source_escalation['incidentEscalationPreviewStatus']} "
        f"source_incident_execution_status={source['incidentExecutionStatus']} "
        f"source_freeze_execution_status={source['freezeExecutionStatus']} "
        f"covered_incident_escalation_status={data['coveredIncidentEscalationPreviewStatus']} "
        f"reentry_admission_states={len(states)} "
        f"reentry_preflight_checks={len(checks)} "
        f"required_reentry_refs={len(refs)} "
        f"blocking_conditions={len(blocking_conditions)} "
        f"forbidden_actions={len(forbidden_actions)} "
        f"required_sources={len(required_sources)} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "repair_evidence_packet=covered "
        "freeze_release_candidate=covered "
        "approval_refresh_candidate=covered "
        "execution_lock_renewal=covered "
        "waes_kwe_reentry_gate=covered "
        "negative_no_write_boundary=covered "
        "starts_server=0 connects_database=0 calls_external_api=0 "
        "writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 writes_formal_evidence=0 "
        "writes_verification_result=0 writes_rollback_result=0 "
        "writes_reentry_result=0 writes_repair_result=0 writes_freeze_release_result=0 "
        "executes_unfreeze=0 executes_retry=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
