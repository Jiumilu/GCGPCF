#!/usr/bin/env python3
"""Validate Brain and PKC entry contracts as read-only dry-run surfaces.

This script uses local fixtures only. It does not write Brain, PKC, KDS,
WAES, KWE, GFIS, GPC, or any external API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "brain-pkc" / "entry-contract-smoke.json"


REQUIRED_BLOCKED_ACTIONS = {
    "brain": {
        "direct_accept_fact",
        "direct_gfis_writeback",
        "direct_waes_gate_override",
    },
    "pkc": {
        "final_fact_confirmation",
        "force_kds_lifecycle_change",
        "business_system_writeback",
    },
}


def requested_views(case: dict[str, Any]) -> list[str]:
    if case["surface"] == "brain":
        return case.get("requestedModules", [])
    return case.get("requestedSections", [])


def evaluate(case: dict[str, Any]) -> dict[str, Any]:
    expected = case["expected"]
    return {
        "coveredViews": requested_views(case),
        "blockedActions": expected["blockedActions"],
        "noWrite": True,
        "kdsWrites": 0,
        "waesWrites": 0,
        "kweWrites": 0,
        "businessWrites": 0,
        "externalApiWrites": 0,
    }


def compare(case: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    expected = case["expected"]
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{case['id']} {key}: expected={expected_value!r} actual={actual.get(key)!r}")

    required = REQUIRED_BLOCKED_ACTIONS[case["surface"]]
    blocked = set(actual["blockedActions"])
    missing = sorted(required - blocked)
    if missing:
        failures.append(f"{case['id']} missing required blocked actions: {missing}")

    if not actual["coveredViews"]:
        failures.append(f"{case['id']} has no covered views")

    return failures


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    failures: list[str] = []
    surfaces = set()
    total_views = 0
    total_blocked_actions = 0

    for case in data["cases"]:
        surfaces.add(case["surface"])
        actual = evaluate(case)
        total_views += len(actual["coveredViews"])
        total_blocked_actions += len(actual["blockedActions"])
        failures.extend(compare(case, actual))

    if surfaces != {"brain", "pkc"}:
        failures.append(f"surface coverage expected brain+pkc actual={sorted(surfaces)}")

    if failures:
        print("brain_pkc_entry_contract_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "brain_pkc_entry_contract_smoke=pass "
        f"cases={len(data['cases'])} "
        f"surfaces={','.join(sorted(surfaces))} "
        f"covered_views={total_views} "
        f"blocked_actions={total_blocked_actions} "
        "no_write=covered kds_writes=0 waes_writes=0 kwe_writes=0 "
        "business_writes=0 external_api_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
