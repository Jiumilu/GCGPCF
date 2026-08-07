#!/usr/bin/env python3
"""Validate the read-only KDS apply-admission boundary for GPCF F-013."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
KDS_ROOT = ROOT.parent / "GlobalCloud KDS"
CHANGE_NAME = "adopt-knowledge-asset-envelope"
CHANGE_ROOT = KDS_ROOT / "openspec/changes" / CHANGE_NAME
FEATURE_PATH = ROOT / "features/active/F-013-knowledge-asset-model-system/feature.yaml"
MANIFEST_PATH = ROOT / "okf/knowledge-asset-contract-manifest.yaml"
KDS_CONTRACT_ROOT = KDS_ROOT / "knowledge_intake/contracts/gpcf/knowledge-asset-envelope/v0.1"
REQUIRED_CHANGE_FILES = (
    ".openspec.yaml",
    "proposal.md",
    "design.md",
    "specs/knowledge-asset-envelope-adoption/spec.md",
    "tasks.md",
)
DIRTY_BLOCKER = "kds_p1_apply_blocked_by_dirty_worktree"
CONTRACT_MIRROR_BLOCKER = "kds_contract_manifest_hash_mismatch"
CONTRACT_MIRROR_FILES = {
    "knowledge-asset-contract-manifest.yaml": MANIFEST_PATH,
    "knowledge-asset-envelope.schema.json": ROOT / "okf/knowledge-asset-envelope.schema.json",
    "knowledge-asset-envelope.example.json": ROOT / "okf/knowledge-asset-envelope.example.json",
    "knowledge-asset-vocabulary.yaml": ROOT / "okf/knowledge-asset-vocabulary.yaml",
    "knowledge-object.example.json": ROOT / "okf/knowledge-object.example.json",
    "knowledge-object-approved-copy.example.json": ROOT / "okf/knowledge-object-approved-copy.example.json",
}


def fail(reason: str) -> None:
    raise SystemExit(f"f013_kds_apply_admission_gate=fail reason={reason}")


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def load_yaml(path: Path) -> dict:
    require(path.is_file(), f"missing_yaml:{path}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(f"invalid_yaml:{path}:{exc}")
    require(isinstance(payload, dict), f"yaml_root_not_mapping:{path}")
    return payload


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=KDS_ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        fail(f"command_timeout:{Path(command[0]).name}")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_contract_mirror() -> tuple[list[str], list[str]]:
    missing: list[str] = []
    mismatched: list[str] = []
    for filename, source_path in CONTRACT_MIRROR_FILES.items():
        target_path = KDS_CONTRACT_ROOT / filename
        if not target_path.is_file():
            missing.append(filename)
        elif sha256_file(target_path) != sha256_file(source_path):
            mismatched.append(filename)
    return missing, mismatched


def main() -> int:
    require(KDS_ROOT.is_dir(), f"missing_kds_repo:{KDS_ROOT}")
    require((KDS_ROOT / ".git").exists(), "kds_repo_not_git_worktree")
    for relative_path in REQUIRED_CHANGE_FILES:
        require((CHANGE_ROOT / relative_path).is_file(), f"missing_change_artifact:{relative_path}")

    openspec = shutil.which("openspec")
    require(openspec is not None, "openspec_cli_unavailable")
    status_result = run([openspec, "status", "--change", CHANGE_NAME, "--json"])
    require(status_result.returncode == 0, "openspec_status_failed")
    try:
        status_payload = json.loads(status_result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"openspec_status_invalid_json:{exc}")
    require(status_payload.get("isComplete") is True, "openspec_planning_incomplete")

    validation_result = run([openspec, "validate", CHANGE_NAME, "--strict"])
    require(validation_result.returncode == 0, "openspec_strict_validation_failed")

    git_result = run(["git", "status", "--short", "--branch"])
    require(git_result.returncode == 0, "kds_git_status_failed")
    status_lines = [line for line in git_result.stdout.splitlines() if line]
    require(bool(status_lines) and status_lines[0].startswith("## "), "kds_git_status_missing_branch")
    branch_line = status_lines[0]
    ahead_match = re.search(r"ahead (\d+)", branch_line)
    behind_match = re.search(r"behind (\d+)", branch_line)
    ahead = int(ahead_match.group(1)) if ahead_match else 0
    behind = int(behind_match.group(1)) if behind_match else 0
    changed_entries = len(status_lines) - 1
    dirty = changed_entries > 0

    staged_result = run(["git", "diff", "--cached", "--name-only"])
    require(staged_result.returncode == 0, "kds_staged_status_failed")
    staged_entries = len([line for line in staged_result.stdout.splitlines() if line])

    feature = load_yaml(FEATURE_PATH)
    require(feature.get("id") == "F-013", "invalid_feature_id")
    require(feature.get("status") == "active", "feature_must_remain_active")
    require((feature.get("loop") or {}).get("current_step") == "evaluate", "feature_step_must_remain_evaluate")
    blockers = feature.get("blockers") or []
    require(isinstance(blockers, list), "feature_blockers_not_list")

    mirror_missing, mirror_mismatched = inspect_contract_mirror()
    contract_mirror_ready = not mirror_missing and not mirror_mismatched
    if contract_mirror_ready:
        require(CONTRACT_MIRROR_BLOCKER not in blockers, "stale_kds_contract_mirror_blocker")
    else:
        require(CONTRACT_MIRROR_BLOCKER in blockers, "missing_kds_contract_mirror_blocker")

    manifest = load_yaml(MANIFEST_PATH)
    status_boundary = manifest.get("status_boundary") or {}
    require(status_boundary.get("completion_status") == "not_complete", "completion_status_must_be_not_complete")
    require(status_boundary.get("kds_write_authorized") is False, "kds_write_must_remain_unauthorized")
    require(status_boundary.get("deployment_authorized") is False, "deployment_must_remain_unauthorized")

    if staged_entries:
        admission = "blocked_staged_changes"
    elif dirty:
        admission = "blocked_dirty_worktree"
    elif ahead:
        admission = "blocked_unreviewed_ahead"
    else:
        admission = "ready_for_authorization"

    if admission.startswith("blocked_"):
        require(DIRTY_BLOCKER in blockers, "missing_kds_apply_blocker")
    else:
        require(DIRTY_BLOCKER not in blockers, "stale_kds_apply_blocker")

    print(
        "f013_kds_apply_admission_gate=pass "
        f"change={CHANGE_NAME} planning=complete strict_validation=pass "
        f"kds_worktree_dirty={str(dirty).lower()} changed_entries={changed_entries} "
        f"staged_entries={staged_entries} ahead={ahead} behind={behind} "
        f"admission={admission} contract_mirror={'pass' if contract_mirror_ready else 'blocked'} "
        f"mirror_missing={len(mirror_missing)} mirror_mismatched={len(mirror_mismatched)} "
        "kds_write_authorized=false deployment_authorized=false "
        "completion_status=not_complete"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
