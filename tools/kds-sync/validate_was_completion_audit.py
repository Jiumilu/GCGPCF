#!/usr/bin/env python3
"""Validate WAS-Ontology completion audit evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
WAS_ROOT = ROOT.parent / "WAS世界资产体系"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-completion-audit-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-completion-audit-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-COMPLETION-AUDIT-001.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
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
REQUIRED_LOCAL_VALIDATORS = [
    "tools/kds-sync/validate_was_status_matrix_control_board_refresh.py",
    "tools/kds-sync/validate_was_loop_context_coverage_refresh.py",
    "tools/kds-sync/validate_was_project_group_ontology_registry.py",
    "tools/kds-sync/validate_was_waes_kds_rag_writeback_gate_pack.py",
    "tools/kds-sync/validate_was_scenario_profile_matrix.py",
    "tools/kds-sync/validate_was_real_source_record_candidate_precheck.py",
    "tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py",
    "tools/kds-sync/validate_gfis_was_source_record_admission_gate.py",
    "tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py",
    "tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py",
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
    require("WAS" in metadata and "Studio" in metadata, f"{path.relative_to(ROOT)} frontmatter must include full project group scope")


def validate_fixture(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if value.get("objective_items") != 8:
        failures.append("objective_items_mismatch")
    if value.get("verified_governance_items") != 8:
        failures.append("verified_governance_items_mismatch")
    if value.get("hold_items") != 1:
        failures.append("hold_items_mismatch")
    if value.get("project_group_scope_count") != 14:
        failures.append("project_group_scope_count_mismatch")
    if value.get("required_validators_passed") != 11:
        failures.append("required_validators_passed_mismatch")
    if value.get("frontmatter_scope_complete") is not True:
        failures.append("frontmatter_scope_incomplete")
    if value.get("governance_completion") != "verified_governance_complete":
        failures.append("governance_completion_invalid")
    if value.get("business_completion") != "hold_waiting_real_source_record":
        failures.append("business_completion_invalid")
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


def run_validator(command: str) -> str:
    if command.startswith("python3 /"):
        parts = ["python3", command.removeprefix("python3 ")]
        cwd = WAS_ROOT
    else:
        parts = command.split()
        cwd = ROOT
    proc = subprocess.run(parts, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    require(proc.returncode == 0, f"validator failed: {command}\n{proc.stdout}")
    return proc.stdout


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_text = read(LOOP_ROUND)
    control_board = read(CONTROL_BOARD)
    status_matrix = read(STATUS_MATRIX)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_text)
    require_frontmatter(CONTROL_BOARD, control_board)
    require_frontmatter(STATUS_MATRIX, status_matrix)

    require(evidence.get("evidence_id") == "WAS-COMPLETION-AUDIT-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_completion_audit_pass_governance_complete_with_business_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-COMPLETION-AUDIT-001", "invalid round id")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    require(len(evidence.get("objective_audit", [])) == 8, "objective audit count mismatch")

    summary = evidence.get("completion_summary", {})
    require(summary.get("objective_items") == 8, "summary objective count mismatch")
    require(summary.get("verified_governance_items") == 8, "summary verified governance mismatch")
    require(summary.get("hold_items") == 1, "summary hold count mismatch")
    require(summary.get("governance_completion") == "verified_governance_complete", "governance completion mismatch")
    require(summary.get("business_completion") == "hold_waiting_real_source_record", "business completion mismatch")
    require(summary.get("frontmatter_scope_complete") is True, "frontmatter scope completion mismatch")

    commands = evidence.get("required_validators", [])
    require(len(commands) == 11, "required validator count mismatch")
    for command in REQUIRED_LOCAL_VALIDATORS:
        require(f"python3 {command}" in commands, f"missing validator command: python3 {command}")
    require(any("WAS世界资产体系/okf/validators/validate_all.py" in command for command in commands), "missing WAS validate_all command")
    for command in commands:
        run_validator(command)

    positive = load_json(FIXTURE_DIR / "completion-audit-positive.json")
    require(not validate_fixture(positive), "positive fixture should pass")
    negative_paths = sorted(FIXTURE_DIR.glob("completion-audit-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        require(validate_fixture(load_json(path)), f"{path.name} should be rejected")

    fixture_gate = evidence.get("fixture_gate", {})
    require(fixture_gate.get("positive_fixtures") == 1, "positive fixture count mismatch")
    require(fixture_gate.get("negative_fixtures") == 3, "negative fixture count mismatch")
    require(fixture_gate.get("expected_positive_acceptance") == 1, "positive acceptance mismatch")
    require(fixture_gate.get("expected_negative_rejection") == 3, "negative rejection mismatch")

    boundary = evidence.get("boundary", {})
    for key in ZERO_BOUNDARY_KEYS:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in FALSE_BOUNDARY_KEYS:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "governance_completion | `verified_governance_complete`",
        "business_completion | `hold_waiting_real_source_record`",
        "real_source_records | `0`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("verified_governance_complete" in loop_text, "loop feedback missing governance completion")
    require("hold_waiting_real_source_record" in loop_text, "loop feedback missing business hold")
    require("GPCF-ONTOLOGY-WAS-COMPLETION-AUDIT-001" in control_board, "control board not pointing to completion audit")
    require("GPCF-ONTOLOGY-WAS-COMPLETION-AUDIT-001" in status_matrix, "status matrix not pointing to completion audit")

    print(
        "was_completion_audit=pass "
        "objective_items=8 verified_governance_items=8 hold_items=1 project_group_scope=14/14 "
        "required_validators=11 governance_completion=verified_governance_complete "
        "business_completion=hold_waiting_real_source_record "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-WAITING-ROOM-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
