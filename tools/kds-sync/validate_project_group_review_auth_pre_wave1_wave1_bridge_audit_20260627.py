#!/usr/bin/env python3
"""Validate the REVIEW-AUTH / Pre-Wave1 / Wave1 bridge audit."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-review-auth-pre-wave1-wave1-bridge-audit-20260627.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-REVIEW-AUTH-PRE-WAVE1-WAVE1-BRIDGE-001.md"
WORKTREE = ROOT / "docs/harness/evidence/globalcloud-project-group-review-auth-gpcf-worktree-confirmation-20260627.md"
RP7 = ROOT / "docs/harness/evidence/globalcloud-project-group-review-auth-gpcf-rp7-review-conclusion-20260627.md"
PRE_WAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md"
WAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-authorization-request-20260626.md"

REQUIRED_TOKENS = [
    "project_group_review_auth_pre_wave1_wave1_bridge_audit_20260627 = controlled",
    "bridge_status = review_auth_to_pre_wave1_to_wave1_order_confirmed",
    "review_auth_gpcf_worktree_status = blocked_by_live_git_gate_and_pending_user_confirmation",
    "review_auth_rp7_result = rework_required",
    "pre_wave1_review_authorization_status = pending_confirmation",
    "wave1_authorization_request_status = prepared",
    "wave1_entry_blocked_by_pre_review = true",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "REVIEW-AUTH-GPCF-WORKTREE-20260627",
    "GPCF-RP7",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "GPCF-WAVE1-AUTHORIZATION-REQUEST-20260626-001",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "单仓桥接锚点",
    "section = 5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "section = 5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "section = 5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "section = 5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc = read(DOC, failures)
    loop = read(LOOP, failures)
    refs = "\n".join(
        [
            read(WORKTREE, failures),
            read(RP7, failures),
            read(PRE_WAVE1, failures),
            read(WAVE1, failures),
        ]
    )

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing bridge audit token: {token}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop:
            failures.append(f"missing loop section: {section}")

    for token in [
        "review_auth_gpcf_worktree_confirmation_request = prepared",
        "rp7_review_result = rework_required",
        "project_group_pre_wave1_review_authorization_request_20260627 = prepared",
        "project_group_wave1_authorization_request_20260626 = prepared",
    ]:
        if token not in refs:
            failures.append(f"missing prerequisite token: {token}")

    result = {
        "gate": "project_group_review_auth_pre_wave1_wave1_bridge_audit_20260627",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "This validates bridge audit structure only; it does not grant review, authorization, stage, commit, push, or accepted/integrated/customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
