#!/usr/bin/env python3
"""Validate the GlobalCloud project-group real execution governance board."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_PROJECTS = [
    "WAES",
    "XWAIL",
    "AaaS",
    "GFIS",
    "GPC",
    "PVAOS",
    "KDS",
    "Brain",
    "GPCF",
    "WAS",
]

REQUIRED_TASKS = [
    "GFIS-REAL-SOR-001",
    "WAES-LINT-RUNTIME-001",
    "KDS-RAG-EXPORT-001",
    "XWAIL-MIN-VALIDATOR-001",
    "AAAS-SERVICE-RUNTIME-001",
    "PVAOS-RELEASE-GATE-001",
    "GPC-EVIDENCE-BROWSER-001",
    "BRAIN-REVIEW-HANDOFF-001",
    "GPCF-EXECUTION-CONTROL-001",
]

REQUIRED_FIELDS = [
    "task_id",
    "project",
    "baseline_evidence",
    "commands",
    "expected_evidence",
    "gate",
    "rollback",
    "dependency_impact",
    "human_confirmation_required",
    "forbidden_claims",
]

REQUIRED_DEPENDENCIES = [
    "WAES -> XWAIL -> AaaS",
    "KDS -> Brain",
    "GFIS/GPC/PVAOS -> SCaaS",
    "WAS -> Ontology -> XWAIL",
    "GPCF -> all projects",
]

REQUIRED_STATUS_TOKENS = [
    "candidate",
    "partial_verified",
    "ready_for_review",
    "ready_for_uat",
    "accepted",
    "integrated",
    "customer_accepted",
]

REQUIRED_BOUNDARY_TOKENS = [
    "mock、fixture、synthetic/dev-only 数据",
    "未经授权的生产、权限或部署动作",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_TASK_DETAIL_TOKENS = {
    "GFIS-REAL-SOR-001": [
        "validate_gfis_was_source_record_submission_precheck.py",
        "gfis-real-source-record-intake-*",
        "WAES review gate",
        "保持 `repair_required`",
        "是，需要订单 owner",
    ],
    "WAES-LINT-RUNTIME-001": [
        "npm run check",
        "waes-lint-runtime-repair-*",
        "WAES quality gate",
        "回滚 lint 修复相关文件",
        "不声明 WAES 治理运行闭环完成",
    ],
    "KDS-RAG-EXPORT-001": [
        "validate_rag_export.py",
        "kds-rag-export-repair-20260625.md",
        "KDS RAG export gate",
        "validate_kds_rag_export_repair.py",
        "回滚 `_governance/scripts/rag_admission_policy.py`",
        "不声明 KDS 真实运行闭环完成",
    ],
    "XWAIL-MIN-VALIDATOR-001": [
        "validate_xwail.py",
        "xwail-min-validator-runtime-*",
        "XWAIL validator gate",
        "保持 `validator_commands_missing`",
        "不声明完整 XWAIL 工具链完成",
    ],
    "AAAS-SERVICE-RUNTIME-001": [
        "validate_service_package.py",
        "aaas-service-runtime-*",
        "AaaS service runtime gate",
        "保持 `service_package_metering_sla_commands_missing`",
        "不声明客户可订阅",
    ],
    "PVAOS-RELEASE-GATE-001": [
        "npm run release:gate:local",
        "pvaos-release-gate-repair-*",
        "PVAOS release local gate",
        "回滚测试环境",
        "不声明发布完成",
    ],
    "GPC-EVIDENCE-BROWSER-001": [
        "npm run quality:repo",
        "gpc-evidence-browser-repair-*",
        "browser/e2e gate",
        "回滚 README 索引",
        "不声明外部联调完成",
    ],
    "BRAIN-REVIEW-HANDOFF-001": [
        "npm run validate:harness-evidence",
        "brain-review-handoff-*",
        "human review gate",
        "保持 `ready_for_review / authorization_boundary`",
        "需要人工确认才能升级",
    ],
    "GPCF-EXECUTION-CONTROL-001": [
        "validate_project_group_real_execution_governance_board.py",
        "项目群真实执行任务变更记录",
        "Loop document gate",
        "最高状态为 `partial/rework`",
        "不声明项目群完成",
    ],
}

FORBIDDEN_UNBOUNDED_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    board_text = read(BOARD, failures)
    register_text = read(CORE_REGISTER, failures)

    for token in [
        "GlobalCloud 项目群真实执行治理总控板",
        "project_group_real_execution_governance = controlled",
        "project_group_real_execution_board = established",
        "next_execution_mode = project_by_project_real_gate_repair",
    ]:
        if token not in board_text:
            failures.append(f"missing board control token: {token}")

    for project in REQUIRED_PROJECTS:
        if project not in board_text:
            failures.append(f"missing project in board: {project}")

    for task in REQUIRED_TASKS:
        if task not in board_text:
            failures.append(f"missing task in board: {task}")

    for task, tokens in REQUIRED_TASK_DETAIL_TOKENS.items():
        row_prefix = f"| `{task}` |"
        rows = [line for line in board_text.splitlines() if line.startswith(row_prefix)]
        if len(rows) != 1:
            failures.append(f"task must have exactly one execution control row: {task}")
            continue
        row = rows[0]
        columns = [part.strip() for part in row.strip().strip("|").split("|")]
        if len(columns) != 10:
            failures.append(f"task execution control row must have 10 columns: {task}")
        for token in tokens:
            if token not in row:
                failures.append(f"task execution control row missing token for {task}: {token}")

    for field in REQUIRED_FIELDS:
        if f"`{field}`" not in board_text:
            failures.append(f"missing task control field: {field}")

    for dependency in REQUIRED_DEPENDENCIES:
        if dependency not in board_text:
            failures.append(f"missing dependency chain: {dependency}")

    for status in REQUIRED_STATUS_TOKENS:
        if f"`{status}`" not in board_text:
            failures.append(f"missing status gate token: {status}")

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in board_text:
            failures.append(f"missing boundary token: {token}")

    for token in FORBIDDEN_UNBOUNDED_CLAIMS:
        if token in board_text:
            failures.append(f"forbidden unbounded completion claim: {token}")

    if "globalcloud-core-chain-real-evidence-register.md" not in board_text:
        failures.append("board must reference the core-chain evidence register")

    if "GlobalCloud 项目群真实执行治理总控板" not in register_text:
        failures.append("core-chain register must reference the real execution governance board")

    result = {
        "gate": "project_group_real_execution_governance_board",
        "status": "pass" if not failures else "fail",
        "projects_checked": len(REQUIRED_PROJECTS),
        "tasks_checked": len(REQUIRED_TASKS),
        "dependencies_checked": len(REQUIRED_DEPENDENCIES),
        "failures": failures,
        "warnings": [
            "This gate validates the governance board structure and boundary wording; it does not execute project repositories.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
