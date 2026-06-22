#!/usr/bin/env python3
"""Validate the controlled P0 start record for the WAS/Ontology 3-hour run."""

from __future__ import annotations

import fnmatch
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_RECEIVING_DIR = Path(
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/"
    "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/"
    "customer-requirement-or-platform-order"
)

EVIDENCE_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p0-start-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/ontology-was-3h-p0-start-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-3H-P0-START-001.md"
PLAN_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-implementation-goals-20260621.json"

ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]

ALLOWED_NON_REAL_PATTERNS = [
    "README.md",
    "*.template.json",
    "pending-business-verification/README.md",
    "pending-business-verification/*.schema.json",
    "rejected-examples/*.customer-requirement-platform-order.source-record.json",
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


def is_allowed_non_real_file(path: Path) -> bool:
    rel = path.relative_to(GFIS_RECEIVING_DIR).as_posix()
    return any(fnmatch.fnmatch(rel, pattern) for pattern in ALLOWED_NON_REAL_PATTERNS)


def count_real_source_record_files() -> int:
    require(GFIS_RECEIVING_DIR.exists(), f"GFIS receiving directory missing: {GFIS_RECEIVING_DIR}")
    count = 0
    for path in GFIS_RECEIVING_DIR.rglob("*"):
        if not path.is_file():
            continue
        if is_allowed_non_real_file(path):
            continue
        if path.name.endswith(".customer-requirement-platform-order.source-record.json"):
            count += 1
    return count


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    plan = load_json(PLAN_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "ONTOLOGY-WAS-3H-P0-START-20260621", "invalid evidence id")
    require(evidence.get("status") == "ontology_was_3h_p0_started", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-3H-P0-START-001", "invalid round id")
    require(evidence.get("plan_ref") == plan.get("evidence_id"), "plan ref mismatch")

    phase = evidence.get("phase", {})
    require(phase.get("phase_id") == "P0-startup-calibration", "phase id mismatch")
    require(phase.get("time_window_minutes") == "0-30", "phase time window mismatch")
    require(phase.get("execution_started") is True, "execution_started must be true")
    require(phase.get("execution_mode") == "controlled_local_evidence_run", "execution mode mismatch")

    startup = evidence.get("startup_assertions", {})
    require(startup.get("planned_minutes") == 180, "planned minutes mismatch")
    require(startup.get("planned_hours") == 3, "planned hours mismatch")
    require(startup.get("current_phase") == "P0-startup-calibration", "current phase mismatch")
    require(startup.get("next_phase") == "P1-real-source-record-readiness", "next phase mismatch")
    require(startup.get("gfis_real_business_lane") == "repair_required", "GFIS lane must remain repair_required")
    for key in ZERO_KEYS:
        require(startup.get(key) == 0, f"{key} must be 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(startup.get(key) is False, f"{key} must be false")

    scan = evidence.get("gfis_receiving_directory_scan", {})
    real_files = count_real_source_record_files()
    require(scan.get("expected_real_source_record_files") == 0, "expected real files must be 0")
    require(scan.get("real_source_record_files_found") == real_files == 0, "GFIS real source-record files must be 0")

    required_outputs = evidence.get("gate_outputs_required_for_p0_exit", [])
    for phrase in [
        "ontology_was_3h_implementation_goals=pass",
        "gfis_was_source_record_field_crosswalk=pass",
        "gfis_was_source_record_negative_fixtures=pass",
        "gfis_was_source_record_submission_precheck=pass",
        "gfis_was_source_record_admission_gate=pass",
        "gfis_was_profile_runtime_gate_mapping=pass",
        "was_project_group_admission=pass",
        "WAS okf validators pass",
    ]:
        require(phrase in required_outputs, f"missing required P0 output: {phrase}")

    exit_gate = evidence.get("p0_exit_gate", {})
    require(exit_gate.get("status") == "pass", "P0 exit gate status mismatch")
    require(exit_gate.get("promotion_allowed") is False, "promotion must not be allowed")
    replay = evidence.get("baseline_validator_replay", {})
    require(replay.get("status") == "pass", "baseline validator replay must pass")
    require(len(replay.get("commands", [])) >= 8, "baseline validator replay command coverage too low")
    outputs = " ".join(replay.get("outputs", []))
    for phrase in [
        "ontology_was_3h_implementation_goals=pass",
        "gfis_was_source_record_submission_precheck=pass",
        "hold_required=1",
        "real_business_lane=repair_required",
        "was_project_group_admission=pass",
        "PASS validate_was_dimensions",
    ]:
        require(phrase in outputs, f"baseline replay missing output phrase: {phrase}")

    for phrase in [
        "does not complete the full 3-hour plan",
        "does not write into GFIS receiving directory",
        "does not create real source-of-record",
        "does not mark accepted or integrated",
        "does not mark production ready",
    ]:
        require(phrase in evidence.get("non_claims", []), f"missing non-claim: {phrase}")

    for phrase in [
        "已开始执行 3 小时阶段目标的 P0 启动校准",
        "execution_started | `true`",
        "real_source_record_files_found | `0`",
        "p0_exit_gate.status | `pass`",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("Ontology/WAS 3 小时目标已进入 P0 启动校准" in loop_round, "loop round missing feedback")

    print(
        "ontology_was_3h_p0_start=pass "
        "phase=P0-startup-calibration execution_started=true planned_minutes=180 "
        "real_source_record_files=0 real_source_records=0 valid_source_records=0 "
        "runtime_primary_key_ready=0 accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
