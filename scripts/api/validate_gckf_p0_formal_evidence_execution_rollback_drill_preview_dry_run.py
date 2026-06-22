#!/usr/bin/env python3
"""Validate P0 formal evidence execution rollback drill preview dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-rollback-drill-preview-dry-run-v0.1.json"
)


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_plan = load_json(data["sourceVerificationPlanPreview"])
    source = source_plan["verificationPlanPreview"]
    drill = data["rollbackDrillPreview"]

    if data.get("rollbackDrillPreviewStatus") != expected["rollbackDrillPreviewStatus"]:
        failures.append("rollbackDrillPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if drill.get("previewStatus") != expected["previewStatus"]:
        failures.append("rollback drill previewStatus must remain candidate_preview")
    if drill.get("executionStatus") != expected["executionStatus"]:
        failures.append("rollback drill executionStatus must remain not_executed")
    if drill.get("rollbackExecutionStatus") != expected["rollbackExecutionStatus"]:
        failures.append("rollbackExecutionStatus must remain not_executed")
    if drill.get("executionMode") != expected["executionMode"]:
        failures.append("rollback drill executionMode mismatch")
    if drill.get("previewType") != expected["previewType"]:
        failures.append("rollback drill previewType mismatch")
    if drill.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("rollback drill preview must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("rollback drill preview must state notFinalAcceptance=true")

    if source_plan.get("verificationPlanPreviewStatus") != expected["sourceVerificationPlanPreviewStatus"]:
        failures.append("source verification plan preview must remain candidate_preview")
    if source.get("executionStatus") != expected["sourceVerificationPlanExecutionStatus"]:
        failures.append("source verification plan executionStatus must remain not_executed")
    if source.get("dryRunOnly") is not True:
        failures.append("source verification plan must remain dryRunOnly=true")
    if drill.get("sourceVerificationPlanPreviewId") != source.get("id"):
        failures.append("sourceVerificationPlanPreviewId must match D38 plan preview id")
    if data.get("coveredVerificationPlanPreviewStatus") != expected["coveredVerificationPlanPreviewStatus"]:
        failures.append("coveredVerificationPlanPreviewStatus mismatch")
    if data["coveredVerificationPlanPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered verification plan preview status must match D38 preview status")

    triggers = set(drill.get("rollbackTriggers", []))
    if len(triggers) != expected["rollbackTriggerCount"]:
        failures.append("rollbackTriggerCount mismatch")
    for trigger in {
        "formal_write_partial_failure",
        "post_write_readback_mismatch",
        "harness_evidence_shape_invalid",
        "ledger_append_failed",
        "audit_trail_append_failed",
        "unexpected_accepted_lifecycle",
        "unexpected_kds_write",
        "unexpected_business_write",
    }:
        if trigger not in triggers:
            failures.append(f"missing rollback trigger: {trigger}")

    steps = set(drill.get("rollbackDrillSteps", []))
    if len(steps) != expected["rollbackDrillStepCount"]:
        failures.append("rollbackDrillStepCount mismatch")
    for step in {
        "confirm_source_verification_plan_preview_is_candidate_preview",
        "confirm_source_verification_plan_execution_status_is_not_executed",
        "confirm_source_verification_plan_is_dry_run_only",
        "acquire_rollback_drill_lock_preview",
        "verify_pre_write_snapshot_ref_available",
        "verify_execution_lock_ref_available",
        "verify_rollback_plan_ref_available",
        "simulate_formal_write_failure_condition",
        "simulate_post_write_readback_mismatch_condition",
        "simulate_harness_evidence_shape_invalid_condition",
        "simulate_ledger_append_failure_condition",
        "simulate_audit_trail_append_failure_condition",
        "preview_compensation_action_sequence",
        "preview_restore_from_pre_write_snapshot",
        "preview_revoke_unexpected_lifecycle_promotion",
        "preview_revoke_unexpected_kds_write",
        "preview_revoke_unexpected_business_write",
        "preview_post_rollback_readback_verification",
        "preview_rollback_audit_trail_append",
        "preview_escalation_to_human_review",
        "preview_escalation_to_committee_review",
        "preview_freeze_if_rollback_fails",
        "assert_rollback_not_executed",
        "assert_no_write_boundary",
    }:
        if step not in steps:
            failures.append(f"missing rollback drill step: {step}")

    refs = set(drill.get("requiredRollbackRefs", []))
    if len(refs) != expected["requiredRollbackRefCount"]:
        failures.append("requiredRollbackRefCount mismatch")
    for ref in {
        "sourceVerificationPlanPreviewRef",
        "sourceEvidencePreviewRef",
        "sourceRequestRef",
        "executionLockRef",
        "rollbackDrillLockRef",
        "preWriteSnapshotRef",
        "postWriteReadbackPlanRef",
        "rollbackPlanRef",
        "compensationActionPlanRef",
        "rollbackAuditTrailRef",
        "humanEscalationRef",
        "committeeEscalationRef",
        "freezeGateRef",
    }:
        if ref not in refs:
            failures.append(f"missing required rollback ref: {ref}")

    blocking_conditions = set(drill.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    for blocking in {
        "source_verification_plan_not_candidate_preview",
        "source_verification_plan_already_executed",
        "source_verification_plan_not_dry_run_only",
        "missing_source_verification_plan_ref",
        "missing_source_evidence_preview_ref",
        "missing_source_request_ref",
        "missing_execution_lock_ref",
        "missing_rollback_drill_lock_ref",
        "missing_pre_write_snapshot_ref",
        "missing_post_write_readback_plan_ref",
        "missing_rollback_plan_ref",
        "missing_compensation_action_plan_ref",
        "missing_rollback_audit_trail_ref",
        "missing_human_escalation_ref",
        "missing_committee_escalation_ref",
        "missing_freeze_gate_ref",
        "rollback_drill_already_executed",
        "rollback_drill_attempts_write",
    }:
        if blocking not in blocking_conditions:
            failures.append(f"missing blocking condition: {blocking}")

    forbidden_actions = set(drill.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "execute_formal_write",
        "execute_rollback",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_verification_result",
        "write_rollback_result",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "convert_drill_preview_to_result",
        "release_execution_lock",
    }:
        if forbidden not in forbidden_actions:
            failures.append(f"missing forbidden action: {forbidden}")

    if len(data.get("requiredSourceRefs", [])) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for source_ref in data.get("requiredSourceRefs", []):
        if not (ROOT / source_ref).exists():
            failures.append(f"missing required source ref: {source_ref}")

    for forbidden in [
        "formal_write_executed",
        "rollback_executed",
        "formal_harness_evidence_record_written",
        "harness_evidence_record_written",
        "verification_result_written",
        "rollback_result_written",
        "accepted",
        "integrated",
        "production_ready",
        "business_write_enabled",
        "kds_write_enabled",
        "drill_preview_converted_to_result",
        "execution_lock_released",
    ]:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")

    forbidden_terms = [
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesVerificationResult\": true",
        "\"writesRollbackResult\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"dryRunOnly\": false",
        "\"rollbackDrillPreviewStatus\": \"accepted\"",
        "\"previewStatus\": \"written\"",
        "\"executionStatus\": \"executed\"",
        "\"rollbackExecutionStatus\": \"executed\"",
        "\"executionMode\": \"write\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
        "\"verificationResultWritten\": true",
        "\"rollbackResultWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden rollback drill preview term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_execution_rollback_drill_preview_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_execution_rollback_drill_preview_dry_run=pass "
        f"status={expected['rollbackDrillPreviewStatus']} "
        f"preview_type={expected['previewType']} "
        f"preview_status={expected['previewStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"rollback_execution_status={expected['rollbackExecutionStatus']} "
        f"execution_mode={expected['executionMode']} "
        f"source_verification_plan_status={expected['sourceVerificationPlanPreviewStatus']} "
        f"source_verification_plan_execution_status={expected['sourceVerificationPlanExecutionStatus']} "
        f"covered_verification_plan_status={expected['coveredVerificationPlanPreviewStatus']} "
        f"rollback_triggers={expected['rollbackTriggerCount']} "
        f"rollback_drill_steps={expected['rollbackDrillStepCount']} "
        f"required_rollback_refs={expected['requiredRollbackRefCount']} "
        f"blocking_conditions={expected['blockingConditionCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "source_lineage=covered "
        "rollback_triggers=covered "
        "compensation_actions=covered "
        "post_rollback_readback=covered "
        "human_committee_escalation=covered "
        "freeze_if_rollback_fails=covered "
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
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
