#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-real-execution-completion-gap-matrix-20260626.md"

REQUIRED_TOKENS = [
    "project_group_real_execution_completion_gap_matrix_20260626 = controlled",
    "requirement_count = 7",
    "coverage_controlled_count = 7",
    "execution_complete_count = 0",
    "remaining_gap_count = 7",
    "project_group_git_clean = blocked",
    "authorization_granted = false",
    "action_executed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "execution_complete = false",
    "auto_ready_for_review_upgrade = false",
    "17 项目当前真实状态基线",
    "17 项目下一批可执行任务",
    "每个任务绑定命令、证据、门禁、回滚边界",
    "项目间依赖矩阵",
    "状态推进到 ready_for_review",
    "accepted/integrated/customer_accepted 只能人工确认",
    "LOOP 持续闭环工程治理系统",
    "globalcloud-project-group-ready-for-review-trigger-map-20260627.md",
    "WAES repair",
    "GFIS source-of-record",
    "GPC external runtime",
    "Brain human review",
    "客户验收",
    "AUTH-WAVE1-WAES-LINT-RUNTIME-20260626",
    "AUTH-WAVE1-GFIS-REAL-SOR-20260626",
    "AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626",
    "AUTH-WAVE1-BRAIN-HUMAN-REVIEW-20260626",
    "AUTH-WAVE1-GPCF-POST-SCHEME-REVIEW-20260626",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "validate_project_group_dev_task_queue_20260626.py",
    "development_queue_ready = true",
    "trigger_layer_binding_count = 17",
    "dependency_edge_binding_count = 17",
    "globalcloud-project-group-authorization-layer-matrix-20260627.md",
    "globalcloud-project-group-human-confirmation-request-20260625.md",
    "globalcloud-project-group-authorization-routing-20260625.md",
    "globalcloud-project-group-review-auth-pre-wave1-wave1-bridge-audit-20260627.md",
    "globalcloud-project-group-wave1-receipt-pre-execution-bridge-audit-20260627.md",
    "globalcloud-project-group-execution-receipt-pre-execution-bridge-audit-20260627.md",
    "globalcloud-project-group-authorization-to-pre-execution-total-bridge-audit-20260627.md",
    "globalcloud-project-group-next-stage-authorization-package-20260627.md",
    "loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md",
    "17 项目 Last-Mile Blocker List",
    "离 `ready_for_review` 或下一人工边界的最后阻塞项",
    "GlobalCloud AAAS",
    "GlobalCloud Brain",
    "WAS世界资产体系",
    "GlobalCloud XiaoC",
    "GlobalCloud WAES",
    "GlobalCloud GPC",
    "GlobalCloud Studio",
    "GlobalCoud GPCF",
    "GlobalCloud XWAIL",
    "GlobalCloud GFIS",
    "GlobalCloud MMC",
    "GlobalCloud KDS",
    "GlobalCloud XiaoG",
    "GlobalCloud PVAOS",
    "GlobalCloud SOP",
    "GlobalCloud PKC",
    "GlobalCloud XGD",
    "P0/P1 收口顺序",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "3 仓 total dirty、14 仓 clean",
    "`GlobalCoud GPCF / GlobalCloud GFIS / GlobalCloud KDS` 为当前 3 仓 review 边界",
    "`AAAS/XWAIL/SOP` delegated wrapper 单仓锚点已回退到各自主任务入口",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-WAVE1-WAES-LINT-RUNTIME-20260626",
    "AUTH-WAVE1-GFIS-REAL-SOR-20260626",
    "AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626",
    "AUTH-WAVE1-BRAIN-HUMAN-REVIEW-20260626",
]

FORBIDDEN_TOKENS = [
    "execution_complete = true",
    "authorization_granted = true",
    "action_executed = true",
    "auto_ready_for_review_upgrade = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
]


def main() -> int:
    failures: list[str] = []
    if not DOC.exists():
        failures.append(f"missing document: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing required token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            failures.append(f"forbidden positive claim: {token}")

    coverage_rows = [line for line in text.splitlines() if "| `coverage_controlled` | `not_complete` |" in line]
    if len(coverage_rows) != 7:
        failures.append(f"expected 7 coverage/not_complete rows, found {len(coverage_rows)}")

    blocker_rows = [line for line in text.splitlines() if line.startswith("| GlobalCloud ") or line.startswith("| WAS世界资产体系 |") or line.startswith("| GlobalCoud GPCF |")]
    blocker_rows = [line for line in blocker_rows if "离 `ready_for_review` 或下一人工边界的最后阻塞项" not in line]
    if len(blocker_rows) < 17:
        failures.append(f"expected at least 17 project blocker rows, found {len(blocker_rows)}")

    operator_rows = [line for line in text.splitlines() if line.startswith("| P0-") or line.startswith("| P1-")]
    if len(operator_rows) < 8:
        failures.append(f"expected at least 8 operator sequence rows, found {len(operator_rows)}")

    result = {
        "gate": "project_group_real_execution_completion_gap_matrix_20260626",
        "status": "fail" if failures else "pass",
        "requirement_count": 7,
        "coverage_controlled_count": 7 if not failures else len(coverage_rows),
        "execution_complete_count": 0,
        "remaining_gap_count": 7,
        "failures": failures,
        "warnings": [
            "This validates the completion gap matrix only; it does not execute tasks, grant authorization, stage, commit, push, deploy, release, sync KDS API, or grant accepted/integrated/customer acceptance."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
