#!/usr/bin/env python3
"""Validate XiaoC model-routing dry-run environment-blocked evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
XIAOC_REPO = ROOT.parent / "GlobalCloud XiaoC"
DOC = ROOT / "docs/harness/XiaoC/evidence/xiaoc-model-routing-dryrun-environment-blocked-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

XIAOC_PLAN = XIAOC_REPO / "GlobalCloud XiaoC 实施方案.md"
XIAOC_PACKAGE = XIAOC_REPO / "package.json"

REQUIRED_DOC_TOKENS = [
    "XIAOC-MODEL-ROUTING-DRYRUN-001",
    "xiaoc_model_routing_dryrun = environment_blocked",
    "target_status_candidate = baseline_controlled / environment_blocked",
    "required_node = ^22.0.0",
    "actual_node = v26.0.0",
    "pnpm_version = 10.6.1",
    "commands_attempted = 4",
    "commands_passed = 0",
    "commands_failed = 4",
    "environment_blocker = ERR_PNPM_UNSUPPORTED_ENGINE",
    "real_model_call_executed = false",
    "wrangler_executed = false",
    "docker_executed = false",
    "production_ready = false",
    "accepted = false",
    "integrated = false",
    "customer_accepted = false",
    "Expected Node `^22.0.0`",
    "Got `v26.0.0`",
    "不声明 XiaoC dry-run 通过",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud XiaoC 实施方案",
    "project: XiaoC",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
    "XiaoC 负责提示工程服务",
    "不声明业务实现完成、不声明客户交付完成、不声明 accepted、integrated 或 production_ready",
]

REQUIRED_PACKAGE_TOKENS = [
    "\"node\": \"^22.0.0\"",
    "\"lint\": \"node scripts/run-many.js lint:ui typecheck:ui lint:mcp-server typecheck:core typecheck:mcp-server build:ui-types typecheck:web typecheck:extension\"",
    "\"typecheck:core\": \"pnpm -F @prompt-optimizer/core typecheck\"",
    "\"test:fast\": \"pnpm -r test --run --passWithNoTests\"",
    "\"check:locale\": \"node scripts/check-locale-parity.mjs\"",
]

REQUIRED_REF_TOKENS = [
    "XIAOC-MODEL-ROUTING-DRYRUN-001",
    "xiaoc-model-routing-dryrun-environment-blocked-20260625.md",
    "validate_xiaoc_model_routing_dryrun_environment_blocked.py",
    "baseline_controlled / environment_blocked",
]

FORBIDDEN_CLAIMS = [
    "xiaoc_model_routing_dryrun = controlled",
    "commands_passed = 4",
    "real_model_call_executed = true",
    "wrangler_executed = true",
    "docker_executed = true",
    "production_ready = true",
    "accepted = true",
    "integrated = true",
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
    plan_text = read(XIAOC_PLAN, failures)
    package_text = read(XIAOC_PACKAGE, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(STATUS, failures), read(TASKS, failures)])

    if not XIAOC_REPO.exists():
        failures.append(f"missing XiaoC repo: {XIAOC_REPO}")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in XiaoC blocked evidence: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in XiaoC implementation plan: {token}")

    for token in REQUIRED_PACKAGE_TOKENS:
        if token not in package_text:
            failures.append(f"missing token in XiaoC package.json: {token}")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive XiaoC claim: {token}")

    result = {
        "gate": "xiaoc_model_routing_dryrun_environment_blocked",
        "status": "pass" if not failures else "fail",
        "task_id": "XIAOC-MODEL-ROUTING-DRYRUN-001",
        "target_status_candidate": "baseline_controlled / environment_blocked",
        "required_node": "^22.0.0",
        "actual_node": "v26.0.0",
        "commands_attempted": 4,
        "commands_passed": 0,
        "commands_failed": 4,
        "failures": failures,
        "warnings": [
            "This validates the XiaoC environment blocker only; it does not validate model routing dry-run success, real model calls, Wrangler, Docker, deployment, accepted, integrated, or customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
