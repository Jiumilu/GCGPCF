#!/usr/bin/env python3
"""Validate CodeGraph GFIS read-only scope review evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-gfis-scope-review-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-gfis-scope-review-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019.md"


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
    require(result.returncode == 0, f"git status failed: {result.stderr}")
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

    require(evidence["evidence_id"] == "CODEGRAPH-GFIS-SCOPE-REVIEW-20260623", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-GFIS-SCOPE-REVIEW-019", "invalid scope")
    require(evidence["status"] == "gfis_scope_review_completed_no_sync_needed", "invalid status")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020", "invalid next round")

    authorization = evidence["authorization"]
    require(authorization["user_authorized"] is True, "scope review must be user-authorized")
    for forbidden in ["codegraph sync", "clean reindex", "business development", "commit", "push", "deploy"]:
        require(forbidden in authorization["explicit_exclusions"], f"missing explicit exclusion: {forbidden}")

    review = evidence["gfis_live_scope_review"]
    status_result = run(["codegraph", "status", "--json", "."], cwd=GFIS)
    require(status_result.returncode == 0, f"codegraph status failed: {status_result.stderr}")
    status = json.loads(status_result.stdout)
    require(status["pendingChanges"] == review["codegraph_status"]["pendingChanges"], "GFIS CodeGraph pending mismatch")
    require(status["worktreeMismatch"] is None, "GFIS worktreeMismatch must be null")
    require(status["index"]["reindexRecommended"] is False, "GFIS reindex must not be recommended")
    require(status["lastIndexed"] == review["codegraph_status"]["lastIndexed"], "GFIS lastIndexed drifted")

    counts = git_dirty_counts(GFIS)
    require(counts == review["git_dirty"], f"GFIS git dirty mismatch: {counts}")

    codegraph_git = run(["git", "status", "--short", "--", ".codegraph"], cwd=GFIS)
    require(codegraph_git.returncode == 0, f".codegraph status failed: {codegraph_git.stderr}")
    require(codegraph_git.stdout.strip() == "", ".codegraph must remain isolated")

    require(review["sync_only_candidate"] is False, "sync-only candidate must be false")
    require(review["clean_reindex_candidate"] is False, "clean reindex candidate must be false")
    require(evidence["observed_drift_resolution"]["codex_performed_gfis_sync"] is False, "GFIS sync must be false")
    require(evidence["observed_drift_resolution"]["codex_performed_gfis_clean_reindex"] is False, "clean reindex must be false")
    require(evidence["observed_drift_resolution"]["codex_modified_gfis_business_files"] is False, "business modification must be false")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        require(section in evidence["five_direction"], f"missing five_direction: {section}")
        require(f"## {section}" in loop_round, f"loop round missing section: {section}")

    localization = run(["python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json"])
    require(localization.returncode == 0, f"localization gate failed: {localization.stdout}{localization.stderr}")
    localization_json = extract_json(localization.stdout)
    require(localization_json["localization_gate"] == "pass", "localization gate must pass")

    loop_gate = run(["python3", "tools/kds-sync/loop_document_gate.py", "--check-only"])
    require(loop_gate.returncode == 0, f"Loop document gate failed: {loop_gate.stdout}{loop_gate.stderr}")
    loop_json = extract_json(loop_gate.stdout)
    require(loop_json["gate"] == "pass", "Loop document gate must pass")

    pollution = run(["python3", "tools/kds-sync/check_document_pollution.py"])
    require(pollution.returncode == 0 and "document_pollution=pass" in pollution.stdout, "document pollution must pass")

    token = run(["python3", "tools/kds-sync/validate_kds_token.py"])
    require(token.returncode == 0 and "kds_token=pass" in token.stdout, "KDS token must pass")

    for phrase in [
        "gfis_scope_review_completed_no_sync_needed",
        "Git dirty 为 1",
        "CodeGraph pending 为 added=0、modified=0、removed=0",
        "不执行 `codegraph sync`",
        "不执行 clean reindex",
        "GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    print(
        "codegraph_gfis_scope_review=pass "
        f"gfis_git_dirty={counts['total']} gfis_pending={sum(counts.get(k, 0) for k in ('added', 'modified', 'removed'))} "
        "sync_only_candidate=false clean_reindex_candidate=false "
        "gfis_sync=false gfis_clean_reindex=false business_development=false "
        "commit=false push=false deploy=false accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-WATCHLIST-STEADY-MONITOR-020"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
