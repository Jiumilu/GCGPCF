#!/usr/bin/env python3
"""Build the current project-group live status snapshot."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import argparse
import json
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
TZ = timezone(timedelta(hours=8))

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

VOLATILE_DIRTY_ALLOWLIST = ["GlobalCoud GPCF"]
FRESHNESS_HOURS = 12

DEFAULT_JSON = ROOT / "docs/harness/evidence/project_group_live_status_current.json"
DEFAULT_MD = ROOT / "docs/harness/evidence/project_group_live_status_current.md"

SENSITIVE_PATTERNS = [
    re.compile(r"(^|/)\.env(\.|$)"),
    re.compile(r"\.pem$"),
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"credential", re.IGNORECASE),
    re.compile(r"token", re.IGNORECASE),
]


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


def git_ahead_behind(repo: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["git", "rev-list", "--left-right", "--count", "@{upstream}...HEAD"],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    left, right = result.stdout.strip().split()
    return int(right), int(left)


def parse_paths(lines: list[str]) -> list[str]:
    paths: list[str] = []
    for line in lines:
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return paths


def is_sensitive_path(path: str) -> bool:
    return any(pattern.search(path) for pattern in SENSITIVE_PATTERNS)


def load_previous(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def stable_from_previous(current: list[str], previous: list[str], bootstrap: bool) -> list[str]:
    current_set = set(current)
    if bootstrap or not previous:
        return sorted(current_set)
    return sorted(current_set & set(previous))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args()

    json_out = Path(args.json_out)
    md_out = Path(args.md_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)

    previous = load_previous(json_out)
    previous_observed_dirty = [str(item) for item in previous.get("observed_dirty", [])]
    previous_observed_ahead = [str(item) for item in previous.get("observed_ahead", [])]
    bootstrap = not bool(previous)

    observed_dirty: list[str] = []
    observed_ahead: list[str] = []
    sensitive_repos: list[str] = []
    dirty_details: dict[str, dict] = {}

    pass_repo_count = 0

    for repo_name in EXPECTED_REPOS:
        repo = PROJECT_ROOT / repo_name
        status_lines = git_status(repo)
        ahead, behind = git_ahead_behind(repo)
        paths = parse_paths(status_lines)
        sensitive = sorted({path for path in paths if is_sensitive_path(path)})
        if status_lines:
            observed_dirty.append(repo_name)
        if ahead > 0:
            observed_ahead.append(repo_name)
        if sensitive:
            sensitive_repos.append(repo_name)
        if not status_lines and ahead == 0 and behind == 0:
            pass_repo_count += 1
        dirty_details[repo_name] = {
            "dirty_count": len(status_lines),
            "ahead": ahead,
            "behind": behind,
            "paths": paths,
            "sensitive_paths": sensitive,
        }

    volatile_dirty = sorted(set(observed_dirty) & set(VOLATILE_DIRTY_ALLOWLIST))
    stable_dirty = stable_from_previous(observed_dirty, previous_observed_dirty, bootstrap)
    stable_ahead = stable_from_previous(observed_ahead, previous_observed_ahead, bootstrap)
    review_boundary = sorted(set(stable_dirty) | set(volatile_dirty) | set(sensitive_repos))

    generated_at = datetime.now(TZ)
    snapshot = {
        "schema_version": "1.0",
        "generated_at": generated_at.isoformat(),
        "freshness_hours": FRESHNESS_HOURS,
        "freshness_ok": True,
        "project_count": len(EXPECTED_REPOS),
        "observed_dirty": observed_dirty,
        "observed_ahead": observed_ahead,
        "stable_dirty": stable_dirty,
        "stable_ahead": stable_ahead,
        "volatile_dirty": volatile_dirty,
        "review_boundary": review_boundary,
        "sensitive_repos": sensitive_repos,
        "pass_repo_count": pass_repo_count,
        "bootstrap_window": bootstrap,
        "previous_generated_at": previous.get("generated_at"),
        "dirty_details": dirty_details,
    }

    json_out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        "---",
        "doc_id: GPCF-DOC-PROJECTGROUPLIVESTATUSCURRENT20260701",
        "title: GlobalCloud 项目群当前 Live 状态快照",
        "project: GPCF",
        "related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]",
        "domain: harness",
        "type: project_group_live_status_current",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/12-GPCF/docs/harness/evidence/project_group_live_status_current.md",
        "source_path: docs/harness/evidence/project_group_live_status_current.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-07-01",
        "supersedes: []",
        "superseded_by: []",
        "data_layer: derived",
        "authority_level: A2",
        "verification_status: source_verified",
        f"generated_at: {generated_at.strftime('%Y-%m-%d %H:%M:%S %z')}",
        "---",
        "",
        "# GlobalCloud 项目群当前 Live 状态快照",
        "",
        "## Summary",
        "",
        f"- generated_at: `{snapshot['generated_at']}`",
        f"- freshness_ok: `{str(snapshot['freshness_ok']).lower()}`",
        f"- project_count: `{snapshot['project_count']}`",
        f"- pass_repo_count: `{snapshot['pass_repo_count']}`",
        f"- bootstrap_window: `{str(snapshot['bootstrap_window']).lower()}`",
        "",
        "## Current sets",
        "",
        f"- observed_dirty: `{', '.join(observed_dirty) if observed_dirty else 'none'}`",
        f"- observed_ahead: `{', '.join(observed_ahead) if observed_ahead else 'none'}`",
        f"- stable_dirty: `{', '.join(stable_dirty) if stable_dirty else 'none'}`",
        f"- stable_ahead: `{', '.join(stable_ahead) if stable_ahead else 'none'}`",
        f"- volatile_dirty: `{', '.join(volatile_dirty) if volatile_dirty else 'none'}`",
        f"- sensitive_repos: `{', '.join(sensitive_repos) if sensitive_repos else 'none'}`",
        f"- review_boundary: `{', '.join(review_boundary) if review_boundary else 'none'}`",
        "",
        "## Repo details",
        "",
        "| Repo | dirty_count | ahead | behind | sensitive_paths |",
        "|---|---:|---:|---:|---|",
    ]
    for repo_name in EXPECTED_REPOS:
        detail = dirty_details[repo_name]
        sensitive = ", ".join(detail["sensitive_paths"]) if detail["sensitive_paths"] else "none"
        md_lines.append(
            f"| `{repo_name}` | {detail['dirty_count']} | {detail['ahead']} | {detail['behind']} | `{sensitive}` |"
        )
    md_out.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "pass",
        "json_out": str(json_out.relative_to(ROOT)),
        "md_out": str(md_out.relative_to(ROOT)),
        "observed_dirty": observed_dirty,
        "observed_ahead": observed_ahead,
        "stable_dirty": stable_dirty,
        "stable_ahead": stable_ahead,
        "review_boundary": review_boundary,
        "bootstrap_window": bootstrap,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
