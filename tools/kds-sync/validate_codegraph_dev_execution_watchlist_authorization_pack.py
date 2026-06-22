#!/usr/bin/env python3
"""Validate CodeGraph watchlist authorization pack evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014.md"
STUDIO_CLOSURE_JSON = ROOT / "docs/harness/evidence/codegraph-studio-sync-only-precheck-20260622.json"

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

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014", "invalid scope")
    require(evidence["status"] == "authorization_pack_ready", "invalid status")
    require(evidence["previous_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013", "invalid previous round")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015", "invalid next round")

    watchlist = evidence["watchlist"]
    require(watchlist["repo_count"] == 4, "watchlist repo_count must be 4")
    require(set(watchlist["repos"]) == set(REPOS), "watchlist repo names mismatch")

    for name, repo in REPOS.items():
        item = watchlist["repos"][name]
        require(repo.exists(), f"repo path missing: {name}")
        status_result = run(["codegraph", "status", "--json", "."], cwd=repo)
        require(status_result.returncode == 0, f"codegraph status failed for {name}: {status_result.stderr}")
        status = json.loads(status_result.stdout)
        require(status["initialized"] is True, f"CodeGraph not initialized: {name}")
        require(status["worktreeMismatch"] is None, f"worktree mismatch: {name}")
        require(status["index"]["reindexRecommended"] is False, f"reindex recommended: {name}")
        if name == "Studio" and STUDIO_CLOSURE_JSON.exists():
            require(status["pendingChanges"]["added"] == 0, "Studio added pending must be zero after sync-only precheck")
            require(status["pendingChanges"]["removed"] == 0, "Studio removed pending must be zero after sync-only precheck")
            require(status["pendingChanges"]["modified"] <= 2, "Studio modified pending must stay within residual watch")
        else:
            require(status["pendingChanges"] == item["codegraph_pending"], f"pending mismatch: {name}")
            require(sum(status["pendingChanges"].values()) > 0, f"watchlist repo must still have pending drift: {name}")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=repo)
        require(git_status.returncode == 0, f".codegraph git status failed for {name}: {git_status.stderr}")
        require(git_status.stdout.strip() == "", f".codegraph must remain git-isolated: {name}")

        counts = git_dirty_counts(repo)
        baseline = item["git_dirty"]
        require(counts["total"] >= baseline["total"], f"git dirty total below evidence baseline: {name}: {counts}")
        require(counts["modified"] >= baseline["modified"], f"git modified count below evidence baseline: {name}: {counts}")
        require(counts["deleted"] >= baseline["deleted"], f"git deleted count below evidence baseline: {name}: {counts}")
        require(counts["untracked"] >= baseline["untracked"], f"git untracked count below evidence baseline: {name}: {counts}")
        require(item["authorization_question"], f"missing authorization question: {name}")
        require(item["recommended_answer"], f"missing recommended answer: {name}")
        require(item["allowed_if_authorized"], f"missing allowed actions: {name}")
        require(item["forbidden"], f"missing forbidden actions: {name}")

    questions = evidence["authorization_questions"]
    require(len(questions) == 5, "authorization question count must be 5")
    by_id = {item["id"]: item for item in questions}
    require(by_id["authorize_studio_sync_only_precheck"]["recommended"] is True, "Studio must be recommended first candidate")
    require(by_id["authorize_clean_reindex_any_repo"]["recommended"] is False, "clean reindex must not be recommended")
    for item in questions:
        require(item["default_if_no_answer"] == "not_authorized", f"default must be not_authorized: {item['id']}")

    governance = evidence["governance"]
    require(governance["mode"] == "authorization_pack_only", "mode must be authorization_pack_only")
    require(governance["codegraph_sync_performed_in_watchlist_repos"] is False, "watchlist sync must not be performed")
    require(governance["clean_reindex_performed"] is False, "clean reindex must not be performed")
    require(governance["business_development_performed"] is False, "business development must not be performed")
    require(governance["commit_performed"] is False, "commit must not be performed")
    require(governance["push_performed"] is False, "push must not be performed")
    require(governance["deployment_performed"] is False, "deploy must not be performed")
    require(governance["codegraph_git_isolated"] is True, "CodeGraph git isolation must be true")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        require(section in evidence["five_direction"], f"missing five_direction section: {section}")
        require(f"## {section}" in loop_round, f"loop round missing five-direction section: {section}")

    previous = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_watchlist_drift_triage.py"])
    require(previous.returncode == 0, f"previous watchlist triage validator failed: {previous.stdout}{previous.stderr}")

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
        "authorization_pack_ready",
        "是否授权 Studio 先进入低风险 CodeGraph sync-only precheck",
        "GFIS clean reindex 继续不授权",
        "Brain、GFIS、KDS 在未取得独立授权前，只允许继续只读监控",
        "GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015",
        "不声明 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    print(
        "codegraph_dev_execution_watchlist_authorization_pack=pass "
        "repo_count=4 "
        "recommended_first=Studio "
        "brain_authorization=defer "
        "gfis_clean_reindex_authorized=false "
        "kds_authorization=defer "
        "watchlist_sync_performed=false "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
