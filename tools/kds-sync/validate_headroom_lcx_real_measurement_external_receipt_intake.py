#!/usr/bin/env python3
"""Validate Headroom LCX external receipt intake evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-intake-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-intake-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_intake.py"
COMPLETED_RECEIPT = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.json"


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
    intake = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("validate_receipt" in builder, "builder must include receipt validation logic")
    require(intake.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-20260623", "invalid evidence id")
    expected_recorded = COMPLETED_RECEIPT.exists()
    expected_status = "receipt_intake_valid_precheck_only" if expected_recorded else "intake_validator_ready_missing_completed_receipt"
    require(intake.get("status") == expected_status, "status must match completed receipt presence")
    require(intake.get("project_count") == 15, "project count mismatch")
    require(intake.get("completed_receipt_recorded") is expected_recorded, "completed receipt recorded flag mismatch")
    require(intake.get("negative_fixture_count") == 11, "negative fixture count mismatch")
    require(intake.get("negative_fixture_expected_accepted_count") == 0, "negative accepted count must be zero")

    receipt_check = intake.get("receipt_check", {})
    if expected_recorded:
        require(receipt_check.get("receipt_instance_valid") is True, "recorded receipt must be valid for precheck-only intake")
        require(receipt_check.get("missing_fields") == [], "recorded receipt must not miss fields")
        require(receipt_check.get("invalid_false_fields") == [], "recorded receipt must not set protected fields true")
        require(receipt_check.get("invalid_fields") == [], "recorded receipt must not contain invalid fields")
    else:
        require(receipt_check.get("receipt_instance_valid") is False, "receipt instance must be invalid while missing")
        require("completed_receipt_file_missing" in receipt_check.get("invalid_fields", []), "missing receipt reason must be recorded")

    rules = intake.get("intake_rules", {})
    for key, value in rules.items():
        require(value is True, f"intake rule must be true: {key}")

    decision = intake.get("pre_execution_decision", {})
    require(decision.get("completed_receipt_recorded") is expected_recorded, "decision completed receipt flag mismatch")
    require(decision.get("receipt_instance_valid") is expected_recorded, "decision receipt valid flag mismatch")
    for field in [
        "can_open_real_measurement",
        "real_measurement_open",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(decision.get(field) is False, f"decision must keep {field}=false")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-INTAKE-20260623",
        expected_status,
        f"completed_receipt_recorded | `{str(expected_recorded).lower()}`",
        f"receipt_instance_valid | `{str(expected_recorded).lower()}`",
        "can_open_real_measurement | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_external_receipt_intake.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_real_measurement_external_receipt_intake.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_real_measurement_external_receipt_intake=pass "
        f"status={expected_status} completed_receipt_recorded={str(expected_recorded).lower()} "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
