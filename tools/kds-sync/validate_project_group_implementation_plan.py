#!/usr/bin/env python3
"""Validate the GlobalCloud project-group implementation-plan control baseline."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "01-architecture/GlobalCloud项目群实施方案.md"
TEMPLATE = ROOT / "templates/project-implementation-plan-template.md"
REGISTER = ROOT / "09-status/globalcloud-project-implementation-control-register.md"
PROPAGATION = ROOT / "02-governance/project-implementation-plan-change-propagation-template.md"
WAS_ONTOLOGY_PROMPT = ROOT / "02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md"

REQUIRED_PLAN_TOKENS = [
    "GlobalCloud 项目群实施方案",
    "唯一总实施主方案",
    "WAS世界资产体系总体方案.md",
    "真实进度",
    "真实研发",
    "真实运行",
    "真实集成",
    "真实交付",
    "真实客户验收",
    "implementation_plan_governance = phase_3_all_project_plans_controlled",
    "loop_enabled: true",
    "WAS/LOOP 实施链路",
    "GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md",
    "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101",
    "不声明任何业务项目已经真实研发完成",
]

REQUIRED_SUPPORT_TOKENS = [
    "project-implementation-plan-template.md",
    "globalcloud-project-implementation-control-register.md",
    "project-implementation-plan-change-propagation-template.md",
]

REQUIRED_WAS_ONTOLOGY_TOKENS = [
    "GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词",
    "latest_monitor_round | `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-100`",
    "next_monitor_round | `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101`",
    "hold_required=1",
    "real_source_records=0",
    "run:",
    "stop:",
    "verify:",
    "recover:",
    "debug:",
    "不声明真实 P4 source-record 已提交",
]

REQUIRED_FILES = [PLAN, TEMPLATE, REGISTER, PROPAGATION, WAS_ONTOLOGY_PROMPT]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    plan_text = read(PLAN, failures)
    template_text = read(TEMPLATE, failures)
    register_text = read(REGISTER, failures)
    propagation_text = read(PROPAGATION, failures)
    was_ontology_text = read(WAS_ONTOLOGY_PROMPT, failures)

    for path in REQUIRED_FILES:
        if path.exists() and "status: controlled" not in path.read_text(encoding="utf-8"):
            failures.append(f"file is not controlled: {path}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in implementation plan: {token}")

    for token in REQUIRED_SUPPORT_TOKENS:
        if token not in plan_text:
            failures.append(f"implementation plan does not reference support token: {token}")

    for token in REQUIRED_WAS_ONTOLOGY_TOKENS:
        if token not in was_ontology_text:
            failures.append(f"missing token in WAS/Ontology implementation prompt: {token}")

    if "项目实施定位" not in template_text or "证据索引" not in template_text:
        failures.append("implementation template missing required structure")

    if "implementation_plan_governance = phase_3_all_project_plans_controlled" not in register_text:
        failures.append("implementation register does not declare phase_3_all_project_plans_controlled")

    if "Implementation Change Proposal" not in propagation_text:
        failures.append("implementation propagation template missing Change Proposal")

    result = {
        "gate": "project_group_implementation_plan",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
