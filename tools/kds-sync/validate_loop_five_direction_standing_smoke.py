#!/usr/bin/env python3
"""Validate five-direction standing adoption on a non-RUN-001 Loop target."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-LOOP-FIVE-DIRECTION-STANDING-SMOKE-001.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-five-direction-standing-smoke-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-five-direction-standing-smoke-20260622.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_loop_five_direction_standing_smoke: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_controlled(text: str, source_path: str) -> None:
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{source_path} missing controlled marker: {phrase}")


def main() -> int:
    round_text = read(ROUND)
    evidence_md = read(EVIDENCE_MD)
    evidence = load_json(EVIDENCE_JSON)

    require_controlled(round_text, "docs/harness/loops/loop-round-GPCF-LOOP-FIVE-DIRECTION-STANDING-SMOKE-001.md")
    require_controlled(evidence_md, "docs/harness/evidence/loop-five-direction-standing-smoke-20260622.md")

    for phrase in [
        "GPCF-LOOP-FIVE-DIRECTION-STANDING-SMOKE-001",
        "GFIS-runtime-gap-resolution-plan",
        "## run",
        "## stop",
        "## verify",
        "## recover",
        "## debug",
        "authorization_boundary",
        "real_business_lane=repair_required",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
    ]:
        require(phrase in round_text, f"round missing phrase: {phrase}")

    require(evidence.get("round_id") == "GPCF-LOOP-FIVE-DIRECTION-STANDING-SMOKE-001", "wrong round_id")
    require(evidence.get("test_target") == "GFIS-runtime-gap-resolution-plan", "wrong test target")
    require(evidence.get("scope") == "no-write", "scope must be no-write")
    require(evidence.get("started") is True, "smoke must start")
    require(evidence.get("completed_for_round") is True, "smoke must complete")
    require(evidence.get("stop_type") == "authorization_boundary", "stop_type must be authorization_boundary")

    directions = evidence.get("directions", {})
    for key in ["run", "stop", "verify", "recover", "debug"]:
        require(directions.get(key, {}).get("implemented") is True, f"direction not implemented: {key}")

    real_lane_counts = evidence.get("real_lane_counts", {})
    for key in ["valid_source_records", "runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]:
        require(real_lane_counts.get(key) == 0, f"real lane count must remain zero: {key}")

    write_counts = evidence.get("write_counts", {})
    for key in ["production_writes", "real_external_api_writes", "kds_fact_writes", "waes_gate_result_writes"]:
        require(write_counts.get(key) == 0, f"write count must remain zero: {key}")

    guards = evidence.get("completion_guards", {})
    for key in ["accepted", "integrated", "production_ready"]:
        require(guards.get(key) is False, f"completion guard must be false: {key}")
    require(guards.get("no_write_boundary_enforced") is True, "no-write boundary must be enforced")
    require(evidence.get("next_authorization_required") is True, "next authorization must be required")

    for phrase in [
        "five_direction_standing_smoke=pass",
        "非 RUN-001 工作 | `pass`",
        "no-write boundary | `enforced`",
        "real_business_lane | `repair_required`",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")

    print(
        "five_direction_standing_smoke=pass "
        "target=GFIS-runtime-gap-resolution-plan scope=no-write "
        "run=implemented stop=implemented verify=implemented recover=implemented debug=implemented "
        "real_business_lane=repair_required accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
