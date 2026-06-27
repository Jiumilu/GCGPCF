#!/usr/bin/env python3
"""Validate the Wave 1 authorization request evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-authorization-request-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"

AUTH_IDS = [
    "AUTH-WAVE1-WAES-LINT-RUNTIME-20260626",
    "AUTH-WAVE1-GFIS-REAL-SOR-20260626",
    "AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626",
    "AUTH-WAVE1-BRAIN-HUMAN-REVIEW-20260626",
    "AUTH-WAVE1-GPCF-POST-SCHEME-REVIEW-20260626",
]

REQUIRED_TOKENS = [
    "project_group_wave1_authorization_request_20260626 = prepared",
    "request_item_count = 5",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repo_count = 6",
    "noise_cleanup_repo_count = 1",
    "review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "allowed_scope",
    "forbidden_scope",
    "pre_execution_gate",
    "rollback_boundary",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md",
    "section = 5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "section = 5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "section = 5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "section = 5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "pending_confirmation",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
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
    doc = read(DOC, failures)
    board = read(BOARD, failures)

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing token in Wave 1 authorization request: {token}")

    for auth_id in AUTH_IDS:
        if auth_id not in doc:
            failures.append(f"missing Wave 1 auth id: {auth_id}")

    for token in FORBIDDEN_TOKENS:
        if token in doc:
            failures.append(f"forbidden positive claim in Wave 1 authorization request: {token}")

    if "globalcloud-project-group-wave1-authorization-request-20260626.md" not in board:
        failures.append("governance board missing Wave 1 authorization request reference")

    result = {
        "gate": "project_group_wave1_authorization_request_20260626",
        "status": "pass" if not failures else "fail",
        "request_item_count": len(AUTH_IDS),
        "failures": failures,
        "warnings": [
            "This validates Wave 1 authorization request structure only; it does not grant authorization, execute tasks, stage, commit, push, deploy, sync KDS API, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
