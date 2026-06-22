#!/usr/bin/env python3
"""Validate Headroom cost sensitivity model evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-COST-SENSITIVITY-MODEL-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_cost_sensitivity_model.py"


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
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")
    require(
        "last_reviewed: 2026-06-21" in metadata or "last_reviewed: 2026-06-22" in metadata,
        f"{path.relative_to(ROOT)} missing controlled marker: last_reviewed",
    )


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("PRICE_PROFILES" in runner, "runner must define price profiles")
    require(evidence.get("evidence_id") == "HEADROOM-COST-SENSITIVITY-MODEL-20260621", "invalid evidence id")
    require(evidence.get("status") == "cost_sensitivity_model_defined", "invalid status")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    profiles = evidence.get("profiles", [])
    require(len(profiles) == 3, "profile count mismatch")
    for profile in profiles:
        require(len(profile.get("measurements", [])) == 15, f"profile project count mismatch: {profile.get('profile_id')}")
        aggregate = profile.get("aggregate", {})
        require(aggregate.get("baseline_cost", 0) > aggregate.get("headroom_cost", 0), "headroom cost must be lower")
        require(aggregate.get("saving_rate", 0) >= aggregate.get("minimum_saving_rate", 0.2), "saving rate below threshold")
        require(aggregate.get("admission_gate") is True, "profile admission gate must pass")
        for row in profile.get("measurements", []):
            require(row.get("profile_admission_gate") is True, f"row gate failed: {profile.get('profile_id')} {row.get('project')}")
    gate = evidence.get("gate", {})
    require(gate.get("profile_count") == 3, "gate profile count mismatch")
    require(gate.get("project_count") == 15, "gate project count mismatch")
    require(gate.get("all_profiles_admission_gate") is True, "all profiles gate must pass")
    require(gate.get("min_profile_saving_rate", 0) >= 0.2, "minimum profile saving rate below threshold")
    require(gate.get("max_profile_saving_rate", 0) >= gate.get("min_profile_saving_rate", 0), "profile saving range invalid")
    require(gate.get("cost_sensitivity_gate") is True, "cost sensitivity gate must pass")
    require(gate.get("production_admission_gate") is False, "production admission must remain false")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-COST-SENSITIVITY-MODEL-20260621",
        "cost_sensitivity_gate | true",
        "profile_count | 3",
        "production_admission_gate | false",
        "measured_production_tokens | false",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_cost_sensitivity_model.py" in loop_round, "loop round missing runner")
    require("validate_headroom_cost_sensitivity_model.py" in loop_round, "loop round missing validator")
    print(
        "headroom_cost_sensitivity_model=pass "
        "profile_count=3 "
        f"min_saving_rate={gate['min_profile_saving_rate']} "
        f"max_saving_rate={gate['max_profile_saving_rate']} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
