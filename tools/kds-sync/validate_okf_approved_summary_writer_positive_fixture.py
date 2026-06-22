#!/usr/bin/env python3
"""Validate the positive dry-run path for the OKF approved summary writer."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRITER = ROOT / "tools/kds-sync/dry_run_okf_approved_summary_writer.py"
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-approved-summary-writer-positive-fixture-20260620.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-approved-summary-writer-positive-fixture-20260620.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_writer():
    spec = importlib.util.spec_from_file_location("okf_approved_summary_writer", WRITER)
    if spec is None or spec.loader is None:
        raise SystemExit("okf_approved_summary_writer_positive_fixture=fail reason=writer_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_ledger() -> str:
    return """# Fixture Ledger

| request_id | status | source_path | kds_path | summary_scope | owner_approval | sensitivity_review | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OKF-SUM-FIXTURE-001 | approved | `09-status/kds-okf-v01-full-implementation-plan.md` | `开发/91-治理与验收/09-status/kds-okf-v01-full-implementation-plan.md` | governance-purpose-only | lujunxiang 2026-06-20 | pass | Positive dry-run fixture only. |
"""


def fixture_request() -> str:
    return """# Fixture Request

| field | value |
| --- | --- |
| request_id | OKF-SUM-FIXTURE-001 |
| source_path | `09-status/kds-okf-v01-full-implementation-plan.md` |
| kds_path | `开发/91-治理与验收/09-status/kds-okf-v01-full-implementation-plan.md` |
| requested_summary_scope | governance-purpose-only |
| requested_policy | approved_summary |
| requested_by | fixture |
| current_status | pending_review |
| confirmer | lujunxiang |
| confirmation_date | 2026-06-20 |
| owner_approval | approved |
| sensitivity_review | pass |
| approved_summary_scope | governance-purpose-only |
"""


def main() -> int:
    writer = load_writer()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        ledger = tmp / "ledger.md"
        request_dir = tmp / "requests"
        request = request_dir / "okf-v01-summary-approval-request-OKF-SUM-FIXTURE-001.md"
        write_text(ledger, fixture_ledger())
        write_text(request, fixture_request())
        dry_run = writer.run_dry_run(ledger, request_dir)

    passed = dry_run["approved_rows"] == 1 and dry_run["would_write"] == 1 and not dry_run["blocked"]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if passed else "fail",
        "approved_rows": dry_run["approved_rows"],
        "would_write": dry_run["would_write"],
        "blocked": dry_run["blocked"],
        "boundary": {
            "uses_temporary_files_only": True,
            "does_not_modify_okf_concepts": True,
            "does_not_approve_real_summary": True,
        },
    }
    write_text(JSON_OUT, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    markdown = f"""---
doc_id: GPCF-DOC-62444E2231
title: OKF v0.1 Approved Summary Writer Positive Fixture
project: KDS
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-approved-summary-writer-positive-fixture-20260620.md
source_path: docs/harness/evidence/okf-v01-approved-summary-writer-positive-fixture-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Approved Summary Writer Positive Fixture

generated_at: {payload["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {payload["status"]} |
| approved_rows | {payload["approved_rows"]} |
| would_write | {payload["would_write"]} |
| blocked | {len(payload["blocked"])} |
| json | `{rel(JSON_OUT)}` |

## Boundary

- This fixture uses temporary files only.
- It proves the dry-run writer can identify a valid approved request.
- It does not approve any real summary.
- It does not modify OKF concepts.
"""
    write_text(MD_OUT, markdown)
    print(
        "okf_approved_summary_writer_positive_fixture={status} approved_rows={approved_rows} would_write={would_write}".format(
            status=payload["status"],
            approved_rows=payload["approved_rows"],
            would_write=payload["would_write"],
        )
    )
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
