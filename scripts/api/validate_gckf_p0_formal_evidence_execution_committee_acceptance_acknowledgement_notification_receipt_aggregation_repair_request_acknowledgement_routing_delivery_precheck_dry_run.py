#!/usr/bin/env python3
"""Validate P0 repair request acknowledgement routing delivery precheck dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-aggregation-repair-request-acknowledgement-routing-delivery-precheck-dry-run-v0.1.json"
)


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require_all(actual: set[str], expected_values: set[str], label: str, failures: list[str]) -> None:
    for value in expected_values:
        if value not in actual:
            failures.append(f"missing {label}: {value}")


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    source_data = load_json(data["sourceAcknowledgementRoutingPreview"])
    source = source_data["repairRequestAcknowledgementRoutingPreview"]
    precheck = data["routingDeliveryPrecheck"]
    failures: list[str] = []

    if data.get("routingDeliveryPrecheckStatus") != expected["routingDeliveryPrecheckStatus"]:
        failures.append("routingDeliveryPrecheckStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRoutingDelivery") is not expected["notFinalRoutingDelivery"]:
        failures.append("routing delivery must state notFinalRoutingDelivery=true")
    if precheck.get("precheckType") != expected["precheckType"]:
        failures.append("routing delivery precheckType mismatch")
    if precheck.get("precheckStatus") != expected["precheckStatus"]:
        failures.append("routing delivery precheckStatus must remain candidate_preview")
    if precheck.get("executionMode") != expected["executionMode"]:
        failures.append("routing delivery precheck executionMode mismatch")
    if precheck.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("routing delivery precheck must remain dryRunOnly=true")

    for key in (
        "deliveryExecutionStatus",
        "recipientNotificationExecutionStatus",
        "recipientAcknowledgementExecutionStatus",
        "repairOwnerNotificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "intakeAcknowledgementExecutionStatus",
        "repairRequestCompletenessPrecheckExecutionStatus",
        "repairIntakeExecutionStatus",
        "repairRequestCreationStatus",
        "committeeCaseExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if precheck.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("repairRequestAcknowledgementRoutingPreviewStatus") != expected["sourceAcknowledgementRoutingPreviewStatus"]:
        failures.append("source acknowledgement routing preview must remain candidate_preview")
    source_status_map = {
        "acknowledgementRoutingPreviewExecutionStatus": "sourceAcknowledgementRoutingPreviewExecutionStatus",
        "acknowledgementRoutingExecutionStatus": "sourceAcknowledgementRoutingExecutionStatus",
        "intakeAcknowledgementExecutionStatus": "sourceIntakeAcknowledgementExecutionStatus",
        "repairRequestCreationStatus": "sourceRepairRequestCreationStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source acknowledgement routing preview must remain dryRunOnly=true")
    if precheck.get("sourceAcknowledgementRoutingPreviewId") != source.get("id"):
        failures.append("sourceAcknowledgementRoutingPreviewId must match D77 routing preview id")
    if data.get("coveredAcknowledgementRoutingPreviewStatus") != source.get("previewStatus"):
        failures.append("covered acknowledgement routing preview status must match D77 status")

    count_checks = {
        "deliveryPrecheckRoles": "deliveryPrecheckRoleCount",
        "deliveryPrecheckSections": "deliveryPrecheckSectionCount",
        "candidateDeliveryFields": "candidateDeliveryFieldCount",
        "deliveryReadinessPrerequisites": "deliveryReadinessPrerequisiteCount",
        "deliveryDecisionConstraints": "deliveryDecisionConstraintCount",
        "deliveryPrecheckChecks": "deliveryPrecheckCheckCount",
        "requiredDeliveryRefs": "requiredDeliveryRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(precheck.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(precheck.get("deliveryPrecheckSections", [])),
        {
            "candidate_delivery_channel_matrix",
            "candidate_recipient_matrix",
            "candidate_acl_redaction_boundary",
            "candidate_repair_owner_notification_hint",
            "candidate_sla_window_hint",
            "candidate_delivery_blocker_codes",
            "harness_no_write_guard",
            "no_delivery_attestation",
            "no_write_attestation",
        },
        "routing delivery precheck section",
        failures,
    )
    require_all(
        set(precheck.get("deliveryDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "delivery_precheck_not_formal_delivery",
            "no_routing_delivery_execution",
            "no_recipient_notification_execution",
            "no_recipient_acknowledgement_execution",
            "no_repair_owner_notification_execution",
            "no_acknowledgement_routing_execution",
            "no_repair_request_creation",
            "no_committee_case_opening",
            "no_harness_evidence_write",
            "no_business_write",
        },
        "routing delivery precheck constraint",
        failures,
    )
    require_all(
        set(precheck.get("forbiddenActions", [])),
        {
            "execute_routing_delivery",
            "send_recipient_notification",
            "execute_recipient_acknowledgement",
            "send_repair_owner_notification",
            "execute_acknowledgement_routing",
            "create_repair_request",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
        },
        "forbidden action",
        failures,
    )
    for relative_path in data.get("requiredSourceRefs", []):
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")
    for key in (
        "executesRoutingDeliveryPrecheck",
        "executesRoutingDelivery",
        "sendsRecipientNotification",
        "executesRecipientAcknowledgement",
        "sendsRepairOwnerNotification",
        "executesAcknowledgementRouting",
        "executesIntakeAcknowledgement",
        "executesRepairRequestCompletenessPrecheck",
        "executesRepairIntake",
        "createsRepairRequest",
        "opensCommitteeCase",
        "executesCommitteeDecision",
        "executesHumanConfirmation",
        "writesKds",
        "writesBusinessSystem",
        "writesHarnessEvidence",
        "writesFormalEvidence",
        "writesRevenueDistribution",
        "writesContributionScore",
    ):
        if expected[key] is not False:
            failures.append(f"{key} must be false in expectedSummary")

    if failures:
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_delivery_precheck_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_aggregation_repair_request_acknowledgement_routing_delivery_precheck_dry_run=pass")
    print(f"status={precheck['precheckStatus']}")
    print(f"execution_mode={precheck['executionMode']}")
    print("executes_routing_delivery_precheck=0")
    print("executes_routing_delivery=0")
    print("sends_recipient_notification=0")
    print("executes_recipient_acknowledgement=0")
    print("sends_repair_owner_notification=0")
    print("executes_acknowledgement_routing=0")
    print("executes_intake_acknowledgement=0")
    print("creates_repair_request=0")
    print("opens_committee_case=0")
    print("writes_kds=0")
    print("writes_business_system=0")
    print("writes_harness_evidence=0")
    print("writes_formal_evidence=0")
    print("writes_revenue_distribution=0")
    print("writes_contribution_score=0")
    print("no_write=covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
