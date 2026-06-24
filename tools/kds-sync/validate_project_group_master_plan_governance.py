#!/usr/bin/env python3
"""Validate the project-group master-plan governance objective and roadmap."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent

GOVERNANCE_DOC = ROOT / "02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md"
MASTER_PLAN = ROOT / "01-architecture/WAS世界资产体系总体方案.md"
REGISTER = ROOT / "09-status/globalcloud-project-master-plan-control-register.md"
PROJECT_PLAN_TEMPLATE = ROOT / "templates/project-master-plan-template.md"
CHANGE_PROPAGATION_TEMPLATE = ROOT / "02-governance/project-master-plan-change-propagation-template.md"
STATUS_REPORT = ROOT / "09-status/project-group-master-plan-governance-status-report.md"

REQUIRED_DOC_TOKENS = [
    "GlobalCloud 项目群总体方案治理专项目标与路线图",
    "WAS世界资产体系总体方案.md",
    "globalcloud-project-master-plan-control-register.md",
    "project_group_master_plan_governance = controlled",
    "all registered business projects have one authoritative project master plan",
    "shared/python_utils",
    "不作为业务项目",
    "项目总体方案统一结构",
    "传导机制",
    "用户确认边界",
    "实施路线图",
    "validate_project_master_plan_uniqueness.py",
    "validate_project_plan_inheritance.py",
    "validate_project_terms_consistency.py",
    "validate_project_version_compatibility.py",
    "validate_project_group_delivery_readiness.py",
    "非声明边界",
]

REQUIRED_TEMPLATE_TOKENS = [
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

REQUIRED_CHANGE_TEMPLATE_TOKENS = [
    "Change Proposal",
    "Affected Project Matrix",
    "用户确认",
    "传导证据",
    "未经用户确认的结构性变化",
]

REQUIRED_STATUS_REPORT_TOKENS = [
    "project_group_master_plan_governance = controlled",
    "delivery_readiness = partial",
    "all registered business projects have one authoritative project master plan",
    "GPCF 项目总体方案",
    "最终状态报告",
    "project_group_master_plan_governance_completion_audit = pass",
    "完成审计矩阵",
    "后续任何主方案或项目方案结构性变化必须先登记 Change Proposal",
]

REQUIRED_PROJECTS = [
    "WAS世界资产体系",
    "GlobalCloud XWAIL",
    "GlobalCloud AaaS / AAAS",
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
    "GlobalCoud GPCF",
]

REGISTER_PROJECT_ALIASES = {
    "GlobalCloud AaaS / AAAS": "GlobalCloud AAAS / AaaS",
    "GlobalCoud GPCF": "GlobalCloud GPCF",
}

FIRST_BATCH_PATHS = [
    PROJECT_ROOT / "GlobalCloud WAES/GlobalCloud WAES 总体方案.md",
    PROJECT_ROOT / "GlobalCloud GFIS/GlobalCloud GFIS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud PVAOS/GlobalCloud PVAOS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud KDS/GlobalCloud KDS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud Brain/GlobalCloud Brain 总体方案.md",
    PROJECT_ROOT / "GlobalCloud Studio/GlobalCloud Studio 总体方案.md",
]

REQUIRED_VALIDATORS = [
    ROOT / "tools/kds-sync/validate_was_master_plan_control.py",
    ROOT / "tools/kds-sync/validate_project_group_master_plan_governance.py",
    ROOT / "tools/kds-sync/validate_project_master_plan_register.py",
    ROOT / "tools/kds-sync/validate_project_master_plan_uniqueness.py",
    ROOT / "tools/kds-sync/validate_project_plan_inheritance.py",
    ROOT / "tools/kds-sync/validate_project_terms_consistency.py",
    ROOT / "tools/kds-sync/validate_project_version_compatibility.py",
    ROOT / "tools/kds-sync/validate_project_group_delivery_readiness.py",
    ROOT / "tools/kds-sync/validate_project_master_plan_batch_1_authorization.py",
    ROOT / "tools/kds-sync/validate_project_master_plan_batch_2_authorization.py",
]

AUTHORIZATION_DOC = ROOT / "02-governance/project-master-plan-batch-1-authorization-request.md"
AUTHORIZATION_DOC_BATCH_2 = ROOT / "02-governance/project-master-plan-batch-2-authorization-request.md"
REQUIRED_AUTHORIZATION_TOKENS = [
    "authorization_status: confirmed_by_user",
    "我确认开始第一批项目总体方案批量建立",
    "确认时间：2026-06-24",
]
REQUIRED_BATCH_2_AUTHORIZATION_TOKENS = [
    "authorization_status: confirmed_by_user",
    "我确认开始第二批项目总体方案批量建立",
    "确认时间：2026-06-24",
]


def read_text(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    doc_text = read_text(GOVERNANCE_DOC, failures)
    master_text = read_text(MASTER_PLAN, failures)
    register_text = read_text(REGISTER, failures)
    template_text = read_text(PROJECT_PLAN_TEMPLATE, failures)
    change_template_text = read_text(CHANGE_PROPAGATION_TEMPLATE, failures)
    status_report_text = read_text(STATUS_REPORT, failures)
    authorization_text = read_text(AUTHORIZATION_DOC, failures)
    authorization_text_batch_2 = read_text(AUTHORIZATION_DOC_BATCH_2, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing required token in governance doc: {token}")

    for token in REQUIRED_TEMPLATE_TOKENS:
        if token not in template_text:
            failures.append(f"missing required token in project plan template: {token}")

    for token in REQUIRED_CHANGE_TEMPLATE_TOKENS:
        if token not in change_template_text:
            failures.append(f"missing required token in change propagation template: {token}")

    for token in REQUIRED_STATUS_REPORT_TOKENS:
        if token not in status_report_text:
            failures.append(f"missing required token in status report: {token}")

    for token in REQUIRED_AUTHORIZATION_TOKENS:
        if token not in authorization_text:
            failures.append(f"missing required token in batch authorization request: {token}")

    for token in REQUIRED_BATCH_2_AUTHORIZATION_TOKENS:
        if token not in authorization_text_batch_2:
            failures.append(f"missing required token in batch-2 authorization request: {token}")

    for project in REQUIRED_PROJECTS:
        if project not in doc_text:
            failures.append(f"missing project in governance doc: {project}")
        register_project = REGISTER_PROJECT_ALIASES.get(project, project)
        if register_project not in register_text:
            failures.append(f"missing project in control register: {project}")

    if "唯一总体控制性文档" not in master_text:
        failures.append("master plan does not declare unique controlling document")

    if "project_master_plan_alignment = controlled" not in register_text:
        failures.append("register does not declare controlled project master-plan alignment")

    missing_first_batch = [str(path) for path in FIRST_BATCH_PATHS if not path.exists()]
    if missing_first_batch:
        warnings.append("first batch project plans are not yet established: " + "; ".join(missing_first_batch))

    for validator in REQUIRED_VALIDATORS:
        if not validator.exists():
            failures.append(f"missing validator: {validator}")

    result = {
        "gate": "project_group_master_plan_governance",
        "status": "pass" if not failures else "fail",
        "governance_doc": str(GOVERNANCE_DOC),
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
