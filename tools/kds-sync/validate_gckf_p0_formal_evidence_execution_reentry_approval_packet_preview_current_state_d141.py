#!/usr/bin/env python3
"""Validate D141 GCKF P0 formal evidence execution re-entry approval packet preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-reentry-approval-packet-preview-current-state-d141-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-reentry-approval-packet-preview-current-state-d141-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-reentry-approval-packet-preview-current-state-d141-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D141-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_current_state_d141=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d141_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_approval = load_json(ROOT / fixture["sourceHistoricalApprovalPacketPreview"])
    current_preflight = load_json(ROOT / fixture["sourceCurrentReentryPreflightPreview"])
    approval = fixture["approvalPacketPreview"]
    source_approval = historical_approval["approvalPacketPreview"]
    preflight = current_preflight["reentryPreflightPreview"]

    require(fixture.get("approvalPacketPreviewStatus") == expected["approvalPacketPreviewStatus"], "approval_packet_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(approval.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(approval.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(approval.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(approval.get("approvalExecutionStatus") == expected["approvalExecutionStatus"], "approval_execution_status_mismatch")
    require(approval.get("retryExecutionStatus") == expected["retryExecutionStatus"], "retry_execution_status_mismatch")
    require(approval.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(approval.get("executionMode") == expected["executionMode"], "approval_execution_mode_mismatch")
    require(approval.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(approval.get("sourceReentryPreflightPreviewId") == preflight.get("id"), "source_reentry_preflight_preview_id_mismatch")

    require(historical_approval.get("approvalPacketPreviewStatus") == "candidate_preview", "historical_approval_packet_preview_status_mismatch")
    require(source_approval.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_approval.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_preflight.get("reentryPreflightPreviewStatus") == expected["sourceReentryPreflightPreviewStatus"], "source_reentry_preflight_preview_status_mismatch")
    require(preflight.get("reentryExecutionStatus") == expected["sourceReentryExecutionStatus"], "source_reentry_execution_status_mismatch")
    require(preflight.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(preflight.get("retryExecutionStatus") == expected["sourceRetryExecutionStatus"], "source_retry_execution_status_mismatch")
    require(fixture.get("coveredReentryPreflightPreviewStatus") == expected["coveredReentryPreflightPreviewStatus"], "covered_reentry_preflight_preview_status_mismatch")
    require(fixture["coveredReentryPreflightPreviewStatus"] == preflight.get("previewStatus"), "covered_reentry_preflight_preview_not_matched")

    roles = set(approval.get("approvalRoles", []))
    require(len(roles) == expected["approvalRoleCount"], "approval_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "repair_reviewer",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
        },
        "approval_role",
    )

    sections = set(approval.get("approvalPacketSections", []))
    require(len(sections) == expected["approvalPacketSectionCount"], "approval_packet_section_count_mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "incident_summary",
            "repair_summary",
            "reentry_preflight_summary",
            "freeze_release_candidate",
            "execution_lock_renewal",
            "approval_refresh",
            "verification_plan_refresh",
            "rollback_drill_refresh",
            "waes_reentry_gate",
            "kwe_reentry_work_item",
            "harness_review_input",
            "responsibility_boundary",
            "negative_gate_result",
            "no_write_attestation",
        },
        "approval_packet_section",
    )

    checks = set(approval.get("approvalChecks", []))
    require(len(checks) == expected["approvalCheckCount"], "approval_check_count_mismatch")
    require_all(
        checks,
        {
            "source_reentry_preflight_preview_status_is_candidate_preview_with_hold",
            "source_reentry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_reentry_preflight_is_dry_run_only",
            "approval_packet_preview_status_is_candidate_preview_with_hold",
            "request_owner_signer_present",
            "repair_reviewer_signer_present",
            "waes_gate_owner_signer_present",
            "kwe_workflow_owner_signer_present",
            "harness_reviewer_signer_present",
            "committee_representative_signer_present",
            "stop_authority_owner_signer_present",
            "business_system_owner_signer_present",
            "responsibility_boundary_present",
            "approval_sequence_present",
            "harness_review_input_present",
            "negative_gate_result_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_approval_not_executed",
            "assert_retry_not_executed",
            "assert_unfreeze_not_executed",
            "assert_no_write_boundary",
            "approval_requires_future_harness_execution",
            "p1_admission_not_granted",
            "v1_upgrade_not_approved",
        },
        "approval_check",
    )

    refs = set(approval.get("requiredApprovalRefs", []))
    require(len(refs) == expected["requiredApprovalRefCount"], "required_approval_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceReentryPreflightPreviewRef",
            "sourceIncidentEscalationPreviewRef",
            "repairEvidencePacketRef",
            "freezeReleaseCandidateRef",
            "executionLockRenewalCandidateRef",
            "approvalRefreshCandidateRef",
            "verificationPlanRefreshCandidateRef",
            "rollbackDrillRefreshCandidateRef",
            "waesReentryGateCandidateRef",
            "kweReentryWorkItemCandidateRef",
            "harnessReviewInputRef",
            "responsibilityBoundaryRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
            "requestOwnerSignerRef",
            "repairReviewerSignerRef",
            "waesGateOwnerSignerRef",
            "kweWorkflowOwnerSignerRef",
            "harnessReviewerSignerRef",
            "committeeRepresentativeSignerRef",
            "stopAuthorityOwnerSignerRef",
            "businessSystemOwnerSignerRef",
            "holdContextRefs",
        },
        "required_approval_ref",
    )

    blocking_conditions = set(approval.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_reentry_preflight_not_candidate_preview_with_hold",
            "source_reentry_already_executed",
            "source_unfreeze_already_executed",
            "source_retry_already_executed",
            "source_reentry_preflight_not_dry_run_only",
            "missing_source_reentry_preflight_ref",
            "missing_repair_evidence_packet_ref",
            "missing_freeze_release_candidate_ref",
            "missing_execution_lock_renewal_candidate_ref",
            "missing_approval_refresh_candidate_ref",
            "missing_verification_plan_refresh_candidate_ref",
            "missing_rollback_drill_refresh_candidate_ref",
            "missing_waes_reentry_gate_candidate_ref",
            "missing_kwe_reentry_work_item_candidate_ref",
            "missing_harness_review_input_ref",
            "missing_responsibility_boundary_ref",
            "missing_negative_gate_result_ref",
            "missing_no_write_attestation_ref",
            "missing_required_signer",
            "missing_hold_context_refs",
            "approval_preview_attempts_approval",
            "approval_preview_attempts_retry",
            "approval_preview_attempts_unfreeze",
            "approval_preview_attempts_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(approval.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_approval",
            "execute_formal_write",
            "execute_retry",
            "execute_unfreeze",
            "release_freeze",
            "release_execution_lock",
            "write_approval_result",
            "write_reentry_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_verification_result",
            "write_rollback_result",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "mark_production_ready",
            "convert_approval_preview_to_result",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

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

    require(evidence.get("current_approval_packet_preview_status") == "candidate_preview_with_hold", "evidence_approval_packet_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("approval_scope", {}).get("approval_roles") == 8, "evidence_approval_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_reentry_preflight_preview_status") == "candidate_preview_with_hold", "evidence_source_reentry_preflight_preview_status_mismatch")

    d42_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_dry_run.py")
    require(d42_output.startswith("gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_dry_run=pass"), "d42_validator_not_pass")

    d140_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_reentry_preflight_preview_current_state_d140.py")
    require(d140_output.startswith("gckf_p0_formal_evidence_execution_reentry_preflight_preview_current_state_d140=pass"), "d140_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_reentry_approval_packet_preview_current_state_d141=pass")
    print(f"approval_packet_preview_status={fixture.get('approvalPacketPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={approval.get('previewStatus')}")
    print(f"execution_status={approval.get('executionStatus')}")
    print(f"approval_execution_status={approval.get('approvalExecutionStatus')}")
    print(f"retry_execution_status={approval.get('retryExecutionStatus')}")
    print(f"unfreeze_execution_status={approval.get('unfreezeExecutionStatus')}")
    print(f"approval_roles={len(roles)}")
    print(f"approval_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
