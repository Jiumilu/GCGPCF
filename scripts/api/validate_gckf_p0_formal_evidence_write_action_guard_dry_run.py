#!/usr/bin/env python3
"""Validate P0 formal evidence write action guard dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-write-action-guard-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_preflight = load_json(data["sourceApprovalPreflight"])
    source_checklist = source_preflight["preflightChecklist"]
    guarded_action = data["guardedAction"]
    candidate_request = data["candidateWriteRequest"]

    if data.get("guardStatus") != expected["guardStatus"]:
        failures.append("guardStatus must remain candidate")
    if guarded_action.get("guardStatus") != expected["guardStatus"]:
        failures.append("guarded action status must remain candidate")
    if guarded_action.get("actionType") != expected["actionType"]:
        failures.append("actionType mismatch")
    if guarded_action.get("outputType") != expected["outputType"]:
        failures.append("outputType must remain candidate_write_request")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("guard must state notFinalAcceptance=true")

    if source_preflight.get("preflightStatus") != expected["sourcePreflightStatus"]:
        failures.append("source preflight must remain candidate")
    if source_checklist.get("preflightType") != expected["sourcePreflightType"]:
        failures.append("source preflight type mismatch")
    if data.get("coveredPreflightType") != source_checklist.get("preflightType"):
        failures.append("coveredPreflightType must match D27 preflight type")
    if guarded_action.get("sourcePreflightId") != source_checklist.get("id"):
        failures.append("sourcePreflightId must match D27 preflight id")

    source_required_fields = set(source_checklist.get("requiredFields", []))
    required_inputs = set(guarded_action.get("requiredInputs", []))
    if len(required_inputs) != expected["requiredInputCount"]:
        failures.append("requiredInputCount mismatch")
    if not source_required_fields.issubset(required_inputs):
        failures.append("guard requiredInputs must include D27 required fields")
    for required in {"approvalPreflightRef", "idempotencyKey", "writeAuthorityRef", "rollbackPlanRef"}:
        if required not in required_inputs:
            failures.append(f"missing required guard input: {required}")

    guard_checks = set(guarded_action.get("guardChecks", []))
    if len(guard_checks) != expected["guardCheckCount"]:
        failures.append("guardCheckCount mismatch")
    required_checks = {
        "approved_decision_outcome_only",
        "reviewer_authority_present",
        "idempotency_key_present",
        "duplicate_formal_evidence_absent",
        "rollback_plan_present",
        "formal_write_requires_explicit_harness_governance_execution",
        "no_business_writeback_in_same_action",
    }
    if not required_checks.issubset(guard_checks):
        failures.append("guard checks must cover approval, authority, idempotency, duplicate, rollback, separate execution, and no business writeback")

    forbidden_actions = set(guarded_action.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    required_forbidden = {
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "bypass_harness_governance",
    }
    if not required_forbidden.issubset(forbidden_actions):
        failures.append("forbidden actions incomplete")

    if candidate_request.get("requestStatus") != "candidate":
        failures.append("candidate write request must remain candidate")
    if candidate_request.get("formalEvidenceWritten") is not expected["formalEvidenceWritten"]:
        failures.append("formalEvidenceWritten must remain false")
    if candidate_request.get("harnessEvidenceWritten") is not expected["harnessEvidenceWritten"]:
        failures.append("harnessEvidenceWritten must remain false")
    for flag in [
        "requiresSeparateHarnessExecution",
        "requiresHumanOrHarnessGovernanceReviewer",
        "requiresIdempotencyKey",
        "requiresRollbackPlan",
    ]:
        if candidate_request.get(flag) is not True:
            failures.append(f"{flag} must be true")

    if len(data.get("requiredSourceRefs", [])) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for source_ref in data.get("requiredSourceRefs", []):
        if not (ROOT / source_ref).exists():
            failures.append(f"missing required source ref: {source_ref}")

    for forbidden in ["accepted", "integrated", "production_ready", "business_write_enabled", "kds_write_enabled"]:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")

    forbidden_terms = [
        "\"formalEvidenceWritten\": true",
        "\"harnessEvidenceWritten\": true",
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"guardStatus\": \"accepted\"",
        "\"requestStatus\": \"accepted\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden guard term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_formal_evidence_write_action_guard_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_formal_evidence_write_action_guard_dry_run=pass "
        f"status={expected['guardStatus']} "
        f"action_type={expected['actionType']} "
        f"output_type={expected['outputType']} "
        f"source_preflight_status={expected['sourcePreflightStatus']} "
        f"source_preflight_type={expected['sourcePreflightType']} "
        f"required_inputs={expected['requiredInputCount']} "
        f"guard_checks={expected['guardCheckCount']} "
        f"forbidden_actions={expected['forbiddenActionCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "not_final_acceptance=covered "
        "idempotency=covered "
        "rollback=covered "
        "duplicate_guard=covered "
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
