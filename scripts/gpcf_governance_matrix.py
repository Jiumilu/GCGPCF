#!/usr/bin/env python3
"""29 仓治理覆盖矩阵（方案继承 / 本地门禁委托 / CI 远端生效），可重复生成。

用法：
    python3 scripts/gpcf_governance_matrix.py            # Markdown 表格 + 统计
    python3 scripts/gpcf_governance_matrix.py --json     # 机器可读

只读：不修改任何仓；不入门禁（仅作体检与派单依据）。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECT_GROUP = ROOT.parent
REGISTRY = ROOT / "config" / "project-group-projects.yaml"
TOKEN = "GPCF:01-architecture/GlobalCloud 项目群总体方案.md"
SECTIONS = [
    "项目定位", "与项目群主方案的继承关系", "项目群版本基线", "本项目权威职责",
    "本项目不承担的职责", "核心交付物", "与其他项目的接口关系", "技术架构现状和目标架构",
    "测试、交付和运行命令", "LOOP 接入", "风险、依赖、回滚和非声明边界",
]
DELEG_TOKENS = [
    "Delegate project-group loop gate execution to the GPCF canonical gate",
    "GPCF_PROJECT_GROUP_GATE_DELEGATED",
]


def inheritance(repo: Path) -> str:
    cands = sorted([f for f in repo.glob("*总体方案.md") if f.is_file()])
    if not cands:
        return "无文件"
    text = cands[0].read_text(encoding="utf-8", errors="ignore")
    nsec = sum(1 for s in SECTIONS if s in text)
    if TOKEN in text and nsec == len(SECTIONS):
        return "合规"
    if nsec >= 1 or TOKEN in text:
        return "部分"
    return "不合规"


def gate(repo: Path, project_id: str) -> str:
    f = repo / "tools/kds-sync/loop_document_gate.py"
    if not f.is_file():
        return "无"
    text = f.read_text(encoding="utf-8", errors="ignore")
    if project_id == "GPCF":
        return "正本"
    return "委托" if all(t in text for t in DELEG_TOKENS) else "自实现/缺"


def ci_map() -> dict:
    out = subprocess.run([sys.executable, str(ROOT / "tools/kds-sync/scan_ci_coverage.py")],
                         capture_output=True, text=True, cwd=ROOT)
    try:
        return {r["repo"]: r for r in json.loads(out.stdout)["rows"]}
    except Exception:
        return {}


def build_rows() -> list[dict]:
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    cis = ci_map()
    rows = []
    for p in reg["projects"]:
        repo = PROJECT_GROUP / p["repo"]
        c = cis.get(p["repo"], {})
        rows.append({
            "project": p["id"], "repo": p["repo"],
            "inheritance": inheritance(repo), "gate": gate(repo, p["id"]),
            "standards": bool(c.get("standards")),
            "test_remote": bool(c.get("remote_test")),
            "build_remote": bool(c.get("remote_build")),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rows = build_rows()
    stats = {
        "repos": len(rows),
        "inheritance": {k: sum(1 for r in rows if r["inheritance"] == k)
                        for k in ("合规", "部分", "不合规", "无文件")},
        "gate": {k: sum(1 for r in rows if r["gate"] == k) for k in ("委托", "正本", "无", "自实现/缺")},
        "standards": sum(r["standards"] for r in rows),
        "test_remote": sum(r["test_remote"] for r in rows),
        "build_remote": sum(r["build_remote"] for r in rows),
    }
    if args.json:
        print(json.dumps({"summary": stats, "rows": rows}, ensure_ascii=False, indent=1))
        return 0
    print("| 项目 | 总体方案继承 | 本地门禁 | standards | test(远端) | build(远端) |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['project']} | {r['inheritance']} | {r['gate']} | "
              f"{'✓' if r['standards'] else '—'} | {'✓' if r['test_remote'] else '—'} | "
              f"{'✓' if r['build_remote'] else '—'} |")
    print(f"\n继承: {stats['inheritance']}")
    print(f"门禁: {stats['gate']}")
    print(f"CI 远端: standards {stats['standards']}/{stats['repos']} · "
          f"test {stats['test_remote']}/{stats['repos']} · build {stats['build_remote']}/{stats['repos']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
