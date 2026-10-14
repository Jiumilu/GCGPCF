#!/usr/bin/env python3
"""GPCF 治理数据面只读探针 v0.1（M1·D1.3·2026-10-14）

对八视图数据源执行只读探测：存在性/可读性/新鲜度 → 健康分级。
分级：ok（存在且非空）｜stale（动态数据超龄·默认 30 天）｜missing｜empty。
动态数据 = 应当持续更新的（queue/state/闭环运行记录）；
静态台账（09-status/okf/projects 等）= 只在 missing/empty 时报异常。

只读纪律：不写任何治理数据（仅产物落 runtime/evidence/）。

用法：python3 tools/probe_governance_state.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "runtime" / "evidence"
STALE_DAYS = 30  # 动态数据超龄阈值

# (id, 相对路径, 类型: file|dir, 是否动态)
TARGETS = [
    ("queue",        "runtime/queue.json",        "file", True),
    ("state",        "runtime/state.json",        "file", True),
    ("features_active", "features/active",        "dir",  True),
    ("features_done",   "features/done",          "dir",  False),
    ("loops",        "loops",                     "dir",  True),
    ("ledger_09status", "09-status",              "dir",  False),
    ("okf_policies", "okf",                       "dir",  False),
    ("openspec",     "openspec/changes",          "dir",  True),
    ("projects",     "projects",                  "dir",  False),
    ("state_matrix", "registry/project-state-matrix.yaml", "file", False),
    ("master_plan_register", "09-status/globalcloud-project-master-plan-control-register.md", "file", False),
    ("acceptance",   "07-acceptance",             "dir",  False),
    ("evidence_samples", "08-evidence-samples",   "dir",  False),
    ("harness_evidence", "docs/harness/evidence", "dir",  False),
    ("governance_tools", "tools/kds-sync",        "dir",  False),
]


def probe(path: Path, kind: str, dynamic: bool) -> dict:
    res: dict = {"path": str(path.relative_to(ROOT)), "kind": kind, "dynamic": dynamic}
    if not path.exists():
        res.update(health="missing", count=None, freshness_days=None)
        return res
    try:
        if kind == "file":
            res["count"] = 0 if path.stat().st_size == 0 else 1
        else:
            res["count"] = sum(1 for _ in path.iterdir())
        age_days = (datetime.now(timezone.utc)
                    - datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                    ).total_seconds() / 86400
        res["freshness_days"] = round(age_days, 1)
        if res["count"] == 0:
            res["health"] = "empty"
        elif dynamic and age_days > STALE_DAYS:
            res["health"] = "stale"
        else:
            res["health"] = "ok"
    except Exception as e:
        res.update(health="unreadable", error=str(e))
    return res


def main() -> int:
    checks = [probe(ROOT / rel, kind, dyn) for _, rel, kind, dyn in TARGETS]
    summary: dict[str, int] = {}
    for c in checks:
        summary[c["health"]] = summary.get(c["health"], 0) + 1

    out = {
        "schema": "gpcf-governance-probe/0.1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "stale_threshold_days": STALE_DAYS,
        "levels": "ok|stale|empty|missing|unreadable（如实分级，不假绿）",
        "checks": checks,
        "summary": summary,
        "ok": all(c["health"] == "ok" for c in checks),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUT_DIR / f"governance-probe-{datetime.now():%Y%m%d-%H%M}.json"
    outfile.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"[gpcf] governance probe → {outfile.relative_to(ROOT)}")
    print(f"[gpcf] summary={summary}")
    for c in checks:
        flag = "✓" if c["health"] == "ok" else "!"
        extra = f" count={c.get('count')}" if c.get("count") is not None else ""
        extra += f" age={c.get('freshness_days')}d" if c.get("freshness_days") is not None else ""
        print(f"  {flag} {c['path']}: {c['health']}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
