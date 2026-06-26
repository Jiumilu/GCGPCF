#!/usr/bin/env python3
"""Validate Headroom LCX external receipt negative fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py"
NEGATIVE_FIXTURES = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-external-receipt-negative-fixtures.json"

FALSE_FIELDS = [
    "production_proxy_started",
    "production_sdk_enabled",
    "real_kds_write",
    "external_api_write",
    "database_migration",
    "permission_change",
    "accepted",
    "integrated",
    "production_ready",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json_any(path: Path) -> Any:
    return json.loads(read(path))


def load_json(path: Path) -> dict[str, Any]:
    data = load_json_any(path)
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-23",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def rejection_reason(receipt: dict[str, Any]) -> str | None:
    if receipt.get("telemetry") != "off":
        return "telemetry_must_remain_off"
    if receipt.get("sensitive_material_attestation") != "no_unsanitized_customer_contract_pod_financial_secret_or_production_credential_processed":
        return "sensitive_material_attestation_invalid"
    for field in FALSE_FIELDS:
        if receipt.get(field) is not False:
            return f"{field}_must_be_false"
    return None


def main() -> int:
    evidence = load_json(E_JSON)
    fixtures = load_json_any(NEGATIVE_FIXTURES)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_fixtures" in builder, "builder must build fixtures")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-20260623", "invalid evidence id")
    require(evidence.get("status") == "negative_fixtures_ready_no_completed_receipt_recorded", "invalid status")
    require(evidence.get("fixture_count") == 11, "fixture count mismatch")
    require(evidence.get("expected_rejected_count") == 11, "expected rejected count mismatch")
    require(evidence.get("expected_accepted_count") == 0, "expected accepted count must be zero")
    require(fixtures == evidence.get("fixtures"), "fixture file must match evidence fixtures")

    rejected = 0
    accepted = 0
    for item in fixtures:
        receipt = item.get("receipt", {})
        require(isinstance(receipt, dict), "fixture receipt must be an object")
        reason = rejection_reason(receipt)
        if reason:
            rejected += 1
        else:
            accepted += 1
    require(rejected == 11, f"all negative fixtures must be rejected, got {rejected}")
    require(accepted == 0, f"no negative fixture may be accepted, got {accepted}")

    decision = evidence.get("pre_execution_decision", {})
    for field in [
        "completed_receipt_instance_created",
        "can_open_real_measurement",
        "real_measurement_open",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(decision.get(field) is False, f"decision must keep {field}=false")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-20260623",
        "negative_fixtures_ready_no_completed_receipt_recorded",
        "fixture_count | `11`",
        "expected_rejected_count | `11`",
        "expected_accepted_count | `0`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_real_measurement_external_receipt_negative_fixtures=pass "
        "fixture_count=11 rejected_count=11 accepted_count=0 "
        "completed_receipt_instance_created=false real_measurement_open=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
