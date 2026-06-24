#!/usr/bin/env python3
"""Validate the core-chain real evidence governance baseline."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
IMPLEMENTATION_PLAN = ROOT / "01-architecture/GlobalCloud项目群实施方案.md"
TEMPLATE = ROOT / "templates/real-evidence-record-template.md"

REQUIRED_PROJECTS = [
    "GPCF",
    "WAES",
    "XWAIL",
    "AaaS",
    "GFIS",
    "GPC",
    "PVAOS",
    "KDS",
    "Brain",
]

REQUIRED_STATUS_TOKENS = [
    "not_collected",
    "declared",
    "command_defined",
    "candidate",
    "verified",
    "ready_for_review",
    "ready_for_uat",
    "customer_review",
    "customer_accepted",
    "repair_required",
]

REQUIRED_REGISTER_TOKENS = [
    "GlobalCloud 核心链路真实证据台账",
    "WAES -> XWAIL -> AaaS -> GFIS/GPC/PVAOS -> KDS/Brain",
    "真实证据状态机",
    "证据最低标准",
    "核心链路真实证据矩阵",
    "运行命令登记",
    "core_chain_real_evidence_governance = baseline_controlled",
    "real runtime and integration evidence remain pending",
    "不声明任何核心链路项目真实运行完成",
    "不声明任何跨项目接口真实集成完成",
]

REQUIRED_TEMPLATE_TOKENS = [
    "真实证据记录模板",
    "evidence_type",
    "执行命令",
    "原始输出摘要",
    "结论边界",
    "requires_user_confirmation",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    register_text = read(REGISTER, failures)
    implementation_text = read(IMPLEMENTATION_PLAN, failures)
    template_text = read(TEMPLATE, failures)

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in real evidence register: {token}")

    for project in REQUIRED_PROJECTS:
        if project not in register_text:
            failures.append(f"missing core-chain project in real evidence register: {project}")

    for token in REQUIRED_STATUS_TOKENS:
        if token not in register_text:
            failures.append(f"missing status token in real evidence register: {token}")

    for token in REQUIRED_TEMPLATE_TOKENS:
        if token not in template_text:
            failures.append(f"missing token in real evidence template: {token}")

    if "globalcloud-core-chain-real-evidence-register.md" not in implementation_text:
        failures.append("implementation plan does not reference real evidence register")

    if "real-evidence-record-template.md" not in implementation_text:
        failures.append("implementation plan does not reference real evidence template")

    warnings.append("baseline validates evidence governance only; runtime, integration, delivery, and customer acceptance remain pending")

    result = {
        "gate": "core_chain_real_evidence_register",
        "status": "pass" if not failures else "fail",
        "governance": "baseline_controlled",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
