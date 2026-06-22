#!/usr/bin/env python3
"""Validate CodeGraph dev execution steady-state monitor."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-steady-state-monitor-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-steady-state-monitor-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012.md"


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


def pending_total(pending: dict[str, int]) -> int:
    return sum(int(pending.get(key, 0)) for key in ("added", "modified", "removed"))


def extract_json(stdout: str) -> dict[str, Any]:
    start = stdout.find("{")
    end = stdout.rfind("}")
    require(start >= 0 and end >= start, f"no JSON object in command output: {stdout}")
    return json.loads(stdout[start : end + 1])


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-STEADY-STATE-MONITOR-012", "invalid scope")
    require(evidence["status"] == "pass_with_watch", "invalid status")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013", "invalid next round")

    group = evidence["project_group"]
    repos = group["repos"]
    require(group["repo_count"] == 14, "repo_count must be 14")
    require(len(repos) == 14, "repo list must contain 14 repos")
    require(group["studio_included"] is True, "Studio must be included")
    require(group["was_included"] is True, "WAS must be included")
    require({item["name"] for item in repos} >= {"Studio", "WAS", "GPCF", "GFIS"}, "required repos missing")

    live_drift: list[str] = []
    live_pending_by_name: dict[str, dict[str, int]] = {}
    for item in repos:
        repo = Path(item["path"])
        require(repo.exists(), f"repo path missing: {item['name']}")
        status_result = run(["codegraph", "status", "--json", "."], cwd=repo)
        require(status_result.returncode == 0, f"codegraph status failed for {item['name']}: {status_result.stderr}")
        live = json.loads(status_result.stdout)
        pending = live.get("pendingChanges") or {}
        live_pending_by_name[item["name"]] = pending
        require(live.get("initialized") is True, f"repo not initialized: {item['name']}")
        require(live.get("worktreeMismatch") is None, f"worktree mismatch: {item['name']}")
        require((live.get("index") or {}).get("reindexRecommended") is False, f"reindex recommended: {item['name']}")
        require(live.get("fileCount", 0) > 0, f"fileCount missing: {item['name']}")
        require(live.get("nodeCount", 0) > 0, f"nodeCount missing: {item['name']}")
        require(live.get("edgeCount", 0) > 0, f"edgeCount missing: {item['name']}")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=repo)
        require(git_status.returncode == 0, f".codegraph git status failed for {item['name']}: {git_status.stderr}")
        require(git_status.stdout.strip() == "", f".codegraph must remain git-isolated: {item['name']}")

        if pending_total(pending) > 0:
            live_drift.append(item["name"])
    expected_watch = set(evidence["watchlist"]["active_drift_repos"])
    require(set(live_drift).issubset(expected_watch), f"unexpected active drift repos: {live_drift}")
    require({"Brain", "GFIS", "KDS", "Studio"}.issubset(expected_watch), "watchlist must include Brain/GFIS/KDS/Studio")
    require(evidence["watchlist"]["gfis_clean_reindex_authorized"] is False, "GFIS clean reindex must remain unauthorized")
    require(evidence["watchlist"]["clean_reindex_performed"] is False, "clean reindex must not be performed")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must stay false: {key}")

    previous = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_document_localization_debt_closure.py"])
    require(previous.returncode == 0, f"previous localization debt validator failed: {previous.stdout}{previous.stderr}")

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

    query = run(["codegraph", "query", "validate_codegraph_dev_execution_document_localization_debt_closure", "--json"])
    require(query.returncode == 0, f"CodeGraph query failed: {query.stderr}")
    query_json = json.loads(query.stdout)
    require(query_json, "CodeGraph query must return at least one result")
    top = query_json[0]["node"]["filePath"]
    require(top == "tools/kds-sync/validate_codegraph_dev_execution_document_localization_debt_closure.py", "CodeGraph query top result mismatch")

    affected = run(["codegraph", "affected", top, "--json"])
    require(affected.returncode == 0, f"CodeGraph affected failed: {affected.stderr}")
    affected_json = extract_json(affected.stdout)
    require(affected_json["changedFiles"] == [top], "affected changedFiles mismatch")
    require("fallback_reason" in evidence["operational_effect_probe"], "fallback_reason is required when affected_tests is empty")

    for phrase in [
        "pass_with_watch",
        "14 仓 CodeGraph 索引均可读",
        "Brain",
        "GFIS",
        "Studio",
        "不声明 accepted",
        "GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_dev_execution_steady_state_monitor=pass_with_watch "
        "repo_count=14 "
        f"active_drift_repos={','.join(live_drift) if live_drift else 'none'} "
        f"gpcf_pending={pending_total(live_pending_by_name.get('GPCF', {}))} "
        "reindex_recommended=false "
        "codegraph_git_isolated=true "
        "localization_debt=false "
        "accepted=false integrated=false production_ready=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-WATCHLIST-DRIFT-TRIAGE-013"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
