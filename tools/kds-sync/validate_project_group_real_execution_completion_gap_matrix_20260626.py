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
    "project_group_git_clean = partial",
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
