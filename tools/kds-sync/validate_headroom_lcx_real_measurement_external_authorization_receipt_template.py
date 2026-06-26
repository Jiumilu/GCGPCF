#!/usr/bin/env python3
"""Validate Headroom LCX external authorization receipt template evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-authorization-receipt-template-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-001.md"
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt-template.json"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_external_authorization_receipt_template.py"

LEDGER_REF = "docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json"

REQUIRED_FIELDS = [
    "receipt_id",
    "authorized_window_id",
    "authorized_by",
    "authorized_at",
    "sanitized_production_usage_ledger",
    "rollback_plan_id",
    "waes_harness_admission_decision",
    "execution_operator",
    "execution_started_at",
    "execution_finished_at",
    "telemetry",
    "sensitive_material_attestation",
    "production_proxy_started",
    "production_sdk_enabled",
    "real_kds_write",
    "external_api_write",
    "database_migration",
    "permission_change",
    "real_measurement_open",
    "production_token_measurement_allowed",
    "measured_production_tokens",
    "answer_equivalence",
    "waes_harness_receipt_decision",
    "rollback_exercised",
    "evidence_refs",
    "accepted",
    "integrated",
    "production_ready",
]

FALSE_FIELDS = [
    "production_proxy_started",
    "production_sdk_enabled",
    "real_kds_write",
    "external_api_write",
    "database_migration",
    "permission_change",
    "real_measurement_open",
    "production_token_measurement_allowed",
    "measured_production_tokens",
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


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
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


def main() -> int:
    data = load_json(E_JSON)
    fixture = load_json(FIXTURE)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_receipt_template" in builder, "builder must build receipt template")
    require(
        data.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-20260623",
        "invalid evidence id",
    )
    require(data.get("status") == "external_authorization_receipt_template_ready_no_execution", "invalid status")
    require(data.get("receipt_status") == "template_only_pending_external_receipt", "invalid receipt status")
    require(data.get("project_count") == 15, "project count mismatch")
    require(data.get("sanitized_production_usage_ledger") == LEDGER_REF, "ledger reference mismatch")

    template = data.get("receipt_template", {})
    require(isinstance(template, dict), "receipt_template must be an object")
    require(set(REQUIRED_FIELDS).issubset(template.keys()), "missing required receipt template fields")
    require(fixture == template, "fixture must match receipt_template")
    require(template.get("telemetry") == "off", "telemetry must remain off")
    require(template.get("sanitized_production_usage_ledger") == LEDGER_REF, "template ledger reference mismatch")
    for key in FALSE_FIELDS:
        require(template.get(key) is False, f"template must keep {key}=false")

    gates = data.get("pre_execution_gates", {})
    require(gates.get("chain_replay_exists") is True, "chain replay gate must be true")
    require(gates.get("authorization_window_granted") is True, "authorization window grant gate must be true")
    for key in [
        "external_receipt_recorded",
        "real_measurement_open",
        "production_proxy_started",
        "production_sdk_enabled",
        "real_kds_write",
        "external_api_write",
        "database_migration",
        "permission_change",
        "measured_production_tokens",
        "production_token_measurement_allowed",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"pre-execution gate must keep {key}=false")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-AUTHORIZATION-RECEIPT-TEMPLATE-20260623",
        "external_authorization_receipt_template_ready_no_execution",
        "template_only_pending_external_receipt",
        "real_measurement_open | `false`",
        "measured_production_tokens | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
        "模板不等于正式外部回执",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_external_authorization_receipt_template.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_real_measurement_external_authorization_receipt_template.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_real_measurement_external_authorization_receipt_template=pass "
        "project_count=15 receipt_status=template_only_pending_external_receipt "
        "real_measurement_open=false measured_production_tokens=false accepted=false "
        "integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
