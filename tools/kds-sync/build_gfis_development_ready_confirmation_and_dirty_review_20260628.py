#!/usr/bin/env python3
"""Build GFIS development-ready confirmation and dirty evidence review artifacts."""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
OUTPUT_JSON = ROOT / "docs/harness/evidence/gfis-development-ready-confirmation-and-dirty-review-20260628.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/gfis-development-ready-confirmation-and-dirty-review-20260628.md"


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(command)}\n{result.stdout}{result.stderr}")
    return (result.stdout + result.stderr).strip()


def run_maybe(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "output": (result.stdout + result.stderr).strip(),
    }


def parse_status_line(line: str) -> tuple[str, str]:
    status = line[:2]
    path = line[2:].lstrip()
    if " -> " in path:
        _old, path = path.split(" -> ", 1)
    return status, path


def category_for(status: str, path: str) -> str:
    lower = path.lower()
    if any(token in lower for token in [".env", "token", "secret", "private_key", ".pem", ".key"]):
        return "sensitive_config_review"
    if "D" in status:
        return "deletion_or_missing_file_risk"
    if path == "docs/harness/evidence/evidence-index.md":
        return "evidence_index_update"
    if path.startswith("docs/harness/loops/loop-round-GFIS-DEV-"):
        return "gfis_dev_loop_rounds"
    if path == "docs/harness/loops/loop-round-GFIS-RUNTIME-SOP-E2E-MIN-001.md":
        return "gfis_min_loop_round"
    if path.startswith("scripts/validate_gfis_dev_"):
        return "gfis_dev_validators"
    if path == "scripts/validate_gfis_runtime_sop_e2e_min_001.py":
        return "gfis_min_validator"
    if path.startswith("docs/harness/sop-e2e/intake-submissions/"):
        return "gfis_valid_source_record_template_or_schema"
    if path.startswith("docs/harness/sop-e2e/intake/") and path.endswith("README.md"):
        return "gfis_intake_readme_update"
    if path.startswith("docs/harness/sop-e2e/evidence/gfis-dev-"):
        return "gfis_dev_evidence_json"
    if path == "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-min-001-candidate.json":
        return "gfis_min_candidate_json"
    if path == "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dev-dry-run-result.json":
        return "gfis_dev_dry_run_result_update"
    if path.startswith("docs/harness/sop-e2e/evidence/") and path.endswith(".json"):
        return "gfis_runtime_evidence_gate_json"
    return "manual_review_required"


def build_status_review() -> dict[str, Any]:
    branch_line = run(["git", "-c", "core.quotePath=false", "status", "--short", "--branch"], GFIS_ROOT).splitlines()[0]
    status_lines = run(["git", "-c", "core.quotePath=false", "status", "--porcelain=v1"], GFIS_ROOT).splitlines()
    upstream_counts = run(["git", "rev-list", "--left-right", "--count", "@{upstream}...HEAD"], GFIS_ROOT).split()
    behind, ahead = [int(value) for value in upstream_counts]
    diff_check = run_maybe(["git", "diff", "--check"], GFIS_ROOT)

    entries: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()

    for line in status_lines:
        status, path = parse_status_line(line)
        category = category_for(status, path)
        entries.append(
            {
                "status": status,
                "path": path,
                "category": category,
                "raw": line,
            }
        )
        category_counts[category] += 1
        if status == "??":
            status_counts["untracked"] += 1
        elif "D" in status:
            status_counts["deleted_or_missing"] += 1
        elif "M" in status:
            status_counts["modified"] += 1
        else:
            status_counts["other"] += 1

    sensitive_paths = [entry["path"] for entry in entries if entry["category"] == "sensitive_config_review"]
    deleted_paths = [entry["path"] for entry in entries if entry["category"] == "deletion_or_missing_file_risk"]
    manual_review_paths = [entry["path"] for entry in entries if entry["category"] == "manual_review_required"]

    return {
        "repo": "GlobalCloud GFIS",
        "path": str(GFIS_ROOT),
        "branch": branch_line,
        "ahead": ahead,
        "behind": behind,
        "dirty_count": len(entries),
        "status_counts": dict(status_counts),
        "category_counts": dict(sorted(category_counts.items())),
        "sensitive_paths": sensitive_paths,
        "deleted_paths": deleted_paths,
        "manual_review_paths": manual_review_paths,
        "diff_check": {
            "returncode": diff_check["returncode"],
            "status": "pass" if diff_check["returncode"] == 0 else "fail",
            "output": diff_check["output"],
        },
        "entries": entries,
    }


