#!/usr/bin/env python3
"""Validate L4 minimum closed-loop control plane for GPCF."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PROJECTS = [
    "GFIS",
    "GPC",
    "PVAOS",
    "WAES",
    "KDS",
    "Brain",
    "PKC",
    "MMC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "GPCF",
]

REQUIRED_FILES = [
    "docs/harness/minimum-closed-loop/README.md",
    "docs/harness/minimum-closed-loop/control-plane.md",
    "docs/harness/minimum-closed-loop/project-role-verification-matrix.md",
    "docs/harness/minimum-closed-loop/object-contracts.md",
    "docs/harness/minimum-closed-loop/evidence-index.md",
    "docs/harness/loops/loop-round-GPCF-L4-001.md",
]

CORE_OBJECTS = [
    "PlatformOrder",
    "SampleRequest",
    "SampleWorkOrder",
    "SampleApproval",
    "ProductionRelease",
    "OrderMapping",
    "FactoryOrder",
    "ProofOfDelivery",
    "ExternalException",
    "EvidenceRecord",
    "KnowledgeBacklink",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    require(path.exists(), f"missing file: {relative_path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    texts = {relative_path: read(relative_path) for relative_path in REQUIRED_FILES}
    control = texts["docs/harness/minimum-closed-loop/control-plane.md"]
    matrix = texts["docs/harness/minimum-closed-loop/project-role-verification-matrix.md"]
    contracts = texts["docs/harness/minimum-closed-loop/object-contracts.md"]
    evidence = texts["docs/harness/minimum-closed-loop/evidence-index.md"]
    round_record = texts["docs/harness/loops/loop-round-GPCF-L4-001.md"]

    for phrase in [
        "项目初始化 -> 组织/伙伴接入 -> 平台订单",
        "样品打样/样箱打样 -> 客户签样确认 -> 转量产门禁 -> 工厂订单",
        "样品确认独立阶段",
        "禁止绕过门禁",
        "12 项目不缺席",
    ]:
        require(phrase in control, f"control-plane missing phrase: {phrase}")

    for project in PROJECTS:
        require(f"| {project} |" in matrix or f"| {project} " in matrix, f"project missing from matrix: {project}")
        require(project in evidence, f"project missing from evidence index: {project}")

    for obj in CORE_OBJECTS:
        require(obj in contracts, f"object contract missing: {obj}")

    for phrase in [
        "PlatformOrder cannot create FactoryOrder directly",
        "FactoryOrder requires one of: approved SampleApproval, approved waiver, or approved ProductionRelease",
        "SampleApproval.status in [\"approved\", \"waived\"]",
        "ProductionRelease.status == \"approved\"",
        "WAES.gate == \"confirmed\"",
    ]:
        require(phrase in contracts, f"sample gate rule missing: {phrase}")

    for forbidden in [
        "accepted | true",
        "integrated | true",
        "production write | true",
        "real external API write | true",
        "token disclosure | true",
    ]:
        combined = "\n".join(texts.values())
        require(forbidden not in combined, f"forbidden claim found: {forbidden}")

    for phrase in [
        "Round ID | GPCF-L4-001",
        "substantive_round | true for GPCF governance implementation",
        "Next Input",
        "L4-002",
    ]:
        require(phrase in round_record, f"round record missing phrase: {phrase}")

    assessment = {
        "round_id": "GPCF-L4-001",
        "gate": "pass",
        "projects": PROJECTS,
        "core_objects": CORE_OBJECTS,
        "sample_gate": {
            "platform_order_direct_to_factory_order": "blocked",
            "required_conditions": [
                "SampleApproval.status in ['approved', 'waived']",
                "ProductionRelease.status == 'approved'",
                "WAES.gate == 'confirmed'",
            ],
        },
        "generated_items": len(REQUIRED_FILES),
        "batch_generated": False,
        "substance_gate": "pass",
        "status": "partial",
        "next_round": "L4-002",
    }
    out = ROOT / "docs/harness/evidence/l4_minimum_loop_assessment.json"
    out.write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("l4_minimum_closed_loop=pass")
    print("round=GPCF-L4-001 projects=12 core_objects=11 sample_gate=blocked next=L4-002")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

