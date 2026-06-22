#!/usr/bin/env python3
"""Validate Brain/PKC/GFIS Assistant KWE queue read model no-write boundaries."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "brain-pkc-kwe-queue-read-model-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "brain-pkc-kwe-queue-read-model.ts"
FIXTURE = ROOT / "fixtures" / "brain-pkc" / "kwe-queue-read-model-dry-run.json"

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


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def normalized_keys(record: dict[str, Any]) -> set[str]:
    return {re.sub(r"(?<!^)([A-Z])", r"_\1", key).lower() for key in record}


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    views: list[dict[str, Any]] = fixture["views"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "BrainPkcKweQueueSurface": policy["surfaces"],
        "BrainPkcKweQueueScope": policy["scopes"],
        "BrainPkcKweQueueVisibility": policy["visibility_modes"],
        "BrainPkcKweQueueDisplayMode": policy["display_modes"],
        "BrainPkcKweQueueBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    required_blocked_actions = set(policy["blocked_actions"])
    cross_unit_leaks = 0
    totals = {key: 0 for key in NO_WRITE_KEYS}

    for view in views:
        view_id = view["viewId"]
        missing = sorted(required_fields - normalized_keys(view))
        if missing:
            failures.append(f"{view_id} missing required fields: {missing}")
        missing_actions = sorted(required_blocked_actions - set(view["blockedActions"]))
        if missing_actions:
            failures.append(f"{view_id} missing blocked actions: {missing_actions}")
        for key in NO_WRITE_KEYS:
            value = view["noWrite"].get(key)
            if value != 0:
                failures.append(f"{view_id}: {key} must be 0")
            totals[key] += value

        if view["surface"] == "pkc" and view["visibility"] not in {"own_only", "project_authorized"}:
            failures.append(f"{view_id}: PKC visibility must be own_only or project_authorized")
        if view["surface"] == "gfis_assistant" and "complete_approval" not in view["blockedActions"]:
            failures.append(f"{view_id}: GFIS assistant must block approval completion")
        if view["scope"] == "committee_queue" and view["visibility"] != "committee_authorized":
            failures.append(f"{view_id}: committee queue requires committee authorization")
        if view["scope"] == "blocked_queue" and not view["filter"].get("includeBlocked"):
            failures.append(f"{view_id}: blocked queue must include blocked")
        if view["displayMode"] == "masked_cross_unit":
            for ref in view["maskedRouteRefs"]:
                if not ref.startswith("masked:"):
                    cross_unit_leaks += 1
        if view["visibility"] == "governance_aggregate" and view["visibleRouteRefs"] and view["scope"] != "blocked_queue":
            cross_unit_leaks += 1

    checks = {
        "viewCount": len(views),
        "brainViews": sum(1 for view in views if view["surface"] == "brain"),
        "pkcViews": sum(1 for view in views if view["surface"] == "pkc"),
        "gfisAssistantViews": sum(1 for view in views if view["surface"] == "gfis_assistant"),
        "committeeAuthorizedViews": sum(1 for view in views if view["visibility"] == "committee_authorized"),
        "ownOnlyViews": sum(1 for view in views if view["visibility"] == "own_only"),
        "maskedViews": sum(1 for view in views if view["maskedRouteRefs"] or view["displayMode"] == "masked_cross_unit"),
        "blockedQueueViews": sum(1 for view in views if view["scope"] == "blocked_queue"),
        "blockedActionCount": sum(len(view["blockedActions"]) for view in views),
        "crossUnitLeakCount": cross_unit_leaks,
        **totals,
    }

    for key, value in policy["hard_boundaries"].items():
        if value is not True:
            failures.append(f"policy hard_boundaries.{key} is not true")
    for key, value in policy["no_write_assertions"].items():
        if value != 0:
            failures.append(f"policy no_write_assertions.{key} is non-zero")
    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("brain_pkc_kwe_queue_read_model=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "brain_pkc_kwe_queue_read_model=pass "
        f"views={checks['viewCount']} brain_views={checks['brainViews']} pkc_views={checks['pkcViews']} "
        f"gfis_assistant_views={checks['gfisAssistantViews']} "
        f"committee_authorized_views={checks['committeeAuthorizedViews']} own_only_views={checks['ownOnlyViews']} "
        f"masked_views={checks['maskedViews']} blocked_queue_views={checks['blockedQueueViews']} "
        f"blocked_actions={checks['blockedActionCount']} cross_unit_leaks=0 "
        "writes_kwe_work_item=0 writes_kds_lifecycle=0 writes_kds_fact=0 "
        "writes_kds_accepted_fact=0 writes_waes_gate_result=0 writes_business_system=0 "
        "writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
