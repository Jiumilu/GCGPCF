#!/usr/bin/env python3
"""Validate the dynamic project-group live status snapshot."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
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
CURRENT_JSON = ROOT / "docs/harness/evidence/project_group_live_status_current.json"
FRESHNESS_HOURS = 12
TZ = timezone(timedelta(hours=8))

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

VOLATILE_DIRTY_ALLOWLIST = ["GlobalCoud GPCF"]

CORE_DOC_TOKENS = [
    "GPCF-LIVE-STATUS-SNAPSHOT-20260626-001",
    "project_group_live_status_snapshot_20260626 = controlled",
    "live_status_snapshot_controlled",
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


def load_current_snapshot(failures: list[str]) -> dict:
    if not CURRENT_JSON.exists():
        failures.append(f"missing current snapshot: {CURRENT_JSON}")
        return {}
    try:
        return json.loads(CURRENT_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"failed to parse current snapshot: {exc}")
        return {}


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(STATUS, failures)])
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)
    current = load_current_snapshot(failures)

    for token in CORE_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in live status snapshot: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive claim: {token}")

    generated_at_raw = str(current.get("generated_at") or "")
    if not generated_at_raw:
        failures.append("current snapshot missing generated_at")
    else:
        try:
            generated_at = datetime.fromisoformat(generated_at_raw)
            if datetime.now(TZ) - generated_at > timedelta(hours=FRESHNESS_HOURS):
                failures.append("current snapshot is stale")
        except ValueError:
            failures.append("current snapshot generated_at is invalid")

    observed_dirty: list[str] = []
    observed_ahead: list[str] = []
    sensitive_repos: list[str] = []
    pass_repo_count = 0
    live_dirty_counts: dict[str, int] = {}

    dirty_details = current.get("dirty_details", {})

    for repo_name in EXPECTED_REPOS:
        repo = PROJECT_ROOT / repo_name
        if not repo.exists():
            failures.append(f"missing repo: {repo_name}")
            continue
        try:
            lines = git_status(repo)
            ahead, behind = git_ahead_behind(repo)
        except subprocess.CalledProcessError as exc:
            failures.append(f"git scan failed for {repo_name}: {exc.stderr.strip()}")
            continue
        live_dirty_counts[repo_name] = len(lines)
        if lines:
            observed_dirty.append(repo_name)
        if ahead > 0:
            observed_ahead.append(repo_name)
        detail = dirty_details.get(repo_name, {})
        if detail.get("sensitive_paths"):
            sensitive_repos.append(repo_name)
        if not lines and ahead == 0 and behind == 0:
            pass_repo_count += 1

    snapshot_observed_dirty = [str(item) for item in current.get("observed_dirty", [])]
    snapshot_observed_ahead = [str(item) for item in current.get("observed_ahead", [])]
    snapshot_stable_dirty = [str(item) for item in current.get("stable_dirty", [])]
    snapshot_stable_ahead = [str(item) for item in current.get("stable_ahead", [])]
    snapshot_volatile_dirty = [str(item) for item in current.get("volatile_dirty", [])]
    snapshot_review_boundary = [str(item) for item in current.get("review_boundary", [])]
    snapshot_sensitive_repos = [str(item) for item in current.get("sensitive_repos", [])]

    if snapshot_observed_dirty != observed_dirty:
        failures.append(f"observed_dirty mismatch: snapshot={snapshot_observed_dirty}, actual={observed_dirty}")
    if snapshot_observed_ahead != observed_ahead:
        failures.append(f"observed_ahead mismatch: snapshot={snapshot_observed_ahead}, actual={observed_ahead}")

    expected_volatile_dirty = sorted(set(observed_dirty) & set(VOLATILE_DIRTY_ALLOWLIST))
    if snapshot_volatile_dirty != expected_volatile_dirty:
        failures.append(f"volatile_dirty mismatch: snapshot={snapshot_volatile_dirty}, expected={expected_volatile_dirty}")

    if not set(snapshot_stable_dirty).issubset(set(snapshot_observed_dirty)):
        failures.append("stable_dirty must be a subset of observed_dirty")
    if not set(snapshot_stable_ahead).issubset(set(snapshot_observed_ahead)):
        failures.append("stable_ahead must be a subset of observed_ahead")
    expected_review_boundary = sorted(set(snapshot_stable_dirty) | set(snapshot_volatile_dirty) | set(snapshot_sensitive_repos))
    if snapshot_review_boundary != expected_review_boundary:
        failures.append(
            f"review_boundary mismatch: snapshot={snapshot_review_boundary}, expected={expected_review_boundary}"
        )
    if int(current.get("pass_repo_count", -1)) != pass_repo_count:
        failures.append(f"pass_repo_count mismatch: snapshot={current.get('pass_repo_count')}, actual={pass_repo_count}")
    if snapshot_sensitive_repos != sensitive_repos:
        failures.append(f"sensitive_repos mismatch: snapshot={snapshot_sensitive_repos}, actual={sensitive_repos}")

    result = {
        "gate": "project_group_live_status_snapshot_20260626",
        "status": "pass" if not failures else "fail",
        "checked_repo_count": len(EXPECTED_REPOS),
        "dirty_repo_count": len(observed_dirty),
        "dirty_repos": observed_dirty,
        "observed_ahead": observed_ahead,
        "stable_dirty_repos": snapshot_stable_dirty,
        "stable_ahead_repos": snapshot_stable_ahead,
        "optional_volatile_dirty_repos": snapshot_volatile_dirty,
        "review_boundary": snapshot_review_boundary,
        "live_dirty_counts": live_dirty_counts,
        "current_snapshot": str(CURRENT_JSON.relative_to(ROOT)),
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates the live status snapshot only; it does not delete files, stage, commit, push, sync KDS API, deploy, or grant accepted/integrated/customer acceptance status."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
