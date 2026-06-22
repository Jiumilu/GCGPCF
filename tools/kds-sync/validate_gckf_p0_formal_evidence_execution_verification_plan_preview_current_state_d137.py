#!/usr/bin/env python3
"""Validate D137 GCKF P0 formal evidence execution verification plan preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-verification-plan-preview-current-state-d137-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-verification-plan-preview-current-state-d137-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-verification-plan-preview-current-state-d137-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D137-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_verification_plan_preview_current_state_d137=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d137_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_plan = load_json(ROOT / fixture["sourceHistoricalVerificationPlanPreview"])
    current_preview = load_json(ROOT / fixture["sourceCurrentEvidencePreview"])
    plan = fixture["verificationPlanPreview"]
    source_plan = historical_plan["verificationPlanPreview"]
    preview = current_preview["evidencePreview"]

    require(fixture.get("verificationPlanPreviewStatus") == expected["verificationPlanPreviewStatus"], "verification_plan_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(plan.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(plan.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(plan.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(plan.get("executionMode") == expected["executionMode"], "plan_execution_mode_mismatch")
    require(plan.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(plan.get("sourceEvidencePreviewId") == preview.get("id"), "source_evidence_preview_id_mismatch")

    require(historical_plan.get("verificationPlanPreviewStatus") == "candidate_preview", "historical_verification_plan_preview_status_mismatch")
    require(source_plan.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_plan.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_preview.get("evidencePreviewStatus") == expected["sourceEvidencePreviewStatus"], "source_evidence_preview_status_mismatch")
    require(preview.get("executionStatus") == expected["sourceEvidencePreviewExecutionStatus"], "source_evidence_preview_execution_status_mismatch")
    require(fixture.get("coveredEvidencePreviewStatus") == expected["coveredEvidencePreviewStatus"], "covered_evidence_preview_status_mismatch")
    require(fixture["coveredEvidencePreviewStatus"] == preview.get("previewStatus"), "covered_evidence_preview_not_matched")

    scopes = set(plan.get("verificationScopes", []))
    require(len(scopes) == expected["verificationScopeCount"], "verification_scope_count_mismatch")
    for scope in {
        "source_request_integrity",
        "authority_chain_integrity",
        "execution_lock_integrity",
        "pre_write_snapshot_integrity",
        "post_write_readback_integrity",
        "harness_evidence_shape_integrity",
        "ledger_append_integrity",
        "audit_trail_integrity",
        "rollback_plan_integrity",
        "hold_context_integrity",
        "negative_no_write_boundary",
    }:
        require(scope in scopes, f"missing_verification_scope:{scope}")

    checks = set(plan.get("verificationChecks", []))
    require(len(checks) == expected["verificationCheckCount"], "verification_check_count_mismatch")
    for check in {
        "source_evidence_preview_status_is_candidate_preview_with_hold",
        "source_evidence_preview_execution_status_is_not_executed",
        "source_evidence_preview_is_dry_run_only",
        "verification_plan_status_is_candidate_preview_with_hold",
        "execution_mode_is_dry_run_no_write",
        "verify_source_request_ref_matches_current_request",
        "verify_source_guard_ref_available_before_write",
        "verify_authority_refs_available_before_write",
        "verify_human_authorization_ref_available_before_write",
        "verify_committee_authorization_ref_available_before_write",
        "verify_freeze_gate_result_ref_available_before_write",
        "verify_duplicate_check_ref_available_before_write",
        "verify_idempotency_key_available_before_write",
        "verify_execution_lock_ref_available_before_write",
        "verify_pre_write_snapshot_ref_available_before_write",
        "verify_post_write_readback_plan_exists",
        "verify_harness_evidence_shape_plan_exists",
        "verify_ledger_append_plan_exists",
        "verify_audit_trail_plan_exists",
        "verify_rollback_plan_ref_available_before_write",
        "verify_hold_context_refs_available_before_write",
        "verify_negative_no_kds_write_boundary",
        "verify_negative_no_business_write_boundary",
        "verify_negative_no_accepted_lifecycle_boundary",
        "verification_requires_future_harness_execution",
        "p1_admission_not_granted",
        "v1_upgrade_not_approved",
    }:
        require(check in checks, f"missing_verification_check:{check}")

    required_plan_refs = set(plan.get("requiredPlanRefs", []))
    require(len(required_plan_refs) == expected["requiredPlanRefCount"], "required_plan_ref_count_mismatch")
    for ref in {
        "sourceRequestRef",
        "sourceGuardRef",
        "sourceStepRef",
        "authorityRefs",
        "humanAuthorizationRef",
        "committeeAuthorizationRef",
        "freezeGateResultRef",
        "duplicateCheckRef",
        "idempotencyKey",
        "executionLockRef",
        "preWriteSnapshotRef",
        "postWriteReadbackPlanRef",
        "harnessEvidenceShapePlanRef",
        "ledgerAppendPlanRef",
        "auditTrailRef",
        "rollbackPlanRef",
        "holdContextRefs",
    }:
        require(ref in required_plan_refs, f"missing_required_plan_ref:{ref}")

    blocking_conditions = set(plan.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    for blocking in {
        "source_evidence_preview_not_candidate_preview_with_hold",
        "source_evidence_preview_already_executed",
        "source_evidence_preview_not_dry_run_only",
        "missing_source_request_ref",
        "missing_source_guard_ref",
        "missing_authority_refs",
        "missing_human_authorization_ref",
        "missing_committee_authorization_ref",
        "missing_freeze_gate_result_ref",
        "missing_duplicate_check_ref",
        "missing_idempotency_key",
        "missing_execution_lock_ref",
        "missing_pre_write_snapshot_ref",
        "missing_post_write_readback_plan",
        "missing_harness_evidence_shape_plan",
        "missing_ledger_append_plan",
        "missing_audit_trail_ref",
        "missing_rollback_plan_ref",
        "missing_hold_context_refs",
    }:
        require(blocking in blocking_conditions, f"missing_blocking_condition:{blocking}")

    forbidden_actions = set(plan.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    for forbidden in {
        "execute_formal_write",
        "write_formal_evidence",
        "write_harness_evidence",
        "write_verification_result",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "convert_plan_preview_to_result",
        "release_execution_lock",
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_preview.get("holdContextRefs", []))
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

    require(evidence.get("current_verification_plan_preview_status") == "candidate_preview_with_hold", "evidence_verification_plan_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("plan_scope", {}).get("verification_scopes") == 11, "evidence_verification_scope_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_evidence_preview_status") == "candidate_preview_with_hold", "evidence_source_evidence_preview_status_mismatch")

    d38_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_verification_plan_preview_dry_run.py")
    require(d38_output.startswith("gckf_p0_formal_evidence_execution_verification_plan_preview_dry_run=pass"), "d38_validator_not_pass")

    d136_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_evidence_preview_current_state_d136.py")
    require(d136_output.startswith("gckf_p0_formal_evidence_execution_evidence_preview_current_state_d136=pass"), "d136_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_verification_plan_preview_current_state_d137=pass")
    print(f"verification_plan_preview_status={fixture.get('verificationPlanPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={plan.get('previewStatus')}")
    print(f"execution_status={plan.get('executionStatus')}")
    print(f"verification_scopes={len(scopes)}")
    print(f"verification_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
