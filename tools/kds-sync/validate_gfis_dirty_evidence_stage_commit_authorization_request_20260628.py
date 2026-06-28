#!/usr/bin/env python3
"""Validate GFIS dirty evidence stage/commit authorization request."""

from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
DOC = ROOT / "docs/harness/evidence/gfis-dirty-evidence-stage-commit-authorization-request-20260628.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_gfis_dirty_evidence_stage_commit_authorization_request_20260628: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-c", "core.quotePath=false", *args], cwd=GFIS_ROOT, text=True, capture_output=True, check=False)


def live_counts() -> tuple[int, dict[str, int]]:
    result = run_git(["status", "--porcelain=v1"])
    require(result.returncode == 0, f"git status failed: {result.stdout}{result.stderr}")
    counts: Counter[str] = Counter()
    for line in result.stdout.splitlines():
        status = line[:2]
        lower_path = line[2:].lstrip().lower()
        require(not any(token in lower_path for token in [".env", "token", "secret", "private_key", ".pem", ".key"]), f"sensitive path in GFIS status: {lower_path}")
        require("D" not in status, f"deletion risk in GFIS status: {line}")
        if status == "??":
            counts["untracked"] += 1
        elif "M" in status:
            counts["modified"] += 1
        else:
            counts["other"] += 1
    return sum(counts.values()), dict(counts)


def require_doc_tokens(text: str) -> None:
    required = [
        "gfis_dirty_evidence_stage_commit_authorization_request_20260628 = prepared",
        "mainline = GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001",
        "request_item_count = 2",
        "authorization_granted_count = 0",
        "action_executed_count = 0",
        "development_ready_for_real_business_validation = candidate_confirmed_for_entry_record",
        "real_business_validation_lane = pending_source_of_record",
        "real_business_lane = repair_required",
        "gfis_ahead = 0",
        "gfis_behind = 0",
        "gfis_dirty_count = 91",
        "gfis_modified_count = 53",
        "gfis_untracked_count = 38",
        "gfis_deleted_or_missing_count = 0",
        "gfis_sensitive_path_count = 0",
        "gfis_manual_review_required_count = 0",
        "gfis_diff_check = pass",
        "gfis_current_staged_count = 0",
        "AUTH-GFIS-DIRTY-EVIDENCE-STAGE-20260628",
        "AUTH-GFIS-DIRTY-EVIDENCE-COMMIT-20260628",
        "stage_allowed = false",
        "commit_allowed = false",
        "push_allowed = false",
        "delete_allowed = false",
        "cleanup_allowed = false",
        "deploy_allowed = false",
        "real_external_api_allowed = false",
        "real_kds_api_allowed = false",
        "status_promotion_allowed = false",
        "authorization_granted = false",
        "action_executed = false",
        "stage_executed = false",
        "commit_executed = false",
        "push_executed = false",
        "accepted = false",
        "integrated = false",
        "production_ready = false",
        "customer_accepted = false",
    ]
    for token in required:
        require(token in text, f"missing token: {token}")

    forbidden = [
        "authorization_granted = true",
        "action_executed = true",
        "stage_allowed = true",
        "commit_allowed = true",
        "push_allowed = true",
        "delete_allowed = true",
        "cleanup_allowed = true",
        "deploy_allowed = true",
        "real_external_api_allowed = true",
        "real_kds_api_allowed = true",
        "status_promotion_allowed = true",
        "stage_executed = true",
        "commit_executed = true",
        "push_executed = true",
        "real_business_verified = true",
        "accepted = true",
        "integrated = true",
        "production_ready = true",
        "customer_accepted = true",
        "真实业务验证已完成",
        "真实 KDS API 已同步",
    ]
    for token in forbidden:
        require(token not in text, f"forbidden token: {token}")


def main() -> int:
    require(DOC.exists(), f"missing doc: {DOC.relative_to(ROOT)}")
    total, counts = live_counts()
    require(total == 91, f"GFIS dirty count changed: {total}")
    require(counts.get("modified") == 53, f"GFIS modified count changed: {counts}")
    require(counts.get("untracked") == 38, f"GFIS untracked count changed: {counts}")
    require(counts.get("other", 0) == 0, f"GFIS has unexpected status entries: {counts}")

    cached = run_git(["diff", "--cached", "--name-only"])
    require(cached.returncode == 0, f"git diff --cached failed: {cached.stdout}{cached.stderr}")
    require(not cached.stdout.strip(), "GFIS already has staged files")

    ahead_behind = run_git(["rev-list", "--left-right", "--count", "@{upstream}...HEAD"])
    require(ahead_behind.returncode == 0, f"GFIS ahead/behind check failed: {ahead_behind.stdout}{ahead_behind.stderr}")
    require(ahead_behind.stdout.strip() == "0\t0", f"GFIS ahead/behind changed: {ahead_behind.stdout.strip()}")

    diff_check = run_git(["diff", "--check"])
    require(diff_check.returncode == 0, f"GFIS diff check failed: {diff_check.stdout}{diff_check.stderr}")

    text = DOC.read_text(encoding="utf-8", errors="ignore")
    require_doc_tokens(text)

    print(
        "gfis_dirty_evidence_stage_commit_authorization_request_20260628=pass "
        "status=prepared request_item_count=2 authorization_granted_count=0 action_executed_count=0 "
        "gfis_dirty_count=91 gfis_modified_count=53 gfis_untracked_count=38 "
        "gfis_deleted_or_missing_count=0 gfis_sensitive_path_count=0 gfis_current_staged_count=0 "
        "stage_allowed=false commit_allowed=false push_allowed=false "
        "accepted=false integrated=false production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
