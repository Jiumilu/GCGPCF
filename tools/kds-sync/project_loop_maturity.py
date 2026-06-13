#!/usr/bin/env python3
"""Generate project document completeness and Loop maturity matrix."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
DOC_REGISTER = ROOT / "09-status/globalcloud-document-control-register.md"
OUTPUT = ROOT / "09-status/globalcloud-project-document-loop-maturity-matrix.md"

PROJECT_ORDER = [
    "GFIS",
    "GPC",
    "PVAOS",
    "WAES",
    "KDS",
    "Brain",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "GPCF",
]

PROJECT_FOLDERS = {
    "GFIS": "01-GFIS",
    "GPC": "02-GPC",
    "PVAOS": "03-PVAOS",
    "WAES": "04-WAES",
    "KDS": "05-KDS",
    "Brain": "06-Brain",
    "PKC": "07-PKC",
    "XiaoC": "08-XiaoC",
    "XGD": "09-XGD",
    "XiaoG": "10-XiaoG",
    "MMC": "11-MMC",
    "GPCF": "12-GPCF",
}

BASIC_DOCS = [
    ("manifest", "Manifest"),
    ("loop_state", "loop-state"),
    ("architecture", "项目主线/架构边界"),
    ("evidence", "evidence/证据目录"),
    ("acceptance", "验收/状态审计"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_table(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cols = [col.strip() for col in line.strip().strip("|").split("|")]
        if not cols or cols[0] in {"---", "#"} or set(cols[0]) == {"-"}:
            continue
        if all(set(col.replace(" ", "")) <= {"-"} for col in cols):
            continue
        rows.append(cols)
    return rows


def parse_project_status() -> dict[str, dict[str, str]]:
    rows = parse_table(read(STATUS_MATRIX))
    projects: dict[str, dict[str, str]] = {}
    for cols in rows:
        if len(cols) < 13 or not cols[0].isdigit():
            continue
        name = cols[1]
        code = cols[2]
        project = name.replace("GlobalCloud ", "").replace("GlobalCoud ", "")
        projects[project] = {
            "name": name,
            "code": code,
            "mainline": cols[3],
            "agent": cols[4],
            "manifest": cols[5],
            "loop_state": cols[6],
            "rounds": cols[7],
            "evidence_rate": cols[8],
            "status": cols[9],
            "blockers": cols[10],
            "harness": cols[11],
            "next": cols[12],
        }
    return projects


def parse_doc_counts() -> tuple[dict[str, int], dict[str, int]]:
    text = read(DOC_REGISTER)
    project_counts: dict[str, int] = {project: 0 for project in PROJECT_ORDER}
    kds_counts: dict[str, int] = {project: 0 for project in PROJECT_ORDER}
    in_stats = False
    for line in text.splitlines():
        if line.startswith("## 12 项目文档总量统计"):
            in_stats = True
            continue
        if in_stats and line.startswith("## "):
            break
        if not in_stats or not line.startswith("|"):
            continue
        cols = [col.strip() for col in line.strip().strip("|").split("|")]
        if len(cols) < 5 or cols[0] not in PROJECT_ORDER:
            continue
        try:
            project_counts[cols[0]] = int(cols[2])
            kds_counts[cols[0]] = int(cols[3])
        except ValueError:
            continue
    return project_counts, kds_counts


def evidence_sample_count(project: str) -> int:
    evidence_dir = ROOT / "08-evidence-samples" / project
    if not evidence_dir.exists():
        return 0
    return len([path for path in evidence_dir.rglob("*") if path.is_file()])


def has_project_signal(project: str, patterns: tuple[str, ...]) -> bool:
    text = read(DOC_REGISTER)
    project_lines = [
        line
        for line in text.splitlines()
        if f"| {project} |" in line or f"/{PROJECT_FOLDERS[project]}/" in line
    ]
    haystack = "\n".join(project_lines)
    return any(re.search(pattern, haystack, re.IGNORECASE) for pattern in patterns)


def basic_doc_flags(project: str, row: dict[str, str], doc_count: int) -> dict[str, bool]:
    manifest = row.get("manifest", "否") not in {"否", "-", ""}
    loop_state = row.get("loop_state", "否") not in {"否", "-", ""}
    architecture = doc_count > 0 or has_project_signal(project, (r"architecture", r"架构", r"主线", r"alignment"))
    evidence = evidence_sample_count(project) > 0 or has_project_signal(project, (r"evidence", r"证据", r"\.harness"))
    acceptance = has_project_signal(project, (r"acceptance", r"验收", r"status-audit", r"状态"))
    return {
        "manifest": manifest,
        "loop_state": loop_state,
        "architecture": architecture,
        "evidence": evidence,
        "acceptance": acceptance,
    }


def evidence_rate_value(value: str) -> int:
    match = re.search(r"(\d+)", value)
    return int(match.group(1)) if match else 0


def maturity(row: dict[str, str], flags: dict[str, bool]) -> tuple[str, str]:
    status = row.get("status", "not_started")
    rounds = int(row.get("rounds", "0") or 0)
    evidence_rate = evidence_rate_value(row.get("evidence_rate", "0%"))
    if status in {"accepted", "integrated"}:
        return "L5", "已通过验收或集成"
    if status in {"harness_review", "audit_ready"}:
        return "L4", "已进入审计/验收"
    if evidence_rate >= 80:
        return "L3", "证据接近可审计"
    if rounds > 0:
        return "L2", "已进入微循环"
    if flags["manifest"] or sum(flags.values()) >= 2 or status == "partial":
        return "L1", "已有基础但未 loop_ready"
    return "L0", "未进入 Loop"


def completeness_score(flags: dict[str, bool], doc_count: int, kds_count: int) -> int:
    score = sum(14 for ok in flags.values() if ok)
    score += min(doc_count, 10)
    score += 10 if kds_count > 0 else 0
    return min(score, 100)


def gap_text(flags: dict[str, bool], row: dict[str, str], doc_count: int) -> str:
    gaps = [label for key, label in BASIC_DOCS if not flags[key]]
    if doc_count == 0:
        gaps.insert(0, "项目级文档")
    blocker = row.get("blockers", "-")
    if blocker and blocker != "-":
        gaps.append(blocker)
    return "；".join(dict.fromkeys(gaps)) if gaps else "无重大缺口"


def yes_no(value: bool) -> str:
    return "是" if value else "否"


def build_report() -> str:
    status_rows = parse_project_status()
    doc_counts, kds_counts = parse_doc_counts()
    today = date.today().isoformat()
    lines = [
        "---",
        "doc_id: GPCF-DOC-PROJECT-LOOP-MATURITY",
        "title: GlobalCloud 项目文档完整度与 Loop 成熟度量化矩阵",
        "project: GPCF",
        "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]",
        "domain: status",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/91-治理与验收/09-status/globalcloud-project-document-loop-maturity-matrix.md",
        "source_path: 09-status/globalcloud-project-document-loop-maturity-matrix.md",
        "sync_direction: bidirectional",
        f"last_reviewed: {today}",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# GlobalCloud 项目文档完整度与 Loop 成熟度量化矩阵",
        "",
        f"日期：{today}",
        "",
        "用途：将 12 个项目的基本文档体系、Loop 覆盖情况和量化成熟度收口到同一张表，作为下一轮 Loop 初始化和补债顺序依据。",
        "",
        "## 评分规则",
        "",
        "| 指标 | 说明 | 分值 |",
        "|---|---|---:|",
        "| Manifest | 项目 Manifest 已建立或已有基础 | 14 |",
        "| loop-state | `docs/harness/loop-state.md` 或等价状态记录已建立 | 14 |",
        "| 项目主线/架构边界 | 有项目级主线、架构或边界文档 | 14 |",
        "| evidence/证据目录 | 有项目级 evidence 或样本输入 | 14 |",
        "| 验收/状态审计 | 有验收、状态审计或 Harness 证据 | 14 |",
        "| 项目文档数量 | 直接归属文档数，最多 10 分 | 10 |",
        "| KDS 空间落位 | KDS 项目空间已有镜像文档 | 10 |",
        "",
        "成熟度：L0 未进入 Loop；L1 有基础但未 loop_ready；L2 已进入微循环；L3 证据接近可审计；L4 已进入审计/验收；L5 已通过验收或集成。",
        "",
        "## 12 项目量化矩阵",
        "",
        "| 项目 | 代号 | 文档数 | KDS文档 | Manifest | loop-state | 架构边界 | evidence | 验收审计 | 完整度分 | Loop成熟度 | 当前状态 | 主要缺口 | 下一步 |",
        "|---|---|---:|---:|---|---|---|---|---|---:|---|---|---|---|",
    ]

    totals = {"score": 0, "l0": 0, "l1": 0, "l2plus": 0, "complete": 0}
    for project in PROJECT_ORDER:
        row = status_rows.get(project, {})
        doc_count = doc_counts.get(project, 0)
        kds_count = kds_counts.get(project, 0)
        flags = basic_doc_flags(project, row, doc_count)
        score = completeness_score(flags, doc_count, kds_count)
        level, level_note = maturity(row, flags)
        totals["score"] += score
        totals["complete"] += 1 if score >= 80 else 0
        totals["l0"] += 1 if level == "L0" else 0
        totals["l1"] += 1 if level == "L1" else 0
        totals["l2plus"] += 1 if level not in {"L0", "L1"} else 0
        code = row.get("code", "-")
        lines.append(
            "| "
            + " | ".join(
                [
                    project,
                    code,
                    str(doc_count),
                    str(kds_count),
                    yes_no(flags["manifest"]),
                    yes_no(flags["loop_state"]),
                    yes_no(flags["architecture"]),
                    yes_no(flags["evidence"]),
                    yes_no(flags["acceptance"]),
                    str(score),
                    f"{level}：{level_note}",
                    row.get("status", "not_started"),
                    gap_text(flags, row, doc_count),
                    row.get("next", "-"),
                ]
            )
            + " |"
        )

    avg_score = round(totals["score"] / len(PROJECT_ORDER), 1)
    lines.extend(
        [
            "",
            "## 总体判定",
            "",
            f"- 12 项目平均文档完整度：{avg_score}/100。",
            f"- 文档完整度 >=80 的项目数：{totals['complete']}/12。",
            f"- Loop 成熟度 L0 项目数：{totals['l0']}/12。",
            f"- Loop 成熟度 L1 项目数：{totals['l1']}/12。",
            f"- Loop 成熟度 L2 及以上项目数：{totals['l2plus']}/12。",
            "",
            "## 执行结论",
            "",
            "1. KDS 项目空间已经建立，但项目级基本文档体系尚未全量完善。",
            "2. Loop 机制已经在总控矩阵层覆盖 12 个项目，但项目仓级 loop-state 和 evidence 尚未全量落地。",
            "3. 当前量化体系已经具备可计算指标，下一步必须按本矩阵逐项目补齐，而不能只更新总控文档。",
            "",
            "## 下一轮补齐顺序",
            "",
            "1. GFIS：已完成 `GPCF-GF-LR-030` UAT 问题处置闭环和豁免复核规则，金融事实保持 L4 阻断，下一步建立签收证据接收后的审计准备规则。",
            "2. GPCF：继续补 command log、Git clean evidence 与 KDS TOKEN 上线同步门禁。",
            "3. MMC、KDS、Brain、PKC：作为试点项目补齐 Manifest、loop-state、evidence-index。",
            "4. XiaoC：从 partial 推进到 loop_ready，补齐测试、部署和模型路由证据。",
            "5. GPC、PVAOS、WAES、XGD、XiaoG：补 Manifest 和首轮输入，防止主线空转。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    OUTPUT.write_text(build_report(), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
