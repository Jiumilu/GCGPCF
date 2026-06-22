#!/usr/bin/env python3
"""Validate GPCF-LOOP-FIVE-DIRECTION-RUN-001 no-write runtime evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-LOOP-FIVE-DIRECTION-RUN-001.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-five-direction-run-001-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-five-direction-run-001-20260622.md"
BASE_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_engineering_five_direction_implementation.py"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_loop_five_direction_run_001: {message}")


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
    round_doc = read(ROUND)
    evidence_md = read(EVIDENCE_MD)
    evidence = load_json(EVIDENCE_JSON)
    base_validator = read(BASE_VALIDATOR)
    status_text = "\n".join([read(CONTROL_BOARD), read(LOOP_STATE), read(STATUS_MATRIX)])

    require_controlled(round_doc, "docs/harness/loops/loop-round-GPCF-LOOP-FIVE-DIRECTION-RUN-001.md")
    require_controlled(evidence_md, "docs/harness/evidence/loop-five-direction-run-001-20260622.md")

    for phrase in [
        "GPCF-LOOP-FIVE-DIRECTION-RUN-001",
        "Loop L3 托管冲刺模式 / no-write",
        "五方向运行记录",
        "### 1. run",
        "### 2. stop",
        "### 3. verify",
        "### 4. recover",
        "### 5. debug",
        "stop_type | `authorization_boundary`",
        "substantive_rounds | `1/15`",
        "real_business_lane=repair_required",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
    ]:
        require(phrase in round_doc, f"round doc missing phrase: {phrase}")

    require(evidence.get("started") is True, "evidence must prove run started")
    require(evidence.get("completed_for_round") is True, "evidence must prove round completed")
    require(evidence.get("stop_type") == "authorization_boundary", "stop_type must be authorization_boundary")
    require(evidence.get("mode") == "L3", "mode must be L3")
    require(evidence.get("scope") == "no-write", "scope must be no-write")

    runtime = evidence.get("five_direction_runtime", {})
    for key in ["run", "stop", "verify", "recover", "debug"]:
        require(runtime.get(key, {}).get("status") in {"executed", "recorded"}, f"missing runtime direction: {key}")

    continuous = evidence.get("continuous_runtime", {})
    require(continuous.get("session") == "stopped", "session must stop with legal stop type after RUN-001 scope")
    require(continuous.get("mode") == "L3", "continuous mode must be L3")
    require(continuous.get("declared_rounds") == 1, "declared_rounds must be 1")
    require(continuous.get("substantive_rounds") == 1, "substantive_rounds must be 1")
    require(continuous.get("remaining_rounds") == 14, "remaining_rounds must be 14")
    require(continuous.get("substance_gate") == "pass", "substance_gate must be pass")
    require(continuous.get("final_answer_allowed") is True, "final answer must be allowed by authorization_boundary")

    boundaries = evidence.get("boundaries", {})
    for key in [
        "no_production_write",
        "no_external_api_write",
        "no_kds_fact_write",
        "no_waes_gate_result_write",
        "no_accepted_integrated_upgrade",
    ]:
        require(boundaries.get(key) is True, f"boundary must be true: {key}")
    require(boundaries.get("real_business_lane") == "repair_required", "real business lane must stay repair_required")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundaries.get(key) is False, f"{key} must remain false")

    for phrase in [
        "LOOP-FIVE-DIRECTION-RUN-001-20260622",
        "新加入的五方向内容已经开始运行",
        "validate_loop_five_direction_run_001=pass",
        "loop_document_gate=rework_required localization_debt=true",
        "GPCF-LOOP-FIVE-DIRECTION-RUN-002",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "real_business_lane=repair_required",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
    ]:
        require(phrase in status_text, f"current status missing boundary phrase: {phrase}")

    require(
        "validate_loop_engineering_five_direction_implementation.py" in base_validator,
        "base five-direction validator must remain present",
    )

    forbidden = [
        "\"accepted\": true",
        "\"integrated\": true",
        "\"production_ready\": true",
        "生产写入已完成",
        "真实外部 API 写入已完成",
        "GFIS 真实业务闭环已完成",
    ]
    combined = "\n".join([round_doc, evidence_md, json.dumps(evidence, ensure_ascii=False)])
    for phrase in forbidden:
        require(phrase not in combined, f"forbidden claim present: {phrase}")

    print(
        "validate_loop_five_direction_run_001=pass "
        "round=GPCF-LOOP-FIVE-DIRECTION-RUN-001 mode=L3 scope=no-write "
        "started=true completed_for_round=true stop_type=authorization_boundary "
        "declared_rounds=1/15 substantive_rounds=1/15 remaining_rounds=14 "
        "real_business_lane=repair_required accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
