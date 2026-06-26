#!/usr/bin/env python3
"""Read-only Git clean gate for the 17 GlobalCloud project repositories."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


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

SENSITIVE_PATTERNS = [
    ".env",
    ".env.*",
    "*TOKEN*",
    "*SECRET*",
    "*.pem",
    "*.key",
    "*.p12",
    "id_rsa*",
]


def default_group_root() -> Path:
    return Path(__file__).resolve().parents[5]


def run_git(repo: Path, *args: str) -> dict[str, Any]:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def status_paths(status_lines: list[str]) -> list[str]:
    paths: list[str] = []
    for line in status_lines:
        raw = line[3:] if len(line) > 3 else line
        if " -> " in raw:
            old, new = raw.split(" -> ", 1)
            paths.extend([old.strip(), new.strip()])
        else:
            paths.append(raw.strip())
    return [path.strip('"') for path in paths if path.strip()]


def is_sensitive_path(path: str) -> bool:
    name = Path(path).name
    for pattern in SENSITIVE_PATTERNS:
        if pattern == ".env.*" and name == ".env.example":
            continue
        if fnmatch.fnmatchcase(name, pattern):
            return True
        if fnmatch.fnmatchcase(name.upper(), pattern.upper()):
            return True
    return False


def count_ahead_behind(repo: Path, upstream: str) -> tuple[int | None, int | None, str]:
    result = run_git(repo, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
    if result["returncode"] != 0:
        return None, None, result["stderr"].strip()
    parts = result["stdout"].strip().split()
    if len(parts) != 2:
        return None, None, result["stdout"].strip()
    behind, ahead = int(parts[0]), int(parts[1])
    return ahead, behind, ""


def inspect_repo(root: Path, name: str, fetch_dry_run: bool) -> dict[str, Any]:
    repo = root / name
    item: dict[str, Any] = {
        "name": name,
        "path": str(repo),
        "exists": repo.exists(),
        "is_git_repo": (repo / ".git").exists(),
        "branch": None,
        "upstream": None,
        "dirty_count": None,
        "untracked_count": None,
        "ahead": None,
        "behind": None,
        "diff_check": "not_run",
        "sensitive_paths": [],
        "issues": [],
    }

    if not item["exists"]:
        item["issues"].append("missing_repo")
        return item
    if not item["is_git_repo"]:
        item["issues"].append("not_git_repo")
        return item

    if fetch_dry_run:
        fetch = run_git(repo, "fetch", "--dry-run", "--all", "--prune")
        if fetch["returncode"] != 0:
            item["issues"].append("fetch_dry_run_failed")
            item["fetch_dry_run_error"] = fetch["stderr"].strip()

    branch = run_git(repo, "branch", "--show-current")
    item["branch"] = branch["stdout"].strip()
    if branch["returncode"] != 0 or not item["branch"]:
        item["issues"].append("branch_missing")

    upstream = run_git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream["returncode"] == 0:
        item["upstream"] = upstream["stdout"].strip()
    else:
        item["issues"].append("upstream_missing")

    status = run_git(repo, "status", "--porcelain=v1")
    if status["returncode"] != 0:
        item["issues"].append("status_failed")
        item["status_error"] = status["stderr"].strip()
        status_lines: list[str] = []
    else:
        status_lines = [line for line in status["stdout"].splitlines() if line.strip()]
    item["dirty_count"] = len(status_lines)
    item["untracked_count"] = sum(1 for line in status_lines if line.startswith("??"))
    if status_lines:
        item["issues"].append("dirty")

    sensitive_paths = [path for path in status_paths(status_lines) if is_sensitive_path(path)]
    if sensitive_paths:
        item["sensitive_paths"] = sensitive_paths
        item["issues"].append("sensitive_path")

    if item["upstream"]:
        ahead, behind, error = count_ahead_behind(repo, item["upstream"])
        item["ahead"] = ahead
        item["behind"] = behind
        if error:
            item["issues"].append("ahead_behind_failed")
            item["ahead_behind_error"] = error
        if ahead and ahead > 0:
            item["issues"].append("ahead")
        if behind and behind > 0:
            item["issues"].append("behind")

    diff_check = run_git(repo, "diff", "--check", "--", ".")
    if diff_check["returncode"] == 0:
        item["diff_check"] = "pass"
    else:
        item["diff_check"] = "fail"
        item["issues"].append("diff_check_failed")
        item["diff_check_output"] = (diff_check["stdout"] + diff_check["stderr"]).strip()

    return item


def classify(items: list[dict[str, Any]]) -> str:
    blocked = {
        "missing_repo",
        "not_git_repo",
        "upstream_missing",
        "behind",
        "sensitive_path",
        "diff_check_failed",
        "branch_missing",
        "status_failed",
        "ahead_behind_failed",
        "fetch_dry_run_failed",
    }
    partial = {"dirty", "ahead"}
    all_issues = {issue for item in items for issue in item["issues"]}
    if all_issues & blocked:
        return "blocked"
    if all_issues & partial:
        return "partial"
    return "pass"


def build_report(root: Path, fetch_dry_run: bool) -> dict[str, Any]:
    items = [inspect_repo(root, name, fetch_dry_run) for name in EXPECTED_REPOS]
    gate = classify(items)
    return {
        "gate": gate,
        "root": str(root),
        "expected_repo_count": len(EXPECTED_REPOS),
        "checked_repo_count": len(items),
        "summary": {
            "pass": sum(1 for item in items if not item["issues"]),
            "partial_or_blocked": sum(1 for item in items if item["issues"]),
            "dirty_repos": [item["name"] for item in items if "dirty" in item["issues"]],
            "ahead_repos": [item["name"] for item in items if "ahead" in item["issues"]],
            "behind_repos": [item["name"] for item in items if "behind" in item["issues"]],
            "sensitive_repos": [item["name"] for item in items if "sensitive_path" in item["issues"]],
            "missing_repos": [item["name"] for item in items if "missing_repo" in item["issues"]],
        },
        "repos": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_group_root())
    parser.add_argument("--fetch-dry-run", action="store_true")
    parser.add_argument("--allow-non-pass-exit-zero", action="store_true")
    args = parser.parse_args()

    report = build_report(args.root.expanduser().resolve(), args.fetch_dry_run)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))

    if report["gate"] == "pass" or args.allow_non_pass_exit_zero:
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
