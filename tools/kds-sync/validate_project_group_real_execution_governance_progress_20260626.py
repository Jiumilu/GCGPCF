#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-real-execution-governance-progress-20260626.md"

REQUIRED_STRINGS = [
    "project_group_git_clean = partial",
    "checked_repo_count = 17",
    "dirty_repo_count = 17",
    "pass_repo_count = 0",
    "ahead_repos = 0",
    "behind_repos = 0",
    "sensitive_repos = 0",
    "diff_check = pass",
    "auto_ready_for_review_upgrade = false",
    "authorization_granted = false",
    "action_executed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "WAES-LINT-RUNTIME-001",
    "GFIS-REAL-SOR-001",
    "GPC-EXTERNAL-RUNTIME-EVIDENCE-001",
    "BRAIN-HUMAN-REVIEW-DECISION-001",
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "validate_project_group_real_execution_metadata_coverage_20260626.py",
    "key_doc_count=15",
    "expected_project_count=17",
    "WAES -> XWAIL/AaaS",
    "GFIS/GPC/PVAOS -> SCaaS",
    "KDS -> Brain",
    "run",
    "stop",
    "verify",
    "recover",
    "debug",
]

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


def main() -> int:
    failures: list[str] = []
    if not DOC.exists():
        failures.append(f"missing document: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")

    for value in REQUIRED_STRINGS:
        if value not in text:
            failures.append(f"missing required text: {value}")

    missing_projects = [project for project in PROJECTS if project not in text]
    for project in missing_projects:
        failures.append(f"missing project row: {project}")

    result = {
        "gate": "project_group_real_execution_governance_progress_20260626",
        "status": "fail" if failures else "pass",
        "project_count": len(PROJECTS) - len(missing_projects),
        "required_string_count": len(REQUIRED_STRINGS),
        "failures": failures,
        "warnings": [
            "This validates governance progress evidence only; it does not execute project tasks, clean repos, stage, commit, push, deploy, release, or grant accepted/integrated/customer acceptance."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
