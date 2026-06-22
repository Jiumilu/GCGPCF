#!/usr/bin/env python3
"""Validate Headroom LCX L3.5 synthetic answer-equivalence gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_l35_answer_equivalence_synthetic_gate.py"

PROJECTS = {
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
}
SCENARIOS = {"answer_summary", "citation_preservation", "project_boundary_marker"}


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
    require("synthetic_answer" in runner, "runner must build synthetic answers")
    require("business_answer_equivalence_proven" in runner, "runner must keep business equivalence false")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-20260622", "invalid evidence id")
    require(evidence.get("status") == "l3_5_answer_equivalence_synthetic_gate_pass_check_only", "invalid status")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("scenario_count") == 3, "scenario count mismatch")
    require(evidence.get("sample_count") == 45, "sample count mismatch")
    require(evidence.get("failures") == [], "failures must be empty")

    samples = evidence.get("samples", [])
    require(isinstance(samples, list) and len(samples) == 45, "samples mismatch")
    require({sample.get("project_id") for sample in samples} == PROJECTS, "project coverage mismatch")
    require({sample.get("scenario") for sample in samples} == SCENARIOS, "scenario coverage mismatch")
    for sample in samples:
        require(sample.get("answer_equivalence") == "synthetic_equivalent", "answer equivalence marker mismatch")
        for gate in [
            "answer_equivalence_gate",
            "citation_preservation_gate",
            "marker_preservation_gate",
            "project_boundary_gate",
        ]:
            require(sample.get(gate) is True, f"sample gate must be true: {gate}")
        require(sample.get("sensitive_redaction_gate") == "pass", "sensitive gate mismatch")
        require(sample.get("before_hash") == sample.get("after_hash"), "hash mismatch")
        before = sample.get("before_answer", {})
        after = sample.get("after_answer", {})
        require(before.get("project_id") == after.get("project_id") == sample.get("project_id"), "answer project mismatch")
        require(before.get("citations") == after.get("citations"), "citation mismatch")
        require(before.get("markers") == after.get("markers"), "marker mismatch")
        for key in ["tokens_saved", "saving_rate"]:
            require(sample.get(key) == "not_calculated", f"{key} must not be calculated")
        for key in ["measured_production_tokens", "accepted", "integrated", "production_ready"]:
            require(sample.get(key) is False, f"sample field must be false: {key}")

    gates = evidence.get("gates", {})
    for key in [
        "l3_5_answer_equivalence_synthetic_gate",
        "source_multi_window_stability_gate",
        "project_coverage_gate",
        "sample_count_gate",
        "answer_equivalence_gate",
        "citation_preservation_gate",
        "marker_preservation_gate",
        "project_boundary_gate",
        "synthetic_only",
        "metadata_only",
        "check_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "business_answer_equivalence_proven",
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "headroom_learn_apply_executed",
        "l4_candidate",
        "l5_candidate",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-20260622",
        "sample_count: `45`",
        "l3_5_answer_equivalence_synthetic_gate | true",
        "business_answer_equivalence_proven | false",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in ["run:", "stop:", "verify:", "recover:", "debug:"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")
    require("validate_headroom_lcx_l35_answer_equivalence_synthetic_gate.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_l35_answer_equivalence_synthetic_gate=pass_check_only "
        "project_count=15 scenario_count=3 sample_count=45 answer_equivalence_gate=true "
        "business_answer_equivalence_proven=false l4_candidate=false measured_production_tokens=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
