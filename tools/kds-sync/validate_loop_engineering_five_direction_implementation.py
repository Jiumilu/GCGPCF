#!/usr/bin/env python3
"""Validate the Loop Engineering five-direction implementation package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = ROOT / "02-governance/loop/LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md"
TEMPLATE = ROOT / "templates/loop-round-v2-five-direction.yaml"
FIXTURE = ROOT / "fixtures/loop-dashboard/loop-engineering-five-direction-implementation.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-engineering-five-direction-implementation-20260622.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
LOOP_DOCUMENT_GATE = ROOT / "tools/kds-sync/loop_document_gate.py"
SPEC_MIRROR = ROOT / ".kds/development-space/开发/91-治理与验收/02-governance/loop/LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md"
EVIDENCE_MIRROR = ROOT / ".kds/development-space/开发/05-KDS/docs/harness/evidence/loop-engineering-five-direction-implementation-20260622.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_loop_engineering_five_direction_implementation: {message}")


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
    spec = read(SPEC_DOC)
    template = read(TEMPLATE)
    fixture = load_json(FIXTURE)
    evidence = read(EVIDENCE_MD)
    loop_document_gate = read(LOOP_DOCUMENT_GATE)
    status_text = "\n".join([read(CONTROL_BOARD), read(LOOP_STATE), read(STATUS_MATRIX)])

    require_controlled(spec, "02-governance/loop/LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md")
    require_controlled(evidence, "docs/harness/evidence/loop-engineering-five-direction-implementation-20260622.md")

    for phrase in [
        "Loop Engineering 五方向实施规范",
        "Loop 如何运行",
        "Loop 如何停止",
        "Loop 如何验证",
        "Loop 如何恢复",
        "Loop 如何调试",
        "stop_detector",
        "recovery_checkpoint",
        "precheck",
        "intermediate_check",
        "final_gate",
        "accepted",
        "integrated",
        "production_ready",
        "GFIS 真实业务 lane 仍保持 `repair_required`",
    ]:
        require(phrase in spec, f"spec missing phrase: {phrase}")

    for phrase in [
        "loop_round_v2_five_direction:",
        "run:",
        "stop:",
        "verify:",
        "recover:",
        "debug:",
        "status_ceiling:",
        "accepted_allowed: false",
        "integrated_allowed: false",
        "production_ready_allowed: false",
        "no_production_write: true",
    ]:
        require(phrase in template, f"template missing phrase: {phrase}")

    for phrase in [
        "loop_engineering_five_direction",
        "validate_loop_engineering_five_direction_implementation.py",
    ]:
        require(phrase in loop_document_gate, f"loop_document_gate missing integration phrase: {phrase}")

    require(SPEC_MIRROR.exists(), "spec markdown is not mirrored to KDS development-space")
    require(EVIDENCE_MIRROR.exists(), "evidence markdown is not mirrored to KDS development-space")

    require(fixture.get("status") == "implemented_control_plane", "fixture status must be implemented_control_plane")
    require(fixture.get("status_ceiling") == "partial_repair", "fixture status ceiling must be partial_repair")

    directions = fixture.get("directions", {})
    for key in ["run", "stop", "verify", "recover", "debug"]:
        require(directions.get(key, {}).get("implemented") is True, f"direction not implemented: {key}")

    snapshot = fixture.get("current_debug_snapshot", {})
    real_counts = snapshot.get("real_lane_counts", {})
    for key in ["valid_source_records", "runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]:
        require(real_counts.get(key) == 0, f"real lane count must remain zero: {key}")

    write_counts = snapshot.get("write_counts", {})
    for key in ["production_writes", "real_external_api_writes", "kds_fact_writes", "waes_gate_result_writes"]:
        require(write_counts.get(key) == 0, f"write count must remain zero: {key}")

    recovery = fixture.get("recovery_checkpoint", {})
    for key in ["failed_or_stopped_at", "last_safe_state", "retryable_actions", "non_retryable_actions", "required_inputs", "resume_round"]:
        require(key in recovery, f"recovery checkpoint missing: {key}")
    require("real_business_lane=repair_required" in recovery.get("last_safe_state", ""), "recovery must preserve repair_required")

    guards = fixture.get("completion_guards", {})
    for key in ["accepted_allowed", "integrated_allowed", "production_ready_allowed", "business_completion_claim_allowed"]:
        require(guards.get(key) is False, f"completion guard must be false: {key}")
    require(guards.get("no_write_boundary_enforced") is True, "no-write boundary must be enforced")

    for phrase in [
        "LOOP-FIVE-DIRECTION-IMPLEMENTATION-20260622",
        "failing_gate",
        "GFIS real_business_lane",
        "status_ceiling",
        "partial_repair",
        "valid_source_records | `0`",
        "runtime_primary_key_ready | `0`",
        "review_queue | `0`",
        "runtime_intake | `0`",
        "waes_review | `0`",
        "verified | `0`",
        "loop_engineering_five_direction_implementation=pass",
    ]:
        require(phrase in evidence, f"evidence missing phrase: {phrase}")

    for phrase in [
        "real_business_lane=repair_required",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
    ]:
        require(phrase in status_text, f"current status missing boundary phrase: {phrase}")

    forbidden = [
        "business_completion_claim_allowed\": true",
        "accepted_allowed\": true",
        "integrated_allowed\": true",
        "production_ready_allowed\": true",
        "GFIS 真实业务闭环已完成",
        "GFIS 真实业务闭环已经完成",
    ]
    combined = "\n".join([spec, evidence, json.dumps(fixture, ensure_ascii=False)])
    for phrase in forbidden:
        require(phrase not in combined, f"forbidden claim present: {phrase}")

    print(
        "loop_engineering_five_direction_implementation=pass "
        "run=implemented stop=implemented verify=implemented recover=implemented debug=implemented "
        "status_ceiling=partial_repair real_business_lane=repair_required "
        "runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted_allowed=false integrated_allowed=false production_ready_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
