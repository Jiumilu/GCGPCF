#!/usr/bin/env python3
"""Validate the authoritative WAS master plan control coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MASTER_PLAN = ROOT / "01-architecture/WAS世界资产体系总体方案.md"

REQUIRED_TOKENS = [
    "WAS世界资产体系总体方案",
    "唯一总体控制性文档",
    "GC-WAS-PG-BASELINE-0.1.0",
    "GlobalCloud WAS Project Group Baseline",
    "WAS 定义体系",
    "Ontology 定义语义",
    "XWAIL 定义契约",
    "WAES 负责注册、授权、发布",
    "项目群分层架构",
    "项目总体架构矩阵",
    "项目间协同架构",
    "全项目主方案传导机制",
    "主方案 -> 项目方案",
    "项目方案 -> 主方案",
    "Affected Project Matrix",
    "User Confirmation",
    "用户是否已确认",
    "全项目传导矩阵",
    "传导证明",
    "项目总体方案继承规则",
    "统一术语与名词表",
    "术语变更必须先修改本术语表",
    "统一状态模型",
    "事实源、证据源与知识源矩阵",
    "版本控制基线与兼容矩阵",
    "技术架构现状基线与收敛路线",
    "测试、验收与交付控制体系",
    "LOOP 工程体系",
    "数据、证据与知识治理",
    "安全、权限、租户与合规",
    "组织、决策、风险与依赖治理",
    "商业服务、计量与客户运营",
    "项目总体方案标准模板",
    "冲突判定与变更流程",
    "禁止事项与非声明边界",
    "自动一致性检查与治理脚本",
]

REQUIRED_PROJECTS = [
    "WAS世界资产体系",
    "GlobalCloud XWAIL",
    "GlobalCloud WAES",
    "GlobalCloud AaaS",
    "GlobalCloud AAAS",
    "GFIS",
    "GPC",
    "PVAOS",
    "KDS",
    "Brain",
    "Studio",
    "GPCF",
    "MMC",
    "GlobalCloud PKC",
    "GlobalCloud SOP",
    "GlobalCloud XGD",
    "GlobalCloud XiaoC",
    "GlobalCloud XiaoG",
]

FORBIDDEN_TOKENS = [
    "GPC-Native",
    "协同中台",
    "WAES 是业务主账",
    "文档完成等于业务完成",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    if not MASTER_PLAN.exists():
        failures.append(f"missing master plan: {MASTER_PLAN}")
        text = ""
    else:
        text = MASTER_PLAN.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing required token: {token}")

    for project in REQUIRED_PROJECTS:
        if project not in text:
            failures.append(f"missing project in master plan: {project}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            failures.append(f"forbidden token present: {token}")

    if "status: controlled" not in text:
        failures.append("frontmatter status is not controlled")
    if "version: v1.0" not in text:
        warnings.append("master plan version is not v1.0")

    result = {
        "gate": "was_master_plan_control",
        "status": "pass" if not failures else "fail",
        "master_plan": str(MASTER_PLAN),
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
