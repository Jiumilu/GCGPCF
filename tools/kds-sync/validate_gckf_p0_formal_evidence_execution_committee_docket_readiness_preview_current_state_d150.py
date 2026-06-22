#!/usr/bin/env python3
"""Validate D150 GCKF P0 formal evidence execution committee docket readiness preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-docket-readiness-preview-current-state-d150-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-docket-readiness-preview-current-state-d150-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-docket-readiness-preview-current-state-d150-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D150-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_docket_readiness_preview_current_state_d150=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d150_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_docket = load_json(ROOT / fixture["sourceHistoricalCommitteeDocketReadinessPreview"])
    current_guard = load_json(ROOT / fixture["sourceCurrentCommitteeCaseOpeningGuardPreview"])
    docket = fixture["committeeDocketReadinessPreview"]
    source_docket = historical_docket["committeeDocketReadinessPreview"]
    guard = current_guard["committeeCaseOpeningGuardPreview"]

    require(fixture.get("committeeDocketReadinessPreviewStatus") == expected["committeeDocketReadinessPreviewStatus"], "committee_docket_readiness_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalDocket") is expected["notFinalDocket"], "not_final_docket_mismatch")
    require(docket.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(docket.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(docket.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(docket.get("intakeAcceptanceExecutionStatus") == expected["intakeAcceptanceExecutionStatus"], "intake_acceptance_execution_status_mismatch")
    require(docket.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(docket.get("committeeDocketExecutionStatus") == expected["committeeDocketExecutionStatus"], "committee_docket_execution_status_mismatch")
    require(docket.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(docket.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(docket.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(docket.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(docket.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(docket.get("executionMode") == expected["executionMode"], "docket_execution_mode_mismatch")
    require(docket.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(docket.get("sourceCommitteeCaseOpeningGuardPreviewId") == guard.get("id"), "source_committee_case_opening_guard_preview_id_mismatch")

    require(historical_docket.get("committeeDocketReadinessPreviewStatus") == "candidate_preview", "historical_committee_docket_readiness_preview_status_mismatch")
    require(source_docket.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_docket.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_guard.get("committeeCaseOpeningGuardPreviewStatus") == expected["sourceCommitteeCaseOpeningGuardPreviewStatus"], "source_committee_case_opening_guard_preview_status_mismatch")
    require(guard.get("intakeAcceptanceExecutionStatus") == expected["sourceIntakeAcceptanceExecutionStatus"], "source_intake_acceptance_execution_status_mismatch")
    require(guard.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(guard.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(guard.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(guard.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(guard.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeCaseOpeningGuardPreviewStatus") == expected["coveredCommitteeCaseOpeningGuardPreviewStatus"], "covered_committee_case_opening_guard_preview_status_mismatch")
    require(fixture["coveredCommitteeCaseOpeningGuardPreviewStatus"] == guard.get("previewStatus"), "covered_committee_case_opening_guard_preview_not_matched")

    roles = set(docket.get("docketRoles", []))
    require(len(roles) == expected["docketRoleCount"], "docket_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner",
        },
        "docket_role",
    )
    require(roles == set(guard.get("guardRoles", [])), "docket_roles_not_matched_to_guard_roles")

    sections = set(docket.get("docketSections", []))
    require(len(sections) == expected["docketSectionCount"], "docket_section_count_mismatch")
    require_all(
        sections,
        {
            "source_case_opening_guard_lineage",
            "docket_scope",
            "docket_readiness_prerequisites",
            "committee_material_index",
            "reviewer_assignment_readiness",
            "authority_and_recusal_boundary",
            "freeze_retention_guard",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "business_system_no_write_guard",
            "return_to_case_opening_guard_path",
            "no_write_attestation",
        },
        "docket_section",
    )

    prerequisites = set(docket.get("docketReadinessPrerequisites", []))
    require(len(prerequisites) == expected["docketReadinessPrerequisiteCount"], "docket_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_case_opening_guard_candidate_preview",
            "source_guard_not_case_opening",
            "source_intake_acceptance_not_executed",
            "source_committee_submission_not_executed",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "source_unfreeze_not_executed",
            "source_no_write_attestation_present",
        },
        "docket_readiness_prerequisite",
    )

    decision_constraints = set(docket.get("docketDecisionConstraints", []))
    require(len(decision_constraints) == expected["docketDecisionConstraintCount"], "docket_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "docket_readiness_not_docket_creation",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_harness_evidence_write",
        },
        "docket_decision_constraint",
    )

    checks = set(docket.get("docketChecks", []))
    require(len(checks) == expected["docketCheckCount"], "docket_check_count_mismatch")
    require_all(
        checks,
        {
            "source_case_opening_guard_preview_status_is_candidate_preview_with_hold",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_guard_is_dry_run_only",
            "committee_docket_readiness_preview_status_is_candidate_preview_with_hold",
            "all_docket_roles_covered",
            "all_docket_sections_covered",
            "all_docket_readiness_prerequisites_covered",
            "all_docket_decision_constraints_covered",
            "docket_scope_present",
            "committee_material_index_present",
            "reviewer_assignment_readiness_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_guard_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "business_system_no_write_guard_present",
            "return_to_case_opening_guard_path_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_docket_readiness_not_docket_creation",
            "assert_committee_docket_not_created",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "docket_check",
    )

    refs = set(docket.get("requiredDocketRefs", []))
    require(len(refs) == expected["requiredDocketRefCount"], "required_docket_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseOpeningGuardPreviewRef",
            "sourceCommitteeIntakeAcceptancePrecheckPreviewRef",
            "docketScopeRef",
            "docketReadinessPrerequisitesRef",
            "committeeMaterialIndexRef",
            "reviewerAssignmentReadinessRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionGuardRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "businessSystemNoWriteGuardRef",
            "returnToCaseOpeningGuardPathRef",
            "requestOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
            "holdContextRefs",
        },
        "required_docket_ref",
    )

    blocking_conditions = set(docket.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_case_opening_guard_not_candidate_preview_with_hold",
            "source_intake_acceptance_already_executed",
            "source_committee_packet_already_submitted",
            "source_committee_docket_already_created",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_guard_not_dry_run_only",
            "missing_source_case_opening_guard_ref",
            "missing_docket_scope_ref",
            "missing_docket_readiness_prerequisites_ref",
            "missing_committee_material_index_ref",
            "missing_reviewer_assignment_readiness_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_guard_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_business_system_no_write_guard_ref",
            "missing_return_to_case_opening_guard_path_ref",
            "missing_required_docket_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "docket_preview_attempts_intake_acceptance",
            "docket_preview_attempts_committee_submission",
            "docket_preview_attempts_docket_creation",
            "docket_preview_attempts_case_opening",
            "docket_preview_attempts_committee_decision",
            "docket_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(docket.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "create_committee_docket",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "record_intake_acceptance",
            "record_committee_docket",
            "record_committee_case",
            "record_committee_result",
            "write_harness_evidence",
            "write_formal_evidence",
            "write_kds",
            "write_business_system",
            "write_revenue_distribution",
            "write_contribution_score",
            "promote_lifecycle",
            "mark_p0_accepted",
            "convert_docket_readiness_preview_to_docket",
            "override_waes_gate",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    forbidden_outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(forbidden_outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")

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

    require(evidence.get("current_committee_docket_readiness_preview_status") == "candidate_preview_with_hold", "evidence_committee_docket_readiness_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("docket_roles") == 8, "evidence_docket_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_case_opening_guard_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_case_opening_guard_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_docket_readiness_preview_current_state_d150=pass")
    print(f"committee_docket_readiness_preview_status={fixture.get('committeeDocketReadinessPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={docket.get('previewStatus')}")
    print(f"execution_status={docket.get('executionStatus')}")
    print(f"intake_acceptance_execution_status={docket.get('intakeAcceptanceExecutionStatus')}")
    print(f"committee_submission_execution_status={docket.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_docket_execution_status={docket.get('committeeDocketExecutionStatus')}")
    print(f"committee_case_execution_status={docket.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={docket.get('committeeDecisionExecutionStatus')}")
    print(f"docket_roles={len(roles)}")
    print(f"docket_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
