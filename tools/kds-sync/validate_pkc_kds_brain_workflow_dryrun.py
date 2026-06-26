#!/usr/bin/env python3
"""Validate PKC KDS/Brain workflow dry-run evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKC_REPO = ROOT.parent / "GlobalCloud PKC"
DOC = ROOT / "docs/harness/PKC/evidence/pkc-kds-brain-workflow-dryrun-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

PKC_AGENTS = PKC_REPO / "AGENTS.md"
PKC_PLAN = PKC_REPO / "GlobalCloud PKC 实施方案.md"
PKC_PACKAGE = PKC_REPO / "package.json"

REQUIRED_DOC_TOKENS = [
    "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001",
    "pkc_kds_brain_workflow_dryrun = controlled",
    "target_status_candidate = task_pack_ready / local_dev_dryrun_boundary",
    "lint = pass",
    "typecheck = pass",
    "unit_test = pass",
    "test_files = 10 passed",
    "tests = 57 passed",
    "runtime_verified = local_dev_only",
    "real_kds_integration_verified = false",
    "real_brain_integration_verified = false",
    "real_personal_data_write = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "Unknown project config \"onlyBuiltDependencies\"",
    "不声明真实 KDS 集成完成",
    "不声明真实 Brain 集成完成",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud PKC 实施方案",
    "project: PKC",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
    "PKC 负责知识和提示相关产品入口",
    "不声明业务实现完成、不声明客户交付完成、不声明 accepted、integrated 或 production_ready",
]

REQUIRED_PACKAGE_TOKENS = [
    "\"lint\": \"tsc --noEmit\"",
    "\"typecheck\": \"tsc --noEmit\"",
    "\"test\": \"vitest run\"",
]

REQUIRED_REF_TOKENS = [
    "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001",
    "pkc-kds-brain-workflow-dryrun-20260625.md",
    "validate_pkc_kds_brain_workflow_dryrun.py",
    "task_pack_ready / local_dev_dryrun_boundary",
]

FORBIDDEN_CLAIMS = [
    "real_kds_integration_verified = true",
    "real_brain_integration_verified = true",
    "real_personal_data_write = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    doc_text = read(DOC, failures)
    agents_text = read(PKC_AGENTS, failures)
    plan_text = read(PKC_PLAN, failures)
    package_text = read(PKC_PACKAGE, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(STATUS, failures), read(TASKS, failures)])

    if not PKC_REPO.exists():
        failures.append(f"missing PKC repo: {PKC_REPO}")

    if "globalcloud-collaborative-dev" not in agents_text:
        failures.append("PKC AGENTS missing collaborative development governance reference")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in PKC dry-run evidence: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in PKC implementation plan: {token}")

    for token in REQUIRED_PACKAGE_TOKENS:
        if token not in package_text:
            failures.append(f"missing script token in PKC package.json: {token}")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive PKC claim: {token}")

    result = {
        "gate": "pkc_kds_brain_workflow_dryrun",
        "status": "pass" if not failures else "fail",
        "task_id": "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001",
        "target_status_candidate": "task_pack_ready / local_dev_dryrun_boundary",
        "test_files": "10 passed",
        "tests": "57 passed",
        "real_kds_integration_verified": False,
        "real_brain_integration_verified": False,
        "failures": failures,
        "warnings": [
            "This validates PKC local lint/typecheck/unit-test dry-run only; it does not validate real KDS/Brain integration, delivery, accepted, integrated, production, or customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
