#!/usr/bin/env python3
"""Validate the project-group ready-for-review trigger map."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-ready-for-review-trigger-map-20260627.md"
QUEUE = ROOT / "docs/harness/evidence/globalcloud-project-group-ready-for-review-advancement-queue-20260626.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"

PROJECTS = [
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
]

REQUIRED_TOKENS = [
    "project_group_ready_for_review_trigger_map_20260627 = controlled",
    "project_count = 17",
    "trigger_layer_count = 7",
    "auto_ready_for_review_upgrade = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "pre_wave1_review_bridge",
    "authorization_to_pre_execution_total_bridge",
    "human_review_boundary",
    "local_release_review_boundary",
    "semantic_mapping_boundary",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc = read(DOC, failures)
    refs = "\n".join([read(QUEUE, failures), read(STATUS, failures), read(BOARD, failures)])

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing trigger map token: {token}")

    for project in PROJECTS:
        if project not in doc:
            failures.append(f"missing project row: {project}")

    for token in [
        "project_group_ready_for_review_advancement_queue_20260626 = controlled",
        "ready_for_review_advancement_queue_ready",
        "status_advancement_matrix = controlled",
    ]:
        if token not in refs:
            failures.append(f"missing prerequisite token: {token}")

    result = {
        "gate": "project_group_ready_for_review_trigger_map_20260627",
        "status": "pass" if not failures else "fail",
        "project_count": len(PROJECTS),
        "failures": failures,
        "warnings": [
            "This validates trigger-map structure only; it does not upgrade any project state or grant accepted/integrated/customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
