#!/usr/bin/env python3
"""Validate Headroom LCX P1 proxy dry-run smoke evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_p1_proxy_dry_run_smoke.py"

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
    require("HEADROOM_TELEMETRY" in runner, "runner must force telemetry off")
    require("HEADROOM_PRODUCTION_PROXY" in runner, "runner must test production proxy refusal")
    require("llm_request_sent" in runner, "runner must record no LLM request")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    auth = evidence.get("authorization", {})
    require(auth.get("authorized_by_user") is True, "user authorization must be recorded")
    smoke = evidence.get("proxy_smoke", {})
    require(smoke.get("headroom_proxy_help_pass") is True, "proxy help must pass")
    require(smoke.get("production_refusal_pass") is True, "production refusal must pass")
    require(smoke.get("production_refusal_message_seen") is True, "production refusal message missing")
    require(smoke.get("dry_run_livez_pass") is True, "dry-run livez must pass")
    require(smoke.get("dry_run_livez_status") == 200, "dry-run livez status must be 200")
    require(smoke.get("dry_run_process_terminated") is True, "dry-run proxy process must terminate")
    gates = evidence.get("gates", {})
    for key in [
        "proxy_dry_run_gate",
        "headroom_proxy_help_pass",
        "production_proxy_refused",
        "dry_run_livez_pass",
        "process_terminated",
        "telemetry_default_off",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "production_proxy_started",
        "llm_request_sent",
        "external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "log_messages_enabled",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-20260621",
        "proxy_dry_run_gate | true",
        "production_proxy_refused | true",
        "dry_run_livez_pass | true",
        "llm_request_sent | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_p1_proxy_dry_run_smoke.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_p1_proxy_dry_run_smoke.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_p1_proxy_dry_run_smoke=pass "
        "project_count=15 proxy_dry_run_gate=true production_proxy_refused=true "
        "dry_run_livez_pass=true production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
