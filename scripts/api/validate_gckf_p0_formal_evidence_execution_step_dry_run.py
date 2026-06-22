#!/usr/bin/env python3
"""Validate P0 formal evidence execution step dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-step-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_approval = load_json(data["sourceExecutionApproval"])
    approval = source_approval["approvalCandidate"]
    step = data["executionStep"]

    if data.get("executionStepStatus") != expected["executionStepStatus"]:
        failures.append("executionStepStatus must remain candidate_step")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if step.get("stepStatus") != expected["stepStatus"]:
        failures.append("stepStatus must remain candidate_step")
    if step.get("executionStatus") != expected["executionStatus"]:
        failures.append("executionStatus must remain not_executed")
    if step.get("executionMode") != expected["executionMode"]:
        failures.append("step executionMode mismatch")
    if step.get("stepType") != expected["stepType"]:
        failures.append("stepType mismatch")
    if step.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("execution step must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("execution step must state notFinalAcceptance=true")

    if source_approval.get("executionApprovalStatus") != expected["sourceExecutionApprovalStatus"]:
        failures.append("source execution approval must remain candidate_approval")
    if approval.get("executionStatus") != expected["sourceExecutionApprovalExecutionStatus"]:
        failures.append("source execution approval executionStatus must remain not_executed")
    if approval.get("dryRunOnly") is not True:
        failures.append("source execution approval must remain dryRunOnly=true")
    if step.get("sourceExecutionApprovalId") != approval.get("id"):
        failures.append("sourceExecutionApprovalId must match D33 approval id")
    if data.get("coveredApprovalOutcome") != expected["coveredApprovalOutcome"]:
        failures.append("coveredApprovalOutcome mismatch")
    if data["coveredApprovalOutcome"] != approval.get("approvalOutcome"):
        failures.append("covered approval outcome must match D33 approval outcome")

    required_inputs = set(step.get("requiredInputs", []))
    if len(required_inputs) != expected["requiredInputCount"]:
        failures.append("requiredInputCount mismatch")
    for required in {
        "executionApprovalRef",
        "executionRequestRef",
        "executorId",
        "scheduledAt",
        "authorityRef",
        "approvalOutcome",
        "evidenceRefs",
        "idempotencyKey",
        "duplicateCheckRef",
        "rollbackPlanRef",
        "executionLockRef",
        "auditTrailRef",
        "preWriteSnapshotRef",
        "postWriteVerificationPlanRef",
        "harnessEvidenceTargetRef",
    }:
        if required not in required_inputs:
            failures.append(f"missing required input: {required}")

    checks = set(step.get("stepChecks", []))
    if len(checks) != expected["stepCheckCount"]:
        failures.append("stepCheckCount mismatch")
    for check in {
        "source_execution_approval_status_is_candidate_approval",
        "source_execution_approval_execution_status_is_not_executed",
        "source_execution_approval_is_dry_run_only",
        "approval_outcome_is_approved_for_future_execution_step",
        "execution_mode_is_dry_run_no_write",
        "authority_ref_present",
        "evidence_refs_present",
        "idempotency_key_present",
        "duplicate_formal_evidence_absent",
        "rollback_plan_present",
        "execution_lock_present",
        "audit_trail_ref_present",
        "pre_write_snapshot_ref_present",
        "post_write_verification_plan_ref_present",
        "harness_evidence_target_ref_present",
        "formal_write_requires_separate_final_execution",
        "step_does_not_write_formal_evidence",
    }:
        if check not in checks:
            failures.append(f"missing step check: {check}")

    forbidden_actions = set(step.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "skip_post_write_verification",
        "bypass_duplicate_guard",
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
        "\"executionStepStatus\": \"accepted\"",
        "\"stepStatus\": \"executed\"",
        "\"executionStatus\": \"executed\"",
        "\"executionMode\": \"write\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden execution step term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_execution_step_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_execution_step_dry_run=pass "
        f"status={expected['executionStepStatus']} "
        f"step_type={expected['stepType']} "
        f"step_status={expected['stepStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"execution_mode={expected['executionMode']} "
        f"source_approval_status={expected['sourceExecutionApprovalStatus']} "
        f"source_approval_execution_status={expected['sourceExecutionApprovalExecutionStatus']} "
        f"covered_approval_outcome={expected['coveredApprovalOutcome']} "
        f"required_inputs={expected['requiredInputCount']} "
        f"step_checks={expected['stepCheckCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "pre_write_snapshot=covered "
        "post_write_verification_plan=covered "
        "separate_final_execution=covered "
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
