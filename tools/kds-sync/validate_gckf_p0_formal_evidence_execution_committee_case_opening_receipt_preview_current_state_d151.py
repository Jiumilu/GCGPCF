#!/usr/bin/env python3
"""Validate D151 GCKF P0 formal evidence execution committee case opening receipt preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-case-opening-receipt-preview-current-state-d151-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-committee-case-opening-receipt-preview-current-state-d151-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-committee-case-opening-receipt-preview-current-state-d151-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D151-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_case_opening_receipt_preview_current_state_d151=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d151_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_receipt = load_json(ROOT / fixture["sourceHistoricalCommitteeCaseOpeningReceiptPreview"])
    current_docket = load_json(ROOT / fixture["sourceCurrentCommitteeDocketReadinessPreview"])
    receipt = fixture["committeeCaseOpeningReceiptPreview"]
    source_receipt = historical_receipt["committeeCaseOpeningReceiptPreview"]
    docket = current_docket["committeeDocketReadinessPreview"]

    require(fixture.get("committeeCaseOpeningReceiptPreviewStatus") == expected["committeeCaseOpeningReceiptPreviewStatus"], "committee_case_opening_receipt_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalReceipt") is expected["notFinalReceipt"], "not_final_receipt_mismatch")
    require(receipt.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(receipt.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(receipt.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(receipt.get("intakeAcceptanceExecutionStatus") == expected["intakeAcceptanceExecutionStatus"], "intake_acceptance_execution_status_mismatch")
    require(receipt.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(receipt.get("committeeDocketExecutionStatus") == expected["committeeDocketExecutionStatus"], "committee_docket_execution_status_mismatch")
    require(receipt.get("committeeReceiptExecutionStatus") == expected["committeeReceiptExecutionStatus"], "committee_receipt_execution_status_mismatch")
    require(receipt.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(receipt.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(receipt.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(receipt.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(receipt.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(receipt.get("executionMode") == expected["executionMode"], "receipt_execution_mode_mismatch")
    require(receipt.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(receipt.get("sourceCommitteeDocketReadinessPreviewId") == docket.get("id"), "source_committee_docket_readiness_preview_id_mismatch")

    require(historical_receipt.get("committeeCaseOpeningReceiptPreviewStatus") == "candidate_preview", "historical_committee_case_opening_receipt_preview_status_mismatch")
    require(source_receipt.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_receipt.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_docket.get("committeeDocketReadinessPreviewStatus") == expected["sourceCommitteeDocketReadinessPreviewStatus"], "source_committee_docket_readiness_preview_status_mismatch")
    require(docket.get("intakeAcceptanceExecutionStatus") == expected["sourceIntakeAcceptanceExecutionStatus"], "source_intake_acceptance_execution_status_mismatch")
    require(docket.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(docket.get("committeeDocketExecutionStatus") == expected["sourceCommitteeDocketExecutionStatus"], "source_committee_docket_execution_status_mismatch")
    require(docket.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(docket.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(docket.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(docket.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeDocketReadinessPreviewStatus") == expected["coveredCommitteeDocketReadinessPreviewStatus"], "covered_committee_docket_readiness_preview_status_mismatch")
    require(fixture["coveredCommitteeDocketReadinessPreviewStatus"] == docket.get("previewStatus"), "covered_committee_docket_readiness_preview_not_matched")

    roles = set(receipt.get("receiptRoles", []))
    require(len(roles) == expected["receiptRoleCount"], "receipt_role_count_mismatch")
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
        "receipt_role",
    )
    require(roles == set(docket.get("docketRoles", [])), "receipt_roles_not_matched_to_docket_roles")

    sections = set(receipt.get("receiptSections", []))
    require(len(sections) == expected["receiptSectionCount"], "receipt_section_count_mismatch")
    require_all(
        sections,
        {
            "source_docket_readiness_lineage",
            "receipt_scope",
            "receipt_envelope_fields",
            "receipt_readiness_prerequisites",
            "material_index_acknowledgement",
            "reviewer_assignment_acknowledgement",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "return_to_docket_readiness_path",
            "no_write_attestation",
        },
        "receipt_section",
    )

    envelope_fields = set(receipt.get("receiptEnvelopeFields", []))
    require(len(envelope_fields) == expected["receiptEnvelopeFieldCount"], "receipt_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "receipt_preview_id",
            "source_docket_readiness_preview_id",
            "received_material_index_ref",
            "received_by_role",
            "received_at_preview_time",
            "receipt_status_candidate_preview",
            "exception_return_path_ref",
            "no_write_attestation_ref",
        },
        "receipt_envelope_field",
    )

    prerequisites = set(receipt.get("receiptReadinessPrerequisites", []))
    require(len(prerequisites) == expected["receiptReadinessPrerequisiteCount"], "receipt_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_docket_readiness_candidate_preview",
            "source_docket_not_created",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "source_confirmation_not_executed",
            "source_unfreeze_not_executed",
            "source_no_write_attestation_present",
            "receipt_not_formal_evidence",
        },
        "receipt_readiness_prerequisite",
    )

    decision_constraints = set(receipt.get("receiptDecisionConstraints", []))
    require(len(decision_constraints) == expected["receiptDecisionConstraintCount"], "receipt_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "receipt_preview_not_formal_receipt",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_freeze_release",
            "no_harness_evidence_write",
        },
        "receipt_decision_constraint",
    )

    checks = set(receipt.get("receiptChecks", []))
    require(len(checks) == expected["receiptCheckCount"], "receipt_check_count_mismatch")
    require_all(
        checks,
        {
            "source_docket_readiness_preview_status_is_candidate_preview_with_hold",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_docket_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_docket_readiness_is_dry_run_only",
            "committee_case_opening_receipt_preview_status_is_candidate_preview_with_hold",
            "all_receipt_roles_covered",
            "all_receipt_sections_covered",
            "all_receipt_envelope_fields_covered",
            "all_receipt_readiness_prerequisites_covered",
            "all_receipt_decision_constraints_covered",
            "receipt_scope_present",
            "material_index_acknowledgement_present",
            "reviewer_assignment_acknowledgement_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "return_to_docket_readiness_path_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_receipt_preview_not_formal_receipt",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "receipt_check",
    )

    refs = set(receipt.get("requiredReceiptRefs", []))
    require(len(refs) == expected["requiredReceiptRefCount"], "required_receipt_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeDocketReadinessPreviewRef",
            "sourceCommitteeCaseOpeningGuardPreviewRef",
            "receiptScopeRef",
            "receiptEnvelopeFieldsRef",
            "receiptReadinessPrerequisitesRef",
            "materialIndexAcknowledgementRef",
            "reviewerAssignmentAcknowledgementRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "returnToDocketReadinessPathRef",
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
        "required_receipt_ref",
    )

    blocking_conditions = set(receipt.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_docket_readiness_not_candidate_preview_with_hold",
            "source_intake_acceptance_already_executed",
            "source_committee_packet_already_submitted",
            "source_committee_docket_already_created",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_docket_readiness_not_dry_run_only",
            "missing_source_docket_readiness_ref",
            "missing_receipt_scope_ref",
            "missing_receipt_envelope_fields_ref",
            "missing_material_index_acknowledgement_ref",
            "missing_reviewer_assignment_acknowledgement_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_return_to_docket_readiness_path_ref",
            "missing_required_receipt_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "receipt_preview_attempts_formal_receipt",
            "receipt_preview_attempts_docket_creation",
            "receipt_preview_attempts_case_opening",
            "receipt_preview_attempts_committee_decision",
            "receipt_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(receipt.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "create_committee_docket",
            "record_committee_receipt",
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
            "convert_receipt_preview_to_formal_receipt",
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
    source_hold_refs = set(current_docket.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_case_opening_receipt_preview_status") == "candidate_preview_with_hold", "evidence_committee_case_opening_receipt_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("receipt_roles") == 8, "evidence_receipt_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_docket_readiness_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_docket_readiness_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_case_opening_receipt_preview_current_state_d151=pass")
    print(f"committee_case_opening_receipt_preview_status={fixture.get('committeeCaseOpeningReceiptPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={receipt.get('previewStatus')}")
    print(f"execution_status={receipt.get('executionStatus')}")
    print(f"intake_acceptance_execution_status={receipt.get('intakeAcceptanceExecutionStatus')}")
    print(f"committee_submission_execution_status={receipt.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_docket_execution_status={receipt.get('committeeDocketExecutionStatus')}")
    print(f"committee_receipt_execution_status={receipt.get('committeeReceiptExecutionStatus')}")
    print(f"committee_case_execution_status={receipt.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={receipt.get('committeeDecisionExecutionStatus')}")
    print(f"receipt_roles={len(roles)}")
    print(f"receipt_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
