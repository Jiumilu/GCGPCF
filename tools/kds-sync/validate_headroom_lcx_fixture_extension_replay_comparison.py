#!/usr/bin/env python3
"""Validate Headroom LCX fixture extension replay/comparison evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_fixture_extension_replay_comparison.py"


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

    require(evidence.get("evidence_id") == "HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622", "invalid evidence id")
    require(evidence.get("status") == "fixture_extension_replay_comparison_pass_no_measurement", "invalid status")
    require(evidence.get("scope") == "sanitized_fixture_metadata_replay_comparison_only", "invalid scope")
    require(evidence.get("project_count") == 5, "project count mismatch")
    require(evidence.get("scenario_count") == 3, "scenario count mismatch")
    require(evidence.get("entry_count") == 15, "entry count mismatch")
    require(evidence.get("replay_record_count") == 15, "replay record count mismatch")
    require(evidence.get("comparison_count") == 15, "comparison count mismatch")
    require(evidence.get("mapping_failures") == [], "mapping failures must be empty")
    require(evidence.get("comparison_failures") == [], "comparison failures must be empty")
    require(evidence.get("calculation", {}).get("saving_rate") == "not_calculated", "saving rate must not be calculated")
    require(evidence.get("calculation", {}).get("tokens_saved") == "not_calculated", "tokens saved must not be calculated")

    records = evidence.get("replay_records", [])
    comparisons = evidence.get("comparisons", [])
    require(len(records) == 15 and len(comparisons) == 15, "record/comparison count mismatch")
    require({record.get("project_id") for record in records} == {"GPCF", "KDS", "Brain", "WAES", "GFIS"}, "project coverage mismatch")
    require({record.get("content_type") for record in records} == {"loop_gate_metadata", "retrieval_context_metadata", "tool_output_metadata"}, "scenario coverage mismatch")
    for record in records:
        require(record.get("marker_gate") == "fixture_marker_preserved", "marker gate mismatch")
        require(record.get("answer_equivalence") == "not_measured", "answer equivalence must remain not_measured")
        require(record.get("sensitive_redaction_gate") == "pass", "redaction gate mismatch")
        require(record.get("ccr_retrieval_miss_count") in {0, 1}, "retrieval miss fixture threshold mismatch")
    for comparison in comparisons:
        for key in [
            "marker_gate_preserved",
            "answer_equivalence_unmeasured",
            "sensitive_redaction_gate_pass",
            "ccr_retrieval_miss_count_within_fixture_threshold",
        ]:
            require(comparison.get(key) is True, f"comparison gate must be true: {key}")
        require(comparison.get("raw_text_compared") is False, "raw text must not be compared")
        require(comparison.get("production_tokens_compared") is False, "production tokens must not be compared")

    gates = evidence.get("gates", {})
    for key in [
        "fixture_extension_replay_comparison_gate",
        "metadata_replay_gate",
        "marker_retrieval_miss_comparison_gate",
        "metadata_only",
        "check_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "raw_text_compared",
        "production_tokens_compared",
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
        "HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622",
        "fixture_extension_replay_comparison_gate | true",
        "metadata_replay_gate | true",
        "marker_retrieval_miss_comparison_gate | true",
        "metadata_only | true",
        "saving_rate | not_calculated",
        "tokens_saved | not_calculated",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_fixture_extension_replay_comparison.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_fixture_extension_replay_comparison.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_fixture_extension_replay_comparison=pass_check_only "
        "project_count=5 scenario_count=3 entry_count=15 replay_record_count=15 "
        "comparison_count=15 metadata_only=true saving_rate=not_calculated "
        "measured_production_tokens=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
