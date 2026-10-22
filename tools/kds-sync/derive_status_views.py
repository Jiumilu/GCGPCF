#!/usr/bin/env python3
"""按唯一状态事实源（feature.yaml）派生 queue.json / STATUS 视图，或做一致性检查。

P03（2026-10-22，老卢 Q2 裁定）：feature.yaml 是唯一可写源；queue.json 与项目 STATUS 是派生视图。
-   --check : 只读比对，列出派生视图与源不一致的条目（不一致即应阻断）
-   --write : 按源重算派生字段并写回（仅在静默窗口由治理属主执行）

用法：
    python3 tools/kds-sync/derive_status_views.py --check
    python3 tools/kds-sync/derive_status_views.py --write --only F-017,F-024
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

ROLE_BY_STEP = {
    "plan": "Planner",
    "implement": "Builder",
    "evaluate": "Evaluator",
    "repair": "Repair",
    "commit": "Recorder",
}
STEP_TO_QUEUE_STATUS = {
    "plan": "plan",
    "implement": "implement",
    "evaluate": "evaluated",
    "repair": "repair",
    "commit": "commit",
    "blocked": "blocked",
}


def load_feature(feature_dir: Path) -> dict:
    data = yaml.safe_load((feature_dir / "feature.yaml").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{feature_dir}/feature.yaml 不是 mapping")
    return data


def to_utc_epoch(value) -> float | None:
    """把 '2026-10-22T11:30:00+08:00' / '...Z' 归一到 epoch 秒，用于跨时区比较。"""
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def expected_from_feature(feature: dict) -> dict:
    """由 feature.yaml 计算派生视图应然的字段值。"""
    loop = feature.get("loop") or {}
    step = str(loop.get("current_step") or "").strip()
    status = str(feature.get("status") or "").strip()
    # P03 派生优先级（老卢 2026-10-22 裁定：在源侧补两个维度）
    #   governance_blocked(或 status=blocked) > dispatched=false(queued) > step 映射
    governance_blocked = bool(loop.get("governance_blocked")) or status == "blocked"
    dispatched = loop.get("dispatched", True)
    if status == "done":
        queue_status = "closed"
        role = ROLE_BY_STEP.get("commit", "Recorder")
    elif governance_blocked:
        queue_status = "blocked"
        role = ROLE_BY_STEP.get(step) or "Evaluator"
    elif not dispatched:
        queue_status = "queued"
        role = "Dispatcher"
    else:
        queue_status = STEP_TO_QUEUE_STATUS.get(step)
        role = ROLE_BY_STEP.get(step)
    return {
        "project": feature.get("project"),
        "priority": feature.get("priority"),
        "status": queue_status,
        "current_role": role,
        "updated_at": feature.get("updated_at"),
        "current_step": step,
    }


def iter_features() -> list[Path]:
    dirs: list[Path] = []
    for sub in ("active", "done"):
        base = ROOT / "features" / sub
        if base.is_dir():
            dirs.extend(sorted(p for p in base.iterdir() if p.is_dir()))
    return dirs


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="只读比对派生视图与源")
    mode.add_argument("--write", action="store_true", help="按源重算派生字段并写回")
    parser.add_argument("--only", default="", help="逗号分隔的 Feature ID，仅处理这些（如 F-017,F-024）")
    args = parser.parse_args()

    only = {x.strip() for x in args.only.split(",") if x.strip()}

    queue_path = ROOT / "runtime" / "queue.json"
    queue_doc = json.loads(queue_path.read_text(encoding="utf-8"))
    entries = {item.get("id"): item for item in queue_doc.get("queue", [])}

    mismatches: list[dict] = []
    unknown: list[str] = []
    changed = 0

    for feature_dir in iter_features():
        if not (feature_dir / "feature.yaml").exists():
            # 兼容正在迁移中的工作区目录（例如并发移动 done/active 的中间态）
            continue
        feature = load_feature(feature_dir)
        fid = str(feature.get("id") or "").strip()
        if not fid or (only and fid not in only):
            continue
        want = expected_from_feature(feature)
        entry = entries.get(fid)
        if entry is None:
            unknown.append(fid)
            continue
        diff = {}
        for key in ("project", "priority", "status", "current_role", "updated_at"):
            got, exp = entry.get(key), want[key]
            if key == "updated_at":
                if to_utc_epoch(got) != to_utc_epoch(exp):
                    diff[key] = {"queue": got, "expected": exp, "kind": "real_drift"}
            elif got != exp:
                diff[key] = {"queue": got, "expected": exp, "kind": "real_drift"}
        if not diff:
            continue
        mismatches.append({"feature": fid, "workspace": feature_dir.name, "diff": diff})
        if args.write:
            entry.update({key: want[key] for key in diff})
            changed += 1

    if args.write and changed:
        queue_path.write_text(
            json.dumps(queue_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    categories = {"real_drift": sum(1 for m in mismatches for d in m["diff"].values() if d.get("kind") == "real_drift")}
    result = {
        "gate": "status_source_of_truth",
        "categories": categories,
        "mode": "write" if args.write else "check",
        "source_of_truth": "features/*/*/feature.yaml",
        "derived": "runtime/queue.json",
        "checked_features": len(iter_features()),
        "mismatch_count": len(mismatches),
        "unknown_in_queue": unknown,
        "written": changed if args.write else 0,
        "mismatches": mismatches,
        "conflict_policy": "以 feature.yaml 为准；派生不一致应阻断，禁止人工改派生侧对齐",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.check:
        return 0 if not mismatches else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
