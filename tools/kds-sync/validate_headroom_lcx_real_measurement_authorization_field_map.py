#!/usr/bin/env python3
"""Validate the Headroom LCX real-measurement authorization field map evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_authorization_field_map.py"


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
    field_map = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("real_measurement_authorization_field_map" in runner, "runner must build authorization field map")
    require(field_map.get("field_map_id") == "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623", "invalid field map id")
    require(field_map.get("status") == "authorization_field_map_defined_precheck_only", "invalid field map status")
    require(field_map.get("scope", {}).get("project_count") == 15, "project count mismatch")
    require(field_map.get("current_state", {}).get("production_token_measurement_allowed") is False, "production token measurement must remain false")
    require(field_map.get("current_state", {}).get("measured_production_tokens") is False, "measured production tokens must remain false")
    require(field_map.get("execution_guard", {}).get("executable_now") is False, "execution must remain blocked")
    require(field_map.get("execution_guard", {}).get("requires_real_measurement_authorization_window") is True, "authorization window gate must be required")
    require(field_map.get("execution_guard", {}).get("requires_waes_harness_decision") is True, "WAES/Harness decision gate must be required")
    require(field_map.get("execution_guard", {}).get("requires_sanitized_token_ledger_metadata_only") is True, "sanitized ledger gate must be required")
    require(field_map.get("rollback_anchor", {}).get("rollback_plan_present") is True, "rollback plan must be present")
    require(field_map.get("rollback_anchor", {}).get("rollback_runbook_written") is True, "rollback runbook must be written")

    rows = field_map.get("field_map", [])
    require(len(rows) == 6, "field map must contain 6 fields")
    expected_fields = {
        "authorized_window_id",
        "authorized_by",
        "authorized_at",
        "sanitized_production_token_ledger",
        "rollback_plan_id",
        "waes_harness_admission_decision",
    }
    require({row.get("field") for row in rows} == expected_fields, "field set mismatch")
    require(
        field_map.get("future_runner_inputs")
        == [
            "authorized_window_id",
            "authorized_by",
            "authorized_at",
            "sanitized_production_token_ledger",
            "rollback_plan_id",
            "waes_harness_admission_decision",
        ],
        "future runner input mismatch",
    )

    for row in rows:
        require(row.get("future_runner_input") == row.get("field"), f"future runner input mismatch: {row.get('field')}")
        require(isinstance(row.get("current_value"), str) and row.get("current_value"), f"current value missing: {row.get('field')}")
        require(isinstance(row.get("source_evidence"), str) and row.get("source_evidence"), f"source evidence missing: {row.get('field')}")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623",
        "authorization_field_map_defined_precheck_only",
        "executable_now: `false`",
        "requires_real_measurement_authorization_window: `true`",
        "requires_waes_harness_decision: `true`",
        "requires_no_production_proxy: `true`",
        "production_ready: `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in [
        "authorization field map",
        "build_headroom_lcx_real_measurement_authorization_field_map.py",
        "validate_headroom_lcx_real_measurement_authorization_field_map.py",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "headroom_lcx_real_measurement_authorization_field_map=pass "
        "project_count=15 executable_now=false production_token_measurement_allowed=false "
        "measured_production_tokens=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
