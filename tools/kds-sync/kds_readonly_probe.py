#!/usr/bin/env python3
"""Read-only KDS development-space probe."""

from __future__ import annotations

import argparse
from pathlib import Path

from kds_runtime import (
    KdsClient,
    KdsClientError,
    PLAN_PATH,
    fingerprint,
    parse_sync_register,
    remote_index,
    run_local,
    utc_now,
    write_json,
)

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "09-status/kds-readonly-probe-report.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(REPORT))
    args = parser.parse_args()

    token_code, token_output = run_local(["python3", "tools/kds-sync/validate_kds_token.py"])
    if token_code != 0:
        print("kds_readonly_probe=blocked")
        print(token_output)
        return 1

    client = KdsClient()
    try:
        documents = client.list_documents()
    except KdsClientError as exc:
        print("kds_readonly_probe=blocked")
        print(str(exc))
        return 1

    records = parse_sync_register()
    remote = remote_index(documents)
    missing_remote = [r.kds_path for r in records if r.kds_path not in remote]
    matching_remote = [r.kds_path for r in records if r.kds_path in remote]

    payload = {
        "generated_at": utc_now(),
        "kds_space": client.space,
        "token_fingerprint": fingerprint(client.token),
        "register_records": len(records),
        "remote_documents": len(documents),
        "matching_remote": len(matching_remote),
        "missing_remote": missing_remote,
    }
    write_json(PLAN_PATH.with_name("readonly-probe.json"), payload)

    report = [
        "---",
        "doc_id: GPCF-DOC-KDS-READONLY-PROBE",
        "title: KDS Readonly Probe Report",
        "project: GPCF",
        "related_projects: [GPCF, KDS, WAES]",
        "domain: status",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/91-治理与验收/09-status/kds-readonly-probe-report.md",
        "source_path: 09-status/kds-readonly-probe-report.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-13",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# KDS Readonly Probe Report",
        "",
        f"generated_at: {payload['generated_at']}",
        f"kds_space: {client.space}",
        f"token_fingerprint: {payload['token_fingerprint']}",
        f"register_records: {len(records)}",
        f"remote_documents: {len(documents)}",
        f"matching_remote: {len(matching_remote)}",
        f"missing_remote: {len(missing_remote)}",
        "",
        "## Missing Remote Documents",
        "",
    ]
    report.extend(f"- `{item}`" for item in missing_remote[:200])
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("kds_readonly_probe=pass")
    print(f"report={output_path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
