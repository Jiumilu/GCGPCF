#!/usr/bin/env python3
"""Validate CodeGraph project-group monitor evidence."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-MONITOR-001.md"
POLICY = ROOT / "02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md"

REPOS = [
    ("GlobalCloud Brain", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain")),
    ("GlobalCloud GFIS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")),
    ("GlobalCloud GPC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC")),
    ("GlobalCloud KDS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")),
    ("GlobalCloud MMC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")),
    ("GlobalCloud PKC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC")),
    ("GlobalCloud PVAOS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS")),
    ("GlobalCloud Studio", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio")),
    ("GlobalCloud WAES", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES")),
    ("GlobalCloud XGD", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD")),
    ("GlobalCloud XiaoC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC")),
    ("GlobalCloud XiaoG", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG")),
    ("GlobalCoud GPCF", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")),
    ("WAS世界资产体系", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系")),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    require(completed.returncode == 0, f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stderr}")
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
    policy = read(POLICY)

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-PROJECT-GROUP-MONITOR-20260621", "invalid evidence id")
    require(evidence.get("status") == "project_group_codegraph_monitor_pass_with_active_watchlist", "invalid status")
    require(evidence.get("codegraph", {}).get("monitor_mode") == "controlled_sync_followup", "monitor mode mismatch")
    require(evidence.get("codegraph", {}).get("sync_executed_this_round") is True, "monitor must record controlled sync follow-up")

    project_group = evidence["project_group"]
    require(project_group["repo_count"] == 14, "repo_count must be 14")
    require(project_group["indexed_repo_count"] == 14, "indexed_repo_count must be 14")
    require(project_group["git_protected_repo_count"] == 14, "git_protected_repo_count must be 14")
    require(project_group["codegraph_git_status_entries_total"] == 0, ".codegraph git entries must be 0")
    require(project_group["up_to_date_repo_count"] == 13, "up_to_date_repo_count must be 13")
    require(project_group["pending_sync_repo_count"] == 1, "pending_sync_repo_count must be 1")
    require(
        project_group["pending_sync_projects"] == ["GlobalCloud Studio"],
        "Studio must be the pending sync project",
    )
    require(project_group["policy_exception_projects"] == [], "GFIS policy exception must be cleared in current snapshot")

    repos = {repo["project"]: repo for repo in evidence["repositories"]}
    require(list(repos) == [name for name, _ in REPOS], "repository order mismatch")
    total_git_entries = 0
    for name, path in REPOS:
        require(path.exists() and (path / ".git").exists(), f"{name} Git repo missing")
        require((path / ".codegraph").exists(), f"{name} .codegraph missing")
        exclude = path / ".git/info/exclude"
        require(exclude.exists() and ".codegraph/" in exclude.read_text(encoding="utf-8"), f"{name} missing .codegraph exclude")
        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path).strip()
        require(git_status == "", f"{name} .codegraph appears in git status: {git_status}")
        total_git_entries += int(repos[name]["codegraph_git_status_entries"])
        status = run(["codegraph", "status", str(path)])
        require(parse_count("Files", status) >= int(repos[name]["files"]), f"{name} file count below evidence")
        require(parse_count("Nodes", status) >= int(repos[name]["nodes"]), f"{name} node count below evidence")
        require(parse_count("Edges", status) >= int(repos[name]["edges"]), f"{name} edge count below evidence")
        if repos[name]["index_status"] in {"pending_sync", "policy_exception"}:
            require("Pending Changes:" in status, f"{name} pending notice expected")
        else:
            require("Index is up to date" in status, f"{name} must be up to date")

    require(total_git_entries == 0, "aggregated .codegraph git entries must be 0")
    require("large_generated_validator_exception_candidate" in policy, "large file policy missing GFIS exception")
    for phrase in [
        "project_group_codegraph_monitor_pass_with_watchlist",
        "14 个仓库",
        "Brain green",
        "Studio watch",
        "GFIS green",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")
    for key, value in evidence.get("status_boundaries", {}).items():
        require(value is False, f"status boundary must be false: {key}")

    print(
        "loop_codegraph_project_group_monitor=pass "
        "evidence=LOOP-CODEGRAPH-PROJECT-GROUP-MONITOR-20260621 "
        "repo_count=14 git_protected_repo_count=14 "
        "watchlist=Studio policy_exception=none "
        "codegraph_git_status_entries_total=0 sync_executed=controlled_followup"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
