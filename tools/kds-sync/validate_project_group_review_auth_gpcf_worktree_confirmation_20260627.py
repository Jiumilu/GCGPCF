#!/usr/bin/env python3
"""Validate the 2026-06-27 REVIEW-AUTH GPCF worktree confirmation request."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-review-auth-gpcf-worktree-confirmation-20260627.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-GPCF-WORKTREE-CONFIRMATION-001.md"
AUTH_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md"
GPCF_PACKAGES = ROOT / "docs/harness/evidence/globalcloud-project-group-gpcf-worktree-review-packages-20260627.md"
PRE_WAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"

PACKAGES = ["GPCF-RP1", "GPCF-RP2", "GPCF-RP3", "GPCF-RP4", "GPCF-RP5", "GPCF-RP6", "GPCF-RP7"]

REQUIRED_TOKENS = [
    "review_auth_gpcf_worktree_confirmation_request = prepared",
    "review_auth_id = REVIEW-AUTH-GPCF-WORKTREE-20260627",
    "review_package_count = 7",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "runtime_write_allowed = false",
    "schema_migrate_allowed = false",
    "real_api_write_allowed = false",
    "review_boundary_repo_count | `6`",
    "noise_cleanup_repo_count | `1`",
    "review_boundary_repos_current | `GlobalCloud AAAS`、`GlobalCoud GPCF`、`GlobalCloud XWAIL`、`GlobalCloud GFIS`、`GlobalCloud KDS`、`GlobalCloud SOP`",
    "noise_cleanup_repo_current | `WAS世界资产体系(.DS_Store)`",
    "pre_wave1_review_authorization_required = true",
    "pre_wave1_review_authorization_id = GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "pre_wave1_entry_status = pending_confirmation",
    "只有在 GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001 的 6 仓 review 边界先完成结论登记后",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

FORBIDDEN_TRUE_TOKENS = [
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "runtime_write_allowed = true",
    "schema_migrate_allowed = true",
    "real_api_write_allowed = true",
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
    summary = payload.get("summary", {})
    if gate != "blocked":
        failures.append(f"git gate not blocked: {gate}")
    if summary.get("dirty_repos") != ["GlobalCloud AAAS", "WAS世界资产体系", "GlobalCoud GPCF", "GlobalCloud XWAIL", "GlobalCloud GFIS", "GlobalCloud KDS", "GlobalCloud SOP"]:
        failures.append(f"unexpected dirty repos: {summary.get('dirty_repos')}")
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
    auth_matrix = read(AUTH_MATRIX, failures)
    gpcf_packages = read(GPCF_PACKAGES, failures)
    pre_wave1 = read(PRE_WAVE1, failures)

    for token in REQUIRED_TOKENS:
        if token not in evidence:
            failures.append(f"missing confirmation token: {token}")
    for token in FORBIDDEN_TRUE_TOKENS:
        if token in evidence:
            failures.append(f"forbidden true token in confirmation request: {token}")
    for package in PACKAGES:
        if package not in evidence:
            failures.append(f"missing package in confirmation request: {package}")
        if package not in gpcf_packages:
            failures.append(f"missing package in GPCF review evidence: {package}")
    for token in [
        "authorization_layer_matrix = prepared",
        "REVIEW-AUTH-GPCF-WORKTREE-20260627",
        "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    ]:
        if token not in auth_matrix:
            failures.append(f"missing auth matrix prerequisite: {token}")
    for token in [
        "project_group_pre_wave1_review_authorization_request_20260627 = prepared",
        "pre_wave1_review_authorization_ready",
        "pending_confirmation",
    ]:
        if token not in pre_wave1:
            failures.append(f"missing pre-wave1 prerequisite: {token}")
    for token in ["gpcf_worktree_review_packages = recheck_required", "review_package_count = 7"]:
        if token not in gpcf_packages:
            failures.append(f"missing GPCF review prerequisite: {token}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")

    gate = validate_git_gate(failures)
    result = {
        "project_group_review_auth_gpcf_worktree_confirmation": "pass" if not failures else "fail",
        "review_auth_id": "REVIEW-AUTH-GPCF-WORKTREE-20260627",
        "review_package_count": 7,
        "git_gate": gate,
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "review_allowed": False,
        "stage_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "runtime_write_allowed": False,
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
