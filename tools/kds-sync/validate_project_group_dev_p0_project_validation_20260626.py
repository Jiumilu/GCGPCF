#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group dev P0 project validation evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent

EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-dev-p0-project-validation-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-PROJECT-VALIDATION-001.md"

PROJECTS = [
    "GlobalCloud GPC",
    "GlobalCloud Studio",
    "GlobalCloud MMC",
    "GlobalCloud KDS",
    "GlobalCloud PKC",
]

REQUIRED_TOKENS = [
    "project_validation_ready = true",
    "development_start_allowed = true",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "20 passed",
    "Harness check passed",
    "36 passed",
    "2 passed",
    "Vite build completed",
    "isolate_generated_before_commit",
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

    for token in REQUIRED_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing evidence token: {token}")

    for project in PROJECTS:
        if project not in evidence_text:
            failures.append(f"missing project in validation evidence: {project}")

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
        if data.get("gate") not in {"partial", "pass"}:
            failures.append(f"unexpected project group git gate: {data.get('gate')}")
        summary = data.get("summary", {})
        for key in ["missing_repos", "ahead_repos", "behind_repos", "sensitive_repos"]:
            if summary.get(key) != []:
                failures.append(f"{key} present: {summary.get(key)}")
        for repo in data.get("repos", []):
            if repo.get("diff_check") != "pass":
                failures.append(f"repo diff-check not pass: {repo.get('name')}")

    result = {
        "project_group_dev_p0_project_validation": "pass" if not failures else "fail",
        "checked_projects": len(PROJECTS),
        "project_validation_ready": not failures,
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
