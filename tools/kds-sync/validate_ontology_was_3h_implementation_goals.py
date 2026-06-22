#!/usr/bin/env python3
"""Validate the controlled 3-hour implementation goals for WAS/Ontology."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

EVIDENCE_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-implementation-goals-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/ontology-was-3h-implementation-goals-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-3H-GOALS-001.md"

REQUIRED_PHASES = [
    "P0-startup-calibration",
    "P1-real-source-record-readiness",
    "P2-gate-execution-and-replay",
    "P3-closure-and-next-decision",
]
ZERO_BASELINE_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
    "accepted_integrated",
    "production_ready",
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


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "ONTOLOGY-WAS-3H-IMPLEMENTATION-GOALS-20260621", "invalid evidence id")
    require(evidence.get("status") == "ontology_was_3h_implementation_goals_planned", "invalid evidence status")

    timebox = evidence.get("timebox", {})
    require(timebox.get("planned_minutes") == 180, "planned minutes must be 180")
    require(timebox.get("planned_hours") == 3, "planned hours must be 3")
    require(timebox.get("mode") == "controlled_phase_plan", "timebox mode mismatch")
    require(timebox.get("execution_started") is False, "execution_started must be false")

    baseline = evidence.get("current_baseline", {})
    require(baseline.get("latest_completed_round") == "GPCF-GFIS-WAS-SOURCE-RECORD-CROSSWALK-001", "latest baseline round mismatch")
    require(baseline.get("gfis_real_business_lane") == "repair_required", "GFIS real business lane must remain repair_required")
    for key in ZERO_BASELINE_KEYS:
        require(baseline.get(key) == 0, f"baseline.{key} must be 0")

    phases = evidence.get("phase_goals")
    require(isinstance(phases, list) and len(phases) == 4, "phase goals must have four phases")
    require([phase.get("phase_id") for phase in phases] == REQUIRED_PHASES, "phase order mismatch")
    for phase in phases:
        require(isinstance(phase.get("goal"), str) and phase["goal"], f"{phase.get('phase_id')}: goal missing")
        require(isinstance(phase.get("inputs"), list) and phase["inputs"], f"{phase.get('phase_id')}: inputs missing")
        require(isinstance(phase.get("deliverables"), list) and phase["deliverables"], f"{phase.get('phase_id')}: deliverables missing")
        require(isinstance(phase.get("exit_gate"), str) and phase["exit_gate"], f"{phase.get('phase_id')}: exit gate missing")

    metrics = evidence.get("success_metrics", {})
    require(metrics.get("planned_phase_count") == 4, "planned phase count mismatch")
    require(metrics.get("planned_minutes") == 180, "metrics planned minutes mismatch")
    require(metrics.get("minimum_required_validator_groups") >= 5, "validator group count too low")
    for gate in ["document_pollution", "kds_token", "loop_document_gate"]:
        require(gate in metrics.get("required_document_gates", []), f"missing document gate: {gate}")
    for forbidden in ["accepted", "integrated", "production_ready", "runtime_primary_key_ready_without_real_source_record"]:
        require(forbidden in metrics.get("forbidden_promotions", []), f"missing forbidden promotion: {forbidden}")

    stop_conditions = " ".join(evidence.get("stop_conditions", []))
    for phrase in ["KDS token", "document", "GFIS receiving directory", "production write", "Git push"]:
        require(phrase in stop_conditions, f"stop condition missing phrase: {phrase}")

    non_claims = evidence.get("non_claims", [])
    for phrase in [
        "does not start an autonomous 3-hour run",
        "does not write into GFIS receiving directory",
        "does not create real source-of-record",
        "does not mark accepted or integrated",
        "does not mark production ready",
    ]:
        require(phrase in non_claims, f"missing non-claim: {phrase}")

    for phrase in [
        "已建立 WAS/Ontology 后续 3 小时阶段性实施目标",
        "planned_minutes | `180`",
        "execution_started | `false`",
        "本 evidence 不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("Ontology/WAS 已具备 3 小时受控实施目标" in loop_round, "loop round missing feedback")

    print(
        "ontology_was_3h_implementation_goals=pass "
        "planned_minutes=180 planned_hours=3 phase_count=4 "
        "execution_started=false real_source_records=0 valid_source_records=0 "
        "runtime_primary_key_ready=0 accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
