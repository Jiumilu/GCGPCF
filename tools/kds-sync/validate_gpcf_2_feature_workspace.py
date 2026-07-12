#!/usr/bin/env python3
"""Validate the GPCF 2.0 Feature Workspace baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from gpcf_feature_lib import read_feature  # noqa: E402


PROJECTS = [
    "aaas",
    "brain",
    "was",
    "xiaoc",
    "waes",
    "gpc",
    "studio",
    "gpcf",
    "xwail",
    "gfis",
    "mmc",
    "kds",
    "xiaog",
    "pvaos",
    "sop",
    "pkc",
    "xgd",
    "icp",
]

FEATURE_FIELDS = [
    "id",
    "name",
    "project",
    "status",
    "goal",
    "owner",
    "priority",
    "scope",
    "acceptance",
    "loop",
    "evidence",
    "blockers",
    "created_at",
    "updated_at",
]

EVIDENCE_FIELDS = ["tests", "build", "screenshots", "api", "summary"]
EVIDENCE_STATUS = {"pending", "pass", "fail", "waived", "not_required"}
SCRIPTS = [
    "scripts/gpcf_new_feature.py",
    "scripts/gpcf_dispatch.py",
    "scripts/gpcf_run_loop.py",
    "scripts/gpcf_check_evidence.py",
    "scripts/gpcf_close_feature.py",
    "tools/kds-sync/validate_project_group_skill_chain.py",
    "tools/kds-sync/validate_project_group_ui_engineering_coverage.py",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_gpcf_2_feature_workspace: {message}")


def read(path: str) -> str:
    full = ROOT / path
    require(full.exists(), f"missing file: {path}")
    return full.read_text(encoding="utf-8", errors="ignore")


def validate_feature_dir(path: Path) -> None:
    required = ["feature.yaml", "journal.md", "evidence", "artifacts"]
    for item in required:
        require((path / item).exists(), f"feature missing {item}: {path.relative_to(ROOT)}")
    context_items = [item.name for item in path.iterdir() if not item.name.startswith(".")]
    require(len(context_items) <= 4, f"feature context exceeds 4 items: {path.relative_to(ROOT)}")
    data = read_feature(path / "feature.yaml")
    for field in FEATURE_FIELDS:
        require(field in data, f"feature.yaml missing field {field}: {path.relative_to(ROOT)}")
    for field in EVIDENCE_FIELDS:
        require(field in data["evidence"], f"feature.yaml missing evidence field {field}: {path.relative_to(ROOT)}")
        require(
            str(data["evidence"][field]) in EVIDENCE_STATUS,
            f"unsupported evidence status {field}={data['evidence'][field]}: {path.relative_to(ROOT)}",
        )
    journal = (path / "journal.md").read_text(encoding="utf-8", errors="ignore")
    for phrase in ["这轮做什么", "改了什么", "怎么验证", "发现什么问题", "是否可以提交"]:
        require(phrase in journal, f"journal missing five-question loop phrase: {phrase}")


def main() -> int:
    for directory in [
        "docs/architecture",
        "docs/standards",
        "docs/governance",
        "features/active",
        "features/done",
        "features/archived",
        "loops",
        "runtime/logs",
    ]:
        require((ROOT / directory).is_dir(), f"missing directory: {directory}")

    for project in PROJECTS:
        for filename in ["ROADMAP.md", "STATUS.md", "RISK.md"]:
            require((ROOT / "projects" / project / filename).exists(), f"missing project rhythm file: {project}/{filename}")

    for script in SCRIPTS:
        text = read(script)
        for forbidden in ["git commit", "git push", "kubectl", "vercel deploy", "real KDS API authorized"]:
            require(forbidden not in text, f"script contains forbidden boundary phrase: {script}: {forbidden}")
    evidence_script = read("scripts/gpcf_check_evidence.py")
    require("not_required" not in evidence_script, "evidence gate must not default to not_required")
    for phrase in ["py_compile", "git\", \"diff\", \"--check", "UI evidence required", "API evidence required"]:
        require(phrase in evidence_script, f"evidence gate missing project-profile check: {phrase}")

    for path in ["loops/execution_loop.md", "loops/review_loop.md", "loops/repair_loop.md"]:
        text = read(path)
        require("Feature" in text or "Evidence" in text or "Repair" in text, f"loop doc missing GPCF 2.0 content: {path}")

    runtime_queue = json.loads(read("runtime/queue.json"))
    runtime_state = json.loads(read("runtime/state.json"))
    require(runtime_queue.get("schema_version") == "2.0", "runtime/queue.json schema_version must be 2.0")
    require(runtime_state.get("mode") == "feature_delivery", "runtime/state.json mode must be feature_delivery")
    require(isinstance(runtime_queue.get("queue"), list), "runtime/queue.json queue must be a list")
    queued_ids = {entry.get("id") for entry in runtime_queue.get("queue", [])}
    entries_by_id = {entry.get("id"): entry for entry in runtime_queue.get("queue", [])}
    for role in ["Dispatcher", "Planner", "Builder", "Evaluator", "Repair", "Recorder"]:
        require(role in runtime_state.get("roles", []), f"runtime/state.json missing role: {role}")
    require("F-002" in entries_by_id, "runtime queue must keep F-002 close history")
    require(entries_by_id["F-002"].get("status") == "closed", "F-002 must be closed in runtime queue")
    require(entries_by_id["F-002"].get("current_role") == "Recorder", "F-002 must end at Recorder")
    require("F-003" in entries_by_id, "runtime queue must keep F-003 close history")
    require(entries_by_id["F-003"].get("status") == "closed", "F-003 must be closed in runtime queue")
    require(entries_by_id["F-003"].get("current_role") == "Recorder", "F-003 must end at Recorder")
    require("F-005" in entries_by_id, "runtime queue must include F-005 business chain sample")
    require(entries_by_id["F-005"].get("current_role") == "Recorder", "F-005 must reach Recorder")
    require((ROOT / "runtime/logs/F-002.jsonl").exists(), "missing runtime log for F-002")
    f002_log = read("runtime/logs/F-002.jsonl")
    for phrase in ["Recorder", "closed", "Evidence Gate"]:
        require(phrase in f002_log, f"F-002 runtime log missing phrase: {phrase}")
    f005_log = read("runtime/logs/F-005.jsonl")
    for role in ["Dispatcher", "Planner", "Builder", "Evaluator", "Repair", "Recorder"]:
        require(f'"role": "{role}"' in f005_log, f"F-005 runtime log missing role: {role}")

    implementation = read("docs/governance/gpcf-2-implementation.md")
    inventory = read("docs/governance/gpcf-2-governance-file-inventory.md")
    skill_chain_registry = read("config/project-group-skill-chain.yaml")
    ui_master_plan = read("04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md")
    for phrase in [
        "Program 定方向",
        "Project 管节奏",
        "Feature 做交付",
        "Loop 只服务执行",
        "Evidence 只保留结果",
        "Feature -> Workspace -> Loop -> Evidence -> Merge",
    ]:
        require(phrase in implementation, f"implementation doc missing phrase: {phrase}")
    for phrase in ["高频使用", "低频使用", "无效使用", "保留", "降级", "归档", "待删除"]:
        require(phrase in inventory, f"governance inventory missing category: {phrase}")
    for phrase in [
        "default_entry: globalcloud-loop-orchestrator",
        "globalcloud-document-governance",
        "globalcloud-project-group-git-clean",
        "globalcloud-ui-quality-gate",
        "globalcloud-openspec-governance",
        "ui-ux-pro-max",
    ]:
        require(phrase in skill_chain_registry, f"skill-chain registry missing phrase: {phrase}")
    for phrase in ["AAAS", "XWAIL", "SOP", "ICP"]:
        require(phrase in ui_master_plan, f"UI master plan missing project coverage phrase: {phrase}")

    combined = "\n".join(
        [
            read("AGENTS.md"),
            read("README.md"),
            read("02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md"),
            read("02-governance/loop/LOOP_EXECUTION_RULES.md"),
            read(".codex/skills/globalcloud-loop-orchestrator/SKILL.md"),
            read("tools/kds-sync/loop_document_gate.py"),
            read("tools/kds-sync/validate_project_group_skill_chain.py"),
            read("tools/kds-sync/validate_project_group_ui_engineering_coverage.py"),
        ]
    )
    for phrase in [
        "python scripts/gpcf_new_feature.py",
        "python scripts/gpcf_close_feature.py",
        "gpcf_dispatch.py",
        "Feature 做交付",
        "validate_gpcf_2_feature_workspace.py",
        "config/project-group-skill-chain.yaml",
        "validate_project_group_skill_chain.py",
        "validate_project_group_ui_engineering_coverage.py",
    ]:
        require(phrase in combined, f"GPCF 2.0 rule not propagated: {phrase}")

    feature_dirs = [
        path
        for base in [ROOT / "features/active", ROOT / "features/done", ROOT / "features/archived"]
        for path in base.iterdir()
        if path.is_dir() and path.name.startswith("F-")
    ]
    active_feature_dirs = [path for path in (ROOT / "features/active").iterdir() if path.is_dir() and path.name.startswith("F-")]
    done_feature_dirs = [path for path in (ROOT / "features/done").iterdir() if path.is_dir() and path.name.startswith("F-")]
    require(len(active_feature_dirs) >= 2, "GPCF 2.0 must keep at least 2 active Feature samples after closing one")
    require(any(path.name.startswith("F-002-") for path in done_feature_dirs), "F-002 must be closed into features/done")
    require(any(path.name.startswith("F-003-") for path in done_feature_dirs), "F-003 must be closed into features/done")
    for path in feature_dirs:
        validate_feature_dir(path)
        data = read_feature(path / "feature.yaml")
        if path.parent.name == "active":
            require(data["id"] in queued_ids, f"active feature missing runtime queue entry: {data['id']}")

    print(
        "gpcf_2_feature_workspace=pass "
        "feature_delivery_center=true "
        "project_scope=18 "
        "new_feature_entry=enabled "
        "close_feature_exit=enabled "
        "status_promotion_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
