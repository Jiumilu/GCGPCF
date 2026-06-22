#!/usr/bin/env python3
"""Validate CodeGraph watchlist sync plan evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-watchlist-sync-plan-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-watchlist-sync-plan-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001.md"

REPOS = {
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
    "GlobalCloud GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
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


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-WATCHLIST-SYNC-PLAN-20260621", "invalid evidence id")
    require(evidence["status"] == "watchlist_sync_plan_ready", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001", "invalid scope")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-PACK-002", "invalid next round")
    require(evidence["global_rules"]["sync_without_authorization_allowed_for_brain_or_studio"] is False, "Brain/Studio sync must require authorization")
    require(
        evidence["global_rules"]["required_authorization_phrase"] == "授权执行 Brain/Studio CodeGraph watchlist sync-only closure",
        "authorization phrase mismatch",
    )

    watch = {item["repo"]: item for item in evidence["watchlist"]}
    require(set(watch) == set(REPOS), "watchlist repo set mismatch")

    live_pending: dict[str, int] = {}
    git_entries_total = 0
    for repo_name, repo_path in REPOS.items():
        status = run(["codegraph", "status", "--json", "."], cwd=repo_path)
        require(status.returncode == 0, f"{repo_name} codegraph status failed: {status.stderr}")
        live = json.loads(status.stdout)
        require(live.get("initialized") is True, f"{repo_name} CodeGraph not initialized")
        require(live.get("version") == "1.0.1", f"{repo_name} CodeGraph version mismatch")
        require(live.get("worktreeMismatch") is None, f"{repo_name} worktree mismatch must be null")
        require((live.get("index") or {}).get("reindexRecommended") is False, f"{repo_name} reindex must not be recommended")

        total = pending_total(live.get("pendingChanges") or {})
        live_pending[repo_name] = total
        if repo_name in {"GlobalCloud Brain", "GlobalCloud Studio"}:
            require(total >= 1, f"{repo_name} active drift must remain visible")
            require(watch[repo_name]["classification"] == "active_drift_action_required", f"{repo_name} classification mismatch")
            require(watch[repo_name]["next_action"] == "prepare_sync_authorization_pack", f"{repo_name} next action mismatch")
        elif repo_name == "GlobalCloud GFIS":
            require(total == 1, "GFIS policy exception pending must remain one")
            require(watch[repo_name]["classification"] == "policy_exception_watch", "GFIS classification mismatch")
        elif repo_name == "GlobalCoud GPCF":
            require(total <= 1, "GPCF governance pending must be at most one before final self-sync")
            require(watch[repo_name]["classification"] == "self_sync_clear", "GPCF classification mismatch")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=repo_path)
        require(git_status.returncode == 0, f"{repo_name} git status failed")
        entries = [line for line in git_status.stdout.splitlines() if line.strip()]
        require(entries == [], f"{repo_name} .codegraph appears in git status")
        git_entries_total += len(entries)

    require(git_entries_total == 0, ".codegraph git entries must be zero")
    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "GPCF-CODEGRAPH-WATCHLIST-SYNC-PLAN-001",
        "GlobalCloud Brain",
        "GlobalCloud Studio",
        "policy_exception_watch",
        "授权执行 Brain/Studio CodeGraph watchlist sync-only closure",
        "GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-PACK-002",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_watchlist_sync_plan=pass "
        f"brain_pending={live_pending['GlobalCloud Brain']} "
        f"studio_pending={live_pending['GlobalCloud Studio']} "
        f"gfis_pending={live_pending['GlobalCloud GFIS']} "
        "authorization_required=true "
        "next=GPCF-CODEGRAPH-WATCHLIST-SYNC-AUTHORIZATION-PACK-002"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
