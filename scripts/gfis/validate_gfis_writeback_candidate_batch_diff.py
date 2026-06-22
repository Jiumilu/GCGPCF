#!/usr/bin/env python3
"""Validate GFIS writeback candidate batch diff no-write dry-run.

This validator reads local OKF, shared type, and fixture files only. It does
not write GFIS, GPC, ERP, MES, KDS accepted facts, WAES gate results, KWE work
items, revenue, scores, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-writeback-candidate-batch-diff-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-writeback-candidate-batch-diff.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "writeback-candidate-batch-diff-dry-run.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def normalized_keys(record: dict[str, Any]) -> set[str]:
    return {re.sub(r"(?<!^)([A-Z])", r"_\1", key).lower() for key in record}


def no_write_sum(record: dict[str, Any]) -> int:
    return sum(int(value) for value in record.values())


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    batch = fixture["batch"]
    items: list[dict[str, Any]] = batch["items"]
    expected = fixture["expected"]

    failures: list[str] = []
    hard = policy["hard_boundaries"]
    no_write_policy = policy["no_write_assertions"]
    required_batch = set(policy["required_batch_fields"])
    required_item = set(policy["required_item_fields"])
    required_diff = set(policy["required_field_diff_fields"])

    if union_literals("GfisWritebackBatchDiffAction") != policy["diff_actions"]:
        failures.append("GfisWritebackBatchDiffAction union does not match policy")
    if union_literals("GfisWritebackBatchKweNextAction") != policy["kwe_next_actions"]:
        failures.append("GfisWritebackBatchKweNextAction union does not match policy")
    if union_literals("GfisWritebackBatchRiskLevel") != policy["risk_levels"]:
        failures.append("GfisWritebackBatchRiskLevel union does not match policy")

    missing_batch = sorted(required_batch - normalized_keys(batch))
    if missing_batch:
        failures.append(f"batch missing required fields: {missing_batch}")
    if batch["targetSystem"] != "GFIS":
        failures.append("batch targetSystem must be GFIS")
    if batch["dryRun"] is not True:
        failures.append("batch dryRun must be true")
    if no_write_sum(batch["batchNoWrite"]) != 0:
        failures.append("batchNoWrite contains non-zero counters")

    for item in items:
        missing_item = sorted(required_item - normalized_keys(item))
        if missing_item:
            failures.append(f"{item['candidateId']} missing required fields: {missing_item}")
        if item["approvedForBusinessWrite"]:
            failures.append(f"{item['candidateId']} approves business write")
        if item["targetReceiptRefs"]:
            failures.append(f"{item['candidateId']} emits target receipt refs")
        if item["writebackStatus"] == "written_back":
            failures.append(f"{item['candidateId']} is written_back in dry-run")
        if no_write_sum(item["noWrite"]) != 0:
            failures.append(f"{item['candidateId']} noWrite contains non-zero counters")
        if item["waesGateStatus"] == "blocked" and item["diffAction"] != "block_writeback":
            failures.append(f"{item['candidateId']} blocked gate not mapped to block_writeback")
        if not item["evidenceRefs"] and item["diffAction"] not in {"block_writeback", "return_for_repair"}:
            failures.append(f"{item['candidateId']} lacks evidence but is not blocked or repair")
        if item["targetEntityType"] in {"pod_record", "finance_record", "quality_record"}:
            if item["sensitiveHandling"] not in {"metadata_only", "controlled_original"}:
                failures.append(f"{item['candidateId']} sensitive target lacks controlled handling")
        for diff in item["fieldDiffs"]:
            missing_diff = sorted(required_diff - normalized_keys(diff))
            if missing_diff:
                failures.append(f"{item['candidateId']} diff missing required fields: {missing_diff}")

    checks = {
        "itemCount": len(items),
        "fieldDiffCount": sum(len(item["fieldDiffs"]) for item in items),
        "metadataOnlyItems": sum(1 for item in items if item["sensitiveHandling"] == "metadata_only"),
        "controlledOriginalItems": sum(1 for item in items if item["sensitiveHandling"] == "controlled_original"),
        "humanEscalations": sum(1 for item in items if item["diffAction"] == "escalate_human"),
        "committeeEscalations": sum(1 for item in items if item["diffAction"] == "escalate_committee"),
        "blockedItems": sum(1 for item in items if item["diffAction"] == "block_writeback"),
        "approvedForBusinessWrite": sum(1 for item in items if item["approvedForBusinessWrite"]),
        "targetReceipts": sum(len(item["targetReceiptRefs"]) for item in items),
        "writtenBackStatuses": sum(1 for item in items if item["writebackStatus"] == "written_back"),
        "writesGfis": sum(item["noWrite"]["writesGfis"] for item in items) + batch["batchNoWrite"]["writesGfis"],
        "writesGpc": sum(item["noWrite"]["writesGpc"] for item in items) + batch["batchNoWrite"]["writesGpc"],
        "writesErp": sum(item["noWrite"]["writesErp"] for item in items) + batch["batchNoWrite"]["writesErp"],
        "writesMes": sum(item["noWrite"]["writesMes"] for item in items) + batch["batchNoWrite"]["writesMes"],
        "writesKdsAcceptedFact": sum(item["noWrite"]["writesKdsAcceptedFact"] for item in items)
        + batch["batchNoWrite"]["writesKdsAcceptedFact"],
        "writesWaesGateResult": sum(item["noWrite"]["writesWaesGateResult"] for item in items)
        + batch["batchNoWrite"]["writesWaesGateResult"],
        "writesKweWorkItem": sum(item["noWrite"]["writesKweWorkItem"] for item in items)
        + batch["batchNoWrite"]["writesKweWorkItem"],
        "writesRevenueOrScoreConfirmation": sum(
            item["noWrite"]["writesRevenueOrScoreConfirmation"] for item in items
        )
        + batch["batchNoWrite"]["writesRevenueOrScoreConfirmation"],
        "writesExternalApi": sum(item["noWrite"]["writesExternalApi"] for item in items)
        + batch["batchNoWrite"]["writesExternalApi"],
    }

    for key, value in hard.items():
        if value is not True:
            failures.append(f"policy hard_boundaries.{key} is not true")
    for key, value in no_write_policy.items():
        if value != 0:
            failures.append(f"policy no_write_assertions.{key} is non-zero")
    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("gfis_writeback_candidate_batch_diff=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_writeback_candidate_batch_diff=pass "
        f"items={checks['itemCount']} "
        f"field_diffs={checks['fieldDiffCount']} "
        f"metadata_only_items={checks['metadataOnlyItems']} "
        f"controlled_original_items={checks['controlledOriginalItems']} "
        f"human_escalations={checks['humanEscalations']} "
        f"committee_escalations={checks['committeeEscalations']} "
        f"blocked_items={checks['blockedItems']} "
        "approved_for_business_write=0 target_receipts=0 written_back_statuses=0 "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_kds_accepted_fact=0 writes_waes_gate_result=0 writes_kwe_work_item=0 "
        "writes_revenue_or_score_confirmation=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
