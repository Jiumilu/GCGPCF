#!/usr/bin/env python3
"""校验 K5 资产复用报告与注册表一致（不重新扫描）。"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "runtime" / "asset-registry" / "registry.yaml"
REPORT = ROOT / "runtime" / "asset-registry" / "usage-report.yaml"


def main() -> int:
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    ids = {str(e.get("id")) for e in (reg.get("entries") or []) if e.get("id")}
    if not REPORT.exists():
        print("asset_reuse_report = fail")
        print("reason = usage-report.yaml missing (run measure_asset_reuse.py)")
        return 1
    rep = yaml.safe_load(REPORT.read_text(encoding="utf-8")) or {}
    entries = rep.get("entries") or []
    reported = {str(e.get("id")) for e in entries}
    missing = sorted(ids - reported)
    extra = sorted(reported - ids)
    errors = []
    if missing:
        errors.append(f"missing ids: {', '.join(missing)}")
    if extra:
        errors.append(f"unknown ids: {', '.join(extra)}")
    if len(entries) != len(ids):
        errors.append(f"entry count mismatch: report={len(entries)} registry={len(ids)}")
    for e in entries:
        for field in ("files_total", "projects_total", "cross_repo_files"):
            if not isinstance(e.get(field), int):
                errors.append(f"{e.get('id')}: {field} missing/int invalid")

    print(f"asset_reuse_report: registry={len(ids)} report={len(entries)} "
          f"cross_repo_entries={rep.get('entries_with_cross_repo_reuse', 0)} errors={len(errors)}")
    for err in errors:
        print(f"  FAIL {err}")
    if errors:
        return 1
    print("asset_reuse_report = pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
