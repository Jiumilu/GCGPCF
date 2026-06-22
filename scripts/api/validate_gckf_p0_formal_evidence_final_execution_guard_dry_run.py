#!/usr/bin/env python3
"""Validate P0 formal evidence final execution guard dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-final-execution-guard-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_step = load_json(data["sourceExecutionStep"])
    step = source_step["executionStep"]
    guard = data["finalExecutionGuard"]

    if data.get("finalExecutionGuardStatus") != expected["finalExecutionGuardStatus"]:
        failures.append("finalExecutionGuardStatus must remain candidate_guard")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if guard.get("guardStatus") != expected["guardStatus"]:
        failures.append("guardStatus must remain candidate_guard")
    if guard.get("executionStatus") != expected["executionStatus"]:
        failures.append("executionStatus must remain not_executed")
    if guard.get("executionMode") != expected["executionMode"]:
        failures.append("guard executionMode mismatch")
    if guard.get("guardType") != expected["guardType"]:
        failures.append("guardType mismatch")
    if guard.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("final execution guard must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("final execution guard must state notFinalAcceptance=true")

    if source_step.get("executionStepStatus") != expected["sourceExecutionStepStatus"]:
        failures.append("source execution step must remain candidate_step")
    if step.get("executionStatus") != expected["sourceExecutionStepExecutionStatus"]:
        failures.append("source execution step executionStatus must remain not_executed")
    if step.get("dryRunOnly") is not True:
        failures.append("source execution step must remain dryRunOnly=true")
    if guard.get("sourceExecutionStepId") != step.get("id"):
        failures.append("sourceExecutionStepId must match D34 step id")
    if data.get("coveredStepStatus") != expected["coveredStepStatus"]:
        failures.append("coveredStepStatus mismatch")
    if data["coveredStepStatus"] != step.get("stepStatus"):
        failures.append("covered step status must match D34 step status")

    required_inputs = set(guard.get("requiredInputs", []))
    if len(required_inputs) != expected["requiredInputCount"]:
        failures.append("requiredInputCount mismatch")
    for required in {
        "executionStepRef",
        "executionApprovalRef",
        "executorId",
        "humanAuthorizationRef",
        "committeeAuthorizationRef",
        "freezeGateResultRef",
        "duplicateCheckRef",
        "idempotencyKey",
        "executionLockRef",
        "preWriteSnapshotRef",
        "postWriteVerificationPlanRef",
        "rollbackPlanRef",
        "auditTrailRef",
        "harnessEvidenceTargetRef",
        "formalEvidenceTargetRef",
        "noWriteBoundaryRef",
    }:
        if required not in required_inputs:
            failures.append(f"missing required input: {required}")

    checks = set(guard.get("guardChecks", []))
    if len(checks) != expected["guardCheckCount"]:
        failures.append("guardCheckCount mismatch")
    for check in {
        "source_execution_step_status_is_candidate_step",
        "source_execution_step_execution_status_is_not_executed",
        "source_execution_step_is_dry_run_only",
        "execution_mode_is_dry_run_no_write",
        "human_authorization_present",
        "committee_authorization_present",
        "freeze_gate_allows_future_execution",
        "duplicate_formal_evidence_absent",
        "idempotency_key_present",
        "execution_lock_present",
        "pre_write_snapshot_present",
        "post_write_verification_plan_present",
        "rollback_plan_present",
        "audit_trail_ref_present",
        "harness_evidence_target_ref_present",
        "formal_evidence_target_ref_present",
        "no_write_boundary_present",
        "formal_write_requires_separate_explicit_execution",
    }:
        if check not in checks:
            failures.append(f"missing guard check: {check}")

    blocking_conditions = set(guard.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    for blocking in {
        "missing_human_authorization",
        "missing_committee_authorization",
        "freeze_gate_blocked",
        "duplicate_formal_evidence_found",
        "idempotency_key_missing",
        "execution_lock_missing",
        "pre_write_snapshot_missing",
        "post_write_verification_plan_missing",
        "rollback_plan_missing",
        "audit_trail_missing",
        "formal_evidence_target_missing",
        "no_write_boundary_missing",
    }:
        if blocking not in blocking_conditions:
            failures.append(f"missing blocking condition: {blocking}")

    forbidden_actions = set(guard.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "bypass_freeze_gate",
        "bypass_human_authorization",
        "bypass_committee_authorization",
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
        "formal_harness_evidence_record_written",
        "harness_evidence_record_written",
        "formal_write_executed",
        "accepted",
        "integrated",
        "production_ready",
        "business_write_enabled",
        "kds_write_enabled",
        "freeze_gate_bypassed",
        "human_authorization_bypassed",
        "committee_authorization_bypassed",
    ]:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")

    forbidden_terms = [
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"dryRunOnly\": false",
        "\"finalExecutionGuardStatus\": \"accepted\"",
        "\"guardStatus\": \"passed\"",
        "\"executionStatus\": \"executed\"",
        "\"executionMode\": \"write\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden final execution guard term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_final_execution_guard_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_final_execution_guard_dry_run=pass "
        f"status={expected['finalExecutionGuardStatus']} "
        f"guard_type={expected['guardType']} "
        f"guard_status={expected['guardStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"execution_mode={expected['executionMode']} "
        f"source_step_status={expected['sourceExecutionStepStatus']} "
        f"source_step_execution_status={expected['sourceExecutionStepExecutionStatus']} "
        f"covered_step_status={expected['coveredStepStatus']} "
        f"required_inputs={expected['requiredInputCount']} "
        f"guard_checks={expected['guardCheckCount']} "
        f"blocking_conditions={expected['blockingConditionCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "human_authorization=covered "
        "committee_authorization=covered "
        "freeze_gate=covered "
        "duplicate_guard=covered "
        "separate_explicit_execution=covered "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "writes_formal_evidence=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
