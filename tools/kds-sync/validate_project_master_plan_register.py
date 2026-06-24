#!/usr/bin/env python3
"""Validate the GlobalCloud project master plan control register."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-project-master-plan-control-register.md"
MASTER_PLAN = ROOT / "01-architecture/WAS世界资产体系总体方案.md"

REQUIRED_PROJECTS = [
    "项目群总控",
    "GlobalCloud GPCF",
    "WAS世界资产体系",
    "GlobalCloud XWAIL",
    "GlobalCloud AAAS / AaaS",
    "GlobalCloud WAES",
    "GlobalCloud GFIS",
    "GlobalCloud GPC",
    "GlobalCloud PVAOS",
    "GlobalCloud KDS",
    "GlobalCloud Brain",
    "GlobalCloud Studio",
    "GlobalCloud MMC",
    "GlobalCloud PKC",
    "GlobalCloud SOP",
    "GlobalCloud XGD",
    "GlobalCloud XiaoC",
    "GlobalCloud XiaoG",
    "shared/python_utils",
]

REQUIRED_TOKENS = [
    "GlobalCloud 项目群主方案控制台账",
    "WAS世界资产体系总体方案",
    "每个项目只能有一个当前有效总体方案",
    "主方案变化必须先更新本台账的受影响项目",
    "项目方案变化必须先回流到主方案",
    "用户确认",
    "project_master_plan_alignment = controlled",
    "all registered business projects have one authoritative project master plan",
    "docs/GlobalCloud WAS 总体方案.md",
    "GlobalCloud XWAIL 总体方案.md",
    "docs/GlobalCloud AaaS 总体方案.md",
    "GlobalCloud GPC 总体方案.md",
    "shared/python_utils",
    "not_project",
]

REQUIRED_STATUSES = [
    "authoritative",
    "candidate",
    "missing",
    "conflict",
    "rename_required",
    "not_project",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    if not REGISTER.exists():
        failures.append(f"missing register: {REGISTER}")
        text = ""
    else:
        text = REGISTER.read_text(encoding="utf-8")

    if not MASTER_PLAN.exists():
        failures.append(f"missing master plan: {MASTER_PLAN}")
        master_text = ""
    else:
        master_text = MASTER_PLAN.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing required token in register: {token}")

    for project in REQUIRED_PROJECTS:
        if project not in text:
            failures.append(f"missing project row in register: {project}")

    for status in REQUIRED_STATUSES:
        if f"`{status}`" not in text:
            failures.append(f"missing status definition or usage: {status}")

    if "globalcloud-project-master-plan-control-register.md" not in master_text:
        failures.append("master plan does not reference project master plan register")

    if "validate_project_master_plan_register.py" not in master_text:
        failures.append("master plan does not reference project master plan register validator")

    if "GPC-Native" in text:
        failures.append("legacy token GPC-Native must not appear in the register")

    authoritative_paths = [
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系/docs/GlobalCloud WAS 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XWAIL/GlobalCloud XWAIL 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud AAAS/docs/GlobalCloud AaaS 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC/GlobalCloud GPC 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES/GlobalCloud WAES 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/GlobalCloud GFIS 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS/GlobalCloud PVAOS 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/GlobalCloud KDS 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain/GlobalCloud Brain 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/GlobalCloud Studio 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/GlobalCloud MMC 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC/GlobalCloud PKC 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud SOP/GlobalCloud SOP 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD/GlobalCloud XGD 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC/GlobalCloud XiaoC 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/GlobalCloud XiaoG 总体方案.md"),
        Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF/GlobalCloud GPCF 总体方案.md"),
    ]
    required_plan_tokens = [
        "与项目群主方案的继承关系",
        "项目群版本基线",
        "本项目权威职责",
        "本项目不承担的职责",
        "核心交付物",
        "与其他项目的接口关系",
        "技术架构现状和目标架构",
        "测试、交付和运行命令",
        "LOOP 接入",
        "风险、依赖、回滚和非声明边界",
    ]
    for plan_path in authoritative_paths:
        if not plan_path.exists():
            failures.append(f"missing authoritative project plan: {plan_path}")
            continue
        plan_text = plan_path.read_text(encoding="utf-8")
        for token in required_plan_tokens:
            if token not in plan_text:
                failures.append(f"missing token in {plan_path.name}: {token}")

    result = {
        "gate": "project_master_plan_register",
        "status": "pass" if not failures else "fail",
        "register": str(REGISTER),
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
