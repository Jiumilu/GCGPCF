#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md"

AUTH_IDS = [
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
]

REQUIRED_TOKENS = [
    "project_group_next_stage_authorization_decision_board_20260626 = prepared",
    "decision_item_count = 3",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "deploy_allowed = false",
    "release_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "如果用户只说“继续”或“下一步”，默认不视为授权执行当前 A-C 任一项",
    "globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md",
    "globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md",
    "globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md",
    "globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md",
    "globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md",
    "globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "wave1_entry_blocked_by_pre_review=true",
    "KDS blocker resolved",
    "SOP delegated wrapper",
    "最小核对单",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "post-scheme recognition authorization receipt ledger",
    "当前 active next-stage 授权项只包含 `GPCF/GFIS/SOP` 三项",
    "run",
    "stop",
    "verify",
    "recover",
    "debug",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "deploy_allowed = true",
    "release_allowed = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def main() -> int:
    failures: list[str] = []
    if not DOC.exists():
        failures.append(f"missing document: {DOC.relative_to(ROOT)}")
        text = ""
    else:
        text = DOC.read_text(encoding="utf-8")

    for auth_id in AUTH_IDS:
        if auth_id not in text:
            failures.append(f"missing auth id: {auth_id}")

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing required token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            failures.append(f"forbidden positive claim: {token}")

    result = {
        "gate": "project_group_next_stage_authorization_decision_board_20260626",
        "status": "fail" if failures else "pass",
        "decision_item_count": len(AUTH_IDS),
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "failures": failures,
        "warnings": [
            "This validates the next-stage authorization decision board only; it does not grant authorization, execute tasks, stage, commit, push, deploy, release, sync KDS API, or grant accepted/integrated/customer acceptance."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
