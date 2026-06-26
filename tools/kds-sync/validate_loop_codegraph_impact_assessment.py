#!/usr/bin/env python3
"""Validate CodeGraph operational impact assessment evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-impact-assessment-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-impact-assessment-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-IMPACT-ASSESSMENT-001.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str]) -> str:
    completed = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    require(completed.returncode == 0, f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stdout}\n{completed.stderr}")
    return completed.stdout


def main() -> int:
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "LOOP-CODEGRAPH-IMPACT-ASSESSMENT-20260621", "invalid evidence id")
    require(evidence["status"] == "codegraph_operational_value_evidenced_with_active_watchlist", "invalid status")

    validated = evidence["validated_inputs"]
    require(validated["repo_count"] == 14, "repo_count must be 14")
    require(validated["indexed_repo_count"] == 14, "indexed_repo_count must be 14")
    require(validated["up_to_date_repo_count"] == 11, "up_to_date_repo_count must be 11")
    require(validated["active_drift_repo_count"] == 2, "active drift must be 2")
    require(
        validated["active_drift_projects"] == ["GlobalCloud Brain", "GlobalCloud Studio"],
        "Brain and Studio must be active drift projects",
    )
    require(validated["controlled_residual_projects"] == ["GlobalCloud GFIS"], "GFIS must be controlled residual")
    require(validated["codegraph_git_status_entries_total"] == 0, ".codegraph git entries must be 0")

    dimensions = evidence["impact_dimensions"]
    require(len(dimensions) == 6, "must have six impact dimensions")
    scores = {item["dimension"]: item["score"] for item in dimensions}
    for required in [
        "coverage_truth",
        "drift_detection",
        "loop_decision_support",
        "cost_reduction",
        "risk_control",
        "replayability",
    ]:
        require(required in scores, f"missing dimension: {required}")
    require(sum(scores.values()) == evidence["score"]["total"], "score total mismatch")
    require(evidence["score"]["total"] == 28, "score total must be 28")
    require(evidence["score"]["rating"] == "effective_with_active_watchlist", "invalid rating")

    for path in evidence["source_evidence"]:
        require((ROOT / path).exists(), f"source evidence missing: {path}")

    for key, value in evidence["boundaries"].items():
        require(value is False, f"boundary must remain false: {key}")

    for phrase in [
        "codegraph_operational_value_evidenced_with_active_watchlist",
        "28 / 30",
        "effective_with_active_watchlist",
        "MTTD",
        "MTTR",
        "不证明项目业务完成",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    graphized = run(["python3", "tools/kds-sync/validate_loop_codegraph_project_group_graphized.py"])
    monitor = run(["python3", "tools/kds-sync/validate_loop_codegraph_project_group_monitor.py"])
    require("active_drift=Studio" in graphized, "graphized validator must show Studio watch")
    require("controlled_residual=none" in graphized, "graphized validator must show GFIS residual cleared")
    require("watchlist=Studio" in monitor, "monitor validator must show Studio watchlist")

    print(
        "loop_codegraph_impact_assessment=pass "
        "status=codegraph_operational_value_evidenced_with_active_watchlist "
        "score=28/30 rating=effective_with_active_watchlist "
        "next=GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
