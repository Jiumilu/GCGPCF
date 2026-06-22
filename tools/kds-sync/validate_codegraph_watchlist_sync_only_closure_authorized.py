#!/usr/bin/env python3
"""Validate authorized CodeGraph watchlist sync-only closure evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-watchlist-sync-only-closure-authorized-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-watchlist-sync-only-closure-authorized-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-SYNC-ONLY-CLOSURE-003-AUTHORIZED.md"
AUTH_PACK_JSON = ROOT / "docs/harness/evidence/codegraph-watchlist-sync-authorization-pack-20260621.json"

SYNC_REPOS = {
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
}
WATCH_REPOS = {
    "GlobalCloud GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
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


def assert_codegraph_git_isolated(repo_name: str, repo_path: Path) -> None:
    git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=repo_path)
    require(git_status.returncode == 0, f"git status failed for {repo_name}")
    require(git_status.stdout.strip() == "", f"{repo_name} .codegraph must remain git-isolated")


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    auth_pack = json.loads(read(AUTH_PACK_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-WATCHLIST-SYNC-ONLY-CLOSURE-AUTHORIZED-20260622", "invalid evidence id")
    require(evidence["status"] == "sync_only_closure_completed", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-WATCHLIST-SYNC-ONLY-CLOSURE-003-AUTHORIZED", "invalid scope")
    require(auth_pack["status"] == "authorization_pack_ready", "authorization pack source mismatch")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004", "invalid next round")

    auth = evidence["authorization"]
    require(auth["required_phrase"] == "授权执行 Brain/Studio CodeGraph watchlist sync-only closure", "required phrase mismatch")
    require(auth["phrase_received"] is True, "authorization phrase must be received")
    require(auth["decision"] == "execute_brain_and_studio_codegraph_watchlist_sync_only", "invalid authorization decision")

    executed = {item["repo"]: item for item in evidence["executed_actions"]}
    require(set(executed) == set(SYNC_REPOS), "executed repo set mismatch")

    live_pending: dict[str, int] = {}
    for repo_name, repo_path in SYNC_REPOS.items():
        item = executed[repo_name]
        require(item["sync_executed"] is True, f"{repo_name} sync must be executed")
        require(item["codegraph_git_status_entries"] == 0, f"{repo_name} evidence must keep .codegraph git isolated")
        require(pending_total(item["post_sync_status"]["pendingChanges"]) == 0, f"{repo_name} evidence pending must be zero")

        status = run(["codegraph", "status", "--json", "."], cwd=repo_path)
        require(status.returncode == 0, f"codegraph status failed for {repo_name}: {status.stderr}")
        live = json.loads(status.stdout)
        require(live.get("initialized") is True, f"{repo_name} codegraph must be initialized")
        require(live.get("worktreeMismatch") is None, f"{repo_name} worktree mismatch must be null")
        require((live.get("index") or {}).get("reindexRecommended") is False, f"{repo_name} reindex must not be recommended")
        live_total = pending_total(live.get("pendingChanges") or {})
        require(live_total == 0, f"{repo_name} live pending must be zero")
        live_pending[repo_name] = live_total
        assert_codegraph_git_isolated(repo_name, repo_path)

    gfis_path = WATCH_REPOS["GlobalCloud GFIS"]
    gfis_status = run(["codegraph", "status", "--json", "."], cwd=gfis_path)
    require(gfis_status.returncode == 0, f"GFIS codegraph status failed: {gfis_status.stderr}")
    gfis_live = json.loads(gfis_status.stdout)
    gfis_pending = pending_total(gfis_live.get("pendingChanges") or {})
    require(gfis_pending == 1, "GFIS policy exception watch must remain pending=1")
    assert_codegraph_git_isolated("GlobalCloud GFIS", gfis_path)

    closure = evidence["closure_result"]
    require(closure["brain_pending_total"] == 0, "brain closure pending must be zero")
    require(closure["studio_pending_total"] == 0, "studio closure pending must be zero")
    require(closure["gfis_pending_total"] == 1, "gfis policy watch pending must be one")
    require(closure["gfis_policy_exception_preserved"] is True, "GFIS policy exception must be preserved")
    require(closure["brain_codegraph_git_isolated"] is True, "brain git isolation must be true")
    require(closure["studio_codegraph_git_isolated"] is True, "studio git isolation must be true")
    require(closure["sync_only_closure_completed"] is True, "closure result must be completed")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundary must remain false")

    for phrase in [
        "sync_only_closure_completed",
        "GlobalCloud Brain",
        "GlobalCloud Studio",
        "GlobalCloud GFIS",
        "pending=0",
        "policy exception watch",
        "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004",
        "不进入任何项目业务开发",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_watchlist_sync_only_closure_authorized=pass "
        f"brain_pending={live_pending['GlobalCloud Brain']} "
        f"studio_pending={live_pending['GlobalCloud Studio']} "
        f"gfis_pending={gfis_pending} "
        "brain_sync=true studio_sync=true gfis_sync=false "
        "next=GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
