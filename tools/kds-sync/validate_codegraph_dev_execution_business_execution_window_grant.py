#!/usr/bin/env python3
"""Validate the CodeGraph business execution window grant evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-business-execution-window-grant-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-business-execution-window-grant-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-EXECUTION-WINDOW-GRANT-007.md"
COVERAGE = ROOT / "docs/harness/evidence/codegraph-project-group-full-coverage-20260621.json"
WATCHLIST = ROOT / "docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.json"

KEY_REPOS = {
    "GPCF": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF"),
    "GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
    "Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "KDS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"),
    "Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def validate_repo(repo: Path, name: str) -> dict[str, Any]:
    status = run(["codegraph", "status", "--json", "."], cwd=repo)
    require(status.returncode == 0, f"codegraph status failed for {name}: {status.stderr}")
    live = json.loads(status.stdout)
    require(live.get("initialized") is True, f"{name} codegraph must be initialized")
    require(live.get("index", {}).get("reindexRecommended") is False, f"{name} reindex must not be recommended")

    git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=repo)
    require(git_status.returncode == 0, f".codegraph git status failed for {name}: {git_status.stderr}")
    require(git_status.stdout.strip() == "", f"{name} .codegraph must remain git-isolated")

    return live


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    coverage = load_json(COVERAGE)
    watchlist = load_json(WATCHLIST)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-BUSINESS-EXECUTION-WINDOW-GRANT-20260623", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-EXECUTION-WINDOW-GRANT-007", "invalid scope")
    require(evidence["status"] == "business_execution_window_granted_project_group", "invalid status")

    project_scope = evidence["project_group_scope"]
    require(project_scope["repo_count"] == 14, "repo_count must be 14")
    require(project_scope["coverage_repo_count"] == 14, "coverage_repo_count must be 14")
    require(project_scope["studio_included"] is True, "Studio must be included")
    require(project_scope["was_included"] is True, "WAS must be included")

    auth = evidence["authorization_state"]
    require(auth["authorization_complete"] is True, "authorization must be complete")
    require(auth["authorized"] is True, "authorization must be true")
    require(auth["authorization_phrase"] == "全部授权", "authorization phrase mismatch")
    require(auth["missing_authorization_fields"] == [], "authorization fields must be complete")

    window = evidence["execution_window"]
    require(window["business_implementation_allowed"] is True, "business implementation must be allowed")
    require(window["codegraph_sync_allowed"] is True, "codegraph sync must be allowed")
    for key in [
        "commit_authorized",
        "push_authorized",
        "deployment_authorized",
        "production_write_authorized",
        "external_api_write_authorized",
        "real_kds_write_authorized",
        "real_waes_write_authorized",
        "clean_reindex_authorized",
    ]:
        require(window[key] is False, f"{key} must remain false")

    require(coverage["project_group"]["repo_count"] == 14, "coverage evidence repo_count mismatch")
    require(coverage["project_group"]["indexed_repo_count"] == 14, "coverage evidence indexed_repo_count mismatch")
    require(coverage["project_group"]["studio_included"] is True, "coverage evidence must include Studio")
    require(coverage["project_group"]["was_included"] is True, "coverage evidence must include WAS")
    require(coverage["status"] in {"review_required", "evidence_ready"}, "coverage status mismatch")

    require(watchlist["status"] == "authorization_pack_ready", "watchlist pack status mismatch")
    require(watchlist["governance"]["codegraph_sync_performed_in_watchlist_repos"] is False, "watchlist sync must stay false")
    require(watchlist["governance"]["clean_reindex_performed"] is False, "watchlist clean reindex must stay false")

    live_snapshots = {}
    for name, repo in KEY_REPOS.items():
        require(repo.exists(), f"missing repo path: {name}")
        live_snapshots[name] = validate_repo(repo, name)

    gpcf = live_snapshots["GPCF"]
    gfis = live_snapshots["GFIS"]
    brain = live_snapshots["Brain"]
    kds = live_snapshots["KDS"]
    studio = live_snapshots["Studio"]

    for name, live in [("GPCF", gpcf), ("GFIS", gfis), ("Brain", brain), ("KDS", kds), ("Studio", studio)]:
        pending = live.get("pendingChanges")
        require(isinstance(pending, dict), f"{name} pendingChanges must be a dict")
        for key in ("added", "modified", "removed"):
            require(isinstance(pending.get(key), int), f"{name} pendingChanges.{key} must be an int")
            require(pending[key] >= 0, f"{name} pendingChanges.{key} must be non-negative")
        require(live.get("worktreeMismatch") is None, f"{name} worktreeMismatch must be null")
        require(live.get("index", {}).get("reindexRecommended") is False, f"{name} reindex must not be recommended")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for phrase in [
        "business_execution_window_granted_project_group",
        "business_implementation_allowed | `true`",
        "codegraph_sync_allowed | `true`",
        "commit_authorized | `false`",
        "push_authorized | `false`",
        "production_write_authorized | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
        "不打开 production、commit、push、deploy",
        "GPCF-CODEGRAPH-DEV-EXECUTION-BUSINESS-TASK-INTAKE-008",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "business_execution_window_granted_project_group",
        "business_implementation_allowed=true",
        "codegraph_sync_allowed=true",
        "commit_authorized=false",
        "push_authorized=false",
        "deployment_authorized=false",
        ".codegraph/ 仍保持 Git 隔离",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_dev_execution_business_execution_window_grant=pass "
        "repo_count=14 business_implementation_allowed=true codegraph_sync_allowed=true "
        "commit_authorized=false push_authorized=false deployment_authorized=false "
        "production_write_authorized=false external_api_write_authorized=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
