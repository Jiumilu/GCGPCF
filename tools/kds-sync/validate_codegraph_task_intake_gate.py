#!/usr/bin/env python3
"""Validate the reusable CodeGraph task-intake gate."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/codegraph/codegraph-task-intake-gate.md"
README = ROOT / "docs/codegraph/README.md"
LOOP_INTEGRATION = ROOT / "docs/codegraph/codegraph-loop-integration.md"
AUTH_TEMPLATE = ROOT / "templates/CODEGRAPH_DEV_EXECUTION_AUTHORIZATION_TEMPLATE.json"
EVIDENCE_TEMPLATE = ROOT / "templates/CODEGRAPH_DEV_EXECUTION_EVIDENCE_TEMPLATE.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-task-intake-gate-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-task-intake-gate-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-TASK-INTAKE-GATE-001.md"
POSITIVE = ROOT / "fixtures/codegraph/task-intake-gate/positive-task-intake.json"
NEGATIVE_MISSING_EVIDENCE = ROOT / "fixtures/codegraph/task-intake-gate/negative-missing-codegraph-evidence.json"
NEGATIVE_NO_FALLBACK = ROOT / "fixtures/codegraph/task-intake-gate/negative-empty-affected-tests-no-fallback.json"
NEGATIVE_MISSING_EXPECTED_TESTS = ROOT / "fixtures/codegraph/task-intake-gate/negative-missing-expected-tests.json"


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
    if not path.is_absolute():
        path = ROOT / path
    return json.loads(read(path))


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def require_keys(obj: dict[str, Any], keys: list[str], label: str) -> None:
    for key in keys:
        require(key in obj, f"{label} missing key: {key}")


def require_non_empty_list(value: Any, reason: str) -> None:
    if not isinstance(value, list) or not value:
        raise GateBlocked(reason)


def require_section(obj: dict[str, Any], section: str) -> dict[str, Any]:
    value = obj.get(section)
    if not isinstance(value, dict):
        raise GateBlocked(f"missing_{section}")
    return value


def evaluate_task_intake(task: dict[str, Any]) -> str:
    pre_change = require_section(task, "pre_change_analysis")
    constraints = require_section(task, "implementation_constraints")
    selection = require_section(task, "test_selection")
    codegraph = require_section(task, "codegraph_evidence")
    metrics = require_section(task, "efficiency_metrics")
    status = require_section(task, "status_boundaries")

    if task.get("codegraph_required") is not True:
        raise GateBlocked("codegraph_required_false")

    require_non_empty_list(pre_change.get("target_nodes"), "missing_target_nodes")
    require_non_empty_list(constraints.get("target_nodes"), "missing_target_nodes")
    require_non_empty_list(constraints.get("affected_scope"), "missing_affected_scope")
    require_non_empty_list(constraints.get("files_allowed_to_change"), "missing_files_allowed_to_change")
    require_non_empty_list(constraints.get("files_not_to_touch"), "missing_files_not_to_touch")
    require_non_empty_list(constraints.get("expected_tests"), "missing_expected_tests")
    require_non_empty_list(pre_change.get("query_results"), "missing_query_results")
    require_non_empty_list(pre_change.get("node_inspection"), "missing_node_inspection")

    affected = codegraph.get("affected") or pre_change.get("affected")
    if not isinstance(affected, dict):
        raise GateBlocked("missing_affected")
    affected_tests = affected.get("affectedTests", [])
    if affected_tests == [] and not selection.get("fallback_reason"):
        raise GateBlocked("empty_affected_tests_without_fallback_reason")

    allowed = set(constraints.get("files_allowed_to_change") or [])
    changed = set(codegraph.get("changed_files") or affected.get("changedFiles") or [])
    if changed and not changed.issubset(allowed):
        raise GateBlocked("changed_files_outside_allowed_scope")

    for key in ("accepted", "integrated", "production_ready"):
        if status.get(key) is True:
            raise GateBlocked("accepted_integrated_or_production_ready_true")
    for key in ("production_write", "external_api_write"):
        if status.get(key) is True:
            raise GateBlocked("production_write_or_external_api_write_true")

    for key in ("manual_scan_files", "codegraph_candidate_files", "actual_changed_files", "missed_impact_count", "time_to_first_target", "review_rework_count"):
        if key not in metrics:
            raise GateBlocked(f"missing_metric_{key}")

    require(isinstance(codegraph.get("query"), str) and codegraph["query"].strip(), "missing_codegraph_query")
    require_non_empty_list(codegraph.get("target_nodes"), "missing_codegraph_target_nodes")
    require(isinstance(codegraph.get("test_selection_reason"), str) and codegraph["test_selection_reason"].strip(), "missing_test_selection_reason")
    require(isinstance(codegraph.get("post_change_status"), str) and codegraph["post_change_status"].strip(), "missing_post_change_status")

    return "pass"


def validate_static_artifacts() -> None:
    doc = read(DOC)
    readme = read(README)
    loop_integration = read(LOOP_INTEGRATION)
    auth = load_json(AUTH_TEMPLATE)
    evidence = load_json(EVIDENCE_TEMPLATE)
    evidence_json = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    for phrase in [
        "Task Intake",
        "codegraph query",
        "codegraph node",
        "codegraph affected",
        "target_nodes",
        "affected_scope",
        "files_allowed_to_change",
        "files_not_to_touch",
        "expected_tests",
        "affected_tests",
        "fallback_reason",
        "codegraph_evidence",
        "manual_scan_files",
        "review_rework_count",
        "blocked",
        "Harness / WAES",
    ]:
        require(phrase in doc, f"task intake doc missing phrase: {phrase}")

    for phrase in [
        "CODEGRAPH-TASK-INTAKE-GATE-20260623",
        "task_intake_gate_ready",
        "missing_codegraph_evidence",
        "negative_empty_affected_tests_no_fallback",
    ]:
        require(phrase in json.dumps(evidence_json, ensure_ascii=False), f"task intake evidence json missing phrase: {phrase}")
        require(phrase in evidence_md, f"task intake evidence md missing phrase: {phrase}")

    for phrase in [
        "GPCF-CODEGRAPH-TASK-INTAKE-GATE-001",
        "任务开工前门禁",
        "`affected_tests=[]` 无 fallback 时会阻断进入实现",
    ]:
        require(phrase in loop_round, f"task intake loop round missing phrase: {phrase}")

    require("codegraph-task-intake-gate.md" in readme, "README must link task intake gate")
    require("Task Intake Gate" in loop_integration, "loop integration must mention task intake gate")

    for phrase in [
        "target_nodes",
        "affected_scope",
        "files_allowed_to_change",
        "files_not_to_touch",
        "expected_tests",
        "affected_tests or fallback_reason",
        "post_change_status",
    ]:
        require(phrase in json.dumps(auth, ensure_ascii=False), f"authorization template missing field: {phrase}")

    for phrase in [
        "codegraph_evidence",
        "target_nodes",
        "affected_scope",
        "files_allowed_to_change",
        "files_not_to_touch",
        "expected_tests",
        "fallback_tests",
        "fallback_reason",
        "manual_scan_files",
        "codegraph_candidate_files",
        "actual_changed_files",
        "missed_impact_count",
        "time_to_first_target",
        "review_rework_count",
    ]:
        require(phrase in json.dumps(evidence, ensure_ascii=False), f"evidence template missing field: {phrase}")


def validate_fixture(path: Path, expected: str) -> None:
    task = load_json(path)
    try:
        result = evaluate_task_intake(task)
    except GateBlocked as exc:
        require(expected == "blocked", f"{path.name} should pass, but blocked with {exc.reason}")
        require(exc.reason, f"{path.name} blocked without reason")
        return
    require(expected == result, f"{path.name} unexpected result: {result}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-file", type=Path)
    args = parser.parse_args()

    validate_static_artifacts()

    if args.task_file is not None:
        task = load_json(args.task_file)
        try:
            result = evaluate_task_intake(task)
        except GateBlocked as exc:
            print(f"codegraph_task_intake_gate=blocked block_reason={exc.reason}")
            return 1
        print("codegraph_task_intake_gate=pass")
        return 0

    validate_fixture(POSITIVE, "pass")
    validate_fixture(NEGATIVE_MISSING_EVIDENCE, "blocked")
    validate_fixture(NEGATIVE_NO_FALLBACK, "blocked")
    validate_fixture(NEGATIVE_MISSING_EXPECTED_TESTS, "blocked")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_task_intake_gate=pass "
        "task_schema=ready "
        "positive_fixture=pass "
        "negative_missing_codegraph_evidence=blocked "
        "negative_empty_affected_tests_no_fallback=blocked "
        "negative_missing_expected_tests=blocked "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
