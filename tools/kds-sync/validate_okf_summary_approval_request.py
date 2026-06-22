#!/usr/bin/env python3
"""Validate OKF summary approval request packages."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUESTS = [
    ROOT / "docs/harness/evidence/okf-v01-summary-approval-request-OKF-SUM-20260620-001.md",
]
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.md"


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


def parse_field_table(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in read_text(path).splitlines():
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


def validate_request(path: Path) -> dict[str, str]:
    if not path.exists():
        return {"path": rel(path), "status": "fail", "reason": "missing_request"}
    fields = parse_field_table(path)
    current_status = fields.get("current_status", "")
    if current_status != "pending_review":
        return {"path": rel(path), "status": "fail", "reason": f"unsupported_current_status:{current_status}"}
    required = [
        "request_id",
        "source_path",
        "kds_path",
        "requested_summary_scope",
        "current_status",
        "confirmer",
        "confirmation_date",
        "owner_approval",
        "sensitivity_review",
        "approved_summary_scope",
    ]
    missing = [field for field in required if field not in fields]
    if missing:
        return {"path": rel(path), "status": "fail", "reason": "missing_fields:" + ",".join(missing)}
    pending = [
        "confirmer",
        "confirmation_date",
        "owner_approval",
        "sensitivity_review",
        "approved_summary_scope",
    ]
    if all(fields.get(field) == "pending" for field in pending):
        return {"path": rel(path), "status": "pending_review", "reason": "awaiting_human_confirmation"}
    incomplete = [field for field in pending if fields.get(field) == "pending"]
    if incomplete:
        return {"path": rel(path), "status": "fail", "reason": "partial_confirmation:" + ",".join(incomplete)}
    if fields.get("sensitivity_review") != "pass":
        return {"path": rel(path), "status": "fail", "reason": "sensitivity_review_not_pass"}
    return {"path": rel(path), "status": "ready_for_ledger_update", "reason": "human_confirmation_complete"}


def main() -> int:
    results = [validate_request(path) for path in REQUESTS]
    failures = [item for item in results if item["status"] == "fail"]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if not failures else "fail",
        "requests": results,
        "boundary": {
            "does_not_approve_summaries": True,
            "does_not_modify_okf_concepts": True,
            "source_of_record": "KDS / Git controlled documents",
        },
    }
    write_text(JSON_OUT, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    rows = "\n".join(
        f"| `{item['path']}` | {item['status']} | {item['reason']} |" for item in results
    )
    markdown = f"""---
doc_id: GPCF-DOC-41C37C2200
title: OKF v0.1 Summary Approval Request Gate
project: KDS
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.md
source_path: docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Summary Approval Request Gate

generated_at: {payload["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {payload["status"]} |
| requests | {len(results)} |
| failures | {len(failures)} |
| json | `{rel(JSON_OUT)}` |

## Results

| request | status | reason |
| --- | --- | --- |
{rows}

## Boundary

- This gate validates approval request completeness only.
- It does not approve summaries.
- It does not modify OKF concepts.
- KDS/Git controlled documents remain the source of record.
"""
    write_text(MD_OUT, markdown)
    print(
        "okf_summary_approval_request_gate={status} requests={requests} failures={failures}".format(
            status=payload["status"],
            requests=len(results),
            failures=len(failures),
        )
    )
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
