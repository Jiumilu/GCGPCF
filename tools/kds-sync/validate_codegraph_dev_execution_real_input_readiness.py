#!/usr/bin/env python3
"""Validate CodeGraph development-execution real-input readiness evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-readiness-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-readiness-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017.md"
GFIS_LOOP_STATE = ROOT / "08-evidence-samples/GFIS/loop-state.md"
GFIS_EVIDENCE_INDEX = ROOT / "08-evidence-samples/GFIS/evidence-index.md"
TASK_INTAKE = ROOT / "docs/harness/evidence/codegraph-dev-execution-business-task-intake-008.json"
DEV_STATE = ROOT / "docs/harness/evidence/codegraph-development-state-normal-work-20260626.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    task = load_json(TASK_INTAKE)
    dev_state = load_json(DEV_STATE)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    gfis_loop_state = read(GFIS_LOOP_STATE)
    gfis_evidence_index = read(GFIS_EVIDENCE_INDEX)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-READINESS-017", "invalid scope")
    require(evidence["status"] == "real_input_readiness_blocked", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")

    dev_gate = run(["python3", "tools/kds-sync/validate_codegraph_development_state_normal_work.py"])
    require(dev_gate.returncode == 0, f"development state gate failed: {dev_gate.stdout}{dev_gate.stderr}")
    intake_gate = run([
        "python3",
        "tools/kds-sync/validate_codegraph_task_intake_gate.py",
        "--task-file",
        "docs/harness/evidence/codegraph-dev-execution-business-task-intake-008.json",
    ])
    require(intake_gate.returncode == 0, f"task intake gate failed: {intake_gate.stdout}{intake_gate.stderr}")

    readiness = evidence["codegraph_development_readiness"]
    require(dev_state["status"] == "development_state_normal_work_verified", "development-state evidence status mismatch")
    require(task["status"] == "ready", "task intake must remain ready")
    for key, value in readiness.items():
        require(value is True, f"{key} must be true")

    real = evidence["real_input_readiness"]
    require(real["ready"] is False, "real input readiness must be blocked")
    require(real["submitted_files_found"] == 0, "submitted files must be zero")
    require(real["valid_source_records"] == 0, "valid source records must be zero")
    require(real["real_source_records"] == 0, "real source records must be zero")
    require(real["runtime_primary_key_ready"] == 0, "runtime primary key ready must be zero")
    require(real["runtime_primary_key_missing"] == 12, "runtime primary key missing must be 12")
    require(real["runtime_intake"] == 0, "runtime intake must be zero")
    require(real["waes_review"] == 0, "WAES review must be zero")
    require(real["verified"] == 0, "verified must be zero")
    require(real["kds_coverage_missing_sources"] == 4, "KDS missing sources must be 4")
    require(real["runtime_sop_e2e"] == "repair_required", "runtime SOP must remain repair_required")

    for phrase in [
        "real_source_records=0",
        "runtime_primary_key_ready=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
        "missing_sources=4",
        "真实客户订单原件或平台订单回执",
        "runtime_primary_key_missing=12",
    ]:
        require(phrase in gfis_loop_state, f"GFIS loop-state missing phrase: {phrase}")

    for phrase in [
        "valid_source_records=0",
        "runtime_sop_e2e=repair_required",
        "客户订单原件或平台订单回执",
    ]:
        require(phrase in gfis_evidence_index, f"GFIS evidence index missing phrase: {phrase}")

    decision = evidence["decision"]
    require(decision["development_state_admission"] == "continue_with_codegraph_pre_change_analysis", "invalid development decision")
    require(decision["real_business_execution"] == "blocked_until_real_source_input_arrives", "invalid real business decision")
    require(decision["runtime_state"] == "not_verified", "runtime state must not be verified")
    require(decision["status_ceiling"] == "partial", "status ceiling must be partial")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "real_input_readiness_blocked",
        "CodeGraph 开发态工作链可以继续",
        "submitted_files_found",
        "valid_source_records",
        "runtime_primary_key_missing",
        "blocked_until_real_source_input_arrives",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-COLLECTION-PACK-018",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "run",
        "stop",
        "verify",
        "recover",
        "debug",
        "real_input_readiness_blocked",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-COLLECTION-PACK-018",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_real_input_readiness=blocked "
        "development_state_admission=continue "
        "real_business_execution=blocked_until_real_source_input_arrives "
        "valid_source_records=0 "
        "runtime_primary_key_ready=0 "
        "runtime_primary_key_missing=12 "
        "runtime_intake=0 "
        "waes_review=0 "
        "verified=0 "
        "missing_sources=4 "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-COLLECTION-PACK-018"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
