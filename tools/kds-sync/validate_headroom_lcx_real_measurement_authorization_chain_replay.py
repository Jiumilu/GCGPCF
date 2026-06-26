#!/usr/bin/env python3
"""Validate Headroom LCX real-measurement authorization chain replay evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_authorization_chain_replay.py"

LEDGER_REF = "docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json"


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
    replay = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_chain_replay" in builder, "builder must build chain replay")
    require(replay.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-20260623", "invalid evidence id")
    require(replay.get("status") == "authorization_chain_replayed_precheck_only", "invalid status")
    require(replay.get("project_count") == 15, "project count mismatch")
    require(replay.get("ledger_reference") == LEDGER_REF, "ledger reference mismatch")

    chain = replay.get("chain", [])
    require(isinstance(chain, list) and len(chain) == 5, "chain must contain five steps")
    require({item.get("ledger_reference") for item in chain} == {LEDGER_REF}, "ledger references must match")
    require(
        [item.get("step") for item in chain]
        == [
            "authorization_request",
            "authorization_field_map",
            "approval_signed_bundle",
            "authorization_window_grant",
            "sanitized_usage_ledger",
        ],
        "chain step order mismatch",
    )

    gate = replay.get("chain_gate", {})
    require(gate.get("same_ledger_reference") is True, "same ledger gate must be true")
    for key in [
        "real_measurement_open",
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gate.get(key) is False, f"gate must remain false: {key}")

    for item in chain:
        state = item.get("state", {})
        for key in ["accepted", "integrated", "production_ready"]:
            if key in state:
                require(state[key] is False, f"{item.get('step')} must keep {key}=false")
        if "production_token_measurement_allowed" in state:
            require(state["production_token_measurement_allowed"] is False, f"{item.get('step')} must keep production measurement false")
        if "measured_production_tokens" in state:
            require(state["measured_production_tokens"] is False, f"{item.get('step')} must keep measured tokens false")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-20260623",
        "authorization_chain_replayed_precheck_only",
        "same_ledger_reference | `true`",
        "real_measurement_open | `false`",
        "production_token_measurement_allowed | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_authorization_chain_replay.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_real_measurement_authorization_chain_replay.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_real_measurement_authorization_chain_replay=pass "
        "project_count=15 same_ledger_reference=true real_measurement_open=false "
        "production_token_measurement_allowed=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
