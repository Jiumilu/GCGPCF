#!/usr/bin/env python3
"""Validate WAS real source-record monitor."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-monitor-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-001.md"
WAITING_ROOM_JSON = ROOT / "docs/harness/evidence/was-real-source-record-waiting-room-20260621.json"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
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
    require("Studio" in metadata and "WAS" in metadata, f"{path.relative_to(ROOT)} frontmatter must include full project group scope")


def validate_monitor(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if value.get("required_p4_inputs") != 6:
        failures.append("required_p4_inputs_mismatch")
    for key in ["submitted_real_inputs", "submitted_files_found", "candidate_files_checked", "accepted_for_next_gate"]:
        if value.get(key) != 0:
            failures.append(f"{key}_must_be_zero")
    if value.get("hold_required") != 1:
        failures.append("hold_required_must_be_one")
    if value.get("monitor_state") != "waiting":
        failures.append("monitor_state_must_be_waiting")
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


def run(command: list[str]) -> str:
    proc = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    require(proc.returncode == 0, f"command failed: {' '.join(command)}\n{proc.stdout}")
    return proc.stdout


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    waiting_room = load_json(WAITING_ROOM_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_text = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_text)

    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-MONITOR-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_real_source_record_monitor_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-001", "invalid round id")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")

    waiting_state = waiting_room.get("waiting_state", {})
    checks = evidence.get("monitor_checks", {})
    require(checks.get("required_p4_inputs") == len(waiting_room.get("required_p4_inputs", [])) == 6, "required input count mismatch")
    require(checks.get("submitted_real_inputs") == waiting_state.get("submitted_real_inputs") == 0, "submitted input count mismatch")
    require(checks.get("accepted_for_next_gate") == waiting_state.get("accepted_for_next_gate") == 0, "accepted_for_next_gate mismatch")
    require(checks.get("hold_required") == waiting_state.get("hold_required") == 1, "hold_required mismatch")
    require(checks.get("monitor_state") == "waiting", "monitor state mismatch")

    candidate_output = run(["python3", "tools/kds-sync/validate_was_real_source_record_candidate_precheck.py"])
    submission_output = run(["python3", "tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py"])
    require("submitted_real_candidate_files=0" in candidate_output, "candidate precheck must report 0 submitted real candidates")
    require("accepted_for_next_gate=0" in candidate_output, "candidate precheck must not accept next gate")
    require("submitted_files_found=0" in submission_output, "submission precheck must report 0 submitted files")
    require("hold_required=1" in submission_output, "submission precheck must hold")

    positive = load_json(FIXTURE_DIR / "real-source-record-monitor-positive.json")
    require(not validate_monitor(positive), "positive fixture should pass")
    negative_paths = sorted(FIXTURE_DIR.glob("real-source-record-monitor-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        require(validate_monitor(load_json(path)), f"{path.name} should be rejected")

    boundary = evidence.get("boundary", {})
    for key in ZERO_BOUNDARY_KEYS:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in FALSE_BOUNDARY_KEYS:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "required_p4_inputs | `6`",
        "submitted_real_inputs | `0`",
        "accepted_for_next_gate | `0`",
        "hold_required | `1`",
        "monitor_state | `waiting`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("真实 P4 输入 monitor 已建立" in loop_text, "loop feedback missing")

    print(
        "was_real_source_record_monitor=pass "
        "required_p4_inputs=6 submitted_real_inputs=0 submitted_files_found=0 candidate_files_checked=0 "
        "accepted_for_next_gate=0 hold_required=1 monitor_state=waiting "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-002"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
