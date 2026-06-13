#!/usr/bin/env python3
"""Apply a previously generated KDS development-space sync plan."""

from __future__ import annotations

import argparse
from pathlib import Path

from kds_runtime import (
    KdsClient,
    KdsClientError,
    PLAN_PATH,
    append_ledger,
    load_plan,
    parse_sync_register,
    remote_index,
    run_local,
    sha256_file,
    utc_now,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(PLAN_PATH))
    parser.add_argument("--confirm-development-space", action="store_true")
    parser.add_argument("--max-writes", type=int, default=25)
    args = parser.parse_args()

    if not args.confirm_development_space:
        print("kds_sync_apply=blocked")
        print("missing --confirm-development-space")
        return 1

    for command in (
        ["python3", "tools/kds-sync/validate_kds_token.py"],
        ["python3", "tools/kds-sync/check_document_pollution.py"],
        ["python3", "tools/kds-sync/kds_conflict_guard.py"],
        ["python3", "tools/kds-sync/kds_sync_plan.py", "--require-clean-plan"],
    ):
        code, output = run_local(command)
        if code != 0:
            print("kds_sync_apply=blocked")
            print(output)
            return 1

    plan = load_plan(Path(args.plan))
    if plan.get("status") != "ready":
        print("kds_sync_apply=blocked")
        print("plan status is not ready")
        return 1

    planned_writes = plan.get("create", []) + plan.get("update", [])
    if len(planned_writes) > args.max_writes:
        print("kds_sync_apply=blocked")
        print(f"planned writes {len(planned_writes)} exceed --max-writes {args.max_writes}")
        return 1

    records = {r.kds_path: r for r in parse_sync_register()}
    client = KdsClient()
    try:
        remote = remote_index(client.list_documents())
        applied = 0
        for item in plan.get("create", []):
            record = records[item["kds_path"]]
            content = record.source.read_text(encoding="utf-8")
            status, body = client.create_document(record, content)
            append_ledger({
                "timestamp": utc_now(),
                "actor": "opsx-full-cycle",
                "token_owner": "lujunxiang",
                "token_fingerprint": plan.get("token_fingerprint"),
                "kds_space": plan.get("kds_space"),
                "source_path": record.source_path,
                "kds_path": record.kds_path,
                "action": "write",
                "hash_before": "",
                "hash_after": sha256_file(record.source),
                "result": f"http_{status}",
                "remote_id": body.get("id") or body.get("document_id"),
                "rollback_hint": "archive or restore previous KDS version manually; automatic delete is forbidden",
            })
            applied += 1
        for item in plan.get("update", []):
            record = records[item["kds_path"]]
            content = record.source.read_text(encoding="utf-8")
            status, body = client.update_document(remote[record.kds_path], record, content)
            append_ledger({
                "timestamp": utc_now(),
                "actor": "opsx-full-cycle",
                "token_owner": "lujunxiang",
                "token_fingerprint": plan.get("token_fingerprint"),
                "kds_space": plan.get("kds_space"),
                "source_path": record.source_path,
                "kds_path": record.kds_path,
                "action": "edit",
                "hash_before": item.get("hash_before"),
                "hash_after": sha256_file(record.source),
                "result": f"http_{status}",
                "remote_id": body.get("id") or body.get("document_id"),
                "rollback_hint": "restore prior KDS document version using hash_before and remote version metadata",
            })
            applied += 1
    except (KdsClientError, KeyError) as exc:
        print("kds_sync_apply=blocked")
        print(str(exc))
        return 1

    print("kds_sync_apply=pass")
    print(f"applied={applied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
