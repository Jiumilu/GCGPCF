#!/usr/bin/env python3
"""Validate GFIS Assistant repair prompt checklist dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-assistant-repair-prompt-checklist-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-assistant-repair-prompt-checklist.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "repair-prompt-checklist-dry-run.json"

NO_WRITE_KEYS = (
    "writesGfis",
    "writesGpc",
    "writesErp",
    "writesMes",
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesGapRecord",
    "writesBountyRecord",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
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
    checklists: list[dict[str, Any]] = fixture["checklists"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "GfisAssistantRepairPromptItemType": policy["item_types"],
        "GfisAssistantRepairPromptItemStatus": policy["item_statuses"],
        "GfisAssistantRepairPromptChecklistStatus": policy["checklist_statuses"],
        "GfisAssistantRepairPromptDisplayAction": policy["allowed_display_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    item_types = set(policy["item_types"])
    item_statuses = set(policy["item_statuses"])
    checklist_statuses = set(policy["checklist_statuses"])
    display_actions = set(policy["allowed_display_actions"])
    blocked_actions = set(policy["blocked_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "itemCount": 0,
        "repairRequired": 0,
        "open": 0,
        "blocked": 0,
        "metadataOnlyItems": 0,
        "submitsEvidence": 0,
        "createsGapRecords": 0,
        "createsBountyRecords": 0,
        "createsKweWorkItems": 0,
        "createsWaesGateResults": 0,
        "approvesBusinessWrite": 0,
        "promotesLifecycle": 0,
        "checklistsWithBlockedActions": 0,
    }

    for checklist in checklists:
        checklist_id = checklist["checklistId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in checklist})
        if missing:
            failures.append(f"{checklist_id} missing required fields: {missing}")
        if checklist["checklistStatus"] not in checklist_statuses:
            failures.append(f"{checklist_id}: invalid checklistStatus")
        if not checklist["items"]:
            failures.append(f"{checklist_id}: items are required")
        missing_blocks = sorted(blocked_actions - set(checklist["blockedActions"]))
        if missing_blocks:
            failures.append(f"{checklist_id}: missing blockedActions {missing_blocks}")
        unknown_display = sorted(set(checklist["allowedDisplayActions"]) - display_actions)
        if unknown_display:
            failures.append(f"{checklist_id}: unknown allowedDisplayActions {unknown_display}")

        counts["repairRequired"] += int(checklist["checklistStatus"] == "repair_required")
        counts["open"] += int(checklist["checklistStatus"] == "open")
        counts["blocked"] += int(checklist["checklistStatus"] == "blocked")
        counts["submitsEvidence"] += int(checklist["submitsEvidence"] is True)
        counts["createsGapRecords"] += int(checklist["createsGapRecord"] is True)
        counts["createsBountyRecords"] += int(checklist["createsBountyRecord"] is True)
        counts["createsKweWorkItems"] += int(checklist["createsKweWorkItem"] is True)
        counts["createsWaesGateResults"] += int(checklist["createsWaesGateResult"] is True)
        counts["approvesBusinessWrite"] += int(checklist["approvesBusinessWrite"] is True)
        counts["promotesLifecycle"] += int(checklist["promotesLifecycle"] is True)
        counts["checklistsWithBlockedActions"] += int(bool(checklist["blockedActions"]))

        false_flags = (
            "submitsEvidence",
            "createsGapRecord",
            "createsBountyRecord",
            "createsKweWorkItem",
            "createsWaesGateResult",
            "approvesBusinessWrite",
            "promotesLifecycle",
        )
        for flag in false_flags:
            if checklist[flag] is not False:
                failures.append(f"{checklist_id}: {flag} must be false")

        for item in checklist["items"]:
            counts["itemCount"] += 1
            if item["itemType"] not in item_types:
                failures.append(f"{checklist_id}: invalid itemType {item['itemType']}")
            if item["itemStatus"] not in item_statuses:
                failures.append(f"{checklist_id}: invalid itemStatus {item['itemStatus']}")
            if not item["prompt"] or not item["requiredRefs"]:
                failures.append(f"{checklist_id}: item prompt and requiredRefs are required")
            counts["metadataOnlyItems"] += int(item["metadataOnly"] is True)
            raw_tokens = " ".join(item["requiredRefs"] + item["evidenceHintRefs"] + [item["prompt"]])
            if "raw" in raw_tokens or "原文" in raw_tokens:
                failures.append(f"{checklist_id}: checklist must not expose raw content refs")

        for key in NO_WRITE_KEYS:
            value = checklist["noWrite"].get(key)
            if value != 0:
                failures.append(f"{checklist_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "checklistCount": len(checklists),
        **counts,
        **totals,
    }

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
        print("gfis_assistant_repair_prompt_checklist=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_repair_prompt_checklist=pass "
        f"checklists={actual['checklistCount']} items={actual['itemCount']} "
        f"repair_required={actual['repairRequired']} open={actual['open']} blocked={actual['blocked']} "
        f"metadata_only_items={actual['metadataOnlyItems']} submits_evidence={actual['submitsEvidence']} "
        f"creates_gap_records={actual['createsGapRecords']} creates_bounty_records={actual['createsBountyRecords']} "
        f"creates_kwe_work_items={actual['createsKweWorkItems']} creates_waes_gate_results={actual['createsWaesGateResults']} "
        f"approves_business_write={actual['approvesBusinessWrite']} promotes_lifecycle={actual['promotesLifecycle']} "
        f"checklists_with_blocked_actions={actual['checklistsWithBlockedActions']} "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_gap_record=0 writes_bounty_record=0 "
        "writes_kds_lifecycle=0 writes_kds_fact=0 writes_kds_accepted_fact=0 "
        "writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
