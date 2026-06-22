#!/usr/bin/env python3
"""Validate CodeGraph development execution pilot pack evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-pilot-pack-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-pilot-pack-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002.md"
ADMISSION_VALIDATOR = ROOT / "tools/kds-sync/validate_codegraph_dev_execution_admission.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    require(ADMISSION_VALIDATOR.exists(), "admission validator must exist")

    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-PILOT-PACK-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002", "invalid scope")
    require(evidence["status"] == "pilot_pack_ready", "invalid status")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003", "invalid next round")
    require(evidence["candidate_task"]["business_implementation_allowed"] is False, "business implementation must stay disabled")

    pre_change = evidence["pre_change_analysis"]
    require(pre_change["query"] == "CodeGraph 业务开发执行层准入 validator evidence", "query mismatch")
    require(pre_change["target_nodes"] == ["tools/kds-sync/validate_codegraph_dev_execution_admission.py"], "target nodes mismatch")
    require(pre_change["node_inspection"]["lines"] == 145, "node inspection line count mismatch")
    require(pre_change["node_inspection"]["indexed_dependents"] == 0, "indexed dependents must be zero for pilot candidate")

    affected = pre_change["affected"]
    require(affected["changedFiles"] == ["tools/kds-sync/validate_codegraph_dev_execution_admission.py"], "affected changed files mismatch")
    require(affected["affectedTests"] == [], "affected tests must be empty for this pilot")
    require(affected["totalDependentsTraversed"] == 0, "total dependents traversed must be zero")

    constraints = evidence["implementation_constraints"]
    require(constraints["files_allowed_to_change"] == [], "pilot pack must not allow implementation file changes")
    require(".codegraph/**" in constraints["files_not_to_touch"], ".codegraph must be protected")

    selection = evidence["test_selection"]
    require(selection["affected_tests"] == [], "affected_tests must remain empty")
    require(selection["fallback_tests"], "fallback tests must be recorded")
    require("affectedTests=[]" in selection["fallback_reason"], "fallback reason must cite empty affected tests")

    codegraph_evidence = evidence["codegraph_evidence"]
    require(codegraph_evidence["changed_files"] == [], "pilot pack must not record implementation changed files")
    require(codegraph_evidence["post_change_status"] == "pilot_pack_recorded_pending_codegraph_resync", "unexpected post_change_status")

    metrics = evidence["efficiency_metrics"]
    require(metrics["manual_scan_files"] == 10, "manual scan file baseline mismatch")
    require(metrics["codegraph_candidate_files"] == 1, "candidate file count mismatch")
    require(metrics["actual_changed_files"] == 0, "pilot must not change business implementation files")
    require(metrics["missed_impact_count"] == 0, "missed impact count must be zero")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002",
        "affectedTests=[]",
        "fallback_reason",
        "files_allowed_to_change=[]",
        "actual_changed_files=0",
        "不进入任何业务实现",
        "GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_pilot_pack=pass "
        "target_nodes=1 "
        "affected_tests=0 "
        "fallback_tests=5 "
        "business_implementation=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
