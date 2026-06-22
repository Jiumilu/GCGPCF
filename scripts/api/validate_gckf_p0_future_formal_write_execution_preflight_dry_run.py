#!/usr/bin/env python3
"""Validate P0 future formal write execution preflight dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-future-formal-write-execution-preflight-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_intake = load_json(data["sourceReviewIntake"])
    intake = source_intake["intake"]
    preflight = data["executionPreflight"]

    if data.get("executionPreflightStatus") != expected["executionPreflightStatus"]:
        failures.append("executionPreflightStatus must remain candidate")
    if preflight.get("executionStatus") != expected["executionStatus"]:
        failures.append("executionStatus must remain candidate")
    if preflight.get("preflightType") != expected["preflightType"]:
        failures.append("preflightType mismatch")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("execution preflight must state notFinalAcceptance=true")

    if source_intake.get("intakeStatus") != expected["sourceIntakeStatus"]:
        failures.append("source intake must remain candidate")
    if intake.get("reviewStatus") != expected["sourceIntakeReviewStatus"]:
        failures.append("source intake reviewStatus must remain pending")
    if preflight.get("sourceIntakeId") != intake.get("id"):
        failures.append("sourceIntakeId must match D30 intake id")
    if data.get("coveredDecisionOutcome") != expected["coveredDecisionOutcome"]:
        failures.append("coveredDecisionOutcome mismatch")
    if data["coveredDecisionOutcome"] not in intake.get("allowedDecisionOutcomes", []):
        failures.append("covered decision must be allowed by D30 intake")

    required_inputs = set(preflight.get("requiredInputs", []))
    if len(required_inputs) != expected["requiredInputCount"]:
        failures.append("requiredInputCount mismatch")
    for required in {
        "reviewerId",
        "reviewedAt",
        "sourcePacketRef",
        "approvalDecisionRef",
        "authorityRef",
        "evidenceRefs",
        "idempotencyKey",
        "duplicateCheckRef",
        "rollbackPlanRef",
        "executionLockRef",
        "auditTrailRef",
    }:
        if required not in required_inputs:
            failures.append(f"missing required input: {required}")

    checks = set(preflight.get("preflightChecks", []))
    if len(checks) != expected["preflightCheckCount"]:
        failures.append("preflightCheckCount mismatch")
    for check in {
        "source_intake_status_is_candidate",
        "source_intake_review_status_is_pending",
        "decision_outcome_is_approve_for_future_formal_write",
        "approval_decision_ref_present",
        "authority_ref_present",
        "idempotency_key_present",
        "duplicate_formal_evidence_absent",
        "rollback_plan_present",
        "execution_lock_present",
        "audit_trail_ref_present",
        "formal_write_requires_next_explicit_execution",
    }:
        if check not in checks:
            failures.append(f"missing preflight check: {check}")

    forbidden_actions = set(preflight.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    for forbidden in {
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "skip_execution_preflight",
    }:
        if forbidden not in forbidden_actions:
            failures.append(f"missing forbidden action: {forbidden}")

    if len(data.get("requiredSourceRefs", [])) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for source_ref in data.get("requiredSourceRefs", []):
        if not (ROOT / source_ref).exists():
            failures.append(f"missing required source ref: {source_ref}")

    for forbidden in ["accepted", "integrated", "production_ready", "business_write_enabled", "kds_write_enabled"]:
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
        "\"executionPreflightStatus\": \"accepted\"",
        "\"executionStatus\": \"executed\"",
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden execution preflight term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_future_formal_write_execution_preflight_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_future_formal_write_execution_preflight_dry_run=pass "
        f"status={expected['executionPreflightStatus']} "
        f"preflight_type={expected['preflightType']} "
        f"execution_status={expected['executionStatus']} "
        f"source_intake_status={expected['sourceIntakeStatus']} "
        f"source_intake_review_status={expected['sourceIntakeReviewStatus']} "
        f"covered_decision={expected['coveredDecisionOutcome']} "
        f"required_inputs={expected['requiredInputCount']} "
        f"preflight_checks={expected['preflightCheckCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "execution_lock=covered "
        "audit_trail=covered "
        "future_formal_write_separate=covered "
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
