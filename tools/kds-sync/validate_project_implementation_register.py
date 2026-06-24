#!/usr/bin/env python3
"""Validate the project implementation control register."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-project-implementation-control-register.md"
MASTER_REGISTER = ROOT / "09-status/globalcloud-project-master-plan-control-register.md"

REQUIRED_PROJECTS = [
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
    "GlobalCloud GPCF",
    "shared/python_utils",
]

REQUIRED_TOKENS = [
    "GlobalCloud 项目群实施方案控制台账",
    "每个项目只能有一个当前有效实施方案",
    "实施状态必须由真实进度",
    "implementation_plan_governance = phase_3_all_project_plans_controlled",
    "所有登记业务项目的唯一实施方案已建立并受控",
    "真实研发、真实运行、真实集成、真实交付和客户验收仍需后续证据",
    "not_project",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    text = REGISTER.read_text(encoding="utf-8") if REGISTER.exists() else ""
    master_text = MASTER_REGISTER.read_text(encoding="utf-8") if MASTER_REGISTER.exists() else ""

    if not text:
        failures.append(f"missing register: {REGISTER}")
    if not master_text:
        failures.append(f"missing master plan register: {MASTER_REGISTER}")

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing token in implementation register: {token}")

    for project in REQUIRED_PROJECTS:
        if project not in text:
            failures.append(f"missing project in implementation register: {project}")

    if "project_master_plan_alignment = controlled" not in master_text:
        failures.append("master-plan register is not controlled; implementation cannot proceed")

    result = {
        "gate": "project_implementation_register",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
