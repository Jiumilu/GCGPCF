#!/usr/bin/env python3
"""Validate Headroom LCX external receipt precheck evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_precheck.py"
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
    data = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_precheck" in builder, "builder must build precheck")
    require(data.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-20260623", "invalid evidence id")
    require(data.get("project_count") == 15, "project count mismatch")
    require(data.get("scope") == "external_receipt_instance_precheck_no_measurement", "invalid scope")
    expected_recorded = COMPLETED_RECEIPT.exists()
    expected_status = "receipt_instance_valid_precheck_only" if expected_recorded else "blocked_missing_external_receipt_instance"

    receipt = data.get("receipt_check", {})
    require(receipt.get("external_receipt_recorded") is expected_recorded, "formal receipt recorded flag mismatch")
    require(receipt.get("receipt_instance_valid") is expected_recorded, "receipt validity flag mismatch")
    require(data.get("status") == expected_status, "status must match completed receipt presence")
    require(receipt.get("expected_receipt_path") == "fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.json", "unexpected receipt path")

    decision = data.get("pre_execution_decision", {})
    for key in [
        "can_open_real_measurement",
        "real_measurement_open",
        "production_proxy_started",
        "production_sdk_enabled",
        "real_kds_write",
        "external_api_write",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(decision.get(key) is False, f"decision must keep {key}=false")
    require(decision.get("blocked") is (not expected_recorded), "precheck blocked flag mismatch")
    expected_blocker = "waes_harness_final_receipt_decision_required" if expected_recorded else "blocked_missing_external_receipt_instance"
    require(decision.get("blocker") == expected_blocker, "wrong blocker")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-20260623",
        expected_status,
        f"external_receipt_recorded | `{str(expected_recorded).lower()}`",
        f"receipt_instance_valid | `{str(expected_recorded).lower()}`",
        "can_open_real_measurement | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_external_receipt_precheck.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_real_measurement_external_receipt_precheck.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_real_measurement_external_receipt_precheck=pass "
        f"status={expected_status} project_count=15 "
        f"external_receipt_recorded={str(expected_recorded).lower()} real_measurement_open=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
