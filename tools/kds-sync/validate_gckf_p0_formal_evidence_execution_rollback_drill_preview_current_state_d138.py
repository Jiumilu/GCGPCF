#!/usr/bin/env python3
"""Validate D138 GCKF P0 formal evidence execution rollback drill preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-rollback-drill-preview-current-state-d138-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-rollback-drill-preview-current-state-d138-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-rollback-drill-preview-current-state-d138-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D138-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_rollback_drill_preview_current_state_d138=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d138_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_drill = load_json(ROOT / fixture["sourceHistoricalRollbackDrillPreview"])
    current_plan = load_json(ROOT / fixture["sourceCurrentVerificationPlanPreview"])
    drill = fixture["rollbackDrillPreview"]
    source_drill = historical_drill["rollbackDrillPreview"]
    plan = current_plan["verificationPlanPreview"]

    require(fixture.get("rollbackDrillPreviewStatus") == expected["rollbackDrillPreviewStatus"], "rollback_drill_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(drill.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(drill.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(drill.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(drill.get("rollbackExecutionStatus") == expected["rollbackExecutionStatus"], "rollback_execution_status_mismatch")
    require(drill.get("executionMode") == expected["executionMode"], "drill_execution_mode_mismatch")
    require(drill.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(drill.get("sourceVerificationPlanPreviewId") == plan.get("id"), "source_verification_plan_preview_id_mismatch")

    require(historical_drill.get("rollbackDrillPreviewStatus") == "candidate_preview", "historical_rollback_drill_preview_status_mismatch")
    require(source_drill.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_drill.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_plan.get("verificationPlanPreviewStatus") == expected["sourceVerificationPlanPreviewStatus"], "source_verification_plan_preview_status_mismatch")
    require(plan.get("executionStatus") == expected["sourceVerificationPlanExecutionStatus"], "source_verification_plan_execution_status_mismatch")
    require(fixture.get("coveredVerificationPlanPreviewStatus") == expected["coveredVerificationPlanPreviewStatus"], "covered_verification_plan_preview_status_mismatch")
    require(fixture["coveredVerificationPlanPreviewStatus"] == plan.get("previewStatus"), "covered_verification_plan_preview_not_matched")

    triggers = set(drill.get("rollbackTriggers", []))
    require(len(triggers) == expected["rollbackTriggerCount"], "rollback_trigger_count_mismatch")
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
        require(trigger in triggers, f"missing_rollback_trigger:{trigger}")

    steps = set(drill.get("rollbackDrillSteps", []))
    require(len(steps) == expected["rollbackDrillStepCount"], "rollback_drill_step_count_mismatch")
    for step in {
        "confirm_source_verification_plan_preview_is_candidate_preview_with_hold",
        "confirm_source_verification_plan_execution_status_is_not_executed",
        "confirm_source_verification_plan_is_dry_run_only",
        "acquire_rollback_drill_lock_preview",
        "verify_pre_write_snapshot_ref_available",
        "verify_execution_lock_ref_available",
        "verify_rollback_plan_ref_available",
        "verify_hold_context_refs_available",
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
        "assert_p1_admission_not_granted",
        "assert_v1_upgrade_not_approved",
        "assert_no_write_boundary",
    }:
        require(step in steps, f"missing_rollback_drill_step:{step}")

    refs = set(drill.get("requiredRollbackRefs", []))
    require(len(refs) == expected["requiredRollbackRefCount"], "required_rollback_ref_count_mismatch")
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
        "holdContextRefs",
    }:
        require(ref in refs, f"missing_required_rollback_ref:{ref}")

    blocking_conditions = set(drill.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    for blocking in {
        "source_verification_plan_not_candidate_preview_with_hold",
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
        "missing_hold_context_refs",
        "rollback_drill_already_executed",
        "rollback_drill_attempts_write",
    }:
        require(blocking in blocking_conditions, f"missing_blocking_condition:{blocking}")

    forbidden_actions = set(drill.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
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
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_plan.get("holdContextRefs", []))
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

    require(evidence.get("current_rollback_drill_preview_status") == "candidate_preview_with_hold", "evidence_rollback_drill_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("rollback_scope", {}).get("rollback_triggers") == 8, "evidence_rollback_trigger_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_verification_plan_preview_status") == "candidate_preview_with_hold", "evidence_source_verification_plan_preview_status_mismatch")

    d39_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_rollback_drill_preview_dry_run.py")
    require(d39_output.startswith("gckf_p0_formal_evidence_execution_rollback_drill_preview_dry_run=pass"), "d39_validator_not_pass")

    d137_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_verification_plan_preview_current_state_d137.py")
    require(d137_output.startswith("gckf_p0_formal_evidence_execution_verification_plan_preview_current_state_d137=pass"), "d137_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_rollback_drill_preview_current_state_d138=pass")
    print(f"rollback_drill_preview_status={fixture.get('rollbackDrillPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={drill.get('previewStatus')}")
    print(f"execution_status={drill.get('executionStatus')}")
    print(f"rollback_execution_status={drill.get('rollbackExecutionStatus')}")
    print(f"rollback_triggers={len(triggers)}")
    print(f"rollback_drill_steps={len(steps)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
