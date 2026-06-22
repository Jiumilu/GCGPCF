#!/usr/bin/env python3
"""Validate Headroom LCX P3 learn-preview and working-memory gate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_p3_learn_preview_working_memory_gate.py"
LEARN_PREVIEW = ROOT / "loop/context/headroom/scripts/learn-preview.sh"

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
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    learn_preview = read(LEARN_PREVIEW)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("--preview" not in learn_preview, "learn-preview wrapper must not use unsupported --preview")
    require("--apply" not in learn_preview, "learn-preview wrapper must not pass --apply")
    require("learn_apply_executed" in runner, "runner must record no learn apply")
    require("empty_project_only" in runner, "runner must use empty project only")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("telemetry") == "off", "telemetry must be off")
    learn = evidence.get("learn_preview", {})
    require(learn.get("learn_preview_gate") is True, "learn preview gate must pass")
    require(learn.get("empty_project_only") is True, "learn preview must use empty project only")
    require(learn.get("real_session_scanned") is False, "real sessions must not be scanned")
    require(learn.get("llm_analysis_executed") is False, "LLM analysis must not execute")
    require(learn.get("learn_apply_executed") is False, "learn apply must not execute")
    memory = evidence.get("working_memory_gate", {})
    require(memory.get("apply_guard_gate") is True, "apply guard gate must pass")
    require(memory.get("approval_fixture_synthetic") is True, "approval fixture must be synthetic")
    require(memory.get("apply_manually_only") is True, "memory apply must remain manual only")
    require(memory.get("controlled_rules_modified") is False, "controlled rules must not be modified")
    require(memory.get("headroom_memory_as_kds_source_of_record") is False, "Headroom memory must not become KDS source")
    require(memory.get("cross_project_memory_as_fact") is False, "cross-project memory must not become fact")
    gates = evidence.get("gates", {})
    for key in [
        "p3_learn_preview_working_memory_gate",
        "learn_preview_gate",
        "apply_guard_gate",
        "memory_governance_gate",
        "telemetry_default_off",
        "synthetic_input_only",
        "empty_project_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "real_session_scanned",
        "llm_analysis_executed",
        "learn_apply_executed",
        "controlled_rules_modified",
        "raw_sensitive_context_stored",
        "external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-20260621",
        "p3_learn_preview_working_memory_gate | true",
        "learn_preview_gate | true",
        "apply_guard_gate | true",
        "memory_governance_gate | true",
        "real_session_scanned | false",
        "learn_apply_executed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_p3_learn_preview_working_memory_gate.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_p3_learn_preview_working_memory_gate.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_p3_learn_preview_working_memory_gate=pass "
        "project_count=15 learn_preview_gate=true apply_guard_gate=true "
        "memory_governance_gate=true production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
