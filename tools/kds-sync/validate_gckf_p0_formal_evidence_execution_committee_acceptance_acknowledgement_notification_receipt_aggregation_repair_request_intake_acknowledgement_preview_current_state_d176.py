#!/usr/bin/env python3
"""Validate D176 GCKF P0 repair request intake acknowledgement preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-intake-acknowledgement-preview-current-state-d176-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-intake-acknowledgement-preview-current-state-d176-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-intake-acknowledgement-preview-current-state-d176-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D176-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_intake_acknowledgement_preview_current_state_d176="
        f"fail reason={message}"
    )
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_all(actual: set[str], expected_values: set[str], label: str) -> None:
    for value in expected_values:
        require(value in actual, f"missing_{label}:{value}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    expected = fixture["expectedSummary"]
    historical = load_json(ROOT / fixture["sourceHistoricalRepairRequestIntakeAcknowledgementPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentRepairRequestCompletenessPrecheck"])
    acknowledgement = fixture["repairRequestIntakeAcknowledgementPreview"]
    historical_ack = historical["repairRequestIntakeAcknowledgementPreview"]
    source_precheck = current_source["repairRequestCompletenessPrecheck"]

    require(
        fixture.get("repairRequestIntakeAcknowledgementPreviewStatus") == expected["repairRequestIntakeAcknowledgementPreviewStatus"],
        "acknowledgement_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalRepairRequestIntakeAcknowledgement") is expected["notFinalRepairRequestIntakeAcknowledgement"],
        "not_final_acknowledgement_mismatch",
    )
    require(acknowledgement.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(acknowledgement.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "intakeAcknowledgementPreviewExecutionStatus",
        "intakeAcknowledgementExecutionStatus",
        "repairRequestCompletenessPrecheckPreviewExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus",
        "repairIntakePreviewExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "aggregationCompletenessPrecheckExecutionStatus",
        "notificationReceiptAggregationExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        require(acknowledgement.get(key) == "not_executed", f"{key}_mismatch")

    require(acknowledgement.get("executionMode") == expected["executionMode"], "acknowledgement_execution_mode_mismatch")
    require(acknowledgement.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("repairRequestIntakeAcknowledgementPreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_ack.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_ack.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("repairRequestCompletenessPrecheckStatus") == expected["sourceRepairRequestCompletenessPrecheckStatus"],
        "source_precheck_status_mismatch",
    )
    for source_key, expected_key in (
        ("repairRequestCompletenessPrecheckPreviewExecutionStatus", "sourceRepairRequestCompletenessPrecheckPreviewExecutionStatus"),
        ("repairRequestCompletenessPrecheckExecutionStatus", "sourceRepairRequestCompletenessPrecheckExecutionStatus"),
        ("repairIntakePreviewExecutionStatus", "sourceRepairIntakePreviewExecutionStatus"),
        ("repairIntakeExecutionStatus", "sourceRepairIntakeExecutionStatus"),
        ("repairRequestCreationStatus", "sourceRepairRequestCreationStatus"),
        ("aggregationCompletenessPrecheckExecutionStatus", "sourceAggregationCompletenessPrecheckExecutionStatus"),
        ("notificationReceiptAggregationExecutionStatus", "sourceNotificationReceiptAggregationExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_precheck.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_precheck.get("dryRunOnly") is True, "source_precheck_not_dry_run_only")
    require(
        acknowledgement.get("sourceRepairRequestCompletenessPrecheckId") == source_precheck.get("id"),
        "source_precheck_id_mismatch",
    )
    require(
        fixture.get("coveredRepairRequestCompletenessPrecheckStatus") == expected["coveredRepairRequestCompletenessPrecheckStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredRepairRequestCompletenessPrecheckStatus"] == source_precheck.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(acknowledgement.get("acknowledgementRoles", []))
    sections = set(acknowledgement.get("acknowledgementSections", []))
    fields = set(acknowledgement.get("candidateAcknowledgementFields", []))
    prerequisites = set(acknowledgement.get("acknowledgementReadinessPrerequisites", []))
    constraints = set(acknowledgement.get("acknowledgementDecisionConstraints", []))
    checks = set(acknowledgement.get("acknowledgementChecks", []))
    refs = set(acknowledgement.get("requiredAcknowledgementRefs", []))
    blocking_conditions = set(acknowledgement.get("blockingConditions", []))
    forbidden_actions = set(acknowledgement.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["acknowledgementRoleCount"], "acknowledgement_role_count_mismatch")
    require(len(sections) == expected["acknowledgementSectionCount"], "acknowledgement_section_count_mismatch")
    require(len(fields) == expected["candidateAcknowledgementFieldCount"], "candidate_acknowledgement_field_count_mismatch")
    require(len(prerequisites) == expected["acknowledgementReadinessPrerequisiteCount"], "acknowledgement_prerequisite_count_mismatch")
    require(len(constraints) == expected["acknowledgementDecisionConstraintCount"], "acknowledgement_constraint_count_mismatch")
    require(len(checks) == expected["acknowledgementCheckCount"], "acknowledgement_check_count_mismatch")
    require(len(refs) == expected["requiredAcknowledgementRefCount"], "required_acknowledgement_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "repair_intake_owner",
            "acknowledgement_owner",
            "precheck_owner",
            "aggregation_owner",
            "committee_secretariat",
            "waes_gate_owner",
            "harness_reviewer",
            "acl_owner"
        },
        "acknowledgement_role",
    )
    require_all(
        sections,
        {
            "candidate_receipt_acknowledgement_summary",
            "candidate_precheck_result_snapshot",
            "candidate_missing_material_gap_snapshot",
            "candidate_submitter_notification_boundary",
            "candidate_acl_visibility_boundary",
            "candidate_next_action_hint",
            "candidate_hold_reason_snapshot",
            "candidate_hold_context_refs_snapshot",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation"
        },
        "acknowledgement_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_with_hold_only",
            "acknowledgement_not_formal_acceptance",
            "no_intake_acknowledgement_preview_execution",
            "no_intake_acknowledgement_execution",
            "no_repair_request_completeness_precheck_execution",
            "no_repair_intake_execution",
            "no_repair_request_creation",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write"
        },
        "acknowledgement_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_intake_acknowledgement",
            "execute_repair_request_completeness_precheck",
            "execute_repair_intake",
            "create_repair_request",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system"
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    package_scope = evidence.get("package_scope", {})
    require(
        evidence.get("current_repair_request_intake_acknowledgement_preview_status") == expected["repairRequestIntakeAcknowledgementPreviewStatus"],
        "evidence_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(evidence.get("execution_mode") == "local_evidence_no_write", "evidence_execution_mode_mismatch")
    require(evidence.get("execution_status") == "not_executed", "evidence_execution_status_mismatch")
    require(package_scope.get("acknowledgement_roles") == expected["acknowledgementRoleCount"], "evidence_acknowledgement_roles_mismatch")
    require(package_scope.get("acknowledgement_sections") == expected["acknowledgementSectionCount"], "evidence_acknowledgement_sections_mismatch")
    require(package_scope.get("candidate_acknowledgement_fields") == expected["candidateAcknowledgementFieldCount"], "evidence_candidate_acknowledgement_fields_mismatch")
    require(package_scope.get("acknowledgement_readiness_prerequisites") == expected["acknowledgementReadinessPrerequisiteCount"], "evidence_prerequisites_mismatch")
    require(package_scope.get("acknowledgement_decision_constraints") == expected["acknowledgementDecisionConstraintCount"], "evidence_constraints_mismatch")
    require(package_scope.get("acknowledgement_checks") == expected["acknowledgementCheckCount"], "evidence_checks_mismatch")
    require(package_scope.get("required_acknowledgement_refs") == expected["requiredAcknowledgementRefCount"], "evidence_required_refs_mismatch")
    require(package_scope.get("blocking_conditions") == expected["blockingConditionCount"], "evidence_blocking_conditions_mismatch")
    require(package_scope.get("forbidden_actions") == expected["forbiddenActionCount"], "evidence_forbidden_actions_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_context_refs_mismatch")

    gate_assertions = evidence.get("gateAssertions", {})
    for key in (
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ):
        require(gate_assertions.get(key) is False, f"gate_assertion_not_false:{key}")

    evidence_md = EVIDENCE_MD.read_text(encoding="utf-8")
    loop_md = LOOP_MD.read_text(encoding="utf-8")
    require("candidate_preview_with_hold" in evidence_md, "evidence_md_missing_hold_status")
    require("review_ready_with_hold" in evidence_md, "evidence_md_missing_maximum_state")
    require("Hold 上下文" in evidence_md, "evidence_md_missing_hold_section")
    require("candidate_preview_with_hold" in loop_md, "loop_md_missing_hold_status")
    require("继续保持 no-write" in loop_md, "loop_md_missing_next_round_guidance")

    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_intake_acknowledgement_preview_current_state_d176=pass"
    )
    print(f"repair_request_intake_acknowledgement_preview_status={fixture['repairRequestIntakeAcknowledgementPreviewStatus']}")
    print(f"maximum_state={fixture['maximumState']}")
    print(f"preview_status={acknowledgement['previewStatus']}")
    print(f"execution_status={acknowledgement['executionStatus']}")
    print(f"acknowledgement_roles={len(roles)}")
    print(f"acknowledgement_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
