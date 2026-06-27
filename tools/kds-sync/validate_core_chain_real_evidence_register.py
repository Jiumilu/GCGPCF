#!/usr/bin/env python3
"""Validate the core-chain real evidence governance baseline."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
IMPLEMENTATION_PLAN = ROOT / "GlobalCloud 项目群实施方案.md"
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
    "Trigger Layer 对齐",
    "GlobalCloud 项目群 Ready for Review 触发映射表 2026-06-27",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "development_queue_ready = true",
    "trigger_layer_binding_count = 17",
    "dependency_edge_binding_count = 17",
    "| 链路/项目 | 当前实施方案 | trigger_layer | 真实进度 | 真实研发 | 真实运行 | 真实集成 | 真实交付 | 客户验收 | 下一步 |",
    "authorization_to_pre_execution_total_bridge",
    "repair_authorization_boundary",
    "pre_wave1_review_bridge",
    "source_record_boundary",
    "external_runtime_boundary",
    "local_release_review_boundary",
    "human_review_boundary",
    "真实证据状态机",
    "证据最低标准",
    "核心链路真实证据矩阵",
    "运行命令登记",
    "next_stage_authorization_package_ready",
    "next_stage_authorization_chain_loop_round_ready",
    "validate_project_group_next_stage_authorization_package_20260627.py",
    "validate_project_group_next_stage_authorization_chain_loop_round_20260627.py",
    "单仓锚点",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
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
