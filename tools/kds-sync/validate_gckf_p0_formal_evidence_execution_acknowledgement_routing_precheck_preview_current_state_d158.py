#!/usr/bin/env python3
"""Validate D158 GCKF P0 formal evidence execution acknowledgement routing precheck preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-acknowledgement-routing-precheck-preview-current-state-d158-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-acknowledgement-routing-precheck-preview-current-state-d158-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-acknowledgement-routing-precheck-preview-current-state-d158-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D158-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_formal_evidence_execution_acknowledgement_routing_precheck_preview_current_state_d158=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d158_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_routing = load_json(ROOT / fixture["sourceHistoricalAcknowledgementRoutingPrecheckPreview"])
    current_ack = load_json(ROOT / fixture["sourceCurrentRepairRequestAcknowledgementPreview"])
    routing = fixture["acknowledgementRoutingPrecheckPreview"]
    source_routing = historical_routing["acknowledgementRoutingPrecheckPreview"]
    acknowledgement = current_ack["repairRequestAcknowledgementPreview"]

    require(fixture.get("acknowledgementRoutingPrecheckPreviewStatus") == expected["acknowledgementRoutingPrecheckPreviewStatus"], "acknowledgement_routing_precheck_preview_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalRoutingPrecheck") is expected["notFinalRoutingPrecheck"], "not_final_routing_precheck_mismatch")
    require(routing.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(routing.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(routing.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(routing.get("routingPrecheckExecutionStatus") == expected["routingPrecheckExecutionStatus"], "routing_precheck_execution_status_mismatch")
    require(routing.get("routingExecutionStatus") == expected["routingExecutionStatus"], "routing_execution_status_mismatch")
    require(routing.get("acknowledgementExecutionStatus") == expected["acknowledgementExecutionStatus"], "acknowledgement_execution_status_mismatch")
    require(routing.get("repairRequestExecutionStatus") == expected["repairRequestExecutionStatus"], "repair_request_execution_status_mismatch")
    require(routing.get("supplementIntakeExecutionStatus") == expected["supplementIntakeExecutionStatus"], "supplement_intake_execution_status_mismatch")
    require(routing.get("supplementAcceptanceExecutionStatus") == expected["supplementAcceptanceExecutionStatus"], "supplement_acceptance_execution_status_mismatch")
    require(routing.get("committeeReentryExecutionStatus") == expected["committeeReentryExecutionStatus"], "committee_reentry_execution_status_mismatch")
    require(routing.get("committeeCaseExecutionStatus") == expected["committeeCaseExecutionStatus"], "committee_case_execution_status_mismatch")
    require(routing.get("committeeDecisionExecutionStatus") == expected["committeeDecisionExecutionStatus"], "committee_decision_execution_status_mismatch")
    require(routing.get("confirmationExecutionStatus") == expected["confirmationExecutionStatus"], "confirmation_execution_status_mismatch")
    require(routing.get("unfreezeExecutionStatus") == expected["unfreezeExecutionStatus"], "unfreeze_execution_status_mismatch")
    require(routing.get("formalWriteExecutionStatus") == expected["formalWriteExecutionStatus"], "formal_write_execution_status_mismatch")
    require(routing.get("executionMode") == expected["executionMode"], "routing_execution_mode_mismatch")
    require(routing.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(routing.get("sourceRepairRequestAcknowledgementPreviewId") == acknowledgement.get("id"), "source_repair_request_acknowledgement_preview_id_mismatch")

    require(historical_routing.get("acknowledgementRoutingPrecheckPreviewStatus") == "candidate_preview", "historical_routing_precheck_preview_status_mismatch")
    require(source_routing.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_routing.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")
    require(current_ack.get("repairRequestAcknowledgementPreviewStatus") == expected["sourceRepairRequestAcknowledgementPreviewStatus"], "source_acknowledgement_preview_status_mismatch")
    require(acknowledgement.get("acknowledgementExecutionStatus") == expected["sourceAcknowledgementExecutionStatus"], "source_acknowledgement_execution_status_mismatch")
    require(acknowledgement.get("repairRequestExecutionStatus") == expected["sourceRepairRequestExecutionStatus"], "source_repair_request_execution_status_mismatch")
    require(acknowledgement.get("supplementIntakeExecutionStatus") == expected["sourceSupplementIntakeExecutionStatus"], "source_supplement_intake_execution_status_mismatch")
    require(acknowledgement.get("supplementAcceptanceExecutionStatus") == expected["sourceSupplementAcceptanceExecutionStatus"], "source_supplement_acceptance_execution_status_mismatch")
    require(acknowledgement.get("committeeReentryExecutionStatus") == expected["sourceCommitteeReentryExecutionStatus"], "source_committee_reentry_execution_status_mismatch")
    require(acknowledgement.get("committeeCaseExecutionStatus") == expected["sourceCommitteeCaseExecutionStatus"], "source_committee_case_execution_status_mismatch")
    require(acknowledgement.get("committeeDecisionExecutionStatus") == expected["sourceCommitteeDecisionExecutionStatus"], "source_committee_decision_execution_status_mismatch")
    require(acknowledgement.get("confirmationExecutionStatus") == expected["sourceConfirmationExecutionStatus"], "source_confirmation_execution_status_mismatch")
    require(acknowledgement.get("unfreezeExecutionStatus") == expected["sourceUnfreezeExecutionStatus"], "source_unfreeze_execution_status_mismatch")
    require(fixture.get("coveredRepairRequestAcknowledgementPreviewStatus") == expected["coveredRepairRequestAcknowledgementPreviewStatus"], "covered_repair_request_acknowledgement_preview_status_mismatch")
    require(fixture["coveredRepairRequestAcknowledgementPreviewStatus"] == acknowledgement.get("previewStatus"), "covered_repair_request_acknowledgement_preview_not_matched")

    roles = set(routing.get("routingPrecheckRoles", []))
    require(len(roles) == expected["routingPrecheckRoleCount"], "routing_precheck_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "acknowledgement_owner",
            "routing_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner",
        },
        "routing_precheck_role",
    )
    require(set(acknowledgement.get("acknowledgementRoles", [])).issubset(roles), "routing_precheck_roles_not_covering_acknowledgement_roles")

    sections = set(routing.get("routingPrecheckSections", []))
    require(len(sections) == expected["routingPrecheckSectionCount"], "routing_precheck_section_count_mismatch")
    require_all(
        sections,
        {
            "source_acknowledgement_lineage",
            "routing_precheck_scope",
            "routing_precheck_envelope_fields",
            "routing_precheck_readiness_prerequisites",
            "routing_eligibility_candidates",
            "reviewer_lane_candidates",
            "blocked_routing_reason_candidates",
            "response_due_window_snapshot",
            "candidate_routing_path",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "routing_precheck_section",
    )

    envelope_fields = set(routing.get("routingPrecheckEnvelopeFields", []))
    require(len(envelope_fields) == expected["routingPrecheckEnvelopeFieldCount"], "routing_precheck_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "routing_precheck_preview_id",
            "source_acknowledgement_preview_id",
            "candidate_routing_eligibility_ref",
            "candidate_reviewer_lane",
            "candidate_blocked_reason_code",
            "candidate_response_due_window",
            "candidate_routing_path_ref",
            "candidate_routing_precheck_status",
            "no_write_attestation_ref",
        },
        "routing_precheck_envelope_field",
    )

    prerequisites = set(routing.get("routingPrecheckReadinessPrerequisites", []))
    require(len(prerequisites) == expected["routingPrecheckReadinessPrerequisiteCount"], "routing_precheck_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_acknowledgement_candidate_preview_with_hold",
            "source_acknowledgement_not_formal_acknowledgement",
            "source_acknowledgement_not_executed",
            "source_repair_request_not_executed",
            "source_supplement_material_not_accepted",
            "source_committee_reentry_not_executed",
            "source_committee_case_not_opened",
            "routing_precheck_not_formal_evidence",
        },
        "routing_precheck_readiness_prerequisite",
    )

    decision_constraints = set(routing.get("routingPrecheckDecisionConstraints", []))
    require(len(decision_constraints) == expected["routingPrecheckDecisionConstraintCount"], "routing_precheck_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "routing_precheck_preview_not_formal_routing_precheck",
            "no_routing_precheck_execution",
            "no_routing_execution",
            "no_acknowledgement_execution",
            "no_repair_request_execution",
            "no_supplement_acceptance",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_harness_evidence_write",
        },
        "routing_precheck_decision_constraint",
    )

    checks = set(routing.get("routingPrecheckChecks", []))
    require(len(checks) == expected["routingPrecheckCheckCount"], "routing_precheck_check_count_mismatch")
    require_all(
        checks,
        {
            "source_acknowledgement_preview_status_is_candidate_preview_with_hold",
            "source_acknowledgement_execution_status_is_not_executed",
            "source_repair_request_execution_status_is_not_executed",
            "source_supplement_intake_execution_status_is_not_executed",
            "source_supplement_acceptance_execution_status_is_not_executed",
            "source_committee_reentry_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_acknowledgement_preview_is_dry_run_only",
            "acknowledgement_routing_precheck_preview_status_is_candidate_preview_with_hold",
            "all_routing_precheck_roles_covered",
            "all_routing_precheck_sections_covered",
            "all_routing_precheck_envelope_fields_covered",
            "all_routing_precheck_readiness_prerequisites_covered",
            "all_routing_precheck_decision_constraints_covered",
            "routing_eligibility_candidates_present",
            "reviewer_lane_candidates_present",
            "blocked_routing_reason_candidates_present",
            "response_due_window_snapshot_present",
            "candidate_routing_path_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_routing_precheck_preview_not_formal_routing_precheck",
            "assert_routing_precheck_not_executed",
            "assert_routing_not_executed",
            "assert_committee_reentry_not_executed",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved",
        },
        "routing_precheck_check",
    )

    refs = set(routing.get("requiredRoutingPrecheckRefs", []))
    require(len(refs) == expected["requiredRoutingPrecheckRefCount"], "required_routing_precheck_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceRepairRequestAcknowledgementPreviewRef",
            "sourceSupplementPrecheckRepairRequestPreviewRef",
            "routingPrecheckScopeRef",
            "routingPrecheckEnvelopeFieldsRef",
            "routingPrecheckReadinessPrerequisitesRef",
            "routingEligibilityCandidatesRef",
            "reviewerLaneCandidatesRef",
            "blockedRoutingReasonCandidatesRef",
            "responseDueWindowSnapshotRef",
            "candidateRoutingPathRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "requestOwnerRef",
            "acknowledgementOwnerRef",
            "routingOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "noWriteAttestationRef",
        },
        "required_routing_precheck_ref",
    )

    blocking_conditions = set(routing.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_acknowledgement_preview_not_candidate_preview_with_hold",
            "source_acknowledgement_already_executed",
            "source_repair_request_already_executed",
            "source_supplement_intake_already_executed",
            "source_supplement_material_already_accepted",
            "source_committee_reentry_already_executed",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_acknowledgement_preview_not_dry_run_only",
            "missing_source_acknowledgement_preview_ref",
            "missing_routing_precheck_scope_ref",
            "missing_routing_precheck_envelope_fields_ref",
            "missing_routing_eligibility_candidates_ref",
            "missing_reviewer_lane_candidates_ref",
            "missing_blocked_routing_reason_candidates_ref",
            "missing_response_due_window_snapshot_ref",
            "missing_candidate_routing_path_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_routing_precheck_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "routing_precheck_preview_attempts_formal_routing_precheck",
            "routing_precheck_preview_attempts_routing_execution",
            "routing_precheck_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    forbidden_actions = set(routing.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_routing_precheck",
            "execute_routing",
            "execute_acknowledgement",
            "issue_formal_acknowledgement",
            "execute_repair_request",
            "execute_supplement_intake",
            "accept_supplement_material",
            "execute_intake_acceptance",
            "submit_committee_case_packet",
            "submit_committee_review_input",
            "execute_committee_reentry",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "record_routing_precheck",
            "record_routing",
            "record_acknowledgement",
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
            "convert_routing_precheck_preview_to_formal_routing_precheck",
            "override_waes_gate",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    forbidden_outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(forbidden_outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")
    require_all(
        forbidden_outputs,
        {
            "routing_precheck_executed",
            "routing_executed",
            "acknowledgement_executed",
            "formal_acknowledgement_issued",
            "repair_request_executed",
            "supplement_intake_executed",
            "supplement_material_accepted",
            "intake_acceptance_executed",
            "committee_case_packet_submitted",
            "committee_review_input_submitted",
            "committee_reentry_executed",
            "committee_case_opened",
            "committee_decision_executed",
            "human_confirmation_executed",
            "freeze_released",
            "unfreeze_executed",
            "formal_write_executed",
            "formal_harness_evidence_record_written",
            "harness_evidence_record_written",
            "kds_write_enabled",
            "business_write_enabled",
            "revenue_distribution_written",
            "contribution_score_written",
            "accepted",
            "integrated",
            "production_ready",
            "waes_gate_overridden",
            "routing_precheck_preview_converted_to_formal_routing_precheck",
            "p1_admission_granted",
            "v1_upgrade_approved",
        },
        "forbidden_output",
    )

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_ack.get("holdContextRefs", []))
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

    require(evidence.get("current_acknowledgement_routing_precheck_preview_status") == "candidate_preview_with_hold", "evidence_routing_precheck_preview_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("package_scope", {}).get("routing_precheck_roles") == 10, "evidence_routing_precheck_role_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_repair_request_acknowledgement_preview_status") == "candidate_preview_with_hold", "evidence_source_acknowledgement_preview_status_mismatch")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_acknowledgement_routing_precheck_preview_current_state_d158=pass")
    print(f"acknowledgement_routing_precheck_preview_status={fixture.get('acknowledgementRoutingPrecheckPreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={routing.get('previewStatus')}")
    print(f"execution_status={routing.get('executionStatus')}")
    print(f"routing_precheck_execution_status={routing.get('routingPrecheckExecutionStatus')}")
    print(f"routing_execution_status={routing.get('routingExecutionStatus')}")
    print(f"acknowledgement_execution_status={routing.get('acknowledgementExecutionStatus')}")
    print(f"repair_request_execution_status={routing.get('repairRequestExecutionStatus')}")
    print(f"supplement_intake_execution_status={routing.get('supplementIntakeExecutionStatus')}")
    print(f"supplement_acceptance_execution_status={routing.get('supplementAcceptanceExecutionStatus')}")
    print(f"committee_reentry_execution_status={routing.get('committeeReentryExecutionStatus')}")
    print(f"committee_case_execution_status={routing.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={routing.get('committeeDecisionExecutionStatus')}")
    print(f"routing_precheck_roles={len(roles)}")
    print(f"routing_precheck_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
