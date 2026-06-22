#!/usr/bin/env python3
"""Validate WAS real source-record monitor round 007."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-007-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-monitor-007-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-007.md"
PREVIOUS_MONITOR_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-006-20260621.json"
INTAKE_DIR = ROOT / "docs/harness/intake"
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
    ["python3", "tools/kds-sync/validate_was_real_source_record_monitor_006.py"],
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


def candidate_files() -> list[Path]:
    files: list[Path] = []
    for pattern in ["gfis-was-real-source-record-candidate-*.json", "gfis-was-real-source-record-candidate-*.yaml"]:
        files.extend(INTAKE_DIR.glob(pattern))
    return sorted(path for path in files if path.name != "was-real-source-record-candidate-template.yaml")


def intake_bypass_files() -> dict[str, list[str]]:
    nested: list[str] = []
    sidecar_only: list[str] = []
    unsupported: list[str] = []
    allowed_names = {"was-real-source-record-candidate-template.yaml"}
    allowed_suffixes = {".json", ".yaml"}
    for path in sorted(INTAKE_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(INTAKE_DIR).as_posix()
        lower = path.name.lower()
        if rel in allowed_names:
            continue
        if "/" in rel and lower.startswith("gfis-was-real-source-record-candidate-"):
            nested.append(rel)
        if any(token in lower for token in ["sidecar", "metadata"]) and not lower.startswith("gfis-was-real-source-record-candidate-"):
            sidecar_only.append(rel)
        if lower.startswith("gfis-was-real-source-record-candidate-") and path.suffix.lower() not in allowed_suffixes:
            unsupported.append(rel)
    return {"nested": nested, "sidecar_only": sidecar_only, "unsupported": unsupported}


def monitor_failures(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for key in [
        "submitted_real_candidate_files",
        "replayed_source_record_ids",
        "stale_received_at_candidates",
        "wrong_kds_backlink_scope_candidates",
        "nested_candidate_files",
        "sidecar_only_files",
        "unsupported_extension_files",
        "accepted_for_next_gate",
    ]:
        if value.get(key, 0) != 0:
            failures.append(f"{key}_must_be_zero")
    if value.get("hold_required") != 1:
        failures.append("hold_required_must_be_one")
    if value.get("candidate_replay_state", "none_detected") != "none_detected":
        failures.append("candidate_replay_state_must_be_none_detected")
    if value.get("candidate_bypass_guard", "pass") != "pass":
        failures.append("candidate_bypass_guard_must_pass")
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
    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-MONITOR-007-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_real_source_record_monitor_007_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-007", "invalid round id")
    require(evidence.get("source_round") == previous.get("round_id"), "source round mismatch")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    require(evidence.get("required_commands") == [" ".join(command) for command in REQUIRED_COMMANDS], "required command list mismatch")

    submitted = candidate_files()
    bypass = intake_bypass_files()
    checks = evidence.get("monitor_checks", {})
    require(checks.get("submitted_real_candidate_files") == len(submitted) == 0, "submitted candidate count mismatch")
    require(checks.get("replayed_source_record_ids") == 0, "replayed source record ids must be 0")
    require(checks.get("stale_received_at_candidates") == 0, "stale received_at candidates must be 0")
    require(checks.get("wrong_kds_backlink_scope_candidates") == 0, "wrong KDS backlink scope candidates must be 0")
    require(checks.get("nested_candidate_files") == len(bypass["nested"]) == 0, "nested candidate count mismatch")
    require(checks.get("sidecar_only_files") == len(bypass["sidecar_only"]) == 0, "sidecar-only file count mismatch")
    require(checks.get("unsupported_extension_files") == len(bypass["unsupported"]) == 0, "unsupported extension count mismatch")
    require(checks.get("accepted_for_next_gate") == 0, "accepted_for_next_gate must be 0")
    require(checks.get("hold_required") == 1, "hold_required must be 1")
    require(checks.get("candidate_replay_state") == "none_detected", "candidate replay state must be none_detected")
    require(checks.get("candidate_bypass_guard") == "pass", "candidate bypass guard must pass")

    positive = load_json(FIXTURE_DIR / "real-source-record-monitor-007-positive.json")
    require(not monitor_failures(positive), "positive fixture should pass")
    negatives = sorted(FIXTURE_DIR.glob("real-source-record-monitor-007-negative-*.json"))
    require(len(negatives) == 6, "negative fixture count must be 6")
    for path in negatives:
        require(monitor_failures(load_json(path)), f"{path.name} should be rejected")

    boundary = evidence.get("boundary", {})
    for key in ZERO_KEYS:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in FALSE_KEYS:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    joined_output = "\n".join(run(command) for command in REQUIRED_COMMANDS)
    for phrase in [
        "accepted_for_next_gate=0",
        "hold_required=1",
        "real_source_records=0",
        "valid_source_records=0",
        "runtime_primary_key_ready=0",
        "waes_review=0",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
    ]:
        require(phrase in joined_output, f"required command output missing phrase: {phrase}")

    for phrase in [
        "submitted_real_candidate_files | `0`",
        "replayed_source_record_ids | `0`",
        "stale_received_at_candidates | `0`",
        "wrong_kds_backlink_scope_candidates | `0`",
        "nested_candidate_files | `0`",
        "sidecar_only_files | `0`",
        "unsupported_extension_files | `0`",
        "hold_required | `1`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("真实 P4 输入 monitor 007 已建立" in loop_round, "loop round feedback missing")
    require("replayed_source_record_id" in loop_round and "stale_received_at" in loop_round, "loop round missing replay cases")
    require("wrong_kds_backlink_scope" in loop_round, "loop round missing KDS backlink scope case")
    for phrase in ["nested_candidate", "sidecar_only", "unsupported_extension"]:
        require(phrase in loop_round, f"loop round missing bypass case: {phrase}")

    print(
        "was_real_source_record_monitor_007=pass "
        "submitted_real_candidate_files=0 replayed_source_record_ids=0 stale_received_at_candidates=0 "
        "wrong_kds_backlink_scope_candidates=0 nested_candidate_files=0 sidecar_only_files=0 "
        "unsupported_extension_files=0 accepted_for_next_gate=0 hold_required=1 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 "
        "runtime_intake=0 waes_review=0 verified=0 accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-008"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
