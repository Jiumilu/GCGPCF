#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group dev P0 blocker reduction evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
KDS_ROOT = PROJECT_ROOT / "GlobalCloud KDS"

EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-dev-p0-blocker-reduction-20260626.md"
TASK_QUEUE = ROOT / "docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-P0-BLOCKER-REDUCTION-001.md"
NEW_LEDGER = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json"
OLD_LEDGER = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-production-token-ledger-20260623.json"

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
    task_text = read(TASK_QUEUE, failures)
    loop_text = read(LOOP_ROUND, failures)

    for token in [
        "development_start_allowed = true",
        "project_group_git_gate = partial",
        "accepted = false",
        "integrated = false",
        "production_ready = false",
        "customer_accepted = false",
    ]:
        if token not in evidence_text:
            failures.append(f"missing evidence token: {token}")

    for project in PROJECTS:
        if project not in task_text:
            failures.append(f"missing project in task queue: {project}")

    for token in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {token}" not in loop_text:
            failures.append(f"missing loop control section: {token}")

    if not NEW_LEDGER.exists():
        failures.append(f"missing renamed ledger: {NEW_LEDGER}")
    if OLD_LEDGER.exists():
        failures.append(f"old sensitive-path ledger still exists: {OLD_LEDGER}")

    kds_check = run(["git", "diff", "--check", "--", "wiki/log.md"], KDS_ROOT)
    if kds_check.returncode != 0:
        failures.append("KDS wiki/log.md diff-check failed")

    git_gate = run(
        [
            "python3",
            ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py",
            "--root",
            str(PROJECT_ROOT),
        ],
        ROOT,
    )
    if git_gate.returncode not in (0, 1, 2):
        failures.append("project group git gate did not return a recognized status")
        data = {}
    else:
        try:
            data = json.loads(git_gate.stdout)
        except json.JSONDecodeError as exc:
            failures.append(f"project group git gate JSON parse failed: {exc}")
            data = {}

    if data:
        if data.get("checked_repo_count") != 17 or data.get("expected_repo_count") != 17:
            failures.append("expected 17 checked repos")
        summary = data.get("summary", {})
        if summary.get("missing_repos") != []:
            failures.append(f"missing repos present: {summary.get('missing_repos')}")
        if summary.get("ahead_repos") != []:
            failures.append(f"ahead repos present: {summary.get('ahead_repos')}")
        if summary.get("behind_repos") != []:
            failures.append(f"behind repos present: {summary.get('behind_repos')}")
        if summary.get("sensitive_repos") != []:
            failures.append(f"sensitive repos present: {summary.get('sensitive_repos')}")
        for repo in data.get("repos", []):
            if repo.get("diff_check") != "pass":
                failures.append(f"repo diff-check not pass: {repo.get('name')}")
            if repo.get("sensitive_paths"):
                failures.append(f"repo sensitive paths present: {repo.get('name')}")

    result = {
        "project_group_dev_p0_blocker_reduction": "pass" if not failures else "fail",
        "checked_projects": len(PROJECTS),
        "development_start_allowed": not failures,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
