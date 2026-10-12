#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group P0-C minimal validation evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-p0c-minimal-validation-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0C-MINIMAL-VALIDATION-001.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"

PROJECTS = [
    "GlobalCloud AAAS",
    "WAS世界资产体系",
    "GlobalCloud WAES",
    "GlobalCloud GPC",
    "GlobalCloud PVAOS",
    "GlobalCloud XiaoC",
    "GlobalCloud XiaoG",
    "GlobalCloud XGD",
    "GlobalCloud XWAIL",
    "GlobalCloud GFIS",
    "GlobalCloud SOP",
]

REQUIRED_TOKENS = [
    "p0c_minimal_validation_ready = true",
    "development_start_allowed = true",
    "project_group_git_gate = blocked",
    "dirty_repo_count = 7",
    "sensitive_repos = GlobalCloud KDS(.env.production.example)",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "checked_projects | 11",
    "diff_check | 11/11 pass",
]


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def validate_project_minimal_commands(failures: list[str]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for project in PROJECTS:
        repo = PROJECT_ROOT / project
        status = run(["git", "-C", str(repo), "-c", "core.quotePath=false", "status", "--short", "--branch"])
        diff = run(["git", "-C", str(repo), "diff", "--check", "--", "."])
        item = {
            "project": project,
            "status_exit": status.returncode,
            "diff_check": "pass" if diff.returncode == 0 else "fail",
        }
        results.append(item)
        if status.returncode != 0:
            failures.append(f"status failed: {project}")
        if diff.returncode != 0:
            failures.append(f"diff-check failed: {project}: {(diff.stdout + diff.stderr).strip()}")
    return results


def validate_git_gate(failures: list[str]) -> str:
    result = run(
        [
            "python3",
            str(GIT_GATE),
            "--root",
            str(PROJECT_ROOT),
            "--allow-non-pass-exit-zero",
        ]
    )
    if result.returncode != 0:
        failures.append(f"project group git gate failed: {result.returncode}")
        return "unknown"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"project group git gate JSON parse failed: {exc}")
        return "unknown"
    gate = str(payload.get("gate", "unknown"))
    if gate != "blocked":
        failures.append(f"git gate not blocked: {gate}")
    summary = payload.get("summary", {})
    for key in ["missing_repos", "ahead_repos", "behind_repos"]:
        if summary.get(key) != []:
            failures.append(f"{key} present: {summary.get(key)}")
    if summary.get("sensitive_repos") != ["GlobalCloud KDS"]:
        failures.append(f"sensitive_repos present: {summary.get('sensitive_repos')}")
    for repo in payload.get("repos", []):
        if repo.get("diff_check") != "pass":
            failures.append(f"repo diff-check not pass: {repo.get('name')}")
    return gate


def main() -> int:
    failures: list[str] = []
    evidence = read(EVIDENCE, failures)
    loop_round = read(LOOP_ROUND, failures)

    for token in REQUIRED_TOKENS:
        if token not in evidence:
            failures.append(f"missing evidence token: {token}")
    for project in PROJECTS:
        if project not in evidence:
            failures.append(f"missing project in evidence: {project}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")

    minimal_results = validate_project_minimal_commands(failures)
    gate = validate_git_gate(failures)
    result = {
        "project_group_p0c_minimal_validation": "pass" if not failures else "fail",
        "checked_projects": len(PROJECTS),
        "minimal_results": minimal_results,
        "git_gate": gate,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
        "customer_accepted": False,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
