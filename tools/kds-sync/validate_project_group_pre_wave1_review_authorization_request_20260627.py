#!/usr/bin/env python3
"""Validate the pre-Wave1 review authorization bridge request."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-001.md"
POST_SCHEME_REQUEST = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md"
POST_SCHEME_LEDGER = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md"
POST_SCHEME_COMMAND_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-pre-execution-command-pack-20260626.md"
EXTERNAL_BASELINE = ROOT / "docs/harness/evidence/globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md"
OP_BLOCKERS = ROOT / "docs/harness/evidence/globalcloud-project-group-operational-blocker-resolution-matrix-20260626.md"
WAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-authorization-request-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

AUTH_IDS = [
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
]

REQUIRED_DOC_TOKENS = [
    "project_group_pre_wave1_review_authorization_request_20260627 = prepared",
    "task_id = GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "state_candidate = pre_wave1_review_authorization_ready",
    "review_boundary_count = 3",
    "review_boundary_repo_count = 3",
    "noise_cleanup_repo_count = 0",
    "authorization_granted_count = 0",
    "action_executed_count = 0",
    "wave1_entry_blocked_by_pre_review = true",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repos_current = GlobalCoud GPCF, GlobalCloud GFIS, GlobalCloud SOP",
    "noise_cleanup_repo_current = none",
    "KDS blocker resolved",
    "SOP delegated wrapper 单仓核对卡",
    "target_ledger = globalcloud-project-group-post-scheme-recognition-authorization-receipt-ledger-20260626.md",
    "expected_evidence = docs/harness/evidence/project-group-sop-loop-gate-delegate-review-receipt-*.md",
    "SOP delegated wrapper 确认后状态传导摘要",
    "receipt_recorded_for_auth = AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "allowed_state_propagation = sop_delegate_review_boundary_recorded_only",
    "历史 delegated wrapper 单仓核对卡仍保留在本文附录中",
    "`AAAS/XWAIL` delegated wrapper 单仓锚点已回退到各自主任务入口",
    "validate_project_group_post_scheme_recognition_authorization_receipt_ledger_20260626.py",
    "validate_project_group_post_scheme_recognition_pre_execution_command_pack_20260626.py",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "cleanup_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md",
    "globalcloud-project-group-wave1-authorization-request-20260626.md",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "pending_confirmation",
    "当前 active Pre-Wave1 review 边界只包含 `GPCF/GFIS/SOP` 三仓",
]

FORBIDDEN_TOKENS = [
    "authorization_granted = true",
    "action_executed = true",
    "wave1_entry_blocked_by_pre_review = false",
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "cleanup_allowed = true",
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
    loop = read(LOOP, failures)
    refs = "\n".join(
        [
            read(POST_SCHEME_REQUEST, failures),
            read(POST_SCHEME_LEDGER, failures),
            read(POST_SCHEME_COMMAND_PACK, failures),
            read(EXTERNAL_BASELINE, failures),
            read(OP_BLOCKERS, failures),
            read(WAVE1, failures),
            read(BOARD, failures),
            read(TASK_PACKS, failures),
        ]
    )

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc:
            failures.append(f"missing token in pre-wave1 request: {token}")

    for auth_id in AUTH_IDS:
        if auth_id not in doc:
            failures.append(f"pre-wave1 doc missing auth id: {auth_id}")
        if auth_id not in refs:
            failures.append(f"supporting references missing auth id: {auth_id}")

    auth_rows = [line for line in doc.splitlines() if line.startswith("| `AUTH-")]
    if len(auth_rows) != len(AUTH_IDS):
        failures.append("pre-wave1 bridge must have exactly 3 auth rows")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop:
            failures.append(f"missing loop section: {section}")

    combined = doc + "\n" + refs + "\n" + loop
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim in pre-wave1 bridge: {token}")

    result = {
        "gate": "project_group_pre_wave1_review_authorization_request_20260627",
        "status": "pass" if not failures else "fail",
        "review_boundary_count": len(AUTH_IDS),
        "authorization_granted_count": 0,
        "action_executed_count": 0,
        "wave1_entry_blocked_by_pre_review": True,
        "failures": failures,
        "warnings": [
            "This validates the pre-Wave1 review bridge only; it does not grant review, stage, commit, push, cleanup, Wave 1 execution, or accepted/integrated/customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
