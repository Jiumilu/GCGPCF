#!/usr/bin/env python3
"""Validate the GlobalCloud project-group local skill chain registry."""

from __future__ import annotations

from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "config/project-group-skill-chain.yaml"
PROJECT_REGISTRY = ROOT / "config/project-group-projects.yaml"
PROJECTS_DIR = ROOT / "projects"
SKILLS_ROOT = ROOT / ".codex/skills"
ORCHESTRATOR_SKILL = SKILLS_ROOT / "globalcloud-loop-orchestrator" / "SKILL.md"
FEATURE_WORKSPACE_VALIDATOR = ROOT / "tools/kds-sync/validate_gpcf_2_feature_workspace.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_project_group_skill_chain: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    registry = yaml.safe_load(read(REGISTRY))
    project_registry = yaml.safe_load(read(PROJECT_REGISTRY))
    require(registry.get("schema_version") == 1, "schema_version must be 1")

    skills = registry.get("skills")
    require(isinstance(skills, list) and skills, "skills list must be non-empty")

    default_entry = registry.get("default_entry")
    names = [str(item.get("name", "")).strip() for item in skills]
    require(len(names) == len(set(names)), "skill names must be unique")
    require(default_entry in names, "default_entry must exist in registry")

    actual_dirs = sorted(path.name for path in SKILLS_ROOT.iterdir() if path.is_dir())
    require(sorted(names) == actual_dirs, "registry names must match local skill directories")

    declared_project_count = int(project_registry.get("current_project_count", 0))
    project_registry_slugs = sorted(str(item["slug"]) for item in project_registry.get("projects", []))
    actual_project_dirs = sorted(path.name for path in PROJECTS_DIR.iterdir() if path.is_dir())
    require(declared_project_count == len(project_registry_slugs), "project registry count mismatch")
    require(project_registry_slugs == actual_project_dirs, "project registry slugs must match projects directory")

    roles = set()
    for item in skills:
        name = str(item["name"])
        path = ROOT / str(item["path"])
        role = str(item.get("role", "")).strip()
        require(role, f"skill role missing: {name}")
        require(role not in roles, f"duplicate skill role: {role}")
        roles.add(role)

        required_files = item.get("required_files", [])
        require(isinstance(required_files, list) and required_files, f"required_files missing: {name}")
        for relative in required_files:
            require((path / relative).exists(), f"missing required file for {name}: {relative}")

        skill_text = read(path / "SKILL.md")
        require(f"name: {name}" in skill_text, f"SKILL.md name mismatch: {name}")

        if item.get("agent_manifest"):
            agent_text = read(path / "agents/openai.yaml")
            require("display_name:" in agent_text, f"agent manifest missing display_name: {name}")
            require(
                "short_description:" in agent_text or "default_prompt:" in agent_text,
                f"agent manifest missing short_description/default_prompt: {name}",
            )

    orchestrator = next(item for item in skills if item["name"] == "globalcloud-loop-orchestrator")
    downstream_skills = orchestrator.get("downstream_skills", [])
    require(isinstance(downstream_skills, list) and downstream_skills, "orchestrator downstream_skills missing")
    for downstream in downstream_skills:
        require(downstream in names, f"orchestrator downstream skill not registered: {downstream}")

    coverage = registry.get("project_coverage")
    require(isinstance(coverage, dict), "project_coverage missing")
    require(int(coverage.get("current_project_count", 0)) == declared_project_count, "project_coverage count mismatch")
    default_required_skills = coverage.get("default_required_skills", [])
    require(isinstance(default_required_skills, list) and default_required_skills, "default_required_skills missing")
    for skill in default_required_skills:
        require(skill in names, f"default_required_skill not registered: {skill}")

    projects = coverage.get("projects", [])
    require(isinstance(projects, list) and projects, "project coverage projects missing")
    coverage_slugs = sorted(str(item["slug"]) for item in projects)
    require(coverage_slugs == project_registry_slugs, "project coverage slugs must match project registry")
    for item in projects:
        slug = str(item["slug"])
        required_skills = item.get("required_skills", [])
        require(isinstance(required_skills, list) and required_skills, f"required_skills missing for project: {slug}")
        for skill in default_required_skills:
            require(skill in required_skills, f"default required skill {skill} missing for project: {slug}")
        for skill in required_skills:
            require(skill in names, f"project {slug} references unregistered skill: {skill}")

    orchestrator_text = read(ORCHESTRATOR_SKILL)
    for phrase in [
        "config/project-group-skill-chain.yaml",
        "validate_project_group_skill_chain.py",
        "globalcloud-document-governance",
        "globalcloud-project-group-git-clean",
        "globalcloud-ui-quality-gate",
        "globalcloud-openspec-governance",
    ]:
        require(phrase in orchestrator_text, f"orchestrator skill missing phrase: {phrase}")

    workspace_validator = read(FEATURE_WORKSPACE_VALIDATOR)
    for phrase in [
        "config/project-group-skill-chain.yaml",
        "validate_project_group_skill_chain.py",
        "globalcloud-openspec-governance",
    ]:
        require(phrase in workspace_validator, f"feature workspace validator missing phrase: {phrase}")

    print(
        "project_group_skill_chain=pass "
        f"default_entry={default_entry} "
        f"registered_skills={len(names)} "
        f"actual_skills={len(actual_dirs)} "
        f"covered_projects={len(coverage_slugs)} "
        "orchestrator_chain=validated"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
