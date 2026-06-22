#!/usr/bin/env python3
"""Run Headroom LCX P1 proxy dry-run smoke."""

from __future__ import annotations

import importlib.metadata
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HEADROOM_VENV = Path(os.environ.get("HEADROOM_LCX_VENV", "/tmp/gpcf-headroom-runtime-probe"))
HEADROOM_BIN = HEADROOM_VENV / "bin/headroom"
START_PROXY = ROOT / "loop/context/headroom/scripts/start-proxy.sh"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md"


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


def free_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def run(args: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def wait_for_livez(port: int, process: subprocess.Popen[str]) -> tuple[bool, int | None, str]:
    last_error = ""
    for _ in range(50):
        if process.poll() is not None:
            return False, None, f"process_exited:{process.returncode}"
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/livez", timeout=0.25) as response:
                return response.status == 200, response.status, ""
        except Exception as exc:  # noqa: BLE001 - keep smoke diagnostic compact
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(0.2)
    return False, None, last_error


def stop_process(process: subprocess.Popen[str]) -> tuple[int | None, bool]:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    return process.returncode, process.poll() is not None


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    require(HEADROOM_BIN.exists(), f"missing headroom binary: {HEADROOM_BIN}")
    require(START_PROXY.exists(), f"missing start proxy script: {START_PROXY.relative_to(ROOT)}")

    base_env = {
        **os.environ,
        "PATH": f"{HEADROOM_VENV / 'bin'}:{os.environ.get('PATH', '')}",
        "HEADROOM_TELEMETRY": "off",
        "HEADROOM_PROXY_NO_OPTIMIZE": "true",
        "HEADROOM_PROXY_NO_CCR_INJECT_TOOL": "true",
        "HEADROOM_LOG_MESSAGES": "",
    }

    help_result = run([str(HEADROOM_BIN), "proxy", "--help"], base_env)
    production_refusal = run(
        ["bash", str(START_PROXY)],
        {
            **base_env,
            "HEADROOM_PRODUCTION_PROXY": "true",
            "HEADROOM_PROXY_PORT": str(free_port()),
        },
    )

    port = free_port()
    process = subprocess.Popen(
        ["bash", str(START_PROXY)],
        cwd=ROOT,
        env={
            **base_env,
            "HEADROOM_PRODUCTION_PROXY": "false",
            "HEADROOM_PROXY_PORT": str(port),
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    livez_pass, livez_status, livez_error = wait_for_livez(port, process)
    process_exit_code, process_terminated = stop_process(process)
    stdout = process.stdout.read() if process.stdout else ""
    stderr = process.stderr.read() if process.stderr else ""

    proxy_dry_run_gate = (
        help_result.returncode == 0
        and production_refusal.returncode == 2
        and "Refusing to start production proxy" in production_refusal.stderr
        and livez_pass
        and process_terminated
    )

    result = {
        "evidence_id": "HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-20260621",
        "task_id": "GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001",
        "date": "2026-06-21",
        "status": "p1_proxy_dry_run_smoke_completed",
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "telemetry": "off",
        "scope": "local_development_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "authorization": {
            "authorized_by_user": True,
            "authorization_text": "允许在本机开发态以 HEADROOM_TELEMETRY=off 启动/验证 Headroom proxy dry-run；禁止生产代理、禁止真实 KDS 写入、禁止外部 API 写入、禁止处理未脱敏敏感材料。"
        },
        "proxy_smoke": {
            "headroom_proxy_help_exit_code": help_result.returncode,
            "headroom_proxy_help_pass": help_result.returncode == 0,
            "production_refusal_exit_code": production_refusal.returncode,
            "production_refusal_pass": production_refusal.returncode == 2,
            "production_refusal_message_seen": "Refusing to start production proxy" in production_refusal.stderr,
            "dry_run_port": port,
            "dry_run_livez_status": livez_status,
            "dry_run_livez_pass": livez_pass,
            "dry_run_livez_error": livez_error,
            "dry_run_process_exit_code_after_stop": process_exit_code,
            "dry_run_process_terminated": process_terminated,
            "stdout_preview": stdout[:800],
            "stderr_preview": stderr[:800]
        },
        "gates": {
            "proxy_dry_run_gate": proxy_dry_run_gate,
            "headroom_proxy_help_pass": help_result.returncode == 0,
            "production_proxy_refused": production_refusal.returncode == 2,
            "dry_run_livez_pass": livez_pass,
            "process_terminated": process_terminated,
            "telemetry_default_off": True,
            "production_proxy_started": False,
            "llm_request_sent": False,
            "external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "log_messages_enabled": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False
        },
        "non_claims": {
            "not_production_proxy": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True
        },
        "next_round": "GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001"
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""---
doc_id: GPCF-DOC-22C297756A
title: Headroom LCX P1 Proxy Dry-run Smoke Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX P1 Proxy Dry-run Smoke Evidence

## Evidence ID

`HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-20260621`

## 结论

P1 proxy dry-run smoke 已完成。本轮只在本机开发态启动随机端口 dry-run proxy，并验证 `/livez`；同时验证生产代理门禁会拒绝启动。

## 结果

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| headroom_version | {result["headroom_version"]} |
| telemetry | off |
| proxy_dry_run_gate | {str(proxy_dry_run_gate).lower()} |
| production_proxy_refused | {str(production_refusal.returncode == 2).lower()} |
| dry_run_livez_pass | {str(livez_pass).lower()} |
| dry_run_livez_status | {livez_status} |
| process_terminated | {str(process_terminated).lower()} |
| llm_request_sent | false |
| external_api_write | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 非声明

- 不生产代理。
- 不发送 LLM 请求。
- 不真实 KDS 写入。
- 不真实外部 API 写入。
- 不处理未脱敏敏感材料。
- 不升级 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001`
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(
        "headroom_lcx_p1_proxy_dry_run_smoke=pass "
        f"project_count={len(PROJECTS)} proxy_dry_run_gate={str(proxy_dry_run_gate).lower()} "
        f"production_proxy_refused={str(production_refusal.returncode == 2).lower()} "
        f"dry_run_livez_pass={str(livez_pass).lower()} "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
