#!/usr/bin/env python3
"""Validate XGD TICK/Brain smoke evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
XGD_REPO = ROOT.parent / "GlobalCloud XGD"
DOC = ROOT / "docs/harness/XGD/evidence/xgd-tick-brain-smoke-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

XGD_PLAN = XGD_REPO / "GlobalCloud XGD 实施方案.md"
XGD_PACKAGE = XGD_REPO / "package.json"

REQUIRED_DOC_TOKENS = [
    "XGD-TICK-BRAIN-SMOKE-001",
    "xgd_tick_brain_smoke = controlled",
    "target_status_candidate = task_pack_ready / local_dev_smoke_boundary",
    "harness_validate = pass",
    "unit_test = pass",
    "unit_suites = 5/5",
    "brain_ui_smoke = pass",
    "brain_ui_nodes = 2",
    "brain_ui_links = 1",
    "acui_host = true",
    "brand = SmokeXiaoG AI Agent",
    "long_running_agent_verified = false",
    "external_action_executed = false",
    "production_ready = false",
    "accepted = false",
    "integrated = false",
    "customer_accepted = false",
    "xgd_loop_harness=pass",
    "[PASS] unit tests: 5/5 suites",
    "[PASS] brain-ui smoke",
    "不声明长程 Agent 生产可用",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud XGD 实施方案",
    "project: XGD",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
    "XGD 负责 XiaoG 智能体连续运行框架",
    "不声明业务实现完成、不声明客户交付完成、不声明 accepted、integrated 或 production_ready",
]

REQUIRED_PACKAGE_TOKENS = [
    "\"harness:validate\": \"node scripts/validate_xgd_loop_harness.mjs\"",
    "\"test:unit\": \"node scripts/test-unit.mjs\"",
    "\"smoke:brain-ui\": \"node scripts/smoke-brain-ui.mjs\"",
]

REQUIRED_REF_TOKENS = [
    "XGD-TICK-BRAIN-SMOKE-001",
    "xgd-tick-brain-smoke-20260625.md",
    "validate_xgd_tick_brain_smoke.py",
    "task_pack_ready / local_dev_smoke_boundary",
]

FORBIDDEN_CLAIMS = [
    "long_running_agent_verified = true",
    "external_action_executed = true",
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
    plan_text = read(XGD_PLAN, failures)
    package_text = read(XGD_PACKAGE, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(STATUS, failures), read(TASKS, failures)])

    if not XGD_REPO.exists():
        failures.append(f"missing XGD repo: {XGD_REPO}")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in XGD smoke evidence: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in XGD implementation plan: {token}")

    for token in REQUIRED_PACKAGE_TOKENS:
        if token not in package_text:
            failures.append(f"missing script token in XGD package.json: {token}")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive XGD claim: {token}")

    result = {
        "gate": "xgd_tick_brain_smoke",
        "status": "pass" if not failures else "fail",
        "task_id": "XGD-TICK-BRAIN-SMOKE-001",
        "target_status_candidate": "task_pack_ready / local_dev_smoke_boundary",
        "unit_suites": "5/5",
        "brain_ui_smoke": "pass",
        "long_running_agent_verified": False,
        "external_action_executed": False,
        "failures": failures,
        "warnings": [
            "This validates XGD local harness/unit/Brain UI smoke only; it does not validate long-running agent production readiness, real external actions, accepted, integrated, or customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
