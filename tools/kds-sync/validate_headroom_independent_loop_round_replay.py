#!/usr/bin/env python3
"""Validate independent production-token-free Headroom LOOP replay evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_independent_loop_round_replay.py"
LOOP_OBSERVATION = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-20260621.json"


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
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    loop_observation = load_json(LOOP_OBSERVATION)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("runtime_observation_entries" in runner, "runner must recompute from runtime observation entries")
    require("series[\"windows\"][-1]" in runner, "runner must compare against series baseline")

    require(evidence.get("evidence_id") == "HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-20260621", "invalid evidence id")
    require(evidence.get("status") == "independent_production_token_free_loop_replay_ready", "invalid status")
    require(evidence.get("normalized_scope") == "metric_and_adapter_output_and_cost_evidence_only", "invalid normalized scope")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    aggregate = evidence.get("aggregate", {})
    observation_aggregate = loop_observation.get("aggregate", {})
    require(aggregate.get("runtime_entry_count") == 3, "runtime entry count mismatch")
    require(aggregate.get("runtime_tokens_before") == observation_aggregate.get("runtime_tokens_before"), "runtime tokens before mismatch")
    require(aggregate.get("runtime_tokens_after") == observation_aggregate.get("runtime_tokens_after"), "runtime tokens after mismatch")
    require(aggregate.get("runtime_tokens_saved") == observation_aggregate.get("runtime_tokens_saved"), "runtime tokens saved mismatch")
    require(aggregate.get("runtime_saving_rate") == observation_aggregate.get("runtime_saving_rate"), "runtime saving rate mismatch")
    require(aggregate.get("saving_rate_drift") <= aggregate.get("drift_gate_threshold", 0), "saving rate drift too high")
    require(aggregate.get("saving_rate_stability_gate") is True, "saving rate stability gate must pass")
    require(aggregate.get("blocked_scenarios_excluded") is True, "blocked scenarios must stay excluded")
    require(aggregate.get("production_tokens_used") is False, "production tokens must not be used")
    require(aggregate.get("production_admission_gate") is False, "production gate must stay false")
    require(evidence.get("decision", {}).get("independent_round_gate") is True, "independent round gate must pass")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must stay false")

    substantive = evidence.get("substantive_round", {})
    require(substantive.get("substantive_round_gate") is True, "substantive round gate must pass")
    require(sum(1 for key, value in substantive.items() if key != "substantive_round_gate" and value is True) >= 4, "not enough substantive round markers")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-20260621",
        "independent_round_gate | true",
        "saving_rate_stability_gate | true",
        "production_tokens_used | false",
        "production_admission_gate | false",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_independent_loop_round_replay.py" in loop_round, "loop round missing runner")
    require("validate_headroom_independent_loop_round_replay.py" in loop_round, "loop round missing validator")
    print(
        "headroom_independent_loop_round_replay=pass "
        f"runtime_entry_count={aggregate['runtime_entry_count']} "
        f"runtime_saving_rate={aggregate['runtime_saving_rate']} "
        f"saving_rate_drift={aggregate['saving_rate_drift']} "
        "independent_round_gate=true "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
