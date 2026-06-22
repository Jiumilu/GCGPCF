#!/usr/bin/env python3
"""Validate D133 GCKF P0 formal evidence execution step current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-step-current-state-d133-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-step-current-state-d133-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-step-current-state-d133-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D133-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_step_current_state_d133=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d133_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_step = load_json(ROOT / fixture["sourceHistoricalExecutionStep"])
    current_approval = load_json(ROOT / fixture["sourceCurrentExecutionApproval"])
    step = fixture["executionStep"]
    source_step = historical_step["executionStep"]
    approval = current_approval["approvalCandidate"]

    require(fixture.get("executionStepStatus") == expected["executionStepStatus"], "execution_step_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(step.get("stepType") == expected["stepType"], "step_type_mismatch")
    require(step.get("stepStatus") == expected["stepStatus"], "step_status_mismatch")
    require(step.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(step.get("executionMode") == expected["executionMode"], "step_execution_mode_mismatch")
    require(step.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(step.get("sourceExecutionApprovalId") == approval.get("id"), "source_execution_approval_id_mismatch")

    require(historical_step.get("executionStepStatus") == "candidate_step", "historical_execution_step_status_mismatch")
    require(source_step.get("stepStatus") == "candidate_step", "historical_step_status_mismatch")
    require(source_step.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_approval.get("executionApprovalStatus") == expected["sourceExecutionApprovalStatus"], "source_execution_approval_status_mismatch")
    require(approval.get("executionStatus") == expected["sourceExecutionApprovalExecutionStatus"], "source_execution_approval_execution_status_mismatch")
    require(fixture.get("coveredApprovalOutcome") == expected["coveredApprovalOutcome"], "covered_approval_outcome_mismatch")
    require(fixture["coveredApprovalOutcome"] == approval.get("approvalOutcome"), "covered_approval_not_matched")

    required_inputs = set(step.get("requiredInputs", []))
    require(len(required_inputs) == expected["requiredInputCount"], "required_input_count_mismatch")
    for field in {
        "executionApprovalRef",
        "executionRequestRef",
        "executorId",
        "scheduledAt",
        "authorityRef",
        "approvalOutcome",
        "evidenceRefs",
        "holdContextRefs",
        "idempotencyKey",
        "duplicateCheckRef",
        "rollbackPlanRef",
        "executionLockRef",
        "auditTrailRef",
        "preWriteSnapshotRef",
        "postWriteVerificationPlanRef",
        "harnessEvidenceTargetRef",
    }:
        require(field in required_inputs, f"missing_required_input:{field}")

    checks = set(step.get("stepChecks", []))
    require(len(checks) == expected["stepCheckCount"], "step_check_count_mismatch")
    for check in {
        "source_execution_approval_status_is_candidate_approval_with_hold",
        "source_execution_approval_execution_status_is_not_executed",
        "source_execution_approval_is_dry_run_only",
        "approval_outcome_is_approved_for_future_execution_step",
        "execution_mode_is_dry_run_no_write",
        "authority_ref_present",
        "evidence_refs_present",
        "hold_context_refs_present",
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
        "p1_admission_not_granted",
        "v1_upgrade_not_approved",
    }:
        require(check in checks, f"missing_step_check:{check}")

    forbidden_actions = set(step.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
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
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_approval.get("holdContextRefs", []))
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

    require(evidence.get("current_execution_step_status") == "candidate_step_with_hold", "evidence_execution_step_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("step_scope", {}).get("required_inputs") == 16, "evidence_required_input_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_execution_approval_status") == "candidate_approval_with_hold", "evidence_source_execution_approval_status_mismatch")

    d34_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_step_dry_run.py")
    require(d34_output.startswith("gckf_p0_formal_evidence_execution_step_dry_run=pass"), "d34_validator_not_pass")

    d132_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_approval_current_state_d132.py")
    require(d132_output.startswith("gckf_p0_formal_evidence_execution_approval_current_state_d132=pass"), "d132_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_step_current_state_d133=pass")
    print(f"execution_step_status={fixture.get('executionStepStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"step_status={step.get('stepStatus')}")
    print(f"execution_status={step.get('executionStatus')}")
    print(f"required_inputs={len(required_inputs)}")
    print(f"step_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
