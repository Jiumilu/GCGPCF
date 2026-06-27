#!/usr/bin/env python3
"""Validate the 2026-06-27 external loop gate delegate baseline evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-001.md"
DELEGATE_VALIDATOR = ROOT / "tools/kds-sync/validate_project_group_external_loop_gate_delegates.py"

REPOS = {
    "GlobalCloud AAAS": "AAAS-WAES-BINDING-PRECHECK-001",
    "GlobalCloud XWAIL": "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001",
    "GlobalCloud SOP": "SOP-SCENARIO-OWNER-REVIEW-001",
}

REQUIRED_TOKENS = [
    "project_group_external_loop_gate_delegate_baseline_20260627 = controlled",
    "task_id = GPCF-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-20260627-001",
    "state_candidate = external_loop_gate_delegate_baseline_ready",
    "delegated_repo_count = 3",
    "delegation_only = true",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "runtime_write_allowed = false",
    "status_promotion_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "project_group_external_loop_gate_delegates=pass checked_repos=3 delegation_only=true gfis_status_ceiling=repair_required formal_confirmation_files=0",
]

FORBIDDEN_TOKENS = [
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "runtime_write_allowed = true",
    "status_promotion_allowed = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
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


def validate_repo(repo_name: str, failures: list[str]) -> dict[str, object]:
    repo_root = PROJECT_ROOT / repo_name
    if not repo_root.exists():
        failures.append(f"missing repo: {repo_name}")
        return {}

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_root).stdout.strip()
    upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], repo_root).stdout.strip()
    status = run(["git", "-c", "core.quotePath=false", "status", "--short", "--untracked-files=all"], repo_root)
    status_lines = [line for line in status.stdout.splitlines() if line.strip()]
    untracked = [line for line in status_lines if line.startswith("?? ")]
    diff_check = run(["git", "diff", "--check", "--", "."], repo_root)

    if branch != "main":
        failures.append(f"{repo_name} branch not main: {branch}")
    if upstream != "origin/main":
        failures.append(f"{repo_name} upstream not origin/main: {upstream}")
    if len(status_lines) != 1:
        failures.append(f"{repo_name} dirty count not 1: {len(status_lines)}")
    if untracked != ["?? tools/kds-sync/loop_document_gate.py"]:
        failures.append(f"{repo_name} unexpected untracked set: {untracked}")
    if diff_check.returncode != 0:
        failures.append(f"{repo_name} diff-check failed: {diff_check.stderr or diff_check.stdout}")

    return {
        "branch": branch,
        "upstream": upstream,
        "dirty_count": len(status_lines),
        "untracked_count": len(untracked),
        "untracked_paths": [line[3:] for line in untracked],
        "diff_check": "pass" if diff_check.returncode == 0 else "fail",
    }


def main() -> int:
    failures: list[str] = []
    evidence = read(EVIDENCE, failures)
    loop_round = read(LOOP_ROUND, failures)

    for token in REQUIRED_TOKENS:
        if token not in evidence:
            failures.append(f"missing evidence token: {token}")
    for token in FORBIDDEN_TOKENS:
        if token in evidence:
            failures.append(f"forbidden positive claim in evidence: {token}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")
    for repo_name, task_id in REPOS.items():
        if repo_name not in evidence:
            failures.append(f"missing repo in evidence: {repo_name}")
        if task_id not in evidence:
            failures.append(f"missing task in evidence: {task_id}")

    delegate_result = run(["python3", str(DELEGATE_VALIDATOR)])
    delegate_values = parse_kv_output(delegate_result.stdout)
    if delegate_result.returncode != 0:
        failures.append("external loop gate delegate validator failed: " + (delegate_result.stderr or delegate_result.stdout).strip())
    if delegate_values.get("project_group_external_loop_gate_delegates") != "pass":
        failures.append(f"delegate validator not pass: {delegate_values}")
    if delegate_values.get("checked_repos") != "3":
        failures.append(f"delegate validator checked_repos mismatch: {delegate_values.get('checked_repos')}")
    if delegate_values.get("delegation_only") != "true":
        failures.append(f"delegate validator delegation_only mismatch: {delegate_values.get('delegation_only')}")
    if delegate_values.get("gfis_status_ceiling") != "repair_required":
        failures.append(f"delegate validator gfis_status_ceiling mismatch: {delegate_values.get('gfis_status_ceiling')}")

    repo_results = {repo_name: validate_repo(repo_name, failures) for repo_name in REPOS}
    result = {
        "project_group_external_loop_gate_delegate_baseline_20260627": "pass" if not failures else "fail",
        "delegated_repo_count": len(REPOS),
        "delegate_validator": delegate_values,
        "repos": repo_results,
        "review_allowed": False,
        "stage_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "delete_allowed": False,
        "runtime_write_allowed": False,
        "status_promotion_allowed": False,
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
