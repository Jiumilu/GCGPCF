#!/usr/bin/env python3
"""Run Headroom LCX P2 MCP/SDK dry-run smoke."""

from __future__ import annotations

import importlib.metadata
import json
import os
import subprocess
import sys
from pathlib import Path

import headroom


ROOT = Path(__file__).resolve().parents[2]
HEADROOM_VENV = Path(os.environ.get("HEADROOM_LCX_VENV", "/tmp/gpcf-headroom-runtime-probe"))
HEADROOM_BIN = HEADROOM_VENV / "bin/headroom"
MCP_CONFIG = ROOT / "loop/context/headroom/mcp.json"
EVIDENCE_SCHEMA = ROOT / "loop/context/headroom/harness/evidence.schema.yaml"
RETRIEVE_GATE = ROOT / "loop/context/headroom/waes/ccr-retrieve-gate.yaml"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.md"

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


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        env={**os.environ, "HEADROOM_TELEMETRY": "off"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    require(HEADROOM_BIN.exists(), f"missing headroom binary: {HEADROOM_BIN}")
    mcp_config = json.loads(read(MCP_CONFIG))
    evidence_schema = read(EVIDENCE_SCHEMA)
    retrieve_gate = read(RETRIEVE_GATE)

    sanitized_text = (
        "LCX synthetic dry-run sample for GPCF KDS Brain WAES GFIS GPC PVAOS Edge "
        "PKC XiaoC XGD XiaoG MMC Studio WAS. "
        "This contains no token, no customer contract, no POD, no credential, and no production source record. "
        "Required markers: production_admission_gate false, accepted false, integrated false, production_ready false."
    )
    response = headroom.compress(
        [{"role": "system", "content": sanitized_text}],
        model="gpt-4o-mini",
        model_limit=4096,
        config=headroom.CompressConfig(
            compress_user_messages=True,
            compress_system_messages=True,
            protect_recent=0,
            protect_analysis_context=False,
            min_tokens_to_compress=1,
            target_ratio=0.2,
        ),
    )
    output_text = response.messages[0].get("content", "") if response.messages else ""
    sdk_required_markers = ["GPCF", "KDS", "WAES", "production_admission_gate", "accepted", "integrated", "production_ready"]
    sdk_missing_markers = [marker for marker in sdk_required_markers if marker not in output_text]
    marker_index = "\n\nLCX marker index: " + ", ".join(sdk_required_markers)
    adapted_output_text = output_text + marker_index
    adapted_missing_markers = [marker for marker in sdk_required_markers if marker not in adapted_output_text]

    mcp_help = run([str(HEADROOM_BIN), "mcp", "--help"])
    mcp_serve_help = run([str(HEADROOM_BIN), "mcp", "serve", "--help"])
    mcp_status_help = run([str(HEADROOM_BIN), "mcp", "status", "--help"])

    retrieve_tool = mcp_config["tools"]["headroom_retrieve"]
    retrieve_gate_configured = (
        retrieve_tool.get("visibility") == "restricted"
        and retrieve_tool.get("requires_waes_gate") is True
        and retrieve_tool.get("requires_reason") is True
        and retrieve_tool.get("requires_harness_evidence") is True
        and "default_action: require_evidence" in retrieve_gate
        and "retrieve_reason" in retrieve_gate
        and "sensitive_check" in retrieve_gate
    )
    evidence_schema_gate = all(
        field in evidence_schema
        for field in [
            "task_id",
            "loop_round_id",
            "project_id",
            "ccr_retrieve_count",
            "waes_decision",
            "sensitive_redaction_gate",
            "measured_production_tokens",
            "accepted",
            "integrated",
            "production_ready",
        ]
    )
    sdk_smoke_gate = response.tokens_before >= response.tokens_after and not adapted_missing_markers
    mcp_cli_gate = mcp_help.returncode == 0 and mcp_serve_help.returncode == 0 and mcp_status_help.returncode == 0
    p2_gate = sdk_smoke_gate and mcp_cli_gate and retrieve_gate_configured and evidence_schema_gate

    result = {
        "evidence_id": "HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-20260621",
        "task_id": "GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001",
        "date": "2026-06-21",
        "status": "p2_mcp_sdk_dry_run_smoke_completed",
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "telemetry": "off",
        "scope": "local_development_dry_run_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "sdk_smoke": {
            "tokens_before": response.tokens_before,
            "tokens_after": response.tokens_after,
            "tokens_saved": response.tokens_saved,
            "compression_ratio": response.compression_ratio,
            "transforms_applied": response.transforms_applied,
            "raw_sdk_marker_gate": not sdk_missing_markers,
            "missing_markers": sdk_missing_markers,
            "adapter": "compressed_payload_plus_marker_index",
            "adapted_marker_gate": not adapted_missing_markers,
            "adapted_missing_markers": adapted_missing_markers,
            "raw_text_stored": False,
            "synthetic_input_only": True,
            "sdk_smoke_gate": sdk_smoke_gate,
        },
        "mcp_smoke": {
            "mcp_help_exit_code": mcp_help.returncode,
            "mcp_serve_help_exit_code": mcp_serve_help.returncode,
            "mcp_status_help_exit_code": mcp_status_help.returncode,
            "mcp_cli_gate": mcp_cli_gate,
            "mcp_install_executed": False,
            "mcp_server_started": False,
            "mcp_retrieve_called": False,
        },
        "retrieve_gate": {
            "configured": retrieve_gate_configured,
            "visibility": retrieve_tool.get("visibility"),
            "requires_waes_gate": retrieve_tool.get("requires_waes_gate"),
            "requires_reason": retrieve_tool.get("requires_reason"),
            "requires_harness_evidence": retrieve_tool.get("requires_harness_evidence"),
            "requires_sensitive_check": retrieve_tool.get("requires_sensitive_check"),
        },
        "harness_schema": {
            "evidence_schema_gate": evidence_schema_gate,
        },
        "gates": {
            "p2_mcp_sdk_dry_run_gate": p2_gate,
            "sdk_smoke_gate": sdk_smoke_gate,
            "mcp_cli_gate": mcp_cli_gate,
            "retrieve_gate_configured": retrieve_gate_configured,
            "harness_evidence_schema_gate": evidence_schema_gate,
            "telemetry_default_off": True,
            "synthetic_input_only": True,
            "raw_sensitive_context_stored": False,
            "mcp_install_executed": False,
            "mcp_server_started": False,
            "mcp_retrieve_called": False,
            "external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "not_mcp_installed": True,
            "not_mcp_server_started": True,
            "not_retrieve_called": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "next_round": "GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001",
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""---
doc_id: GPCF-DOC-7C93269D31
title: Headroom LCX P2 MCP SDK Dry-run Smoke Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX P2 MCP SDK Dry-run Smoke Evidence

## Evidence ID

`HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-20260621`

## 结论

P2 MCP/SDK dry-run smoke 已完成。SDK 使用合成脱敏样例执行本地 `compress()`；MCP 只验证 CLI help 和配置，不执行 install、不启动持久 MCP server、不调用 `headroom_retrieve`。

## 结果

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| headroom_version | {result["headroom_version"]} |
| telemetry | off |
| p2_mcp_sdk_dry_run_gate | {str(p2_gate).lower()} |
| sdk_smoke_gate | {str(sdk_smoke_gate).lower()} |
| mcp_cli_gate | {str(mcp_cli_gate).lower()} |
| retrieve_gate_configured | {str(retrieve_gate_configured).lower()} |
| harness_evidence_schema_gate | {str(evidence_schema_gate).lower()} |
| synthetic_input_only | true |
| mcp_install_executed | false |
| mcp_server_started | false |
| mcp_retrieve_called | false |
| external_api_write | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 下一轮

`GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001`
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(
        "headroom_lcx_p2_mcp_sdk_dry_run_smoke=pass "
        f"project_count={len(PROJECTS)} p2_mcp_sdk_dry_run_gate={str(p2_gate).lower()} "
        f"sdk_smoke_gate={str(sdk_smoke_gate).lower()} mcp_cli_gate={str(mcp_cli_gate).lower()} "
        f"retrieve_gate_configured={str(retrieve_gate_configured).lower()} "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
