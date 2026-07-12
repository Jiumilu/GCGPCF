#!/usr/bin/env python3
"""Validate project-group UI engineering coverage across all registered projects.

Validator entry: validate_project_group_ui_engineering_coverage.py
"""

from __future__ import annotations

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
PROJECT_REGISTRY = ROOT / "config/project-group-projects.yaml"
UI_MASTER_PLAN = ROOT / "04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md"
UI_GOVERNANCE_SPEC = ROOT / "04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md"
UI_SKILL = ROOT / ".codex/skills/globalcloud-ui-quality-gate/SKILL.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_project_group_ui_engineering_coverage: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_mapping_projects(text: str) -> list[str]:
    projects: list[str] = []
    capture = False
    for line in text.splitlines():
        if line.strip() == "| 项目 | 主类 | 副类 | 定位摘要 |":
            capture = True
            continue
        if not capture:
            continue
        if not line.startswith("|"):
            break
        if line.startswith("|---"):
            continue
        columns = [column.strip() for column in line.strip().strip("|").split("|")]
        if len(columns) >= 4:
            projects.append(columns[0])
    return projects


def main() -> int:
    registry = yaml.safe_load(read(PROJECT_REGISTRY))
    expected_projects = [str(project["id"]) for project in registry.get("projects", [])]
    require(len(expected_projects) == int(registry.get("current_project_count", 0)), "project registry count mismatch")

    ui_master_plan = read(UI_MASTER_PLAN)
    ui_governance_spec = read(UI_GOVERNANCE_SPEC)
    ui_skill = read(UI_SKILL)

    mapped_projects = extract_mapping_projects(ui_master_plan)
    require(len(mapped_projects) == len(expected_projects), "UI master plan mapping count mismatch")
    require(sorted(mapped_projects) == sorted(expected_projects), "UI master plan mapping projects mismatch")

    for phrase in [
        "项目群 UI 工程总控文件",
        "不同项目类型如何采用不同 UI 规范",
        "UI 质量如何在 Loop 中实际执行",
        "高风险页面类",
        "高风险组件类",
    ]:
        require(phrase in ui_master_plan, f"UI master plan missing phrase: {phrase}")

    for project in expected_projects:
        require(project in ui_master_plan, f"UI master plan missing project mapping: {project}")

    for phrase in [
        "ui_evidence_candidate",
        "G1 Surface Structure",
        "G9 Scope Control",
        "UI gate 为 `ui_ready` 也只代表 `ui_evidence_candidate`",
    ]:
        require(phrase in ui_governance_spec, f"UI governance spec missing phrase: {phrase}")

    for phrase in [
        "GlobalCloud项目群界面工程整体实施方案.md",
        "GlobalCloud项目群UI设计开发治理与评估统一规范.md",
        "WAES baseline reuse",
        "Tool route",
        "Design options",
    ]:
        require(phrase in ui_skill, f"UI skill missing phrase: {phrase}")

    print(
        "project_group_ui_engineering_coverage=pass "
        f"project_count={len(expected_projects)} "
        "ui_master_mapping=complete "
        "ui_governance_chain=validated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
