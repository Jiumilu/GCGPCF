#!/usr/bin/env python3
"""Validate D178 GCKF P0 routing delivery precheck current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-delivery-precheck-current-state-d178-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-delivery-precheck-current-state-d178-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-delivery-precheck-current-state-d178-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D178-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_delivery_precheck_current_state_d178="
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
    historical = load_json(ROOT / fixture["sourceHistoricalRoutingDeliveryPrecheck"])
    current_source = load_json(ROOT / fixture["sourceCurrentRepairRequestAcknowledgementRoutingPreview"])
    precheck = fixture["routingDeliveryPrecheck"]
    historical_precheck = historical["routingDeliveryPrecheck"]
    source_routing = current_source["repairRequestAcknowledgementRoutingPreview"]

    require(
        fixture.get("routingDeliveryPrecheckStatus") == expected["routingDeliveryPrecheckStatus"],
        "precheck_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalRoutingDelivery") is expected["notFinalRoutingDelivery"],
        "not_final_delivery_mismatch",
    )
    require(precheck.get("precheckType") == expected["precheckType"], "precheck_type_mismatch")
    require(precheck.get("precheckStatus") == expected["precheckStatus"], "precheck_preview_status_mismatch")

    for key in (
        "executionStatus",
        "routingDeliveryPrecheckExecutionStatus",
        "deliveryExecutionStatus",
        "recipientNotificationExecutionStatus",
        "recipientAcknowledgementExecutionStatus",
        "repairOwnerNotificationExecutionStatus",
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
        require(precheck.get(key) == "not_executed", f"{key}_mismatch")

    require(precheck.get("executionMode") == expected["executionMode"], "precheck_execution_mode_mismatch")
    require(precheck.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("routingDeliveryPrecheckStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_precheck.get("precheckStatus") == "candidate_preview", "historical_precheck_status_mismatch")
    require(historical_precheck.get("deliveryExecutionStatus") == "not_executed", "historical_delivery_status_mismatch")

    require(
        current_source.get("repairRequestAcknowledgementRoutingPreviewStatus")
        == expected["sourceRepairRequestAcknowledgementRoutingPreviewStatus"],
        "source_routing_status_mismatch",
    )
    for source_key, expected_key in (
        ("acknowledgementRoutingPreviewExecutionStatus", "sourceAcknowledgementRoutingPreviewExecutionStatus"),
        ("acknowledgementRoutingExecutionStatus", "sourceAcknowledgementRoutingExecutionStatus"),
        ("intakeAcknowledgementExecutionStatus", "sourceIntakeAcknowledgementExecutionStatus"),
        ("repairRequestCompletenessPrecheckPreviewExecutionStatus", "sourceRepairRequestCompletenessPrecheckPreviewExecutionStatus"),
        ("repairRequestCompletenessPrecheckExecutionStatus", "sourceRepairRequestCompletenessPrecheckExecutionStatus"),
        ("repairIntakePreviewExecutionStatus", "sourceRepairIntakePreviewExecutionStatus"),
        ("repairIntakeExecutionStatus", "sourceRepairIntakeExecutionStatus"),
        ("repairRequestCreationStatus", "sourceRepairRequestCreationStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus")
    ):
        require(source_routing.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_routing.get("dryRunOnly") is True, "source_routing_not_dry_run_only")
    require(
        precheck.get("sourceRepairRequestAcknowledgementRoutingPreviewId") == source_routing.get("id"),
        "source_routing_preview_id_mismatch",
    )
    require(
        fixture.get("coveredRepairRequestAcknowledgementRoutingPreviewStatus")
        == expected["coveredRepairRequestAcknowledgementRoutingPreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredRepairRequestAcknowledgementRoutingPreviewStatus"] == source_routing.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(precheck.get("deliveryPrecheckRoles", []))
    sections = set(precheck.get("deliveryPrecheckSections", []))
    fields = set(precheck.get("candidateDeliveryFields", []))
    prerequisites = set(precheck.get("deliveryReadinessPrerequisites", []))
    constraints = set(precheck.get("deliveryDecisionConstraints", []))
    checks = set(precheck.get("deliveryPrecheckChecks", []))
    refs = set(precheck.get("requiredDeliveryRefs", []))
    blocking_conditions = set(precheck.get("blockingConditions", []))
    forbidden_actions = set(precheck.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["deliveryPrecheckRoleCount"], "delivery_precheck_role_count_mismatch")
    require(len(sections) == expected["deliveryPrecheckSectionCount"], "delivery_precheck_section_count_mismatch")
    require(len(fields) == expected["candidateDeliveryFieldCount"], "candidate_delivery_field_count_mismatch")
    require(len(prerequisites) == expected["deliveryReadinessPrerequisiteCount"], "delivery_prerequisite_count_mismatch")
    require(len(constraints) == expected["deliveryDecisionConstraintCount"], "delivery_constraint_count_mismatch")
    require(len(checks) == expected["deliveryPrecheckCheckCount"], "delivery_check_count_mismatch")
    require(len(refs) == expected["requiredDeliveryRefCount"], "required_delivery_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
          "routing_owner",
          "delivery_owner",
          "recipient_acl_owner",
          "repair_owner",
          "sla_owner",
          "waes_gate_owner",
          "harness_reviewer",
          "governance_owner",
          "audit_owner"
        },
        "delivery_role",
    )
    require_all(
        sections,
        {
          "candidate_delivery_channel_matrix",
          "candidate_recipient_matrix",
          "candidate_acl_redaction_boundary",
          "candidate_repair_owner_notification_hint",
          "candidate_sla_window_hint",
          "candidate_delivery_blocker_codes",
          "candidate_hold_reason_snapshot",
          "candidate_hold_context_refs_snapshot",
          "waes_negative_gate_snapshot",
          "harness_no_write_guard",
          "no_delivery_attestation",
          "no_write_attestation"
        },
        "delivery_section",
    )
    require_all(
        constraints,
        {
          "candidate_preview_with_hold_only",
          "delivery_precheck_not_formal_delivery",
          "no_routing_delivery_precheck_execution",
          "no_routing_delivery_execution",
          "no_recipient_notification_execution",
          "no_recipient_acknowledgement_execution",
          "no_repair_owner_notification_execution",
          "no_acknowledgement_routing_execution",
          "no_repair_request_creation",
          "no_committee_case_opening",
          "no_harness_evidence_write",
          "no_business_write"
        },
        "delivery_constraint",
    )
    require_all(
        forbidden_actions,
        {
          "execute_routing_delivery_precheck",
          "execute_routing_delivery",
          "send_recipient_notification",
          "execute_recipient_acknowledgement",
          "send_repair_owner_notification",
          "execute_acknowledgement_routing",
          "execute_intake_acknowledgement",
          "create_repair_request",
          "write_harness_evidence",
          "write_kds",
          "write_business_system"
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    require(
        evidence.get("current_routing_delivery_precheck_status") == expected["routingDeliveryPrecheckStatus"],
        "evidence_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(evidence.get("execution_mode") == "local_evidence_no_write", "evidence_execution_mode_mismatch")
    require(evidence.get("execution_status") == "not_executed", "evidence_execution_status_mismatch")

    package_scope = evidence.get("package_scope", {})
    require(package_scope.get("delivery_precheck_roles") == expected["deliveryPrecheckRoleCount"], "evidence_roles_mismatch")
    require(package_scope.get("delivery_precheck_sections") == expected["deliveryPrecheckSectionCount"], "evidence_sections_mismatch")
    require(package_scope.get("candidate_delivery_fields") == expected["candidateDeliveryFieldCount"], "evidence_fields_mismatch")
    require(package_scope.get("delivery_readiness_prerequisites") == expected["deliveryReadinessPrerequisiteCount"], "evidence_prerequisites_mismatch")
    require(package_scope.get("delivery_decision_constraints") == expected["deliveryDecisionConstraintCount"], "evidence_constraints_mismatch")
    require(package_scope.get("delivery_precheck_checks") == expected["deliveryPrecheckCheckCount"], "evidence_checks_mismatch")
    require(package_scope.get("required_delivery_refs") == expected["requiredDeliveryRefCount"], "evidence_refs_mismatch")
    require(package_scope.get("blocking_conditions") == expected["blockingConditionCount"], "evidence_blocks_mismatch")
    require(package_scope.get("forbidden_actions") == expected["forbiddenActionCount"], "evidence_forbidden_actions_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_refs_mismatch")

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
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_delivery_precheck_current_state_d178=pass"
    )
    print(f"routing_delivery_precheck_status={fixture['routingDeliveryPrecheckStatus']}")
    print(f"maximum_state={fixture['maximumState']}")
    print(f"precheck_status={precheck['precheckStatus']}")
    print(f"execution_status={precheck['executionStatus']}")
    print(f"delivery_precheck_roles={len(roles)}")
    print(f"delivery_precheck_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
