#!/usr/bin/env python3
"""Validate WAS real source-record waiting room."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-waiting-room-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-waiting-room-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-WAITING-ROOM-001.md"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
REQUIRED_INPUTS = [
    "customer_order_original_or_platform_receipt",
    "customer_confirmed_product_specification",
    "delivery_requirement",
    "issuer_and_responsible_owner_confirmation",
    "kds_source_backlink",
    "runtime_site_context",
]
ZERO_BOUNDARY_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]
FALSE_BOUNDARY_KEYS = ["accepted", "integrated", "production_ready"]


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


def validate_waiting_room(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if value.get("required_p4_inputs") != REQUIRED_INPUTS:
        failures.append("required_p4_inputs_mismatch")
    if not value.get("owner"):
        failures.append("owner_missing")
    if value.get("intake_state") != "waiting_for_real_inputs":
        failures.append("intake_state_mismatch")
    if value.get("submitted_real_inputs") != 0:
        failures.append("submitted_real_inputs_must_be_zero")
    if value.get("accepted_for_next_gate") != 0:
        failures.append("accepted_for_next_gate_must_be_zero")
    if value.get("hold_required") != 1:
        failures.append("hold_required_must_be_one")
    boundary = value.get("boundary", {})
    if not isinstance(boundary, dict):
        failures.append("boundary_not_object")
        boundary = {}
    for key in ZERO_BOUNDARY_KEYS:
        if boundary.get(key) != 0:
            failures.append(f"boundary_{key}_must_be_zero")
    for key in FALSE_BOUNDARY_KEYS:
        if boundary.get(key) is not False:
            failures.append(f"boundary_{key}_must_be_false")
    return failures


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_text = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_text)

    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-WAITING-ROOM-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_real_source_record_waiting_room_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-WAITING-ROOM-001", "invalid round id")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    inputs = evidence.get("required_p4_inputs", [])
    require([item.get("input_id") for item in inputs] == REQUIRED_INPUTS, "required P4 input list mismatch")
    require(all(item.get("state") == "missing" for item in inputs), "all P4 inputs must remain missing")

    waiting_state = evidence.get("waiting_state", {})
    require(waiting_state.get("submitted_real_inputs") == 0, "submitted real inputs must be 0")
    require(waiting_state.get("accepted_for_next_gate") == 0, "accepted_for_next_gate must be 0")
    require(waiting_state.get("hold_required") == 1, "hold_required must be 1")

    positive = load_json(FIXTURE_DIR / "real-source-record-waiting-room-positive.json")
    require(not validate_waiting_room(positive), "positive fixture should pass")
    negative_paths = sorted(FIXTURE_DIR.glob("real-source-record-waiting-room-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        require(validate_waiting_room(load_json(path)), f"{path.name} should be rejected")

    boundary = evidence.get("boundary", {})
    for key in ZERO_BOUNDARY_KEYS:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in FALSE_BOUNDARY_KEYS:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "submitted_real_inputs | `0`",
        "accepted_for_next_gate | `0`",
        "hold_required | `1`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("真实 source-record waiting room 已建立" in loop_text, "loop feedback missing")

    print(
        "was_real_source_record_waiting_room=pass "
        "required_p4_inputs=6 submitted_real_inputs=0 accepted_for_next_gate=0 hold_required=1 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
