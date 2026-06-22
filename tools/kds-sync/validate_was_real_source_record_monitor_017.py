#!/usr/bin/env python3
"""Validate WAS real source-record monitor round 017."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-017-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-monitor-017-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-017.md"
PREVIOUS_MONITOR_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-016-20260621.json"
INTAKE_DIR = ROOT / "docs/harness/intake"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
ZERO_KEYS = ["real_source_records", "valid_source_records", "runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]
FALSE_KEYS = ["accepted", "integrated", "production_ready"]
FULFILLMENT_KEYS = [
    "customer_acceptance_evidence_gaps",
    "delivery_confirmation_gaps",
    "after_sales_service_gaps",
    "dispute_claim_record_gaps",
    "return_repair_replacement_gaps",
    "compensation_settlement_gaps",
    "accepted_for_fulfillment_closure_profile",
]
REQUIRED_COMMANDS = [
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py"],
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_admission_gate.py"],
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py"],
    ["python3", "tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py"],
    ["python3", "tools/kds-sync/validate_was_real_source_record_candidate_precheck.py"],
    ["python3", "tools/kds-sync/validate_was_real_source_record_monitor_016.py"],
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


def monitor_failures(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if value.get("submitted_real_candidate_files") != 0:
        failures.append("submitted_real_candidate_files_must_be_zero")
    for key in FULFILLMENT_KEYS:
        if value.get(key, 0) != 0:
            failures.append(f"{key}_must_be_zero")
    if value.get("accepted_for_next_gate", 0) != 0:
        failures.append("accepted_for_next_gate_must_be_zero")
    if value.get("hold_required") != 1:
        failures.append("hold_required_must_be_one")
    if value.get("fulfillment_closure_state") != "blocked_no_real_source_record":
        failures.append("fulfillment_closure_state_must_remain_blocked")
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
    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-MONITOR-017-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_real_source_record_monitor_017_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-017", "invalid round id")
    require(evidence.get("source_round") == previous.get("round_id"), "source round mismatch")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    require(evidence.get("required_commands") == [" ".join(command) for command in REQUIRED_COMMANDS], "required command list mismatch")
    require(evidence.get("fulfillment_closure_requirements") == [
        "customer_acceptance_evidence",
        "delivery_confirmation",
        "after_sales_service_record",
        "dispute_claim_record",
        "return_repair_replacement_record",
        "compensation_settlement_record",
    ], "fulfillment closure requirements mismatch")

    submitted = candidate_files()
    checks = evidence.get("monitor_checks", {})
    require(checks.get("submitted_real_candidate_files") == len(submitted) == 0, "submitted candidate count mismatch")
    for key in FULFILLMENT_KEYS:
        require(checks.get(key) == 0, f"{key} must be 0")
    require(checks.get("accepted_for_next_gate") == 0, "accepted_for_next_gate must be 0")
    require(checks.get("hold_required") == 1, "hold_required must be 1")
    require(checks.get("fulfillment_closure_state") == "blocked_no_real_source_record", "fulfillment closure state mismatch")

    positive = load_json(FIXTURE_DIR / "real-source-record-monitor-017-positive.json")
    require(not monitor_failures(positive), "positive fixture should pass")
    negatives = sorted(FIXTURE_DIR.glob("real-source-record-monitor-017-negative-*.json"))
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
        "customer_acceptance_evidence_gaps | `0`",
        "delivery_confirmation_gaps | `0`",
        "after_sales_service_gaps | `0`",
        "dispute_claim_record_gaps | `0`",
        "return_repair_replacement_gaps | `0`",
        "compensation_settlement_gaps | `0`",
        "accepted_for_fulfillment_closure_profile | `0`",
        "accepted_for_next_gate | `0`",
        "hold_required | `1`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("真实 P4 输入 monitor 017 已建立" in loop_round, "loop round feedback missing")
    for phrase in [
        "customer_acceptance_evidence_gap",
        "delivery_confirmation_gap",
        "after_sales_service_gap",
        "dispute_claim_record_gap",
        "return_repair_replacement_gap",
        "compensation_settlement_gap",
    ]:
        require(phrase in loop_round, f"loop round missing fulfillment closure case: {phrase}")

    print(
        "was_real_source_record_monitor_017=pass "
        "submitted_real_candidate_files=0 customer_acceptance_evidence_gaps=0 delivery_confirmation_gaps=0 "
        "after_sales_service_gaps=0 dispute_claim_record_gaps=0 return_repair_replacement_gaps=0 "
        "compensation_settlement_gaps=0 accepted_for_fulfillment_closure_profile=0 "
        "accepted_for_next_gate=0 hold_required=1 real_source_records=0 valid_source_records=0 "
        "runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-018"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
