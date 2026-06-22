#!/usr/bin/env python3
"""Validate P0 formal evidence execution request dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-request-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_preflight = load_json(data["sourceExecutionPreflight"])
    preflight = source_preflight["executionPreflight"]
    request = data["executionRequest"]

    if data.get("executionRequestStatus") != expected["executionRequestStatus"]:
        failures.append("executionRequestStatus must remain candidate")
    if request.get("requestStatus") != expected["requestStatus"]:
        failures.append("requestStatus must remain candidate")
    if request.get("executionStatus") != expected["executionStatus"]:
        failures.append("executionStatus must remain not_executed")
    if request.get("requestType") != expected["requestType"]:
        failures.append("requestType mismatch")
    if request.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("execution request must remain dryRunOnly=true")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("execution request must state notFinalAcceptance=true")

    if source_preflight.get("executionPreflightStatus") != expected["sourcePreflightStatus"]:
        failures.append("source preflight must remain candidate")
    if preflight.get("executionStatus") != expected["sourcePreflightExecutionStatus"]:
        failures.append("source preflight executionStatus must remain candidate")
    if request.get("sourcePreflightId") != preflight.get("id"):
        failures.append("sourcePreflightId must match D31 preflight id")
    if data.get("coveredDecisionOutcome") != expected["coveredDecisionOutcome"]:
        failures.append("coveredDecisionOutcome mismatch")
    if data["coveredDecisionOutcome"] != source_preflight.get("coveredDecisionOutcome"):
        failures.append("covered decision must match D31 preflight decision")

    required_inputs = set(request.get("requiredInputs", []))
    if len(required_inputs) != expected["requiredInputCount"]:
        failures.append("requiredInputCount mismatch")
    for required in {
        "preflightRef",
        "approvalDecisionRef",
        "executionRequestId",
        "requesterId",
        "requestedAt",
        "authorityRef",
        "evidenceRefs",
        "idempotencyKey",
        "duplicateCheckRef",
        "rollbackPlanRef",
        "executionLockRef",
        "auditTrailRef",
        "harnessReviewRouteRef",
    }:
        if required not in required_inputs:
            failures.append(f"missing required input: {required}")

    checks = set(request.get("requestChecks", []))
    if len(checks) != expected["requestCheckCount"]:
        failures.append("requestCheckCount mismatch")
    for check in {
        "source_preflight_status_is_candidate",
        "source_preflight_execution_status_is_candidate",
        "decision_outcome_is_approve_for_future_formal_write",
        "source_preflight_checks_satisfied",
        "approval_decision_ref_present",
        "authority_ref_present",
        "idempotency_key_present",
        "duplicate_formal_evidence_absent",
        "rollback_plan_present",
        "execution_lock_present",
        "audit_trail_ref_present",
        "harness_review_route_present",
        "request_requires_separate_execution_approval",
        "request_does_not_execute_formal_write",
    }:
        if check not in checks:
            failures.append(f"missing request check: {check}")

    forbidden_actions = set(request.get("forbiddenActions", []))
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
        "bypass_harness_review",
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
        "\"executionRequestStatus\": \"accepted\"",
        "\"requestStatus\": \"approved\"",
        "\"executionStatus\": \"executed\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden execution request term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_execution_request_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_execution_request_dry_run=pass "
        f"status={expected['executionRequestStatus']} "
        f"request_type={expected['requestType']} "
        f"request_status={expected['requestStatus']} "
        f"execution_status={expected['executionStatus']} "
        f"source_preflight_status={expected['sourcePreflightStatus']} "
        f"source_preflight_execution_status={expected['sourcePreflightExecutionStatus']} "
        f"covered_decision={expected['coveredDecisionOutcome']} "
        f"required_inputs={expected['requiredInputCount']} "
        f"request_checks={expected['requestCheckCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "dry_run_only=covered "
        "harness_review_route=covered "
        "separate_execution_approval=covered "
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
