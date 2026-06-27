#!/usr/bin/env python3
"""Validate the next-stage authorization package evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-package-20260627.md"
DECISION = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md"
EXAMPLE = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md"
PROCEDURE = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md"
FILL = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md"
CHAIN = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md"
ROUTING = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-routing-20260625.md"
PREWAVE1 = ROOT / "docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md"

AUTH_IDS = [
    "AUTH-WAS-DELETE-DS-STORE-20260626",
    "AUTH-KDS-SCHEME-REVIEW-20260626",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-GPCF-SCHEME-REVIEW-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
]

REQUIRED_TOKENS = [
    "GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001",
    "project_group_next_stage_authorization_package_20260627 = controlled",
    "next_stage_authorization_package_ready",
    "package_item_count | `7`",
    "execution_ledger_target_count | `1`",
    "post_scheme_ledger_target_count | `6`",
    "authorization_granted_count | `0`",
    "action_executed_count | `0`",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "review_boundary_repo_count | `6`",
    "noise_cleanup_repo_count | `1`",
    "review_boundary_repos_current | `GlobalCloud AAAS`、`GlobalCoud GPCF`、`GlobalCloud XWAIL`、`GlobalCloud GFIS`、`GlobalCloud KDS`、`GlobalCloud SOP`",
    "noise_cleanup_repo_current | `WAS世界资产体系(.DS_Store)`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "cleanup_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "单仓复核复用入口",
    "5.5.1 AAAS delegated wrapper 单仓核对卡",
    "5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡",
    "5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡",
    "5.6.3 SOP delegated wrapper 确认后状态传导摘要",
]

FORBIDDEN = [
    "authorization_granted = true",
    "action_executed = true",
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
    refs = "\n".join(
        [
            read(DECISION, failures),
            read(EXAMPLE, failures),
            read(PROCEDURE, failures),
            read(FILL, failures),
            read(CHAIN, failures),
            read(ROUTING, failures),
            read(PREWAVE1, failures),
        ]
    )

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing package token: {token}")

    for auth_id in AUTH_IDS:
        if auth_id not in doc:
            failures.append(f"missing auth id in package: {auth_id}")
        if auth_id not in refs:
            failures.append(f"missing auth id in refs: {auth_id}")

    combined = doc + "\n" + refs
    for token in FORBIDDEN:
        if token in combined:
            failures.append(f"forbidden positive claim found: {token}")

    result = {
        "gate": "project_group_next_stage_authorization_package_20260627",
        "status": "pass" if not failures else "fail",
        "package_item_count": len(AUTH_IDS),
        "execution_ledger_target_count": 1,
        "post_scheme_ledger_target_count": 6,
        "failures": failures,
        "warnings": [
            "This validates the next-stage authorization package only; it does not record authorization or execute any actions.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
