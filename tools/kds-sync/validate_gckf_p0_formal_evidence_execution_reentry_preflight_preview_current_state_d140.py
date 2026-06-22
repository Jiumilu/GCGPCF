#!/usr/bin/env python3
"""Validate D140 GCKF P0 formal evidence execution re-entry preflight preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-reentry-preflight-preview-current-state-d140-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-reentry-preflight-preview-current-state-d140-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-reentry-preflight-preview-current-state-d140-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D140-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_reentry_preflight_preview_current_state_d140=fail reason={message}")
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


def require_all(actual: set[str], expected_values: set[str], label: str) -> None:
    for value in expected_values:
        require(value in actual, f"missing_{label}:{value}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d140_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_reentry = load_json(ROOT / fixture["sourceHistoricalReentryPreflightPreview"])
    current_escalation = load_json(ROOT / fixture["sourceCurrentIncidentEscalationPreview"])
    reentry = fixture["reentryPreflightPreview"]
    source_reentry = historical_reentry["reentryPreflightPreview"]
    escalation = current_escalation["incidentEscalationPreview"]

    require(fixture.get("reentryPreflightPreviewStatus") == expected["reentryPreflightPreviewStatus"], "reentry_preflight_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(reentry.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(reentry.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(reentry.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(reentry.get("reentryExecutionStatus") == expected["reentryExecutionStatus"], "reentry_execution_status_mismatch")
    require(reentry.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(reentry.get("retryExecutionStatus") == expected["retryExecutionStatus"], "retry_execution_status_mismatch")
    require(reentry.get("executionMode") == expected["executionMode"], "reentry_execution_mode_mismatch")
    require(reentry.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(reentry.get("sourceIncidentEscalationPreviewId") == escalation.get("id"), "source_incident_escalation_preview_id_mismatch")

    require(historical_reentry.get("reentryPreflightPreviewStatus") == "candidate_preview", "historical_reentry_preflight_preview_status_mismatch")
    require(source_reentry.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_reentry.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_escalation.get("incidentEscalationPreviewStatus") == expected["sourceIncidentEscalationPreviewStatus"], "source_incident_escalation_preview_status_mismatch")
    require(escalation.get("incidentExecutionStatus") == expected["sourceIncidentExecutionStatus"], "source_incident_execution_status_mismatch")
    require(escalation.get("freezeExecutionStatus") == expected["sourceFreezeExecutionStatus"], "source_freeze_execution_status_mismatch")
    require(fixture.get("coveredIncidentEscalationPreviewStatus") == expected["coveredIncidentEscalationPreviewStatus"], "covered_incident_escalation_preview_status_mismatch")
    require(fixture["coveredIncidentEscalationPreviewStatus"] == escalation.get("previewStatus"), "covered_incident_escalation_preview_not_matched")

    states = set(reentry.get("reentryAdmissionStates", []))
    require(len(states) == expected["reentryAdmissionStateCount"], "reentry_admission_state_count_mismatch")
    require_all(
        states,
        {
            "repair_required",
            "repair_submitted",
            "repair_human_review_required",
            "repair_committee_review_required",
            "ready_for_reentry_candidate",
            "reentry_blocked",
        },
        "reentry_admission_state",
    )

    checks = set(reentry.get("reentryPreflightChecks", []))
    require(len(checks) == expected["reentryPreflightCheckCount"], "reentry_preflight_check_count_mismatch")
    require_all(
        checks,
        {
            "source_incident_escalation_preview_status_is_candidate_preview_with_hold",
            "source_incident_execution_status_is_not_executed",
            "source_freeze_execution_status_is_not_executed",
            "source_incident_escalation_is_dry_run_only",
            "repair_or_reopen_work_item_present",
            "repair_evidence_packet_present",
            "repair_evidence_shape_valid",
            "human_repair_review_packet_present",
            "committee_repair_review_packet_present",
            "stop_authority_release_packet_present",
            "freeze_release_candidate_packet_present",
            "execution_lock_renewal_candidate_present",
            "approval_refresh_candidate_present",
            "verification_plan_refresh_candidate_present",
            "rollback_drill_refresh_candidate_present",
            "incident_audit_trail_link_present",
            "harness_evidence_candidate_link_present",
            "waes_reentry_gate_candidate_present",
            "kwe_reentry_work_item_candidate_present",
            "notify_original_approvers_candidate_present",
            "preview_hold_context_refs",
            "assert_unfreeze_not_executed",
            "assert_retry_not_executed",
            "assert_no_write_boundary",
            "reentry_requires_future_harness_execution",
            "p1_admission_not_granted",
            "v1_upgrade_not_approved",
        },
        "reentry_preflight_check",
    )

    refs = set(reentry.get("requiredReentryRefs", []))
    require(len(refs) == expected["requiredReentryRefCount"], "required_reentry_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceIncidentEscalationPreviewRef",
            "sourceRollbackDrillPreviewRef",
            "sourceVerificationPlanPreviewRef",
            "repairOrReopenWorkItemRef",
            "repairEvidencePacketRef",
            "humanRepairReviewPacketRef",
            "committeeRepairReviewPacketRef",
            "stopAuthorityReleasePacketRef",
            "freezeReleaseCandidateRef",
            "executionLockRenewalCandidateRef",
            "approvalRefreshCandidateRef",
            "verificationPlanRefreshCandidateRef",
            "rollbackDrillRefreshCandidateRef",
            "incidentAuditTrailRef",
            "harnessEvidenceCandidateRef",
            "waesReentryGateCandidateRef",
            "kweReentryWorkItemCandidateRef",
            "holdContextRefs",
        },
        "required_reentry_ref",
    )

    blocking_conditions = set(reentry.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_incident_escalation_not_candidate_preview_with_hold",
            "source_incident_already_executed",
            "source_freeze_already_executed",
            "source_incident_escalation_not_dry_run_only",
            "missing_source_incident_escalation_ref",
            "missing_repair_or_reopen_work_item_ref",
            "missing_repair_evidence_packet_ref",
            "missing_human_repair_review_packet_ref",
            "missing_committee_repair_review_packet_ref",
            "missing_stop_authority_release_packet_ref",
            "missing_freeze_release_candidate_ref",
            "missing_execution_lock_renewal_candidate_ref",
            "missing_approval_refresh_candidate_ref",
            "missing_verification_plan_refresh_candidate_ref",
            "missing_rollback_drill_refresh_candidate_ref",
            "missing_incident_audit_trail_ref",
            "missing_harness_evidence_candidate_ref",
            "missing_waes_reentry_gate_candidate_ref",
            "missing_kwe_reentry_work_item_candidate_ref",
            "missing_hold_context_refs",
            "reentry_preview_attempts_unfreeze",
            "reentry_preview_attempts_retry",
            "reentry_preview_attempts_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(reentry.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_formal_write",
            "execute_retry",
            "execute_unfreeze",
            "release_freeze",
            "release_execution_lock",
            "write_reentry_result",
            "write_repair_result",
            "write_freeze_release_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_verification_result",
            "write_rollback_result",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "mark_production_ready",
            "convert_reentry_preview_to_result",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_escalation.get("holdContextRefs", []))
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

    require(evidence.get("current_reentry_preflight_preview_status") == "candidate_preview_with_hold", "evidence_reentry_preflight_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("reentry_scope", {}).get("reentry_admission_states") == 6, "evidence_reentry_admission_state_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_incident_escalation_preview_status") == "candidate_preview_with_hold", "evidence_source_incident_escalation_preview_status_mismatch")

    d41_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_reentry_preflight_preview_dry_run.py")
    require(d41_output.startswith("gckf_p0_formal_evidence_execution_reentry_preflight_preview_dry_run=pass"), "d41_validator_not_pass")

    d139_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_incident_escalation_preview_current_state_d139.py")
    require(d139_output.startswith("gckf_p0_formal_evidence_execution_incident_escalation_preview_current_state_d139=pass"), "d139_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_reentry_preflight_preview_current_state_d140=pass")
    print(f"reentry_preflight_preview_status={fixture.get('reentryPreflightPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={reentry.get('previewStatus')}")
    print(f"execution_status={reentry.get('executionStatus')}")
    print(f"reentry_execution_status={reentry.get('reentryExecutionStatus')}")
    print(f"unfreeze_execution_status={reentry.get('unfreezeExecutionStatus')}")
    print(f"retry_execution_status={reentry.get('retryExecutionStatus')}")
    print(f"reentry_admission_states={len(states)}")
    print(f"reentry_preflight_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
