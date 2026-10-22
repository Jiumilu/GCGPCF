#!/usr/bin/env python3
"""VU 台账校验（PG-02 质量门禁）。

检查：必填字段、vu_id 唯一、项目在 project_scope、每项目 3–5 个 VU、
stage/weight/data_class 合法、同项目 scene 不重复。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "runtime" / "vu-ledger.yaml"

REQUIRED = ["vu_id", "project", "weight", "scene", "authority", "object",
            "source_of_record", "acceptor", "stage", "stage_evidence", "data_class", "inferred"]
STAGES = {"S0", "S1", "S2", "S3", "S4"}
DATA_CLASSES = {"none", "fixture", "dry_run", "poc", "synthetic", "real"}
WEIGHTS = {1, 2, 3, 4, 5, 6}
MIN_VUS, MAX_VUS = 3, 5


def fail(msg: str) -> int:
    print("vu_ledger = fail")
    print(f"reason = {msg}")
    return 1


def main() -> int:
    data = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}
    units = data.get("vu_units") or []
    scope = data.get("project_scope") or []
    if not units or not scope:
        return fail("vu_units / project_scope missing")
    project_ids = {p.get("id") for p in scope if isinstance(p, dict)}
    errors: list[str] = []

    ids = Counter(u.get("vu_id") for u in units)
    for vid, count in ids.items():
        if not vid:
            errors.append("vu_id missing")
        elif count > 1:
            errors.append(f"duplicate vu_id: {vid} x{count}")

    per_project = Counter(u.get("project") for u in units)
    for project, count in per_project.items():
        if project not in project_ids:
            errors.append(f"project not in scope: {project}")
        if not (MIN_VUS <= count <= MAX_VUS):
            errors.append(f"{project}: VU count {count} not in [{MIN_VUS},{MAX_VUS}]")

    scenes = Counter((u.get("project"), u.get("scene")) for u in units)
    for (project, scene), count in scenes.items():
        if count > 1:
            errors.append(f"duplicate scene in {project}: {scene} x{count}")

    for u in units:
        vid = u.get("vu_id")
        for field in REQUIRED:
            if field not in u or u.get(field) in (None, ""):
                errors.append(f"{vid}: missing {field}")
        if u.get("stage") not in STAGES:
            errors.append(f"{vid}: invalid stage {u.get('stage')}")
        if u.get("weight") not in WEIGHTS:
            errors.append(f"{vid}: invalid weight {u.get('weight')}")
        if u.get("data_class") not in DATA_CLASSES:
            errors.append(f"{vid}: invalid data_class {u.get('data_class')}")
        if u.get("inferred") is not True:
            errors.append(f"{vid}: inferred must be true (首版基线)")

    print(f"vu_ledger: units={len(units)} projects={len(per_project)} weights_sum={sum(u.get('weight', 0) for u in units)} errors={len(errors)}")
    for e in errors[:20]:
        print(f"  FAIL {e}")
    if errors:
        return 1
    print("vu_ledger = pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