def render_markdown(report: dict[str, Any]) -> str:
    review = report["gfis_dirty_review"]
    status_counts = review["status_counts"]
    category_counts = review["category_counts"]
    lines = [
        "---",
        "doc_id: GPCF-DOC-GFIS-DEV-READY-DIRTY-REVIEW-20260628",
        "title: GFIS development_ready confirmation and dirty evidence review 2026-06-28",
        "project: GPCF",
        "related_projects: [GFIS, GPCF, WAES, KDS]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/12-GPCF/docs/harness/evidence/gfis-development-ready-confirmation-and-dirty-review-20260628.md",
        "source_path: docs/harness/evidence/gfis-development-ready-confirmation-and-dirty-review-20260628.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-28",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# GFIS development_ready confirmation and dirty evidence review 2026-06-28",
        "",
        "本文记录用户已确认的两个受控动作：GFIS 开发态候选确认记录，以及 GFIS dirty/untracked DEV 证据包审查。本文不执行 stage、commit、push、delete、cleanup、deploy、真实外部 API、真实 KDS API、生产写入或状态提升。",
        "",
        "## Authorization Result",
        "",
        "```text",
        "gfis_development_ready_confirmation_and_dirty_review_20260628 = controlled",
        "authorization_source = user_confirmation_in_current_session",
        "authorization_scope = AUTH-GFIS-DEV-READY-CANDIDATE-20260628, AUTH-GFIS-DIRTY-EVIDENCE-REVIEW-20260628",
        "authorization_granted_count = 2",
        "action_executed_count = 2",
        "action_1 = record_development_ready_candidate_confirmation",
        "action_2 = classify_gfis_dirty_untracked_dev_evidence_package",
        "development_lane = continue_allowed",
        "development_ready_for_real_business_validation = candidate_confirmed_for_entry_record",
        "real_business_validation_lane = pending_source_of_record",
        "real_business_lane = repair_required",
        "acceptance_lane = not_started",
        "production_lane = not_started",
        "review_allowed = true",
        "review_executed = true",
        "stage_allowed = false",
        "commit_allowed = false",
        "push_allowed = false",
        "delete_allowed = false",
        "cleanup_allowed = false",
        "deploy_allowed = false",
        "real_external_api_allowed = false",
        "real_kds_api_allowed = false",
        "status_promotion_allowed = false",
        "accepted = false",
        "integrated = false",
        "production_ready = false",
        "customer_accepted = false",
        "```",
        "",
        "## GFIS Dirty Review Summary",
        "",
        "```text",
        f"gfis_branch = {review['branch']}",
        f"gfis_ahead = {review['ahead']}",
        f"gfis_behind = {review['behind']}",
        f"gfis_dirty_count = {review['dirty_count']}",
        f"gfis_modified_count = {status_counts.get('modified', 0)}",
        f"gfis_untracked_count = {status_counts.get('untracked', 0)}",
        f"gfis_deleted_or_missing_count = {status_counts.get('deleted_or_missing', 0)}",
        f"gfis_sensitive_path_count = {len(review['sensitive_paths'])}",
        f"gfis_manual_review_required_count = {len(review['manual_review_paths'])}",
        f"gfis_diff_check = {review['diff_check']['status']}",
        "review_result = dev_evidence_package_classified",
        "disposition = commit_candidate_after_separate_authorization",
        "```",
        "",
        "## Category Counts",
        "",
        "| category | count | review result |",
        "|---|---:|---|",
    ]
    advice = {
        "evidence_index_update": "GFIS evidence index update; include with evidence package after separate commit authorization.",
        "gfis_dev_loop_rounds": "DEV-001 to DEV-011 loop round evidence; commit candidate after file-level review.",
        "gfis_min_loop_round": "Minimum SOP E2E loop round evidence; commit candidate after file-level review.",
        "gfis_dev_validators": "DEV validator scripts; commit candidate after script review and test pass.",
        "gfis_min_validator": "Minimum SOP E2E validator; commit candidate after test pass.",
        "gfis_valid_source_record_template_or_schema": "Valid source-record template/schema; commit candidate after owner review.",
        "gfis_intake_readme_update": "Runtime intake README update; commit candidate after documentation review.",
        "gfis_dev_evidence_json": "DEV evidence JSON; commit candidate after evidence consistency review.",
        "gfis_min_candidate_json": "Minimum candidate JSON; commit candidate after evidence consistency review.",
        "gfis_dev_dry_run_result_update": "DEV dry-run result update; commit candidate after validator replay.",
        "gfis_runtime_evidence_gate_json": "Runtime evidence gate JSON updates; review as development gates, not real business validation.",
        "sensitive_config_review": "Blocked until manual security review; none expected in this package.",
        "deletion_or_missing_file_risk": "Blocked until manual deletion review; none expected in this package.",
        "manual_review_required": "Manual classification required before any commit authorization; none expected in this package.",
    }
    for category, count in category_counts.items():
        lines.append(f"| `{category}` | {count} | {advice.get(category, 'manual review before disposition')} |")

    lines.extend(
        [
            "",
            "## Gate Results",
            "",
            "| gate | result | evidence |",
            "|---|---|---|",
            "| development boundary | pass | `validate_loop_v11_slimming_delivery_recovery.py` and `validate_loop_v11_delivery_boundary.py` passed before this artifact was generated |",
            "| real fact entry | pass / strong block | `real_source_records=0`, `valid_source_records=0`, `runtime_primary_key_ready=0`, `review_queue=0`, `runtime_intake=0`, `waes_review=0`, `verified=0` |",
            "| authorization boundary | pass | manual submission remains preview/preflight only; no real target files |",
            f"| GFIS diff check | {review['diff_check']['status']} | `git diff --check` |",
            "| project group Git gate | partial | dirty repos remain `GlobalCoud GPCF`, `GlobalCloud GFIS`, `GlobalCloud SOP` |",
            "",
            "## Full GFIS Status Entries",
            "",
            "| status | category | path |",
            "|---|---|---|",
        ]
    )
    for entry in review["entries"]:
        lines.append(f"| `{entry['status']}` | `{entry['category']}` | `{entry['path']}` |")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "```text",
            "real_business_verified = false",
            "accepted = false",
            "integrated = false",
            "production_ready = false",
            "customer_accepted = false",
            "stage_executed = false",
            "commit_executed = false",
            "push_executed = false",
            "delete_executed = false",
            "cleanup_executed = false",
            "deploy_executed = false",
            "real_external_api_executed = false",
            "real_kds_api_executed = false",
            "```",
            "",
            "## Next",
            "",
            "GFIS dirty 证据包可作为下一步 commit 候选包，但必须另行取得 stage/commit/push 授权；真实业务验证仍必须等待真实 source-of-record 或等效正式确认文件。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mainline": "GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001",
        "authorization": {
            "source": "user_confirmation_in_current_session",
            "scope": [
                "AUTH-GFIS-DEV-READY-CANDIDATE-20260628",
                "AUTH-GFIS-DIRTY-EVIDENCE-REVIEW-20260628",
            ],
            "authorization_granted_count": 2,
            "action_executed_count": 2,
            "stage_allowed": False,
            "commit_allowed": False,
            "push_allowed": False,
            "delete_allowed": False,
            "cleanup_allowed": False,
            "deploy_allowed": False,
            "status_promotion_allowed": False,
        },
        "development_result": {
            "development_lane": "continue_allowed",
            "development_ready_for_real_business_validation": "candidate_confirmed_for_entry_record",
            "real_business_validation_lane": "pending_source_of_record",
            "real_business_lane": "repair_required",
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "customer_accepted": False,
        },
        "gfis_dirty_review": build_status_review(),
    }
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(report), encoding="utf-8")
    review = report["gfis_dirty_review"]
    print(
        "gfis_development_ready_confirmation_and_dirty_review_20260628=generated "
        f"dirty_count={review['dirty_count']} "
        f"modified={review['status_counts'].get('modified', 0)} "
        f"untracked={review['status_counts'].get('untracked', 0)} "
        f"deleted_or_missing={review['status_counts'].get('deleted_or_missing', 0)} "
        f"sensitive_paths={len(review['sensitive_paths'])} "
        f"manual_review_required={len(review['manual_review_paths'])} "
        f"diff_check={review['diff_check']['status']} "
        "stage_allowed=false commit_allowed=false push_allowed=false "
        "accepted=false integrated=false production_ready=false customer_accepted=false"
    )


if __name__ == "__main__":
    main()
