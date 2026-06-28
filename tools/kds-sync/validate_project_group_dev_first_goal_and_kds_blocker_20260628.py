#!/usr/bin/env python3
"""Validate the dev-first Loop goal prompt and KDS sensitive blocker classification."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
KDS_ROOT = PROJECT_ROOT / "GlobalCloud KDS"
GOAL_PROMPT = ROOT / "docs/harness/evidence/globalcloud-project-group-dev-first-loop-goal-prompt-20260628.md"
KDS_EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-kds-sensitive-blocker-classification-20260628.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DEV-FIRST-KDS-BLOCKER-001.md"
KDS_DEV_VALIDATOR = KDS_ROOT / "scripts/validate_kds_dev_001_local_api_sync_dry_run.py"

GOAL_TOKENS = [
    "dev_first_loop_goal_prompt = active",
    "default_local_dev_allowed = true",
    "redundant_governance_reduction = true",
    "evidence_generation_policy = minimal_required",
    "first_execution_item = KDS-BLOCKER-001",
    "kds_dev_001_local_api_sync_dry_run = pass_check_only",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "deploy_allowed = false",
    "runtime_write_allowed = false",
    "schema_migrate_allowed = false",
    "real_api_write_allowed = false",
    "status_promotion_allowed = false",
]

KDS_TOKENS = [
    "kds_sensitive_blocker_classification = resolved_not_in_git_status",
    "kds_sensitive_blocker_live_classification = clean_not_present_in_status",
    "kds_dev_001_local_api_sync_dry_run = pass_check_only",
    "kds_hard_blocker_unknown = false",
    "kds_git_gate_status = no_longer_blocked_by_kds_sensitive_path",
    "kds_blocker_reason = env_production_example_not_present_in_live_git_status",
    "kds_real_secret_detected = false",
    "kds_placeholder_token_detected = not_observed",
    "kds_default_password_detected = not_observed",
    "kds_production_write_detected = false",
    "kds_schema_migrate_detected = false",
    "kds_real_api_write_detected = false",
    "kds_safe_to_auto_commit = false",
    "kds_live_api_called = false",
    "kds_sync_executed = false",
    "kds_docker_started = false",
    "kds_gbrain_write_executed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "deploy_allowed = false",
    "runtime_write_allowed = false",
    "schema_migrate_allowed = false",
    "real_api_write_allowed = false",
    "status_promotion_allowed = false",
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

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"),
]


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def validate_kds_live(failures: list[str]) -> dict[str, object]:
    if not KDS_ROOT.exists():
        failures.append(f"missing KDS repo: {KDS_ROOT}")
        return {}

    status = run(["git", "-c", "core.quotePath=false", "status", "--porcelain=v1"], KDS_ROOT)
    status_lines = [line for line in status.stdout.splitlines() if line.strip()]
    tracked_modified = [line for line in status_lines if line.startswith(" M ") or line.startswith("M ")]
    untracked = [line for line in status_lines if line.startswith("?? ")]

    diff_check = run(["git", "diff", "--check", "--", "."], KDS_ROOT)
    shortstat = run(["git", "diff", "--shortstat", "--", "."], KDS_ROOT).stdout.strip()
    env_path = KDS_ROOT / ".env.production.example"
    env_text = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
    env_assignments: dict[str, str] = {}
    for line in env_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        env_assignments[key.strip()] = value.strip()

    if status.returncode != 0:
        failures.append(f"KDS git status failed: {status.stdout or status.stderr}")
    if diff_check.returncode != 0:
        failures.append(f"KDS diff-check failed: {diff_check.stdout or diff_check.stderr}")
    env_template_in_status = ".env.production.example" in status.stdout
    if env_path.exists():
        if env_assignments.get("KDS_DEVELOPMENT_SPACE_TOKEN") != "change-me":
            failures.append("KDS template token placeholder missing")
        if env_assignments.get("POSTGRES_PASSWORD") != "gbrain":
            failures.append("KDS default postgres password marker missing")
    for pattern in SECRET_PATTERNS:
        if pattern.search(env_text):
            failures.append(f"real secret-like pattern detected: {pattern.pattern}")

    kds_dev_values: dict[str, str] = {}
    if not KDS_DEV_VALIDATOR.exists():
        failures.append("KDS-DEV-001 validator missing")
    else:
        kds_dev = run(["python3", str(KDS_DEV_VALIDATOR.relative_to(KDS_ROOT))], KDS_ROOT)
        kds_dev_values = parse_kv_output(kds_dev.stdout)
        if kds_dev.returncode != 0:
            failures.append(f"KDS-DEV-001 validator failed: {kds_dev.stdout or kds_dev.stderr}")
        elif "kds_dev_001_local_api_sync_dry_run=pass" not in kds_dev.stdout:
            failures.append("KDS-DEV-001 validator output missing pass marker")
        if kds_dev_values.get("commit_allowed") != "true":
            failures.append("KDS-DEV-001 validator must allow commit after Git-safe rename")
        if kds_dev_values.get("push_allowed") != "true":
            failures.append("KDS-DEV-001 validator must allow push after Git-safe rename")
        for key in ["live_api_called", "sync_executed", "docker_started", "gbrain_write_executed"]:
            if kds_dev_values.get(key) != "false":
                failures.append(f"KDS-DEV-001 must keep {key}=false")

    return {
        "tracked_modified_count": len(tracked_modified),
        "untracked_entry_count": len(untracked),
        "diff_check": "pass" if diff_check.returncode == 0 else "fail",
        "shortstat": shortstat,
        "env_template_present": env_path.exists(),
        "env_template_in_git_status": env_template_in_status,
        "sensitive_path_state": "active_sensitive_template_candidate"
        if env_path.exists() or env_template_in_status
        else "resolved_not_in_git_status",
        "env_values_redacted": True,
        "env_assignment_keys": sorted(env_assignments),
        "placeholder_token": "change-me" in env_text,
        "default_password": "POSTGRES_PASSWORD=gbrain" in env_text,
        "owner_review_required": True,
        "safe_to_auto_commit": False,
        "kds_dev_001_local_api_sync_dry_run": KDS_DEV_VALIDATOR.exists(),
        "kds_dev_001_output": kds_dev_values,
    }


def main() -> int:
    failures: list[str] = []
    goal_prompt = read(GOAL_PROMPT, failures)
    kds_evidence = read(KDS_EVIDENCE, failures)
    loop_round = read(LOOP_ROUND, failures)

    for token in GOAL_TOKENS:
        if token not in goal_prompt:
            failures.append(f"missing goal prompt token: {token}")
    for token in KDS_TOKENS:
        if token not in kds_evidence:
            failures.append(f"missing KDS evidence token: {token}")
    for token in FORBIDDEN_TOKENS:
        if token in goal_prompt or token in kds_evidence:
            failures.append(f"forbidden token present: {token}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")

    kds_live = validate_kds_live(failures)
    current_classification = (
        "classified_sensitive_template_candidate"
        if kds_live.get("sensitive_path_state") == "active_sensitive_template_candidate"
        else "resolved_not_in_git_status"
    )
    live_classification = (
        "masked_live_check"
        if kds_live.get("sensitive_path_state") == "active_sensitive_template_candidate"
        else "clean_not_present_in_status"
    )

    result = {
        "project_group_dev_first_goal_and_kds_blocker": "pass" if not failures else "fail",
        "dev_first_loop_goal_prompt": "active",
        "first_execution_item": "KDS-BLOCKER-001",
        "second_execution_item": "KDS-DEV-001",
        "kds_sensitive_blocker_classification": current_classification,
        "kds_sensitive_blocker_live_classification": live_classification,
        "kds_live": kds_live,
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
