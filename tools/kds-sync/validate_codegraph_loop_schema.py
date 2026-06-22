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
        "snapshot_id:",
        "context_queries:",
        "explored_symbols:",
        "impact_paths:",
        "impacted_tests:",
        "risk_flags:",
        "evidence_ref:",
    ]
    for field in required_fields:
        require(field in task, f"task template missing field: {field}")

    for field in ["changed_files:", "impacted_symbols:", "impacted_tests:", "risk_flags:", "status: review_required"]:
        require(field in review, f"review template missing field: {field}")

    for field in ["query_count:", "impact_paths_count:", "impacted_tests_count:", "automatic_status_upgrade: false"]:
        require(field in retro, f"retrospective template missing field: {field}")

    for phrase in ["Task Intake", "CodeGraph Context", "Impact Analysis", "Evidence Capture", "KDS / OKF Candidate Record"]:
        require(phrase in doc, f"loop integration doc missing phrase: {phrase}")

    print("codegraph_loop_schema=pass templates=3 required_fields=7 automatic_status_upgrade=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
