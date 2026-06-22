#!/usr/bin/env python3
"""Validate D135 GCKF P0 formal evidence final execution request current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-final-execution-request-current-state-d135-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-final-execution-request-current-state-d135-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-final-execution-request-current-state-d135-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D135-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_final_execution_request_current_state_d135=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d135_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_request = load_json(ROOT / fixture["sourceHistoricalFinalExecutionRequest"])
    current_guard = load_json(ROOT / fixture["sourceCurrentFinalExecutionGuard"])
    request = fixture["finalExecutionRequest"]
    source_request = historical_request["finalExecutionRequest"]
    guard = current_guard["finalExecutionGuard"]

    require(fixture.get("finalExecutionRequestStatus") == expected["finalExecutionRequestStatus"], "final_execution_request_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(request.get("requestType") == expected["requestType"], "request_type_mismatch")
    require(request.get("requestStatus") == expected["requestStatus"], "request_status_mismatch")
    require(request.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(request.get("executionMode") == expected["executionMode"], "request_execution_mode_mismatch")
    require(request.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(request.get("sourceFinalExecutionGuardId") == guard.get("id"), "source_final_execution_guard_id_mismatch")

    require(historical_request.get("finalExecutionRequestStatus") == "candidate_request", "historical_final_execution_request_status_mismatch")
    require(source_request.get("requestStatus") == "candidate_request", "historical_request_status_mismatch")
    require(source_request.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_guard.get("finalExecutionGuardStatus") == expected["sourceFinalExecutionGuardStatus"], "source_final_execution_guard_status_mismatch")
    require(guard.get("executionStatus") == expected["sourceFinalExecutionGuardExecutionStatus"], "source_final_execution_guard_execution_status_mismatch")
    require(fixture.get("coveredGuardStatus") == expected["coveredGuardStatus"], "covered_guard_status_mismatch")
    require(fixture["coveredGuardStatus"] == guard.get("guardStatus"), "covered_guard_not_matched")

    required_inputs = set(request.get("requiredInputs", []))
    require(len(required_inputs) == expected["requiredInputCount"], "required_input_count_mismatch")
    for field in {
        "finalExecutionGuardRef",
        "executionStepRef",
        "executionApprovalRef",
        "executorId",
        "requesterId",
        "humanAuthorizationRef",
        "committeeAuthorizationRef",
        "freezeGateResultRef",
        "holdContextRefs",
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
        require(field in required_inputs, f"missing_required_input:{field}")

    checks = set(request.get("requestChecks", []))
    require(len(checks) == expected["requestCheckCount"], "request_check_count_mismatch")
    for check in {
        "source_final_execution_guard_status_is_candidate_guard_with_hold",
        "source_final_execution_guard_execution_status_is_not_executed",
        "source_final_execution_guard_is_dry_run_only",
        "execution_mode_is_dry_run_no_write",
        "request_status_is_candidate_request_with_hold",
        "human_authorization_ref_present",
        "committee_authorization_ref_present",
        "freeze_gate_result_ref_present",
        "hold_context_refs_present",
        "duplicate_check_ref_present",
        "idempotency_key_present",
        "execution_lock_ref_present",
        "pre_write_snapshot_ref_present",
        "post_write_verification_plan_ref_present",
        "rollback_plan_ref_present",
        "audit_trail_ref_present",
        "harness_evidence_target_ref_present",
        "formal_evidence_target_ref_present",
        "no_write_boundary_ref_present",
        "request_does_not_execute_formal_evidence",
        "formal_write_requires_separate_harness_execution",
        "p1_admission_not_granted",
        "v1_upgrade_not_approved",
    }:
        require(check in checks, f"missing_request_check:{check}")

    blocking_conditions = set(request.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    for blocking in {
        "source_guard_not_candidate_guard_with_hold",
        "source_guard_already_executed",
        "source_guard_not_dry_run_only",
        "missing_requester",
        "missing_human_authorization",
        "missing_committee_authorization",
        "freeze_gate_blocked",
        "missing_hold_context_refs",
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
        require(blocking in blocking_conditions, f"missing_blocking_condition:{blocking}")

    forbidden_actions = set(request.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "convert_candidate_guard_to_passed",
        "bypass_freeze_gate",
        "bypass_human_authorization",
        "bypass_committee_authorization",
        "release_execution_lock",
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_guard.get("holdContextRefs", []))
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

    require(evidence.get("current_final_execution_request_status") == "candidate_request_with_hold", "evidence_final_execution_request_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("request_scope", {}).get("required_inputs") == 19, "evidence_required_input_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_final_execution_guard_status") == "candidate_guard_with_hold", "evidence_source_final_execution_guard_status_mismatch")

    d36_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_final_execution_request_dry_run.py")
    require(d36_output.startswith("gckf_p0_formal_evidence_final_execution_request_dry_run=pass"), "d36_validator_not_pass")

    d134_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_final_execution_guard_current_state_d134.py")
    require(d134_output.startswith("gckf_p0_formal_evidence_final_execution_guard_current_state_d134=pass"), "d134_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_final_execution_request_current_state_d135=pass")
    print(f"final_execution_request_status={fixture.get('finalExecutionRequestStatus')}")
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
