#!/usr/bin/env python3
"""Validate the 2026-06-27 GFIS dirty drift classification."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-gfis-dirty-drift-classification-20260627.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-GFIS-DIRTY-DRIFT-CLASSIFICATION-001.md"

REQUIRED_TOKENS = [
    "gfis_dirty_drift_classification = timestamp_only_evidence_drift",
    "gfis_dirty_drift_review_result = classified",
    "gfis_dirty_file_count = 51",
    "gfis_untracked_file_count = 0",
    "gfis_diff_check = pass",
    "gfis_changed_field_set = generated_at",
    "gfis_dirty_drift_hard_blocker = false",
    "gfis_dirty_drift_stage_candidate = false",
    "gfis_dirty_drift_commit_candidate = false",
    "gfis_dirty_drift_push_candidate = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "deploy_allowed = false",
    "runtime_write_allowed = false",
    "schema_migrate_allowed = false",
    "real_api_write_allowed = false",
    "status_promotion_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

FORBIDDEN_TOKENS = [
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "deploy_allowed = true",
    "runtime_write_allowed = true",
    "schema_migrate_allowed = true",
    "real_api_write_allowed = true",
    "status_promotion_allowed = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def validate_gfis(failures: list[str]) -> dict[str, object]:
    if not GFIS_ROOT.exists():
        failures.append(f"missing GFIS repo: {GFIS_ROOT}")
        return {}

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], GFIS_ROOT).stdout.strip()
    upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], GFIS_ROOT).stdout.strip()
    status = run(["git", "-c", "core.quotePath=false", "status", "--porcelain=v1"], GFIS_ROOT)
    status_lines = [line for line in status.stdout.splitlines() if line.strip()]
    dirty_paths = [line[3:] for line in status_lines if len(line) > 3]
    untracked = [line for line in status_lines if line.startswith("?? ")]

    diff_check = run(["git", "diff", "--check", "--", "."], GFIS_ROOT)
    shortstat = run(["git", "diff", "--shortstat", "--", "."], GFIS_ROOT).stdout.strip()
    diff = run(["git", "diff", "-U0", "--", "docs/harness/sop-e2e/evidence"], GFIS_ROOT)

    if branch != "main":
        failures.append(f"GFIS branch not main: {branch}")
    if upstream != "origin/main":
        failures.append(f"GFIS upstream not origin/main: {upstream}")
    if len(status_lines) != 51:
        failures.append(f"GFIS dirty count not 51: {len(status_lines)}")
    if untracked:
        failures.append(f"GFIS has untracked files: {untracked[:5]}")
    if diff_check.returncode != 0:
        failures.append(f"GFIS diff-check failed: {diff_check.stderr or diff_check.stdout}")
    if "51 files changed, 51 insertions(+), 51 deletions(-)" not in shortstat:
        failures.append(f"unexpected GFIS shortstat: {shortstat}")

    for path in dirty_paths:
        if not path.startswith("docs/harness/sop-e2e/evidence/"):
            failures.append(f"GFIS dirty path outside evidence: {path}")
        if not path.endswith(".json"):
            failures.append(f"GFIS dirty path is not JSON: {path}")

    changed_lines = []
    for line in diff.stdout.splitlines():
        if line.startswith(("+++", "---")):
            continue
        if line.startswith(("+", "-")):
            changed_lines.append(line)
            if '"generated_at":' not in line:
                failures.append(f"non-generated_at diff line: {line[:160]}")
    if len(changed_lines) != 102:
        failures.append(f"GFIS changed line count not 102: {len(changed_lines)}")

    return {
        "branch": branch,
        "upstream": upstream,
        "dirty_file_count": len(status_lines),
        "untracked_file_count": len(untracked),
        "shortstat": shortstat,
        "changed_line_count": len(changed_lines),
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
            failures.append(f"forbidden token in evidence: {token}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")

    gfis = validate_gfis(failures)
    result = {
        "project_group_gfis_dirty_drift_classification": "pass" if not failures else "fail",
        "gfis_dirty_drift_classification": "timestamp_only_evidence_drift",
        "gfis_dirty_drift_review_result": "classified",
        "gfis": gfis,
        "stage_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "delete_allowed": False,
        "deploy_allowed": False,
        "runtime_write_allowed": False,
        "schema_migrate_allowed": False,
        "real_api_write_allowed": False,
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
