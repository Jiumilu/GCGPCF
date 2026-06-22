#!/usr/bin/env python3
"""Validate 2026-06-22 CodeGraph watchlist threshold review evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-watchlist-threshold-review-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-watchlist-threshold-review-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005.md"

REPOS = {
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud KDS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"),
    "GlobalCloud GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
    "GlobalCoud GPCF": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF"),
}


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


def live_status(repo_name: str) -> dict:
    status = run(["codegraph", "status", "--json", "."], cwd=REPOS[repo_name])
    require(status.returncode == 0, f"{repo_name} codegraph status failed: {status.stderr}")
    live = json.loads(status.stdout)
    require(live.get("initialized") is True, f"{repo_name} CodeGraph not initialized")
    require(live.get("version") == "1.0.1", f"{repo_name} CodeGraph version mismatch")
    require(live.get("worktreeMismatch") is None, f"{repo_name} worktree mismatch must be null")
    require((live.get("index") or {}).get("reindexRecommended") is False, f"{repo_name} reindex must not be recommended")
    return live


def assert_codegraph_git_isolated(repo_name: str) -> int:
    git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=REPOS[repo_name])
    require(git_status.returncode == 0, f"{repo_name} git status failed")
    entries = [line for line in git_status.stdout.splitlines() if line.strip()]
    require(entries == [], f"{repo_name} .codegraph appears in git status")
    return len(entries)


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-20260622", "invalid evidence id")
    require(evidence["status"] == "watchlist_threshold_review_no_new_sync_authorization", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005", "invalid scope")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-WATCHLIST-MONITOR-006", "invalid next round")
    require(evidence["threshold_policy"]["sync_authorization_required_for_non_gpcf"] is True, "non-GPCF sync must require authorization")
    require(evidence["summary"]["non_gpcf_sync_authorized"] is False, "non-GPCF sync must not be authorized")
    require(evidence["summary"]["gpcf_pending_after_self_sync"] == 0, "GPCF after self-sync must be zero")

    review = {item["repo"]: item for item in evidence["live_review"]}
    require(set(review) == set(REPOS), "live review repo set mismatch")

    live_pending: dict[str, int] = {}
    git_entries_total = 0
    for repo_name in REPOS:
        live = live_status(repo_name)
        pending = live.get("pendingChanges") or {}
        total = pending_total(pending)
        live_pending[repo_name] = total
        git_entries_total += assert_codegraph_git_isolated(repo_name)

        if repo_name == "GlobalCloud Brain":
            require(int(pending.get("added", 0)) == 0, "Brain added drift would require action")
            require(int(pending.get("removed", 0)) == 0, "Brain removed drift would require action")
            require(total <= 5, "Brain crossed action threshold")
            require(review[repo_name]["threshold_result"] == "watch", "Brain threshold result mismatch")
            require(review[repo_name]["decision"] == "no_new_sync_authorization", "Brain decision mismatch")
        elif repo_name == "GlobalCloud KDS":
            require(int(pending.get("added", 0)) == 0, "KDS added drift would require action")
            require(int(pending.get("removed", 0)) == 0, "KDS removed drift would require action")
            require(total <= 5, "KDS crossed action threshold")
            require(review[repo_name]["threshold_result"] == "watch", "KDS threshold result mismatch")
            require(review[repo_name]["decision"] == "no_sync", "KDS decision mismatch")
        elif repo_name == "GlobalCloud GFIS":
            require(total == 1, "GFIS policy exception pending must remain one")
            require(int(pending.get("added", 0)) == 1, "GFIS policy exception must remain added=1")
            require(review[repo_name]["threshold_result"] == "policy_exception_watch", "GFIS threshold result mismatch")
        elif repo_name == "GlobalCloud Studio":
            require(total == 0, "Studio must remain steady")
            require(review[repo_name]["threshold_result"] == "steady", "Studio threshold result mismatch")
        elif repo_name == "GlobalCoud GPCF":
            require(total == 0, "GPCF must be zero after self-sync")
            require(review[repo_name]["threshold_result"] == "self_sync_required_after_evidence", "GPCF threshold result mismatch")

    require(git_entries_total == 0, ".codegraph git entries must be zero")
    require(evidence["summary"]["codegraph_git_status_entries_total"] == 0, "evidence git entry total must be zero")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for phrase in [
        "watchlist_threshold_review_no_new_sync_authorization",
        "GlobalCloud Brain",
        "GlobalCloud KDS",
        "policy_exception_watch",
        "不执行 Brain / KDS / GFIS / Studio sync",
        "GPCF-CODEGRAPH-WATCHLIST-MONITOR-006",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "非声明"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_watchlist_threshold_review_20260622=pass "
        f"brain_pending={live_pending['GlobalCloud Brain']} "
        f"kds_pending={live_pending['GlobalCloud KDS']} "
        f"gfis_pending={live_pending['GlobalCloud GFIS']} "
        f"studio_pending={live_pending['GlobalCloud Studio']} "
        f"gpcf_pending={live_pending['GlobalCoud GPCF']} "
        "non_gpcf_sync_authorized=false "
        "next=GPCF-CODEGRAPH-WATCHLIST-MONITOR-006"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
