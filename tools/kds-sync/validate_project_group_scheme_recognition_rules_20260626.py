#!/usr/bin/env python3
"""Validate GlobalCloud project-group scheme recognition rules across repositories."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GPCF = ROOT / "GlobalCoud GPCF"
INDEX = GPCF / "02-governance/GlobalCloud 项目群方案体系识别规则.md"
MASTER_PLAN = GPCF / "01-architecture/GlobalCloud 项目群总体方案.md"
IMPLEMENTATION_PLAN = GPCF / "GlobalCloud 项目群实施方案.md"

PROJECT_FILES = {
    "GlobalCloud AAAS": (
        "AGENTS.md",
        "docs/GlobalCloud AaaS 总体方案.md",
        "docs/GlobalCloud AaaS 实施方案.md",
    ),
    "GlobalCloud Brain": (
        "AGENTS.md",
        "GlobalCloud Brain 总体方案.md",
        "GlobalCloud Brain 实施方案.md",
    ),
    "GlobalCloud GFIS": (
        "AGENTS.md",
        "GlobalCloud GFIS 总体方案.md",
        "GlobalCloud GFIS 实施方案.md",
    ),
    "GlobalCloud GPC": (
        "AGENTS.md",
        "GlobalCloud GPC 总体方案.md",
        "GlobalCloud GPC 实施方案.md",
    ),
    "GlobalCloud KDS": (
        "AGENTS.md",
        "GlobalCloud KDS 总体方案.md",
        "GlobalCloud KDS 实施方案.md",
    ),
    "GlobalCloud MMC": (
        "AGENTS.md",
        "GlobalCloud MMC 总体方案.md",
        "GlobalCloud MMC 实施方案.md",
    ),
    "GlobalCloud PKC": (
        "AGENTS.md",
        "GlobalCloud PKC 总体方案.md",
        "GlobalCloud PKC 实施方案.md",
    ),
    "GlobalCloud PVAOS": (
        "AGENTS.md",
        "GlobalCloud PVAOS 总体方案.md",
        "GlobalCloud PVAOS 实施方案.md",
    ),
    "GlobalCloud SOP": (
        "AGENTS.md",
        "GlobalCloud SOP 总体方案.md",
        "GlobalCloud SOP 实施方案.md",
    ),
    "GlobalCloud Studio": (
        "AGENTS.md",
        "GlobalCloud Studio 总体方案.md",
        "GlobalCloud Studio 实施方案.md",
    ),
    "GlobalCloud WAES": (
        "AGENTS.md",
        "GlobalCloud WAES 总体方案.md",
        "GlobalCloud WAES 实施方案.md",
    ),
    "GlobalCloud XGD": (
        "AGENTS.md",
        "GlobalCloud XGD 总体方案.md",
        "GlobalCloud XGD 实施方案.md",
    ),
    "GlobalCloud XWAIL": (
        "AGENTS.md",
        "GlobalCloud XWAIL 总体方案.md",
        "GlobalCloud XWAIL 实施方案.md",
    ),
    "GlobalCloud XiaoC": (
        "AGENTS.md",
        "GlobalCloud XiaoC 总体方案.md",
        "GlobalCloud XiaoC 实施方案.md",
    ),
    "GlobalCloud XiaoG": (
        "AGENTS.md",
        "GlobalCloud XiaoG 总体方案.md",
        "GlobalCloud XiaoG 实施方案.md",
    ),
    "GlobalCoud GPCF": (
        "AGENTS.md",
        "GlobalCloud GPCF 总体方案.md",
        "GlobalCloud GPCF 实施方案.md",
    ),
    "WAS世界资产体系": (
        "AGENTS.md",
        "docs/GlobalCloud WAS 总体方案.md",
        "docs/GlobalCloud WAS 实施方案.md",
    ),
}

AGENTS_TOKENS = [
    "GlobalCloud 项目群总控体系识别规则",
    "GlobalCloud 项目群总体方案体系",
    "GlobalCloud 项目群实施方案体系",
    "所有项目级总体方案必须继承项目群总体方案",
    "所有项目级实施方案必须继承项目群实施方案",
    "项目级方案变化必须回传项目群主方案",
    "accepted",
    "integrated",
    "production_ready",
    "customer_accepted",
]

PLAN_TOKENS = [
    "项目群主方案继承声明",
    "本项目总体方案继承《GlobalCloud 项目群总体方案》",
    "本项目实施方案继承《GlobalCloud 项目群实施方案》",
    "若本项目方案与项目群主方案冲突，以项目群主方案为准",
]

INDEX_TOKENS = [
    "project_group_scheme_recognition_rules = controlled",
    "agents_recognition_scope = 17 projects",
    "project_plan_inheritance_scope = 34 files",
    "GlobalCloud 项目群总体方案体系",
    "GlobalCloud 项目群实施方案体系",
    "GPCF:01-architecture/GlobalCloud 项目群总体方案.md",
    "GPCF:GlobalCloud 项目群实施方案.md",
]

MASTER_PLAN_TOKENS = [
    "project_group_master_plan = controlled",
    "project_group_implementation_plan = controlled",
    "scheme_recognition_scope = AGENTS.md + project master plans + project implementation plans",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(label: str, text: str, tokens: list[str], failures: list[str]) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{label} missing token: {token}")


def main() -> int:
    failures: list[str] = []
    index_text = read(INDEX, failures)
    master_text = read(MASTER_PLAN, failures)
    implementation_text = read(IMPLEMENTATION_PLAN, failures)

    require_tokens("scheme recognition index", index_text, INDEX_TOKENS, failures)
    require_tokens("project group master plan", master_text, MASTER_PLAN_TOKENS, failures)
    if "GlobalCloud 项目群实施方案" not in implementation_text:
        failures.append("project group implementation plan missing title token")

    agents_checked = 0
    plan_files_checked = 0
    for project, rels in PROJECT_FILES.items():
        repo = ROOT / project
        agents_rel, master_rel, implementation_rel = rels
        agents_text = read(repo / agents_rel, failures)
        require_tokens(f"{project} AGENTS.md", agents_text, AGENTS_TOKENS, failures)
        agents_checked += 1

        for rel in [master_rel, implementation_rel]:
            plan_text = read(repo / rel, failures)
            require_tokens(f"{project}/{rel}", plan_text, PLAN_TOKENS, failures)
            plan_files_checked += 1

    result = {
        "gate": "project_group_scheme_recognition_rules_20260626",
        "status": "pass" if not failures else "fail",
        "agents_checked": agents_checked,
        "project_plan_files_checked": plan_files_checked,
        "failures": failures,
        "warnings": [
            "This validates session-entry recognition and plan inheritance only; it does not execute project tasks, stage, commit, push, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
