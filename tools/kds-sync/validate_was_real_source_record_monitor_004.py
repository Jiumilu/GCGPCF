#!/usr/bin/env python3
"""Validate WAS real source-record monitor round 004."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-004-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-monitor-004-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-004.md"
PREVIOUS_MONITOR_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-003-20260621.json"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
ZERO_KEYS = ["real_source_records", "valid_source_records", "runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]
FALSE_KEYS = ["accepted", "integrated", "production_ready"]
REQUIRED_COMMANDS = [
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py"],
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_admission_gate.py"],
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py"],
    ["python3", "tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py"],
    ["python3", "tools/kds-sync/validate_was_real_source_record_candidate_precheck.py"],
    ["python3", "tools/kds-sync/validate_was_real_source_record_monitor_003.py"],
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
        "Studio",
        "WAS",
        "domain: ontology-governance",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def monitor_failures(value: dict[str, Any]) -> list[str]:
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
    if value.get("candidate_file_quality") != "none_submitted":
        failures.append("candidate_file_quality_must_be_none_submitted")
    boundary = value.get("boundary", {})
    if not isinstance(boundary, dict):
        return failures + ["boundary_not_object"]
    for key in ZERO_KEYS:
        if boundary.get(key) != 0:
            failures.append(f"boundary_{key}_must_be_zero")
    for key in FALSE_KEYS:
        if boundary.get(key) is not False:
            failures.append(f"boundary_{key}_must_be_false")
    return failures


def run(command: list[str]) -> str:
    proc = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    require(proc.returncode == 0, f"command failed: {' '.join(command)}\n{proc.stdout}")
    return proc.stdout


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    previous = load_json(PREVIOUS_MONITOR_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-MONITOR-004-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_real_source_record_monitor_004_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-004", "invalid round id")
    require(evidence.get("source_round") == previous.get("round_id"), "source round mismatch")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")

    checks = evidence.get("monitor_checks", {})
    require(not monitor_failures(checks | {"boundary": evidence.get("boundary", {})}), "monitor checks must represent held state")
    require(evidence.get("required_commands") == [" ".join(command) for command in REQUIRED_COMMANDS], "required command list mismatch")

    joined_output = "\n".join(run(command) for command in REQUIRED_COMMANDS)
    for phrase in [
        "submitted_files_found=0",
        "accepted_for_next_gate=0",
        "hold_required=1",
        "real_source_records=0",
        "valid_source_records=0",
        "runtime_primary_key_ready=0",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
    ]:
        require(phrase in joined_output, f"required command output missing phrase: {phrase}")

    positive = load_json(FIXTURE_DIR / "real-source-record-monitor-004-positive.json")
    require(not monitor_failures(positive), "positive fixture should pass")
    negatives = sorted(FIXTURE_DIR.glob("real-source-record-monitor-004-negative-*.json"))
    require(len(negatives) == 3, "negative fixture count must be 3")
    for path in negatives:
        require(monitor_failures(load_json(path)), f"{path.name} should be rejected")

    boundary = evidence.get("boundary", {})
    for key in ZERO_KEYS:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in FALSE_KEYS:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "required_p4_inputs | `6`",
        "submitted_real_inputs | `0`",
        "submitted_files_found | `0`",
        "accepted_for_next_gate | `0`",
        "hold_required | `1`",
        "candidate_file_quality | `none_submitted`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("真实 P4 输入 monitor 004 已建立" in loop_round, "loop round feedback missing")

    print(
        "was_real_source_record_monitor_004=pass "
        "required_p4_inputs=6 submitted_real_inputs=0 submitted_files_found=0 candidate_files_checked=0 "
        "accepted_for_next_gate=0 hold_required=1 monitor_state=waiting candidate_file_quality=none_submitted "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 "
        "runtime_intake=0 waes_review=0 verified=0 accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-005"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
