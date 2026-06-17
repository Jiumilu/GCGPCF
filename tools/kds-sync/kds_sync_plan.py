#!/usr/bin/env python3
"""Generate a dry-run plan for real KDS development-space synchronization."""

from __future__ import annotations

import argparse
from pathlib import Path

from kds_runtime import (
    ALLOWED_SYNC_STATUSES,
    KdsClient,
    KdsClientError,
    PLAN_PATH,
    SKIPPED_SYNC_STATUSES,
    fingerprint,
    parse_sync_register,
    remote_hash,
    remote_index,
    run_local,
    sha256_file,
    utc_now,
    write_json,
)

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "09-status/kds-development-space-sync-plan.md"
SELF_REFRESH_SOURCE_PATHS = {
    "09-status/kds-development-space-sync-plan.md",
    "09-status/kds-readonly-probe-report.md",
}


def build_plan(require_remote: bool) -> tuple[int, dict]:
    control_code, control_output = run_local(["python3", "tools/kds-sync/document_control.py"])
    if control_code != 0:
        return 1, {"status": "blocked", "reason": control_output}

    token_code, token_output = run_local(["python3", "tools/kds-sync/validate_kds_token.py"])
    if token_code != 0:
        return 1, {"status": "blocked", "reason": token_output}

    conflict_code, conflict_output = run_local(["python3", "tools/kds-sync/kds_conflict_guard.py"])
    if conflict_code != 0:
        return 1, {"status": "blocked", "reason": conflict_output}

    client = KdsClient()
    try:
        documents = client.list_documents()
    except KdsClientError as exc:
        if require_remote:
            return 1, {"status": "blocked", "reason": str(exc)}
        documents = []
    remote = remote_index(documents)

    create: list[dict] = []
    update: list[dict] = []
    skip: list[dict] = []
    self_refresh: list[dict] = []
    conflicts: list[dict] = []
    missing_local: list[dict] = []

    for record in parse_sync_register():
        if not record.source.exists():
            missing_local.append({"source_path": record.source_path, "kds_path": record.kds_path})
            continue
        if record.source_path in SELF_REFRESH_SOURCE_PATHS:
            self_refresh.append({
                "source_path": record.source_path,
                "kds_path": record.kds_path,
                "status": "self_refresh",
            })
            continue
        status = record.status
        if status in SKIPPED_SYNC_STATUSES or status not in ALLOWED_SYNC_STATUSES:
            skip.append({"source_path": record.source_path, "kds_path": record.kds_path, "status": status})
            continue
        local_hash = sha256_file(record.source)
        remote_doc = remote.get(record.kds_path)
        if not remote_doc:
            create.append({
                "doc_id": record.doc_id,
                "source_path": record.source_path,
                "kds_path": record.kds_path,
                "hash_after": local_hash,
            })
            continue
        before_hash = remote_hash(remote_doc)
        if before_hash and before_hash != local_hash:
            update.append({
                "doc_id": record.doc_id,
                "source_path": record.source_path,
                "kds_path": record.kds_path,
                "hash_before": before_hash,
                "hash_after": local_hash,
                "remote_version": remote_doc.get("version"),
                "remote_etag": remote_doc.get("etag"),
            })
        elif not before_hash:
            conflicts.append({
                "doc_id": record.doc_id,
                "source_path": record.source_path,
                "kds_path": record.kds_path,
                "reason": "remote hash unavailable; cannot prove conflict-free update",
            })

    plan = {
        "generated_at": utc_now(),
        "status": "blocked" if conflicts or missing_local else "ready",
        "kds_space": client.space,
        "token_fingerprint": fingerprint(client.token),
        "remote_documents": len(documents),
        "create": create,
        "update": update,
        "skip": skip,
        "self_refresh": self_refresh,
        "conflicts": conflicts,
        "missing_local": missing_local,
    }
    return (0 if plan["status"] == "ready" else 1), plan


def write_report(plan: dict, path: Path) -> None:
    lines = [
        "---",
        "doc_id: GPCF-DOC-KDS-SYNC-PLAN",
        "title: KDS Development Space Sync Plan",
        "project: GPCF",
        "related_projects: [GPCF, KDS, WAES]",
        "domain: status",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/91-治理与验收/09-status/kds-development-space-sync-plan.md",
        "source_path: 09-status/kds-development-space-sync-plan.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-13",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# KDS Development Space Sync Plan",
        "",
        f"generated_at: {plan.get('generated_at', '')}",
        f"status: {plan.get('status', '')}",
        f"kds_space: {plan.get('kds_space', '')}",
        f"token_fingerprint: {plan.get('token_fingerprint', '')}",
        f"remote_documents: {plan.get('remote_documents', 0)}",
        "",
    ]
    for key in ("create", "update", "conflicts", "missing_local", "self_refresh", "skip"):
        rows = plan.get(key, [])
        lines.extend([f"## {key}", "", f"count: {len(rows)}", ""])
        for item in rows[:200]:
            lines.append(f"- `{item.get('source_path', item.get('kds_path', ''))}` -> `{item.get('kds_path', '')}`")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def mirror_report_if_registered(path: Path) -> None:
    report = path.resolve()
    for record in parse_sync_register():
        if record.source.resolve() == report:
            mirror = record.local_mirror
            mirror.parent.mkdir(parents=True, exist_ok=True)
            mirror.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-clean-plan", action="store_true")
    parser.add_argument("--allow-unconfigured-remote", action="store_true")
    parser.add_argument("--output", default=str(PLAN_PATH))
    parser.add_argument("--report", default=str(REPORT))
    args = parser.parse_args()

    code, plan = build_plan(require_remote=not args.allow_unconfigured_remote)
    output = Path(args.output)
    report = Path(args.report)
    write_json(output, plan)
    write_report(plan, report)
    mirror_report_if_registered(report)
    if args.require_clean_plan and plan.get("status") != "ready":
        print("kds_sync_plan=blocked")
        print(plan.get("reason") or f"conflicts={len(plan.get('conflicts', []))}")
        return 1
    print("kds_sync_plan=" + ("pass" if code == 0 else "blocked"))
    print(f"plan={output.relative_to(ROOT).as_posix()}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
