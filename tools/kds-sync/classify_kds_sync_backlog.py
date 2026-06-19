#!/usr/bin/env python3
"""Classify KDS sync-plan backlog for controlled, no-blind-write execution."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PLAN = ROOT / ".kds/sync-plan.json"
DEFAULT_JSON = ROOT / "docs/harness/evidence/kds-phase10-backlog-triage-20260619.json"
DEFAULT_MD = ROOT / "docs/harness/evidence/kds-phase10-backlog-triage-20260619.md"


def classify(path: str) -> tuple[str, str, str]:
    if path in {
        "09-status/kds-development-space-sync-plan.md",
        "09-status/kds-readonly-probe-report.md",
        "09-status/globalcloud-document-health-report.md",
    }:
        return "self_refresh_control_surface", "hold_self_refresh", "dynamic generated governance report"
    if "kds-md-okf" in path or "odf-phase" in path or path.startswith(".okf/"):
        return "closure_related_governance", "directed_sync_candidate", "Phase 6-10 governance and OKF/ODF closure surface"
    if path.startswith("docs/harness/loops/") or "/loops/" in path:
        return "loop_evidence_backlog", "requires_batch_review", "high churn Loop evidence; batch by loop range"
    if path.startswith(".harness/runs/") or path.startswith(".harness/"):
        return "harness_archive_backlog", "requires_archive_batch_review", "archive evidence; sync only by archive batch"
    if path.endswith("/README.md") or path == "README.md":
        return "generated_readme_surface", "hold_until_self_refresh_stable", "generated directory index"
    if path.startswith("09-status/") or "register" in path:
        return "status_register_backlog", "directed_sync_candidate", "governance register or status document"
    if path.startswith("03-data-ai-knowledge/") or "/03-data-ai-knowledge/" in path:
        return "kds_knowledge_backlog", "requires_human_review", "knowledge or candidate source; no blind write"
    if path.startswith("01-architecture/") or "/01-architecture/" in path:
        return "architecture_backlog", "requires_architecture_batch_review", "cross-project architecture"
    if path.startswith("05-agent-team/") or "/05-agent-team/" in path:
        return "agent_team_backlog", "requires_owner_review", "agent-team planning surface"
    if path.startswith("08-evidence-samples/") or "/08-evidence-samples/" in path:
        return "evidence_sample_backlog", "requires_evidence_batch_review", "project evidence sample"
    if path.startswith("docs/harness/evidence/") or "/docs/harness/evidence/" in path:
        return "harness_evidence_backlog", "requires_evidence_batch_review", "harness evidence"
    return "other_backlog", "requires_manual_triage", "unclassified path"


def load_plan(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def classify_items(plan: dict) -> list[dict]:
    rows: list[dict] = []
    for action in ("create", "update"):
        for item in plan.get(action, []):
            source_path = str(item.get("source_path", ""))
            bucket, disposition, reason = classify(source_path)
            rows.append({
                "action": action,
                "source_path": source_path,
                "kds_path": item.get("kds_path"),
                "bucket": bucket,
                "disposition": disposition,
                "reason": reason,
            })
    for item in plan.get("self_refresh", []):
        rows.append({
            "action": "self_refresh",
            "source_path": item.get("source_path"),
            "kds_path": item.get("kds_path"),
            "bucket": "self_refresh_control_surface",
            "disposition": "hold_self_refresh",
            "reason": "self-refresh item excluded from normal create/update chasing",
        })
    return rows


def summarize(rows: list[dict]) -> dict:
    return {
        "by_action": dict(Counter(str(row["action"]) for row in rows)),
        "by_bucket": dict(Counter(str(row["bucket"]) for row in rows)),
        "by_disposition": dict(Counter(str(row["disposition"]) for row in rows)),
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")
    return "\n".join(lines)


def write_markdown(path: Path, payload: dict) -> None:
    summary = payload["summary"]
    samples = payload["items"][:40]
    lines = [
        "---",
        "doc_id: GPCF-DOC-PHASE10-BACKLOG-TRIAGE",
        "title: KDS Phase 10 Backlog Triage Report",
        "project: KDS",
        "related_projects: [GPCF, KDS, WAES, GFIS, GPC, Brain, XiaoC, XGD, XiaoG]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/kds-phase10-backlog-triage-20260619.md",
        "source_path: docs/harness/evidence/kds-phase10-backlog-triage-20260619.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-19",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# KDS Phase 10 Backlog Triage Report",
        "",
        f"generated_at: {payload['generated_at']}",
        "",
        "## Scope",
        "",
        "This report classifies the current KDS sync-plan backlog for controlled execution. It is not a KDS write operation and does not authorize global blind sync.",
        "",
        "## Sync Plan Snapshot",
        "",
        md_table(
            ["metric", "value"],
            [[key, str(value)] for key, value in payload["plan_snapshot"].items()],
        ),
        "",
        "## By Action",
        "",
        md_table(["action", "count"], [[key, str(value)] for key, value in summary["by_action"].items()]),
        "",
        "## By Bucket",
        "",
        md_table(["bucket", "count"], [[key, str(value)] for key, value in summary["by_bucket"].items()]),
        "",
        "## By Disposition",
        "",
        md_table(["disposition", "count"], [[key, str(value)] for key, value in summary["by_disposition"].items()]),
        "",
        "## No-Blind-Write Queue Policy",
        "",
        "- `directed_sync_candidate`: may be synced only by explicit `--source-path` after gates pass.",
        "- `hold_self_refresh` and `hold_until_self_refresh_stable`: do not chase with repeated writes; stabilize generation first.",
        "- `requires_*_review`: group into small batches with human or owner review before any KDS write.",
        "- `requires_manual_triage`: no write until classified.",
        "",
        "## Sample Queue Items",
        "",
        md_table(
            ["action", "bucket", "disposition", "source_path"],
            [[str(row["action"]), str(row["bucket"]), str(row["disposition"]), str(row["source_path"])] for row in samples],
        ),
        "",
        "## Boundaries",
        "",
        "- No global blind KDS sync.",
        "- No accepted/integrated status upgrade.",
        "- No production system, database, or external business API writes.",
        "- OKF remains a read-only navigation layer.",
        "- KDS sync evidence must come from `.kds/sync-ledger.jsonl` with `result=http_200`.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(DEFAULT_PLAN))
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args()

    plan_path = Path(args.plan)
    plan = load_plan(plan_path)
    rows = classify_items(plan)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "plan_path": str(plan_path.relative_to(ROOT) if plan_path.is_absolute() else plan_path),
        "plan_snapshot": {
            "status": plan.get("status"),
            "remote_documents": plan.get("remote_documents"),
            "create": len(plan.get("create", [])),
            "update": len(plan.get("update", [])),
            "skip": len(plan.get("skip", [])),
            "self_refresh": len(plan.get("self_refresh", [])),
            "conflicts": len(plan.get("conflicts", [])),
            "missing_local": len(plan.get("missing_local", [])),
        },
        "summary": summarize(rows),
        "items": rows,
    }
    write_json(Path(args.json_out), payload)
    write_markdown(Path(args.md_out), payload)
    if args.print_summary:
        print(json.dumps({"phase10_backlog_triage": "pass", **payload["plan_snapshot"], **payload["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
