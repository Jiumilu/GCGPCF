#!/usr/bin/env python3
"""Validate Headroom LCX fixture stability gate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-STABILITY-GATE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_fixture_stability_gate.py"


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

    require(evidence.get("evidence_id") == "HEADROOM-LCX-FIXTURE-STABILITY-GATE-20260622", "invalid evidence id")
    require(evidence.get("status") == "fixture_stability_gate_pass_no_measurement", "invalid status")
    require(evidence.get("scope") == "sanitized_fixture_metadata_stability_only", "invalid scope")
    require(evidence.get("round_count") == 3, "round count mismatch")
    require(evidence.get("project_count") == 5, "project count mismatch")
    require(evidence.get("scenario_count") == 3, "scenario count mismatch")
    require(evidence.get("entry_count") == 15, "entry count mismatch")
    require(evidence.get("stable_hash_count") == 1, "stable hash count mismatch")
    require(evidence.get("failures") == [], "failures must be empty")
    require(evidence.get("calculation", {}).get("saving_rate") == "not_calculated", "saving rate must not be calculated")
    require(evidence.get("calculation", {}).get("tokens_saved") == "not_calculated", "tokens saved must not be calculated")
    rounds = evidence.get("rounds", [])
    require(isinstance(rounds, list) and len(rounds) == 3, "rounds mismatch")
    hashes = {round_item.get("stable_hash") for round_item in rounds}
    require(len(hashes) == 1 and next(iter(hashes)), "round hashes must be stable")
    for round_item in rounds:
        require(round_item.get("entry_count") == 15, "round entry count mismatch")
        require(len(round_item.get("record_keys", [])) == 15, "round record key count mismatch")
        forbidden = round_item.get("forbidden_claims", {})
        for key, value in forbidden.items():
            require(value is False, f"forbidden claim must be false: {key}")

    gates = evidence.get("gates", {})
    for key in [
        "fixture_stability_gate",
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
        "HEADROOM-LCX-FIXTURE-STABILITY-GATE-20260622",
        "fixture_stability_gate | true",
        "multi_round_stability_gate | true",
        "metadata_only | true",
        "saving_rate | not_calculated",
        "tokens_saved | not_calculated",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_fixture_stability_gate.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_fixture_stability_gate.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_fixture_stability_gate=pass_check_only "
        "round_count=3 project_count=5 scenario_count=3 entry_count=15 "
        "stable_hash_count=1 metadata_only=true saving_rate=not_calculated "
        "measured_production_tokens=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
