#!/usr/bin/env python3
"""Validate CodeGraph development execution Harness/Loop gate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "docs/codegraph/codegraph-dev-execution-harness-gate.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-harness-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-harness-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003.md"
POSITIVE = ROOT / "fixtures/codegraph/dev-execution-harness-gate/positive-pilot-evidence.json"
NEGATIVE = ROOT / "fixtures/codegraph/dev-execution-harness-gate/negative-missing-fallback-reason.json"


class GateBlocked(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


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


def require_section(evidence: dict[str, Any], section: str) -> dict[str, Any]:
    value = evidence.get(section)
    if not isinstance(value, dict):
        raise GateBlocked(f"missing_{section}")
    return value


def require_non_empty_list(value: Any, reason: str) -> None:
    if not isinstance(value, list) or not value:
        raise GateBlocked(reason)


def evaluate_harness_gate(evidence: dict[str, Any]) -> str:
    pre_change = require_section(evidence, "pre_change_analysis")
    constraints = require_section(evidence, "implementation_constraints")
    selection = require_section(evidence, "test_selection")
    codegraph = require_section(evidence, "codegraph_evidence")
    metrics = require_section(evidence, "efficiency_metrics")
    status = require_section(evidence, "status_boundaries")

    require_non_empty_list(pre_change.get("target_nodes"), "missing_target_nodes")
    require_non_empty_list(constraints.get("target_nodes"), "missing_target_nodes")
    require_non_empty_list(codegraph.get("target_nodes"), "missing_target_nodes")
    require_non_empty_list(constraints.get("affected_scope"), "missing_affected_scope")

    affected = codegraph.get("affected") or pre_change.get("affected")
    if not isinstance(affected, dict):
        raise GateBlocked("missing_affected")
    affected_tests = affected.get("affectedTests", [])
    if affected_tests == [] and not selection.get("fallback_reason"):
        raise GateBlocked("empty_affected_tests_without_fallback_reason")

    allowed = set(constraints.get("files_allowed_to_change") or [])
    changed = set(codegraph.get("changed_files") or [])
    if changed and not changed.issubset(allowed):
        raise GateBlocked("changed_files_outside_allowed_scope")

    for key in ("accepted", "integrated", "production_ready"):
        if status.get(key) is True:
            raise GateBlocked("accepted_integrated_or_production_ready_true")
    for key in ("production_write", "external_api_write"):
        if status.get(key) is True:
            raise GateBlocked("production_write_or_external_api_write_true")

    for key in ("manual_scan_files", "codegraph_candidate_files", "actual_changed_files", "missed_impact_count", "time_to_first_target"):
        if key not in metrics:
            raise GateBlocked(f"missing_metric_{key}")

    return "pass"


def main() -> int:
    policy = read(POLICY)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    evidence = load_json(EVIDENCE_JSON)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003", "invalid scope")
    require(evidence["status"] == "harness_gate_ready", "invalid status")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004", "invalid next round")

    positive = load_json(POSITIVE)
    negative = load_json(NEGATIVE)
    require(evaluate_harness_gate(positive) == "pass", "positive fixture must pass")
    try:
        evaluate_harness_gate(negative)
    except GateBlocked as exc:
        require(exc.reason == "empty_affected_tests_without_fallback_reason", "negative fixture blocked for wrong reason")
    else:
        raise SystemExit("FAIL: negative fixture must be blocked")

    require(evidence["dry_run_results"]["positive_fixture"] == "pass", "positive dry-run result mismatch")
    require(evidence["dry_run_results"]["negative_fixture"] == "blocked", "negative dry-run result mismatch")
    require(
        evidence["dry_run_results"]["negative_block_reason"] == "empty_affected_tests_without_fallback_reason",
        "negative block reason mismatch",
    )

    for rule in [
        "missing_codegraph_evidence",
        "missing_target_nodes",
        "missing_affected_scope",
        "empty_affected_tests_without_fallback_reason",
        "changed_files_outside_allowed_scope",
        "accepted_integrated_or_production_ready_true",
        "production_write_or_external_api_write_true",
        "codegraph_claimed_as_final_waes_or_harness_decision",
    ]:
        require(rule in evidence["blocking_rules"], f"evidence missing blocking rule: {rule}")

    for phrase in [
        "codegraph_dev_execution_harness_gate=blocked",
        "affected.affectedTests=[]",
        "fallback_reason",
        "CodeGraph 替代 WAES/Harness/人工验收裁决",
        "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004",
    ]:
        require(phrase in policy, f"policy missing phrase: {phrase}")

    for phrase in [
        "GPCF-CODEGRAPH-DEV-EXECUTION-HARNESS-GATE-003",
        "positive_fixture=pass",
        "negative_fixture=blocked",
        "不进入业务实现",
        "不代表业务完成",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_harness_gate=pass "
        "positive_fixture=pass "
        "negative_fixture=blocked "
        "block_reason=empty_affected_tests_without_fallback_reason "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
