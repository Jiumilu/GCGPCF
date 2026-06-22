#!/usr/bin/env python3
"""Build evidence for the multi-bundle OKF collection."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-collection-gate-20260620.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-collection-gate-20260620.md"


def run(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    commands = {
        "kds_bundle": [sys.executable, "tools/kds-sync/validate_okf_bundle.py", "--bundle", ".okf/bundles/kds-v0.1"],
        "governance_bundle": [sys.executable, "tools/kds-sync/validate_okf_bundle.py", "--bundle", ".okf/bundles/governance-v0.1"],
        "architecture_bundle": [sys.executable, "tools/kds-sync/validate_okf_bundle.py", "--bundle", ".okf/bundles/architecture-v0.1"],
        "collection": [sys.executable, "tools/kds-sync/validate_okf_collection.py"],
        "relationship_graph": [sys.executable, "tools/kds-sync/build_okf_relationship_graph.py"],
        "consumption_benchmark": [sys.executable, "tools/kds-sync/benchmark_okf_consumption.py"],
        "summary_approval_request_gate": [sys.executable, "tools/kds-sync/validate_okf_summary_approval_request.py"],
        "summary_approval_negative_fixtures": [sys.executable, "tools/kds-sync/validate_okf_summary_approval_negative_fixtures.py"],
        "summary_approval_expiry_gate": [sys.executable, "tools/kds-sync/validate_okf_summary_approval_expiry.py"],
        "summary_admission_gate": [sys.executable, "tools/kds-sync/validate_okf_summary_admission_gate.py"],
        "approved_summary_writer_dry_run": [sys.executable, "tools/kds-sync/dry_run_okf_approved_summary_writer.py"],
        "approved_summary_writer_positive_fixture": [sys.executable, "tools/kds-sync/validate_okf_approved_summary_writer_positive_fixture.py"],
    }
    results = {}
    for name, command in commands.items():
        code, output = run(command)
        results[name] = {"exit_code": code, "output": output}
    status = "pass" if all(item["exit_code"] == 0 for item in results.values()) else "fail"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "results": results,
        "boundary": {
            "source_of_record": "KDS / Git controlled documents",
            "derivation_policy": "metadata_only_no_body_copy",
            "does_not_replace_kds": True,
            "does_not_upgrade_business_status": True,
        },
    }
    write_text(JSON_OUT, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    rows_list = []
    for name, item in results.items():
        escaped_output = item["output"].replace("|", "\\|")
        rows_list.append(f"| {name} | {item['exit_code']} | `{escaped_output}` |")
    rows = "\n".join(rows_list)
    markdown = f"""---
doc_id: GPCF-DOC-1DB6FC4926
title: OKF v0.1 Collection Gate Evidence
project: GPCF
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-collection-gate-20260620.md
source_path: docs/harness/evidence/okf-v01-collection-gate-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Collection Gate Evidence

generated_at: {payload["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {status} |
| bundles | 3 |
| policy | `metadata_only_no_body_copy` |
| source_of_record | `KDS / Git controlled documents` |
| relationship_graph | `docs/harness/evidence/okf-v01-relationship-graph-20260620.md` |
| consumption_benchmark | `docs/harness/evidence/okf-v01-consumption-benchmark-20260620.md` |
| summary_admission_gate | `docs/harness/evidence/okf-v01-summary-admission-gate-20260620.md` |
| summary_admission_ledger | `docs/harness/evidence/okf-v01-summary-admission-ledger-20260620.md` |
| summary_approval_request_gate | `docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.md` |
| summary_approval_negative_fixtures | `docs/harness/evidence/okf-v01-summary-approval-negative-fixtures-20260620.md` |
| summary_approval_expiry_gate | `docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md` |
| approved_summary_writer_dry_run | `docs/harness/evidence/okf-v01-approved-summary-writer-dry-run-20260620.md` |
| approved_summary_writer_positive_fixture | `docs/harness/evidence/okf-v01-approved-summary-writer-positive-fixture-20260620.md` |

## Results

| gate | exit_code | output |
| --- | ---: | --- |
{rows}

## Boundary

- OKF is a derived consumption and exchange layer.
- KDS / Git controlled documents remain source of record.
- This evidence does not upgrade business, acceptance or integration status.
"""
    write_text(MD_OUT, markdown)
    print(f"okf_collection_report={status} markdown={MD_OUT.relative_to(ROOT).as_posix()} json={JSON_OUT.relative_to(ROOT).as_posix()}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
