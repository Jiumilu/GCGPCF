#!/usr/bin/env python3
"""Validate the CodeGraph watchlist sync plan evidence."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-watchlist-sync-plan-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-watchlist-sync-plan-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001.md"
MONITOR_JSON = ROOT / "docs/harness/evidence/loop-codegraph-project-group-monitor-20260621.json"
POLICY = ROOT / "02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md"

WATCHLIST_PROJECTS = {
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
    "GlobalCoud GPCF": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF"),
}
POLICY_EXCEPTION_PROJECTS = {
    "GlobalCloud GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
}


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


def assert_repo_guard(name: str, path: Path, expected: dict[str, object], require_pending: bool = True) -> str:
    require(path.exists() and (path / ".git").exists(), f"{name} Git repo missing")
    require((path / ".codegraph").exists(), f"{name} .codegraph missing")
    exclude = path / ".git/info/exclude"
    require(exclude.exists() and ".codegraph/" in exclude.read_text(encoding="utf-8"), f"{name} missing .codegraph exclude")
    git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path).strip()
    require(git_status == "", f"{name} .codegraph appears in git status: {git_status}")
    status = run(["codegraph", "status", str(path)])
    index = expected["current_index"]
    require(parse_count("Files", status) >= int(index["files"]), f"{name} file count below evidence")
    require(parse_count("Nodes", status) >= int(index["nodes"]), f"{name} node count below evidence")
    require(parse_count("Edges", status) >= int(index["edges"]), f"{name} edge count below evidence")
    if require_pending:
        require("Pending Changes:" in status, f"{name} pending notice expected")
    return status


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    require(run(["codegraph", "--version"]).strip() == "1.0.1", "codegraph version must be 1.0.1")

    evidence = json.loads(read(EVIDENCE_JSON))
    monitor = json.loads(read(MONITOR_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    policy = read(POLICY)

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-WATCHLIST-SYNC-PLAN-20260621", "invalid evidence id")
    require(evidence.get("status") == "watchlist_sync_plan_defined", "invalid status")
    require(evidence.get("codegraph", {}).get("monitor_mode") == "read_only", "plan must be read-only")
    require(evidence.get("codegraph", {}).get("sync_executed_this_round") is False, "plan must not execute sync")
    require(monitor.get("project_group", {}).get("repo_count") == 13, "source monitor must cover 13 repos")

    watchlist = {item["project"]: item for item in evidence["watchlist"]}
    exceptions = {item["project"]: item for item in evidence["policy_exceptions"]}
    require(set(watchlist) == set(WATCHLIST_PROJECTS), "watchlist projects must be Brain, Studio, and GPCF")
    require(set(exceptions) == set(POLICY_EXCEPTION_PROJECTS), "policy exception must be GFIS only")

    for name, path in WATCHLIST_PROJECTS.items():
        assert_repo_guard(name, path, watchlist[name])
        require(watchlist[name]["decision"].startswith("defer_sync"), f"{name} must remain deferred")
        require(int(watchlist[name]["codegraph_git_status_entries"]) == 0, f"{name} .codegraph git entries must be 0")

    for name, path in POLICY_EXCEPTION_PROJECTS.items():
        assert_repo_guard(name, path, exceptions[name])
        require(exceptions[name]["decision"] == "keep_policy_exception_no_sync", f"{name} must remain no-sync policy exception")
        require(int(exceptions[name]["codegraph_git_status_entries"]) == 0, f"{name} .codegraph git entries must be 0")

    sync_plan = evidence["sync_plan"]
    require(sync_plan["authorized_projects_if_user_approves_next_round"] == list(WATCHLIST_PROJECTS), "authorized project list mismatch")
    require(sync_plan["excluded_projects"] == ["GlobalCloud GFIS"], "GFIS must be excluded")
    require("dirty worktree state" in sync_plan["risk_boundary"], "risk boundary must mention dirty worktree state")
    require("large_generated_validator_exception_candidate" in policy, "large-file policy missing GFIS exception")

    for key, value in evidence.get("status_boundaries", {}).items():
        require(value is False, f"status boundary must be false: {key}")

    for phrase in [
        "watchlist_sync_plan_defined",
        "本轮未执行 `codegraph sync`",
        "Brain、Studio、GPCF",
        "GFIS policy exception",
        "GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-001",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "不执行 `codegraph sync`"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "loop_codegraph_watchlist_sync_plan=pass "
        "evidence=LOOP-CODEGRAPH-WATCHLIST-SYNC-PLAN-20260621 "
        "watchlist=Brain,Studio,GPCF policy_exception=GFIS "
        "sync_executed=false next=GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
