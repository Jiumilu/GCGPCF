#!/usr/bin/env python3
"""K5 复用度量 v2：统计资产注册表条目在 GPCF 与兄弟项目仓中的引用。

单次 ripgrep 扫描（所有 asset id 一次匹配），再按文件计数；输出 usage-report.yaml。
只读扫描，不修改任何资产正文。
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT.parent
REGISTRY = ROOT / "runtime" / "asset-registry" / "registry.yaml"
OUT = ROOT / "runtime" / "asset-registry" / "usage-report.yaml"


def main() -> int:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    entries = [e for e in (data.get("entries") or []) if e.get("id")]
    ids = [str(e["id"]) for e in entries]
    pattern = "|".join(re.escape(i) for i in ids)
    cmd = [
        "rg", "-l", "-e", pattern, "--no-messages", "--max-filesize", "2M",
        "-g", "*.md", "-g", "*.yaml", "-g", "*.yml", "-g", "*.json",
        "-g", "*.py", "-g", "*.ts", "-g", "*.tsx",
        "-g", "!**/node_modules/**", "-g", "!**/.git/**", "-g", "!**/dist/**",
        "-g", "!**/build/**", "-g", "!**/.kds/**", "-g", "!**/.venv/**",
        "-g", "!**/coverage/**", "-g", "!**/__pycache__/**",
        "-g", "!**/runtime/asset-registry/**",
        str(WORKSPACE),
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"asset_reuse: scan failed: {exc}")
        return 1
    matched = [Path(p) for p in res.stdout.splitlines() if p.strip()]

    stats = {i: {"files": 0, "projects": set(), "gcpf_files": 0, "cross": set()} for i in ids}
    for path in matched:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            rel = path.relative_to(WORKSPACE)
        except (OSError, ValueError):
            continue
        project = rel.parts[0] if rel.parts else ""
        for i in ids:
            if i in text:
                stats[i]["files"] += 1
                stats[i]["projects"].add(project)
                if project == "GlobalCloud GPCF":
                    stats[i]["gcpf_files"] += 1
                else:
                    stats[i]["cross"].add(project)

    report = []
    for entry in entries:
        i = str(entry["id"])
        st = stats[i]
        report.append({
            "id": i,
            "type": entry.get("type"),
            "owner": entry.get("owner"),
            "reused_by_declared": len(entry.get("reused_by") or []),
            "files_total": st["files"],
            "projects_total": len(st["projects"]),
            "gcpf_files": st["gcpf_files"],
            "cross_repo_files": st["files"] - st["gcpf_files"],
            "cross_repo_projects": sorted(st["cross"]),
        })

    out = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "source_registry": "runtime/asset-registry/registry.yaml",
        "entries_total": len(entries),
        "entries_with_cross_repo_reuse": sum(1 for e in report if e["cross_repo_files"] > 0),
        "entries": report,
    }
    OUT.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"asset_reuse: entries={len(entries)} matched_files={len(matched)} "
          f"cross_repo_entries={out['entries_with_cross_repo_reuse']}")
    print("asset_reuse = pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
