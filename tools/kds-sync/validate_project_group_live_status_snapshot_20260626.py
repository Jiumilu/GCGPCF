#!/usr/bin/env python3
"""Validate the 2026-06-26 GlobalCloud project-group live status snapshot."""

from __future__ import annotations

import json
import os
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
    "GlobalCloud Brain",
]

OPTIONAL_VOLATILE_DIRTY_REPOS = [
    "GlobalCoud GPCF",
]

EXPECTED_AHEAD_REPOS: list[str] = []

REQUIRED_DOC_TOKENS = [
    "GPCF-LIVE-STATUS-SNAPSHOT-20260626-001",
    "project_group_live_status_snapshot_20260626 = controlled",
    "live_status_snapshot_controlled",
    "snapshot_date | `2026-06-26`",
    "recheck_date | `2026-06-28`",
    "checked_repo_count | `17`",
    "expected_repo_count | `17`",
    "git_gate | `partial`",
    "dirty_repo_count | `1`",
    "review_boundary_repo_count = 1",
    "noise_cleanup_repo_count = 0",
    "pass_repo_count | `16`",
    "ahead_repos | `0`",
    "behind_repos | `0`",
    "sensitive_repos | `0`",
    "diff_check | `pass`",
    "当前 stable dirty 仓为 `GlobalCloud Brain`",
    "review_boundary_repos_current = GlobalCloud Brain",
    "noise_cleanup_repo_current = none",
    "gpcf_dirty_count_policy = volatile_observation_not_fact_entry",
    "GPCF 本仓瞬时行数不得作为真实事实入口或状态升级依据",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "KDS 已从当前 dirty/sensitive 阻塞源中移除",
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

GFIS_ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "formal_confirmation_files",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def validate_gfis_real_fact_entry(failures: list[str]) -> dict[str, str]:
    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        values = parse_kv_output(cached)
    else:
        result = subprocess.run(
            ["python3", "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        values = parse_kv_output(result.stdout)
        if result.returncode != 0:
            failures.append("GFIS real-fact entry gate failed: " + result.stdout.strip())
            return values
    if values.get("strong_block") != "true":
        failures.append("GFIS real-fact entry gate must keep strong_block=true")
    if values.get("status_ceiling") != "repair_required":
        failures.append("GFIS real-fact entry status ceiling must remain repair_required")
    for key in GFIS_ZERO_KEYS:
        if values.get(key) != "0":
            failures.append(f"GFIS real-fact entry must keep {key}=0, got {values.get(key)!r}")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


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


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(STATUS, failures)])
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in live status snapshot: {token}")

    dirty_repos: list[str] = []
    ahead_repos: list[str] = []
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
        try:
            ahead, _behind = git_ahead_behind(repo)
        except subprocess.CalledProcessError as exc:
            failures.append(f"git ahead/behind failed for {repo_name}: {exc.stderr.strip()}")
            ahead = 0
        if ahead:
            ahead_repos.append(repo_name)
        if repo_name not in doc_text:
            failures.append(f"missing repo row in live status snapshot: {repo_name}")

    allowed_dirty_repos = set(EXPECTED_DIRTY_REPOS + OPTIONAL_VOLATILE_DIRTY_REPOS)
    missing_required_dirty = [repo for repo in EXPECTED_DIRTY_REPOS if repo not in dirty_repos]
    unexpected_dirty = [repo for repo in dirty_repos if repo not in allowed_dirty_repos]
    if missing_required_dirty or unexpected_dirty:
        failures.append(
            "dirty repo set drifted: "
            f"required={EXPECTED_DIRTY_REPOS}, optional_volatile={OPTIONAL_VOLATILE_DIRTY_REPOS}, actual={dirty_repos}"
        )

    for repo_name in EXPECTED_DIRTY_REPOS:
        if live_dirty_counts.get(repo_name, 0) <= 0:
            failures.append(f"expected dirty repo is clean: {repo_name}")

    if ahead_repos != EXPECTED_AHEAD_REPOS:
        failures.append(f"ahead repo set drifted: expected={EXPECTED_AHEAD_REPOS}, actual={ahead_repos}")

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
        "stable_dirty_repos": EXPECTED_DIRTY_REPOS,
        "optional_volatile_dirty_repos": OPTIONAL_VOLATILE_DIRTY_REPOS,
        "ahead_repos": ahead_repos,
        "live_dirty_counts": live_dirty_counts,
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates the live status snapshot only; it does not delete files, stage, commit, push, sync KDS API, deploy, or grant accepted/integrated/customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
