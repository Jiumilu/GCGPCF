#!/usr/bin/env python3
"""Validate WAES/Harness final receipt decision response intake for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-intake-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-response-intake-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-RESPONSE-INTAKE-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_response_intake.py"
TARGET_RESPONSE = ROOT / "fixtures/headroom/headroom-lcx-waes-harness-final-receipt-decision.response.json"


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
    evidence = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("validate_response" in builder, "builder must validate response")
    expected_recorded = TARGET_RESPONSE.exists()
    expected_status = "final_response_intake_valid_pending_chain_replay" if expected_recorded else "response_intake_ready_missing_final_response"
    require(evidence.get("status") == expected_status, "status mismatch")
    require(evidence.get("final_response_recorded") is expected_recorded, "recorded flag mismatch")

    check = evidence.get("response_check", {})
    if expected_recorded:
        require(check.get("response_instance_valid") is True, "response should be valid when recorded")
        require(check.get("missing_fields") == [], "recorded response must not miss fields")
        require(check.get("invalid_false_fields") == [], "recorded response must keep protected flags false")
        require(check.get("invalid_fields") == [], "recorded response must not contain invalid fields")
    else:
        require(check.get("response_instance_valid") is False, "missing response cannot be valid")
        require("final_response_file_missing" in check.get("invalid_fields", []), "missing response reason must be recorded")

    decision = evidence.get("pre_execution_decision", {})
    require(decision.get("waes_harness_final_decision_recorded") is expected_recorded, "final decision recorded flag mismatch")
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
        expected_status,
        f"waes_harness_final_decision_recorded | `{str(expected_recorded).lower()}`",
        "real_measurement_open | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_waes_harness_final_receipt_decision_response_intake.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_waes_harness_final_receipt_decision_response_intake.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_waes_harness_final_receipt_decision_response_intake=pass "
        f"status={expected_status} final_response_recorded={str(expected_recorded).lower()} "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
