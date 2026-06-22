#!/usr/bin/env python3
"""Validate the P3 closure evidence for WAS/Ontology."""

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

EVIDENCE_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p3-closure-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/ontology-was-3h-p3-closure-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-3H-P3-CLOSURE-001.md"
PLAN_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-implementation-goals-20260621.json"
P2_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p2-gate-replay-20260621.json"

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
        if not path.is_file() or is_allowed_non_real_file(path):
            continue
        if path.name.endswith(".customer-requirement-platform-order.source-record.json"):
            count += 1
    return count


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    plan = load_json(PLAN_JSON)
    p2 = load_json(P2_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "ONTOLOGY-WAS-3H-P3-CLOSURE-20260621", "invalid evidence id")
    require(evidence.get("status") == "ontology_was_3h_p3_closure_pass", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-3H-P3-CLOSURE-001", "invalid round id")
    require(evidence.get("plan_ref") == plan.get("evidence_id"), "plan ref mismatch")
    require(evidence.get("previous_round") == p2.get("round_id"), "previous round mismatch")

    phase = evidence.get("phase", {})
    require(phase.get("phase_id") == "P3-closure-and-next-decision", "phase id mismatch")
    require(phase.get("time_window_minutes") == "135-180", "time window mismatch")
    require(phase.get("execution_started") is True, "execution_started must be true")
    require(phase.get("execution_mode") == "controlled_document_governance_closure", "execution mode mismatch")

    chain = evidence.get("phase_chain_summary", {})
    require(chain.get("planned_phase_count") == 4, "planned phase count mismatch")
    require(chain.get("completed_phase_count") == 4, "completed phase count mismatch")
    for key in ["p0_status", "p1_status", "p2_status", "p3_status"]:
        require(chain.get(key) == "pass", f"{key} must pass")

    governance = evidence.get("document_governance_closure", {})
    for key in ["document_control", "document_pollution", "kds_token", "loop_document_gate"]:
        require(governance.get(key) == "pass", f"{key} must pass")
    require(governance.get("missing_metadata") == 0, "missing metadata must be 0")
    require(governance.get("missing_readme_dirs") == 0, "missing README dirs must be 0")
    require(governance.get("loop_repo_md") >= 1750, "loop repo md count too low")
    require(governance.get("loop_kds_md") >= governance.get("loop_repo_md"), "KDS md count must cover repo md count")

    boundary = evidence.get("business_boundary_closure", {})
    require(boundary.get("gfis_receiving_directory_real_source_record_files") == count_real_source_record_files() == 0, "GFIS real source-record files must be 0")
    require(boundary.get("submitted_files_found") == 0, "submitted_files_found must be 0")
    require(boundary.get("accepted_for_next_gate") == 0, "accepted_for_next_gate must be 0")
    require(boundary.get("hold_required") == 1, "hold_required must be 1")
    require(boundary.get("gfis_real_business_lane") == "repair_required", "GFIS lane must remain repair_required")
    for key in ZERO_KEYS:
        require(boundary.get(key) == 0, f"{key} must be 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"{key} must be false")

    decision = evidence.get("next_decision_boundary", {})
    require(decision.get("recommended_next_round") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-INTAKE-PACK-001", "recommended next round mismatch")
    require(len(decision.get("allowed_next_actions", [])) >= 4, "allowed next actions too few")
    for blocked in ["create runtime primary key", "mark accepted or integrated", "mark production ready"]:
        require(blocked in decision.get("blocked_actions_without_real_input", []), f"missing blocked action: {blocked}")

    exit_gate = evidence.get("p3_exit_gate", {})
    require(exit_gate.get("status") == "pass", "P3 exit gate must pass")
    require(exit_gate.get("promotion_allowed") is False, "promotion must not be allowed")

    for phrase in [
        "phase_id | `P3-closure-and-next-decision`",
        "document_control | `pass`",
        "loop_document_gate | `pass`",
        "gfis_receiving_directory_real_source_record_files | `0`",
        "p3_exit_gate.status | `pass`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("Ontology/WAS 3 小时阶段目标已完成 P3 收口" in loop_round, "loop round missing feedback")

    print(
        "ontology_was_3h_p3_closure=pass "
        "phase=P3-closure-and-next-decision completed_phase_count=4 "
        "document_control=pass document_pollution=pass kds_token=pass loop_document_gate=pass "
        "gfis_real_source_record_files=0 hold_required=1 real_source_records=0 "
        "valid_source_records=0 runtime_primary_key_ready=0 accepted=false integrated=false "
        "production_ready=false next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-INTAKE-PACK-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
