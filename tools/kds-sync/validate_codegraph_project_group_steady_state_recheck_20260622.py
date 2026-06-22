#!/usr/bin/env python3
"""Validate 2026-06-22 project-group CodeGraph steady-state recheck evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-project-group-steady-state-recheck-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-project-group-steady-state-recheck-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004.md"

REPOS = [
    ("gfis", "GlobalCloud GFIS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")),
    ("gpc", "GlobalCloud GPC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC")),
    ("pvaos", "GlobalCloud PVAOS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS")),
    ("waes", "GlobalCloud WAES", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES")),
    ("kds", "GlobalCloud KDS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")),
    ("brain", "GlobalCloud Brain", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain")),
    ("pkc", "GlobalCloud PKC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC")),
    ("xiaoc", "GlobalCloud XiaoC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC")),
    ("xgd", "GlobalCloud XGD", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD")),
    ("xiaog", "GlobalCloud XiaoG", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG")),
    ("mmc", "GlobalCloud MMC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")),
    ("gpcf", "GlobalCoud GPCF", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")),
    ("studio", "GlobalCloud Studio", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio")),
    ("was", "WAS世界资产体系", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系")),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def pending_total(pending: dict) -> int:
    return sum(int(pending.get(key, 0)) for key in ("added", "modified", "removed"))


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-20260622", "invalid evidence id")
    require(evidence["status"] == "steady_state_recheck_pass_with_watch", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004", "invalid scope")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005", "invalid next round")

    summary = evidence["summary"]
    require(summary["repo_count"] == 14, "repo count must be 14")
    require(summary["initialized_repo_count"] == 14, "initialized count must be 14")
    require(summary["codegraph_git_status_entries_total"] == 0, "git entries must be zero")
    require(summary["gfis_policy_exception_pending"] == 1, "GFIS policy exception must be one")
    require(summary["gpcf_pending_after_self_sync"] == 0, "GPCF must be synced after evidence generation")

    initialized_count = 0
    git_entries_total = 0
    live_pending: dict[str, int] = {}
    for repo_id, name, path in REPOS:
        status = run(["codegraph", "status", "--json", "."], cwd=path)
        require(status.returncode == 0, f"{name} codegraph status failed: {status.stderr}")
        live = json.loads(status.stdout)
        require(live.get("initialized") is True, f"{name} CodeGraph not initialized")
        require(live.get("version") == "1.0.1", f"{name} CodeGraph version mismatch")
        require(live.get("worktreeMismatch") is None, f"{name} worktree mismatch must be null")
        require((live.get("index") or {}).get("reindexRecommended") is False, f"{name} reindex must not be recommended")
        initialized_count += 1

        total = pending_total(live.get("pendingChanges") or {})
        live_pending[repo_id] = total
        if repo_id == "gfis":
            require(total == 1, "GFIS policy exception pending must remain one")
        if repo_id == "gpcf":
            require(total == 0, "GPCF pending must be zero after self-sync")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path)
        require(git_status.returncode == 0, f"{name} git status failed")
        entries = [line for line in git_status.stdout.splitlines() if line.strip()]
        require(entries == [], f"{name} .codegraph appears in git status")
        git_entries_total += len(entries)

    require(initialized_count == 14, "initialized count must be 14")
    require(git_entries_total == 0, "live .codegraph git entries must be zero")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "steady_state_recheck_pass_with_watch",
        "GlobalCloud Brain",
        "GlobalCloud KDS",
        "GlobalCloud GFIS",
        "Studio 在本轮 live recheck 为 pending=0",
        "不执行 Brain / KDS / GFIS / Studio sync",
        "GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "非声明"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_project_group_steady_state_recheck_20260622=pass_with_watch "
        f"repo_count=14 brain_pending={live_pending['brain']} "
        f"kds_pending={live_pending['kds']} studio_pending={live_pending['studio']} "
        f"gfis_pending={live_pending['gfis']} codegraph_git_entries=0 "
        "next=GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
