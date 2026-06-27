#!/usr/bin/env python3
"""Validate the next-stage authorization chain loop round."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md"
DECISION_BOARD = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md"
EXAMPLE_PACK = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md"
RECORDING_PROCEDURE = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md"
HUMAN_FILL = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md"
CHAIN_AUDIT = ROOT / "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md"

REQUIRED_TOKENS = [
    "loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001",
    "globalcloud-project-group-next-stage-authorization-decision-board-20260626.md",
    "globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md",
    "globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md",
    "globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md",
    "globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "7 项",
    "execution ledger",
    "post-scheme receipt ledger",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    loop_text = read(LOOP, failures)
    refs = "\n".join(
        [
            read(DECISION_BOARD, failures),
            read(EXAMPLE_PACK, failures),
            read(RECORDING_PROCEDURE, failures),
            read(HUMAN_FILL, failures),
            read(CHAIN_AUDIT, failures),
        ]
    )

    for token in REQUIRED_TOKENS:
        if token not in loop_text:
            failures.append(f"missing loop-round token: {token}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_text:
            failures.append(f"missing loop section: {section}")

    for auth_id in [
        "AUTH-WAS-DELETE-DS-STORE-20260626",
        "AUTH-KDS-SCHEME-REVIEW-20260626",
        "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
        "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
        "AUTH-GPCF-SCHEME-REVIEW-20260626",
        "AUTH-GFIS-SCHEME-REVIEW-20260626",
        "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    ]:
        if auth_id not in refs:
            failures.append(f"missing auth id in supporting refs: {auth_id}")

    result = {
        "gate": "project_group_next_stage_authorization_chain_loop_round_20260627",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "This validates loop-round structure only; it does not record authorization or execute any next-stage actions.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
