#!/usr/bin/env python3
"""Validate the 2026-06-27 SOP/PKC generated-output-dist isolation evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-generated-output-dist-isolation-20260627.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GENERATED-OUTPUT-DIST-ISOLATION-001.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"
SOP = PROJECT_ROOT / "GlobalCloud SOP"
PKC = PROJECT_ROOT / "GlobalCloud PKC"

REQUIRED_TOKENS = [
    "generated_output_dist_isolation = recheck_required",
    "sop_generated_output_dist_candidates = 1",
    "pkc_generated_output_dist_candidates = 0",
    "sop_status_clean = false",
    "pkc_status_clean = true",
    "project_group_git_gate = blocked",
    "dirty_repo_count = 7",
    "sensitive_repos = GlobalCloud KDS(.env.production.example)",
    "development_start_allowed = true",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

GENERATED_PREFIXES = ("dist/", "output/", "generated/")


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def git_status(repo: Path, failures: list[str]) -> list[str]:
    result = run(["git", "-C", str(repo), "status", "--porcelain=v1"])
    if result.returncode != 0:
        failures.append(f"git status failed for {repo.name}: {result.stderr.strip()}")
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def diff_check(repo: Path, failures: list[str]) -> None:
    result = run(["git", "-C", str(repo), "diff", "--check", "--", "."])
    if result.returncode != 0:
        failures.append(f"diff-check failed for {repo.name}: {result.stdout.strip() or result.stderr.strip()}")


def generated_candidates(status_lines: list[str]) -> list[str]:
    candidates: list[str] = []
    for line in status_lines:
        path = line[3:] if len(line) > 3 else line
        if path.startswith(GENERATED_PREFIXES):
            candidates.append(path)
    return candidates


def validate_git_gate(failures: list[str]) -> str:
    result = run(["python3", str(GIT_GATE), "--root", str(PROJECT_ROOT), "--allow-non-pass-exit-zero"])
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
    if summary.get("missing_repos") != []:
        failures.append(f"missing repos present: {summary.get('missing_repos')}")
    if summary.get("ahead_repos") != []:
        failures.append(f"ahead repos present: {summary.get('ahead_repos')}")
    if summary.get("behind_repos") != []:
        failures.append(f"behind repos present: {summary.get('behind_repos')}")
    if summary.get("sensitive_repos") != ["GlobalCloud KDS"]:
        failures.append(f"sensitive repos present: {summary.get('sensitive_repos')}")
    for repo in payload.get("repos", []):
        if repo.get("diff_check") != "pass":
            failures.append(f"repo diff-check not pass: {repo.get('name')}")
        if repo.get("name") == "GlobalCloud PKC" and repo.get("dirty_count") != 0:
            failures.append("PKC is not clean in project-group gate")
    return gate


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

    sop_status = git_status(SOP, failures)
    pkc_status = git_status(PKC, failures)
    diff_check(SOP, failures)
    diff_check(PKC, failures)

    sop_candidates = generated_candidates(sop_status)
    pkc_candidates = generated_candidates(pkc_status)
    if pkc_status:
        failures.append(f"PKC status not clean: {pkc_status[:5]}")
    if sop_candidates != ["output/.DS_Store"]:
        failures.append(f"unexpected SOP generated/output/dist candidates: {sop_candidates}")
    if pkc_candidates:
        failures.append(f"PKC generated/output/dist candidates present: {pkc_candidates}")

    gate = validate_git_gate(failures)
    result = {
        "project_group_generated_output_dist_isolation": "pass" if not failures else "fail",
        "sop_generated_output_dist_candidates": len(sop_candidates),
        "pkc_generated_output_dist_candidates": len(pkc_candidates),
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
