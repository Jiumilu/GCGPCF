#!/usr/bin/env python3
"""Validate the GlobalCloud full project real-state baseline evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

PROJECTS = [
    "GlobalCloud AAAS",
    "GlobalCloud Brain",
    "WAS世界资产体系",
    "GlobalCloud XiaoC",
    "GlobalCloud WAES",
    "GlobalCloud GPC",
    "GlobalCloud Studio",
    "GlobalCoud GPCF",
    "GlobalCloud XWAIL",
    "GlobalCloud GFIS",
    "GlobalCloud MMC",
    "GlobalCloud KDS",
    "GlobalCloud XiaoG",
    "GlobalCloud PVAOS",
    "GlobalCloud SOP",
    "GlobalCloud PKC",
    "GlobalCloud XGD",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-FULL-PROJECT-BASELINE-001",
    "expected_project_count | 17",
    "checked_project_count | 17",
    "full_project_baseline = controlled",
    "project_group_git_clean = partial",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "ready_for_review",
    "partial_or_repair",
    "governance_controlled",
    "baseline_only",
    "BASELINE-ONLY-PROJECT-TASK-PACKS",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-FULL-PROJECT-BASELINE-001",
    "globalcloud-project-group-full-project-baseline-20260625.md",
    "validate_project_group_full_project_baseline.py",
    "full_project_baseline = controlled",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "project_group_git_clean = pass",
    "commit_allowed = true",
    "push_allowed = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in full project baseline: {token}")

    for project in PROJECTS:
        row_prefix = f"|"
        if project not in doc_text:
            failures.append(f"missing project in full project baseline: {project}")
            continue
        rows = [line for line in doc_text.splitlines() if line.startswith(row_prefix) and f"| {project} |" in line]
        if len(rows) != 1:
            failures.append(f"project must have exactly one baseline row: {project}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "project_group_full_project_baseline",
        "status": "pass" if not failures else "fail",
        "projects_checked": len(PROJECTS),
        "baseline": "controlled" if not failures else "failed",
        "failures": failures,
        "warnings": [
            "This validates 17-project baseline coverage only; it does not grant accepted, integrated, production, customer acceptance, commit, or push authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
