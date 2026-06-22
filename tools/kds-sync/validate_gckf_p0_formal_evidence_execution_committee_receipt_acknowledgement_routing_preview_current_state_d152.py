#!/usr/bin/env python3
"""Validate D152 GCKF P0 formal evidence execution committee receipt acknowledgement routing preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-receipt-acknowledgement-routing-preview-current-state-d152-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-committee-receipt-acknowledgement-routing-preview-current-state-d152-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-committee-receipt-acknowledgement-routing-preview-current-state-d152-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D152-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_committee_receipt_acknowledgement_routing_preview_current_state_d152=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d152_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_routing = load_json(ROOT / fixture["sourceHistoricalCommitteeReceiptAcknowledgementRoutingPreview"])
    current_receipt = load_json(ROOT / fixture["sourceCurrentCommitteeCaseOpeningReceiptPreview"])
    routing = fixture["committeeReceiptAcknowledgementRoutingPreview"]
    source_routing = historical_routing["committeeReceiptAcknowledgementRoutingPreview"]
    receipt = current_receipt["committeeCaseOpeningReceiptPreview"]

    require(fixture.get("committeeReceiptAcknowledgementRoutingPreviewStatus") == expected["committeeReceiptAcknowledgementRoutingPreviewStatus"], "committee_receipt_acknowledgement_routing_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalRouting") is expected["notFinalRouting"], "not_final_routing_mismatch")
    require(routing.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(routing.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(routing.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(routing.get("intakeAcceptanceExecutionStatus") == expected["intakeAcceptanceExecutionStatus"], "intake_acceptance_execution_status_mismatch")
    require(routing.get("committeeSubmissionExecutionStatus") == expected["committeeSubmissionExecutionStatus"], "committee_submission_execution_status_mismatch")
    require(routing.get("committeeDocketExecutionStatus") == expected["committeeDocketExecutionStatus"], "committee_docket_execution_status_mismatch")
    require(routing.get("committeeReceiptExecutionStatus") == expected["committeeReceiptExecutionStatus"], "committee_receipt_execution_status_mismatch")
    require(routing.get("committeeRoutingExecutionStatus") == expected["committeeRoutingExecutionStatus"], "committee_routing_execution_status_mismatch")
    require(routing.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(routing.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(routing.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(routing.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(routing.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(routing.get("executionMode") == expected["executionMode"], "routing_execution_mode_mismatch")
    require(routing.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(routing.get("sourceCommitteeCaseOpeningReceiptPreviewId") == receipt.get("id"), "source_committee_case_opening_receipt_preview_id_mismatch")

    require(historical_routing.get("committeeReceiptAcknowledgementRoutingPreviewStatus") == "candidate_preview", "historical_committee_receipt_acknowledgement_routing_preview_status_mismatch")
    require(source_routing.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_routing.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_receipt.get("committeeCaseOpeningReceiptPreviewStatus") == expected["sourceCommitteeCaseOpeningReceiptPreviewStatus"], "source_committee_case_opening_receipt_preview_status_mismatch")
    require(receipt.get("intakeAcceptanceExecutionStatus") == expected["sourceIntakeAcceptanceExecutionStatus"], "source_intake_acceptance_execution_status_mismatch")
    require(receipt.get("committeeSubmissionExecutionStatus") == expected["sourceCommitteeSubmissionExecutionStatus"], "source_committee_submission_execution_status_mismatch")
    require(receipt.get("committeeDocketExecutionStatus") == expected["sourceCommitteeDocketExecutionStatus"], "source_committee_docket_execution_status_mismatch")
    require(receipt.get("committeeReceiptExecutionStatus") == expected["sourceCommitteeReceiptExecutionStatus"], "source_committee_receipt_execution_status_mismatch")
    require(receipt.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(receipt.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(receipt.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(receipt.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredCommitteeCaseOpeningReceiptPreviewStatus") == expected["coveredCommitteeCaseOpeningReceiptPreviewStatus"], "covered_committee_case_opening_receipt_preview_status_mismatch")
    require(fixture["coveredCommitteeCaseOpeningReceiptPreviewStatus"] == receipt.get("previewStatus"), "covered_committee_case_opening_receipt_preview_not_matched")

    roles = set(routing.get("routingRoles", []))
    require(len(roles) == expected["routingRoleCount"], "routing_role_count_mismatch")
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
        "routing_role",
    )
    require(roles == set(receipt.get("receiptRoles", [])), "routing_roles_not_matched_to_receipt_roles")

    sections = set(routing.get("routingSections", []))
    require(len(sections) == expected["routingSectionCount"], "routing_section_count_mismatch")
    require_all(
        sections,
        {
            "source_receipt_lineage",
            "acknowledgement_scope",
            "routing_envelope_fields",
            "routing_readiness_prerequisites",
            "recipient_role_matrix",
            "routing_path_candidates",
            "exception_return_candidates",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "routing_section",
    )

    envelope_fields = set(routing.get("routingEnvelopeFields", []))
    require(len(envelope_fields) == expected["routingEnvelopeFieldCount"], "routing_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "routing_preview_id",
            "source_receipt_preview_id",
            "acknowledgement_material_index_ref",
            "candidate_recipient_role",
            "candidate_route_status",
            "candidate_route_reason",
            "exception_return_path_ref",
            "no_write_attestation_ref",
        },
        "routing_envelope_field",
    )

    prerequisites = set(routing.get("routingReadinessPrerequisites", []))
    require(len(prerequisites) == expected["routingReadinessPrerequisiteCount"], "routing_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_receipt_candidate_preview_with_hold",
            "source_receipt_not_formal_receipt",
            "source_docket_not_created",
            "source_committee_case_not_opened",
            "source_committee_decision_not_executed",
            "source_confirmation_not_executed",
            "source_unfreeze_not_executed",
            "routing_not_formal_evidence",
        },
        "routing_readiness_prerequisite",
    )

    decision_constraints = set(routing.get("routingDecisionConstraints", []))
    require(len(decision_constraints) == expected["routingDecisionConstraintCount"], "routing_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "routing_preview_not_formal_routing",
            "no_intake_acceptance",
            "no_committee_submission",
            "no_committee_docket_creation",
            "no_formal_receipt_record",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_harness_evidence_write",
        },
        "routing_decision_constraint",
    )

    checks = set(routing.get("routingChecks", []))
    require(len(checks) == expected["routingCheckCount"], "routing_check_count_mismatch")
    require_all(
        checks,
        {
            "source_receipt_preview_status_is_candidate_preview_with_hold",
            "source_intake_acceptance_execution_status_is_not_executed",
            "source_committee_submission_execution_status_is_not_executed",
            "source_committee_docket_execution_status_is_not_executed",
            "source_committee_receipt_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_receipt_preview_is_dry_run_only",
            "committee_receipt_acknowledgement_routing_preview_status_is_candidate_preview_with_hold",
            "all_routing_roles_covered",
            "all_routing_sections_covered",
            "all_routing_envelope_fields_covered",
            "all_routing_readiness_prerequisites_covered",
            "all_routing_decision_constraints_covered",
            "acknowledgement_scope_present",
            "recipient_role_matrix_present",
            "routing_path_candidates_present",
            "exception_return_candidates_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_routing_preview_not_formal_routing",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "routing_check",
    )

    refs = set(routing.get("requiredRoutingRefs", []))
    require(len(refs) == expected["requiredRoutingRefCount"], "required_routing_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceCommitteeCaseOpeningReceiptPreviewRef",
            "sourceCommitteeDocketReadinessPreviewRef",
            "acknowledgementScopeRef",
            "routingEnvelopeFieldsRef",
            "routingReadinessPrerequisitesRef",
            "recipientRoleMatrixRef",
            "routingPathCandidatesRef",
            "exceptionReturnCandidatesRef",
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
        "required_routing_ref",
    )

    blocking_conditions = set(routing.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_receipt_preview_not_candidate_preview_with_hold",
            "source_receipt_already_recorded",
            "source_intake_acceptance_already_executed",
            "source_committee_packet_already_submitted",
            "source_committee_docket_already_created",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_receipt_preview_not_dry_run_only",
            "missing_source_receipt_preview_ref",
            "missing_acknowledgement_scope_ref",
            "missing_routing_envelope_fields_ref",
            "missing_recipient_role_matrix_ref",
            "missing_routing_path_candidates_ref",
            "missing_exception_return_candidates_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_routing_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "routing_preview_attempts_formal_routing",
            "routing_preview_attempts_formal_receipt_record",
            "routing_preview_attempts_case_opening",
            "routing_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(routing.get("forbiddenActions", []))
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
            "convert_routing_preview_to_formal_routing",
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
    source_hold_refs = set(current_receipt.get("holdContextRefs", []))
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

    require(evidence.get("current_committee_receipt_acknowledgement_routing_preview_status") == "candidate_preview_with_hold", "evidence_committee_receipt_acknowledgement_routing_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("routing_roles") == 8, "evidence_routing_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_committee_case_opening_receipt_preview_status") == "candidate_preview_with_hold", "evidence_source_committee_case_opening_receipt_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_committee_receipt_acknowledgement_routing_preview_current_state_d152=pass")
    print(f"committee_receipt_acknowledgement_routing_preview_status={fixture.get('committeeReceiptAcknowledgementRoutingPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={routing.get('previewStatus')}")
    print(f"execution_status={routing.get('executionStatus')}")
    print(f"intake_acceptance_execution_status={routing.get('intakeAcceptanceExecutionStatus')}")
    print(f"committee_submission_execution_status={routing.get('committeeSubmissionExecutionStatus')}")
    print(f"committee_docket_execution_status={routing.get('committeeDocketExecutionStatus')}")
    print(f"committee_receipt_execution_status={routing.get('committeeReceiptExecutionStatus')}")
    print(f"committee_routing_execution_status={routing.get('committeeRoutingExecutionStatus')}")
    print(f"committee_case_execution_status={routing.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={routing.get('committeeDecisionExecutionStatus')}")
    print(f"routing_roles={len(roles)}")
    print(f"routing_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
