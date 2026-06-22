#!/usr/bin/env python3
"""Validate Brain/PKC revenue attribution read model no-write boundaries.

This validator reads local OKF, shared type, and fixture files only. It does
not confirm scores, distribute revenue, mutate KDS lifecycle, write WAES/KWE,
write business systems, or call external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "brain-pkc-revenue-attribution-read-model-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "brain-pkc-revenue-attribution-read-model.ts"
FIXTURE = ROOT / "fixtures" / "brain-pkc" / "revenue-attribution-read-model-dry-run.json"


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
    views: list[dict[str, Any]] = fixture["views"]
    expected = fixture["expected"]

    failures: list[str] = []
    required_fields = set(policy["required_fields"])
    required_blocked = set(policy["blocked_actions"])

    unions = {
        "BrainPkcRevenueAttributionSurface": policy["surfaces"],
        "BrainPkcRevenueAttributionScope": policy["scopes"],
        "BrainPkcRevenueAttributionVisibility": policy["visibility_modes"],
        "BrainPkcRevenueAttributionDisplayMode": policy["display_modes"],
        "BrainPkcRevenueAttributionBlockedAction": policy["blocked_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    cross_unit_leaks = 0
    for view in views:
        missing = sorted(required_fields - normalized_keys(view))
        if missing:
            failures.append(f"{view['viewId']} missing required fields: {missing}")
        if no_write_sum(view["noWrite"]):
            failures.append(f"{view['viewId']} has non-zero noWrite counters")
        missing_blocked = sorted(required_blocked - set(view["blockedActions"]))
        if missing_blocked:
            failures.append(f"{view['viewId']} missing blocked actions: {missing_blocked}")
        if view["surface"] == "pkc" and view["visibility"] not in {"own_only", "project_authorized"}:
            failures.append(f"{view['viewId']} PKC view has excessive visibility")
        if view["displayMode"] == "masked_cross_unit":
            for ref in view["maskedContributionRefs"]:
                if not ref.startswith("masked:"):
                    cross_unit_leaks += 1
            if any(ref.startswith("contribution-gehua-team") for ref in view["visibleContributionRefs"]):
                cross_unit_leaks += 1
        if view["visibility"] == "governance_aggregate" and view["visibleContributionRefs"]:
            cross_unit_leaks += 1
        if view["scope"] == "committee_review" and view["visibility"] != "committee_authorized":
            failures.append(f"{view['viewId']} committee review lacks committee authorization")

    checks = {
        "viewCount": len(views),
        "brainViews": sum(1 for view in views if view["surface"] == "brain"),
        "pkcViews": sum(1 for view in views if view["surface"] == "pkc"),
        "maskedViews": sum(1 for view in views if view["maskedContributionRefs"] or view["displayMode"] == "masked_cross_unit"),
        "committeeAuthorizedViews": sum(1 for view in views if view["visibility"] == "committee_authorized"),
        "ownOnlyViews": sum(1 for view in views if view["visibility"] == "own_only"),
        "blockedActionCount": sum(len(view["blockedActions"]) for view in views),
        "crossUnitLeakCount": cross_unit_leaks,
        "writesKdsLifecycle": sum(view["noWrite"]["writesKdsLifecycle"] for view in views),
        "writesWaesGateResult": sum(view["noWrite"]["writesWaesGateResult"] for view in views),
        "writesKweWorkItem": sum(view["noWrite"]["writesKweWorkItem"] for view in views),
        "writesScoreConfirmation": sum(view["noWrite"]["writesScoreConfirmation"] for view in views),
        "writesRevenueDistribution": sum(view["noWrite"]["writesRevenueDistribution"] for view in views),
        "writesBusinessSystem": sum(view["noWrite"]["writesBusinessSystem"] for view in views),
        "writesExternalApi": sum(view["noWrite"]["writesExternalApi"] for view in views),
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
        print("brain_pkc_revenue_attribution_read_model=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "brain_pkc_revenue_attribution_read_model=pass "
        f"views={checks['viewCount']} brain_views={checks['brainViews']} pkc_views={checks['pkcViews']} "
        f"masked_views={checks['maskedViews']} committee_authorized_views={checks['committeeAuthorizedViews']} "
        f"own_only_views={checks['ownOnlyViews']} blocked_actions={checks['blockedActionCount']} "
        "cross_unit_leaks=0 writes_kds_lifecycle=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_score_confirmation=0 writes_revenue_distribution=0 "
        "writes_business_system=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
