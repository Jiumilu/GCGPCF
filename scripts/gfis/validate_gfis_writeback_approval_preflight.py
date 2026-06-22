#!/usr/bin/env python3
"""Validate GFIS writeback approval preflight dry-run boundary.

This validator checks local policies, type declarations, and fixtures only. It
does not approve writeback, write GFIS/GPC/ERP/MES, mutate KDS lifecycle, create
WAES gate results, create KWE work items, confirm revenue or scores, or call
external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-writeback-approval-preflight-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-writeback-approval-preflight.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "writeback-approval-preflight-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesKdsAcceptedFact",
    "writesKdsLifecycle",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesTargetReceipt",
    "writesRevenueOrScoreConfirmation",
    "writesExternalApi",
)


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
    batch: dict[str, Any] = fixture["preflightBatch"]
    items: list[dict[str, Any]] = batch["items"]
    expected = fixture["expected"]
    failures: list[str] = []

    policy_statuses = set(policy["preflight_statuses"])
    type_statuses = extract_union_literals(type_text, "GfisWritebackApprovalPreflightStatus")
    if policy_statuses != type_statuses:
        fail(failures, f"preflight status mismatch policy={sorted(policy_statuses)} type={sorted(type_statuses)}")

    batch_fields = {camel_to_snake(key) for key in batch.keys()}
    missing_batch = sorted(set(policy["required_batch_fields"]) - batch_fields)
    if missing_batch:
        fail(failures, f"missing batch fields: {missing_batch}")

    item_fields = {camel_to_snake(key) for key in items[0].keys()}
    missing_item = sorted(set(policy["required_item_fields"]) - item_fields)
    if missing_item:
        fail(failures, f"missing item fields: {missing_item}")

    for key, value in policy["hard_boundaries"].items():
        if value is not True:
            fail(failures, f"hard boundary must be true: {key}")
    if any(value != 0 for value in policy["no_write_guards"].values()):
        fail(failures, "policy no_write_guards must all be zero")

    if batch["dryRun"] is not True:
        fail(failures, "batch dryRun must be true")
    for key in NO_WRITE_KEYS:
        if batch["batchNoWrite"].get(key) != 0:
            fail(failures, f"batchNoWrite {key} must be 0")

    counts = {
        "humanRequired": 0,
        "committeeRequired": 0,
        "metadataOnlyRequired": 0,
        "repairRequired": 0,
        "blocked": 0,
        "approvalEligible": 0,
        "businessWriteAllowed": 0,
        "targetReceipts": 0,
        "itemsWithLifecycleAudit": 0,
        "itemsWithWaesGateRefs": 0,
        "metadataOnlyItems": 0,
        "controlledOriginalItems": 0,
    }
    totals = {key: 0 for key in NO_WRITE_KEYS}

    for item in items:
        item_id = item["preflightId"]
        status = item["preflightStatus"]
        waes_status = item["waesGateStatus"]
        lifecycle_status = item["lifecycleAuditStatus"]
        sensitive = item["sensitiveHandling"]

        if status not in policy_statuses:
            fail(failures, f"{item_id}: unknown preflightStatus {status}")

        if item["approvalEligible"] is not False:
            fail(failures, f"{item_id}: approvalEligible must be false")
        if item["businessWriteAllowed"] is not False:
            fail(failures, f"{item_id}: businessWriteAllowed must be false")
        if item["targetReceiptRefs"]:
            fail(failures, f"{item_id}: targetReceiptRefs must be empty")

        for key in NO_WRITE_KEYS:
            value = item["noWrite"].get(key)
            if value != 0:
                fail(failures, f"{item_id}: {key} must be 0")
            totals[key] += value

        if item["lifecycleAuditRefs"]:
            counts["itemsWithLifecycleAudit"] += 1
        elif status not in {"repair_required", "blocked"}:
            fail(failures, f"{item_id}: missing lifecycleAuditRefs must repair or block")

        if item["waesGateRefs"]:
            counts["itemsWithWaesGateRefs"] += 1

        if not item["evidenceRefs"] and status not in {"repair_required", "blocked"}:
            fail(failures, f"{item_id}: missing evidence must repair or block")

        if waes_status == "blocked" and status != "blocked":
            fail(failures, f"{item_id}: blocked WAES gate must block preflight")
        if waes_status == "committee_required" and status != "committee_required":
            fail(failures, f"{item_id}: committee WAES gate must require committee")
        if waes_status == "human_required" and sensitive != "metadata_only" and status != "human_required":
            fail(failures, f"{item_id}: human WAES gate must require human when not metadata-only")
        if sensitive == "metadata_only":
            counts["metadataOnlyItems"] += 1
            if status not in {"metadata_only_required", "blocked"}:
                fail(failures, f"{item_id}: metadata-only item must be metadata_only_required or blocked")
        if sensitive == "controlled_original":
            counts["controlledOriginalItems"] += 1
            if not item["evidenceRefs"] and status != "blocked":
                fail(failures, f"{item_id}: controlled original item requires evidence unless blocked")

        if lifecycle_status == "blocked" and status != "blocked":
            fail(failures, f"{item_id}: blocked lifecycle audit must block preflight")

        if status == "human_required":
            counts["humanRequired"] += 1
        elif status == "committee_required":
            counts["committeeRequired"] += 1
        elif status == "metadata_only_required":
            counts["metadataOnlyRequired"] += 1
        elif status == "repair_required":
            counts["repairRequired"] += 1
        elif status == "blocked":
            counts["blocked"] += 1

        counts["approvalEligible"] += int(item["approvalEligible"] is True)
        counts["businessWriteAllowed"] += int(item["businessWriteAllowed"] is True)
        counts["targetReceipts"] += len(item["targetReceiptRefs"])

    actual = {
        "itemCount": len(items),
        **counts,
        "writesGfis": totals["writesGfis"],
        "writesGpc": totals["writesGpc"],
        "writesErp": totals["writesErp"],
        "writesMes": totals["writesMes"],
        "writesKdsAcceptedFact": totals["writesKdsAcceptedFact"],
        "writesKdsLifecycle": totals["writesKdsLifecycle"],
        "writesWaesGateResult": totals["writesWaesGateResult"],
        "writesKweWorkItem": totals["writesKweWorkItem"],
        "writesTargetReceipt": totals["writesTargetReceipt"],
        "writesRevenueOrScoreConfirmation": totals["writesRevenueOrScoreConfirmation"],
        "writesExternalApi": totals["writesExternalApi"],
    }

    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            fail(failures, f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("gfis_writeback_approval_preflight=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_writeback_approval_preflight=pass "
        f"items={actual['itemCount']} "
        f"human_required={actual['humanRequired']} "
        f"committee_required={actual['committeeRequired']} "
        f"metadata_only_required={actual['metadataOnlyRequired']} "
        f"repair_required={actual['repairRequired']} "
        f"blocked={actual['blocked']} "
        f"approval_eligible={actual['approvalEligible']} "
        f"business_write_allowed={actual['businessWriteAllowed']} "
        f"target_receipts={actual['targetReceipts']} "
        f"items_with_lifecycle_audit={actual['itemsWithLifecycleAudit']} "
        f"items_with_waes_gate_refs={actual['itemsWithWaesGateRefs']} "
        f"metadata_only_items={actual['metadataOnlyItems']} "
        f"controlled_original_items={actual['controlledOriginalItems']} "
        f"writes_gfis={actual['writesGfis']} "
        f"writes_gpc={actual['writesGpc']} "
        f"writes_erp={actual['writesErp']} "
        f"writes_mes={actual['writesMes']} "
        f"writes_kds_accepted_fact={actual['writesKdsAcceptedFact']} "
        f"writes_kds_lifecycle={actual['writesKdsLifecycle']} "
        f"writes_waes_gate_result={actual['writesWaesGateResult']} "
        f"writes_kwe_work_item={actual['writesKweWorkItem']} "
        f"writes_target_receipt={actual['writesTargetReceipt']} "
        f"writes_revenue_or_score_confirmation={actual['writesRevenueOrScoreConfirmation']} "
        f"writes_external_api={actual['writesExternalApi']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
