#!/usr/bin/env python3
"""Validate D139 GCKF P0 formal evidence execution incident escalation preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-incident-escalation-preview-current-state-d139-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-incident-escalation-preview-current-state-d139-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-incident-escalation-preview-current-state-d139-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D139-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_incident_escalation_preview_current_state_d139=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d139_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_escalation = load_json(ROOT / fixture["sourceHistoricalIncidentEscalationPreview"])
    current_drill = load_json(ROOT / fixture["sourceCurrentRollbackDrillPreview"])
    escalation = fixture["incidentEscalationPreview"]
    source_escalation = historical_escalation["incidentEscalationPreview"]
    drill = current_drill["rollbackDrillPreview"]

    require(fixture.get("incidentEscalationPreviewStatus") == expected["incidentEscalationPreviewStatus"], "incident_escalation_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(escalation.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(escalation.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(escalation.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(escalation.get("incidentExecutionStatus") == expected["incidentExecutionStatus"], "incident_execution_status_mismatch")
    require(escalation.get("freezeExecutionStatus") == expected["freezeExecutionStatus"], "freeze_execution_status_mismatch")
    require(escalation.get("executionMode") == expected["executionMode"], "escalation_execution_mode_mismatch")
    require(escalation.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(escalation.get("sourceRollbackDrillPreviewId") == drill.get("id"), "source_rollback_drill_preview_id_mismatch")

    require(historical_escalation.get("incidentEscalationPreviewStatus") == "candidate_preview", "historical_incident_escalation_preview_status_mismatch")
    require(source_escalation.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_escalation.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_drill.get("rollbackDrillPreviewStatus") == expected["sourceRollbackDrillPreviewStatus"], "source_rollback_drill_preview_status_mismatch")
    require(drill.get("executionStatus") == expected["sourceRollbackDrillExecutionStatus"], "source_rollback_drill_execution_status_mismatch")
    require(drill.get("rollbackExecutionStatus") == expected["sourceRollbackExecutionStatus"], "source_rollback_execution_status_mismatch")
    require(fixture.get("coveredRollbackDrillPreviewStatus") == expected["coveredRollbackDrillPreviewStatus"], "covered_rollback_drill_preview_status_mismatch")
    require(fixture["coveredRollbackDrillPreviewStatus"] == drill.get("previewStatus"), "covered_rollback_drill_preview_not_matched")

    incident_classes = set(escalation.get("incidentClasses", []))
    require(len(incident_classes) == expected["incidentClassCount"], "incident_class_count_mismatch")
    require_all(
        incident_classes,
        {
            "formal_write_failure",
            "verification_failure",
            "rollback_failure",
            "unexpected_kds_write",
            "unexpected_business_write",
            "unexpected_lifecycle_promotion",
            "evidence_shape_violation",
            "audit_trail_violation",
        },
        "incident_class",
    )

    severity_levels = set(escalation.get("severityLevels", []))
    require(len(severity_levels) == expected["severityLevelCount"], "severity_level_count_mismatch")
    require_all(
        severity_levels,
        {"S0_info", "S1_minor", "S2_major", "S3_critical", "S4_stop_authority_required"},
        "severity_level",
    )

    freeze_scopes = set(escalation.get("freezeScopes", []))
    require(len(freeze_scopes) == expected["freezeScopeCount"], "freeze_scope_count_mismatch")
    require_all(
        freeze_scopes,
        {
            "source_request",
            "candidate_evidence",
            "execution_lock",
            "kds_object",
            "writeback_candidate",
            "rag_admission",
            "contribution_revenue_effects",
            "external_share",
        },
        "freeze_scope",
    )

    checks = set(escalation.get("escalationChecks", []))
    require(len(checks) == expected["escalationCheckCount"], "escalation_check_count_mismatch")
    require_all(
        checks,
        {
            "source_rollback_drill_preview_status_is_candidate_preview_with_hold",
            "source_rollback_drill_execution_status_is_not_executed",
            "source_rollback_execution_status_is_not_executed",
            "source_rollback_drill_is_dry_run_only",
            "incident_preview_status_is_candidate_preview_with_hold",
            "execution_mode_is_dry_run_no_write",
            "classify_incident_from_execution_or_verification_or_rollback_failure",
            "map_incident_class_to_severity",
            "map_severity_to_freeze_scope",
            "map_severity_to_human_review_required",
            "map_severity_to_committee_review_required",
            "map_severity_to_stop_authority_required",
            "preview_freeze_request_packet",
            "preview_human_review_packet",
            "preview_committee_review_packet",
            "preview_stop_authority_packet",
            "preview_notification_targets",
            "preview_audit_trail_entry",
            "preview_harness_evidence_candidate_link",
            "preview_repair_or_reopen_work_item",
            "preview_hold_context_refs",
            "assert_incident_not_written",
            "assert_freeze_not_executed",
            "assert_no_write_boundary",
            "incident_escalation_requires_future_harness_execution",
            "p1_admission_not_granted",
            "v1_upgrade_not_approved",
        },
        "escalation_check",
    )

    refs = set(escalation.get("requiredEscalationRefs", []))
    require(len(refs) == expected["requiredEscalationRefCount"], "required_escalation_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceRollbackDrillPreviewRef",
            "sourceVerificationPlanPreviewRef",
            "sourceEvidencePreviewRef",
            "sourceRequestRef",
            "executionLockRef",
            "freezeGateRef",
            "humanEscalationRef",
            "committeeEscalationRef",
            "stopAuthorityRef",
            "notificationTargetRefs",
            "incidentAuditTrailRef",
            "harnessEvidenceCandidateRef",
            "repairOrReopenWorkItemRef",
            "holdContextRefs",
        },
        "required_escalation_ref",
    )

    blocking_conditions = set(escalation.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_rollback_drill_not_candidate_preview_with_hold",
            "source_rollback_drill_already_executed",
            "source_rollback_already_executed",
            "source_rollback_drill_not_dry_run_only",
            "missing_source_rollback_drill_ref",
            "missing_source_verification_plan_ref",
            "missing_source_evidence_preview_ref",
            "missing_source_request_ref",
            "missing_execution_lock_ref",
            "missing_freeze_gate_ref",
            "missing_human_escalation_ref",
            "missing_committee_escalation_ref",
            "missing_stop_authority_ref",
            "missing_notification_targets",
            "missing_incident_audit_trail_ref",
            "missing_harness_evidence_candidate_ref",
            "missing_repair_or_reopen_work_item_ref",
            "missing_hold_context_refs",
            "incident_preview_attempts_write",
            "freeze_preview_attempts_execution",
        },
        "blocking_condition",
    )

    forbidden_actions = set(escalation.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_formal_write",
            "execute_rollback",
            "execute_freeze",
            "write_incident_result",
            "write_freeze_result",
            "write_formal_evidence",
            "write_harness_evidence",
            "write_verification_result",
            "write_rollback_result",
            "write_kds",
            "write_business_system",
            "promote_lifecycle",
            "mark_p0_accepted",
            "mark_production_ready",
            "convert_escalation_preview_to_result",
            "release_execution_lock",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_drill.get("holdContextRefs", []))
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

    require(evidence.get("current_incident_escalation_preview_status") == "candidate_preview_with_hold", "evidence_incident_escalation_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("escalation_scope", {}).get("incident_classes") == 8, "evidence_incident_class_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_rollback_drill_preview_status") == "candidate_preview_with_hold", "evidence_source_rollback_drill_preview_status_mismatch")

    d40_output = run_command("python3", "scripts/api/validate_gckf_p0_formal_evidence_execution_incident_escalation_preview_dry_run.py")
    require(d40_output.startswith("gckf_p0_formal_evidence_execution_incident_escalation_preview_dry_run=pass"), "d40_validator_not_pass")

    d138_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_formal_evidence_execution_rollback_drill_preview_current_state_d138.py")
    require(d138_output.startswith("gckf_p0_formal_evidence_execution_rollback_drill_preview_current_state_d138=pass"), "d138_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_incident_escalation_preview_current_state_d139=pass")
    print(f"incident_escalation_preview_status={fixture.get('incidentEscalationPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={escalation.get('previewStatus')}")
    print(f"execution_status={escalation.get('executionStatus')}")
    print(f"incident_execution_status={escalation.get('incidentExecutionStatus')}")
    print(f"freeze_execution_status={escalation.get('freezeExecutionStatus')}")
    print(f"incident_classes={len(incident_classes)}")
    print(f"escalation_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
