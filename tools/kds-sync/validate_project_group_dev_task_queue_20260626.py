#!/usr/bin/env python3
"""Validate the 2026-06-26 GlobalCloud project-group dev task queue."""

from __future__ import annotations

import json
from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
TRIGGER_MAP = ROOT / "docs/harness/evidence/globalcloud-project-group-ready-for-review-trigger-map-20260627.md"

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
    "GlobalCloud 项目群开发态任务队列",
    "development_queue_ready = true",
    "project_count = 17",
    "trigger_layer_binding_count = 17",
    "dependency_edge_binding_count = 17",
    "开发态任务级 Trigger Layer / Dependency Edge 绑定",
    "| 项目 | trigger_layer | dependency_edge | authoritative_entry | 当前开发态入口含义 |",
    "pre_wave1_review_bridge",
    "authorization_to_pre_execution_total_bridge",
    "repair_authorization_boundary",
    "source_record_boundary",
    "external_runtime_boundary",
    "human_review_boundary",
    "environment_block_boundary",
    "local_release_review_boundary",
    "local_document_smoke_boundary",
    "authorization_pack_boundary",
    "local_dev_dryrun_boundary",
    "local_dev_smoke_boundary",
    "WAES -> XWAIL",
    "XWAIL -> AaaS",
    "KDS -> Brain",
    "GFIS/GPC/PVAOS -> SCaaS",
    "WAS -> Ontology -> XWAIL",
    "GPCF -> all projects",
    "PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES",
    "AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "AUTH-WAVE1-WAES-LINT-RUNTIME-20260626",
    "AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626",
    "AUTH-GFIS-SCHEME-REVIEW-20260626",
    "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
    "2026-06-28 live override",
    "当前项目群 Git gate 为 `partial`",
    "`GlobalCoud GPCF`、`GlobalCloud GFIS`、`GlobalCloud SOP`",
    "KDS 已从当前 dirty/sensitive 阻塞源移除",
    "KDS blocker 已解除并保持 clean",
    "sensitive_path=resolved_not_in_git_status",
    "GFIS-RUNTIME-SOP-E2E-MIN-001",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

FORBIDDEN_TOKENS = [
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
    doc_text = read(DOC, failures)
    refs_text = read(TASK_PACKS, failures) + "\n" + read(TRIGGER_MAP, failures)
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)

    for token in REQUIRED_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in dev task queue: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in doc_text:
            failures.append(f"forbidden positive claim in dev task queue: {token}")

    for project in PROJECTS:
        if project not in doc_text:
            failures.append(f"missing project in dev task queue: {project}")

    binding_rows = []
    p0_rows = []
    for line in doc_text.splitlines():
        if line.startswith("| P0 |"):
            p0_rows.append(line)
        if not line.startswith("|"):
            continue
        cols = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cols) == 5 and cols[0] in PROJECTS:
            binding_rows.append(cols)

    if len(binding_rows) != 17:
        failures.append(f"dev task queue binding rows must be 17, found {len(binding_rows)}")
    if len(p0_rows) != 17:
        failures.append(f"dev task queue P0 rows must be 17, found {len(p0_rows)}")

    for cols in binding_rows:
        project, trigger_layer, dependency_edge, authoritative_entry, note = cols
        if not trigger_layer.startswith("`") or not trigger_layer.endswith("`"):
            failures.append(f"binding trigger_layer must be explicit: {project}")
        if not dependency_edge.startswith("`") or not dependency_edge.endswith("`"):
            failures.append(f"binding dependency_edge must be explicit: {project}")
        if not authoritative_entry.startswith("`") or not authoritative_entry.endswith("`"):
            failures.append(f"binding authoritative_entry must be explicit: {project}")
        if not note or note == "-":
            failures.append(f"binding note must be non-empty: {project}")

    for token in [
        "globalcloud-project-group-next-executable-task-packs-20260625.md",
        "globalcloud-project-group-ready-for-review-trigger-map-20260627.md",
        "trigger_layer_count = 7",
        "task_row_count = 41",
    ]:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    result = {
        "gate": "project_group_dev_task_queue_20260626",
        "status": "pass" if not failures else "fail",
        "project_count": len(PROJECTS),
        "binding_row_count": len(binding_rows),
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates dev-task queue control only; it does not execute project tasks or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
