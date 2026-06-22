#!/usr/bin/env python3
"""Validate the P1 source-record readiness evidence for WAS/Ontology."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

EVIDENCE_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p1-source-record-readiness-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/ontology-was-3h-p1-source-record-readiness-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-3H-P1-SOURCE-READINESS-001.md"
PLAN_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-implementation-goals-20260621.json"
P0_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p0-start-20260621.json"
CROSSWALK_JSON = ROOT / "docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.json"
NEGATIVE_JSON = ROOT / "docs/harness/evidence/gfis-was-source-record-negative-fixtures-20260621.json"
PRECHECK_JSON = ROOT / "docs/harness/evidence/gfis-was-source-record-submission-precheck-20260621.json"


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
    plan = load_json(PLAN_JSON)
    p0 = load_json(P0_JSON)
    crosswalk = load_json(CROSSWALK_JSON)
    negative = load_json(NEGATIVE_JSON)
    precheck = load_json(PRECHECK_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "ONTOLOGY-WAS-3H-P1-SOURCE-RECORD-READINESS-20260621", "invalid evidence id")
    require(evidence.get("status") == "ontology_was_3h_p1_source_record_readiness_ready", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-3H-P1-SOURCE-READINESS-001", "invalid round id")
    require(evidence.get("plan_ref") == plan.get("evidence_id"), "plan ref mismatch")
    require(evidence.get("previous_round") == p0.get("round_id"), "previous round mismatch")

    phase = evidence.get("phase", {})
    require(phase.get("phase_id") == "P1-real-source-record-readiness", "phase id mismatch")
    require(phase.get("time_window_minutes") == "30-75", "phase time window mismatch")
    require(phase.get("execution_started") is True, "P1 execution_started must be true")

    contract = evidence.get("source_contract", {})
    require(contract.get("object_family") == "CustomerRequirementOrPlatformOrder", "object family mismatch")
    require(contract.get("required_gfis_native_field_count") == len(precheck.get("gfis_native_required_fields", [])) == 12, "GFIS required field count mismatch")
    require(contract.get("required_was_field_count") == len(precheck.get("was_required_fields", [])) == 12, "WAS required field count mismatch")
    require(contract.get("crosswalk_entry_count") == len(crosswalk.get("crosswalk", [])) == 12, "crosswalk count mismatch")
    require(contract.get("negative_fixture_reject_count") == negative.get("fixture_summary", {}).get("rejected_fixture_count") == 6, "negative reject count mismatch")
    require(contract.get("current_submitted_files_found") == precheck.get("directory_scan", {}).get("submitted_files_found") == 0, "submitted files must be 0")
    require(contract.get("current_accepted_for_next_gate") == precheck.get("directory_scan", {}).get("accepted_for_next_gate") == 0, "accepted_for_next_gate must be 0")
    require(contract.get("current_hold_required") == precheck.get("directory_scan", {}).get("hold_required") == 1, "hold_required must be 1")

    checklist = evidence.get("operator_facing_intake_checklist", [])
    matrix = evidence.get("field_completion_matrix", [])
    hold_reasons = evidence.get("hold_reason_catalog", [])
    rejections = evidence.get("explicit_rejection_sources", [])
    metrics = evidence.get("readiness_metrics", {})

    require(len(checklist) == metrics.get("checklist_items") == 5, "checklist count mismatch")
    require(len(matrix) == metrics.get("field_completion_entries") == 12, "matrix count mismatch")
    require(sum(1 for row in matrix if row.get("completion_state") == "ready_by_rule") == metrics.get("ready_by_rule_entries") == 9, "ready_by_rule count mismatch")
    require(sum(1 for row in matrix if row.get("completion_state") == "missing_real_input") == metrics.get("missing_real_input_entries") == 3, "missing_real_input count mismatch")
    require(len(hold_reasons) == metrics.get("hold_reasons") == 12, "hold reason count mismatch")
    require(len(rejections) == metrics.get("explicit_rejection_sources") == 6, "rejection source count mismatch")

    for field in precheck.get("was_required_fields", []):
        require(any(row.get("was_field") == field for row in matrix), f"missing WAS field in matrix: {field}")
    for source in ["gfis_demo", "formal_quotation_only", "contract_review_draft_only", "kds_candidate_without_owner_confirmation", "loop_document_only", "user_statement_only"]:
        require(source in rejections, f"missing rejection source: {source}")

    for key in ["real_source_records", "valid_source_records", "runtime_primary_key_ready"]:
        require(metrics.get(key) == 0, f"{key} must be 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(metrics.get(key) is False, f"{key} must be false")

    exit_gate = evidence.get("p1_exit_gate", {})
    require(exit_gate.get("status") == "pass", "P1 exit gate must pass")
    require(exit_gate.get("promotion_allowed") is False, "promotion must not be allowed")
    require(evidence.get("next_phase") == "P2-gate-execution-and-replay", "next phase mismatch")

    for phrase in [
        "checklist_items | `5`",
        "field_completion_entries | `12`",
        "missing_real_input_entries | `3`",
        "explicit_rejection_sources | `6`",
        "p1_exit_gate.status | `pass`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("Ontology/WAS 3 小时目标已完成 P1 source-record 准备度清单" in loop_round, "loop round missing feedback")

    print(
        "ontology_was_3h_p1_source_record_readiness=pass "
        "phase=P1-real-source-record-readiness checklist_items=5 field_completion_entries=12 "
        "ready_by_rule_entries=9 missing_real_input_entries=3 hold_reasons=12 "
        "explicit_rejection_sources=6 real_source_records=0 valid_source_records=0 "
        "runtime_primary_key_ready=0 accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
