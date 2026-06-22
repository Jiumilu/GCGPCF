#!/usr/bin/env python3
"""Validate Headroom LCX authorization boundary review evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_authorization_boundary_review.py"


PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
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
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("AUTHORIZATION_SIGNAL" in runner, "runner must record authorization signal")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    review = evidence.get("authorization_review", {})
    require(review.get("authorization_signal_present") is True, "authorization signal must be present")
    require(review.get("authorization_complete") is False, "authorization must remain incomplete")
    require(review.get("missing_required_field_count") == 6, "missing field count must be 6")
    require(review.get("production_admission_gate") is False, "production admission must remain false")
    gates = evidence.get("gates", {})
    for key in ["authorization_boundary_review_gate", "authorization_signal_present"]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "authorization_complete",
        "authorized_window_present",
        "authorized_by_present",
        "authorized_at_present",
        "sanitized_production_token_ledger_present",
        "rollback_plan_present",
        "waes_harness_admission_decision_present",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-AUTHORIZATION-BOUNDARY-REVIEW-20260621",
        "authorization_signal_present | true",
        "authorization_complete | false",
        "missing_required_field_count | 6",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_authorization_boundary_review.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_authorization_boundary_review.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_authorization_boundary_review=pass "
        "project_count=15 authorization_signal_present=true authorization_complete=false "
        "missing_required_field_count=6 production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
