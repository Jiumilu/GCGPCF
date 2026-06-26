#!/usr/bin/env python3
"""Validate Headroom LCX external receipt human fill request."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-human-fill-request-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_human_fill_request.py"

REQUIRED_COMMANDS = [
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_intake.py",
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py",
    "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_completion_package.py",
    "python3 tools/kds-sync/validate_headroom_lcx_completion_audit.py",
    "python3 tools/kds-sync/validate_headroom_lcx_objective_coverage_matrix.py",
    "python3 tools/kds-sync/check_document_pollution.py",
    "python3 tools/kds-sync/validate_kds_token.py",
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
    request = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_request" in builder, "builder must build request")
    require(request.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-20260623", "invalid evidence id")
    require(request.get("status") == "human_fill_request_ready_no_completed_receipt_recorded", "invalid status")
    require(request.get("project_count") == 15, "project count mismatch")
    require(request.get("target_completed_receipt_path") == "fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.json", "target receipt path mismatch")
    require(set(REQUIRED_COMMANDS).issubset(set(request.get("verification_commands_after_fill", []))), "missing verification commands")

    for field in request.get("must_replace_required_placeholders", []):
        require(field in request.get("required_fields", []), f"placeholder field not required: {field}")
    for field in request.get("must_remain_false", []):
        require(field in request.get("required_fields", []), f"false field not required: {field}")
        require(request.get("forbidden_values", {}).get(field) is True, f"forbidden true value missing for {field}")

    decision = request.get("pre_execution_decision", {})
    for field in [
        "completed_receipt_recorded",
        "receipt_instance_valid",
        "can_open_real_measurement",
        "real_measurement_open",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(decision.get(field) is False, f"decision must keep {field}=false")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-HUMAN-FILL-REQUEST-20260623",
        "human_fill_request_ready_no_completed_receipt_recorded",
        "target_completed_receipt_path",
        "validate_headroom_lcx_real_measurement_external_receipt_intake.py",
        "completed_receipt_recorded | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_external_receipt_human_fill_request.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_real_measurement_external_receipt_human_fill_request.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_real_measurement_external_receipt_human_fill_request=pass "
        "status=human_fill_request_ready_no_completed_receipt_recorded "
        "completed_receipt_recorded=false real_measurement_open=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
