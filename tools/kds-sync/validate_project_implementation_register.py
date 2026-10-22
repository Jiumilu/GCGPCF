#!/usr/bin/env python3
"""Validate the project implementation control register."""

from __future__ import annotations

import json
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-project-implementation-control-register.md"
MASTER_REGISTER = ROOT / "09-status/globalcloud-project-master-plan-control-register.md"

REGISTRY = yaml.safe_load((ROOT / "config/project-group-projects.yaml").read_text(encoding="utf-8"))
DISPLAY_NAMES = {"WAS": "WAS世界资产体系", "AAAS": "GlobalCloud AAAS / AaaS", "SpaceAIStudio": "GlobalCloud SpaceAI Studio"}
REQUIRED_PROJECTS = [
    DISPLAY_NAMES.get(str(item["id"]), f"GlobalCloud {item['id']}")
    for item in REGISTRY["projects"]
] + ["shared/python_utils"]

REQUIRED_TOKENS = [
    "GlobalCloud 项目群实施方案控制台账",
    "每个项目只能有一个当前有效实施方案",
    "实施状态必须由真实进度",
    "globalcloud-project-group-ready-for-review-trigger-map-20260627.md",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "| project | 当前有效总体方案 | 当前有效实施方案 | implementation_status | trigger_layer | 当前里程碑 | 证据 | 下一步 |",
    "semantic_mapping_boundary",
    "pre_wave1_review_bridge",
    "repair_authorization_boundary",
    "source_record_boundary",
    "external_runtime_boundary",
    "local_release_review_boundary",
    "human_review_boundary",
    "local_document_smoke_boundary",
    "local_dev_dryrun_boundary",
    "local_dev_smoke_boundary",
    "environment_block_boundary",
    "authorization_pack_boundary",
    "authorization_to_pre_execution_total_bridge",
    "not_project_boundary",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "implementation_plan_governance = repair_required_for_current_29_project_scope",
    "current_state_baseline_refresh_controlled = true",
    "development_queue_ready = true",
    "不得声明全部项目唯一实施方案已建立",
    "真实研发、运行、集成、交付和客户验收仍需逐项证据",
    "not_project",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    text = REGISTER.read_text(encoding="utf-8") if REGISTER.exists() else ""
    master_text = MASTER_REGISTER.read_text(encoding="utf-8") if MASTER_REGISTER.exists() else ""

    if not text:
        failures.append(f"missing register: {REGISTER}")
    if not master_text:
        failures.append(f"missing master plan register: {MASTER_REGISTER}")

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing token in implementation register: {token}")

    table = text.split("## 4. 项目实施方案盘点", 1)[-1].split("## 5. 当前结论", 1)[0]
    rows = [line.split("|")[1].strip() for line in table.splitlines() if line.startswith("| ") and not line.startswith("| ---")]
    for project in REQUIRED_PROJECTS:
        if rows.count(project) != 1:
            failures.append(f"expected exactly one project row in implementation register: {project}")

    if "project_master_plan_alignment = repair_required" in master_text:
        warnings.append("current project scope has unresolved master-plan candidates")

    result = {
        "gate": "project_implementation_register",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
