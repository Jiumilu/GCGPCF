#!/usr/bin/env python3
"""Validate Headroom LCX session summary declaration boundary."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-session-summary-declaration-boundary-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-session-summary-declaration-boundary-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SESSION-SUMMARY-DECLARATION-BOUNDARY-001.md"

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

BLOCKED_CLAIMS = [
    "Headroom is accepted",
    "Headroom is integrated",
    "Headroom is production_ready",
    "production token savings have been measured",
    "production proxy is authorized or running",
    "real KDS API write has occurred",
    "WAES/Harness has admitted production measurement",
    "Headroom memory is a KDS fact source",
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
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "HEADROOM-LCX-SESSION-SUMMARY-DECLARATION-BOUNDARY-20260622", "invalid evidence id")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("projects") == PROJECTS, "project list mismatch")
    require(evidence.get("main_task_summary", {}).get("current_state") == "partial_controlled_not_production_ready", "invalid current state")
    for claim in BLOCKED_CLAIMS:
        require(claim in evidence.get("blocked_claims", []), f"missing blocked claim: {claim}")
    gates = evidence.get("gates", {})
    require(gates.get("declaration_boundary_gate") is True, "declaration boundary gate must be true")
    require(gates.get("session_summary_recorded") is True, "session summary must be recorded")
    require(gates.get("authorization_complete") is True, "authorization fields must be complete")
    require(evidence.get("open_authorization_fields") == [], "open authorization fields must be empty")
    require(evidence.get("current_blocker") == "production_token_measurement_allowed=false", "current blocker mismatch")
    require(gates.get("waes_harness_admitted") is True, "WAES/Harness admission must be true for sanitized precheck")
    for key in [
        "production_token_measurement_allowed",
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
        "HEADROOM-LCX-SESSION-SUMMARY-DECLARATION-BOUNDARY-20260622",
        "declaration_boundary_gate | true",
        "authorization_complete | true",
        "waes_harness_admitted | true",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_headroom_lcx_session_summary_declaration_boundary.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_session_summary_declaration_boundary=pass "
        "project_count=15 declaration_boundary_gate=true authorization_complete=true "
        "waes_harness_admitted=true production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
