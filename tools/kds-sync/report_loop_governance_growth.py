#!/usr/bin/env python3
"""J3 观测器：loop 治理「暂停新增」规则的月度观测。

背景：`02-governance/loop/LOOP_GOVERNANCE_SLIMMING_AND_DELIVERY_RECOVERY.md`
冻结规则 1/2 规定「暂停新增 LOOP 治理文档 / 暂停新增非 P0 validator」，
但 2026-10-27 前该规则没有任何观测手段——只能靠人自觉，等于口号。
本脚本把该规则变成可复跑的月度计数（J3）。

设计要点（为什么是两个指标而不是一个）：
- 规则原文是「暂停**新增**文档」。用「净增行数」当判据是假判据：
  2026-08 实测新增篇数 0、净增行数 +888（改名同步、翻译补行都会推高它），
  即「文档没新增，但行数涨了」——用行数判「新增」会误判。
- 因此：J3-a（新增篇数）作判据；J3-b（净增行数）只作体量膨胀的**观测指标**，
  不得作为「暂停新增」的判据，退出条件另立。

口径（只读，不改仓）：
- 范围 A（文档）：`02-governance/loop/` 下 `*.md`（含子目录）。
- 范围 B（校验器）：`tools/kds-sync/` 下 `*.py`，对应冻结规则 2。
- 月度归属：按**提交日期**（`%ad`, --date=short）落到自然月，不按文件 mtime。
- added/deleted = 当月新增/删除篇数（name-status A/D）。
- net_lines = 当月新增行 - 当月删除行（numstat），仅作观测。
- end_count = 该月末最后一次提交时该范围的篇数。

判定：
- J3-a 生效 = 最近 2 个**完整**自然月（不含进行中的当前月）added == 0。
- 当前月不参与判定：半个月的数字不足以判「生效」。

用法：
    python3 tools/kds-sync/report_loop_governance_growth.py            # 人读表
    python3 tools/kds-sync/report_loop_governance_growth.py --json     # 机器读
    python3 tools/kds-sync/report_loop_governance_growth.py --strict   # J3-a 未生效时 exit 1
    python3 tools/kds-sync/report_loop_governance_growth.py --months 6 # 展示近 6 个月
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCOPE_DOCS = "02-governance/loop/"
SCOPE_TOOLS = "tools/kds-sync/"


def git(*args: str) -> str:
    out = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if out.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} 失败: {out.stderr.strip()}")
    return out.stdout


def month_of(yyyy_mm_dd: str) -> str:
    return yyyy_mm_dd[:7]


def months_range(n: int) -> list[str]:
    today = date.today()
    out, y, m = [], today.year, today.month
    for _ in range(n):
        out.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return sorted(out)


def scan(scope: str, suffix: str) -> dict:
    """返回给定范围按月的 added/deleted 篇数与 numstat 增删行。"""
    added = defaultdict(int)
    deleted = defaultdict(int)
    lines_add = defaultdict(int)
    lines_del = defaultdict(int)

    cur = None
    for line in git(
        "log", "--name-status", "--date=short", "--format=__C__%ad", "--", scope
    ).splitlines():
        if line.startswith("__C__"):
            cur = month_of(line[5:].strip())
            continue
        if not cur or "\t" not in line:
            continue
        st, path = line.split("\t", 1)
        if not path.endswith(suffix):
            continue
        if st.startswith("A"):
            added[cur] += 1
        elif st.startswith("D"):
            deleted[cur] += 1

    cur = None
    for line in git(
        "log", "--numstat", "--date=short", "--format=__C__%ad", "--", scope
    ).splitlines():
        if line.startswith("__C__"):
            cur = month_of(line[5:].strip())
            continue
        parts = line.split("\t")
        if len(parts) != 3 or not parts[2].endswith(suffix):
            continue
        a, d, _p = parts
        if a.isdigit():
            lines_add[cur] += int(a)
        if d.isdigit():
            lines_del[cur] += int(d)

    end_count = {}
    for mon in sorted(set(list(added) + list(deleted) + list(lines_add))):
        y, m = int(mon[:4]), int(mon[5:7])
        nxt = f"{y + (m // 12):04d}-{(m % 12) + 1:02d}-01"
        sha = git("rev-list", "-1", f"--before={nxt}", "HEAD").strip()
        if not sha:
            continue
        files = git("ls-tree", "-r", "--name-only", sha, "--", scope)
        end_count[mon] = sum(1 for f in files.splitlines() if f.endswith(suffix))
    return {
        "added": dict(added),
        "deleted": dict(deleted),
        "lines_add": dict(lines_add),
        "lines_del": dict(lines_del),
        "end_count": end_count,
    }


def rows_for(data: dict, months: list[str], today_month: str) -> list[dict]:
    rows = []
    for mon in months:
        net = data["lines_add"].get(mon, 0) - data["lines_del"].get(mon, 0)
        rows.append(
            {
                "month": mon,
                "added_files": data["added"].get(mon, 0),
                "deleted_files": data["deleted"].get(mon, 0),
                "net_files": data["added"].get(mon, 0) - data["deleted"].get(mon, 0),
                "net_lines": net,
                "end_count": data["end_count"].get(mon),
                "in_progress": mon == today_month,
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="J3 观测器：loop 治理产物月度净增")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="J3-a 未生效时返回 1")
    ap.add_argument("--months", type=int, default=6, help="展示最近几个月（默认 6）")
    args = ap.parse_args()

    months = months_range(max(args.months, 2))
    today_month = date.today().strftime("%Y-%m")
    complete = [m for m in months if m < today_month]
    window = complete[-2:]

    docs = scan(SCOPE_DOCS, ".md")
    tools = scan(SCOPE_TOOLS, ".py")
    doc_rows = rows_for(docs, months, today_month)
    tool_rows = rows_for(tools, months, today_month)

    j3a_ok = bool(window) and all(docs["added"].get(m, 0) == 0 for m in window)
    body_ok = bool(window) and all(
        (docs["lines_add"].get(m, 0) - docs["lines_del"].get(m, 0)) <= 0 for m in window
    )
    rule2_ok = bool(window) and all(tools["added"].get(m, 0) == 0 for m in window)

    result = {
        "scope_docs": SCOPE_DOCS,
        "scope_tools": SCOPE_TOOLS,
        "judged_months": window,
        "J3a_pause_new_docs": {
            "criterion": "连续 2 个完整自然月 added_files == 0",
            "observed": j3a_ok,
        },
        "J3b_body_growth": {
            "criterion": "参考观测，不作「暂停新增」判据",
            "net_lines_le_0": body_ok,
            "why_not_a_criterion": (
                "2026-08 实测 added_files=0 而 net_lines=+888："
                "改名同步/翻译补行同样推高行数，用行数判「新增」是假判据"
            ),
        },
        "rule2_pause_new_validators": {
            "criterion": "连续 2 个完整自然月新增 .py == 0",
            "observed": rule2_ok,
        },
        "rows_docs": doc_rows,
        "rows_tools": tool_rows,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        def table(title: str, rows: list[dict], unit: str) -> None:
            print(title)
            print("-" * 80)
            print("%-9s %8s %8s %8s %9s %9s" % ("月份", "新增" + unit, "删除" + unit,
                                                "净增" + unit, "净增行", "月末存量"))
            for r in rows:
                end = "" if r["end_count"] is None else str(r["end_count"])
                flag = "  ← 进行中（不参与判定）" if r["in_progress"] else ""
                print("%-9s %8d %8d %8d %9d %9s%s" % (
                    r["month"], r["added_files"], r["deleted_files"],
                    r["net_files"], r["net_lines"], end, flag))
            print()

        print("J3 观测：loop 治理「暂停新增」规则（只读，按提交日期归月）")
        print("=" * 80)
        table("A. 文档范围 %s —— 冻结规则 1" % SCOPE_DOCS, doc_rows, "篇")
        table("B. 校验器范围 %s —— 冻结规则 2" % SCOPE_TOOLS, tool_rows, "个")
        print("-" * 80)
        print("判定月份（最近两个完整自然月）：%s" % (", ".join(window) or "(不足 2 个月)"))
        print("J3-a 暂停新增文档：%s（判据：连续 2 个完整月 added_files == 0）"
              % ("已生效" if j3a_ok else "未生效"))
        print("J3-b 体量净增（仅观测，非判据）：%s"
              % ("近两月净增 <= 0" if body_ok else "近两月净增 > 0（含改名/翻译同步等非新增改动）"))
        print("    不拿行数判「新增」的理由：%s" % result["J3b_body_growth"]["why_not_a_criterion"])
        print("冻结规则 2 暂停新增校验器：%s（判据：连续 2 个完整月新增 .py == 0）"
              % ("已生效" if rule2_ok else "未生效"))
        print("当前月为进行中月份，不参与判定——半个月的数字不足以判「生效」。")

    if args.strict and not j3a_ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
