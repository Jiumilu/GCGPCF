#!/usr/bin/env python3
"""Validate OKF summary approval request expiry rules."""

from __future__ import annotations

import json
import re
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUESTS = [
    ROOT / "docs/harness/evidence/okf-v01-summary-approval-request-OKF-SUM-20260620-001.md",
]
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md"
AS_OF = date(2026, 6, 21)
MAX_PENDING_DAYS = 14


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_field_table(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip().strip("`") for part in line.strip("|").split("|")]
        if len(parts) != 2:
            continue
        key, value = parts
        if key in {"field", "---"} or key.startswith("---"):
            continue
        fields[key] = value
    return fields


def parse_request_date(text: str, fields: dict[str, str]) -> date | None:
    if "request_date" in fields:
        return date.fromisoformat(fields["request_date"])
    match = re.search(r"日期：(\d{4}-\d{2}-\d{2})", text)
    if match:
        return date.fromisoformat(match.group(1))
    return None


def validate_request(path: Path, *, as_of: date = AS_OF) -> dict[str, str | int]:
    if not path.exists():
        return {"path": rel(path), "status": "fail", "reason": "missing_request", "age_days": -1}
    text = read_text(path)
    fields = parse_field_table(text)
    request_date = parse_request_date(text, fields)
    if request_date is None:
        return {"path": rel(path), "status": "fail", "reason": "missing_request_date", "age_days": -1}
    age_days = (as_of - request_date).days
    if age_days < 0:
        return {"path": rel(path), "status": "fail", "reason": "request_date_in_future", "age_days": age_days}
    if fields.get("current_status") != "pending_review":
        return {
            "path": rel(path),
            "status": "fail",
            "reason": "unsupported_current_status:" + fields.get("current_status", ""),
            "age_days": age_days,
        }
    if age_days > MAX_PENDING_DAYS:
        return {"path": rel(path), "status": "expired_blocked", "reason": "pending_request_expired", "age_days": age_days}
    return {"path": rel(path), "status": "active_pending", "reason": "within_pending_review_window", "age_days": age_days}


def render_fixture(request_date: str) -> str:
    return f"""# Expiry Fixture

日期：{request_date}

| field | value |
| --- | --- |
| request_id | EXP-001 |
| source_path | 09-status/kds-okf-v01-full-implementation-plan.md |
| kds_path | 开发/91-治理与验收/09-status/kds-okf-v01-full-implementation-plan.md |
| requested_summary_scope | governance-purpose-only |
| current_status | pending_review |
| confirmer | pending |
| confirmation_date | pending |
| owner_approval | pending |
| sensitivity_review | pending |
| approved_summary_scope | pending |
"""


def run_expired_fixture() -> dict[str, str | int]:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "expired-request.md"
        write_text(path, render_fixture("2026-05-30"))
        result = validate_request(path)
    passed = result["status"] == "expired_blocked" and result["reason"] == "pending_request_expired"
    return {
        "name": "expired_pending_request",
        "expected_status": "expired_blocked",
        "actual_status": str(result["status"]),
        "actual_reason": str(result["reason"]),
        "age_days": int(result["age_days"]),
        "status": "pass" if passed else "fail",
    }


def main() -> int:
    requests = [validate_request(path) for path in REQUESTS]
    fixture = run_expired_fixture()
    request_failures = [item for item in requests if item["status"] in {"fail", "expired_blocked"}]
    status = "pass" if not request_failures and fixture["status"] == "pass" else "fail"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "as_of": AS_OF.isoformat(),
        "max_pending_days": MAX_PENDING_DAYS,
        "requests": requests,
        "fixtures": [fixture],
        "boundary": {
            "does_not_approve_summaries": True,
            "does_not_modify_okf_concepts": True,
            "expired_pending_requests_are_blocked": True,
        },
    }
    write_text(JSON_OUT, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    request_rows = "\n".join(
        "| `{path}` | {status} | {age_days} | {reason} |".format(**item) for item in requests
    )
    fixture_rows = (
        "| {name} | {expected_status} | {actual_status} | {age_days} | {actual_reason} | {status} |".format(
            **fixture
        )
    )
    markdown = f"""---
doc_id: GPCF-DOC-82F7D65D59
title: OKF v0.1 Summary Approval Expiry Gate
project: KDS
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md
source_path: docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# OKF v0.1 Summary Approval Expiry Gate

generated_at: {payload["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {status} |
| as_of | {AS_OF.isoformat()} |
| max_pending_days | {MAX_PENDING_DAYS} |
| requests | {len(requests)} |
| json | `{rel(JSON_OUT)}` |

## Requests

| request | status | age_days | reason |
| --- | --- | ---: | --- |
{request_rows}

## Fixtures

| fixture | expected_status | actual_status | age_days | actual_reason | status |
| --- | --- | --- | ---: | --- | --- |
{fixture_rows}

## Boundary

- This gate validates pending approval request freshness only.
- It does not approve summaries.
- It does not modify OKF concepts.
- Expired pending requests must be recreated or explicitly re-confirmed before ledger update.
"""
    write_text(MD_OUT, markdown)
    print(
        "okf_summary_approval_expiry_gate={status} requests={requests} expired_real_requests={expired} fixtures=1".format(
            status=status,
            requests=len(requests),
            expired=len(request_failures),
        )
    )
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
