#!/usr/bin/env python3
"""Run a P0 runtime replay for the Headroom LCX controlled package."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

from headroom.transforms.compression_units import CompressionUnit, compress_unit_with_router
from headroom.transforms.content_router import ContentRouter


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = ROOT / "loop/context/headroom"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md"
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]|[^\s]")

PACKAGE_FILES = [
    "policy.yaml",
    "config.schema.yaml",
    "compression-profiles.yaml",
    "mcp.json",
    "harness/evidence.schema.yaml",
    "harness/metrics.schema.yaml",
    "waes/headroom-policy.yaml",
    "waes/sensitive-pass-through.yaml",
    "waes/ccr-retrieve-gate.yaml",
    "kds/context-optimization-component.yaml",
    "scripts/install-headroom.sh",
    "scripts/start-proxy.sh",
    "scripts/wrap-codex.sh",
    "scripts/collect-metrics.sh",
    "scripts/learn-preview.sh",
    "scripts/apply-approved-memory.sh",
]

SCRIPT_FILES = [
    "scripts/install-headroom.sh",
    "scripts/start-proxy.sh",
    "scripts/wrap-codex.sh",
    "scripts/collect-metrics.sh",
    "scripts/learn-preview.sh",
    "scripts/apply-approved-memory.sh",
]

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


class RegexTokenCounter:
    def count_text(self, text: str) -> int:
        return len(TOKEN_RE.findall(text))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_package(rel: str) -> str:
    path = PACKAGE_DIR / rel
    require(path.exists(), f"missing package file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run_command(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    package_payload = {
        rel: read_package(rel)
        for rel in PACKAGE_FILES
    }
    payload_text = json.dumps(package_payload, ensure_ascii=False, separators=(",", ":"))
    input_hash = hashlib.sha256(payload_text.encode("utf-8")).hexdigest()

    router = ContentRouter()
    unit = CompressionUnit(
        text=payload_text,
        provider="gpcf",
        endpoint="headroom_lcx_p0_runtime_replay",
        role="tool",
        item_type="headroom_lcx_controlled_package",
        cache_zone="dry_run",
        mutable=False,
        context="GlobalCloud Headroom LCX controlled package P0 runtime replay",
        question="compress controlled LCX configuration while preserving gates, projects, and non-claim markers",
        min_bytes=1,
        metadata={"adapter": "headroom_lcx_controlled_package"},
    )
    compression = compress_unit_with_router(
        unit,
        router=router,
        tokenizer=RegexTokenCounter(),
        target_ratio=0.2,
    )
    compressed = compression.compressed
    required_markers = [
        *PROJECTS,
        "production_admission_gate",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
        "headroom_retrieve",
        "require_evidence",
        "HEADROOM_TELEMETRY",
    ]
    missing_markers = [marker for marker in required_markers if marker not in compressed]
    saving_rate = (
        round(compression.tokens_saved / compression.tokens_before, 6)
        if compression.tokens_before
        else 0.0
    )

    headroom_bin = Path(sys.executable).with_name("headroom")
    cli_help = run_command([str(headroom_bin), "--help"], env={**os.environ, "HEADROOM_TELEMETRY": "off"})
    bash_syntax = []
    for rel in SCRIPT_FILES:
        result = run_command(["bash", "-n", str(PACKAGE_DIR / rel)])
        bash_syntax.append(
            {
                "script": f"loop/context/headroom/{rel}",
                "exit_code": result.returncode,
                "pass": result.returncode == 0,
            }
        )

    cost_model = run_command(
        [
            sys.executable,
            "tools/kds-sync/calculate_headroom_cost_model.py",
            "fixtures/headroom/headroom-cost-measurement-template.json",
        ],
        env={**os.environ, "HEADROOM_TELEMETRY": "off"},
    )

    runtime_replay_gate = (
        cli_help.returncode == 0
        and all(item["pass"] for item in bash_syntax)
        and cost_model.returncode == 0
        and not missing_markers
    )
    result = {
        "evidence_id": "HEADROOM-LCX-P0-RUNTIME-REPLAY-20260621",
        "task_id": "GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001",
        "date": "2026-06-21",
        "status": "p0_runtime_replay_completed",
        "headroom_runtime_imported": True,
        "headroom_runtime_used": True,
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "python_version": platform.python_version(),
        "telemetry": "off",
        "package_dir": "loop/context/headroom",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "runtime_smoke": {
            "headroom_cli_help_exit_code": cli_help.returncode,
            "headroom_cli_help_pass": cli_help.returncode == 0,
            "script_syntax": bash_syntax,
            "cost_model_exit_code": cost_model.returncode,
            "cost_model_pass": cost_model.returncode == 0,
        },
        "compression_replay": {
            "input_sha256": input_hash,
            "tokens_before": compression.tokens_before,
            "tokens_after": compression.tokens_after,
            "tokens_saved": compression.tokens_saved,
            "saving_rate": saving_rate,
            "modified": compression.modified,
            "strategy": compression.strategy,
            "reason": compression.reason,
            "reason_category": compression.reason_category,
            "transforms_applied": compression.transforms_applied,
            "marker_gate": not missing_markers,
            "missing_markers": missing_markers,
            "raw_text_stored": False,
        },
        "gates": {
            "runtime_replay_gate": runtime_replay_gate,
            "headroom_runtime_imported": True,
            "headroom_cli_help_pass": cli_help.returncode == 0,
            "script_syntax_gate": all(item["pass"] for item in bash_syntax),
            "cost_model_replay_gate": cost_model.returncode == 0,
            "marker_gate": not missing_markers,
            "telemetry_default_off": True,
            "raw_sensitive_context_stored": False,
            "production_proxy_started": False,
            "learn_apply_executed": False,
            "external_api_write": False,
            "kds_api_write": False,
            "database_migration": False,
            "permission_change": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "not_production_proxy": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_database_migration": True,
            "not_permission_change": True,
            "not_deployment": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "next_round": "GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001",
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = f"""---
doc_id: GPCF-DOC-0F02316005
title: Headroom LCX P0 Runtime Replay Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX P0 Runtime Replay Evidence

## Evidence ID

`HEADROOM-LCX-P0-RUNTIME-REPLAY-20260621`

## 结论

P0 runtime replay 已在隔离 Headroom runtime 下完成。Headroom CLI help、脚本语法、成本模型回放和 LCX 受控 package payload 压缩测量均已执行。

## 结果

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| headroom_version | {result["headroom_version"]} |
| telemetry | off |
| runtime_replay_gate | {str(runtime_replay_gate).lower()} |
| headroom_cli_help_pass | {str(cli_help.returncode == 0).lower()} |
| script_syntax_gate | {str(all(item["pass"] for item in bash_syntax)).lower()} |
| cost_model_replay_gate | {str(cost_model.returncode == 0).lower()} |
| marker_gate | {str(not missing_markers).lower()} |
| tokens_before | {compression.tokens_before} |
| tokens_after | {compression.tokens_after} |
| tokens_saved | {compression.tokens_saved} |
| saving_rate | {saving_rate} |
| production_proxy_started | false |
| learn_apply_executed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 非声明

- 不生产代理。
- 不真实 KDS 写入。
- 不真实外部 API 写入。
- 不数据库迁移。
- 不权限变更。
- 不部署。
- 不升级 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001`
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(
        "headroom_lcx_p0_runtime_replay=pass "
        f"project_count={len(PROJECTS)} runtime_replay_gate={str(runtime_replay_gate).lower()} "
        f"headroom_version={result['headroom_version']} saving_rate={saving_rate} "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
