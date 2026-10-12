#!/usr/bin/env python3
"""Validate CodeGraph impact regression watch evidence."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-impact-regression-watch-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-impact-regression-watch-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007.md"
BASELINE = ROOT / "docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.json"
TARGET = "tools/kds-sync/validate_codegraph_impact_metrics_baseline.py"

REPOS = {
    "GlobalCloud GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
    "GlobalCloud GPC": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC"),
    "GlobalCloud PVAOS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS"),
    "GlobalCloud WAES": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES"),
    "GlobalCloud KDS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"),
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud PKC": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC"),
    "GlobalCloud XiaoC": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC"),
    "GlobalCloud XGD": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD"),
    "GlobalCloud XiaoG": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG"),
    "GlobalCloud MMC": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC"),
    "GlobalCoud GPCF": ROOT,
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
    "WAS世界资产体系": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    baseline = json.loads(read(BASELINE))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-IMPACT-REGRESSION-WATCH-20260621", "invalid evidence id")
    require(evidence["status"] == "impact_regression_watch_active", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007", "invalid scope")
    require(baseline["status"] == "impact_metrics_baseline_ready", "baseline status mismatch")

    goals = {item["goal"]: item for item in evidence["next_stage_goals"]}
    for goal in ["coverage_regression_watch", "impact_precision_watch", "noise_control_watch", "active_drift_watch", "loop_input_generation"]:
        require(goal in goals, f"missing next-stage goal: {goal}")
    require(goals["active_drift_watch"]["current_result"] == "watch_required", "active drift must require watch")

    initialized = 0
    git_entries = 0
    live_pending: dict[str, dict] = {}
    for name, path in REPOS.items():
        require(path.exists() and (path / ".git").exists(), f"repo missing: {name}")
        status = run(["codegraph", "status", "--json", "."], cwd=path)
        require(status.returncode == 0, f"codegraph status failed for {name}: {status.stderr}")
        data = json.loads(status.stdout)
        require(data.get("initialized") is True, f"codegraph not initialized: {name}")
        initialized += 1
        live_pending[name] = data.get("pendingChanges") or {}
        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path)
        require(git_status.returncode == 0, f"git status failed for {name}")
        git_entries += len([line for line in git_status.stdout.splitlines() if line.strip()])
    require(initialized == 14, "initialized repo count must be 14")
    require(git_entries == 0, ".codegraph git entries must be zero")

    sample = evidence["project_group_regression_sample"]
    require(sample["repo_count"] == 14, "repo_count must be 14")
    require(sample["initialized_repo_count"] == 14, "initialized_repo_count must be 14")
    require(sample["git_protected_repo_count"] == 14, "git_protected_repo_count must be 14")
    require(sample["codegraph_git_status_entries_total"] == 0, "evidence git status entries must be zero")

    watch = {item["repo"]: item for item in sample["watch_repos"]}
    require(watch["GlobalCloud GFIS"]["classification"] == "policy_exception_watch", "GFIS classification mismatch")
    require(watch["GlobalCloud Brain"]["classification"] == "active_drift_watch", "Brain classification mismatch")
    require(watch["GlobalCloud Studio"]["classification"] == "active_drift_regression_watch", "Studio classification mismatch")
    require(sum(live_pending["GlobalCloud Studio"].values()) >= 0, "Studio pending must be readable")

    query = run(["codegraph", "query", "codegraph_impact_metrics_baseline", "--json"])
    require(query.returncode == 0, f"codegraph query failed: {query.stderr}")
    results = json.loads(query.stdout)
    require(len(results) >= 4, "query should return at least 4 results")
    require(results[0]["node"]["filePath"] == TARGET, "top query result must be target validator")

    node = run(["codegraph", "node", TARGET])
    require(node.returncode == 0, f"codegraph node failed: {node.stderr}")
    require("144 lines" in node.stdout, "line count must be reported")
    require("10 symbols" in node.stdout, "symbol count must be reported")
    require("no other indexed file depends on it" in node.stdout, "target should have no indexed dependents")

    affected = run(["codegraph", "affected", TARGET, "--json"])
    require(affected.returncode == 0, f"codegraph affected failed: {affected.stderr}")
    affected_json = json.loads(affected.stdout)
    require(affected_json["affectedTests"] == [], "affected tests must be empty")
    require(affected_json["totalDependentsTraversed"] == 0, "dependents traversed must be zero")

    broad = run(["codegraph", "impact", "main", "--depth", "2"])
    require(broad.returncode == 0, f"codegraph impact failed: {broad.stderr}")
    match = re.search(r"Impact of changing \"main\" — ([0-9]+) affected symbols", broad.stdout)
    require(match is not None, "broad impact count missing")
    require(int(match.group(1)) >= 50, "main impact must remain noisy")

    rg = run([
        "rg",
        "-n",
        "validate_codegraph_impact_metrics_baseline|CODEGRAPH-IMPACT-METRICS-BASELINE-20260621|GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006|GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007",
        "docs",
        "tools",
        "governance",
        "harness",
        "loop",
        "09-status",
    ])
    require(rg.returncode == 0, "rg regression watch should find references")
    require(len(rg.stdout.splitlines()) >= evidence["impact_regression_sample"]["text_scan"]["matched_lines"], "rg line count regressed")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundary must remain false")

    for phrase in ["impact_regression_watch_active", "active_drift_regression_watch", "101 affected symbols", "GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008"]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_impact_regression_watch=pass "
        "repo_count=14 git_protected=14 impact_regression=false "
        "studio_watch=active_drift_regression_watch "
        "next=GPCF-CODEGRAPH-DRIFT-ALERT-THRESHOLDS-008"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
