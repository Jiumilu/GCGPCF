#!/usr/bin/env python3
"""Validate negative fixtures for OKF summary approval requests."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APPROVAL_VALIDATOR = ROOT / "tools/kds-sync/validate_okf_summary_approval_request.py"
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md"

FIXTURES = [
    {
        "name": "missing_required_fields",
        "fields": {
            "request_id": "NEG-001",
            "current_status": "pending_review",
        },
        "expected_status": "fail",
        "expected_reason_prefix": "missing_fields:",
    },
    {
        "name": "partial_confirmation",
        "fields": {
            "request_id": "NEG-002",
            "source_path": "09-status/kds-okf-v01-full-implementation-plan.md",
            "kds_path": "开发/91-治理与验收/09-status/kds-okf-v01-full-implementation-plan.md",
            "requested_summary_scope": "governance-purpose-only",
            "current_status": "pending_review",
            "confirmer": "lujunxiang",
            "confirmation_date": "2026-06-20",
            "owner_approval": "approved",
            "sensitivity_review": "pending",
            "approved_summary_scope": "pending",
        },
        "expected_status": "fail",
        "expected_reason_prefix": "partial_confirmation:",
    },
    {
        "name": "sensitivity_not_pass",
        "fields": {
            "request_id": "NEG-003",
            "source_path": "09-status/kds-okf-v01-full-implementation-plan.md",
            "kds_path": "开发/91-治理与验收/09-status/kds-okf-v01-full-implementation-plan.md",
            "requested_summary_scope": "governance-purpose-only",
            "current_status": "pending_review",
            "confirmer": "lujunxiang",
            "confirmation_date": "2026-06-20",
            "owner_approval": "approved",
            "sensitivity_review": "fail",
            "approved_summary_scope": "governance-purpose-only",
        },
        "expected_status": "fail",
        "expected_reason_prefix": "sensitivity_review_not_pass",
    },
    {
        "name": "pending_request_allowed",
        "fields": {
            "request_id": "NEG-004",
            "source_path": "09-status/kds-okf-v01-full-implementation-plan.md",
            "kds_path": "开发/91-治理与验收/09-status/kds-okf-v01-full-implementation-plan.md",
            "requested_summary_scope": "governance-purpose-only",
            "current_status": "pending_review",
            "confirmer": "pending",
            "confirmation_date": "pending",
            "owner_approval": "pending",
            "sensitivity_review": "pending",
            "approved_summary_scope": "pending",
        },
        "expected_status": "pending_review",
        "expected_reason_prefix": "awaiting_human_confirmation",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_validator():
    spec = importlib.util.spec_from_file_location("okf_summary_approval_request", APPROVAL_VALIDATOR)
    if spec is None or spec.loader is None:
        raise SystemExit("okf_summary_approval_negative_fixtures=fail reason=validator_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_request(fields: dict[str, str]) -> str:
    rows = "\n".join(f"| {key} | {value} |" for key, value in fields.items())
    return f"""# Negative Fixture

| field | value |
| --- | --- |
{rows}
"""


def run_fixtures() -> dict:
    validator = load_validator()
    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        for fixture in FIXTURES:
            path = tmp / f"{fixture['name']}.md"
            write_text(path, render_request(fixture["fields"]))
            result = validator.validate_request(path)
            status_match = result["status"] == fixture["expected_status"]
            reason_match = result["reason"].startswith(fixture["expected_reason_prefix"])
            passed = status_match and reason_match
            results.append(
                {
                    "name": fixture["name"],
                    "actual_status": result["status"],
                    "actual_reason": result["reason"],
                    "expected_status": fixture["expected_status"],
                    "expected_reason_prefix": fixture["expected_reason_prefix"],
                    "status": "pass" if passed else "fail",
                }
            )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if all(item["status"] == "pass" for item in results) else "fail",
        "fixtures": results,
        "boundary": {
            "does_not_approve_summaries": True,
            "does_not_modify_okf_concepts": True,
            "uses_temporary_files_only": True,
        },
    }


def write_markdown(report: dict) -> None:
    rows = "\n".join(
        "| {name} | {expected_status} | {actual_status} | {actual_reason} | {status} |".format(
            name=item["name"],
            expected_status=item["expected_status"],
            actual_status=item["actual_status"],
            actual_reason=item["actual_reason"],
            status=item["status"],
        )
        for item in report["fixtures"]
    )
    content = f"""---
doc_id: GPCF-DOC-E9D4362ECF
title: OKF v0.1 Summary Approval Negative Fixtures
project: KDS
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md
source_path: docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Summary Approval Negative Fixtures

generated_at: {report["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {report["status"]} |
| fixtures | {len(report["fixtures"])} |
| json | `{rel(JSON_OUT)}` |

## Results

| fixture | expected_status | actual_status | actual_reason | status |
| --- | --- | --- | --- | --- |
{rows}

## Boundary

- These fixtures validate the approval-request gate only.
- They do not approve summaries.
- They do not modify OKF concepts.
- Temporary files are used only during validation.
"""
    write_text(MD_OUT, content)


def main() -> int:
    report = run_fixtures()
    write_text(JSON_OUT, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_markdown(report)
    print(
        "okf_summary_approval_negative_fixtures={status} fixtures={fixtures}".format(
            status=report["status"],
            fixtures=len(report["fixtures"]),
        )
    )
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
