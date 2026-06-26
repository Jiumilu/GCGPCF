#!/usr/bin/env python3
"""Validate the 2026-06-26 GlobalCloud project-group live status snapshot."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-live-status-snapshot-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

EXPECTED_REPOS = [
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

EXPECTED_DIRTY_REPOS = [
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
    "GPCF-LIVE-STATUS-SNAPSHOT-20260626-001",
    "project_group_live_status_snapshot_20260626 = controlled",
    "live_status_snapshot_controlled",
    "snapshot_date | `2026-06-26`",
    "checked_repo_count | `17`",
    "expected_repo_count | `17`",
    "git_gate | `partial`",
    "dirty_repo_count | `17`",
    "pass_repo_count | `0`",
    "ahead_repos | `0`",
    "behind_repos | `0`",
    "sensitive_repos | `0`",
    "diff_check | `pass`",
    "仓集合已变",
    "方案识别规则写入后全部项目均为 dirty",
    "已发生 live 漂移",
    "authorization_boundary",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-LIVE-STATUS-SNAPSHOT-20260626-001",
    "globalcloud-project-group-live-status-snapshot-20260626.md",
    "validate_project_group_live_status_snapshot_20260626.py",
    "live_status_snapshot_controlled",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
    "项目群 Git 全量 clean = true",
    "真实 KDS API 已同步 = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def git_status(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(STATUS, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in live status snapshot: {token}")

    dirty_repos: list[str] = []
    live_dirty_counts: dict[str, int] = {}
    for repo_name in EXPECTED_REPOS:
        repo = PROJECT_ROOT / repo_name
        if not repo.exists():
            failures.append(f"missing repo: {repo_name}")
            continue
        try:
            lines = git_status(repo)
        except subprocess.CalledProcessError as exc:
            failures.append(f"git status failed for {repo_name}: {exc.stderr.strip()}")
            continue
        live_dirty_counts[repo_name] = len(lines)
        if lines:
            dirty_repos.append(repo_name)
        if repo_name not in doc_text:
            failures.append(f"missing repo row in live status snapshot: {repo_name}")

    if dirty_repos != EXPECTED_DIRTY_REPOS:
        failures.append(f"dirty repo set drifted: expected={EXPECTED_DIRTY_REPOS}, actual={dirty_repos}")

    for repo_name in EXPECTED_DIRTY_REPOS:
        if live_dirty_counts.get(repo_name, 0) <= 0:
            failures.append(f"expected dirty repo is clean: {repo_name}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive claim: {token}")

    result = {
        "gate": "project_group_live_status_snapshot_20260626",
        "status": "pass" if not failures else "fail",
        "checked_repo_count": len(EXPECTED_REPOS),
        "dirty_repo_count": len(dirty_repos),
        "dirty_repos": dirty_repos,
        "live_dirty_counts": live_dirty_counts,
        "failures": failures,
        "warnings": [
            "This validates the live status snapshot only; it does not delete files, stage, commit, push, sync KDS API, deploy, or grant accepted/integrated/customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
