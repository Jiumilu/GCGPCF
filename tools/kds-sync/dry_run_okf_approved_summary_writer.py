#!/usr/bin/env python3
"""Dry-run writer for OKF approved summaries."""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/harness/evidence/okf-v01-summary-admission-ledger-20260620.md"
APPROVAL_VALIDATOR = ROOT / "tools/kds-sync/validate_okf_summary_approval_request.py"
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-approved-summary-writer-dry-run-20260620.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-approved-summary-writer-dry-run-20260620.md"


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


def parse_table(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    headers: list[str] = []
    for line in read_text(path).splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip().strip("`") for part in line.strip("|").split("|")]
        if not headers:
            headers = parts
            continue
        if all(part.startswith("---") or set(part) <= {":", "-"} for part in parts):
            continue
        if len(parts) != len(headers):
            continue
        rows.append(dict(zip(headers, parts)))
    return rows


def load_validator():
    spec = importlib.util.spec_from_file_location("okf_summary_approval_request", APPROVAL_VALIDATOR)
    if spec is None or spec.loader is None:
        raise SystemExit("okf_approved_summary_writer_dry_run=fail reason=validator_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request_path(request_id: str, request_dir: Path) -> Path:
    return request_dir / f"okf-v01-summary-approval-request-{request_id}.md"


def run_dry_run(ledger: Path, request_dir: Path) -> dict:
    validator = load_validator()
    ledger_rows = parse_table(ledger)
    approved_rows = [row for row in ledger_rows if row.get("status") == "approved"]
    candidates = []
    blocked = []
    for row in approved_rows:
        req_path = request_path(row.get("request_id", ""), request_dir)
        result = validator.validate_request(req_path)
        if result["status"] == "ready_for_ledger_update":
            candidates.append(
                {
                    "request_id": row.get("request_id", ""),
                    "source_path": row.get("source_path", ""),
                    "kds_path": row.get("kds_path", ""),
                    "summary_scope": row.get("summary_scope", ""),
                    "request_path": rel(req_path),
                }
            )
        else:
            blocked.append(
                {
                    "request_id": row.get("request_id", ""),
                    "request_path": rel(req_path) if req_path.exists() else req_path.as_posix(),
                    "reason": result["reason"],
                }
            )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "mode": "dry_run",
        "ledger_rows": len(ledger_rows),
        "approved_rows": len(approved_rows),
        "would_write": len(candidates),
        "blocked": blocked,
        "candidates": candidates,
        "boundary": {
            "does_not_modify_okf_concepts": True,
            "does_not_write_source_documents": True,
            "does_not_approve_summaries": True,
            "source_of_record": "KDS / Git controlled documents",
        },
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", default=str(LEDGER))
    parser.add_argument("--request-dir", default=str(ROOT / "docs/harness/evidence"))
    parser.add_argument("--json", default=str(JSON_OUT))
    parser.add_argument("--markdown", default=str(MD_OUT))
    args = parser.parse_args()

    ledger = Path(args.ledger)
    request_dir = Path(args.request_dir)
    json_out = Path(args.json)
    md_out = Path(args.markdown)
    payload = run_dry_run(ledger, request_dir)
    write_text(json_out, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    candidate_rows = "\n".join(
        f"| {item['request_id']} | `{item['source_path']}` | `{item['summary_scope']}` |"
        for item in payload["candidates"]
    )
    if not candidate_rows:
        candidate_rows = "| none | none | none |"
    blocked_rows = "\n".join(
        f"| {item['request_id']} | `{item['request_path']}` | {item['reason']} |" for item in payload["blocked"]
    )
    if not blocked_rows:
        blocked_rows = "| none | none | none |"
    markdown = f"""---
doc_id: GPCF-DOC-88076261D5
title: OKF v0.1 Approved Summary Writer Dry Run
project: KDS
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-approved-summary-writer-dry-run-20260620.md
source_path: docs/harness/evidence/okf-v01-approved-summary-writer-dry-run-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Approved Summary Writer Dry Run

generated_at: {payload["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {payload["status"]} |
| mode | {payload["mode"]} |
| ledger_rows | {payload["ledger_rows"]} |
| approved_rows | {payload["approved_rows"]} |
| would_write | {payload["would_write"]} |
| json | `{rel(json_out)}` |

## Would Write

| request_id | source_path | summary_scope |
| --- | --- | --- |
{candidate_rows}

## Blocked

| request_id | request_path | reason |
| --- | --- | --- |
{blocked_rows}

## Boundary

- Dry run only.
- No OKF concept is modified.
- No source document is modified.
- No summary is approved by this evidence.
- KDS/Git controlled documents remain the source of record.
"""
    write_text(md_out, markdown)
    print(
        "okf_approved_summary_writer_dry_run=pass "
        f"approved_rows={payload['approved_rows']} would_write={payload['would_write']} blocked={len(payload['blocked'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
