#!/usr/bin/env python3
"""Validate D153 GCKF P0 formal evidence execution committee case opening exception return preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-case-opening-exception-return-preview-current-state-d153-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-committee-case-opening-exception-return-preview-current-state-d153-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-committee-case-opening-exception-return-preview-current-state-d153-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D153-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_case_opening_exception_return_preview_current_state_d153=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d153_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_return = load_json(ROOT / fixture["sourceHistoricalCommitteeCaseOpeningExceptionReturnPreview"])
    current_routing = load_json(ROOT / fixture["sourceCurrentCommitteeReceiptAcknowledgementRoutingPreview"])
    return_preview = fixture["committeeCaseOpeningExceptionReturnPreview"]
    source_return = historical_return["committeeCaseOpeningExceptionReturnPreview"]
    routing = current_routing["committeeReceiptAcknowledgementRoutingPreview"]

    require(fixture.get("committeeCaseOpeningExceptionReturnPreviewStatus") == expected["committeeCaseOpeningExceptionReturnPreviewStatus"], "committee_case_opening_exception_return_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalReturn") is expected["notFinalReturn"], "not_final_return_mismatch")
    require(return_preview.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(return_preview.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(return_preview.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(return_preview.get("intakeAcceptanceExecutionStatus") == expected["intakeAcceptanceExecutionStatus"], "intake_acceptance_execution_status_mismatch")
    require(return_preview.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(return_preview.get("committeeDocketExecutionStatus") == expected["committeeDocketExecutionStatus"], "committee_docket_execution_status_mismatch")
    require(return_preview.get("committeeReceiptExecutionStatus") == expected["committeeReceiptExecutionStatus"], "committee_receipt_execution_status_mismatch")
    require(return_preview.get("committeeRoutingExecutionStatus") == expected["committeeRoutingExecutionStatus"], "committee_routing_execution_status_mismatch")
    require(return_preview.get("committeeExceptionReturnExecutionStatus") == expected["committeeExceptionReturnExecutionStatus"], "committee_exception_return_execution_status_mismatch")
    require(return_preview.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(return_preview.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(return_preview.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(return_preview.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(return_preview.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(return_preview.get("executionMode") == expected["executionMode"], "return_execution_mode_mismatch")
    require(return_preview.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(return_preview.get("sourceCommitteeReceiptAcknowledgementRoutingPreviewId") == routing.get("id"), "source_committee_receipt_acknowledgement_routing_preview_id_mismatch")

    require(historical_return.get("committeeCaseOpeningExceptionReturnPreviewStatus") == "candidate_preview", "historical_committee_case_opening_exception_return_preview_status_mismatch")
    require(source_return.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_return.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_routing.get("committeeReceiptAcknowledgementRoutingPreviewStatus") == expected["sourceCommitteeReceiptAcknowledgementRoutingPreviewStatus"], "source_committee_receipt_acknowledgement_routing_preview_status_mismatch")
    require(routing.get("intakeAcceptanceExecutionStatus") == expected["sourceIntakeAcceptanceExecutionStatus"], "source_intake_acceptance_execution_status_mismatch")
    require(routing.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(routing.get("committeeDocketExecutionStatus") == expected["sourceCommitteeDocketExecutionStatus"], "source_committee_docket_execution_status_mismatch")
    require(routing.get("committeeReceiptExecutionStatus") == expected["sourceCommitteeReceiptExecutionStatus"], "source_committee_receipt_execution_status_mismatch")
    require(routing.get("committeeRoutingExecutionStatus") == expected["sourceCommitteeRoutingExecutionStatus"], "source_committee_routing_execution_status_mismatch")
    require(routing.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(routing.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(routing.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(routing.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeReceiptAcknowledgementRoutingPreviewStatus") == expected["coveredCommitteeReceiptAcknowledgementRoutingPreviewStatus"], "covered_committee_receipt_acknowledgement_routing_preview_status_mismatch")
    require(fixture["coveredCommitteeReceiptAcknowledgementRoutingPreviewStatus"] == routing.get("previewStatus"), "covered_committee_receipt_acknowledgement_routing_preview_not_matched")

    roles = set(return_preview.get("returnRoles", []))
    require(len(roles) == expected["returnRoleCount"], "return_role_count_mismatch")
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
        "return_role",
    )
    require(roles == set(routing.get("routingRoles", [])), "return_roles_not_matched_to_routing_roles")

    sections = set(return_preview.get("returnSections", []))
    require(len(sections) == expected["returnSectionCount"], "return_section_count_mismatch")
    require_all(
        sections,
        {
            "source_routing_lineage",
            "exception_return_scope",
            "return_envelope_fields",
            "return_readiness_prerequisites",
            "return_reason_candidates",
            "responsible_role_candidates",
            "supplement_request_candidates",
            "reentry_path_candidates",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "return_section",
    )

    envelope_fields = set(return_preview.get("returnEnvelopeFields", []))
    require(len(envelope_fields) == expected["returnEnvelopeFieldCount"], "return_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "return_preview_id",
            "source_routing_preview_id",
            "candidate_return_reason_code",
            "candidate_responsible_role",
            "candidate_required_supplement_ref",
            "candidate_reentry_path_ref",
            "candidate_return_status",
            "no_write_attestation_ref",
        },
        "return_envelope_field",
    )

    prerequisites = set(return_preview.get("returnReadinessPrerequisites", []))
    require(len(prerequisites) == expected["returnReadinessPrerequisiteCount"], "return_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_routing_candidate_preview_with_hold",
            "source_routing_not_formal_routing",
            "source_receipt_not_formal_receipt",
            "source_docket_not_created",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "source_confirmation_not_executed",
            "return_not_formal_evidence",
        },
        "return_readiness_prerequisite",
    )

    decision_constraints = set(return_preview.get("returnDecisionConstraints", []))
    require(len(decision_constraints) == expected["returnDecisionConstraintCount"], "return_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "return_preview_not_formal_return",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_formal_receipt_record",
            "no_formal_routing_execution",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_harness_evidence_write",
        },
        "return_decision_constraint",
    )

    checks = set(return_preview.get("returnChecks", []))
    require(len(checks) == expected["returnCheckCount"], "return_check_count_mismatch")
    require_all(
        checks,
        {
            "source_routing_preview_status_is_candidate_preview_with_hold",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_docket_execution_status_is_not_executed",
            "source_committee_receipt_execution_status_is_not_executed",
            "source_committee_routing_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_routing_preview_is_dry_run_only",
            "committee_case_opening_exception_return_preview_status_is_candidate_preview_with_hold",
            "all_return_roles_covered",
            "all_return_sections_covered",
            "all_return_envelope_fields_covered",
            "all_return_readiness_prerequisites_covered",
            "all_return_decision_constraints_covered",
            "return_reason_candidates_present",
            "responsible_role_candidates_present",
            "supplement_request_candidates_present",
            "reentry_path_candidates_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_return_preview_not_formal_return",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "return_check",
    )

    refs = set(return_preview.get("requiredReturnRefs", []))
    require(len(refs) == expected["requiredReturnRefCount"], "required_return_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeReceiptAcknowledgementRoutingPreviewRef",
            "sourceCommitteeCaseOpeningReceiptPreviewRef",
            "exceptionReturnScopeRef",
            "returnEnvelopeFieldsRef",
            "returnReadinessPrerequisitesRef",
            "returnReasonCandidatesRef",
            "responsibleRoleCandidatesRef",
            "supplementRequestCandidatesRef",
            "reentryPathCandidatesRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
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
        "required_return_ref",
    )

    blocking_conditions = set(return_preview.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_routing_preview_not_candidate_preview_with_hold",
            "source_routing_already_executed",
            "source_receipt_already_recorded",
            "source_intake_acceptance_already_executed",
            "source_committee_packet_already_submitted",
            "source_committee_docket_already_created",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_routing_preview_not_dry_run_only",
            "missing_source_routing_preview_ref",
            "missing_exception_return_scope_ref",
            "missing_return_envelope_fields_ref",
            "missing_return_reason_candidates_ref",
            "missing_responsible_role_candidates_ref",
            "missing_supplement_request_candidates_ref",
            "missing_reentry_path_candidates_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_return_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "return_preview_attempts_formal_return",
            "return_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(return_preview.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "create_committee_docket",
            "record_committee_receipt",
            "execute_committee_routing",
            "execute_committee_exception_return",
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
            "convert_return_preview_to_formal_return",
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
    source_hold_refs = set(current_routing.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_case_opening_exception_return_preview_status") == "candidate_preview_with_hold", "evidence_committee_case_opening_exception_return_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("return_roles") == 8, "evidence_return_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_receipt_acknowledgement_routing_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_receipt_acknowledgement_routing_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_case_opening_exception_return_preview_current_state_d153=pass")
    print(f"committee_case_opening_exception_return_preview_status={fixture.get('committeeCaseOpeningExceptionReturnPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={return_preview.get('previewStatus')}")
    print(f"execution_status={return_preview.get('executionStatus')}")
    print(f"intake_acceptance_execution_status={return_preview.get('intakeAcceptanceExecutionStatus')}")
    print(f"committee_submission_execution_status={return_preview.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_docket_execution_status={return_preview.get('committeeDocketExecutionStatus')}")
    print(f"committee_receipt_execution_status={return_preview.get('committeeReceiptExecutionStatus')}")
    print(f"committee_routing_execution_status={return_preview.get('committeeRoutingExecutionStatus')}")
    print(f"committee_exception_return_execution_status={return_preview.get('committeeExceptionReturnExecutionStatus')}")
    print(f"committee_case_execution_status={return_preview.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={return_preview.get('committeeDecisionExecutionStatus')}")
    print(f"return_roles={len(roles)}")
    print(f"return_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
