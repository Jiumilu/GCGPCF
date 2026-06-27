#!/usr/bin/env python3
"""Validate the 2026-06-27 REVIEW-AUTH GPCF-RP7 review conclusion."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-review-auth-gpcf-rp7-review-conclusion-20260627.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-GPCF-RP7-CONCLUSION-001.md"
GENERATED_ISOLATION = ROOT / "tools/kds-sync/validate_project_group_generated_output_dist_isolation_20260627.py"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"

REQUIRED_TOKENS = [
    "review_auth_id = REVIEW-AUTH-GPCF-WORKTREE-20260627",
    "review_package_id = GPCF-RP7",
    "rp7_review_conclusion_registered = true",
    "rp7_review_result = rework_required",
    "rp7_rework_reason = project_group_live_gate_blocked_with_sop_output_candidate",
    "rp7_stage_candidate = false",
    "rp7_commit_candidate = false",
    "rp7_push_candidate = false",
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
    "rp7_review_result = pass",
    "rp7_stage_candidate = true",
    "rp7_commit_candidate = true",
    "rp7_push_candidate = true",
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


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def validate_generated_isolation(failures: list[str]) -> str:
    result = run(["python3", str(GENERATED_ISOLATION)])
    if result.returncode != 0:
        failures.append(f"generated/output/dist isolation validator failed: {result.returncode}")
        return "fail"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"generated/output/dist isolation JSON parse failed: {exc}")
        return "fail"
    status = payload.get("project_group_generated_output_dist_isolation")
    if status != "pass":
        failures.append(f"generated/output/dist isolation recheck not controlled: {status}")
    return str(status)


def validate_git_gate(failures: list[str]) -> tuple[str, list[str]]:
    result = run(["python3", str(GIT_GATE), "--root", str(PROJECT_ROOT), "--allow-non-pass-exit-zero"])
    if result.returncode != 0:
        failures.append(f"project group git gate failed: {result.returncode}")
        return "unknown", []
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"project group git gate JSON parse failed: {exc}")
        return "unknown", []

    gate = str(payload.get("gate", "unknown"))
    summary = payload.get("summary", {})
    dirty_repos = summary.get("dirty_repos", [])
    if gate != "blocked":
        failures.append(f"git gate expected blocked for rework conclusion: {gate}")
    if dirty_repos != ["GlobalCloud AAAS", "WAS世界资产体系", "GlobalCoud GPCF", "GlobalCloud XWAIL", "GlobalCloud GFIS", "GlobalCloud KDS", "GlobalCloud SOP"]:
        failures.append(f"dirty repos do not match recorded drift: {dirty_repos}")
    for key in ["missing_repos", "ahead_repos", "behind_repos"]:
        if summary.get(key) != []:
            failures.append(f"{key} present: {summary.get(key)}")
    if summary.get("sensitive_repos") != ["GlobalCloud KDS"]:
        failures.append(f"sensitive_repos present: {summary.get('sensitive_repos')}")
    for repo in payload.get("repos", []):
        if repo.get("diff_check") != "pass":
            failures.append(f"repo diff-check not pass: {repo.get('name')}")
    return gate, dirty_repos


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

    generated_status = validate_generated_isolation(failures)
    gate, dirty_repos = validate_git_gate(failures)

    result = {
        "project_group_review_auth_gpcf_rp7_conclusion": "pass" if not failures else "fail",
        "review_auth_id": "REVIEW-AUTH-GPCF-WORKTREE-20260627",
        "review_package_id": "GPCF-RP7",
        "rp7_review_result": "rework_required",
        "rp7_rework_reason": "project_group_live_gate_blocked_with_sop_output_candidate",
        "generated_output_dist_isolation": generated_status,
        "git_gate": gate,
        "dirty_repos": dirty_repos,
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
