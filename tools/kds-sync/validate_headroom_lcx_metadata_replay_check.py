#!/usr/bin/env python3
"""Validate Headroom LCX sanitized metadata replay check evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_metadata_replay_check.py"

PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require("--check-only is required" in runner, "runner must require --check-only")
    require("FIELD_MAP" in runner, "runner must define field map")
    require("not_calculated" in runner, "runner must not calculate savings")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-METADATA-REPLAY-CHECK-20260622", "invalid evidence id")
    require(evidence.get("status") == "metadata_replay_check_pass_no_measurement", "invalid status")
    require(evidence.get("scope") == "sanitized_metadata_replay_check_only", "invalid scope")
    require(evidence.get("project_count") == 15 and evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("entry_count") == 1, "entry count mismatch")
    require(evidence.get("replay_record_count") == 1, "replay record count mismatch")
    require(evidence.get("mapping_failures") == [], "mapping failures must be empty")
    require(evidence.get("marker_failures") == [], "marker failures must be empty")
    require(evidence.get("calculation", {}).get("saving_rate") == "not_calculated", "saving rate must not be calculated")
    require(evidence.get("calculation", {}).get("tokens_saved") == "not_calculated", "tokens saved must not be calculated")

    field_map = evidence.get("field_map", {})
    for source, target in {
        "measurement_id": "task_id_candidate",
        "project": "project_id",
        "scenario": "content_type",
        "sensitive_redaction_gate": "sensitive_redaction_gate",
        "project_marker_gate": "marker_gate",
        "retrieval_miss_count": "ccr_retrieval_miss_count",
    }.items():
        require(field_map.get(source) == target, f"field map mismatch: {source}")

    schema_checks = evidence.get("schema_checks", {})
    for key in [
        "ledger_is_sanitized_precheck_template",
        "dry_run_gate_passed",
        "dry_run_check_only",
        "no_raw_prompt",
        "no_raw_completion",
        "no_customer_contract_text",
        "no_provider_secret",
        "telemetry_off",
    ]:
        require(schema_checks.get(key) is True, f"schema check must be true: {key}")

    records = evidence.get("replay_records", [])
    require(isinstance(records, list) and len(records) == 1, "replay records mismatch")
    record = records[0]
    require(record.get("project_id") == "GPCF", "project marker must be GPCF")
    require(record.get("marker_gate") == "not_measured", "marker gate must remain not_measured")
    require(record.get("sensitive_redaction_gate") == "pass", "sensitive redaction gate must pass")
    require(record.get("ccr_retrieval_miss_count") == 0, "retrieval miss count mismatch")

    gates = evidence.get("gates", {})
    for key in ["metadata_replay_gate", "field_mapping_gate", "project_marker_gate", "evidence_schema_gate", "check_only"]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-METADATA-REPLAY-CHECK-20260622",
        "metadata_replay_gate | true",
        "field_mapping_gate | true",
        "project_marker_gate | true",
        "evidence_schema_gate | true",
        "check_only | true",
        "saving_rate | not_calculated",
        "tokens_saved | not_calculated",
        "production_token_measurement_allowed | false",
        "measured_production_tokens | false",
        "production_proxy_started | false",
        "kds_api_write | false",
        "sensitive_material_processed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_metadata_replay_check.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_metadata_replay_check.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_metadata_replay_check=pass_check_only "
        "project_count=15 entry_count=1 replay_record_count=1 check_only=true "
        "saving_rate=not_calculated measured_production_tokens=false "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
