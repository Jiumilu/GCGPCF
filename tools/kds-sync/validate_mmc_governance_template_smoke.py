#!/usr/bin/env python3
"""Validate MMC governance template smoke evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MMC_REPO = ROOT.parent / "GlobalCloud MMC"
DOC = ROOT / "docs/harness/MMC/evidence/mmc-governance-template-smoke-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

MMC_AGENTS = MMC_REPO / "AGENTS.md"
MMC_PLAN = MMC_REPO / "GlobalCloud MMC 实施方案.md"

REQUIRED_DOC_TOKENS = [
    "MMC-GOVERNANCE-TEMPLATE-SMOKE-001",
    "mmc_governance_template_smoke = controlled",
    "target_status_candidate = task_pack_ready / local_document_smoke_boundary",
    "runtime_verified = false",
    "integration_verified = false",
    "delivery_verified = false",
    "customer_accepted = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "source_agents = AGENTS.md",
    "source_implementation_plan = GlobalCloud MMC 实施方案.md",
    "不声明 MMC runtime 已通过",
    "不声明下游项目已接入 MMC 模板",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud MMC 实施方案",
    "project: MMC",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
    "MMC 负责 Harness Engineering 控制台",
    "不声明业务实现完成、不声明客户交付完成、不声明 accepted、integrated 或 production_ready",
]

REQUIRED_REF_TOKENS = [
    "MMC-GOVERNANCE-TEMPLATE-SMOKE-001",
    "mmc-governance-template-smoke-20260625.md",
    "validate_mmc_governance_template_smoke.py",
    "task_pack_ready / local_document_smoke_boundary",
]

FORBIDDEN_CLAIMS = [
    "runtime_verified = true",
    "integration_verified = true",
    "delivery_verified = true",
    "customer_accepted = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    doc_text = read(DOC, failures)
    agents_text = read(MMC_AGENTS, failures)
    plan_text = read(MMC_PLAN, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(STATUS, failures), read(TASKS, failures)])

    if not MMC_REPO.exists():
        failures.append(f"missing MMC repo: {MMC_REPO}")

    if "GlobalCloud Harness Engineering" not in agents_text:
        failures.append("MMC AGENTS missing Harness Engineering positioning")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in MMC smoke evidence: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in MMC implementation plan: {token}")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive MMC claim: {token}")

    result = {
        "gate": "mmc_governance_template_smoke",
        "status": "pass" if not failures else "fail",
        "task_id": "MMC-GOVERNANCE-TEMPLATE-SMOKE-001",
        "target_status_candidate": "task_pack_ready / local_document_smoke_boundary",
        "runtime_verified": False,
        "integration_verified": False,
        "failures": failures,
        "warnings": [
            "This validates MMC governance template smoke only; it does not validate MMC runtime, integration, delivery, accepted, integrated, production, or customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
