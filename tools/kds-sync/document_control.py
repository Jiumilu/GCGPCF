#!/usr/bin/env python3
"""GlobalCloud document control and KDS development-space sync.

This script is intentionally deterministic: document IDs derive from source
paths, generated registers are sorted, and KDS mirror files preserve the
repository path under a controlled project/domain folder.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = date.today().isoformat()

PROJECTS = {
    "GFIS": ("01-GFIS", ["GFIS", "工厂", "厂行", "Edge"]),
    "GPC": ("02-GPC", ["GPC", "绿色供应链公共服务平台", "供应链", "平台订单", "链同"]),
    "PVAOS": ("03-PVAOS", ["PVAOS", "门户", "租户", "伙伴", "组织"]),
    "WAES": ("04-WAES", ["WAES", "宪衡", "治理", "证据", "审计", "状态", "验收"]),
    "KDS": ("05-KDS", ["KDS", "知识主存", "知源", "Knowledge"]),
    "Brain": ("06-Brain", ["Brain", "LLM Wiki", "知识引擎", "GCBrain", "gbrain"]),
    "PKC": ("07-PKC", ["PKC", "个人知识"]),
    "XiaoC": ("08-XiaoC", ["XiaoC", "小即", "蚁后", "灵策"]),
    "XGD": ("09-XGD", ["XGD", "大象", "Hermes", "评证"]),
    "XiaoG": ("10-XiaoG", ["XiaoG", "ESP32", "语音"]),
    "MMC": ("11-MMC", ["MMC", "管理配置", "模板基线"]),
    "GPCF": ("12-GPCF", ["GPCF", "GlobalCoud GPCF", "项目群", "总控"]),
    "Studio": ("13-Studio", ["Studio", "GlobalCloud Studio", "Hermes", "Agent 工作台"]),
}

WAS_ONTOLOGY_GOVERNANCE_DOCS = {
    "docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.md",
    "docs/harness/evidence/was-real-source-record-monitor-100-20260623.md",
    "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001.md",
    "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-100.md",
}

WAS_ONTOLOGY_PROJECT_GROUP = [
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
    "Studio",
    "WAS",
]

PROJECT_GROUP_REAL_EXECUTION_CORE_DOCS = {
    "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-ready-for-review-advancement-queue-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-execution-command-pack-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-pre-execution-environment-readiness-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-authorization-request-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-authorization-receipt-ledger-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-human-confirmation-request-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-authorization-routing-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-package-20260627.md",
    "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-objective-coverage-audit-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-governance-progress-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-completion-gap-matrix-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-receipt-pre-execution-bridge-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-execution-receipt-pre-execution-bridge-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-authorization-to-pre-execution-total-bridge-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-ready-for-review-trigger-map-20260627.md",
    "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md",
    "02-governance/loop/LOOP_DELIVERY_EFFICIENCY_CONTROL.md",
    "09-status/gpcf-project-status-matrix.md",
    "09-status/globalcloud-document-health-report.md",
    "09-status/globalcloud-project-group-real-execution-governance-board.md",
    "02-governance/loop/LOOP_CONTROL_BOARD.md",
    "09-status/project-group-master-plan-governance-status-report.md",
    "02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md",
    "09-status/globalcloud-project-implementation-control-register.md",
}

PROJECT_GROUP_FULL_SCOPE = [
    "AAAS",
    "Brain",
    "WAS",
    "XiaoC",
    "WAES",
    "GPC",
    "Studio",
    "GPCF",
    "XWAIL",
    "GFIS",
    "MMC",
    "KDS",
    "XiaoG",
    "PVAOS",
    "SOP",
    "PKC",
    "XGD",
]

DOMAIN_BY_TOP = {
    "00-index": "index",
    "01-architecture": "architecture",
    "02-governance": "governance",
    "03-data-ai-knowledge": "data-ai-knowledge",
    "04-ui-delivery": "ui-delivery",
    "05-agent-team": "agent-team",
    "06-workstreams": "workstreams",
    "07-acceptance": "acceptance",
    "08-evidence-samples": "evidence",
    "09-status": "status",
    "10-archive": "archive",
    "docs": "docs",
    "openspec": "openspec",
    "templates": "templates",
    ".harness": "harness-evidence",
    ".codex": "operational-skill",
    "tools": "tools",
}

README_META = {
    "00-index": ("索引与入口", "集中保存项目群总索引、阅读入口和口径基线。"),
    "01-architecture": ("架构方案", "保存项目群架构、系统边界、主线矩阵、实施路线和关键架构决策。"),
    "02-governance": ("治理规范", "保存状态门控、证据治理、实施准入、工具使用、成本控制和全过程交付规范。"),
    "03-data-ai-knowledge": ("数据、AI 与知识", "保存对象目录、事件合同、连接器合同、KDS/Brain 分层、模型授权和数据治理文档。"),
    "04-ui-delivery": ("界面与交付体验", "保存 P0 界面闭环、统一体验骨架、组件库、样板页和交互验收文档。"),
    "05-agent-team": ("智能体团队", "保存小即团队、专项责任、执行台账、周报、缺口清单和实施前验证文档。"),
    "06-workstreams": ("专项工作流", "保存各专项会话状态、验证包、执行记录和只读预检结论。"),
    "07-acceptance": ("验收矩阵", "保存一期验收矩阵、验收场景、证据要求和完成判定。"),
    "08-evidence-samples": ("证据样本", "保存运行前样本、证据链样本、审批阻断样本和历史会话归档。"),
    "09-status": ("状态与控制台账", "保存项目状态矩阵、项目主线矩阵、文档控制清单和 KDS 同步台账。"),
    "10-archive": ("过期与历史归档", "保存过期、被替代、历史会话和旧来源导入文档。"),
    "docs": ("工程说明", "保存工程手册、Harness 说明和 KDS/Brain 相关开发资料。"),
    "openspec": ("OpenSpec 变更", "保存规格变更、任务、设计和能力规格草案。"),
    "templates": ("模板库", "保存循环审计、证据索引、loop-state 和执行记录模板。"),
    ".harness": ("Harness 运行证据", "保存 Harness 运行过程、状态审计、任务和验收矩阵。"),
}

GENERIC_DIR_PURPOSE = {
    "10-archive/deprecated": ("过期文档归档", "保存已过期、不再建议引用但仍需保留审计线索的文档。"),
    "10-archive/superseded": ("被替代文档归档", "保存已被新版本替代的文档。"),
    "10-archive/historical-sessions": ("历史会话归档", "保存历史会话、过程记录和人工确认上下文。"),
    "10-archive/imported-legacy": ("旧来源导入归档", "保存旧来源或外部导入的历史文档。"),
    "docs/harness": ("Harness 工程说明", "保存 Harness 验收、状态审计、多租户权限和证据说明。"),
    "docs/harness/evidence": ("Harness 证据说明", "保存 Harness evidence 目录说明与证据约定。"),
    "openspec/changes": ("OpenSpec 变更集", "保存 OpenSpec 变更提案、设计、任务和规格增量。"),
    "openspec/specs": ("OpenSpec 主规格", "保存 OpenSpec 主规格目录。"),
    "tools": ("工具目录", "保存文档治理、同步和辅助脚本。"),
    "tools/kds-sync": ("KDS 同步工具", "保存文档控制与 KDS 开发空间同步脚本。"),
    ".codex": ("Codex 本地配置", "保存本地技能和 Codex 工作配置，按运行类文档受控。"),
    ".codex/skills": ("Codex 本地技能", "保存本地技能目录，技能正文不直接加受控元数据。"),
    ".codex/skills/ui-ux-pro-max": ("UI/UX 技能", "保存 UI/UX Pro Max 技能定义，按运行类文档登记和镜像。"),
    ".harness/runs": ("Harness 运行记录", "保存 Harness 每次运行的审计、验收、任务和提案记录。"),
}

EXCLUDE_DIRS = {".git", ".kds"}
NO_FRONTMATTER_FILES = {".codex/skills/ui-ux-pro-max/SKILL.md"}
GENERATED_REGISTERS = {
    "09-status/globalcloud-document-control-register.md",
    "09-status/kds-development-space-sync-register.md",
    "09-status/document-deprecation-register.md",
}
PROJECT_GROUP_IMPLEMENTATION_PLAN = "GlobalCloud 项目群实施方案.md"

SCOPE_ENV = "DOCUMENT_CONTROL_SCOPE"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_markdown() -> list[Path]:
    docs: list[Path] = []
    for path in ROOT.rglob("*.md"):
        parts = set(path.relative_to(ROOT).parts)
        if parts & EXCLUDE_DIRS:
            continue
        docs.append(path)
    return sorted(docs, key=rel)


def doc_id(source_path: str) -> str:
    digest = hashlib.sha1(source_path.encode("utf-8")).hexdigest()[:10].upper()
    return f"GPCF-DOC-{digest}"


def controlled_doc_id(source_path: str, existing_frontmatter: dict[str, str]) -> str:
    existing_doc_id = existing_frontmatter.get("doc_id", "").strip()
    if existing_doc_id:
        return existing_doc_id
    return doc_id(source_path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def title_for(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def top_dir(source_path: str) -> str:
    return source_path.split("/", 1)[0]


def domain_for(source_path: str) -> str:
    if source_path in WAS_ONTOLOGY_GOVERNANCE_DOCS:
        return "ontology-governance"
    if source_path == PROJECT_GROUP_IMPLEMENTATION_PLAN:
        return "architecture"
    if source_path.startswith(".okf/"):
        return "governance"
    return DOMAIN_BY_TOP.get(top_dir(source_path), "general")


def status_for(source_path: str) -> str:
    if source_path.startswith("10-archive/"):
        return "archive"
    if "session-archives/" in source_path or source_path.startswith(".harness/"):
        return "archive"
    if "template" in source_path.lower() or "模板" in source_path:
        return "controlled"
    if source_path.startswith("openspec/changes/"):
        return "draft"
    if source_path.startswith(".codex/"):
        return "operational_controlled"
    return "controlled"


def frontmatter_managed_for(source_path: str) -> bool:
    if source_path.startswith(".okf/bundles/"):
        return False
    if source_path.startswith((".codex/", ".agents/")):
        return False
    if source_path in NO_FRONTMATTER_FILES:
        return False
    if source_path.startswith(".codex/skills/") and source_path.endswith("/SKILL.md"):
        return False
    return True


def project_for(source_path: str, title: str, text: str) -> tuple[str, list[str]]:
    if source_path in WAS_ONTOLOGY_GOVERNANCE_DOCS:
        primary = "GPCF" if source_path.startswith("docs/harness/loops/") else "KDS"
        return primary, WAS_ONTOLOGY_PROJECT_GROUP
    if source_path == PROJECT_GROUP_IMPLEMENTATION_PLAN:
        return "GPCF", PROJECT_GROUP_FULL_SCOPE
    if source_path in PROJECT_GROUP_REAL_EXECUTION_CORE_DOCS:
        if source_path.startswith("02-governance/loop/"):
            return "WAES", PROJECT_GROUP_FULL_SCOPE
        if source_path.startswith("02-governance/"):
            return "WAES", PROJECT_GROUP_FULL_SCOPE
        if source_path.startswith("09-status/"):
            return "GPCF", PROJECT_GROUP_FULL_SCOPE
        haystack = f"{source_path}\n{title}\n{text[:5000]}"
        hits: list[str] = []
        for project, (_, keys) in PROJECTS.items():
            if any(key in haystack for key in keys):
                hits.append(project)
        primary = hits[0] if hits else "GPCF"
        return primary, PROJECT_GROUP_FULL_SCOPE
    if source_path in {
        "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md",
        "02-governance/loop/LOOP_CAPABILITY_REGISTRY.md",
    }:
        return "WAES", ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
    if source_path.startswith(".okf/"):
        return "GPCF", ["GPCF", "GPC", "WAES", "KDS"]
    haystack = f"{source_path}\n{title}\n{text[:5000]}"
    hits: list[str] = []
    for project, (_, keys) in PROJECTS.items():
        if any(key in haystack for key in keys):
            hits.append(project)
    if not hits:
        hits = ["GPCF"]
    evidence_project = None
    if source_path.startswith("08-evidence-samples/"):
        parts = source_path.split("/")
        if len(parts) > 1 and parts[1] in PROJECTS:
            evidence_project = parts[1]
    harness_project = None
    if source_path.startswith("docs/harness/"):
        parts = source_path.split("/")
        if len(parts) > 2 and parts[2] in PROJECTS:
            harness_project = parts[2]

    if evidence_project:
        primary = evidence_project
    elif harness_project:
        primary = harness_project
    elif source_path == "README.md" or source_path.startswith(("00-index/", "tools/", "templates/", ".codex/")):
        primary = "GPCF"
    elif source_path.startswith("01-architecture/") or source_path.startswith("09-status/"):
        primary = "GPCF"
    elif source_path.startswith("02-governance/"):
        primary = "WAES" if "WAES" in hits or "治理" in haystack or "证据" in haystack else "GPCF"
    elif source_path.startswith("03-data-ai-knowledge/"):
        primary = "KDS" if "KDS" in hits or "知识" in haystack else "GPCF"
    elif source_path.startswith("04-ui-delivery/"):
        primary = "GPC" if "GPC" in hits else "GPCF"
    elif source_path.startswith("05-agent-team/") or source_path.startswith("06-workstreams/"):
        primary = "XiaoC" if "XiaoC" in hits or "小即" in haystack else "GPCF"
    elif source_path.startswith("07-acceptance/") or source_path.startswith("08-evidence-samples/") or source_path.startswith(".harness/"):
        primary = "WAES"
    elif source_path.startswith("docs/harness/evidence/gckf-p0-") and "current-state" in source_path:
        primary = "GPCF"
    elif source_path.startswith(("docs/harness/loop-state.md", "docs/harness/loops/", "docs/harness/evidence/evidence-index.md")):
        primary = "GPCF"
    elif source_path.startswith("docs/") or source_path.startswith("openspec/"):
        primary = "KDS" if ("KDS" in hits or "Brain" in hits) else "GPCF"
    else:
        primary = hits[0]
    related = sorted(set(hits), key=list(PROJECTS.keys()).index)
    if primary not in related:
        related.insert(0, primary)
    return primary, related


def kds_path_for(source_path: str, project: str, status: str, domain: str) -> str:
    if source_path == PROJECT_GROUP_IMPLEMENTATION_PLAN:
        return "开发/12-GPCF/GlobalCloud 项目群实施方案.md"
    if source_path.startswith(".okf/"):
        return f"开发/12-GPCF/{source_path}"
    if source_path.startswith("08-evidence-samples/GFIS/docs/"):
        return "开发/01-GFIS/docs/" + source_path.rsplit("/", 1)[-1]
    if source_path == "README.md":
        return "开发/00-项目群总控/README.md"
    if status in {"deprecated", "superseded", "archive"}:
        base = "99-过期文档" if status != "archive" else "92-证据与会话归档"
    elif domain in {"architecture", "data-ai-knowledge"} and project == "GPCF":
        base = "90-跨项目架构"
    elif domain in {"governance", "acceptance", "status"}:
        base = "91-治理与验收"
    elif project in PROJECTS:
        base = PROJECTS[project][0]
    else:
        base = "00-项目群总控"
    return f"开发/{base}/{source_path}"


def metadata_block(record: dict[str, object]) -> str:
    keys = [
        "doc_id",
        "title",
        "project",
        "related_projects",
        "domain",
        "status",
        "version",
        "owner",
        "kds_space",
        "kds_path",
        "source_path",
        "sync_direction",
        "last_reviewed",
        "supersedes",
        "superseded_by",
    ]
    lines = ["---"]
    for key in keys:
        value = record[key]
        if isinstance(value, list):
            rendered = "[" + ", ".join(str(v) for v in value) + "]"
        else:
            rendered = str(value).replace('"', '\\"')
            rendered = f'"{rendered}"' if any(ch in rendered for ch in [":", "#", "[", "]"]) else rendered
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def strip_existing_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    parsed: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip().strip('"')
    return parsed, body.lstrip("\n")


def build_records(paths: list[Path]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in paths:
        source_path = rel(path)
        text = read_text(path)
        existing, body = strip_existing_frontmatter(text)
        title = title_for(path, body)
        project, related = project_for(source_path, title, body)
        domain = domain_for(source_path)
        status = status_for(source_path)
        record = {
            "doc_id": controlled_doc_id(source_path, existing),
            "title": title,
            "project": project,
            "related_projects": related,
            "domain": domain,
            "status": status,
            "version": "v1.0",
            "owner": project,
            "kds_space": "开发",
            "kds_path": kds_path_for(source_path, project, status, domain),
            "source_path": source_path,
            "sync_direction": "bidirectional" if status != "operational_controlled" else "register_and_mirror",
            "last_reviewed": existing.get("last_reviewed", TODAY),
            "supersedes": [],
            "superseded_by": [],
            "frontmatter_managed": frontmatter_managed_for(source_path),
        }
        records.append(record)
    return records


def apply_frontmatter(records: list[dict[str, object]]) -> None:
    for record in records:
        source_path = str(record["source_path"])
        if not record["frontmatter_managed"]:
            continue
        path = ROOT / source_path
        text = read_text(path)
        existing, body = strip_existing_frontmatter(text)
        # Preserve non-control frontmatter keys if they exist by leaving current
        # content alone only when an explicit external marker is present.
        if existing.get("doc_control") == "external":
            continue
        stripped_body = body.rstrip()
        if stripped_body:
            write_text(path, metadata_block(record) + stripped_body + "\n")
        else:
            write_text(path, metadata_block(record).rstrip() + "\n")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out.extend("| " + " | ".join(cell.replace("\n", " ") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def project_summary_rows(records: list[dict[str, object]]) -> list[list[str]]:
    rows: list[list[str]] = []
    for project, (folder, _) in PROJECTS.items():
        by_project = [r for r in records if str(r["project"]) == project]
        by_folder = [r for r in records if str(r["kds_path"]).startswith(f"开发/{folder}/")]
        rows.append([
            project,
            folder,
            str(len(by_project)),
            str(len(by_folder)),
            "已建空间" if by_folder else "已建空间，暂无直接镜像文档",
        ])
    return rows


def public_space_summary_rows(records: list[dict[str, object]]) -> list[list[str]]:
    public_spaces = [
        ("00-项目群总控", "项目群总入口与根 README"),
        ("90-跨项目架构", "跨项目架构、主线、数据/知识跨域文档"),
        ("91-治理与验收", "治理、验收、状态、台账与门禁文档"),
        ("92-证据与会话归档", "Harness、证据样本、历史会话与归档文档"),
        ("99-过期文档", "deprecated / superseded 文档"),
    ]
    rows: list[list[str]] = []
    for folder, meaning in public_spaces:
        count = sum(1 for r in records if str(r["kds_path"]).startswith(f"开发/{folder}/"))
        rows.append([folder, meaning, str(count)])
    return rows


def write_registers(records: list[dict[str, object]]) -> None:
    rows = []
    for r in records:
        rows.append([
            str(r["doc_id"]),
            str(r["title"]).replace("|", "\\|"),
            str(r["source_path"]),
            str(r["project"]),
            ", ".join(r["related_projects"]),
            str(r["domain"]),
            str(r["status"]),
            str(r["kds_path"]),
        ])
    content = "# GlobalCloud 文档控制总台账\n\n"
    content += f"日期：{TODAY}\n\n"
    content += "用途：登记 GPCF 仓库内所有 Markdown 文档的受控身份、项目归属、状态、源路径与 KDS 开发空间路径。\n\n"
    content += "## 12 项目文档总量统计\n\n"
    content += "说明：`project 字段文档数` 表示当前 GPCF 文档体系中直接归属到该项目的文档数；`KDS 项目空间文档数` 表示镜像落在 KDS `开发/{项目空间}` 下的文档数。跨项目架构、治理验收、证据归档等公共文档会进入公共空间，不一定落在单项目空间。\n\n"
    content += markdown_table(["project", "kds_project_folder", "project 字段文档数", "KDS 项目空间文档数", "说明"], project_summary_rows(records))
    content += "\n\n"
    content += "## KDS 公共空间文档统计\n\n"
    content += markdown_table(["kds_public_folder", "meaning", "document_count"], public_space_summary_rows(records))
    content += "\n\n"
    content += "## 全量文档清单\n\n"
    content += markdown_table(["doc_id", "title", "source_path", "project", "related_projects", "domain", "status", "kds_path"], rows)
    content += "\n"
    write_text(ROOT / "09-status/globalcloud-document-control-register.md", content)

    sync_rows = []
    for r in records:
        sync_rows.append([
            str(r["doc_id"]),
            str(r["source_path"]),
            str(r["kds_path"]),
            str(r["sync_direction"]),
            "pending_api" if str(r["kds_path"]).startswith("开发/") else "n/a",
        ])
    sync = "# KDS 开发空间同步台账\n\n"
    sync += f"日期：{TODAY}\n\n"
    sync += "用途：登记 Git 文档与 KDS `开发` 空间的双向同步映射。当前实现包含仓库内 `.kds/development-space/开发` 本地镜像与真实 KDS API 同步工具链；单文档 API 状态以 `kds_api_status` 和真实同步审计流水为准。\n\n"
    sync += "## 范围说明\n\n"
    sync += "当前台账覆盖的是 **GPCF 仓库中已经纳入 KDS `开发` 空间的文档镜像**。其它项目的真实项目仓库文档，只有在后续从对应项目仓导入或同步到本仓/KDS 后，才会出现在本台账中。\n\n"
    sync += "其它项目当前在 KDS 中的位置如下：`开发/01-GFIS`、`开发/02-GPC`、`开发/03-PVAOS`、`开发/04-WAES`、`开发/05-KDS`、`开发/06-Brain`、`开发/07-PKC`、`开发/08-XiaoC`、`开发/09-XGD`、`开发/10-XiaoG`、`开发/11-MMC`、`开发/12-GPCF`。跨项目文档主要在 `开发/90-跨项目架构`、`开发/91-治理与验收`、`开发/92-证据与会话归档`。\n\n"
    sync += "## 12 项目文档总量统计\n\n"
    sync += markdown_table(["project", "kds_project_folder", "project 字段文档数", "KDS 项目空间文档数", "说明"], project_summary_rows(records))
    sync += "\n\n"
    sync += "## KDS 公共空间文档统计\n\n"
    sync += markdown_table(["kds_public_folder", "meaning", "document_count"], public_space_summary_rows(records))
    sync += "\n\n"
    sync += "## 全量同步清单\n\n"
    sync += markdown_table(["doc_id", "git_source", "kds_path", "sync_direction", "kds_api_status"], sync_rows)
    sync += "\n"
    write_text(ROOT / "09-status/kds-development-space-sync-register.md", sync)

    dep_rows = []
    for r in records:
        if r["status"] in {"deprecated", "superseded", "archive", "operational_controlled"}:
            dep_rows.append([
                str(r["doc_id"]),
                str(r["title"]).replace("|", "\\|"),
                str(r["source_path"]),
                str(r["status"]),
                str(r["kds_path"]),
            ])
    dep = "# 文档过期与归档台账\n\n"
    dep += f"日期：{TODAY}\n\n"
    dep += "用途：登记历史、过期、被替代和运行类文档，避免误用为当前项目完成状态或当前业务口径。\n\n"
    dep += markdown_table(["doc_id", "title", "source_path", "status", "kds_path"], dep_rows)
    dep += "\n"
    write_text(ROOT / "09-status/document-deprecation-register.md", dep)


def readme_records_for(prefix: str, records: list[dict[str, object]]) -> list[dict[str, object]]:
    return [r for r in records if str(r["source_path"]).startswith(prefix + "/")]


def write_directory_readmes(records: list[dict[str, object]]) -> None:
    for dirname, (label, purpose) in README_META.items():
        if dirname.startswith((".codex", ".agents")):
            continue
        dir_path = ROOT / dirname
        if not dir_path.exists():
            continue
        scoped = readme_records_for(dirname, records)
        projects = sorted({str(r["project"]) for r in scoped}, key=lambda p: list(PROJECTS.keys()).index(p) if p in PROJECTS else 99)
        rows = [[str(r["doc_id"]), str(r["title"]).replace("|", "\\|"), str(r["source_path"]), str(r["project"]), str(r["status"])] for r in scoped]
        content = f"# {label}\n\n"
        content += f"目录：`{dirname}`\n\n"
        content += f"用途：{purpose}\n\n"
        content += "KDS 空间：`开发`\n\n"
        content += f"KDS 路径前缀：`开发/{'92-证据与会话归档' if dirname.startswith('.harness') else '12-GPCF'}/{dirname}/`\n\n"
        content += f"关联项目：{', '.join(projects) if projects else 'GPCF'}\n\n"
        content += "受控规则：\n\n"
        content += "- 本目录新增 Markdown 文档必须纳入 `09-status/globalcloud-document-control-register.md`。\n"
        content += "- 当前有效文档使用 `controlled`；草案使用 `draft`；历史证据使用 `archive`。\n"
        content += "- 过期或被替代文档必须登记到 `09-status/document-deprecation-register.md`，不得静默删除。\n"
        content += "- KDS 双向同步以 `09-status/kds-development-space-sync-register.md` 为准。\n\n"
        if rows:
            content += "## 文档清单\n\n"
            content += markdown_table(["doc_id", "title", "source_path", "project", "status"], rows)
            content += "\n"
        write_text(dir_path / "README.md", content)


def should_have_readme(dir_path: Path) -> bool:
    if dir_path == ROOT:
        return False
    try:
        rel_dir = rel(dir_path)
    except ValueError:
        return False
    parts = set(dir_path.relative_to(ROOT).parts)
    if parts & EXCLUDE_DIRS:
        return False
    if rel_dir in README_META:
        return False
    if rel_dir.startswith((".codex", ".agents")):
        return False
    if rel_dir.startswith(".okf/bundles"):
        return False
    if rel_dir in GENERIC_DIR_PURPOSE:
        return True
    if any(p.suffix == ".md" for p in dir_path.iterdir() if p.is_file()):
        return True
    if rel_dir.startswith(".harness/runs/"):
        return True
    if rel_dir.startswith("openspec/changes/"):
        return True
    return False


def write_generic_readmes(records: list[dict[str, object]]) -> None:
    dirs = sorted([p for p in ROOT.rglob("*") if p.is_dir() and should_have_readme(p)], key=rel)
    for dir_path in dirs:
        rel_dir = rel(dir_path)
        label, purpose = GENERIC_DIR_PURPOSE.get(rel_dir, (dir_path.name, "保存本目录下的受控文档、证据或规格材料。"))
        scoped = readme_records_for(rel_dir, records)
        projects = sorted({str(r["project"]) for r in scoped}, key=lambda p: list(PROJECTS.keys()).index(p) if p in PROJECTS else 99)
        rows = [[str(r["doc_id"]), str(r["title"]).replace("|", "\\|"), str(r["source_path"]), str(r["project"]), str(r["status"])] for r in scoped]
        content = f"# {label}\n\n"
        content += f"目录：`{rel_dir}`\n\n"
        content += f"用途：{purpose}\n\n"
        content += "KDS 空间：`开发`\n\n"
        content += f"关联项目：{', '.join(projects) if projects else 'GPCF'}\n\n"
        content += "受控规则：\n\n"
        content += "- 本目录新增 Markdown 文档必须重新运行 `python3 tools/kds-sync/document_control.py`。\n"
        content += "- 当前有效文档使用 `controlled`；草案使用 `draft`；历史证据使用 `archive`。\n"
        content += "- 过期或被替代文档不得删除，必须进入归档台账或保留替代关系。\n\n"
        if rows:
            content += "## 文档清单\n\n"
            content += markdown_table(["doc_id", "title", "source_path", "project", "status"], rows)
            content += "\n"
        write_text(dir_path / "README.md", content)


def mirror_to_kds(records: list[dict[str, object]]) -> None:
    kds_root = ROOT / ".kds/development-space"
    if kds_root.exists():
        try:
            shutil.rmtree(kds_root, ignore_errors=True)
        except OSError:
            for child in sorted(kds_root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
                try:
                    if child.is_dir():
                        child.rmdir()
                    else:
                        child.unlink()
                except FileNotFoundError:
                    continue
            try:
                kds_root.rmdir()
            except FileNotFoundError:
                pass
    ledger_path = ROOT / ".kds/local-mirror-ledger.jsonl"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    entries = []
    for r in records:
        source = ROOT / str(r["source_path"])
        target = kds_root / str(r["kds_path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        entries.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "git_to_kds_local_mirror",
            "doc_id": r["doc_id"],
            "source_path": r["source_path"],
            "kds_path": r["kds_path"],
            "status": "mirrored",
        })
    write_text(ledger_path, "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries))


def parse_scope_paths() -> set[str]:
    raw = os.environ.get(SCOPE_ENV, "").strip()
    if not raw:
        return set()
    return {item.strip() for item in raw.split(",") if item.strip()}


def mirror_scope_to_kds(records: list[dict[str, object]]) -> None:
    kds_root = ROOT / ".kds/development-space"
    ledger_path = ROOT / ".kds/local-mirror-ledger.jsonl"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    scoped_sources = {str(r["source_path"]) for r in records}
    existing_entries: list[dict[str, object]] = []
    if ledger_path.exists():
        for line in ledger_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(entry.get("source_path", "")) not in scoped_sources:
                existing_entries.append(entry)
    entries = []
    for r in records:
        source = ROOT / str(r["source_path"])
        target = kds_root / str(r["kds_path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        entries.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "git_to_kds_local_mirror_scoped",
            "doc_id": r["doc_id"],
            "source_path": r["source_path"],
            "kds_path": r["kds_path"],
            "status": "mirrored",
        })
    write_text(ledger_path, "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in existing_entries + entries))


def write_kds_readme(records: list[dict[str, object]]) -> None:
    base = ROOT / ".kds/development-space/开发"
    rows = []
    for project, (folder, _) in PROJECTS.items():
        scoped = [r for r in records if str(r["kds_path"]).startswith(f"开发/{folder}/")]
        count = len(scoped)
        rows.append([project, folder, str(count)])
        project_dir = base / folder
        project_dir.mkdir(parents=True, exist_ok=True)
        project_content = f"# {project} 开发文档空间\n\n"
        project_content += f"生成日期：{TODAY}\n\n"
        project_content += f"用途：KDS `开发` 空间中 `{project}` 项目的受控文档入口。\n\n"
        if scoped:
            project_rows = [[str(r["doc_id"]), str(r["title"]).replace("|", "\\|"), str(r["source_path"]), str(r["status"])] for r in scoped]
            project_content += markdown_table(["doc_id", "title", "source_path", "status"], project_rows)
            project_content += "\n"
        else:
            project_content += "当前没有直接归属到本项目空间的源文档；相关内容可能位于 `90-跨项目架构` 或 `91-治理与验收`。\n"
        write_text(project_dir / "README.md", project_content)
    for folder in ["00-项目群总控", "90-跨项目架构", "91-治理与验收", "92-证据与会话归档", "99-过期文档"]:
        (base / folder).mkdir(parents=True, exist_ok=True)
    content = "# KDS 开发空间本地镜像\n\n"
    content += f"生成日期：{TODAY}\n\n"
    content += "用途：作为 KDS `开发` 空间的本地可审计镜像，并与真实 KDS API 同步工具链共同构成开发空间双向同步基础。\n\n"
    content += markdown_table(["project", "folder", "document_count"], rows)
    content += "\n"
    write_text(base / "README.md", content)


def write_tool_readme() -> None:
    content = "# KDS Sync Tools\n\n"
    content += "用途：维护 GlobalCloud GPCF 文档控制体系、目录 README、KDS `开发` 空间本地镜像和同步台账。\n\n"
    content += "运行：\n\n```bash\npython3 tools/kds-sync/document_control.py\n```\n\n"
    content += "输出：\n\n"
    content += "- `09-status/globalcloud-document-control-register.md`\n"
    content += "- `09-status/kds-development-space-sync-register.md`\n"
    content += "- `09-status/document-deprecation-register.md`\n"
    content += "- `.kds/development-space/开发/`\n"
    content += "- `.kds/local-mirror-ledger.jsonl`\n"
    content += "- `.kds/sync-ledger.jsonl`\n"
    write_text(ROOT / "tools/kds-sync/README.md", content)


def main() -> None:
    scope_paths = parse_scope_paths()
    if scope_paths:
        paths = iter_markdown()
        records = build_records(paths)
        scoped_records = [r for r in records if str(r["source_path"]) in scope_paths]
        missing = sorted(scope_paths - {str(r["source_path"]) for r in scoped_records})
        if missing:
            raise SystemExit(f"{SCOPE_ENV} contains unknown source paths: {', '.join(missing)}")
        apply_frontmatter(scoped_records)
        paths = iter_markdown()
        records = build_records(paths)
        write_registers(records)
        paths = iter_markdown()
        records = build_records(paths)
        register_records = [r for r in records if str(r["source_path"]) in GENERATED_REGISTERS]
        apply_frontmatter(register_records)
        paths = iter_markdown()
        records = build_records(paths)
        scoped_records = [r for r in records if str(r["source_path"]) in scope_paths]
        register_records = [r for r in records if str(r["source_path"]) in GENERATED_REGISTERS]
        mirror_scope_to_kds(scoped_records + register_records)
        return

    paths = iter_markdown()
    records = build_records(paths)
    apply_frontmatter(records)

    # Generate control surfaces, then make the generated files controlled too.
    # The final operation before mirroring must be frontmatter application, not
    # another overwrite of README/register content.
    for _ in range(2):
        paths = iter_markdown()
        records = build_records(paths)
        write_registers(records)
        write_directory_readmes(records)
        write_generic_readmes(records)
        write_tool_readme()
        paths = iter_markdown()
        records = build_records(paths)
        apply_frontmatter(records)

    paths = iter_markdown()
    records = build_records(paths)
    mirror_to_kds(records)
    write_kds_readme(records)


if __name__ == "__main__":
    main()
