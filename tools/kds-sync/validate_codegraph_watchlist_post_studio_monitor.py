#!/usr/bin/env python3
"""Validate CodeGraph watchlist post-Studio monitor evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-watchlist-post-studio-monitor-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-watchlist-post-studio-monitor-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016.md"

REPOS = {
    "Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
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
    return json.loads(read(path))


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def extract_json(stdout: str) -> dict[str, Any]:
    start = stdout.find("{")
    end = stdout.rfind("}")
    require(start >= 0 and end >= start, f"no JSON object in command output: {stdout}")
    return json.loads(stdout[start : end + 1])


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


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016", "invalid scope")
    require(evidence["status"] == "watch_required", "invalid status")
    require(evidence["previous_round"] == "GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015", "invalid previous round")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017", "invalid next round")
    require(evidence["review_rework_count"] == 0, "review rework count baseline must be zero")

    watchlist = evidence["watchlist"]
    require(watchlist["repo_count"] == 4, "watchlist repo_count must be 4")
    require(set(watchlist["repos"]) == set(REPOS), "watchlist repo names mismatch")

    for name, repo in REPOS.items():
        item = watchlist["repos"][name]
        status_result = run(["codegraph", "status", "--json", "."], cwd=repo)
        require(status_result.returncode == 0, f"codegraph status failed for {name}: {status_result.stderr}")
        status = json.loads(status_result.stdout)
        require(status["initialized"] is True, f"CodeGraph not initialized: {name}")
        require(status["worktreeMismatch"] is None, f"worktree mismatch: {name}")
        require(status["index"]["reindexRecommended"] is False, f"reindex recommended: {name}")
        require(status["pendingChanges"] == item["codegraph_pending"], f"pending mismatch: {name}")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=repo)
        require(git_status.returncode == 0, f".codegraph git status failed for {name}: {git_status.stderr}")
        require(git_status.stdout.strip() == "", f".codegraph must remain git-isolated: {name}")

        counts = git_dirty_counts(repo)
        baseline = item["git_dirty"]
        require(counts["total"] >= baseline["total"], f"git dirty total below monitor baseline: {name}: {counts}")
        require(counts["modified"] >= baseline["modified"], f"git modified below monitor baseline: {name}: {counts}")
        require(counts["deleted"] >= baseline["deleted"], f"git deleted below monitor baseline: {name}: {counts}")
        require(counts["untracked"] >= baseline["untracked"], f"git untracked below monitor baseline: {name}: {counts}")

    governance = evidence["governance"]
    require(governance["mode"] == "post_studio_monitor_only", "invalid governance mode")
    for key, value in governance.items():
        if key in {"mode", "codegraph_git_isolated"}:
            continue
        require(value is False, f"governance action must be false: {key}")
    require(governance["codegraph_git_isolated"] is True, "CodeGraph git isolation must be true")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        require(section in evidence["five_direction"], f"missing five_direction section: {section}")
        require(f"## {section}" in loop_round, f"loop round missing section: {section}")

    localization = run(["python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json"])
    require(localization.returncode == 0, f"localization gate failed: {localization.stdout}{localization.stderr}")
    localization_json = extract_json(localization.stdout)
    require(localization_json["localization_gate"] == "pass", "localization gate must pass")
    require(localization_json["findings"] == 0, "localization findings must be zero")

    loop_gate = run(["python3", "tools/kds-sync/loop_document_gate.py", "--check-only"])
    require(loop_gate.returncode == 0, f"Loop document gate failed: {loop_gate.stdout}{loop_gate.stderr}")
    loop_json = extract_json(loop_gate.stdout)
    require(loop_json["gate"] == "pass", "Loop document gate must pass")
    require(loop_json["localization_debt"] is False, "localization_debt must be false")

    pollution = run(["python3", "tools/kds-sync/check_document_pollution.py"])
    require(pollution.returncode == 0 and "document_pollution=pass" in pollution.stdout, "document pollution must pass")

    token = run(["python3", "tools/kds-sync/validate_kds_token.py"])
    require(token.returncode == 0 and "kds_token=pass" in token.stdout, "KDS token must pass")

    for phrase in [
        "watch_required",
        "Brain：CodeGraph pending 已归零，Git dirty=0，继续监控即可。",
        "GFIS：CodeGraph pending 已归零，Git dirty=0，继续监控即可。",
        "Studio：CodeGraph pending 已归零，Git dirty=0，sync-only 已收口。",
        "KDS：CodeGraph pending 为 modified=2，仍有 17 个 Git dirty",
        "GFIS clean reindex 仍不授权",
        "GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017",
        "review_rework_count=0",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    print(
        "codegraph_watchlist_post_studio_monitor=watch_required "
        "studio_residual_modified=0 "
        "kds_dirty_total=17 "
        "brain_authorization=monitor_only "
        "gfis_clean_reindex_authorized=false "
        "kds_authorization=required "
        "business_development=false commit=false push=false deploy=false "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-KDS-MIRROR-SCOPE-REVIEW-AUTHORIZATION-017"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
