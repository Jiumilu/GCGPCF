#!/usr/bin/env python3
"""Validate Headroom LCX P0 runtime replay evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_p0_runtime_replay.py"


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
    require("HEADROOM_TELEMETRY" in runner, "runner must enforce telemetry off")
    require("production_proxy_started" in runner, "runner must record production proxy non-action")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-P0-RUNTIME-REPLAY-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("headroom_runtime_imported") is True, "runtime must import")
    require(evidence.get("headroom_runtime_used") is True, "runtime must be used")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    smoke = evidence.get("runtime_smoke", {})
    require(smoke.get("headroom_cli_help_pass") is True, "headroom CLI help must pass")
    require(smoke.get("cost_model_pass") is True, "cost model replay must pass")
    require(all(item.get("pass") is True for item in smoke.get("script_syntax", [])), "all scripts must pass bash syntax")
    replay = evidence.get("compression_replay", {})
    require(replay.get("marker_gate") is True, "marker gate must pass")
    require(replay.get("raw_text_stored") is False, "raw text must not be stored")
    require(replay.get("tokens_before", 0) >= replay.get("tokens_after", 0), "tokens must not increase")
    gates = evidence.get("gates", {})
    for key in [
        "runtime_replay_gate",
        "headroom_runtime_imported",
        "headroom_cli_help_pass",
        "script_syntax_gate",
        "cost_model_replay_gate",
        "marker_gate",
        "telemetry_default_off",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "raw_sensitive_context_stored",
        "production_proxy_started",
        "learn_apply_executed",
        "external_api_write",
        "kds_api_write",
        "database_migration",
        "permission_change",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-P0-RUNTIME-REPLAY-20260621",
        "runtime_replay_gate | true",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_p0_runtime_replay.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_p0_runtime_replay.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_p0_runtime_replay=pass "
        "project_count=15 runtime_replay_gate=true "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
