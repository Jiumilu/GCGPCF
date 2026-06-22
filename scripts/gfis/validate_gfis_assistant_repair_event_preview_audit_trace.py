#!/usr/bin/env python3
"""Validate GFIS Assistant repair event preview audit trace no-write boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-event-preview-audit-trace-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-event-preview-audit-trace.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-event-preview-audit-trace-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesAuditTraceRecord",
    "writesEventRecord",
    "writesActionReceipt",
    "writesReadReceipt",
    "writesHarnessEvidence",
    "writesAdmissionRecord",
    "writesReviewQueueItem",
    "writesConfirmationRecord",
    "writesDecisionRecord",
    "writesGapRecord",
    "writesBountyRecord",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
    "writesEvidenceRecord",
    "writesTargetReceipt",
    "writesCommitteeDecisionCompletion",
    "writesRevenueOrScoreConfirmation",
    "writesQuotaTransfer",
    "writesBountySettlement",
    "writesExternalApi",
)


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    traces: list[dict[str, Any]] = fixture["auditTraces"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairEventPreviewAuditTraceType": policy["trace_types"],
        "GfisAssistantRepairEventPreviewAuditTraceStatus": policy["trace_statuses"],
        "GfisAssistantRepairEventPreviewAuditTraceDecision": policy["trace_decisions"],
        "GfisAssistantRepairEventPreviewAuditTraceBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    trace_types = set(policy["trace_types"])
    trace_statuses = set(policy["trace_statuses"])
    trace_decisions = set(policy["trace_decisions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainSurface": 0,
        "pkcSurface": 0,
        "gfisAssistantSurface": 0,
        "displayAuditTrace": 0,
        "repairAuditTrace": 0,
        "metadataBoundaryAuditTrace": 0,
        "committeeAuditTrace": 0,
        "freezeAuditTrace": 0,
        "blockedWriteAuditTrace": 0,
        "tracePreviewOnly": 0,
        "blockedTracePreview": 0,
        "metadataTracePreview": 0,
        "repairTracePreview": 0,
        "committeeTracePreview": 0,
        "freezeTracePreview": 0,
        "showTraceOnly": 0,
        "showRepairTrace": 0,
        "showMetadataBoundaryTrace": 0,
        "showCommitteeTrace": 0,
        "showFreezeTrace": 0,
        "showBlockedWriteTrace": 0,
        "createsAuditTraceRecords": 0,
        "createsEventRecords": 0,
        "createsActionReceipts": 0,
        "createsReadReceipts": 0,
        "createsHarnessEvidence": 0,
        "createsWaesGateResults": 0,
        "createsKweWorkItems": 0,
        "persistsEvidence": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "completesCommitteeDecision": 0,
    }
    surface_keys = {"brain": "brainSurface", "pkc": "pkcSurface", "gfis_assistant": "gfisAssistantSurface"}
    type_keys = {
        "display_audit_trace": "displayAuditTrace",
        "repair_audit_trace": "repairAuditTrace",
        "metadata_boundary_audit_trace": "metadataBoundaryAuditTrace",
        "committee_audit_trace": "committeeAuditTrace",
        "freeze_audit_trace": "freezeAuditTrace",
        "blocked_write_audit_trace": "blockedWriteAuditTrace",
    }
    status_keys = {
        "trace_preview_only": "tracePreviewOnly",
        "blocked_trace_preview": "blockedTracePreview",
        "metadata_trace_preview": "metadataTracePreview",
        "repair_trace_preview": "repairTracePreview",
        "committee_trace_preview": "committeeTracePreview",
        "freeze_trace_preview": "freezeTracePreview",
    }
    decision_keys = {
        "show_trace_only": "showTraceOnly",
        "show_repair_trace": "showRepairTrace",
        "show_metadata_boundary_trace": "showMetadataBoundaryTrace",
        "show_committee_trace": "showCommitteeTrace",
        "show_freeze_trace": "showFreezeTrace",
        "show_blocked_write_trace": "showBlockedWriteTrace",
    }

    for trace in traces:
        trace_id = trace["auditTraceId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in trace})
        if missing:
            failures.append(f"{trace_id} missing required fields: {missing}")
        if trace["traceType"] not in trace_types:
            failures.append(f"{trace_id}: invalid traceType")
        if trace["traceStatus"] not in trace_statuses:
            failures.append(f"{trace_id}: invalid traceStatus")
        if trace["traceDecision"] not in trace_decisions:
            failures.append(f"{trace_id}: invalid traceDecision")
        missing_blocks = sorted(blocked_actions - set(trace["blockedActions"]))
        if missing_blocks:
            failures.append(f"{trace_id}: missing blockedActions {missing_blocks}")
        if not trace["traceSummaryRef"] or not trace["reasonRefs"] or not trace["auditNoteRefs"]:
            failures.append(f"{trace_id}: traceSummaryRef, reasonRefs, and auditNoteRefs are required")

        counts[surface_keys[trace["surface"]]] += 1
        counts[type_keys[trace["traceType"]]] += 1
        counts[status_keys[trace["traceStatus"]]] += 1
        counts[decision_keys[trace["traceDecision"]]] += 1
        false_flags = (
            "createsAuditTraceRecord",
            "createsEventRecord",
            "createsActionReceipt",
            "createsReadReceipt",
            "createsHarnessEvidence",
            "createsWaesGateResult",
            "createsKweWorkItem",
            "persistsEvidence",
            "approvesBusinessWrite",
            "promotesLifecycle",
            "completesCommitteeDecision",
        )
        for flag in false_flags:
            if trace[flag] is not False:
                failures.append(f"{trace_id}: {flag} must be false")
        counts["createsAuditTraceRecords"] += int(trace["createsAuditTraceRecord"] is True)
        counts["createsEventRecords"] += int(trace["createsEventRecord"] is True)
        counts["createsActionReceipts"] += int(trace["createsActionReceipt"] is True)
        counts["createsReadReceipts"] += int(trace["createsReadReceipt"] is True)
        counts["createsHarnessEvidence"] += int(trace["createsHarnessEvidence"] is True)
        counts["createsWaesGateResults"] += int(trace["createsWaesGateResult"] is True)
        counts["createsKweWorkItems"] += int(trace["createsKweWorkItem"] is True)
        counts["persistsEvidence"] += int(trace["persistsEvidence"] is True)
        counts["approvesBusinessWrite"] += int(trace["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(trace["promotesLifecycle"] is True)
        counts["completesCommitteeDecision"] += int(trace["completesCommitteeDecision"] is True)

        ref_text = " ".join(
            [trace["traceSummaryRef"]]
            + trace["lineageHintRefs"]
            + trace["reasonRefs"]
            + trace["auditNoteRefs"]
            + trace["blockedActions"]
        )
        if "raw" in ref_text or "原文" in ref_text:
            failures.append(f"{trace_id}: audit trace preview must not expose raw content refs")
        for key in NO_WRITE_KEYS:
            value = trace["noWrite"].get(key)
            if value != 0:
                failures.append(f"{trace_id}: {key} must be 0")
            totals[key] += value

    actual = {"auditTraceCount": len(traces), **counts, **totals}

    for key, value in policy["hard_boundaries"].items():
        if value is not True:
            failures.append(f"policy hard_boundaries.{key} is not true")
    for key, value in policy["no_write_guards"].items():
        if value != 0:
            failures.append(f"policy no_write_guards.{key} is non-zero")
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("gfis_assistant_repair_event_preview_audit_trace=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_event_preview_audit_trace=pass "
        f"traces={actual['auditTraceCount']} brain={actual['brainSurface']} pkc={actual['pkcSurface']} "
        f"gfis_assistant={actual['gfisAssistantSurface']} display_audit_trace={actual['displayAuditTrace']} "
        f"repair_audit_trace={actual['repairAuditTrace']} metadata_boundary_audit_trace={actual['metadataBoundaryAuditTrace']} "
        f"committee_audit_trace={actual['committeeAuditTrace']} freeze_audit_trace={actual['freezeAuditTrace']} "
        f"blocked_write_audit_trace={actual['blockedWriteAuditTrace']} creates_audit_trace_records={actual['createsAuditTraceRecords']} "
        f"creates_event_records={actual['createsEventRecords']} creates_action_receipts={actual['createsActionReceipts']} "
        f"creates_read_receipts={actual['createsReadReceipts']} creates_harness_evidence={actual['createsHarnessEvidence']} "
        f"creates_waes_gate_results={actual['createsWaesGateResults']} creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"persists_evidence={actual['persistsEvidence']} approves_business_write={actual['approvesBusinessWrite']} "
        f"promotes_lifecycle={actual['promotesLifecycle']} completes_committee_decision={actual['completesCommitteeDecision']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_audit_trace_record=0 writes_event_record=0 "
        "writes_action_receipt=0 writes_read_receipt=0 writes_harness_evidence=0 "
        "writes_admission_record=0 writes_review_queue_item=0 writes_confirmation_record=0 "
        "writes_decision_record=0 writes_gap_record=0 writes_bounty_record=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_evidence_record=0 writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
