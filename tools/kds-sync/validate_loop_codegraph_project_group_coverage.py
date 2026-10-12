#!/usr/bin/env python3
"""Validate project-group CodeGraph coverage evidence."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.json"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-001.md"

REQUIRED_FRONTMATTER_KEYS = [
    "doc_id:",
    "title:",
    "project:",
    "related_projects:",
    "domain:",
    "status:",
    "version:",
    "owner:",
    "kds_space:",
    "kds_path:",
    "source_path:",
    "sync_direction:",
    "last_reviewed:",
    "supersedes:",
    "superseded_by:",
]

EXPECTED_PROJECTS = [
    "GlobalCloud Brain",
    "GlobalCloud GFIS",
    "GlobalCloud GPC",
    "GlobalCloud KDS",
    "GlobalCloud MMC",
    "GlobalCloud PKC",
    "GlobalCloud PVAOS",
    "GlobalCloud Studio",
    "GlobalCloud WAES",
    "GlobalCloud XGD",
    "GlobalCloud XiaoC",
    "GlobalCloud XiaoG",
    "GlobalCoud GPCF",
    "WAS 世界资产体系",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def run(args: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stderr}",
    )
    return completed.stdout


def frontmatter(path: Path, text: str) -> str:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    return text[:end]


def validate_controlled(path: Path, text: str, source_path: str) -> None:
    metadata = frontmatter(path, text)
    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in metadata, f"{path.relative_to(ROOT)} missing front matter key {key}")
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def parse_status(output: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for key in ["Files", "Nodes", "Edges", "DB Size"]:
        match = re.search(rf"{re.escape(key)}:\s+([0-9,.]+(?:\s+MB)?)", output)
        require(match is not None, f"CodeGraph status missing {key}")
        values[key] = match.group(1).replace(",", "")
    return values


def main() -> int:
    plan = read(PLAN)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    evidence = load_json(EVIDENCE_JSON)

    validate_controlled(PLAN, plan, "02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md")
    validate_controlled(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.md",
    )
    validate_controlled(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-001.md",
    )

    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    version = run(["codegraph", "--version"]).strip()
    require(version == "1.0.1", f"unexpected codegraph version: {version}")

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-PROJECT-GROUP-COVERAGE-20260620", "invalid evidence id")
    require(evidence.get("status") == "codegraph_project_group_indexed", "invalid evidence status")
    require(evidence.get("project_group", {}).get("repo_count") == 14, "repo_count must be 14")
    require(evidence.get("project_group", {}).get("studio_included") is True, "Studio must be included")
    require(evidence.get("project_group", {}).get("was_included") is True, "WAS must be included")
    require(evidence.get("codegraph", {}).get("mcp_install_executed") is False, "MCP install must be false")

    repositories = evidence.get("repositories", [])
    require(isinstance(repositories, list), "repositories must be a list")
    require(len(repositories) == 14, "repositories must include 14 entries")

    names = [repo.get("project") for repo in repositories]
    require(names == EXPECTED_PROJECTS, "repository order or names do not match expected project group")

    for repo in repositories:
        project = repo["project"]
        path = Path(repo["path"])
        require(path.exists(), f"{project} path missing: {path}")
        require((path / ".git").exists(), f"{project} missing .git")
        require((path / ".codegraph").exists(), f"{project} missing .codegraph")

        exclude = path / ".git/info/exclude"
        require(exclude.exists(), f"{project} missing git info exclude")
        require(".codegraph/" in exclude.read_text(encoding="utf-8"), f"{project} .codegraph not excluded")

        status_count = run(["git", "-C", str(path), "status", "--short", "--", ".codegraph"]).strip()
        require(status_count == "", f"{project} has tracked/untracked .codegraph status: {status_count}")

        status = run(["codegraph", "status", str(path)])
        parsed = parse_status(status)
        require(int(parsed["Files"]) > 0, f"{project} files must be positive")
        require(int(parsed["Nodes"]) > 0, f"{project} nodes must be positive")
        require(int(parsed["Edges"]) > 0, f"{project} edges must be positive")

        if project == "GlobalCloud Studio":
            require(repo.get("loop_context_detected") is True, "Studio loop context must be detected")
            require((path / "docs/harness/loops").exists(), "Studio loop directory missing")
        if project == "WAS 世界资产体系":
            require(int(parsed["Files"]) == int(repo["files"]), "WAS files mismatch")
            require(int(parsed["Nodes"]) == int(repo["nodes"]), "WAS nodes mismatch")
            require(int(parsed["Edges"]) == int(repo["edges"]), "WAS edges mismatch")
            require(repo.get("loop_context_detected") is True, "WAS loop context must be detected")
            require(repo.get("role") == "semantic_foundation_project", "WAS role mismatch")
            require(repo.get("remote") == "https://github.com/Jiumilu/GCWAS.git", "WAS remote mismatch")
            require(repo.get("was_validator_status") == "pass", "WAS validator status mismatch")
            require(repo.get("accepted") is False, "WAS must not be accepted")
            require(repo.get("integrated") is False, "WAS must not be integrated")
            require(repo.get("production_ready") is False, "WAS must not be production ready")
            require((path / "okf/validators/validate_all.py").exists(), "WAS validator missing")
            was_validation = run(["python3", "okf/validators/validate_all.py"], cwd=path)
            require("PASS validate_was_dimensions" in was_validation, "WAS validator did not pass")

    for phrase in [
        "GlobalCloud Studio",
        "WAS世界资产体系",
        "semantic_foundation_project",
        "project_group_repo_count | 14",
        "studio_included | true",
        "was_included | true",
        "不执行 `codegraph install`",
        "不修改 Agent MCP 配置",
        "不授权生产写入",
    ]:
        require(phrase in plan, f"coverage plan missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "studio_included=true"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "loop_codegraph_project_group_coverage=pass "
        "evidence=LOOP-CODEGRAPH-PROJECT-GROUP-COVERAGE-20260620 "
        "repo_count=14 studio_included=true was_included=true codegraph_version=1.0.1 "
        "mcp_install_executed=false codegraph_git_status_entries=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
