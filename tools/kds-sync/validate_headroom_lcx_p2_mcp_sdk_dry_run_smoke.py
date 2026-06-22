#!/usr/bin/env python3
"""Validate Headroom LCX P2 MCP/SDK dry-run smoke evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py"

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
    require("headroom.compress" in runner, "runner must execute SDK compress")
    require("headroom_retrieve" in runner, "runner must inspect retrieve gate")
    require("mcp_install_executed" in runner, "runner must record no MCP install")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    sdk = evidence.get("sdk_smoke", {})
    require(sdk.get("sdk_smoke_gate") is True, "SDK smoke gate must pass")
    require(sdk.get("adapter") == "compressed_payload_plus_marker_index", "SDK smoke must use marker-preserving adapter")
    require(sdk.get("adapted_marker_gate") is True, "adapted SDK marker gate must pass")
    require(sdk.get("synthetic_input_only") is True, "SDK input must be synthetic")
    require(sdk.get("raw_text_stored") is False, "raw text must not be stored")
    mcp = evidence.get("mcp_smoke", {})
    require(mcp.get("mcp_cli_gate") is True, "MCP CLI gate must pass")
    require(mcp.get("mcp_install_executed") is False, "MCP install must not execute")
    require(mcp.get("mcp_server_started") is False, "MCP server must not start")
    require(mcp.get("mcp_retrieve_called") is False, "MCP retrieve must not be called")
    retrieve = evidence.get("retrieve_gate", {})
    require(retrieve.get("configured") is True, "retrieve gate must be configured")
    require(retrieve.get("visibility") == "restricted", "retrieve visibility must be restricted")
    require(retrieve.get("requires_waes_gate") is True, "retrieve must require WAES gate")
    require(retrieve.get("requires_reason") is True, "retrieve must require reason")
    gates = evidence.get("gates", {})
    for key in [
        "p2_mcp_sdk_dry_run_gate",
        "sdk_smoke_gate",
        "mcp_cli_gate",
        "retrieve_gate_configured",
        "harness_evidence_schema_gate",
        "telemetry_default_off",
        "synthetic_input_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "raw_sensitive_context_stored",
        "mcp_install_executed",
        "mcp_server_started",
        "mcp_retrieve_called",
        "external_api_write",
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
        "HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-20260621",
        "p2_mcp_sdk_dry_run_gate | true",
        "sdk_smoke_gate | true",
        "mcp_cli_gate | true",
        "retrieve_gate_configured | true",
        "mcp_retrieve_called | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_p2_mcp_sdk_dry_run_smoke=pass "
        "project_count=15 p2_mcp_sdk_dry_run_gate=true sdk_smoke_gate=true "
        "mcp_cli_gate=true retrieve_gate_configured=true "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
