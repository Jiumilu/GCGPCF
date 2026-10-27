#!/usr/bin/env python3
"""Daily project-group status audit (PG-10).

Reads config/project-group-projects.yaml, runtime/queue.json and
features/active/*/feature.yaml, then emits a per-project audit plus an
anomaly list. Read-only: writes only the requested outputs.

Usage:
  python3 tools/kds-sync/daily_project_status_audit.py
  python3 tools/kds-sync/daily_project_status_audit.py --check
  python3 tools/kds-sync/daily_project_status_audit.py --date 20261022
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config/project-group-projects.yaml"
QUEUE = ROOT / "runtime/queue.json"
ACTIVE = ROOT / "features/active"
AUDIT_DIR = ROOT / "runtime/audit"

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
EVIDENCE_FIELDS = ("tests", "build", "screenshots", "api", "summary")
TZ = timezone(timedelta(hours=8))


def load_project_ids() -> list[str]:
    text = CONFIG.read_text(encoding="utf-8")
    ids: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- {id:"):
            ids.append(line.split("id:", 1)[1].split(",", 1)[0].strip())
    return ids


def load_queue() -> dict:
    return json.loads(QUEUE.read_text(encoding="utf-8")).get("queue", [])


def load_features() -> list[dict]:
    features = []
    for f in sorted(ACTIVE.glob("*/feature.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8")) if yaml else {}
        data = data or {}
        data["_path"] = str(f.relative_to(ROOT))
        features.append(data)
    return features


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def stale_days(dt, now):
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    return max(0, (now - dt).days)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if yaml is None:
        print("daily_project_status_audit = fail")
        print("reason = PyYAML not installed")
        return 1

    now = datetime.now(TZ)
    project_ids = load_project_ids()
    queue = load_queue()
    features = load_features()
    qmap = {str(item.get("id")): item for item in queue}

    per_project: dict[str, dict] = {}
    anomalies: list[dict] = []

    for pid in project_ids:
        per_project[pid] = {
            "project": pid,
            "active_features": 0,
            "blocked_features": 0,
            "max_priority": None,
            "stale_days_max": 0,
            "evidence_gaps": 0,
            "status_mismatch": 0,
            "features": [],
        }

    slug_to_id = {pid.lower(): pid for pid in project_ids}
    for f in features:
        pid_raw = str(f.get("project") or "")
        pid = slug_to_id.get(pid_raw.lower(), pid_raw)
        rec = per_project.setdefault(pid, {
            "project": pid, "active_features": 0, "blocked_features": 0,
            "max_priority": None, "stale_days_max": 0, "evidence_gaps": 0,
            "status_mismatch": 0, "features": [],
        })
        fid = str(f.get("id") or "")
        q = qmap.get(fid, {})
        qstatus = str(q.get("status") or "unknown")
        fstatus = str(f.get("status") or "unknown")
        priority = str(f.get("priority") or "")
        step = str((f.get("loop") or {}).get("current_step") or "")
        evidence = f.get("evidence") or {}
        gaps = [k for k in EVIDENCE_FIELDS if str(evidence.get(k) or "").lower() not in ("pass", "waived")]
        stale = stale_days(parse_dt(f.get("updated_at")), now)
        blockers = f.get("blockers") or []

        rec["active_features"] += 1
        if qstatus == "blocked" or fstatus == "blocked" or fstatus == "blocked":
            rec["blocked_features"] += 1
        if priority and (rec["max_priority"] is None or PRIORITY_ORDER.get(priority, 9) < PRIORITY_ORDER.get(rec["max_priority"], 9)):
            rec["max_priority"] = priority
        if stale is not None:
            rec["stale_days_max"] = max(rec["stale_days_max"], stale)
        rec["evidence_gaps"] += len(gaps)
        mismatch = qstatus not in ("unknown", "closed") and fstatus in ("blocked", "active") and qstatus == "blocked" and fstatus == "active"
        if mismatch:
            rec["status_mismatch"] += 1
        rec["features"].append({
            "id": fid, "name": f.get("name"), "priority": priority,
            "queue_status": qstatus, "feature_status": fstatus,
            "current_step": step, "stale_days": stale,
            "evidence_gaps": gaps, "blockers_count": len(blockers),
        })

        if len(blockers) > 0 and stale is not None and stale >= 30:
            anomalies.append({"type": "blocked_over_30d", "project": pid, "feature": fid, "stale_days": stale, "blockers": len(blockers)})
        if gaps:
            anomalies.append({"type": "evidence_gap", "project": pid, "feature": fid, "fields": gaps})
        if mismatch:
            anomalies.append({"type": "status_mismatch", "project": pid, "feature": fid, "queue_status": qstatus, "feature_status": fstatus})

    for pid, rec in per_project.items():
        if rec["active_features"] == 0:
            anomalies.append({"type": "no_active_feature", "project": pid})

    summary = {
        "date": args.date,
        "generated_at": now.isoformat(timespec="seconds"),
        "project_count": len(project_ids),
        "active_feature_count": len(features),
        "blocked_feature_count": sum(1 for f in features if str(f.get("status")) == "blocked"),
        "anomaly_count": len(anomalies),
        "projects": per_project,
        "anomalies": anomalies,
    }

    if args.check:
        print(f"daily_project_status_audit = pass")
        print(f"project_count = {summary['project_count']}")
        print(f"active_feature_count = {summary['active_feature_count']}")
        print(f"anomaly_count = {summary['anomaly_count']}")
        return 0

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    jsonl = AUDIT_DIR / f"daily-status-{args.date}.jsonl"
    md = AUDIT_DIR / f"daily-status-{args.date}.md"
    jsonl.write_text(json.dumps(summary, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "---",
        f"doc_id: GPCF-DOC-DAILY-STATUS-{args.date}",
        f"title: 项目群日巡检 {args.date}",
        "project: GPCF",
        "domain: governance",
        "status: draft",
        "owner: GPCF",
        f"last_reviewed: {args.date[:4]}-{args.date[4:6]}-{args.date[6:]}",
        "---",
        "",
        f"# 项目群日巡检 {args.date}",
        "",
        f"- 项目数：{summary['project_count']}",
        f"- 活跃 Feature：{summary['active_feature_count']}",
        f"- 异常：{summary['anomaly_count']}",
        "",
        "## 异常清单",
        "",
        "| 类型 | 项目 | Feature | 说明 |",
        "|---|---|---|---|",
    ]
    for a in anomalies[:200]:
        detail = a.get("stale_days") or a.get("fields") or a.get("queue_status") or ""
        lines.append(f"| {a['type']} | {a.get('project','')} | {a.get('feature','')} | {detail} |")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"daily_project_status_audit = pass")
    print(f"project_count = {summary['project_count']}")
    print(f"active_feature_count = {summary['active_feature_count']}")
    print(f"anomaly_count = {summary['anomaly_count']}")
    print(f"jsonl = {jsonl.relative_to(ROOT)}")
    print(f"markdown = {md.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
