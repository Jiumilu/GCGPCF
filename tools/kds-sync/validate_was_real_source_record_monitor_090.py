#!/usr/bin/env python3
"""Validate WAS real source-record monitor round 090."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-090-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-monitor-090-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-090.md"
SOURCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-monitor-089-20260622.json"
INTAKE_DIR = ROOT / "docs/harness/intake"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
ZERO_KEYS = ["real_source_records", "valid_source_records", "runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]
FALSE_KEYS = ["accepted", "integrated", "production_ready"]
MONITOR_KEYS = [
    "meter_calibration_certificate_gaps",
    "mrv_data_acquisition_log_gaps",
    "emissions_calculation_workbook_gaps",
    "digital_chain_of_custody_signature_gaps",
    "mrv_anomaly_correction_record_gaps",
    "third_party_verifier_data_package_gaps",
    "retention_access_control_log_gaps",
    "accepted_for_digital_mrv_profile",
]
REQUIREMENTS = [
    "meter_calibration_certificate",
    "mrv_data_acquisition_log",
    "emissions_calculation_workbook",
    "digital_chain_of_custody_signature",
    "mrv_anomaly_correction_record",
    "third_party_verifier_data_package",
    "retention_access_control_log",
]
REQUIRED_COMMANDS = [
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py"],
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_admission_gate.py"],
    ["python3", "tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py"],
    ["python3", "tools/kds-sync/validate_ontology_was_real_source_record_intake_pack.py"],
    ["python3", "tools/kds-sync/validate_was_real_source_record_candidate_precheck.py"],
]
MD_PHRASES = [
    "submitted_real_candidate_files | `0`",
    "meter_calibration_certificate_gaps | `0`",
    "mrv_data_acquisition_log_gaps | `0`",
    "emissions_calculation_workbook_gaps | `0`",
    "digital_chain_of_custody_signature_gaps | `0`",
    "mrv_anomaly_correction_record_gaps | `0`",
    "third_party_verifier_data_package_gaps | `0`",
    "retention_access_control_log_gaps | `0`",
    "accepted_for_digital_mrv_profile | `0`",
    "accepted_for_next_gate | `0`",
    "hold_required | `1`",
    "production_ready | `False`",
]
LOOP_CASES = [
    "meter_calibration_certificate_gap",
    "mrv_data_acquisition_log_gap",
    "emissions_calculation_workbook_gap",
    "digital_chain_of_custody_signature_gap",
    "mrv_anomaly_correction_record_gap",
    "third_party_verifier_data_package_gap",
    "retention_access_control_log_gap",
]
NEGATIVE_FIXTURES = [
    "real-source-record-monitor-090-negative-meter_calibration_certificate_gap.json",
    "real-source-record-monitor-090-negative-mrv_data_acquisition_log_gap.json",
    "real-source-record-monitor-090-negative-emissions_calculation_workbook_gap.json",
    "real-source-record-monitor-090-negative-digital_chain_of_custody_signature_gap.json",
    "real-source-record-monitor-090-negative-mrv_anomaly_correction_record_gap.json",
    "real-source-record-monitor-090-negative-third_party_verifier_data_package_gap.json",
    "real-source-record-monitor-090-negative-retention_access_control_log_gap.json",
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
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
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
    for key in MONITOR_KEYS:
        if value.get(key, 0) != 0:
            failures.append(f"{key}_must_be_zero")
    if value.get("accepted_for_next_gate", 0) != 0:
        failures.append("accepted_for_next_gate_must_be_zero")
    if value.get("hold_required") != 1:
        failures.append("hold_required_must_be_one")
    if value.get("digital_mrv_state") != "blocked_no_real_source_record":
        failures.append("digital_mrv_state_must_remain_blocked")
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
    source = load_json(SOURCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-MONITOR-090-20260622", "invalid evidence id")
    require(evidence.get("status") == "was_real_source_record_monitor_090_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-090", "invalid round id")
    require(evidence.get("source_round") == source.get("round_id"), "source round mismatch")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    require(evidence.get("required_commands") == [" ".join(command) for command in REQUIRED_COMMANDS], "required command list mismatch")
    require(evidence.get("digital_mrv_requirements") == REQUIREMENTS, "digital MRV requirements mismatch")

    checks = evidence.get("monitor_checks", {})
    require(checks.get("submitted_real_candidate_files") == len(candidate_files()) == 0, "submitted candidate count mismatch")
    for key in MONITOR_KEYS:
        require(checks.get(key) == 0, f"{key} must be 0")
    require(checks.get("accepted_for_next_gate") == 0, "accepted_for_next_gate must be 0")
    require(checks.get("hold_required") == 1, "hold_required must be 1")
    require(checks.get("digital_mrv_state") == "blocked_no_real_source_record", "digital MRV state mismatch")

    positive = load_json(FIXTURE_DIR / "real-source-record-monitor-090-positive.json")
    require(not monitor_failures(positive), "positive fixture should pass")
    negatives = [FIXTURE_DIR / name for name in NEGATIVE_FIXTURES]
    require(len(negatives) == 7, "negative fixture count must be 7")
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
    for phrase in MD_PHRASES:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("真实 P4 输入 monitor 090 已建立" in loop_round, "loop round debug missing")
    for phrase in LOOP_CASES:
        require(phrase in loop_round, f"loop round missing digital MRV case: {phrase}")
    for heading in ["## run", "## stop", "## verify", "## recover", "## debug"]:
        require(heading in loop_round, f"loop round missing five-direction heading: {heading}")
    print(
        "was_real_source_record_monitor_090=pass submitted_real_candidate_files=0 "
        "meter_calibration_certificate_gaps=0 mrv_data_acquisition_log_gaps=0 "
        "emissions_calculation_workbook_gaps=0 digital_chain_of_custody_signature_gaps=0 "
        "mrv_anomaly_correction_record_gaps=0 third_party_verifier_data_package_gaps=0 "
        "retention_access_control_log_gaps=0 accepted_for_digital_mrv_profile=0 "
        "accepted_for_next_gate=0 hold_required=1 real_source_records=0 valid_source_records=0 "
        "runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-091"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
