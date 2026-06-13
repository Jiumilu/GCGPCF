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
    "docs/harness/loops/loop-round-GPCF-L4-006.md",
    "docs/harness/loops/loop-round-GPCF-L4-007.md",
    "docs/harness/loops/loop-round-GPCF-L4-008.md",
    "docs/harness/loops/loop-round-GPCF-L4-009.md",
    "docs/harness/loops/loop-round-GPCF-L4-010.md",
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
    round_record_l4_006 = texts["docs/harness/loops/loop-round-GPCF-L4-006.md"]
    round_record_l4_007 = texts["docs/harness/loops/loop-round-GPCF-L4-007.md"]
    round_record_l4_008 = texts["docs/harness/loops/loop-round-GPCF-L4-008.md"]
    round_record_l4_009 = texts["docs/harness/loops/loop-round-GPCF-L4-009.md"]
    round_record_l4_010 = texts["docs/harness/loops/loop-round-GPCF-L4-010.md"]

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

    pvaos_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS")
    pvaos_retrieval = read_external(str(pvaos_root / "docs/harness/evidence/kds-retrieval-PVAOS-L4-006.json"))
    pvaos_service = read_external(str(pvaos_root / "src/app/services/l4OrganizationPartnerBaselineService.ts"))
    pvaos_fixture = read_external(str(pvaos_root / "src/app/data/l4OrganizationPartnerBaseline.fixture.json"))
    pvaos_round = read_external(str(pvaos_root / "docs/harness/loops/loop-round-PVAOS-L4-006.md"))

    for phrase in [
        "Round ID | GPCF-L4-006",
        "PVAOS-L4-006",
        "Tenant",
        "Organization",
        "Partner",
        "ProjectSpace",
        "PermissionBoundary",
        "96/100",
        "项目群阶段累计评分 | 55/100",
        "GPC-L4-007",
    ]:
        require(phrase in round_record_l4_006 + "\n" + evidence, f"L4-006 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"PVAOS-L4-006\"",
        "l4OrganizationPartnerBaseline",
        "buildOrganizationPartnerBaselineDryRun",
        "GPC.organization_partner_input",
        "WAES.permission_boundary_audit",
        "PVAOS只提供租户/组织/伙伴/项目空间/权限边界输入",
        "tenants=1 organizations=2 partners=1 project_spaces=1 permission_boundaries=1",
    ]:
        require(
            phrase in pvaos_retrieval + "\n" + pvaos_service + "\n" + pvaos_fixture + "\n" + pvaos_round,
            f"PVAOS L4-006 evidence missing phrase: {phrase}",
        )

    gpc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC")
    gpc_retrieval = read_external(str(gpc_root / "docs/harness/evidence/kds-retrieval-GPC-L4-007.json"))
    gpc_fixture = read_external(str(gpc_root / "l4_contracts/gpc_l4_platform_order_contract.fixture.json"))
    gpc_validator = read_external(str(gpc_root / "scripts/validate_gpc_l4_platform_contract.py"))
    gpc_round = read_external(str(gpc_root / "docs/harness/loops/loop-round-GPC-L4-007.md"))

    for phrase in [
        "Round ID | GPCF-L4-007",
        "GPC-L4-007",
        "PlatformOrder",
        "QuoteReviewContract",
        "SampleRequest",
        "SampleApproval",
        "ProductionRelease",
        "ProofOfDelivery",
        "96/100",
        "项目群阶段累计评分 | 64/100",
        "GFIS-L4-008",
    ]:
        require(phrase in round_record_l4_007 + "\n" + evidence, f"L4-007 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"GPC-L4-007\"",
        "PlatformOrder cannot create FactoryOrder directly",
        "ProofOfDelivery cannot be marked delivered without receiver evidence",
        "GPC must not write GFIS factory execution facts",
        "GFIS.factory_order_input_after_release",
        "WAES.sample_release_gate",
        "KDS.knowledge_backlink_candidate",
        "orders=1 sample_requests=1 sample_approvals=1 production_releases=1 pod_records=1",
    ]:
        require(
            phrase in gpc_retrieval + "\n" + gpc_fixture + "\n" + gpc_validator + "\n" + gpc_round,
            f"GPC L4-007 evidence missing phrase: {phrase}",
        )

    gfis_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")
    gfis_retrieval = read_external(str(gfis_root / "docs/harness/evidence/kds-retrieval-GFIS-L4-008.json"))
    gfis_fixture = read_external(str(gfis_root / "gcfis_demo/field_samples/gfis_l4_factory_sample_order_readonly.json"))
    gfis_validator = read_external(str(gfis_root / "scripts/validate_gfis_l4_factory_sample_order_readonly.py"))
    gfis_round = read_external(str(gfis_root / "docs/harness/loops/loop-round-GFIS-L4-008.md"))

    for phrase in [
        "Round ID | GPCF-L4-008",
        "GFIS-L4-008",
        "FormulaResearch",
        "SampleWorkOrder",
        "FactoryOrder",
        "WorkOrder",
        "QualityInventoryBatch",
        "Shipment",
        "96/100",
        "项目群阶段累计评分 | 73/100",
        "XiaoC-L4-009",
    ]:
        require(phrase in round_record_l4_008 + "\n" + evidence, f"L4-008 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"GFIS-L4-008\"",
        "GFIS owns formula research",
        "GFIS does not own customer SampleApproval or ProofOfDelivery",
        "approved SampleApproval, approved ProductionRelease and WAES gate confirmed",
        "must not run bench migrate",
        "formula_research=1 sample_work_orders=1 factory_orders=1 work_orders=1 quality_inventory_batches=1 shipments=1",
    ]:
        require(
            phrase in gfis_retrieval + "\n" + gfis_fixture + "\n" + gfis_validator + "\n" + gfis_round,
            f"GFIS L4-008 evidence missing phrase: {phrase}",
        )

    xiaoc_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC")
    xiaoc_retrieval = read_external(str(xiaoc_root / "docs/harness/evidence/kds-retrieval-XiaoC-L4-009.json"))
    xiaoc_fixture = read_external(str(xiaoc_root / "l4_orchestration/xiaoc_l4_agent_orchestration_dry_run.fixture.json"))
    xiaoc_validator = read_external(str(xiaoc_root / "scripts/validate_xiaoc_l4_agent_orchestration.mjs"))
    xiaoc_round = read_external(str(xiaoc_root / "docs/harness/loops/loop-round-XiaoC-L4-009.md"))

    for phrase in [
        "Round ID | GPCF-L4-009",
        "XiaoC-L4-009",
        "TaskBreakdown",
        "ModelRoute",
        "AgentDispatchPlan",
        "AgentResultAggregation",
        "95/100",
        "项目群阶段累计评分 | 81/100",
        "XGD-L4-010",
    ]:
        require(phrase in round_record_l4_009 + "\n" + evidence, f"L4-009 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"XiaoC-L4-009\"",
        "TaskBreakdown",
        "ModelRoute",
        "AgentDispatchPlan",
        "AgentResultAggregation",
        "XiaoC does not write business facts",
        "bypass_waes",
        "task_breakdowns=5 model_routes=5 agent_dispatches=5 audit_candidates=1",
    ]:
        require(
            phrase in xiaoc_retrieval + "\n" + xiaoc_fixture + "\n" + xiaoc_validator + "\n" + xiaoc_round,
            f"XiaoC L4-009 evidence missing phrase: {phrase}",
        )

    xgd_root = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD")
    xgd_retrieval = read_external(str(xgd_root / "docs/harness/evidence/kds-retrieval-XGD-L4-010.json"))
    xgd_fixture = read_external(str(xgd_root / "l4_analysis/xgd_l4_risk_analysis_dry_run.fixture.json"))
    xgd_validator = read_external(str(xgd_root / "scripts/validate_xgd_l4_risk_analysis.mjs"))
    xgd_round = read_external(str(xgd_root / "docs/harness/loops/loop-round-XGD-L4-010.md"))

    for phrase in [
        "Round ID | GPCF-L4-010",
        "XGD-L4-010",
        "RiskAnalysis",
        "BottleneckProjection",
        "RootCauseHypothesis",
        "ReliabilityAssessment",
        "RecommendationPacket",
        "95/100",
        "项目群阶段累计评分 | 88/100",
        "XiaoG-L4-011",
    ]:
        require(phrase in round_record_l4_010 + "\n" + evidence, f"L4-010 GPCF evidence missing phrase: {phrase}")

    for phrase in [
        "\"retrieval_mode\": \"local_mirror\"",
        "\"round_id\": \"XGD-L4-010\"",
        "RiskAnalysis",
        "BottleneckProjection",
        "ReliabilityAssessment",
        "RecommendationPacket",
        "XGD outputs analysis, recommendations and projections only",
        "XGD does not approve business decisions",
        "risk_analysis=3 global_projection=2 reliability_assessments=1 recommendation_packets=1",
    ]:
        require(
            phrase in xgd_retrieval + "\n" + xgd_fixture + "\n" + xgd_validator + "\n" + xgd_round,
            f"XGD L4-010 evidence missing phrase: {phrase}",
        )

    assessment = {
        "round_id": "GPCF-L4-010",
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
        "generated_items": 58,
        "batch_generated": False,
        "substance_gate": "pass",
        "status": "partial",
        "next_round": "L4-011",
        "completed_rounds": ["GPCF-L4-001", "GPCF-L4-002", "GPCF-L4-003", "GPCF-L4-004", "GPCF-L4-005", "GPCF-L4-006", "GPCF-L4-007", "GPCF-L4-008", "GPCF-L4-009", "GPCF-L4-010"],
        "project_group_score": 88,
        "l4_round_scores": {
            "GPCF-L4-003": 96,
            "GPCF-L4-004": 92,
            "GPCF-L4-005": 96,
            "GPCF-L4-006": 96,
            "GPCF-L4-007": 96,
            "GPCF-L4-008": 96,
            "GPCF-L4-009": 95,
            "GPCF-L4-010": 95,
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
            "PVAOS": {
                "round_id": "PVAOS-L4-006",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "organization_partner_permission_baseline": "pass",
                "score": 96,
                "accepted_integrated": False,
            },
            "GPC": {
                "round_id": "GPC-L4-007",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "platform_order_contract": "pass",
                "score": 96,
                "accepted_integrated": False,
            },
            "GFIS": {
                "round_id": "GFIS-L4-008",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "factory_sample_order_readonly": "pass",
                "score": 96,
                "accepted_integrated": False,
            },
            "XiaoC": {
                "round_id": "XiaoC-L4-009",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "agent_orchestration_dry_run": "pass",
                "score": 95,
                "accepted_integrated": False,
            },
            "XGD": {
                "round_id": "XGD-L4-010",
                "status": "ready_for_review",
                "kds_retrieval": "completed",
                "risk_analysis_dry_run": "pass",
                "score": 95,
                "accepted_integrated": False,
            },
        },
    }
    out = ROOT / "docs/harness/evidence/l4_minimum_loop_assessment.json"
    out.write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("l4_minimum_closed_loop=pass")
    print("round=GPCF-L4-010 projects=12 core_objects=11 sample_gate=blocked resource_gate=blocked project_group_score=88 next=L4-011")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
