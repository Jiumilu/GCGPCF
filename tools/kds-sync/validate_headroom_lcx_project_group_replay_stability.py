#!/usr/bin/env python3
"""Validate 15-project Headroom LCX replay/comparison/stability evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_project_group_replay_stability.py"

PROJECTS = {
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
}
SCENARIOS = {"loop_gate_metadata", "retrieval_context_metadata", "tool_output_metadata"}


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
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("--check-only is required" in runner, "runner must require --check-only")
    require("canonical_hash" in runner, "runner must define canonical hash")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-20260622", "invalid evidence id")
    require(evidence.get("status") == "project_group_replay_stability_pass_no_measurement", "invalid status")
    require(evidence.get("round_count") == 3, "round count mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("scenario_count") == 3, "scenario count mismatch")
    require(evidence.get("entry_count") == 45, "entry count mismatch")
    require(evidence.get("replay_record_count") == 45, "replay count mismatch")
    require(evidence.get("comparison_count") == 45, "comparison count mismatch")
    require(evidence.get("stable_hash_count") == 1, "stable hash count mismatch")
    require(evidence.get("failures") == [], "failures must be empty")
    require(evidence.get("calculation", {}).get("saving_rate") == "not_calculated", "saving rate must not be calculated")
    rounds = evidence.get("rounds", [])
    require(isinstance(rounds, list) and len(rounds) == 3, "rounds mismatch")
    hashes = {item.get("stable_hash") for item in rounds}
    require(len(hashes) == 1 and next(iter(hashes)), "round hashes must be stable")
    for round_item in rounds:
        require(round_item.get("entry_count") == 45, "round entry count mismatch")
        require({item.get("project_id") for item in round_item.get("records", [])} == PROJECTS, "round project coverage mismatch")
        require({item.get("content_type") for item in round_item.get("records", [])} == SCENARIOS, "round scenario coverage mismatch")
        for comparison in round_item.get("comparisons", []):
            for key in [
                "marker_gate_preserved",
                "answer_equivalence_unmeasured",
                "sensitive_redaction_gate_pass",
                "ccr_retrieval_miss_count_within_fixture_threshold",
            ]:
                require(comparison.get(key) is True, f"comparison gate must be true: {key}")
    gates = evidence.get("gates", {})
    for key in [
        "project_group_replay_stability_gate",
        "metadata_replay_gate",
        "marker_retrieval_miss_comparison_gate",
        "multi_round_stability_gate",
        "project_coverage_gate",
        "scenario_coverage_gate",
        "entry_count_gate",
        "metadata_only",
        "check_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-20260622",
        "project_group_replay_stability_gate | true",
        "multi_round_stability_gate | true",
        "metadata_only | true",
        "saving_rate | not_calculated",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_project_group_replay_stability.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_project_group_replay_stability.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_project_group_replay_stability=pass_check_only "
        "round_count=3 project_count=15 scenario_count=3 entry_count=45 stable_hash_count=1 "
        "metadata_only=true saving_rate=not_calculated measured_production_tokens=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
