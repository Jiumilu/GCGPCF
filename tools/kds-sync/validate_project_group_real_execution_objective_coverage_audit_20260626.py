#!/usr/bin/env python3
"""Validate the project-group real-execution objective coverage audit."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-real-execution-objective-coverage-audit-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

REQUIRED_DOC_TOKENS = [
    "GPCF-REAL-EXECUTION-OBJECTIVE-COVERAGE-AUDIT-20260626-001",
    "project_group_real_execution_objective_coverage_audit_20260626 = controlled",
    "real_execution_objective_coverage_audit_controlled",
    "requirement_count | `7`",
    "covered_requirement_count | `7`",
    "unresolved_boundary_count | `4`",
    "对每个项目建立当前真实状态基线",
    "明确每个项目的下一批可执行任务",
    "每个任务绑定命令、证据、门禁、回滚边界",
    "将项目间依赖纳入矩阵",
    "逐步把各项目状态从 candidate/partial_verified/repair_required 推进到 ready_for_review",
    "只有经过人工确认，才允许进入 accepted、integrated 或客户验收状态",
    "确保项目群内所有会话识别项目群总体方案体系和实施方案体系",
    "WAES -> XWAIL -> AaaS",
    "KDS -> Brain",
    "GFIS/GPC/PVAOS -> SCaaS",
    "WAS -> Ontology -> XWAIL",
    "GPCF -> all projects",
    "validate_project_group_scheme_recognition_rules_20260626.py",
    "17 个 `AGENTS.md`",
    "34 个项目级方案文件",
    "globalcloud-project-group-ready-for-review-trigger-map-20260627.md",
    "validate_project_group_ready_for_review_trigger_map_20260627.py",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "validate_project_group_dev_task_queue_20260626.py",
    "17 项目开发态任务队列",
    "17 项目任务级 trigger/dependency 绑定",
    "trigger_layer_binding_count = 41",
    "dependency_edge_binding_count = 41",
    "auto_ready_for_review_upgrade=false",
    "authorization_granted=false",
    "action_executed=false",
    "globalcloud-project-group-next-stage-authorization-decision-board-20260626.md",
    "globalcloud-project-group-authorization-layer-matrix-20260627.md",
    "globalcloud-project-group-human-confirmation-request-20260625.md",
    "globalcloud-project-group-authorization-routing-20260625.md",
    "globalcloud-project-group-review-auth-pre-wave1-wave1-bridge-audit-20260627.md",
    "globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md",
    "globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md",
    "globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md",
    "globalcloud-project-group-next-stage-authorization-package-20260627.md",
    "loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md",
    "globalcloud-project-group-wave1-receipt-pre-execution-bridge-audit-20260627.md",
    "globalcloud-project-group-execution-receipt-pre-execution-bridge-audit-20260627.md",
    "globalcloud-project-group-authorization-to-pre-execution-total-bridge-audit-20260627.md",
    "validate_project_group_authorization_layer_matrix_20260627.py",
    "validate_project_group_human_confirmation_request.py",
    "validate_project_group_authorization_routing.py",
    "validate_project_group_review_auth_pre_wave1_wave1_bridge_audit_20260627.py",
    "validate_project_group_wave1_receipt_pre_execution_bridge_audit_20260627.py",
    "validate_project_group_execution_receipt_pre_execution_bridge_audit_20260627.py",
    "validate_project_group_authorization_to_pre_execution_total_bridge_audit_20260627.py",
    "validate_project_group_next_stage_authorization_package_20260627.py",
    "validate_project_group_next_stage_authorization_chain_loop_round_20260627.py",
    "kds_api_sync_executed=false",
    "commit_executed=false",
    "push_executed=false",
    "accepted=false",
    "integrated=false",
    "production_ready=false",
    "customer_accepted=false",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-REAL-EXECUTION-OBJECTIVE-COVERAGE-AUDIT-20260626-001",
    "globalcloud-project-group-real-execution-objective-coverage-audit-20260626.md",
    "validate_project_group_real_execution_objective_coverage_audit_20260626.py",
    "project_group_real_execution_objective_coverage_audit_20260626 = controlled",
    "real_execution_objective_coverage_audit_controlled",
]

FORBIDDEN_TOKENS = [
    "accepted=true",
    "integrated=true",
    "production_ready=true",
    "customer_accepted=true",
    "auto_ready_for_review_upgrade=true",
    "authorization_granted=true",
    "action_executed=true",
    "kds_api_sync_executed=true",
    "commit_executed=true",
    "push_executed=true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(label: str, text: str, tokens: list[str], failures: list[str]) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{label} missing token: {token}")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    governance_text = "\n".join(
        [
            read(BOARD, failures),
            read(CORE_REGISTER, failures),
            read(TASK_PACKS, failures),
        ]
    )

    require_tokens("coverage audit", doc_text, REQUIRED_DOC_TOKENS, failures)
    require_tokens("governance", governance_text, REQUIRED_GOVERNANCE_TOKENS, failures)

    covered_rows = [line for line in doc_text.splitlines() if "| `covered`" in line]
    if len(covered_rows) != 7:
        failures.append(f"coverage audit must have 7 covered requirement rows, found {len(covered_rows)}")

    combined = doc_text + "\n" + governance_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_real_execution_objective_coverage_audit_20260626",
        "status": "pass" if not failures else "fail",
        "requirement_count": 7,
        "covered_requirement_count": 7 if not failures else len(covered_rows),
        "failures": failures,
        "warnings": [
            "This validates objective coverage only; it does not execute tasks, clean KDS, stage, commit, push, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
