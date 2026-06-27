#!/usr/bin/env python3
"""Validate the 2026-06-27 GPCF worktree review package evidence."""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-gpcf-worktree-review-packages-20260627.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GPCF-WORKTREE-REVIEW-PACKAGES-001.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"

REQUIRED_TOKENS = [
    "gpcf_worktree_review_packages = recheck_required",
    "review_package_count = 7",
    "project_group_git_gate = blocked",
    "clean_repo_count = 10",
    "dirty_repo_count = 7",
    "dirty_repos_current = GlobalCloud AAAS, WAS世界资产体系, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "missing_repos = 0",
    "behind_repos = 0",
    "sensitive_repos = 1",
    "diff_check_failed_repos = 0",
    "development_start_allowed = true",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "GPCF-RP1",
    "GPCF-RP2",
    "GPCF-RP3",
    "GPCF-RP4",
    "GPCF-RP5",
    "GPCF-RP6",
    "GPCF-RP7",
]


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def status_paths() -> list[str]:
    result = run(["git", "-c", "core.quotePath=false", "status", "--porcelain=v1"])
    if result.returncode != 0:
        return []
    return [line[3:] if len(line) > 3 else line for line in result.stdout.splitlines() if line.strip()]


def classify(path: str) -> str:
    if path.startswith(".kds/development-space/"):
        return "kds_local_mirror"
    if path.startswith(".kds/local-mirror-ledger"):
        return "kds_local_mirror_ledger"
    if path.startswith("09-status/"):
        return "status_registers"
    if path.startswith("docs/harness/evidence/agent-reach-p9-"):
        return "agent_reach_evidence"
    if path.startswith("docs/harness/evidence/globalcloud-project-group-"):
        return "project_group_p0_evidence"
    if path.startswith("docs/harness/loops/"):
        return "loop_rounds"
    if path.startswith("docs/"):
        return "docs_indexes"
    if path.startswith("tools/kds-sync/") and "agent_reach" in path:
        return "agent_reach_tooling"
    if path.startswith("tools/kds-sync/") and "project_group" in path:
        return "project_group_p0_validator"
    if path.startswith("fixtures/agent-reach/"):
        return "agent_reach_fixtures"
    return "other"


def validate_git_gate(failures: list[str]) -> tuple[str, int, list[str]]:
    result = run(["python3", str(GIT_GATE), "--root", str(PROJECT_ROOT), "--allow-non-pass-exit-zero"])
    if result.returncode != 0:
        failures.append(f"project group git gate failed: {result.returncode}")
        return "unknown", 0, []
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"project group git gate JSON parse failed: {exc}")
        return "unknown", 0, []
    gate = str(payload.get("gate", "unknown"))
    summary = payload.get("summary", {})
    dirty_repos = summary.get("dirty_repos", [])
    if gate != "blocked":
        failures.append(f"git gate not blocked: {gate}")
    if dirty_repos != ["GlobalCloud AAAS", "WAS世界资产体系", "GlobalCoud GPCF", "GlobalCloud XWAIL", "GlobalCloud GFIS", "GlobalCloud KDS", "GlobalCloud SOP"]:
        failures.append(f"unexpected dirty repos: {dirty_repos}")
    for key in ["missing_repos", "ahead_repos", "behind_repos"]:
        if summary.get(key) != []:
            failures.append(f"{key} present: {summary.get(key)}")
    if summary.get("sensitive_repos") != ["GlobalCloud KDS"]:
        failures.append(f"sensitive_repos present: {summary.get('sensitive_repos')}")
    for repo in payload.get("repos", []):
        if repo.get("diff_check") != "pass":
            failures.append(f"repo diff-check not pass: {repo.get('name')}")
    return gate, int(summary.get("pass", 0)), dirty_repos


def main() -> int:
    failures: list[str] = []
    evidence = read(EVIDENCE, failures)
    loop_round = read(LOOP_ROUND, failures)
    for token in REQUIRED_TOKENS:
        if token not in evidence:
            failures.append(f"missing evidence token: {token}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")

    paths = status_paths()
    categories = Counter(classify(path) for path in paths)
    expected_categories = {
        "kds_local_mirror",
        "kds_local_mirror_ledger",
        "status_registers",
        "docs_indexes",
        "agent_reach_evidence",
        "project_group_p0_evidence",
        "loop_rounds",
        "agent_reach_tooling",
        "project_group_p0_validator",
    }
    missing_categories = sorted(category for category in expected_categories if categories.get(category, 0) == 0)
    if missing_categories:
        failures.append(f"missing expected categories: {missing_categories}")

    gate, clean_repo_count, dirty_repos = validate_git_gate(failures)
    result = {
        "project_group_gpcf_worktree_review_packages": "pass" if not failures else "fail",
        "review_package_count": 7,
        "git_gate": gate,
        "clean_repo_count": clean_repo_count,
        "dirty_repos": dirty_repos,
        "category_counts": dict(sorted(categories.items())),
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
