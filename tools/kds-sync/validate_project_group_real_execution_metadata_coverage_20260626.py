#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_PROJECTS = [
    "AAAS",
    "Brain",
    "WAS",
    "XiaoC",
    "WAES",
    "GPC",
    "Studio",
    "GPCF",
    "XWAIL",
    "GFIS",
    "MMC",
    "KDS",
    "XiaoG",
    "PVAOS",
    "SOP",
    "PKC",
    "XGD",
]

KEY_DOCS = [
    "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-ready-for-review-advancement-queue-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-execution-command-pack-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-pre-execution-environment-readiness-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-authorization-request-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-authorization-receipt-ledger-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-objective-coverage-audit-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-governance-progress-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-completion-gap-matrix-20260626.md",
]


def parse_related(text: str) -> list[str]:
    match = re.search(r"^related_projects:\s*\[(.*)\]\s*$", text, flags=re.MULTILINE)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def main() -> int:
    failures: list[str] = []
    expected = set(EXPECTED_PROJECTS)

    for relative in KEY_DOCS:
        path = ROOT / relative
        if not path.exists():
            failures.append(f"missing key doc: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        related = parse_related(text)
        related_set = set(related)
        missing = sorted(expected - related_set)
        extra = sorted(related_set - expected)
        if missing:
            failures.append(f"{relative} missing related_projects: {missing}")
        if extra:
            failures.append(f"{relative} has unexpected related_projects: {extra}")
        if len(related) != len(EXPECTED_PROJECTS):
            failures.append(f"{relative} related_projects count is {len(related)}, expected {len(EXPECTED_PROJECTS)}")

    result = {
        "gate": "project_group_real_execution_metadata_coverage_20260626",
        "status": "fail" if failures else "pass",
        "key_doc_count": len(KEY_DOCS),
        "expected_project_count": len(EXPECTED_PROJECTS),
        "failures": failures,
        "warnings": [
            "This validates frontmatter related_projects coverage only; it does not execute tasks, grant authorization, stage, commit, push, deploy, release, sync KDS API, or grant accepted/integrated/customer acceptance."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
