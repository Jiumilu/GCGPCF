#!/usr/bin/env python3
"""Validate D136 GCKF P0 formal evidence execution evidence preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-evidence-preview-current-state-d136-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-evidence-preview-current-state-d136-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-evidence-preview-current-state-d136-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D136-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_evidence_preview_current_state_d136=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d136_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_preview = load_json(ROOT / fixture["sourceHistoricalEvidencePreview"])
    current_request = load_json(ROOT / fixture["sourceCurrentFinalExecutionRequest"])
    preview = fixture["evidencePreview"]
    source_preview = historical_preview["evidencePreview"]
    request = current_request["finalExecutionRequest"]

    require(fixture.get("evidencePreviewStatus") == expected["evidencePreviewStatus"], "evidence_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(preview.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(preview.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(preview.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(preview.get("executionMode") == expected["executionMode"], "preview_execution_mode_mismatch")
    require(preview.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(preview.get("sourceFinalExecutionRequestId") == request.get("id"), "source_final_execution_request_id_mismatch")

    require(historical_preview.get("evidencePreviewStatus") == "candidate_preview", "historical_evidence_preview_status_mismatch")
    require(source_preview.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_preview.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_request.get("finalExecutionRequestStatus") == expected["sourceFinalExecutionRequestStatus"], "source_final_execution_request_status_mismatch")
    require(request.get("executionStatus") == expected["sourceFinalExecutionRequestExecutionStatus"], "source_final_execution_request_execution_status_mismatch")
    require(fixture.get("coveredRequestStatus") == expected["coveredRequestStatus"], "covered_request_status_mismatch")
    require(fixture["coveredRequestStatus"] == request.get("requestStatus"), "covered_request_not_matched")

    fields = set(preview.get("previewFields", []))
    require(len(fields) == expected["previewFieldCount"], "preview_field_count_mismatch")
    for field in {
        "evidenceId",
        "evidenceType",
        "tenantId",
        "projectId",
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
        "postWriteVerificationPlanRef",
        "rollbackPlanRef",
        "auditTrailRef",
        "holdContextRefs",
        "createdBy",
        "createdAt",
        "status",
    }:
        require(field in fields, f"missing_preview_field:{field}")

    checks = set(preview.get("previewChecks", []))
    require(len(checks) == expected["previewCheckCount"], "preview_check_count_mismatch")
    for check in {
        "source_final_execution_request_status_is_candidate_request_with_hold",
        "source_final_execution_request_execution_status_is_not_executed",
        "source_final_execution_request_is_dry_run_only",
        "execution_mode_is_dry_run_no_write",
        "preview_status_is_candidate_preview_with_hold",
        "preview_contains_source_request_ref",
        "preview_contains_source_guard_ref",
        "preview_contains_source_step_ref",
        "preview_contains_authority_refs",
        "preview_contains_human_authorization_ref",
        "preview_contains_committee_authorization_ref",
        "preview_contains_freeze_gate_result_ref",
        "preview_contains_duplicate_check_ref",
        "preview_contains_idempotency_key",
        "preview_contains_execution_lock_ref",
        "preview_contains_pre_write_snapshot_ref",
        "preview_contains_post_write_verification_plan_ref",
        "preview_contains_rollback_plan_ref",
        "preview_contains_audit_trail_ref",
        "preview_contains_hold_context_refs",
        "preview_does_not_write_harness_evidence",
        "preview_does_not_write_formal_evidence",
        "preview_requires_future_harness_execution",
        "p1_admission_not_granted",
        "v1_upgrade_not_approved",
    }:
        require(check in checks, f"missing_preview_check:{check}")

    blocking_conditions = set(preview.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    for blocking in {
        "source_request_not_candidate_request_with_hold",
        "source_request_already_executed",
        "source_request_not_dry_run_only",
        "missing_source_request_ref",
        "missing_authority_refs",
        "missing_human_authorization",
        "missing_committee_authorization",
        "missing_freeze_gate_result",
        "missing_duplicate_check",
        "missing_idempotency_key",
        "missing_execution_lock",
        "missing_pre_write_snapshot",
        "missing_post_write_verification_plan",
        "missing_rollback_plan",
        "missing_audit_trail",
        "missing_hold_context_refs",
    }:
        require(blocking in blocking_conditions, f"missing_blocking_condition:{blocking}")

    forbidden_actions = set(preview.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    for forbidden in {
        "write_formal_evidence",
        "write_harness_evidence",
        "execute_formal_write",
        "write_kds",
        "write_business_system",
        "promote_lifecycle",
        "mark_p0_accepted",
        "mark_production_ready",
        "convert_preview_to_evidence",
        "convert_request_to_approved",
        "release_execution_lock",
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_request.get("holdContextRefs", []))
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

    require(evidence.get("current_evidence_preview_status") == "candidate_preview_with_hold", "evidence_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("preview_scope", {}).get("preview_fields") == 22, "evidence_preview_field_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_final_execution_request_status") == "candidate_request_with_hold", "evidence_source_final_execution_request_status_mismatch")

    d37_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_evidence_preview_dry_run.py")
    require(d37_output.startswith("gckf_p0_formal_evidence_execution_evidence_preview_dry_run=pass"), "d37_validator_not_pass")

    d135_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_final_execution_request_current_state_d135.py")
    require(d135_output.startswith("gckf_p0_formal_evidence_final_execution_request_current_state_d135=pass"), "d135_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_evidence_preview_current_state_d136=pass")
    print(f"evidence_preview_status={fixture.get('evidencePreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={preview.get('previewStatus')}")
    print(f"execution_status={preview.get('executionStatus')}")
    print(f"preview_fields={len(fields)}")
    print(f"preview_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
