#!/usr/bin/env python3
"""Validate P0 notification acknowledgement receipt routing acknowledgement preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-notification-acknowledgement-receipt-routing-acknowledgement-preview-dry-run-v0.1.json"
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
    failures: list[str] = []
    source_data = load_json(data["sourceNotificationAcknowledgementReceiptPreview"])
    source = source_data["notificationAcknowledgementReceiptPreview"]
    routing_ack = data["receiptRoutingAcknowledgementPreview"]

    if data.get("receiptRoutingAcknowledgementPreviewStatus") != expected["receiptRoutingAcknowledgementPreviewStatus"]:
        failures.append("receiptRoutingAcknowledgementPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalReceiptRoutingAcknowledgement") is not expected["notFinalReceiptRoutingAcknowledgement"]:
        failures.append("routing acknowledgement preview must state notFinalReceiptRoutingAcknowledgement=true")
    if routing_ack.get("previewType") != expected["previewType"]:
        failures.append("receipt routing acknowledgement previewType mismatch")
    if routing_ack.get("previewStatus") != expected["previewStatus"]:
        failures.append("receipt routing acknowledgement previewStatus must remain candidate_preview")
    if routing_ack.get("executionMode") != expected["executionMode"]:
        failures.append("receipt routing acknowledgement executionMode mismatch")
    if routing_ack.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("receipt routing acknowledgement must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "routingAcknowledgementPreviewExecutionStatus",
        "routingAcknowledgementExecutionStatus",
        "receiptPreviewExecutionStatus",
        "receiptExecutionStatus",
        "notificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "committeeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if routing_ack.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("notificationAcknowledgementReceiptPreviewStatus") != expected[
        "sourceNotificationAcknowledgementReceiptPreviewStatus"
    ]:
        failures.append("source receipt preview must remain candidate_preview")
    source_status_map = {
        "receiptPreviewExecutionStatus": "sourceReceiptPreviewExecutionStatus",
        "receiptExecutionStatus": "sourceReceiptExecutionStatus",
        "notificationExecutionStatus": "sourceNotificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus": "sourceAcknowledgementRoutingExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source receipt preview must remain dryRunOnly=true")
    if routing_ack.get("sourceNotificationAcknowledgementReceiptPreviewId") != source.get("id"):
        failures.append("sourceNotificationAcknowledgementReceiptPreviewId must match D71 preview id")
    if data.get("coveredNotificationAcknowledgementReceiptPreviewStatus") != source.get("previewStatus"):
        failures.append("covered receipt status must match D71 preview status")

    count_checks = {
        "routingAcknowledgementRoles": "routingAcknowledgementRoleCount",
        "routingAcknowledgementSections": "routingAcknowledgementSectionCount",
        "candidateRoutingAcknowledgementFields": "candidateRoutingAcknowledgementFieldCount",
        "routingAcknowledgementReadinessPrerequisites": "routingAcknowledgementReadinessPrerequisiteCount",
        "routingAcknowledgementDecisionConstraints": "routingAcknowledgementDecisionConstraintCount",
        "routingAcknowledgementChecks": "routingAcknowledgementCheckCount",
        "requiredRoutingAcknowledgementRefs": "requiredRoutingAcknowledgementRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(routing_ack.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(routing_ack.get("routingAcknowledgementSections", [])),
        {
            "candidate_routing_acknowledgement_header",
            "candidate_receipt_acknowledgement_matrix",
            "candidate_routing_channel_matrix",
            "candidate_routing_acknowledgement_payload_summary",
            "candidate_acl_boundary_snapshot",
            "candidate_routing_hold_conditions",
            "candidate_routing_blocker_codes",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "receipt routing acknowledgement section",
        failures,
    )
    require_all(
        set(routing_ack.get("routingAcknowledgementDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "routing_acknowledgement_preview_not_formal_acknowledgement",
            "no_routing_acknowledgement_preview_execution",
            "no_routing_acknowledgement_execution",
            "no_receipt_preview_execution",
            "no_receipt_execution",
            "no_notification_execution",
            "no_acknowledgement_routing_execution",
            "no_committee_case_opening",
            "no_formal_write",
            "no_harness_evidence_write",
        },
        "receipt routing acknowledgement constraint",
        failures,
    )
    require_all(
        set(routing_ack.get("forbiddenActions", [])),
        {
            "execute_routing_acknowledgement_preview",
            "execute_routing_acknowledgement",
            "execute_receipt_preview",
            "execute_receipt",
            "execute_notification",
            "execute_acknowledgement_routing",
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
        "executesRoutingAcknowledgementPreview",
        "executesRoutingAcknowledgement",
        "executesReceiptPreview",
        "executesReceipt",
        "executesNotification",
        "executesAcknowledgementRouting",
        "executesCommitteeAcceptance",
        "executesCommitteeAcknowledgement",
        "opensCommitteeCase",
        "executesCommitteeDecision",
        "executesHumanConfirmation",
        "releasesFreeze",
        "executesUnfreeze",
        "executesIntakeGuard",
        "executesRoutingPackage",
        "executesRouting",
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
        print("gckf_p0_formal_evidence_execution_notification_acknowledgement_receipt_routing_acknowledgement_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_notification_acknowledgement_receipt_routing_acknowledgement_preview_dry_run=pass")
    print(f"status={routing_ack['previewStatus']}")
    print(f"execution_mode={routing_ack['executionMode']}")
    print("executes_routing_acknowledgement_preview=0")
    print("executes_routing_acknowledgement=0")
    print("executes_receipt_preview=0")
    print("executes_receipt=0")
    print("executes_notification=0")
    print("executes_acknowledgement_routing=0")
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
