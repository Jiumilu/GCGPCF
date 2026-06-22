#!/usr/bin/env python3
"""Validate KWE approval route packet dry-run boundary.

This validator checks local policy, shared type text, and fixture declarations
only. It does not create KWE work items, mutate KDS lifecycle, write facts,
create WAES gate results, write business systems, complete committee decisions,
confirm revenue or scores, or call external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "kwe-approval-route-packet-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "kwe-approval-route-packet.ts"
FIXTURE = ROOT / "fixtures" / "kwe" / "approval-route-packet-dry-run.json"

NO_WRITE_KEYS = (
    "writesKweWorkItem",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
    "writesWaesGateResult",
    "writesBusinessSystem",
    "writesTargetReceipt",
    "writesCommitteeDecisionCompletion",
    "writesRevenueOrScoreConfirmation",
    "writesQuotaTransfer",
    "writesBountySettlement",
    "writesExternalApi",
)

EXPECTED_ROUTE = {
    "human_required": ("human_queue", "route_ready"),
    "committee_required": ("committee_queue", "route_ready"),
    "metadata_only_required": ("metadata_only_queue", "route_ready"),
    "repair_required": ("repair_queue", "repair_required"),
    "blocked": ("blocked_queue", "blocked"),
    "preflight_required": ("repair_queue", "preflight_required"),
}


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def extract_union_literals(text: str, type_name: str) -> set[str]:
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise AssertionError(f"missing union type: {type_name}")
    return set(re.findall(r'"([^"]+)"', match.group("body")))


def fail(failures: list[str], message: str) -> None:
    failures.append(message)


def main() -> int:
    policy = yaml.safe_load(POLICY.read_text())
    type_text = TYPE_FILE.read_text()
    fixture = json.loads(FIXTURE.read_text())
    packet: dict[str, Any] = fixture["routePacket"]
    items: list[dict[str, Any]] = packet["items"]
    expected = fixture["expected"]
    failures: list[str] = []

    policy_queues = set(policy["route_queues"])
    type_queues = extract_union_literals(type_text, "KweApprovalRouteQueue")
    if policy_queues != type_queues:
        fail(failures, f"route queue mismatch policy={sorted(policy_queues)} type={sorted(type_queues)}")

    policy_statuses = set(policy["route_statuses"])
    type_statuses = extract_union_literals(type_text, "KweApprovalRouteStatus")
    if policy_statuses != type_statuses:
        fail(failures, f"route status mismatch policy={sorted(policy_statuses)} type={sorted(type_statuses)}")

    packet_fields = {camel_to_snake(key) for key in packet.keys()}
    missing_packet = sorted(set(policy["required_packet_fields"]) - packet_fields)
    if missing_packet:
        fail(failures, f"missing packet fields: {missing_packet}")

    item_fields = {camel_to_snake(key) for key in items[0].keys()}
    missing_item = sorted(set(policy["required_item_fields"]) - item_fields)
    if missing_item:
        fail(failures, f"missing item fields: {missing_item}")

    for key, value in policy["hard_boundaries"].items():
        if value is not True:
            fail(failures, f"hard boundary must be true: {key}")
    if any(value != 0 for value in policy["no_write_guards"].values()):
        fail(failures, "policy no_write_guards must all be zero")
    if packet["dryRun"] is not True:
        fail(failures, "packet dryRun must be true")
    for key in NO_WRITE_KEYS:
        if packet["packetNoWrite"].get(key) != 0:
            fail(failures, f"packetNoWrite {key} must be 0")

    queue_counts = {
        "humanQueue": 0,
        "committeeQueue": 0,
        "metadataOnlyQueue": 0,
        "repairQueue": 0,
        "blockedQueue": 0,
    }
    queue_key = {
        "human_queue": "humanQueue",
        "committee_queue": "committeeQueue",
        "metadata_only_queue": "metadataOnlyQueue",
        "repair_queue": "repairQueue",
        "blocked_queue": "blockedQueue",
    }
    totals = {key: 0 for key in NO_WRITE_KEYS}
    route_ready = 0
    blocked = 0
    creates_work_items = 0
    items_with_evidence = 0
    items_with_waes = 0
    items_with_lifecycle = 0

    for item in items:
        route_id = item["routeId"]
        preflight_status = item["preflightStatus"]
        expected_queue, expected_status = EXPECTED_ROUTE[preflight_status]
        if item["routeQueue"] != expected_queue:
            fail(failures, f"{route_id}: routeQueue expected {expected_queue} actual {item['routeQueue']}")
        if item["routeStatus"] != expected_status:
            fail(failures, f"{route_id}: routeStatus expected {expected_status} actual {item['routeStatus']}")

        if item["createsKweWorkItem"] is not False:
            fail(failures, f"{route_id}: createsKweWorkItem must be false")
        creates_work_items += int(item["createsKweWorkItem"] is True)

        for key in NO_WRITE_KEYS:
            value = item["noWrite"].get(key)
            if value != 0:
                fail(failures, f"{route_id}: {key} must be 0")
            totals[key] += value

        queue_counts[queue_key[item["routeQueue"]]] += 1
        route_ready += int(item["routeStatus"] == "route_ready")
        blocked += int(item["routeStatus"] == "blocked")
        items_with_evidence += int(bool(item["evidenceRefs"]))
        items_with_waes += int(bool(item["waesGateRefs"]))
        items_with_lifecycle += int(bool(item["lifecycleAuditRefs"]))

        if item["preflightStatus"] == "blocked" and item["routeQueue"] != "blocked_queue":
            fail(failures, f"{route_id}: blocked preflight must route to blocked_queue")
        if item["preflightStatus"] == "committee_required" and item["routeQueue"] != "committee_queue":
            fail(failures, f"{route_id}: committee preflight must route to committee_queue")
        if item["sensitiveHandling"] == "metadata_only" and item["routeQueue"] != "metadata_only_queue":
            fail(failures, f"{route_id}: metadata-only route must use metadata_only_queue")
        if item["routeQueue"] == "repair_queue" and item["routeStatus"] == "route_ready":
            fail(failures, f"{route_id}: repair queue cannot be route_ready")

    actual = {
        "itemCount": len(items),
        **queue_counts,
        "routeReady": route_ready,
        "blocked": blocked,
        "createsKweWorkItems": creates_work_items,
        "itemsWithEvidence": items_with_evidence,
        "itemsWithWaesGateRefs": items_with_waes,
        "itemsWithLifecycleAuditRefs": items_with_lifecycle,
        **totals,
    }

    if packet["queueSummary"] != queue_counts:
        fail(failures, f"queueSummary mismatch expected={queue_counts} actual={packet['queueSummary']}")

    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            fail(failures, f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("kwe_approval_route_packet=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kwe_approval_route_packet=pass "
        f"items={actual['itemCount']} "
        f"human_queue={actual['humanQueue']} "
        f"committee_queue={actual['committeeQueue']} "
        f"metadata_only_queue={actual['metadataOnlyQueue']} "
        f"repair_queue={actual['repairQueue']} "
        f"blocked_queue={actual['blockedQueue']} "
        f"route_ready={actual['routeReady']} "
        f"blocked={actual['blocked']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} "
        f"items_with_evidence={actual['itemsWithEvidence']} "
        f"items_with_waes_gate_refs={actual['itemsWithWaesGateRefs']} "
        f"items_with_lifecycle_audit_refs={actual['itemsWithLifecycleAuditRefs']} "
        f"writes_kwe_work_item={actual['writesKweWorkItem']} "
        f"writes_kds_lifecycle={actual['writesKdsLifecycle']} "
        f"writes_kds_fact={actual['writesKdsFact']} "
        f"writes_kds_accepted_fact={actual['writesKdsAcceptedFact']} "
        f"writes_waes_gate_result={actual['writesWaesGateResult']} "
        f"writes_business_system={actual['writesBusinessSystem']} "
        f"writes_target_receipt={actual['writesTargetReceipt']} "
        f"writes_committee_decision_completion={actual['writesCommitteeDecisionCompletion']} "
        f"writes_revenue_or_score_confirmation={actual['writesRevenueOrScoreConfirmation']} "
        f"writes_quota_transfer={actual['writesQuotaTransfer']} "
        f"writes_bounty_settlement={actual['writesBountySettlement']} "
        f"writes_external_api={actual['writesExternalApi']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
