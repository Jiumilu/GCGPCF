#!/usr/bin/env python3
"""Validate D164 GCKF P0 formal evidence execution reviewer acceptance acknowledgement routing package preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-reviewer-acceptance-acknowledgement-routing-package-preview-current-state-d164-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-reviewer-acceptance-acknowledgement-routing-package-preview-current-state-d164-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-reviewer-acceptance-acknowledgement-routing-package-preview-current-state-d164-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D164-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_reviewer_acceptance_acknowledgement_routing_package_preview_current_state_d164="
        f"fail reason={message}"
    )
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d164_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical = load_json(ROOT / fixture["sourceHistoricalReviewerAcceptanceAcknowledgementRoutingPackagePreview"])
    current_ack = load_json(ROOT / fixture["sourceCurrentReviewerAcceptanceAcknowledgementPreview"])
    package = fixture["reviewerAcceptanceAcknowledgementRoutingPackagePreview"]
    source_historical = historical["reviewerAcceptanceAcknowledgementRoutingPackagePreview"]
    source_ack = current_ack["reviewerAcceptanceAcknowledgementPreview"]

    require(
        fixture.get("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus")
        == expected["reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus"],
        "routing_package_preview_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalRoutingPackage") is expected["notFinalRoutingPackage"], "not_final_routing_package_mismatch")

    require(package.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(package.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    require(package.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    for key in (
        "routingPackageExecutionStatus",
        "reviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus",
        "routingReceiptExecutionStatus",
        "assignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus",
        "routingPrecheckExecutionStatus",
        "routingExecutionStatus",
        "acknowledgementExecutionStatus",
        "repairRequestExecutionStatus",
        "supplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus"
    ):
        require(package.get(key) == expected[key], f"{key}_mismatch")
    require(package.get("executionMode") == expected["executionMode"], "package_execution_mode_mismatch")
    require(package.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")
    require(
        package.get("sourceReviewerAcceptanceAcknowledgementPreviewId") == source_ack.get("id"),
        "source_reviewer_acceptance_acknowledgement_preview_id_mismatch",
    )

    require(
        historical.get("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus") == "candidate_preview",
        "historical_routing_package_preview_status_mismatch",
    )
    require(source_historical.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(source_historical.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_ack.get("reviewerAcceptanceAcknowledgementPreviewStatus")
        == expected["sourceReviewerAcceptanceAcknowledgementPreviewStatus"],
        "source_reviewer_acceptance_acknowledgement_preview_status_mismatch",
    )
    for source_key, expected_key in (
        ("reviewerAcceptanceAcknowledgementExecutionStatus", "sourceReviewerAcceptanceAcknowledgementExecutionStatus"),
        ("reviewerAcceptancePrecheckExecutionStatus", "sourceReviewerAcceptancePrecheckExecutionStatus"),
        ("reviewerAcceptanceExecutionStatus", "sourceReviewerAcceptanceExecutionStatus"),
        ("routingReceiptExecutionStatus", "sourceRoutingReceiptExecutionStatus"),
        ("assignmentAcknowledgementExecutionStatus", "sourceAssignmentAcknowledgementExecutionStatus"),
        ("reviewerNotificationExecutionStatus", "sourceReviewerNotificationExecutionStatus"),
        ("reviewerAssignmentExecutionStatus", "sourceReviewerAssignmentExecutionStatus"),
        ("routingPrecheckExecutionStatus", "sourceRoutingPrecheckExecutionStatus"),
        ("routingExecutionStatus", "sourceRoutingExecutionStatus"),
        ("acknowledgementExecutionStatus", "sourceAcknowledgementExecutionStatus"),
        ("repairRequestExecutionStatus", "sourceRepairRequestExecutionStatus"),
        ("supplementIntakeExecutionStatus", "sourceSupplementIntakeExecutionStatus"),
        ("supplementAcceptanceExecutionStatus", "sourceSupplementAcceptanceExecutionStatus"),
        ("committeeReentryExecutionStatus", "sourceCommitteeReentryExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_ack.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_ack.get("dryRunOnly") is True, "source_ack_preview_not_dry_run_only")
    require(
        fixture.get("coveredReviewerAcceptanceAcknowledgementPreviewStatus")
        == expected["coveredReviewerAcceptanceAcknowledgementPreviewStatus"],
        "covered_reviewer_acceptance_acknowledgement_preview_status_mismatch",
    )
    require(
        fixture["coveredReviewerAcceptanceAcknowledgementPreviewStatus"] == source_ack.get("previewStatus"),
        "covered_reviewer_acceptance_acknowledgement_preview_not_matched",
    )

    roles = set(package.get("routingPackageRoles", []))
    require(len(roles) == expected["routingPackageRoleCount"], "routing_package_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "acknowledgement_owner",
            "routing_owner",
            "reviewer_assignment_owner",
            "assignment_acknowledgement_owner",
            "routing_receipt_owner",
            "reviewer_acceptance_precheck_owner",
            "reviewer_acceptance_acknowledgement_owner",
            "routing_package_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
            "governance_owner"
        },
        "routing_package_role",
    )
    require(set(source_ack.get("reviewerAcceptanceAcknowledgementRoles", [])).issubset(roles), "routing_package_roles_not_covering_ack_roles")

    sections = set(package.get("routingPackageSections", []))
    require(len(sections) == expected["routingPackageSectionCount"], "routing_package_section_count_mismatch")
    require_all(
        sections,
        {
            "source_reviewer_acceptance_acknowledgement_lineage",
            "routing_package_scope",
            "routing_package_envelope_fields",
            "routing_package_readiness_prerequisites",
            "candidate_package_destination_matrix",
            "candidate_acknowledgement_to_package_mapping",
            "candidate_package_blocker_codes",
            "candidate_package_hold_conditions",
            "candidate_access_boundary_snapshot",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation"
        },
        "routing_package_section",
    )

    envelope_fields = set(package.get("routingPackageEnvelopeFields", []))
    require(len(envelope_fields) == expected["routingPackageEnvelopeFieldCount"], "routing_package_envelope_field_count_mismatch")
    require_all(
        envelope_fields,
        {
            "routing_package_preview_id",
            "source_reviewer_acceptance_acknowledgement_preview_id",
            "candidate_acceptance_acknowledgement_ref",
            "candidate_routing_package_ref",
            "candidate_package_destination_role",
            "candidate_package_blocker_code",
            "candidate_hold_condition_ref",
            "candidate_routing_package_status",
            "no_write_attestation_ref"
        },
        "routing_package_envelope_field",
    )

    prerequisites = set(package.get("routingPackageReadinessPrerequisites", []))
    require(len(prerequisites) == expected["routingPackageReadinessPrerequisiteCount"], "routing_package_readiness_prerequisite_count_mismatch")
    require_all(
        prerequisites,
        {
            "source_reviewer_acceptance_acknowledgement_candidate_preview_with_hold",
            "source_reviewer_acceptance_acknowledgement_not_formal_acknowledgement",
            "source_reviewer_acceptance_acknowledgement_not_executed",
            "source_reviewer_acceptance_not_executed",
            "source_reviewer_notification_not_executed",
            "source_routing_not_executed",
            "source_committee_case_not_opened",
            "routing_package_not_formal_evidence"
        },
        "routing_package_readiness_prerequisite",
    )

    decision_constraints = set(package.get("routingPackageDecisionConstraints", []))
    require(len(decision_constraints) == expected["routingPackageDecisionConstraintCount"], "routing_package_decision_constraint_count_mismatch")
    require_all(
        decision_constraints,
        {
            "candidate_preview_only",
            "routing_package_not_formal_package",
            "no_routing_package_execution",
            "no_routing_package_submission",
            "no_reviewer_acceptance_acknowledgement_execution",
            "no_reviewer_acceptance_precheck_execution",
            "no_reviewer_acceptance_execution",
            "no_routing_receipt_execution",
            "no_assignment_acknowledgement_execution",
            "no_reviewer_notification",
            "no_reviewer_assignment_execution",
            "no_routing_precheck_execution",
            "no_routing_execution",
            "no_acknowledgement_execution",
            "no_repair_request_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_human_confirmation",
            "no_harness_evidence_write"
        },
        "routing_package_decision_constraint",
    )

    checks = set(package.get("routingPackageChecks", []))
    require(len(checks) == expected["routingPackageCheckCount"], "routing_package_check_count_mismatch")
    require_all(
        checks,
        {
            "source_reviewer_acceptance_acknowledgement_status_is_candidate_preview_with_hold",
            "source_reviewer_acceptance_acknowledgement_execution_status_is_not_executed",
            "source_reviewer_acceptance_precheck_execution_status_is_not_executed",
            "source_reviewer_acceptance_execution_status_is_not_executed",
            "source_routing_receipt_execution_status_is_not_executed",
            "source_assignment_acknowledgement_execution_status_is_not_executed",
            "source_reviewer_notification_execution_status_is_not_executed",
            "source_reviewer_assignment_execution_status_is_not_executed",
            "source_routing_precheck_execution_status_is_not_executed",
            "source_routing_execution_status_is_not_executed",
            "source_acknowledgement_execution_status_is_not_executed",
            "source_repair_request_execution_status_is_not_executed",
            "source_supplement_intake_execution_status_is_not_executed",
            "source_supplement_acceptance_execution_status_is_not_executed",
            "source_committee_reentry_execution_status_is_not_executed",
            "source_committee_case_execution_status_is_not_executed",
            "source_committee_decision_execution_status_is_not_executed",
            "source_confirmation_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_reviewer_acceptance_acknowledgement_preview_is_dry_run_only",
            "routing_package_preview_status_is_candidate_preview_with_hold",
            "all_routing_package_roles_covered",
            "all_routing_package_sections_covered",
            "all_routing_package_envelope_fields_covered",
            "all_routing_package_readiness_prerequisites_covered",
            "all_routing_package_decision_constraints_covered",
            "candidate_package_destination_matrix_present",
            "candidate_acknowledgement_to_package_mapping_present",
            "candidate_package_blocker_codes_present",
            "candidate_package_hold_conditions_present",
            "candidate_access_boundary_snapshot_present",
            "authority_and_recusal_boundary_present",
            "freeze_retention_statement_present",
            "waes_negative_gate_snapshot_present",
            "harness_no_write_guard_present",
            "no_write_attestation_present",
            "preview_hold_context_refs",
            "assert_routing_package_not_formal_package",
            "assert_routing_package_not_executed",
            "assert_reviewer_acceptance_acknowledgement_not_executed",
            "assert_reviewer_acceptance_precheck_not_executed",
            "assert_reviewer_acceptance_not_executed",
            "assert_routing_receipt_not_executed",
            "assert_assignment_acknowledgement_not_executed",
            "assert_reviewer_notification_not_executed",
            "assert_reviewer_assignment_not_executed",
            "assert_committee_reentry_not_executed",
            "assert_committee_case_not_opened",
            "assert_no_write_boundary",
            "assert_p1_admission_not_granted",
            "assert_v1_upgrade_not_approved"
        },
        "routing_package_check",
    )

    refs = set(package.get("requiredRoutingPackageRefs", []))
    require(len(refs) == expected["requiredRoutingPackageRefCount"], "required_routing_package_ref_count_mismatch")
    require_all(
        refs,
        {
            "sourceReviewerAcceptanceAcknowledgementPreviewRef",
            "sourceRoutingReceiptReviewerAcceptancePrecheckPreviewRef",
            "routingPackageScopeRef",
            "routingPackageEnvelopeFieldsRef",
            "routingPackageReadinessPrerequisitesRef",
            "candidatePackageDestinationMatrixRef",
            "candidateAcknowledgementToPackageMappingRef",
            "candidatePackageBlockerCodesRef",
            "candidatePackageHoldConditionsRef",
            "candidateAccessBoundarySnapshotRef",
            "authorityAndRecusalBoundaryRef",
            "freezeRetentionStatementRef",
            "waesNegativeGateSnapshotRef",
            "harnessNoWriteGuardRef",
            "requestOwnerRef",
            "acknowledgementOwnerRef",
            "reviewerAcceptanceAcknowledgementOwnerRef",
            "routingPackageOwnerRef",
            "reviewerAcceptanceOwnerRef",
            "routingOwnerRef",
            "reviewerAssignmentOwnerRef",
            "assignmentAcknowledgementOwnerRef",
            "routingReceiptOwnerRef",
            "waesGateOwnerRef",
            "kweWorkflowOwnerRef",
            "harnessReviewerRef",
            "committeeRepresentativeRef",
            "stopAuthorityOwnerRef",
            "businessSystemOwnerRef",
            "governanceOwnerRef",
            "noWriteAttestationRef"
        },
        "required_routing_package_ref",
    )

    blocking_conditions = set(package.get("blockingConditions", []))
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require_all(
        blocking_conditions,
        {
            "source_reviewer_acceptance_acknowledgement_preview_not_candidate_preview_with_hold",
            "source_reviewer_acceptance_acknowledgement_already_executed",
            "source_reviewer_acceptance_precheck_already_executed",
            "source_reviewer_acceptance_already_executed",
            "source_routing_receipt_already_executed",
            "source_assignment_acknowledgement_already_executed",
            "source_reviewer_notification_already_executed",
            "source_reviewer_assignment_already_executed",
            "source_routing_precheck_already_executed",
            "source_routing_already_executed",
            "source_acknowledgement_already_executed",
            "source_repair_request_already_executed",
            "source_supplement_intake_already_executed",
            "source_supplement_material_already_accepted",
            "source_committee_reentry_already_executed",
            "source_committee_case_already_opened",
            "source_committee_decision_already_executed",
            "source_confirmation_already_executed",
            "source_unfreeze_already_executed",
            "source_reviewer_acceptance_acknowledgement_preview_not_dry_run_only",
            "missing_source_reviewer_acceptance_acknowledgement_preview_ref",
            "missing_routing_package_scope_ref",
            "missing_routing_package_envelope_fields_ref",
            "missing_routing_package_readiness_prerequisites_ref",
            "missing_candidate_package_destination_matrix_ref",
            "missing_candidate_acknowledgement_to_package_mapping_ref",
            "missing_candidate_package_blocker_codes_ref",
            "missing_candidate_package_hold_conditions_ref",
            "missing_candidate_access_boundary_snapshot_ref",
            "missing_authority_and_recusal_boundary_ref",
            "missing_freeze_retention_statement_ref",
            "missing_waes_negative_gate_snapshot_ref",
            "missing_harness_no_write_guard_ref",
            "missing_required_routing_package_role",
            "missing_no_write_attestation_ref",
            "missing_hold_context_refs",
            "routing_package_preview_attempts_formal_package",
            "routing_package_preview_attempts_package_submission",
            "routing_package_preview_attempts_reviewer_acceptance_acknowledgement_execution",
            "routing_package_preview_attempts_reviewer_acceptance_execution",
            "routing_package_preview_attempts_routing_execution",
            "routing_package_preview_attempts_committee_reentry",
            "routing_package_preview_attempts_committee_case_opening",
            "routing_package_preview_attempts_harness_evidence_write"
        },
        "blocking_condition",
    )

    forbidden_actions = set(package.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require_all(
        forbidden_actions,
        {
            "execute_routing_package",
            "submit_routing_package",
            "execute_reviewer_acceptance_acknowledgement",
            "execute_reviewer_acceptance_precheck",
            "accept_reviewer",
            "execute_routing_receipt",
            "execute_assignment_acknowledgement",
            "notify_reviewer",
            "execute_reviewer_assignment",
            "execute_routing_precheck",
            "execute_routing",
            "execute_acknowledgement",
            "execute_repair_request",
            "execute_supplement_intake",
            "accept_supplement_material",
            "execute_intake_acceptance",
            "issue_formal_routing_package",
            "issue_formal_reviewer_acceptance_acknowledgement",
            "issue_formal_reviewer_acceptance",
            "issue_formal_routing_receipt",
            "issue_formal_acknowledgement",
            "execute_committee_reentry",
            "open_committee_case",
            "execute_committee_decision",
            "execute_human_confirmation",
            "execute_freeze_release",
            "execute_unfreeze",
            "record_routing_package",
            "record_reviewer_acceptance_acknowledgement",
            "record_reviewer_acceptance_precheck",
            "record_reviewer_acceptance",
            "record_routing_receipt",
            "record_assignment_acknowledgement",
            "record_reviewer_notification",
            "record_reviewer_assignment",
            "record_routing_precheck",
            "record_routing",
            "record_acknowledgement",
            "record_repair_request",
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
            "convert_routing_package_preview_to_formal_package",
            "override_waes_gate",
            "grant_p1_admission",
            "approve_v1_upgrade"
        },
        "forbidden_action",
    )

    forbidden_outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(forbidden_outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")
    require_all(
        forbidden_outputs,
        {
            "routing_package_executed",
            "routing_package_submitted",
            "reviewer_acceptance_acknowledgement_executed",
            "reviewer_acceptance_precheck_executed",
            "reviewer_accepted",
            "routing_receipt_executed",
            "assignment_acknowledgement_executed",
            "reviewer_notified",
            "reviewer_assignment_executed",
            "routing_precheck_executed",
            "routing_executed",
            "acknowledgement_executed",
            "repair_request_executed",
            "supplement_intake_executed",
            "supplement_material_accepted",
            "intake_acceptance_executed",
            "formal_routing_package_issued",
            "formal_reviewer_acceptance_acknowledgement_issued",
            "formal_reviewer_acceptance_issued",
            "formal_routing_receipt_issued",
            "formal_acknowledgement_issued",
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
            "routing_package_preview_converted_to_formal_package",
            "p1_admission_granted",
            "v1_upgrade_approved"
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
        "v1UpgradeRecommended"
    ]:
        require(fixture["currentGateAssertions"].get(key) is False, f"current_gate_assertion_not_false:{key}")

    require(len(fixture.get("requiredSourceRefs", [])) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")

    require(
        evidence.get("current_reviewer_acceptance_acknowledgement_routing_package_preview_status")
        == "candidate_preview_with_hold",
        "evidence_routing_package_preview_status_mismatch",
    )
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(
        evidence.get("package_scope", {}).get("routing_package_roles") == 16,
        "evidence_routing_package_role_count_mismatch",
    )
    require(
        evidence.get("hold_context", {}).get("source_reviewer_acceptance_acknowledgement_preview_status")
        == "candidate_preview_with_hold",
        "evidence_source_ack_preview_status_mismatch",
    )

    localization = json.loads(
        run_command(
            "python3",
            "tools/kds-sync/check_chinese_localization_gate.py",
            "--json",
            "--max-findings",
            "10000",
        )
    )
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_formal_evidence_execution_reviewer_acceptance_acknowledgement_routing_package_preview_current_state_d164=pass")
    print(f"reviewer_acceptance_acknowledgement_routing_package_preview_status={fixture.get('reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"preview_status={package.get('previewStatus')}")
    print(f"execution_status={package.get('executionStatus')}")
    print(f"routing_package_execution_status={package.get('routingPackageExecutionStatus')}")
    print(f"reviewer_acceptance_acknowledgement_execution_status={package.get('reviewerAcceptanceAcknowledgementExecutionStatus')}")
    print(f"reviewer_acceptance_precheck_execution_status={package.get('reviewerAcceptancePrecheckExecutionStatus')}")
    print(f"reviewer_acceptance_execution_status={package.get('reviewerAcceptanceExecutionStatus')}")
    print(f"routing_receipt_execution_status={package.get('routingReceiptExecutionStatus')}")
    print(f"assignment_acknowledgement_execution_status={package.get('assignmentAcknowledgementExecutionStatus')}")
    print(f"reviewer_assignment_execution_status={package.get('reviewerAssignmentExecutionStatus')}")
    print(f"routing_precheck_execution_status={package.get('routingPrecheckExecutionStatus')}")
    print(f"routing_execution_status={package.get('routingExecutionStatus')}")
    print(f"acknowledgement_execution_status={package.get('acknowledgementExecutionStatus')}")
    print(f"repair_request_execution_status={package.get('repairRequestExecutionStatus')}")
    print(f"supplement_intake_execution_status={package.get('supplementIntakeExecutionStatus')}")
    print(f"supplement_acceptance_execution_status={package.get('supplementAcceptanceExecutionStatus')}")
    print(f"committee_reentry_execution_status={package.get('committeeReentryExecutionStatus')}")
    print(f"committee_case_execution_status={package.get('committeeCaseExecutionStatus')}")
    print(f"committee_decision_execution_status={package.get('committeeDecisionExecutionStatus')}")
    print(f"routing_package_roles={len(roles)}")
    print(f"routing_package_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
