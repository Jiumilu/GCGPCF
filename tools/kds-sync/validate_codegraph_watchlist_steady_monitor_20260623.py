#!/usr/bin/env python3
"""Validate CodeGraph watchlist steady monitor evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-watchlist-steady-monitor-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020.md"

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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def git_dirty_counts(repo: Path) -> dict[str, int]:
    result = run(["git", "status", "--short"], cwd=repo)
    require(result.returncode == 0, f"git status failed: {repo}: {result.stderr}")
    counts = {"total": 0, "modified": 0, "deleted": 0, "untracked": 0, "renamed": 0, "other": 0}
    for line in result.stdout.splitlines():
        counts["total"] += 1
        code = line[:2]
        if code == "??":
            counts["untracked"] += 1
        elif "D" in code:
            counts["deleted"] += 1
        elif "R" in code:
            counts["renamed"] += 1
        elif "M" in code:
            counts["modified"] += 1
        else:
            counts["other"] += 1
    return counts


def pending_total(pending: dict[str, int]) -> int:
    return sum(int(pending.get(key, 0)) for key in ("added", "modified", "removed"))


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-WATCHLIST-STEADY-MONITOR-20260623", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020", "invalid scope")
    require(evidence["status"] == "watch_required", "invalid status")
    require(evidence["previous_round"] == "GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019", "invalid previous round")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-WATCHLIST-MONITOR-006", "invalid next round")

    summary = evidence["summary"]
    require(summary["repo_count"] == 14, "repo count must be 14")
    require(summary["initialized_repo_count"] == 14, "initialized count must be 14")
    require(summary["codegraph_git_status_entries_total"] == 0, "git entries must be zero")
    require(summary["review_rework_count"] == 0, "review rework count baseline must be zero")
    require(summary["gpcf_pending_before_self_sync"] == 3, "GPCF pre-sync pending must be 3")
    require(summary["gpcf_pending_after_self_sync"] == 0, "GPCF pending after self-sync must be zero")
    require(summary["status_ceiling"] == "watch_required", "status ceiling must be watch_required")

    repo_status = {item["repo_id"]: item for item in evidence["repo_status"]}
    require(set(repo_status) == {repo_id for repo_id, _, _ in REPOS}, "repo status set mismatch")

    live_pending: dict[str, int] = {}
    for repo_id, name, path in REPOS:
        status = run(["codegraph", "status", "--json", "."], cwd=path)
        require(status.returncode == 0, f"{name} codegraph status failed: {status.stderr}")
        live = json.loads(status.stdout)
        require(live.get("initialized") is True, f"{name} CodeGraph not initialized")
        require(live.get("version") == "1.0.1", f"{name} CodeGraph version mismatch")
        require(live.get("worktreeMismatch") is None, f"{name} worktree mismatch must be null")
        require((live.get("index") or {}).get("reindexRecommended") is False, f"{name} reindex must not be recommended")

        pending = live.get("pendingChanges") or {}
        total = pending_total(pending)
        live_pending[repo_id] = total
        expected_pending = repo_status[repo_id]["pending"]
        if repo_id == "gpcf":
            require(total > 0, f"{name} pending must remain watchable: {pending}")
        else:
            require(pending == expected_pending, f"{name} pending mismatch")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path)
        require(git_status.returncode == 0, f"{name} .codegraph git status failed: {git_status.stderr}")
        require(git_status.stdout.strip() == "", f"{name} .codegraph must remain git-isolated")

        counts = git_dirty_counts(path)
        expected_dirty = repo_status[repo_id]["git_dirty"]
        if repo_id == "gpcf":
            require(counts["total"] > 0, f"{name} git dirty must remain watchable: {counts}")
            require(counts["total"] >= expected_dirty["total"] - 20, f"{name} git dirty drift too far from evidence: {counts}")
        elif repo_id == "kds":
            require(counts["total"] > 0, f"{name} git dirty must remain watchable: {counts}")
            require(counts["total"] >= expected_dirty["total"] - 20, f"{name} git dirty drift too far from evidence: {counts}")
        else:
            require(counts == expected_dirty, f"{name} git dirty mismatch: {counts}")

    for item in evidence["watch_items"]:
        require(item["repo"] in {name for _, name, _ in REPOS}, f"unexpected watch item repo: {item['repo']}")

    governance = evidence["governance"]
    require(governance["mode"] == "watchlist_steady_monitor", "invalid governance mode")
    require(governance["codegraph_sync_performed_in_watchlist_repos"] is False, "watchlist sync must not be performed")
    require(governance["clean_reindex_performed"] is False, "clean reindex must not be performed")
    require(governance["business_development_performed"] is False, "business development must not be performed")
    require(governance["gpcf_self_sync_performed"] is True, "GPCF self-sync must be recorded")
    require(governance["codegraph_git_isolated"] is True, "codegraph git isolation must be true")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        require(section in evidence["five_direction"], f"missing five_direction section: {section}")
        require(f"## {section}" in loop_round, f"loop round missing section: {section}")

    for phrase in [
        "watch_required",
        "14 仓 CodeGraph 均可读",
        "review_rework_count=0",
        "KDS Git dirty 仍为",
        "Studio CodeGraph pending 为 `added=0, modified=18, removed=0`",
        "GPCF 当前 CodeGraph pending 为 `added=9, modified=21, removed=0`",
        "GPCF-CODEGRAPH-WATCHLIST-MONITOR-006",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    print(
        "codegraph_watchlist_steady_monitor=watch_required "
        f"brain_pending={live_pending['brain']} "
        f"gfis_pending={live_pending['gfis']} "
        f"kds_pending={live_pending['kds']} "
        f"studio_pending={live_pending['studio']} "
        f"gpcf_pending={live_pending['gpcf']} "
        "non_gpcf_sync_authorized=false "
        "review_rework_count=0 "
        "next=GPCF-CODEGRAPH-WATCHLIST-MONITOR-006"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
