#!/usr/bin/env python3
"""Validate GFIS Writeback Sandbox policy.

This validator reads local OKF, shared type and fixture files only. It does not
write GFIS, GPC, ERP, MES, KDS, WAES, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "gfis-writeback-sandbox-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "gfis-writeback-sandbox.ts"
FIXTURE = ROOT / "fixtures" / "gfis" / "writeback-sandbox-policy-smoke.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected"]

    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]
    failures: list[str] = []

    if union_literals("GfisWritebackMode") != policy["writeback_modes"]:
        failures.append("GfisWritebackMode union does not match policy")
    if union_literals("GfisWritebackFinalAction") != policy["final_actions"]:
        failures.append("GfisWritebackFinalAction union does not match policy")
    if any(mode in policy["allowed_before_p1"] for mode in policy["blocked_before_p1"]):
        failures.append("allowed_before_p1 overlaps blocked_before_p1")

    checks = {
        "writebackModeCount": len(policy["writeback_modes"]),
        "allowedBeforeP1": policy["allowed_before_p1"],
        "blockedBeforeP1": policy["blocked_before_p1"],
        "finalActionCount": len(policy["final_actions"]),
        "minimumFieldCount": len(policy["minimum_fields"]),
        "approvedWriteRequiresCount": len(policy["approved_write_requires"]),
        "productionWriteRequiresCount": len(policy["production_write_requires"]),
        "aiAllowedModes": hard["ai_allowed_modes"],
        "aiBlockedModes": hard["ai_blocked_modes"],
        "noWriteCannotEmitTargetReceipt": hard["no_write_cannot_emit_target_receipt"],
        "sandboxCannotEmitTargetReceipt": hard["sandbox_cannot_emit_target_receipt"],
        "finalActionAcceptedIsNotWritebackReceipt": hard["final_action_accepted_is_not_writeback_receipt"],
        "missingEvidenceBlocks": hard["missing_evidence_blocks"],
        "missingWaesResultBlocks": hard["missing_waes_result_blocks"],
        "missingBusinessOwnerBlocks": hard["missing_business_owner_blocks"],
        "writesGfis": no_write["writes_gfis"],
        "writesGpc": no_write["writes_gpc"],
        "writesErp": no_write["writes_erp"],
        "writesMes": no_write["writes_mes"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("gfis_writeback_sandbox_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_writeback_sandbox_policy_smoke=pass "
        f"modes={checks['writebackModeCount']} "
        "allowed_before_p1=no_write,sandbox "
        "blocked_before_p1=approved_write,production_write "
        f"minimum_fields={checks['minimumFieldCount']} "
        f"approved_requires={checks['approvedWriteRequiresCount']} "
        f"production_requires={checks['productionWriteRequiresCount']} "
        "ai_boundary=covered "
        "accepted_is_not_receipt=covered "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
