#!/usr/bin/env python3
"""Validate WAES/Harness final receipt decision human fill request for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_human_fill_request.py"


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
    require("build_request" in builder, "builder must build request")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-20260623", "invalid evidence id")
    require(evidence.get("status") == "waes_harness_final_receipt_decision_human_fill_request_ready", "invalid status")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require("decision_maker" in evidence.get("must_replace_required_placeholders", []), "decision_maker must be required")
    require("decision_value" in evidence.get("must_replace_required_placeholders", []), "decision_value must be required")
    require("admitted_for_next_precheck_only" in evidence.get("allowed_decision_values", []), "allowed admit decision missing")
    require("rejected_requires_rework" in evidence.get("allowed_decision_values", []), "allowed reject decision missing")

    for field in evidence.get("must_remain_false", []):
        require(field in evidence.get("required_fields", []), f"false field not in required fields: {field}")

    commands = set(evidence.get("verification_commands_after_fill", []))
    for command in [
        "python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_response_template.py",
        "python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_request.py",
        "python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_intake.py",
        "python3 tools/kds-sync/check_document_pollution.py",
        "python3 tools/kds-sync/validate_kds_token.py",
    ]:
        require(command in commands, f"missing verification command: {command}")

    decision = evidence.get("pre_execution_decision", {})
    for field in [
        "waes_harness_final_decision_recorded",
        "can_open_real_measurement",
        "real_measurement_open",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(decision.get(field) is False, f"decision must keep {field}=false")

    for phrase in [
        "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-HUMAN-FILL-REQUEST-20260623",
        "waes_harness_final_receipt_decision_human_fill_request_ready",
        "decision_maker",
        "real_measurement_open | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_waes_harness_final_receipt_decision_human_fill_request.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_waes_harness_final_receipt_decision_human_fill_request.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_waes_harness_final_receipt_decision_human_fill_request=pass "
        "status=waes_harness_final_receipt_decision_human_fill_request_ready "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
