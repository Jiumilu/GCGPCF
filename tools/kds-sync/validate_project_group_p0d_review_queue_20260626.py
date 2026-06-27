#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group P0-D review queue evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-p0d-review-queue-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0D-REVIEW-QUEUE-001.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"

REQUIRED_TOKENS = [
    "p0d_review_queue_ready = true",
    "review_queue_count = 7",
    "development_start_allowed = true",
    "project_group_git_gate = blocked",
    "dirty_repo_count = 7",
    "sensitive_repos = GlobalCloud KDS(.env.production.example)",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "P0-D-Q1",
    "P0-D-Q2",
    "P0-D-Q3",
    "P0-D-Q4",
    "P0-D-Q5",
    "P0-D-Q6",
    "P0-D-Q7",
    "governance_evidence_kds_mirror_review_queue",
    "knowledge_import_governance_review_queue",
    "build_artifact_review_queue",
    "sop_operations_owner_review_queue",
    "local_artifact_isolation_queue",
    "release_review_queue",
]


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


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
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")

    gate = validate_git_gate(failures)
    result = {
        "project_group_p0d_review_queue": "pass" if not failures else "fail",
        "review_queue_count": 7,
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
