#!/usr/bin/env python3
"""Validate WAES/Harness final receipt decision fill recommendation for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-fill-recommendation-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-fill-recommendation-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_fill_recommendation.py"
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-waes-harness-final-receipt-decision.response.recommended.json"


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
    fixture = load_json(FIXTURE)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_recommendation" in builder, "builder must build recommendation")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-20260623", "invalid evidence id")
    require(evidence.get("status") == "fill_recommendation_ready_not_formal_decision", "invalid status")
    require(evidence.get("recommended_response") == fixture, "fixture must match recommended response")
    require(fixture.get("decision_value") == "admitted_for_next_precheck_only", "recommended decision should stay next precheck only")
    require(fixture.get("can_open_real_measurement") is False, "recommendation must not open measurement")
    require(fixture.get("accepted") is False, "recommendation must keep accepted false")
    require("confirm" in fixture.get("decision_maker", ""), "decision maker must remain confirmation placeholder")

    boundary = evidence.get("recommendation_boundary", {})
    for field in [
        "recommendation_only",
        "not_formal_response",
        "requires_waes_harness_confirmation",
    ]:
        require(boundary.get(field) is True, f"boundary must keep {field}=true")
    for field in [
        "can_open_real_measurement",
        "real_measurement_open",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(boundary.get(field) is False, f"boundary must keep {field}=false")

    for phrase in [
        "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-20260623",
        "fill_recommendation_ready_not_formal_decision",
        "recommendation_only | `true`",
        "real_measurement_open | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_waes_harness_final_receipt_decision_fill_recommendation.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_waes_harness_final_receipt_decision_fill_recommendation.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_waes_harness_final_receipt_decision_fill_recommendation=pass "
        "status=fill_recommendation_ready_not_formal_decision "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
