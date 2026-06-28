#!/usr/bin/env python3
"""Validate GFIS development-ready confirmation and dirty evidence review."""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
OUTPUT_JSON = ROOT / "docs/harness/evidence/gfis-development-ready-confirmation-and-dirty-review-20260628.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/gfis-development-ready-confirmation-and-dirty-review-20260628.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_gfis_development_ready_confirmation_and_dirty_review_20260628: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def load_report() -> dict[str, Any]:
    require(OUTPUT_JSON.exists(), f"missing json evidence: {OUTPUT_JSON.relative_to(ROOT)}")
    require(OUTPUT_MD.exists(), f"missing markdown evidence: {OUTPUT_MD.relative_to(ROOT)}")
    with OUTPUT_JSON.open(encoding="utf-8") as handle:
        data = json.load(handle)
    require(isinstance(data, dict), "json evidence must be an object")
    return data


def parse_status_line(line: str) -> tuple[str, str]:
    status = line[:2]
    path = line[2:].lstrip()
    if " -> " in path:
        _old, path = path.split(" -> ", 1)
    return status, path


def live_status_counts() -> tuple[list[str], dict[str, int]]:
    result = run(["git", "-c", "core.quotePath=false", "status", "--porcelain=v1"], GFIS_ROOT)
    require(result.returncode == 0, f"git status failed: {result.stdout}{result.stderr}")
    lines = result.stdout.splitlines()
    counts: Counter[str] = Counter()
    for line in lines:
        status, _path = parse_status_line(line)
        if status == "??":
            counts["untracked"] += 1
        elif "D" in status:
            counts["deleted_or_missing"] += 1
        elif "M" in status:
            counts["modified"] += 1
        else:
            counts["other"] += 1
    return lines, dict(counts)


def require_markdown_tokens(text: str) -> None:
    required_tokens = [
        "gfis_development_ready_confirmation_and_dirty_review_20260628 = controlled",
        "authorization_granted_count = 2",
        "action_executed_count = 2",
        "development_ready_for_real_business_validation = candidate_confirmed_for_entry_record",
        "real_business_validation_lane = pending_source_of_record",
        "real_business_lane = repair_required",
        "gfis_dirty_count = 91",
        "gfis_modified_count = 53",
        "gfis_untracked_count = 38",
        "gfis_deleted_or_missing_count = 0",
        "gfis_sensitive_path_count = 0",
        "gfis_manual_review_required_count = 0",
        "review_result = dev_evidence_package_classified",
        "disposition = commit_candidate_after_separate_authorization",
        "stage_allowed = false",
        "commit_allowed = false",
        "push_allowed = false",
        "accepted = false",
        "integrated = false",
        "production_ready = false",
        "customer_accepted = false",
        "stage_executed = false",
        "commit_executed = false",
        "push_executed = false",
    ]
    for token in required_tokens:
        require(token in text, f"markdown missing token: {token}")

    forbidden_tokens = [
        "accepted = true",
        "integrated = true",
        "production_ready = true",
        "customer_accepted = true",
        "stage_allowed = true",
        "commit_allowed = true",
        "push_allowed = true",
        "deploy_allowed = true",
        "real_external_api_allowed = true",
        "real_kds_api_allowed = true",
        "status_promotion_allowed = true",
        "real_business_verified = true",
    ]
    for token in forbidden_tokens:
        require(token not in text, f"markdown contains forbidden token: {token}")


def main() -> int:
    report = load_report()
    review = report.get("gfis_dirty_review", {})
    require(isinstance(review, dict), "missing gfis_dirty_review object")

    live_lines, live_counts = live_status_counts()
    require(review.get("dirty_count") == len(live_lines), "dirty_count does not match live GFIS status")
    require(review.get("status_counts") == live_counts, "status_counts do not match live GFIS status")
    require(review.get("dirty_count") == 91, "GFIS dirty count baseline changed")
    require(review.get("status_counts", {}).get("modified") == 53, "GFIS modified count baseline changed")
    require(review.get("status_counts", {}).get("untracked") == 38, "GFIS untracked count baseline changed")
    require(review.get("status_counts", {}).get("deleted_or_missing", 0) == 0, "GFIS deletion risk must remain 0")
    require(review.get("ahead") == 0 and review.get("behind") == 0, "GFIS ahead/behind must remain 0/0")
    require(review.get("diff_check", {}).get("status") == "pass", "GFIS diff check must pass")
    require(review.get("sensitive_paths") == [], "sensitive paths must remain empty")
    require(review.get("deleted_paths") == [], "deleted paths must remain empty")
    require(review.get("manual_review_paths") == [], "manual review paths must remain empty")

    authorization = report.get("authorization", {})
    require(authorization.get("authorization_granted_count") == 2, "authorization count must be 2")
    require(authorization.get("action_executed_count") == 2, "action count must be 2")
    for key in [
        "stage_allowed",
        "commit_allowed",
        "push_allowed",
        "delete_allowed",
        "cleanup_allowed",
        "deploy_allowed",
        "status_promotion_allowed",
    ]:
        require(authorization.get(key) is False, f"{key} must remain false")

    development_result = report.get("development_result", {})
    require(
        development_result.get("development_ready_for_real_business_validation")
        == "candidate_confirmed_for_entry_record",
        "development ready result must remain candidate_confirmed_for_entry_record",
    )
    require(development_result.get("real_business_validation_lane") == "pending_source_of_record", "real lane must remain pending")
    require(development_result.get("real_business_lane") == "repair_required", "real business lane must remain repair_required")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        require(development_result.get(key) is False, f"{key} must remain false")

    markdown = OUTPUT_MD.read_text(encoding="utf-8")
    require_markdown_tokens(markdown)

    print(
        "gfis_development_ready_confirmation_and_dirty_review_20260628=pass "
        f"dirty_count={review['dirty_count']} "
        f"modified={review['status_counts'].get('modified', 0)} "
        f"untracked={review['status_counts'].get('untracked', 0)} "
        f"deleted_or_missing={review['status_counts'].get('deleted_or_missing', 0)} "
        f"sensitive_paths={len(review['sensitive_paths'])} "
        f"manual_review_required={len(review['manual_review_paths'])} "
        "development_ready_for_real_business_validation=candidate_confirmed_for_entry_record "
        "real_business_validation_lane=pending_source_of_record "
        "stage_allowed=false commit_allowed=false push_allowed=false "
        "accepted=false integrated=false production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
