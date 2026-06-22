#!/usr/bin/env python3
"""Validate D131 GCKF P0 formal evidence execution request current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-request-current-state-d131-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-request-current-state-d131-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-request-current-state-d131-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D131-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_request_current_state_d131=fail reason={message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run_command(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        fail(f"command_failed:{' '.join(args)}:{stderr}")
    return result.stdout.strip()


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d131_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_request = load_json(ROOT / fixture["sourceHistoricalExecutionRequest"])
    current_preflight = load_json(ROOT / fixture["sourceCurrentExecutionPreflight"])
    request = fixture["executionRequest"]
    source_request = historical_request["executionRequest"]
    preflight = current_preflight["executionPreflight"]

    require(fixture.get("executionRequestStatus") == expected["executionRequestStatus"], "execution_request_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(request.get("requestType") == expected["requestType"], "request_type_mismatch")
    require(request.get("requestStatus") == expected["requestStatus"], "request_status_mismatch")
    require(request.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(request.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(request.get("sourcePreflightId") == preflight.get("id"), "source_preflight_id_mismatch")

    require(historical_request.get("executionRequestStatus") == "candidate", "historical_execution_request_status_mismatch")
    require(source_request.get("requestStatus") == "candidate", "historical_request_status_mismatch")
    require(source_request.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_preflight.get("executionPreflightStatus") == expected["sourcePreflightStatus"], "source_preflight_status_mismatch")
    require(preflight.get("executionStatus") == expected["sourcePreflightExecutionStatus"], "source_preflight_execution_status_mismatch")
    require(fixture.get("coveredDecisionOutcome") == expected["coveredDecisionOutcome"], "covered_decision_outcome_mismatch")
    require(fixture["coveredDecisionOutcome"] == current_preflight.get("coveredDecisionOutcome"), "covered_decision_not_matched")

    required_inputs = set(request.get("requiredInputs", []))
    require(len(required_inputs) == expected["requiredInputCount"], "required_input_count_mismatch")
    for field in {
        "preflightRef",
        "approvalDecisionRef",
        "executionRequestId",
        "requesterId",
        "requestedAt",
        "authorityRef",
        "evidenceRefs",
        "holdContextRefs",
        "idempotencyKey",
        "duplicateCheckRef",
        "rollbackPlanRef",
        "executionLockRef",
        "auditTrailRef",
        "harnessReviewRouteRef",
    }:
        require(field in required_inputs, f"missing_required_input:{field}")

    checks = set(request.get("requestChecks", []))
    require(len(checks) == expected["requestCheckCount"], "request_check_count_mismatch")
    for check in {
        "source_preflight_status_is_candidate_with_hold",
        "source_preflight_execution_status_is_candidate_with_hold",
        "decision_outcome_is_approve_for_future_formal_write",
        "source_preflight_checks_satisfied",
        "approval_decision_ref_present",
        "authority_ref_present",
        "hold_context_refs_present",
        "idempotency_key_present",
        "duplicate_formal_evidence_absent",
        "rollback_plan_present",
        "execution_lock_present",
        "audit_trail_ref_present",
        "harness_review_route_present",
        "request_requires_separate_execution_approval",
        "request_does_not_execute_formal_write",
        "p1_admission_not_granted",
        "v1_upgrade_not_approved",
    }:
        require(check in checks, f"missing_request_check:{check}")

    forbidden_actions = set(request.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "bypass_harness_review",
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_preflight.get("holdContextRefs", []))
    for hold_ref in hold_refs:
        require(hold_ref in source_hold_refs, f"missing_hold_context_ref:{hold_ref}")

    for key in [
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ]:
        require(fixture["currentGateAssertions"].get(key) is False, f"current_gate_assertion_not_false:{key}")

    require(len(fixture.get("requiredSourceRefs", [])) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")

    require(evidence.get("current_execution_request_status") == "candidate_with_hold", "evidence_execution_request_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("request_scope", {}).get("required_inputs") == 14, "evidence_required_input_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_preflight_status") == "candidate_with_hold", "evidence_source_preflight_status_mismatch")

    d32_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_request_dry_run.py")
    require(d32_output.startswith("gckf_p0_formal_evidence_execution_request_dry_run=pass"), "d32_validator_not_pass")

    d130_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_future_formal_write_execution_preflight_current_state_d130.py")
    require(d130_output.startswith("gckf_p0_future_formal_write_execution_preflight_current_state_d130=pass"), "d130_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_request_current_state_d131=pass")
    print(f"execution_request_status={fixture.get('executionRequestStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"request_status={request.get('requestStatus')}")
    print(f"execution_status={request.get('executionStatus')}")
    print(f"required_inputs={len(required_inputs)}")
    print(f"request_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
