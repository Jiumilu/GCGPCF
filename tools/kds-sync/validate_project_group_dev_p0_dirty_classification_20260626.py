#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group dev P0 dirty classification evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent

EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-dev-p0-dirty-classification-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-DIRTY-CLASSIFICATION-001.md"

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

REQUIRED_EVIDENCE_TOKENS = [
    "dirty_classification_ready = true",
    "development_start_allowed = true",
    "project_group_git_gate = blocked",
    "dirty_repo_count = 7",
    "sensitive_repos = GlobalCloud KDS(.env.production.example)",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "dev_candidate_requires_project_test",
    "isolate_generated_before_commit",
    "keep_as_dev_candidate_after_owner_review",
]


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    evidence_text = read(EVIDENCE, failures)
    loop_text = read(LOOP_ROUND, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing evidence token: {token}")

    for project in PROJECTS:
        if project not in evidence_text:
            failures.append(f"missing project in dirty classification evidence: {project}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_text:
            failures.append(f"missing loop control section: {section}")

    git_gate = run(
        [
            "python3",
            ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py",
            "--root",
            str(PROJECT_ROOT),
        ],
        ROOT,
    )
    try:
        data = json.loads(git_gate.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"project group git gate JSON parse failed: {exc}")
        data = {}

    if data:
        if data.get("gate") != "blocked":
            failures.append(f"unexpected project group git gate: {data.get('gate')}")
        if data.get("checked_repo_count") != 17 or data.get("expected_repo_count") != 17:
            failures.append("expected 17 checked repos")
        summary = data.get("summary", {})
        for key in ["missing_repos", "ahead_repos", "behind_repos"]:
            if summary.get(key) != []:
                failures.append(f"{key} present: {summary.get(key)}")
        if summary.get("sensitive_repos") != ["GlobalCloud KDS"]:
            failures.append(f"sensitive_repos present: {summary.get('sensitive_repos')}")
        for repo in data.get("repos", []):
            if repo.get("diff_check") != "pass":
                failures.append(f"repo diff-check not pass: {repo.get('name')}")

    result = {
        "project_group_dev_p0_dirty_classification": "pass" if not failures else "fail",
        "checked_projects": len(PROJECTS),
        "dirty_classification_ready": not failures,
        "development_start_allowed": not failures,
        "project_group_git_gate": data.get("gate") if data else "unknown",
        "accepted": False,
        "integrated": False,
        "production_ready": False,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
