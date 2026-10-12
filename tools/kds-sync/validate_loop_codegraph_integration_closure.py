#!/usr/bin/env python3
"""Validate CodeGraph project-group integration closure evidence."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-integration-closure-audit-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-integration-closure-audit-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-INTEGRATION-CLOSURE-001.md"

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
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str]) -> str:
    completed = subprocess.run(args, text=True, capture_output=True, check=False)
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stderr}",
    )
    return completed.stdout


def parse_count(label: str, output: str) -> int:
    match = re.search(rf"{re.escape(label)}:\s+([0-9,.]+)", output)
    require(match is not None, f"CodeGraph status missing {label}")
    return int(match.group(1).replace(",", ""))


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    require(run(["codegraph", "--version"]).strip() == "1.0.1", "codegraph version must be 1.0.1")

    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-INTEGRATION-CLOSURE-AUDIT-20260621", "invalid evidence id")
    require(evidence.get("status") == "project_group_codegraph_integrated_with_sync_drift", "invalid status")
    require(evidence.get("project_group", {}).get("repo_count") == 13, "repo_count must be 13")
    require(evidence.get("project_group", {}).get("indexed_repo_count") == 13, "indexed_repo_count must be 13")
    require(evidence.get("project_group", {}).get("git_protected_repo_count") == 13, "git_protected_repo_count must be 13")
    require(evidence.get("project_group", {}).get("codegraph_git_status_entries_total") == 0, "codegraph git status entries must be 0")
    require(evidence.get("audit_policy", {}).get("ran_codegraph_sync") is False, "closure audit must not run sync")
    require(evidence.get("audit_policy", {}).get("modified_project_repositories") is False, "must not modify project repositories")
    require(evidence.get("audit_policy", {}).get("modified_business_code") is False, "must not modify business code")

    repos = evidence.get("repositories", [])
    require([repo.get("project") for repo in repos] == EXPECTED_PROJECTS, "repository order or names mismatch")

    codegraph_status_total = 0
    pending_sync = []
    for repo in repos:
        project = repo["project"]
        path = Path(repo["path"])
        require(path.exists(), f"{project} path missing")
        require((path / ".git").exists(), f"{project} missing .git")
        require((path / ".codegraph").exists(), f"{project} missing .codegraph")
        exclude = path / ".git/info/exclude"
        require(exclude.exists() and ".codegraph/" in exclude.read_text(encoding="utf-8"), f"{project} missing .codegraph exclude")

        git_status = run(["git", "-C", str(path), "status", "--short", "--", ".codegraph"]).strip()
        require(git_status == "", f"{project} .codegraph appears in git status: {git_status}")

        status = run(["codegraph", "status", str(path)])
        require(parse_count("Files", status) >= int(repo["files"]), f"{project} file count below closure snapshot")
        require(parse_count("Nodes", status) >= int(repo["nodes"]), f"{project} node count below closure snapshot")
        require(parse_count("Edges", status) >= int(repo["edges"]), f"{project} edge count below closure snapshot")
        codegraph_status_total += int(repo["codegraph_git_status_entries"])
        if repo.get("index_status") == "pending_sync":
            pending_sync.append(project)

    require(codegraph_status_total == 0, "aggregated codegraph git status entries must be 0")
    require(pending_sync == evidence.get("project_group", {}).get("pending_sync_projects"), "pending sync projects mismatch")

    for phrase in [
        "CodeGraph 在项目群和 Loop 工程中的部署集成",
        "GPCF-CODEGRAPH-SYNC-DRIFT-001",
        "业务代码修改",
        "本轮未运行 `codegraph sync`",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-SYNC-DRIFT-001"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for key, value in evidence.get("status_boundaries", {}).items():
        require(value is False, f"status boundary must be false: {key}")

    print(
        "loop_codegraph_integration_closure=pass "
        "evidence=LOOP-CODEGRAPH-INTEGRATION-CLOSURE-AUDIT-20260621 "
        "repo_count=13 indexed_repo_count=13 git_protected_repo_count=13 "
        "pending_sync_repo_count=4 codegraph_git_status_entries_total=0 "
        "ran_codegraph_sync=false project_internal_development=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
