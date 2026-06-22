#!/usr/bin/env python3
"""Validate CodeGraph impact-report dry-run evidence."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-impact-report-dry-run-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-impact-report-dry-run-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005.md"
TARGET = "tools/kds-sync/validate_codegraph_project_group_steady_state_verify.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-IMPACT-REPORT-DRY-RUN-20260621", "invalid evidence id")
    require(evidence["status"] == "impact_report_dry_run_pass", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005", "invalid scope")
    require(evidence["target"]["repo"] == "GlobalCoud GPCF", "target repo mismatch")
    require(TARGET in evidence["target"]["changed_files"], "target validator must be a changed file")

    query = run(["codegraph", "query", "codegraph_project_group_steady_state_verify", "--json"])
    require(query.returncode == 0, f"codegraph query failed: {query.stderr}")
    query_results = json.loads(query.stdout)
    require(len(query_results) >= 4, "targeted query should return at least 4 results")
    require(query_results[0]["node"]["filePath"] == TARGET, "top query result must be target validator")

    node = run(["codegraph", "node", TARGET])
    require(node.returncode == 0, f"codegraph node failed: {node.stderr}")
    require("no other indexed file depends on it" in node.stdout, "target validator should have no indexed dependents")
    require("129 lines" in node.stdout, "target validator line count should be reported")

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
        "validate_codegraph_project_group_steady_state_verify|CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-20260621|GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004|GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005",
        "docs",
        "tools",
        "governance",
        "harness",
        "loop",
        "09-status",
    ])
    require(rg.returncode == 0, "rg baseline should find references")
    require(len(rg.stdout.splitlines()) >= evidence["rg_baseline"]["matched_lines"], "rg baseline line count regressed")

    impact = evidence["impact_report"]
    require(impact["risk"]["level"] == "low", "risk level must be low")
    require(impact["risk"]["waes_required"] is False, "WAES must not be required for this low-risk dry-run")
    require(impact["impacted_tests"] == [], "impacted tests must be empty in evidence")
    require("function:main" in impact["impacted_symbols"], "main symbol must be recorded")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundary must remain false")

    for phrase in ["CodeGraph Impact Report Dry-run", "0 affected tests", "101 affected symbols", "GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006"]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_impact_report_dry_run=pass "
        "target=validate_codegraph_project_group_steady_state_verify "
        "affected_tests=0 broad_main_noise>=50 "
        "next=GPCF-CODEGRAPH-IMPACT-METRICS-BASELINE-006"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
