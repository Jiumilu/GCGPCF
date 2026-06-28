#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-real-execution-governance-progress-20260626.md"

REQUIRED_STRINGS = [
    "project_group_git_clean = blocked",
    "checked_repo_count = 17",
    "dirty_repo_count = 3",
    "review_boundary_repo_count = 3",
    "noise_cleanup_repo_count = 0",
    "pass_repo_count = 14",
    "ahead_repos = 0",
    "behind_repos = 0",
    "sensitive_repos = 1",
    "diff_check = pass",
    "live_project_group_git_gate = blocked",
    "auto_ready_for_review_upgrade = false",
    "authorization_granted = false",
    "action_executed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "WAES-LINT-RUNTIME-001",
    "GFIS-REAL-SOR-001",
    "GPC-EXTERNAL-RUNTIME-EVIDENCE-001",
    "BRAIN-HUMAN-REVIEW-DECISION-001",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001",
    "AAAS-WAES-BINDING-PRECHECK-001",
    "SOP-SCENARIO-OWNER-REVIEW-001",
    "validate_project_group_next_stage_authorization_decision_board_20260626.py",
    "validate_project_group_next_stage_authorization_receipt_example_pack_20260627.py",
    "validate_project_group_next_stage_authorization_receipt_recording_procedure_20260627.py",
    "validate_project_group_next_stage_authorization_human_fill_request_20260627.py",
    "validate_project_group_next_stage_authorization_package_20260627.py",
    "validate_project_group_next_stage_authorization_chain_loop_round_20260627.py",
    "validate_project_group_real_execution_metadata_coverage_20260626.py",
    "validate_project_group_wave1_receipt_pre_execution_bridge_audit_20260627.py",
    "validate_project_group_execution_receipt_pre_execution_bridge_audit_20260627.py",
    "validate_project_group_ready_for_review_trigger_map_20260627.py",
    "validate_project_group_dev_task_queue_20260626.py",
    "validate_core_chain_real_evidence_register.py",
    "validate_project_implementation_register.py",
    "17 项目开发态入口已显式绑定 `trigger_layer`、`dependency_edge` 和 authoritative entry",
    "binding_row_count=17",
    "41 条任务行已显式绑定 `trigger_layer`、`dependency_edge` 和 authoritative entry",
    "task_pack_count=41",
    "trigger_layer_binding_count=41",
    "dependency_edge_binding_count=41",
    "GPCF-NEXT-STAGE-AUTHORIZATION-HUMAN-FILL-REQUEST-20260627-001",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "key_doc_count=36",
    "WAES -> XWAIL/AaaS",
    "GFIS/GPC/PVAOS -> SCaaS",
    "KDS -> Brain",
    "review_boundary_repos_current = GlobalCoud GPCF, GlobalCloud GFIS, GlobalCloud KDS",
    "noise_cleanup_repo_current = none",
    "trigger_layer 控制面传导",
    "trigger layer 已从总控板传导到核心链路证据台账和实施方案台账",
    "core_trigger_layer_count=8",
    "implementation_trigger_layer_count=18",
    "run",
    "stop",
    "verify",
    "recover",
    "debug",
]

PROJECTS = [
    "GlobalCoud GPCF",
    "GlobalCloud GFIS",
    "GlobalCloud KDS",
]


def main() -> int:
    failures: list[str] = []
    if not DOC.exists():
        failures.append(f"missing document: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")

    for value in REQUIRED_STRINGS:
        if value not in text:
            failures.append(f"missing required text: {value}")

    missing_projects = [project for project in PROJECTS if project not in text]
    for project in missing_projects:
        failures.append(f"missing project row: {project}")

    result = {
        "gate": "project_group_real_execution_governance_progress_20260626",
        "status": "fail" if failures else "pass",
        "project_count": len(PROJECTS) - len(missing_projects),
        "required_string_count": len(REQUIRED_STRINGS),
        "failures": failures,
        "warnings": [
            "This validates governance progress evidence only; it does not execute project tasks, clean repos, stage, commit, push, deploy, release, or grant accepted/integrated/customer acceptance."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
