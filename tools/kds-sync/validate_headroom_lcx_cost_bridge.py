#!/usr/bin/env python3
"""Validate the Headroom LCX cost bridge evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-cost-bridge-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-cost-bridge-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COST-BRIDGE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_cost_bridge.py"


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
    bridge = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    runner = read(RUNNER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_bridge" in runner, "runner must build cost bridge")

    require(bridge.get("evidence_id") == "HEADROOM-LCX-COST-BRIDGE-20260623", "invalid evidence id")
    require(bridge.get("status") == "cost_bridge_defined_replay_only", "invalid status")
    require(bridge.get("project_count") == 15, "project count mismatch")
    require(bridge.get("bridge_mode") == "replay_only", "bridge mode must remain replay only")

    current_state = bridge.get("current_state", {})
    require(current_state.get("cost_sensitivity_gate") is True, "cost sensitivity gate must pass")
    require(current_state.get("series_gate") is True, "series gate must pass")
    require(current_state.get("independent_round_gate") is True, "independent replay gate must pass")
    require(current_state.get("metadata_replay_gate") is True, "metadata replay gate must pass")
    require(current_state.get("production_token_measurement_allowed") is False, "token measurement must remain false")
    require(current_state.get("measured_production_tokens") is False, "measured tokens must remain false")
    require(current_state.get("production_admission_gate") is False, "production admission gate must remain false")
    require(current_state.get("accepted") is False, "accepted must remain false")
    require(current_state.get("integrated") is False, "integrated must remain false")
    require(current_state.get("production_ready") is False, "production ready must remain false")

    for phrase in [
        "HEADROOM-LCX-COST-BRIDGE-20260623",
        "cost_bridge_defined_replay_only",
        "replay_only",
        "production_token_measurement_allowed | `false`",
        "measured_production_tokens | `false`",
        "production_admission_gate | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"md missing phrase: {phrase}")

    for phrase in [
        "cost bridge",
        "build_headroom_lcx_cost_bridge.py",
        "validate_headroom_lcx_cost_bridge.py",
        "replay only 成本桥接层",
        "不产生真实生产 token 结论",
    ]:
        require(phrase in loop, f"loop missing phrase: {phrase}")

    print(
        "headroom_lcx_cost_bridge=pass "
        "project_count=15 bridge_mode=replay_only "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
