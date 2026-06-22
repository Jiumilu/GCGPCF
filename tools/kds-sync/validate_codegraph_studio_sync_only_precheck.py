#!/usr/bin/env python3
"""Validate CodeGraph Studio sync-only precheck evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
STUDIO = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio")
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-studio-sync-only-precheck-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-studio-sync-only-precheck-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015.md"
AUTHORIZATION_PACK = ROOT / "docs/harness/evidence/codegraph-dev-execution-watchlist-authorization-pack-20260622.json"


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

    require(evidence["evidence_id"] == "CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015", "invalid scope")
    require(evidence["status"] == "studio_codegraph_sync_only_pass_with_residual_watch", "invalid status")
    require(evidence["previous_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-AUTHORIZATION-PACK-014", "invalid previous round")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016", "invalid next round")

    studio = evidence["studio"]
    require(STUDIO.exists(), "Studio repo missing")
    require(studio["pre_sync_codegraph_pending"] == {"added": 2, "modified": 9, "removed": 0}, "pre-sync pending mismatch")
    require(studio["sync_result"]["changed_files_synced"] == 12, "changed file count mismatch")
    require(studio["sync_result"]["added_files_synced"] == 2, "added sync count mismatch")
    require(studio["sync_result"]["modified_files_synced"] == 10, "modified sync count mismatch")
    require(studio["sync_result"]["nodes_changed"] == 237, "nodes changed mismatch")
    require(studio["followup_sync_result"]["changed_files_synced"] == 2, "follow-up changed file count mismatch")
    require(studio["followup_sync_result"]["modified_files_synced"] == 2, "follow-up modified sync count mismatch")
    require(studio["followup_sync_result"]["nodes_changed"] == 22, "follow-up nodes changed mismatch")

    status_result = run(["codegraph", "status", "--json", "."], cwd=STUDIO)
    require(status_result.returncode == 0, f"Studio codegraph status failed: {status_result.stderr}")
    status = json.loads(status_result.stdout)
    require(status["initialized"] is True, "Studio CodeGraph not initialized")
    require(status["pendingChanges"]["added"] == 0, "Studio added pending must be zero")
    require(status["pendingChanges"]["removed"] == 0, "Studio removed pending must be zero")
    require(status["pendingChanges"]["modified"] <= studio["residual_watch"]["allowed_pending_ceiling"]["modified"], "Studio modified pending exceeds residual watch ceiling")
    require(status["worktreeMismatch"] is None, "Studio worktree mismatch must be null")
    require(status["index"]["reindexRecommended"] is False, "Studio reindex must not be recommended")
    require(status["fileCount"] == studio["post_sync_codegraph"]["fileCount"], "Studio fileCount mismatch")
    require(status["nodeCount"] == studio["post_sync_codegraph"]["nodeCount"], "Studio nodeCount mismatch")
    require(status["edgeCount"] == studio["post_sync_codegraph"]["edgeCount"], "Studio edgeCount mismatch")

    git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=STUDIO)
    require(git_status.returncode == 0, f"Studio .codegraph git status failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", "Studio .codegraph must remain git-isolated")

    counts = git_dirty_counts(STUDIO)
    require(counts == studio["git_dirty_after_sync"], f"Studio dirty counts mismatch: {counts}")

    for key, value in evidence["other_watchlist_repos"].items():
        require(value is False, f"other watchlist action must be false: {key}")
    for key, value in evidence["governance"].items():
        if key == "mode":
            require(value == "studio_sync_only_precheck", "invalid governance mode")
        else:
            require(value is False, f"governance action must be false: {key}")
    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    for section in ["run", "stop", "verify", "recover", "debug"]:
        require(section in evidence["five_direction"], f"missing five_direction section: {section}")
        require(f"## {section}" in loop_round, f"loop round missing five-direction section: {section}")

    authorization_pack = load_json(AUTHORIZATION_PACK)
    require(authorization_pack["status"] == "authorization_pack_ready", "authorization pack must be ready")
    require(authorization_pack["next_round"] == "GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015", "authorization pack must point to Studio precheck")

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
        "studio_codegraph_sync_only_pass_with_residual_watch",
        "sync 前：`pendingChanges={added:2, modified:9, removed:0}`",
        "最终观测：`pendingChanges={added:0, modified:7, removed:0}`",
        "CodeGraph sync-only 已执行，但 Studio 仍存在小幅 modified residual watch",
        "不声明 Studio 业务实现完成",
        "GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    print(
        "codegraph_studio_sync_only_precheck=pass_with_residual_watch "
        f"studio_pending_modified={status['pendingChanges']['modified']} "
        "studio_reindex_recommended=false "
        "studio_dirty_total=12 "
        "studio_codegraph_git_isolated=true "
        "business_development=false "
        "commit=false push=false deploy=false "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
