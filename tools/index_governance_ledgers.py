#!/usr/bin/env python3
"""GPCF 台账索引器 v0.1（M1·D1.2·2026-10-14）

把 09-status/ 台账（Markdown 受控件）解析为结构化索引：
doc_id/标题/状态/版本/域/责任人/最近复核/同步方向/来源路径。

只读纪律：
- 不写任何治理数据（仅产物落 runtime/evidence/）；
- 无 frontmatter 或字段缺失如实记录（findings，不猜测填充）；
- 解析采用简易 key:value（frontmatter 为平面结构，不引入 yaml 依赖）。

用法：python3 tools/index_governance_ledgers.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_DIR = ROOT / "09-status"
OUT_DIR = ROOT / "runtime" / "evidence"

FIELDS = ("doc_id", "title", "project", "domain", "status", "version",
          "owner", "kds_space", "kds_path", "source_path",
          "sync_direction", "last_reviewed")


def parse_frontmatter(text: str) -> dict | None:
    """解析平面 frontmatter（--- 包围的 key: value 段）。"""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line or line.startswith((" ", "-", "#")):
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def mtime(p: Path) -> str:
    return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat()


def main() -> int:
    findings: list[dict] = []
    entries: list[dict] = []
    if not LEDGER_DIR.is_dir():
        print(f"[gpcf] 台账目录不存在：{LEDGER_DIR}")
        return 1

    for p in sorted(LEDGER_DIR.glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception as e:
            findings.append({"file": p.name, "finding": f"读取失败：{e}"})
            continue
        fm = parse_frontmatter(text)
        if fm is None:
            findings.append({"file": p.name, "finding": "无 frontmatter（如实标注）"})
            entries.append({"file": p.name, "has_frontmatter": False, "mtime": mtime(p)})
            continue
        missing = [f for f in ("doc_id", "title", "status") if not fm.get(f)]
        if missing:
            findings.append({"file": p.name, "finding": f"字段缺失：{','.join(missing)}"})
        entry = {"file": p.name, "has_frontmatter": True, "mtime": mtime(p)}
        entry.update({k: fm.get(k, "") for k in FIELDS})
        entries.append(entry)

    def agg(key: str) -> dict:
        out: dict[str, int] = {}
        for e in entries:
            v = e.get(key) or "(未标)"
            out[v] = out.get(v, 0) + 1
        return dict(sorted(out.items(), key=lambda kv: -kv[1]))

    out = {
        "schema": "gpcf-ledger-index/0.1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "source": "09-status/*.md",
        "count": len(entries),
        "by_status": agg("status"),
        "by_domain": agg("domain"),
        "by_sync_direction": agg("sync_direction"),
        "entries": entries,
        "findings": findings,
        "ok": len(findings) == 0,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUT_DIR / f"ledger-index-{datetime.now():%Y%m%d-%H%M}.json"
    outfile.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"[gpcf] ledger index → {outfile.relative_to(ROOT)}")
    print(f"[gpcf] count={out['count']} by_status={out['by_status']}")
    print(f"[gpcf] by_domain={out['by_domain']}")
    print(f"[gpcf] findings={len(findings)} ok={out['ok']}")
    for f in findings[:8]:
        print(f"  ! {f['file']}: {f['finding']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
