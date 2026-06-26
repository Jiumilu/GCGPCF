#!/usr/bin/env python3
"""Validate the Wave 1 execution command pack evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-wave1-execution-command-pack-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"

PACKS = [
    "WAVE1-WAES-LINT-RUNTIME-001",
    "WAVE1-GFIS-REAL-SOR-001",
    "WAVE1-GPC-EXTERNAL-RUNTIME-001",
    "WAVE1-BRAIN-HUMAN-REVIEW-001",
    "WAVE1-GPCF-POST-SCHEME-REVIEW-001",
]

REQUIRED_TOKENS = [
    "project_group_wave1_execution_command_pack_20260626 = controlled",
    "wave = 1",
    "command_pack_count = 5",
    "authorization_required_count = 5",
    "action_executed_count = 0",
    "WAES -> XWAIL -> AaaS",
    "GFIS/GPC/PVAOS -> SCaaS",
    "KDS -> Brain",
    "GPCF -> all projects",
    "validate_project_group_current_state_baseline_refresh_20260626.py",
    "loop_document_gate.py",
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
            failures.append(f"missing token in Wave 1 command pack: {token}")

    for pack in PACKS:
        if pack not in doc:
            failures.append(f"missing Wave 1 pack: {pack}")

    for token in FORBIDDEN_TOKENS:
        if token in doc:
            failures.append(f"forbidden positive claim in Wave 1 command pack: {token}")

    if "globalcloud-project-group-wave1-execution-command-pack-20260626.md" not in board:
        failures.append("governance board missing Wave 1 command pack reference")

    result = {
        "gate": "project_group_wave1_execution_command_pack_20260626",
        "status": "pass" if not failures else "fail",
        "command_pack_count": len(PACKS),
        "failures": failures,
        "warnings": [
            "This validates Wave 1 command pack coverage only; it does not execute tasks, modify source code, stage, commit, push, deploy, sync KDS API, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
