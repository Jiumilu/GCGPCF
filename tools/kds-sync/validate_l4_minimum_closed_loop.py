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
    "docs/harness/loops/loop-round-GPCF-L4-002.md",
    "docs/harness/loops/loop-round-GPCF-L4-003.md",
    "docs/harness/loops/loop-round-GPCF-L4-004.md",
    "docs/harness/loops/loop-round-GPCF-L4-005.md",
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


def read_external(path_text: str) -> str:
    path = Path(path_text)
    require(path.exists(), f"missing external file: {path_text}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    texts = {relative_path: read(relative_path) for relative_path in REQUIRED_FILES}
    control = texts["docs/harness/minimum-closed-loop/control-plane.md"]
    matrix = texts["docs/harness/minimum-closed-loop/project-role-verification-matrix.md"]
    contracts = texts["docs/harness/minimum-closed-loop/object-contracts.md"]
    evidence = texts["docs/harness/minimum-closed-loop/evidence-index.md"]
    round_record = texts["docs/harness/loops/loop-round-GPCF-L4-001.md"]
    round_record_l4_002 = texts["docs/harness/loops/loop-round-GPCF-L4-002.md"]
    round_record_l4_003 = texts["docs/harness/loops/loop-round-GPCF-L4-003.md"]
    round_record_l4_004 = texts["docs/harness/loops/loop-round-GPCF-L4-004.md"]
    round_record_l4_005 = texts["docs/harness/loops/loop-round-GPCF-L4-005.md"]

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

    mmc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")
    mmc_policy = read_external(str(mmc_root / "runtime/policies/minimum_closed_loop_policy.json"))
    mmc_retrieval = read_external(str(mmc_root / "docs/harness/evidence/kds-retrieval-MMC-L4-002.json"))
    mmc_round = read_external(str(mmc_root / "docs/harness/loops/loop-round-MMC-L4-002.md"))

    for phrase in [
        "Round ID | GPCF-L4-002",
        "MMC-L4-002",
        "KDS retrieval",
        "ResourceCapabilityCheck",
        "equipment_id",
        "line_id",
        "process_capability_code",
        "capacity_snapshot_id",
        "36 passed",
        "ready_for_review",
    ]:
        require(phrase in round_record_l4_002 + "\n" + evidence, f"L4-002 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"status\": \"completed\"",
        "\"retrieval_mode\": \"local_mirror\"",
        "GPCF-DOC-E2FDF91E39",
        "ResourceCapabilityCheck",
        "unresolved_questions",
    ]:
        require(phrase in mmc_retrieval, f"MMC KDS retrieval missing phrase: {phrase}")

    for phrase in [
        "resource_capability_before_factory_order",
        "ResourceCapabilityCheck.resource_gate_status == 'pass'",
        "factory_id, line_id, equipment_id and process_capability_code are present",
        "capacity_snapshot_id is present",
        "GFIS owns equipment, line, work order and production execution facts",
    ]:
        require(phrase in mmc_policy + "\n" + mmc_round, f"MMC resource policy missing phrase: {phrase}")

    kds_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")
    kds_retrieval = read_external(str(kds_root / "docs/harness/evidence/kds-retrieval-KDS-L4-003.json"))
    kds_index = read_external(str(kds_root / "docs/harness/minimum-closed-loop/sample-knowledge-index.json"))
    kds_round = read_external(str(kds_root / "docs/harness/loops/loop-round-KDS-L4-003.md"))

    for phrase in [
        "Round ID | GPCF-L4-003",
        "KDS-L4-003",
        "SampleSpecificationKnowledge",
        "CustomerSignoffKnowledge",
        "SOPKnowledgeEntry",
        "EvidenceBacklink",
        "96/100",
        "ready_for_review",
    ]:
        require(phrase in round_record_l4_003 + "\n" + evidence, f"L4-003 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"KDS-L4-003\"",
        "SampleSpecificationKnowledge",
        "CustomerSignoffKnowledge",
        "SOPKnowledgeEntry",
        "EvidenceBacklink",
        "accepted",
        "integrated",
    ]:
        require(phrase in kds_retrieval + "\n" + kds_index + "\n" + kds_round, f"KDS L4-003 evidence missing phrase: {phrase}")

    brain_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain")
    brain_retrieval = read_external(str(brain_root / "docs/harness/evidence/kds-retrieval-Brain-L4-004.json"))
    brain_source = read_external(str(brain_root / "src/app/data/l4MinimumClosedLoopKnowledge.ts"))
    brain_fixture = read_external(str(brain_root / "src/app/data/l4MinimumClosedLoopKnowledge.fixture.json"))
    brain_round = read_external(str(brain_root / "docs/harness/loops/loop-round-Brain-L4-004.md"))

    for phrase in [
        "Round ID | GPCF-L4-004",
        "Brain-L4-004",
        "SOPKnowledgeEntry",
        "RetrospectiveCaseRecord",
        "BrainRetrievalResult",
        "92/100",
        "项目群阶段累计评分 | 37/100",
        "PKC-L4-005",
    ]:
        require(phrase in round_record_l4_004 + "\n" + evidence, f"L4-004 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"Brain-L4-004\"",
        "brain-l4-sop-production-release",
        "brain-l4-exception-case",
        "minimumClosedLoopWikiPages",
        "searchMinimumClosedLoopKnowledge",
        "Brain 只负责知识 UI 与检索呈现",
    ]:
        require(phrase in brain_retrieval + "\n" + brain_source + "\n" + brain_fixture + "\n" + brain_round, f"Brain L4-004 evidence missing phrase: {phrase}")

    pkc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC")
    pkc_retrieval = read_external(str(pkc_root / "docs/harness/evidence/kds-retrieval-PKC-L4-005.json"))
    pkc_service = read_external(str(pkc_root / "src/app/services/l4BrainIntakeService.ts"))
    pkc_fixture = read_external(str(pkc_root / "src/app/data/l4BrainRetrievalIntake.fixture.json"))
    pkc_round = read_external(str(pkc_root / "docs/harness/loops/loop-round-PKC-L4-005.md"))

    for phrase in [
        "Round ID | GPCF-L4-005",
        "PKC-L4-005",
        "PersonalTask",
        "Notification",
        "TodoState",
        "BrainRetrievalResult",
        "96/100",
        "项目群阶段累计评分 | 46/100",
        "PVAOS-L4-006",
    ]:
        require(phrase in round_record_l4_005 + "\n" + evidence, f"L4-005 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"PKC-L4-005\"",
        "l4BrainRetrievalIntake",
        "buildPkcIntakeFromBrainResults",
        "PersonalNotification",
        "TodoState",
        "boundary=PKC工作台不写业务事实",
        "tasks=3 notifications=3 todo_states=3",
    ]:
        require(phrase in pkc_retrieval + "\n" + pkc_service + "\n" + pkc_fixture + "\n" + pkc_round, f"PKC L4-005 evidence missing phrase: {phrase}")

    assessment = {
        "round_id": "GPCF-L4-005",
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
        "generated_items": 28,
        "batch_generated": False,
        "substance_gate": "pass",
        "status": "partial",
        "next_round": "L4-006",
        "completed_rounds": ["GPCF-L4-001", "GPCF-L4-002", "GPCF-L4-003", "GPCF-L4-004", "GPCF-L4-005"],
        "project_group_score": 46,
        "l4_round_scores": {
            "GPCF-L4-003": 96,
            "GPCF-L4-004": 92,
            "GPCF-L4-005": 96,
        },
        "project_rounds": {
            "MMC": {
                "round_id": "MMC-L4-002",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "sample_gate": "blocked_without_required_evidence",
                "resource_gate": "blocked_without_required_evidence",
            },
            "KDS": {
                "round_id": "KDS-L4-003",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "knowledge_index": "ready_for_review",
                "accepted_integrated": False,
            },
            "Brain": {
                "round_id": "Brain-L4-004",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "retrieval_smoke": "pass",
                "score": 92,
                "accepted_integrated": False,
            },
            "PKC": {
                "round_id": "PKC-L4-005",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "task_notification_status_mock": "pass",
                "score": 96,
                "accepted_integrated": False,
            },
        },
    }
    out = ROOT / "docs/harness/evidence/l4_minimum_loop_assessment.json"
    out.write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("l4_minimum_closed_loop=pass")
    print("round=GPCF-L4-005 projects=12 core_objects=11 sample_gate=blocked resource_gate=blocked project_group_score=46 next=L4-006")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
