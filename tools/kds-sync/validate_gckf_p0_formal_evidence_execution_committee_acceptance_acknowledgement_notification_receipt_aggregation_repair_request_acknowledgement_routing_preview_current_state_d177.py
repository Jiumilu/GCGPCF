#!/usr/bin/env python3
"""Validate D177 GCKF P0 repair request acknowledgement routing preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-preview-current-state-d177-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-preview-current-state-d177-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-preview-current-state-d177-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D177-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_preview_current_state_d177="
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
    historical = load_json(ROOT / fixture["sourceHistoricalRepairRequestAcknowledgementRoutingPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentRepairRequestIntakeAcknowledgementPreview"])
    routing = fixture["repairRequestAcknowledgementRoutingPreview"]
    historical_routing = historical["repairRequestAcknowledgementRoutingPreview"]
    source_ack = current_source["repairRequestIntakeAcknowledgementPreview"]

    require(
        fixture.get("repairRequestAcknowledgementRoutingPreviewStatus")
        == expected["repairRequestAcknowledgementRoutingPreviewStatus"],
        "routing_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalRepairRequestAcknowledgementRouting")
        is expected["notFinalRepairRequestAcknowledgementRouting"],
        "not_final_routing_mismatch",
    )
    require(routing.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(routing.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "acknowledgementRoutingPreviewExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "intakeAcknowledgementExecutionStatus",
        "repairRequestCompletenessPrecheckPreviewExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus",
        "repairIntakePreviewExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        require(routing.get(key) == "not_executed", f"{key}_mismatch")

    require(routing.get("executionMode") == expected["executionMode"], "routing_execution_mode_mismatch")
    require(routing.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("repairRequestAcknowledgementRoutingPreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_routing.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_routing.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("repairRequestIntakeAcknowledgementPreviewStatus")
        == expected["sourceRepairRequestIntakeAcknowledgementPreviewStatus"],
        "source_ack_status_mismatch",
    )
    for source_key, expected_key in (
        ("intakeAcknowledgementPreviewExecutionStatus", "sourceIntakeAcknowledgementPreviewExecutionStatus"),
        ("intakeAcknowledgementExecutionStatus", "sourceIntakeAcknowledgementExecutionStatus"),
        ("repairRequestCompletenessPrecheckPreviewExecutionStatus", "sourceRepairRequestCompletenessPrecheckPreviewExecutionStatus"),
        ("repairRequestCompletenessPrecheckExecutionStatus", "sourceRepairRequestCompletenessPrecheckExecutionStatus"),
        ("repairIntakePreviewExecutionStatus", "sourceRepairIntakePreviewExecutionStatus"),
        ("repairIntakeExecutionStatus", "sourceRepairIntakeExecutionStatus"),
        ("repairRequestCreationStatus", "sourceRepairRequestCreationStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_ack.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_ack.get("dryRunOnly") is True, "source_ack_not_dry_run_only")
    require(
        routing.get("sourceRepairRequestIntakeAcknowledgementPreviewId") == source_ack.get("id"),
        "source_ack_id_mismatch",
    )
    require(
        fixture.get("coveredRepairRequestIntakeAcknowledgementPreviewStatus")
        == expected["coveredRepairRequestIntakeAcknowledgementPreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredRepairRequestIntakeAcknowledgementPreviewStatus"] == source_ack.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(routing.get("routingRoles", []))
    sections = set(routing.get("routingSections", []))
    fields = set(routing.get("candidateRoutingFields", []))
    prerequisites = set(routing.get("routingReadinessPrerequisites", []))
    constraints = set(routing.get("routingDecisionConstraints", []))
    checks = set(routing.get("routingChecks", []))
    refs = set(routing.get("requiredRoutingRefs", []))
    blocking_conditions = set(routing.get("blockingConditions", []))
    forbidden_actions = set(routing.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["routingRoleCount"], "routing_role_count_mismatch")
    require(len(sections) == expected["routingSectionCount"], "routing_section_count_mismatch")
    require(len(fields) == expected["candidateRoutingFieldCount"], "candidate_routing_field_count_mismatch")
    require(len(prerequisites) == expected["routingReadinessPrerequisiteCount"], "routing_prerequisite_count_mismatch")
    require(len(constraints) == expected["routingDecisionConstraintCount"], "routing_constraint_count_mismatch")
    require(len(checks) == expected["routingCheckCount"], "routing_check_count_mismatch")
    require(len(refs) == expected["requiredRoutingRefCount"], "required_routing_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "repair_intake_owner",
            "acknowledgement_owner",
            "routing_owner",
            "precheck_owner",
            "aggregation_owner",
            "committee_secretariat",
            "waes_gate_owner",
            "harness_reviewer",
            "acl_owner",
        },
        "routing_role",
    )
    require_all(
        sections,
        {
            "candidate_route_target_matrix",
            "candidate_routing_step_matrix",
            "candidate_recipient_acl_boundary",
            "candidate_repair_owner_hint",
            "candidate_sla_hint",
            "candidate_hold_reason_snapshot",
            "candidate_hold_context_refs_snapshot",
            "candidate_routing_blocker_codes",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "routing_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_with_hold_only",
            "routing_not_formal_acceptance",
            "no_acknowledgement_routing_preview_execution",
            "no_acknowledgement_routing_execution",
            "no_intake_acknowledgement_execution",
            "no_repair_request_completeness_precheck_execution",
            "no_repair_intake_execution",
            "no_repair_request_creation",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "routing_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_acknowledgement_routing_preview",
            "execute_acknowledgement_routing",
            "execute_intake_acknowledgement",
            "execute_repair_request_completeness_precheck",
            "execute_repair_intake",
            "create_repair_request",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    require(
        evidence.get("current_repair_request_acknowledgement_routing_preview_status")
        == expected["repairRequestAcknowledgementRoutingPreviewStatus"],
        "evidence_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(evidence.get("execution_mode") == "local_evidence_no_write", "evidence_execution_mode_mismatch")
    require(evidence.get("execution_status") == "not_executed", "evidence_execution_status_mismatch")

    package_scope = evidence.get("package_scope", {})
    require(package_scope.get("routing_roles") == expected["routingRoleCount"], "evidence_routing_roles_mismatch")
    require(package_scope.get("routing_sections") == expected["routingSectionCount"], "evidence_routing_sections_mismatch")
    require(package_scope.get("candidate_routing_fields") == expected["candidateRoutingFieldCount"], "evidence_candidate_routing_fields_mismatch")
    require(package_scope.get("routing_readiness_prerequisites") == expected["routingReadinessPrerequisiteCount"], "evidence_prerequisites_mismatch")
    require(package_scope.get("routing_decision_constraints") == expected["routingDecisionConstraintCount"], "evidence_constraints_mismatch")
    require(package_scope.get("routing_checks") == expected["routingCheckCount"], "evidence_checks_mismatch")
    require(package_scope.get("required_routing_refs") == expected["requiredRoutingRefCount"], "evidence_required_refs_mismatch")
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
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_preview_current_state_d177=pass"
    )
    print(f"repair_request_acknowledgement_routing_preview_status={fixture['repairRequestAcknowledgementRoutingPreviewStatus']}")
    print(f"maximum_state={fixture['maximumState']}")
    print(f"preview_status={routing['previewStatus']}")
    print(f"execution_status={routing['executionStatus']}")
    print(f"routing_roles={len(roles)}")
    print(f"routing_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
