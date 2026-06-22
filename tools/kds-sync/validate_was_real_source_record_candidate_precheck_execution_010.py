#!/usr/bin/env python3
"""Validate current re-execution evidence for WAS/Ontology P4 candidate precheck."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-candidate-precheck-execution-010-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-candidate-precheck-execution-010-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-EXECUTION-010.md"
INTAKE_DIR = ROOT / "docs/harness/intake"
TEMPLATE = INTAKE_DIR / "was-real-source-record-candidate-template.yaml"
POSITIVE = ROOT / "fixtures/was/p4-candidate-precheck-execution-010-positive-hold.json"
NEGATIVE = ROOT / "fixtures/was/p4-candidate-precheck-execution-010-negative-false-promotion.json"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
BOUNDARY_ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]
REQUIRED_COMMANDS = [
    "python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py",
    "python3 tools/kds-sync/validate_gfis_was_source_record_admission_gate.py",
    "python3 tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py",
    "python3 tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py",
]
SUPPLEMENTAL_COMMANDS = [
    "python3 tools/kds-sync/validate_was_real_source_record_candidate_precheck.py",
    "python3 tools/kds-sync/validate_was_real_source_record_monitor_094.py",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(read(path))
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        "domain: ontology-governance",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "Studio",
        "WAS",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def candidate_files() -> list[Path]:
    files: list[Path] = []
    for pattern in ["gfis-was-real-source-record-candidate-*.json", "gfis-was-real-source-record-candidate-*.yaml"]:
        files.extend(INTAKE_DIR.glob(pattern))
    return sorted(path for path in files if path.name != TEMPLATE.name)


def valid_hold_state(payload: dict[str, Any]) -> bool:
    return (
        payload.get("submitted_real_candidate_files") == 0
        and payload.get("candidate_files_checked") == 0
        and payload.get("accepted_for_next_gate") == 0
        and payload.get("hold_required") == 1
        and all(payload.get(key) == 0 for key in BOUNDARY_ZERO_KEYS)
        and payload.get("accepted") is False
        and payload.get("integrated") is False
        and payload.get("production_ready") is False
    )


def run_required_commands() -> list[str]:
    outputs: list[str] = []
    for command in REQUIRED_COMMANDS + SUPPLEMENTAL_COMMANDS:
        result = subprocess.run(command.split(), cwd=ROOT, text=True, capture_output=True, check=False)
        require(result.returncode == 0, f"command failed: {command}\n{result.stdout}{result.stderr}")
        outputs.append(result.stdout.strip())
    return outputs


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    positive = load_json(POSITIVE)
    negative = load_json(NEGATIVE)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require(TEMPLATE.exists(), "candidate template missing")

    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-EXECUTION-010-20260622", "invalid evidence id")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-EXECUTION-010", "invalid round id")
    require(evidence.get("executed_round") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001", "executed round mismatch")
    require(evidence.get("source_round") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-094", "source round mismatch")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    command_gate = evidence.get("command_gate", {})
    require(command_gate.get("required_commands") == REQUIRED_COMMANDS, "required command list mismatch")
    require(command_gate.get("supplemental_commands") == SUPPLEMENTAL_COMMANDS, "supplemental command list mismatch")

    live_scan = evidence.get("live_intake_scan", {})
    require(valid_hold_state({**live_scan, **evidence.get("boundary", {})}), "evidence must remain in empty hold state")
    require(len(candidate_files()) == 0, "real candidate files unexpectedly present")
    require(valid_hold_state(positive), "positive hold fixture should pass")
    require(not valid_hold_state(negative), "negative false-promotion fixture should fail")

    for key in BOUNDARY_ZERO_KEYS:
        require(f"{key} | `0`" in evidence_md, f"evidence md missing zero marker: {key}")
    for marker in ["accepted | `false`", "integrated | `false`", "production_ready | `false`"]:
        require(marker in evidence_md, f"evidence md missing marker: {marker}")
    require("GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-095" in evidence_md, "next round missing from evidence md")
    require("loop_was_context" in loop_round, "loop round missing loop_was_context")
    require("run" in loop_round and "stop" in loop_round and "verify" in loop_round and "recover" in loop_round and "debug" in loop_round, "loop round missing run/stop/verify/recover/debug")

    command_outputs = run_required_commands()
    require(len(command_outputs) == command_gate.get("expected_pass_count") == 6, "command pass count mismatch")
    require(any("accepted_for_next_gate=0" in output for output in command_outputs), "precheck output must keep accepted_for_next_gate=0")
    require(any("hold_required=1" in output for output in command_outputs), "precheck output must keep hold_required=1")
    require(any("was_real_source_record_monitor_094=pass" in output for output in command_outputs), "monitor 094 output missing")

    print(
        "was_real_source_record_candidate_precheck_execution_010=pass "
        "submitted_real_candidate_files=0 candidate_files_checked=0 accepted_for_next_gate=0 "
        "hold_required=1 real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 "
        "review_queue=0 runtime_intake=0 waes_review=0 verified=0 accepted=false integrated=false "
        "production_ready=false next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-095"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
