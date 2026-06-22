#!/usr/bin/env python3
"""Validate the P2 gate replay evidence for WAS/Ontology."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

EVIDENCE_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p2-gate-replay-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/ontology-was-3h-p2-gate-replay-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-3H-P2-GATE-REPLAY-001.md"
PLAN_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-implementation-goals-20260621.json"
P1_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p1-source-record-readiness-20260621.json"

ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]

REQUIRED_GATES = [
    "ontology_was_3h_p0_start",
    "ontology_was_3h_p1_source_record_readiness",
    "gfis_was_source_record_submission_precheck",
    "gfis_was_source_record_negative_fixtures",
    "gfis_was_source_record_field_crosswalk",
    "gfis_was_source_record_admission_gate",
    "gfis_was_profile_runtime_gate_mapping",
    "was_project_group_admission",
    "was_okf_validators",
]

REQUIRED_OKF_VALIDATORS = [
    "validate_was_dimensions",
    "validate_was_flows",
    "validate_was_object_contract",
    "validate_was_relationship_contract",
    "validate_was_event_contract",
    "validate_was_loop_record",
    "validate_was_rag_admission",
    "validate_was_waes_gate_input",
    "validate_was_pool_link",
    "validate_no_illegal_promotion",
    "validate_no_stale_bundle",
    "validate_gfis_runtime_sop_e2e_profile",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(read(path))
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


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
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    plan = load_json(PLAN_JSON)
    p1 = load_json(P1_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "ONTOLOGY-WAS-3H-P2-GATE-REPLAY-20260621", "invalid evidence id")
    require(evidence.get("status") == "ontology_was_3h_p2_gate_replay_pass", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-3H-P2-GATE-REPLAY-001", "invalid round id")
    require(evidence.get("plan_ref") == plan.get("evidence_id"), "plan ref mismatch")
    require(evidence.get("previous_round") == p1.get("round_id"), "previous round mismatch")

    phase = evidence.get("phase", {})
    require(phase.get("phase_id") == "P2-gate-execution-and-replay", "phase id mismatch")
    require(phase.get("time_window_minutes") == "75-135", "time window mismatch")
    require(phase.get("execution_started") is True, "execution_started must be true")
    require(phase.get("execution_mode") == "controlled_local_validator_replay", "execution mode mismatch")

    summary = evidence.get("gate_replay_summary", {})
    require(summary.get("gate_groups_executed") == 9, "gate groups executed mismatch")
    require(summary.get("gate_groups_passed") == 9, "gate groups passed mismatch")
    require(summary.get("failed_gate_groups") == 0, "failed gate groups must be 0")
    require(summary.get("was_okf_validator_count") == 12, "WAS OKF validator count mismatch")
    require(summary.get("was_okf_validator_passed") == 12, "WAS OKF validator passed mismatch")
    for key in ZERO_KEYS:
        require(summary.get(key) == 0, f"{key} must be 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(summary.get(key) is False, f"{key} must be false")

    gate_outputs = evidence.get("gate_outputs", [])
    require(len(gate_outputs) == 9, "gate output count mismatch")
    seen_gates = [entry.get("gate") for entry in gate_outputs]
    require(seen_gates == REQUIRED_GATES, "gate output order mismatch")
    for entry in gate_outputs:
        require(entry.get("result") == "pass", f"{entry.get('gate')} must pass")
        require("=pass" in entry.get("output", "") or "PASS " in entry.get("output", ""), f"{entry.get('gate')} output missing pass marker")

    okf_output = gate_outputs[-1].get("output", "")
    for validator in REQUIRED_OKF_VALIDATORS:
        require(f"PASS {validator}" in okf_output, f"missing OKF validator: {validator}")

    exit_gate = evidence.get("p2_exit_gate", {})
    require(exit_gate.get("status") == "pass", "P2 exit gate must pass")
    require(exit_gate.get("blocker") is None, "P2 blocker must be null")
    require(exit_gate.get("promotion_allowed") is False, "promotion must not be allowed")
    require(evidence.get("next_phase") == "P3-closure-and-next-decision", "next phase mismatch")

    for phrase in [
        "gate_groups_executed | `9`",
        "gate_groups_passed | `9`",
        "was_okf_validator_count | `12`",
        "was_okf_validator_passed | `12`",
        "p2_exit_gate.status | `pass`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("Ontology/WAS 3 小时目标已完成 P2 门禁执行与回放" in loop_round, "loop round missing feedback")

    print(
        "ontology_was_3h_p2_gate_replay=pass "
        "phase=P2-gate-execution-and-replay gate_groups_executed=9 gate_groups_passed=9 "
        "failed_gate_groups=0 was_okf_validator_count=12 was_okf_validator_passed=12 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 "
        "review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
