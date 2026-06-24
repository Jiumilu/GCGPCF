#!/usr/bin/env python3
"""Validate Loop templates and documentation include CodeGraph evidence schema."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TASK_TEMPLATE = ROOT / "loop/templates/loop-task-with-codegraph.yaml"
REVIEW_TEMPLATE = ROOT / "loop/templates/loop-review-with-codegraph.yaml"
RETRO_TEMPLATE = ROOT / "loop/templates/loop-retrospective-with-codegraph.yaml"
DOC = ROOT / "docs/codegraph/codegraph-loop-integration.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    task = read(TASK_TEMPLATE)
    review = read(REVIEW_TEMPLATE)
    retro = read(RETRO_TEMPLATE)
    doc = read(DOC)

    required_fields = [
        "required: true",
        "assumptions:",
        "tradeoff_options:",
        "simpler_path:",
        "minimal_scope:",
        "task_intake:",
        "query:",
        "query_results:",
        "target_nodes:",
        "node_inspection:",
        "affected:",
        "affected_scope:",
        "files_allowed_to_change:",
        "files_not_to_touch:",
        "expected_tests:",
        "affected_tests:",
        "fallback_tests:",
        "fallback_reason:",
        "acceptance_criteria:",
        "clarifying_questions:",
        "resolved_before_run:",
        "snapshot_id:",
        "context_queries:",
        "explored_symbols:",
        "impact_paths:",
        "impacted_tests:",
        "risk_flags:",
        "evidence_ref:",
        "codegraph_evidence:",
        "test_selection_reason:",
        "post_change_status:",
        "efficiency_metrics:",
        "manual_scan_files:",
        "codegraph_candidate_files:",
        "actual_changed_files:",
        "missed_impact_count:",
        "time_to_first_target:",
        "review_rework_count:",
    ]
    for field in required_fields:
        require(field in task, f"task template missing field: {field}")

    for field in ["changed_files:", "impacted_symbols:", "impacted_tests:", "risk_flags:", "status: review_required"]:
        require(field in review, f"review template missing field: {field}")
    for field in ["assumptions_reported:", "assumptions_clarified:", "minimal_scope_confirmed:", "alternative_paths_disclosed:", "tradeoff_documented:", "acceptance_checklist:", "orphan_cleanup_checked:", "reusable_criteria:"]:
        require(field in review, f"review template missing field: {field}")

    for field in ["query_count:", "impact_paths_count:", "impacted_tests_count:", "automatic_status_upgrade: false", "karpathy_gate:"]:
        require(field in retro, f"retrospective template missing field: {field}")

    for phrase in ["Task Intake", "CodeGraph Context", "Impact Analysis", "Evidence Capture", "KDS / OKF Candidate Record", "Karpathy 行为门禁", "assumptions", "acceptance_criteria", "clarifying_questions"]:
        require(phrase in doc, f"loop integration doc missing phrase: {phrase}")

    print(
        f"codegraph_loop_schema=pass templates=3 required_fields={len(required_fields)} "
        "automatic_status_upgrade=false karpathy_gate=enabled"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
