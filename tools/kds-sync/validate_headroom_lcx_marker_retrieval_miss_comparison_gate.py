#!/usr/bin/env python3
"""Validate Headroom LCX marker/retrieval-miss comparison gate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_marker_retrieval_miss_comparison_gate.py"

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

ALLOWED_COMPARE_FIELDS = [
    "marker_gate",
    "sensitive_redaction_gate",
    "ccr_retrieval_miss_count",
    "answer_equivalence",
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
    require("ALLOWED_COMPARE_FIELDS" in runner, "runner must define allowed fields")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-20260622", "invalid evidence id")
    require(evidence.get("status") == "marker_retrieval_miss_comparison_gate_pass_no_measurement", "invalid status")
    require(evidence.get("scope") == "sanitized_metadata_comparison_only", "invalid scope")
    require(evidence.get("project_count") == 15 and evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("allowed_compare_fields") == ALLOWED_COMPARE_FIELDS, "allowed compare fields mismatch")
    require(evidence.get("entry_count") == 1, "entry count mismatch")
    require(evidence.get("comparison_count") == 1, "comparison count mismatch")
    require(evidence.get("comparison_failures") == [], "comparison failures must be empty")
    require(evidence.get("calculation", {}).get("saving_rate") == "not_calculated", "saving rate must not be calculated")
    require(evidence.get("calculation", {}).get("tokens_saved") == "not_calculated", "tokens saved must not be calculated")

    comparisons = evidence.get("comparisons", [])
    require(isinstance(comparisons, list) and len(comparisons) == 1, "comparisons mismatch")
    comparison = comparisons[0]
    require(comparison.get("project_id") == "GPCF", "project id mismatch")
    require(comparison.get("compared_fields", {}).get("marker_gate") == "not_measured", "marker gate must remain not_measured")
    require(comparison.get("compared_fields", {}).get("answer_equivalence") == "not_measured", "answer equivalence must remain not_measured")
    require(comparison.get("compared_fields", {}).get("sensitive_redaction_gate") == "pass", "redaction gate mismatch")
    require(comparison.get("compared_fields", {}).get("ccr_retrieval_miss_count") == 0, "retrieval miss count mismatch")
    for key in [
        "marker_gate_preserved",
        "answer_equivalence_preserved",
        "sensitive_redaction_gate_pass",
        "ccr_retrieval_miss_count_zero",
    ]:
        require(comparison.get(key) is True, f"comparison gate must be true: {key}")
    for key in ["raw_text_compared", "production_tokens_compared"]:
        require(comparison.get(key) is False, f"comparison gate must be false: {key}")

    gates = evidence.get("gates", {})
    for key in ["marker_retrieval_miss_comparison_gate", "metadata_only", "check_only"]:
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
        "HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-20260622",
        "marker_retrieval_miss_comparison_gate | true",
        "metadata_only | true",
        "raw_text_compared | false",
        "production_tokens_compared | false",
        "saving_rate | not_calculated",
        "tokens_saved | not_calculated",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_marker_retrieval_miss_comparison_gate.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_marker_retrieval_miss_comparison_gate.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_marker_retrieval_miss_comparison_gate=pass_check_only "
        "project_count=15 entry_count=1 comparison_count=1 metadata_only=true "
        "saving_rate=not_calculated measured_production_tokens=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
