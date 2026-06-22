#!/usr/bin/env python3
"""Validate D149 GCKF P0 formal evidence execution committee case opening guard preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-case-opening-guard-preview-current-state-d149-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-case-opening-guard-preview-current-state-d149-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-formal-evidence-execution-committee-case-opening-guard-preview-current-state-d149-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D149-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_case_opening_guard_preview_current_state_d149=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d149_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_guard = load_json(ROOT / fixture["sourceHistoricalCommitteeCaseOpeningGuardPreview"])
    current_precheck = load_json(ROOT / fixture["sourceCurrentCommitteeIntakeAcceptancePrecheckPreview"])
    guard = fixture["committeeCaseOpeningGuardPreview"]
    source_guard = historical_guard["committeeCaseOpeningGuardPreview"]
    precheck = current_precheck["committeeIntakeAcceptancePrecheckPreview"]

    require(fixture.get("committeeCaseOpeningGuardPreviewStatus") == expected["committeeCaseOpeningGuardPreviewStatus"], "committee_case_opening_guard_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalCaseOpening") is expected["notFinalCaseOpening"], "not_final_case_opening_mismatch")
    require(guard.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(guard.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(guard.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(guard.get("intakeAcceptanceExecutionStatus") == expected["intakeAcceptanceExecutionStatus"], "intake_acceptance_execution_status_mismatch")
    require(guard.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(guard.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(guard.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(guard.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(guard.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(guard.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(guard.get("executionMode") == expected["executionMode"], "guard_execution_mode_mismatch")
    require(guard.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(guard.get("sourceCommitteeIntakeAcceptancePrecheckPreviewId") == precheck.get("id"), "source_committee_intake_acceptance_precheck_preview_id_mismatch")

    require(historical_guard.get("committeeCaseOpeningGuardPreviewStatus") == "candidate_preview", "historical_committee_case_opening_guard_preview_status_mismatch")
    require(source_guard.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_guard.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_precheck.get("committeeIntakeAcceptancePrecheckPreviewStatus") == expected["sourceCommitteeIntakeAcceptancePrecheckPreviewStatus"], "source_committee_intake_acceptance_precheck_preview_status_mismatch")
    require(precheck.get("intakeAcceptanceExecutionStatus") == expected["sourceIntakeAcceptanceExecutionStatus"], "source_intake_acceptance_execution_status_mismatch")
    require(precheck.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(precheck.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(precheck.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(precheck.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(precheck.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeIntakeAcceptancePrecheckPreviewStatus") == expected["coveredCommitteeIntakeAcceptancePrecheckPreviewStatus"], "covered_committee_intake_acceptance_precheck_preview_status_mismatch")
    require(fixture["coveredCommitteeIntakeAcceptancePrecheckPreviewStatus"] == precheck.get("previewStatus"), "covered_committee_intake_acceptance_precheck_preview_not_matched")

    roles = set(guard.get("guardRoles", []))
    require(len(roles) == expected["guardRoleCount"], "guard_role_count_mismatch")
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
        "guard_role",
    )
    require(roles == set(precheck.get("precheckRoles", [])), "guard_roles_not_matched_to_precheck_roles")

    sections = set(guard.get("guardSections", []))
    require(len(sections) == expected["guardSectionCount"], "guard_section_count_mismatch")
    require_all(
        sections,
        {
            "source_intake_precheck_lineage",
            "case_opening_scope",
            "case_opening_prerequisites",
            "committee_submission_readiness",
            "committee_authority_boundary",
            "freeze_retention_guard",
            "waes_negative_gate_guard",
            "harness_no_write_guard",
            "business_system_no_write_guard",
            "revenue_contribution_no_write_guard",
            "return_to_intake_precheck_path",
            "no_write_attestation",
        },
        "guard_section",
    )

    prerequisites = set(guard.get("caseOpeningPrerequisites", []))
    require(len(prerequisites) == expected["caseOpeningPrerequisiteCount"], "case_opening_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_intake_precheck_candidate_preview",
            "source_intake_precheck_not_acceptance",
            "source_case_packet_not_submitted",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "source_confirmation_not_executed",
            "source_unfreeze_not_executed",
            "source_no_write_attestation_present",
        },
        "case_opening_prerequisite",
    )

    decision_constraints = set(guard.get("guardDecisionConstraints", []))
    require(len(decision_constraints) == expected["guardDecisionConstraintCount"], "guard_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "guard_not_case_opening",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "guard_decision_constraint",
    )

    checks = set(guard.get("guardChecks", []))
    require(len(checks) == expected["guardCheckCount"], "guard_check_count_mismatch")
    require_all(
        checks,
        {
            "source_intake_precheck_preview_status_is_candidate_preview_with_hold",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_precheck_is_dry_run_only",
            "committee_case_opening_guard_preview_status_is_candidate_preview_with_hold",
            "all_guard_roles_covered",
            "all_guard_sections_covered",
            "all_case_opening_prerequisites_covered",
            "all_guard_decision_constraints_covered",
            "case_opening_scope_present",
            "committee_submission_readiness_present",
            "committee_authority_boundary_present",
            "freeze_retention_guard_present",
            "waes_negative_gate_guard_present",
            "harness_no_write_guard_present",
            "business_system_no_write_guard_present",
            "revenue_contribution_no_write_guard_present",
            "return_to_intake_precheck_path_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_guard_not_case_opening",
            "assert_committee_case_not_opened",
            "assert_committee_decision_not_executed",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "guard_check",
    )

    refs = set(guard.get("requiredGuardRefs", []))
    require(len(refs) == expected["requiredGuardRefCount"], "required_guard_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeIntakeAcceptancePrecheckPreviewRef",
            "sourceCommitteeCaseReviewPacketPreviewRef",
            "caseOpeningScopeRef",
            "caseOpeningPrerequisitesRef",
            "committeeSubmissionReadinessRef",
            "committeeAuthorityBoundaryRef",
            "freezeRetentionGuardRef",
            "waesNegativeGateGuardRef",
            "harnessNoWriteGuardRef",
            "businessSystemNoWriteGuardRef",
            "revenueContributionNoWriteGuardRef",
            "returnToIntakePrecheckPathRef",
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
        "required_guard_ref",
    )

    blocking_conditions = set(guard.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_intake_precheck_not_candidate_preview_with_hold",
            "source_intake_acceptance_already_executed",
            "source_committee_packet_already_submitted",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_precheck_not_dry_run_only",
            "missing_source_intake_precheck_ref",
            "missing_case_opening_scope_ref",
            "missing_case_opening_prerequisites_ref",
            "missing_committee_submission_readiness_ref",
            "missing_committee_authority_boundary_ref",
            "missing_freeze_retention_guard_ref",
            "missing_waes_negative_gate_guard_ref",
            "missing_harness_no_write_guard_ref",
            "missing_business_system_no_write_guard_ref",
            "missing_revenue_contribution_no_write_guard_ref",
            "missing_return_to_intake_precheck_path_ref",
            "missing_required_guard_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "guard_attempts_intake_acceptance",
            "guard_attempts_committee_submission",
            "guard_attempts_case_opening",
            "guard_attempts_committee_decision",
            "guard_attempts_formal_write",
            "guard_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(guard.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "execute_formal_write",
            "record_intake_acceptance",
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
            "convert_guard_preview_to_case_opening",
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
    source_hold_refs = set(current_precheck.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_case_opening_guard_preview_status") == "candidate_preview_with_hold", "evidence_committee_case_opening_guard_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("guard_roles") == 8, "evidence_guard_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_intake_acceptance_precheck_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_intake_acceptance_precheck_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_case_opening_guard_preview_current_state_d149=pass")
    print(f"committee_case_opening_guard_preview_status={fixture.get('committeeCaseOpeningGuardPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={guard.get('previewStatus')}")
    print(f"execution_status={guard.get('executionStatus')}")
    print(f"intake_acceptance_execution_status={guard.get('intakeAcceptanceExecutionStatus')}")
    print(f"committee_submission_execution_status={guard.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_case_execution_status={guard.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={guard.get('committeeDecisionExecutionStatus')}")
    print(f"guard_roles={len(roles)}")
    print(f"guard_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
