#!/usr/bin/env python3
"""Validate Headroom LCX external receipt completion package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_completion_package.py"
COMPLETED_TEMPLATE = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.template.json"
AUTHORIZED_COMPLETED_RECEIPT = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.json"

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
    package = load_json(E_JSON)
    completed_template = load_json(COMPLETED_TEMPLATE)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_package" in builder, "builder must build package")
    require(package.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-20260623", "invalid evidence id")
    require(package.get("status") == "completion_package_ready_no_completed_receipt_recorded", "invalid status")
    require(package.get("project_count") == 15, "project count mismatch")
    require(package.get("completed_template_path") == COMPLETED_TEMPLATE.relative_to(ROOT).as_posix(), "template path mismatch")
    require(package.get("forbidden_completed_receipt_path_until_human_fill") == AUTHORIZED_COMPLETED_RECEIPT.relative_to(ROOT).as_posix(), "receipt path mismatch")
    require(package.get("completed_template") == completed_template, "fixture template must match package template")

    require(completed_template.get("telemetry") == "off", "telemetry must stay off")
    require("REQUIRED" in completed_template.get("execution_operator", ""), "operator must remain a required placeholder")
    require("REQUIRED" in completed_template.get("waes_harness_receipt_decision", ""), "WAES/Harness receipt decision must remain required")
    for field in FALSE_FIELDS:
        require(completed_template.get(field) is False, f"completed template must keep {field}=false")
    if AUTHORIZED_COMPLETED_RECEIPT.exists():
        completed_receipt = load_json(AUTHORIZED_COMPLETED_RECEIPT)
        for field in FALSE_FIELDS:
            require(completed_receipt.get(field) is False, f"completed receipt must keep {field}=false")

    rules = package.get("negative_validation_rules", {})
    for key, value in rules.items():
        require(value is True, f"negative rule must be true: {key}")

    decision = package.get("pre_execution_decision", {})
    for key in [
        "external_receipt_recorded",
        "completed_receipt_instance_created",
        "can_open_real_measurement",
        "real_measurement_open",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(decision.get(key) is False, f"decision must keep {key}=false")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-20260623",
        "completion_package_ready_no_completed_receipt_recorded",
        "completed_template_path",
        "must_not_create_completed_receipt_automatically",
        "completed_receipt_instance_created | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_external_receipt_completion_package.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_real_measurement_external_receipt_completion_package.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_real_measurement_external_receipt_completion_package=pass "
        "status=completion_package_ready_no_completed_receipt_recorded project_count=15 "
        "completed_receipt_instance_created=false real_measurement_open=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
