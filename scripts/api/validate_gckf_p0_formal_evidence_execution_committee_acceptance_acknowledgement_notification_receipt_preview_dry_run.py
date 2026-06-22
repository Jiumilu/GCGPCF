#!/usr/bin/env python3
"""Validate P0 committee acceptance acknowledgement notification receipt preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-notification-receipt-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceCommitteeAcceptanceAcknowledgementNotificationPreview"])
    source = source_data["committeeAcceptanceAcknowledgementNotificationPreview"]
    receipt = data["committeeAcceptanceAcknowledgementNotificationReceiptPreview"]

    if data.get("committeeAcceptanceAcknowledgementNotificationReceiptPreviewStatus") != expected[
        "committeeAcceptanceAcknowledgementNotificationReceiptPreviewStatus"
    ]:
        failures.append("committeeAcceptanceAcknowledgementNotificationReceiptPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalCommitteeAcceptanceAcknowledgementNotificationReceipt") is not expected[
        "notFinalCommitteeAcceptanceAcknowledgementNotificationReceipt"
    ]:
        failures.append("notification receipt preview must state notFinalCommitteeAcceptanceAcknowledgementNotificationReceipt=true")
    if receipt.get("previewType") != expected["previewType"]:
        failures.append("committee acceptance acknowledgement notification receipt previewType mismatch")
    if receipt.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee acceptance acknowledgement notification receipt previewStatus must remain candidate_preview")
    if receipt.get("executionMode") != expected["executionMode"]:
        failures.append("committee acceptance acknowledgement notification receipt executionMode mismatch")
    if receipt.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee acceptance acknowledgement notification receipt must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "notificationReceiptPreviewExecutionStatus",
        "notificationReceiptExecutionStatus",
        "notificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "envelopeAssemblyExecutionStatus",
        "committeeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if receipt.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("committeeAcceptanceAcknowledgementNotificationPreviewStatus") != expected[
        "sourceCommitteeAcceptanceAcknowledgementNotificationPreviewStatus"
    ]:
        failures.append("source notification preview must remain candidate_preview")
    source_status_map = {
        "notificationPreviewExecutionStatus": "sourceNotificationPreviewExecutionStatus",
        "notificationExecutionStatus": "sourceNotificationExecutionStatus",
        "acknowledgementRoutingExecutionStatus": "sourceAcknowledgementRoutingExecutionStatus",
        "envelopeAssemblyExecutionStatus": "sourceEnvelopeAssemblyExecutionStatus",
        "committeeAcceptanceExecutionStatus": "sourceCommitteeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus": "sourceCommitteeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source notification preview must remain dryRunOnly=true")
    if receipt.get("sourceCommitteeAcceptanceAcknowledgementNotificationPreviewId") != source.get("id"):
        failures.append("sourceCommitteeAcceptanceAcknowledgementNotificationPreviewId must match D70 preview id")
    if data.get("coveredCommitteeAcceptanceAcknowledgementNotificationPreviewStatus") != source.get("previewStatus"):
        failures.append("covered notification status must match D70 preview status")

    count_checks = {
        "receiptRoles": "receiptRoleCount",
        "receiptSections": "receiptSectionCount",
        "candidateReceiptFields": "candidateReceiptFieldCount",
        "receiptReadinessPrerequisites": "receiptReadinessPrerequisiteCount",
        "receiptDecisionConstraints": "receiptDecisionConstraintCount",
        "receiptChecks": "receiptCheckCount",
        "requiredReceiptRefs": "requiredReceiptRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(receipt.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(receipt.get("receiptSections", [])),
        {
            "candidate_receipt_header",
            "candidate_recipient_acknowledgement_matrix",
            "candidate_channel_receipt_matrix",
            "candidate_message_digest_reference",
            "candidate_acl_boundary_snapshot",
            "candidate_delivery_hold_conditions",
            "candidate_delivery_blocker_codes",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "committee acceptance acknowledgement notification receipt section",
        failures,
    )
    require_all(
        set(receipt.get("receiptDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "receipt_preview_not_formal_receipt",
            "no_notification_receipt_preview_execution",
            "no_notification_receipt_execution",
            "no_notification_execution",
            "no_acknowledgement_routing_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_harness_evidence_write",
        },
        "committee acceptance acknowledgement notification receipt constraint",
        failures,
    )
    require_all(
        set(receipt.get("forbiddenActions", [])),
        {
            "execute_notification_receipt_preview",
            "execute_notification_receipt",
            "execute_notification",
            "execute_acknowledgement_routing",
            "execute_committee_acceptance",
            "execute_committee_acknowledgement",
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
        "executesNotificationReceiptPreview",
        "executesNotificationReceipt",
        "executesNotification",
        "executesAcknowledgementRouting",
        "executesEnvelopeAssembly",
        "executesCommitteeAcceptancePrecheck",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_notification_receipt_preview_dry_run=pass")
    print(f"status={receipt['previewStatus']}")
    print(f"execution_mode={receipt['executionMode']}")
    print("executes_notification_receipt_preview=0")
    print("executes_notification_receipt=0")
    print("executes_notification=0")
    print("executes_acknowledgement_routing=0")
    print("executes_committee_acceptance=0")
    print("executes_committee_acknowledgement=0")
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
