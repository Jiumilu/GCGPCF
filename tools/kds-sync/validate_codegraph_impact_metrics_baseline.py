#!/usr/bin/env python3
"""Validate CodeGraph impact metrics baseline evidence."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-impact-metrics-baseline-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006.md"
TARGET = "tools/kds-sync/validate_codegraph_impact_report_dry_run.py"

REPOS = [
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC"),
    ROOT,
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
    Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系"),
]


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
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-IMPACT-METRICS-BASELINE-20260621", "invalid evidence id")
    require(evidence["status"] == "impact_metrics_baseline_ready", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006", "invalid scope")

    baseline = evidence["project_group_baseline"]
    require(baseline["repo_count"] == 14, "repo count must be 14")
    require(baseline["indexed_repo_count"] == 14, "indexed repo count must be 14")
    require(baseline["git_protected_repo_count"] == 14, "git-protected repo count must be 14")
    require(baseline["codegraph_git_status_entries_total"] == 0, ".codegraph git entries must be zero")
    require(baseline["studio_included"] is True, "Studio must be included")
    require(baseline["was_included"] is True, "WAS must be included")

    initialized = 0
    git_entries = 0
    for repo in REPOS:
        require(repo.exists() and (repo / ".git").exists(), f"repo missing: {repo}")
        status = run(["codegraph", "status", "--json", "."], cwd=repo)
        require(status.returncode == 0, f"codegraph status failed for {repo}: {status.stderr}")
        data = json.loads(status.stdout)
        require(data.get("initialized") is True, f"codegraph not initialized: {repo}")
        initialized += 1
        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=repo)
        require(git_status.returncode == 0, f"git status failed for {repo}")
        git_entries += len([line for line in git_status.stdout.splitlines() if line.strip()])
    require(initialized == 14, "live initialized repo count must be 14")
    require(git_entries == 0, "live .codegraph git entries must be zero")

    query = run(["codegraph", "query", "codegraph_impact_report_dry_run", "--json"])
    require(query.returncode == 0, f"codegraph query failed: {query.stderr}")
    query_results = json.loads(query.stdout)
    require(len(query_results) >= 4, "query should return at least 4 results")
    require(query_results[0]["node"]["filePath"] == TARGET, "top query result must be target validator")

    node = run(["codegraph", "node", TARGET])
    require(node.returncode == 0, f"codegraph node failed: {node.stderr}")
    require("108 lines" in node.stdout, "target line count must be reported")
    require("9 symbols" in node.stdout, "target symbol count must be reported")
    require("no other indexed file depends on it" in node.stdout, "target should have no indexed dependents")

    affected = run(["codegraph", "affected", TARGET, "--json"])
    require(affected.returncode == 0, f"codegraph affected failed: {affected.stderr}")
    affected_json = json.loads(affected.stdout)
    require(affected_json["affectedTests"] == [], "affected tests must be empty")
    require(affected_json["totalDependentsTraversed"] == 0, "dependents traversed must be zero")

    broad = run(["codegraph", "impact", "main", "--depth", "2"])
    require(broad.returncode == 0, f"codegraph broad impact failed: {broad.stderr}")
    match = re.search(r"Impact of changing \"main\" — ([0-9]+) affected symbols", broad.stdout)
    require(match is not None, "broad impact count missing")
    require(int(match.group(1)) >= 50, "broad main impact should remain a noisy negative control")

    rg = run([
        "rg",
        "-n",
        "validate_codegraph_impact_report_dry_run|CODEGRAPH-IMPACT-REPORT-DRY-RUN-20260621|GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005|GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006",
        "docs",
        "tools",
        "governance",
        "harness",
        "loop",
        "09-status",
    ])
    require(rg.returncode == 0, "rg baseline should find references")
    require(len(rg.stdout.splitlines()) >= evidence["text_scan_baseline"]["matched_lines"], "rg matched lines regressed")

    for metric in ["coverage", "query_precision", "impact_precision", "noise_control", "manual_scan_reduction", "gate_replayability"]:
        require(metric in evidence["metrics"], f"missing metric: {metric}")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundary must remain false")

    for phrase in ["impact_metrics_baseline_ready", "13 个 matched files / 28 个 matched lines", "101 affected symbols", "GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007"]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_impact_metrics_baseline=pass "
        "repo_count=14 git_protected=14 target=validate_codegraph_impact_report_dry_run "
        "affected_tests=0 rg_files>=13 rg_lines>=28 "
        "next=GPCF-CODEGRAPH-IMPACT-REGRESSION-WATCH-007"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
