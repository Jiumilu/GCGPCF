#!/usr/bin/env python3
"""Validate WAES precheck bundle read model dry-run boundary."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "waes-precheck-bundle-read-model-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "waes-precheck-bundle-read-model.ts"
FIXTURE = ROOT / "fixtures" / "waes" / "precheck-bundle-read-model-dry-run.json"

NO_WRITE_KEYS = (
    "writesWaesGateResult",
    "writesKweWorkItem",
    "writesKdsLifecycle",
    "writesKdsFact",
    "writesKdsAcceptedFact",
    "writesBusinessSystem",
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
    bundles: list[dict[str, Any]] = fixture["bundles"]
    expected = fixture["expected"]
    failures: list[str] = []

    unions = {
        "WaesPrecheckBundleSurface": policy["surfaces"],
        "WaesPrecheckBundleScope": policy["scopes"],
        "WaesPrecheckBundleReadAction": policy["allowed_read_actions"],
        "WaesPrecheckBundleBlockedAction": policy["blocked_write_actions"],
    }
    for type_name, expected_literals in unions.items():
        if union_literals(type_name) != expected_literals:
            failures.append(f"{type_name} union does not match policy")

    required_fields = set(policy["required_fields"])
    surfaces = set(policy["surfaces"])
    scopes = set(policy["scopes"])
    allowed_read_actions = set(policy["allowed_read_actions"])
    blocked_write_actions = set(policy["blocked_write_actions"])
    totals = {key: 0 for key in NO_WRITE_KEYS}
    counts = {
        "brainBundles": 0,
        "kweBundles": 0,
        "gfisAssistantBundles": 0,
        "bundlesWithBlockedActions": 0,
        "gateSummaryItems": 0,
        "canCreateWaesGateResults": 0,
        "canCreateKweWorkItems": 0,
        "canPromoteLifecycle": 0,
    }

    for bundle in bundles:
        bundle_id = bundle["bundleId"]
        missing = sorted(required_fields - {camel_to_snake(key) for key in bundle})
        if missing:
            failures.append(f"{bundle_id} missing required fields: {missing}")
        if bundle["surface"] not in surfaces:
            failures.append(f"{bundle_id}: invalid surface")
        if bundle["scope"] not in scopes:
            failures.append(f"{bundle_id}: invalid scope")
        if not bundle["precheckRefs"] or not bundle["routeRefs"]:
            failures.append(f"{bundle_id}: precheckRefs and routeRefs are required")
        if not bundle["gateSummary"]:
            failures.append(f"{bundle_id}: gateSummary is required")
        unknown_reads = sorted(set(bundle["allowedReadActions"]) - allowed_read_actions)
        if unknown_reads:
            failures.append(f"{bundle_id}: unknown allowedReadActions {unknown_reads}")
        missing_blocks = sorted(blocked_write_actions - set(bundle["blockedActions"]))
        if missing_blocks:
            failures.append(f"{bundle_id}: missing blockedActions {missing_blocks}")

        counts["brainBundles"] += int(bundle["surface"] == "brain")
        counts["kweBundles"] += int(bundle["surface"] == "kwe")
        counts["gfisAssistantBundles"] += int(bundle["surface"] == "gfis_assistant")
        counts["bundlesWithBlockedActions"] += int(bool(bundle["blockedActions"]))
        counts["gateSummaryItems"] += len(bundle["gateSummary"])
        counts["canCreateWaesGateResults"] += int(bundle["canCreateWaesGateResult"] is True)
        counts["canCreateKweWorkItems"] += int(bundle["canCreateKweWorkItem"] is True)
        counts["canPromoteLifecycle"] += int(bundle["canPromoteLifecycle"] is True)

        if bundle["canCreateWaesGateResult"] is not False:
            failures.append(f"{bundle_id}: canCreateWaesGateResult must be false")
        if bundle["canCreateKweWorkItem"] is not False:
            failures.append(f"{bundle_id}: canCreateKweWorkItem must be false")
        if bundle["canPromoteLifecycle"] is not False:
            failures.append(f"{bundle_id}: canPromoteLifecycle must be false")

        for item in bundle["gateSummary"]:
            if item["count"] <= 0:
                failures.append(f"{bundle_id}: gateSummary count must be positive")
        for key in NO_WRITE_KEYS:
            value = bundle["noWrite"].get(key)
            if value != 0:
                failures.append(f"{bundle_id}: {key} must be 0")
            totals[key] += value

    actual = {
        "bundleCount": len(bundles),
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
        print("waes_precheck_bundle_read_model=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "waes_precheck_bundle_read_model=pass "
        f"bundles={actual['bundleCount']} brain_bundles={actual['brainBundles']} "
        f"kwe_bundles={actual['kweBundles']} gfis_assistant_bundles={actual['gfisAssistantBundles']} "
        f"bundles_with_blocked_actions={actual['bundlesWithBlockedActions']} "
        f"gate_summary_items={actual['gateSummaryItems']} "
        f"can_create_waes_gate_results={actual['canCreateWaesGateResults']} "
        f"can_create_kwe_work_items={actual['canCreateKweWorkItems']} "
        f"can_promote_lifecycle={actual['canPromoteLifecycle']} "
        "writes_waes_gate_result=0 writes_kwe_work_item=0 writes_kds_lifecycle=0 "
        "writes_kds_fact=0 writes_kds_accepted_fact=0 writes_business_system=0 "
        "writes_target_receipt=0 writes_committee_decision_completion=0 "
        "writes_revenue_or_score_confirmation=0 writes_quota_transfer=0 "
        "writes_bounty_settlement=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
