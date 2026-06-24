#!/usr/bin/env python3
"""Validate inheritance structure for established project implementation plans."""

from __future__ import annotations

import json
from pathlib import Path

from validate_project_implementation_uniqueness import EXPECTED_IMPLEMENTATION_PLANS, REQUIRED_PROJECTS


REQUIRED_SECTIONS = [
    "项目实施定位",
    "对应项目总体方案",
    "实施目标",
    "当前真实状态",
    "实施里程碑",
    "研发任务清单",
    "运行环境与启动命令",
    "集成关系与接口契约",
    "测试与验证计划",
    "交付物清单",
    "客户验收路径",
    "风险、依赖、阻塞与回滚",
    "LOOP 接入",
    "证据索引",
    "非声明边界",
]

REQUIRED_TOKENS = [
    "GlobalCloud项目群实施方案.md",
    "loop_enabled: true",
    "不声明业务实现完成",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    checked_projects: set[str] = set()
    for project, paths in EXPECTED_IMPLEMENTATION_PLANS.items():
        for path in paths:
            if not path.exists():
                continue
            checked_projects.add(project)
            checked.append(str(path))
            text = path.read_text(encoding="utf-8")
            for section in REQUIRED_SECTIONS:
                if section not in text:
                    failures.append(f"{path.name}: missing section {section}")
            for token in REQUIRED_TOKENS:
                if token not in text:
                    failures.append(f"{path.name}: missing token {token}")

    missing_required = sorted(REQUIRED_PROJECTS - checked_projects)
    for project in missing_required:
        failures.append(f"implementation plan not checked: {project}")

    if not checked:
        warnings.append("no project implementation plans established yet")

    result = {
        "gate": "project_implementation_inheritance",
        "status": "pass" if not failures else "fail",
        "phase": "phase_3_all_project_plans_controlled",
        "failures": failures,
        "warnings": warnings,
        "checked": checked,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
