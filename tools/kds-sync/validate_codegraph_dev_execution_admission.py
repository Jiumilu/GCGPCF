#!/usr/bin/env python3
"""Validate CodeGraph business development execution admission artifacts."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/codegraph/codegraph-dev-execution-admission.md"
TEMPLATE = ROOT / "templates/CODEGRAPH_DEV_EXECUTION_EVIDENCE_TEMPLATE.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-admission-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-admission-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001.md"


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


def require_keys(obj: dict[str, Any], keys: list[str], label: str) -> None:
    for key in keys:
        require(key in obj, f"{label} missing key: {key}")


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")

    doc = read(DOC)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    template = load_json(TEMPLATE)
    evidence = load_json(EVIDENCE_JSON)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-ADMISSION-20260621", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001", "invalid scope")
    require(evidence["status"] == "dev_execution_admission_ready", "invalid status")
    require(evidence["next_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002", "invalid next round")

    expected_projects = {"GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"}
    require(set(evidence["project_group_scope"]) == expected_projects, "project group scope must cover 14 projects")

    required_commands = [
        'codegraph query "<功能/模块/接口关键词>" --json',
        'codegraph node "<候选文件>"',
        'codegraph affected "<候选文件>" --json',
    ]
    require(evidence["required_commands"] == required_commands, "required command list mismatch")
    for command in required_commands:
        require(command in doc, f"admission doc missing command: {command}")
        require(command in evidence_md, f"evidence markdown missing command: {command}")

    required_layers = [
        "pre_change_impact_location",
        "implementation_scope_constraint",
        "affected_test_selection",
        "acceptance_evidence",
        "efficiency_metrics",
    ]
    require(evidence["required_layers"] == required_layers, "required layers mismatch")

    implementation_fields = ["target_nodes", "affected_scope", "files_allowed_to_change", "files_not_to_touch", "expected_tests"]
    test_fields = ["affected_tests", "fallback_tests", "fallback_reason"]
    codegraph_evidence_fields = ["query", "target_nodes", "affected", "changed_files", "test_selection_reason", "post_change_status"]
    metric_fields = ["manual_scan_files", "codegraph_candidate_files", "actual_changed_files", "affected_tests", "missed_impact_count", "time_to_first_target"]
    exception_fields = ["reason", "fallback_scan", "reviewer", "expires_at"]

    require_keys(template["pre_change_analysis"], ["query", "query_results", "target_nodes", "node_inspection", "affected"], "template pre_change_analysis")
    require_keys(template["implementation_constraints"], implementation_fields, "template implementation_constraints")
    require_keys(template["test_selection"], test_fields, "template test_selection")
    require_keys(template["codegraph_evidence"], codegraph_evidence_fields, "template codegraph_evidence")
    require_keys(template["efficiency_metrics"], metric_fields, "template efficiency_metrics")
    require_keys(template["codegraph_unavailable_exception"], exception_fields, "template codegraph_unavailable_exception")

    for group, fields in {
        "implementation_constraints": implementation_fields,
        "test_selection": test_fields,
        "codegraph_evidence": codegraph_evidence_fields,
        "efficiency_metrics": metric_fields,
    }.items():
        require(evidence["required_fields"][group] == fields, f"evidence required_fields mismatch: {group}")

    for phrase in [
        "没有这一步，任务不能进入实现",
        "dev_execution_admission=blocked",
        "codegraph_unavailable_exception",
        "不代表业务变更完成",
        "不代表 WAES",
        "GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002",
    ]:
        require(phrase in doc, f"admission doc missing phrase: {phrase}")

    for phrase in [
        "GPCF-CODEGRAPH-DEV-EXECUTION-ADMISSION-001",
        "dev_execution_admission_ready",
        "codegraph_evidence",
        "fallback_reason",
        "missed_impact_count",
        "不代表业务完成",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for value in template["status_boundaries"].values():
        require(value is False, "template status boundaries must stay false")
    for value in evidence["status_boundaries"].values():
        require(value is False, "evidence status boundaries must stay false")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_admission=pass "
        "required_commands=3 "
        "required_layers=5 "
        "template=json "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-PILOT-PACK-002"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
