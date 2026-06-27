#!/usr/bin/env python3
"""Validate the LOOP capability registry baseline."""

from __future__ import annotations

from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "02-governance/loop/LOOP_CAPABILITY_REGISTRY.md"
MASTER = ROOT / "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md"
README = ROOT / "02-governance/loop/README.md"
SUPERPOWERS_VALIDATOR = ROOT / "tools/kds-sync/validate_superpowers_loop_admission.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_capability_registry: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def require_controlled(text: str, source_path: str) -> None:
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{source_path} missing controlled marker: {phrase}")


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    registry = read(REGISTRY)
    master = read(MASTER)
    readme = read(README)

    require_controlled(registry, "02-governance/loop/LOOP_CAPABILITY_REGISTRY.md")
    require(
        "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]" in registry,
        "registry must keep project-group related_projects",
    )

    for phrase in [
        "LOOP 能力注册表",
        "技能池",
        "工具池",
        "方法池",
        "状态模型",
        "风险分级",
        "注册字段",
        "核心能力族与子能力矩阵",
        "能力族升级规则",
        "快速准入",
        "default_enabled",
        "pilot` 以上状态变化必须有 evidence",
        "降级",
        "停用",
        "废弃",
        "替代",
        "validate_loop_capability_registry.py",
        "loop_document_gate.py",
        "rework_required",
    ]:
        require(phrase in registry, f"registry missing governance phrase: {phrase}")

    for phrase in [
        "fast_admitted",
        "candidate",
        "pilot",
        "controlled",
        "default_enabled",
        "downgraded",
        "disabled",
        "deprecated",
        "superseded",
    ]:
        require(phrase in registry, f"registry missing status: {phrase}")

    for phrase in [
        "capability_id",
        "type",
        "status",
        "risk_level",
        "version_scope",
        "owner",
        "allowed_contexts",
        "forbidden_contexts",
        "evidence_required",
        "validator_or_gate",
        "rollback_or_disable",
        "last_reviewed",
    ]:
        require(phrase in registry, f"registry missing field: {phrase}")

    for phrase in [
        "globalcloud-loop-orchestrator",
        "globalcloud-document-governance",
        "globalcloud-ui-quality-gate",
        "opsx-full-cycle",
        "globalcloud-harness-governance",
        "software-project-assessment",
    ]:
        require(phrase in registry, f"registry missing core skill: {phrase}")

    for phrase in [
        "loop_document_gate.py",
        "check_document_pollution.py",
        "validate_kds_token.py",
        "check_chinese_localization_gate.py",
        "validate_loop_engineering_master_plan.py",
        "validate_loop_capability_registry.py",
        "validate_loop_baseline_sync_readiness.py",
        "validate_loop_engineering_five_direction_implementation.py",
        "validate_loop_round_efficiency_audit.py",
        "validate_continuous_round_substance.py",
        "validate_l3_continuation_guard.py",
        "git status",
        "git diff",
        "git diff --check",
        "document_control.py",
    ]:
        require(phrase in registry, f"registry missing core tool: {phrase}")

    for phrase in [
        "六段式",
        "任务包",
        "evidence",
        "no-write",
        "test_data_lane",
        "candidate_lane",
        "real_business_lane",
        "owner",
        "WAES",
        "Harness",
        "三层评分",
        "分层裁决",
        "受控工程修改",
        "按任务授权",
        "CodeGraph",
        "外部搜索/检索",
        "RAG/语义索引",
        "多智能体并行开发",
        "Agent-Reach",
        "Ontology",
        "Headroom",
        "WAS / Ontology-WAS",
        "OKF/ODF",
        "LCX",
        "WAES-KDS RAG writeback",
        "只读索引",
        "依赖分析",
        "调用图分析",
        "公开资料核验",
        "受控文档召回",
        "分离文件分析",
        "Superpowers LOOP execution discipline",
        "method.superpowers.loop_execution_discipline",
    ]:
        require(phrase in registry, f"registry missing core method: {phrase}")

    for phrase in [
        "method.superpowers.loop_execution_discipline",
        "method/skill wrapper",
        "candidate",
        "medium",
        "SOP + GPCF",
        "planning,tdd,debugging,verification,review,independent_subtasks",
        "auto_commit,auto_push,production_write,cross_repo_write,status_promotion,release,deployment",
        "validate_superpowers_loop_admission.py + validate_loop_project_group_gate_readiness.py",
        "disabled / repair_required",
    ]:
        require(phrase in registry, f"registry missing Superpowers admission field: {phrase}")

    for phrase in [
        "family.codegraph",
        "family.agent_reach",
        "family.ontology",
        "family.was_ontology_was",
        "family.headroom",
        "family.okf_odf",
        "family.lcx",
        "family.waes_kds_rag_writeback",
        "core method family",
        "method/tool family",
        "semantic governance method",
        "cost/runtime measurement method",
        "governance method family",
        "gate/writeback method",
        "controlled/pilot",
        "candidate/pilot",
        "medium/high by sub-capability",
        "controlled with restrictions",
    ]:
        require(phrase in registry, f"registry missing capability family marker: {phrase}")

    for phrase in [
        "只读分析、索引、评估、候选生成可以进入 `controlled`",
        "写回、同步、外部 API、跨仓执行、成本测量、自动修复必须保持 `pilot` 或 `candidate`",
        "`pilot` 以上状态变化必须有 evidence",
        "能力族必须绑定 validator 或 evidence",
        "真实 KDS API 写入",
        "WAES 写回",
        "GFIS 运行层写入",
        "生产 token",
        "生产成本测量",
        "外部 API 写入",
    ]:
        require(phrase in registry, f"registry missing capability family boundary: {phrase}")

    for phrase in [
        "validate_codegraph_*",
        "CodeGraph drift/watchlist evidence",
        "validate_agent_reach_*",
        "Agent-Reach benchmark/review evidence",
        "validate_ontology_*",
        "Ontology contract evidence",
        "validate_was_*",
        "validate_ontology_was_*",
        "source-record intake evidence",
        "validate_headroom_*",
        "Headroom dry-run/proxy/runtime evidence",
        "RAG index evidence",
        "validate_okf_*",
        "ODF gate evidence",
        "validate_headroom_lcx_*",
        "LCX authorization evidence",
        "validate_was_waes_kds_rag_writeback_gate_pack.py",
        "writeback evidence",
    ]:
        require(phrase in registry, f"registry missing capability family evidence binding: {phrase}")

    for phrase in [
        "写入、自动化、跨仓和外部 API 子能力",
        "pilot",
        "candidate",
        "显式任务授权",
    ]:
        require(phrase in registry, f"registry missing sub-capability boundary: {phrase}")

    for phrase in [
        "LOOP_CAPABILITY_REGISTRY.md",
        "技能、工具和方法",
        "快速准入",
        "风险分级",
        "pilot` 以上状态变化必须有 evidence",
        "downgraded",
        "disabled",
        "deprecated",
        "superseded",
        "validate_loop_capability_registry.py",
    ]:
        require(phrase in master, f"master missing capability registry linkage: {phrase}")

    require(
        "LOOP 能力注册表 | 02-governance/loop/LOOP_CAPABILITY_REGISTRY.md" in readme,
        "loop README missing capability registry entry",
    )

    superpowers_validator = read(SUPERPOWERS_VALIDATOR)
    for phrase in [
        "method.superpowers.loop_execution_discipline",
        "planning,tdd,debugging,verification,review,independent_subtasks",
        "auto_commit,auto_push,production_write,cross_repo_write,status_promotion,release,deployment",
        "validate_loop_project_group_gate_readiness.py",
        "superpowers_loop_admission=pass status=candidate",
    ]:
        require(phrase in superpowers_validator, f"Superpowers validator missing phrase: {phrase}")

    forbidden = [
        "能力登记授权 production write",
        "能力登记授权 external API write",
        "能力登记授权 schema sync",
        "能力登记授权 deployment",
        "能力登记授权 commit",
        "能力登记授权 push",
        "能力登记授权 accepted",
        "能力登记授权 integrated",
    ]
    for phrase in forbidden:
        require(phrase not in registry, f"forbidden capability claim present: {phrase}")

    print(
        "loop_capability_registry=pass "
        "pools=skill,tool,method "
        "statuses=fast_admitted,candidate,pilot,controlled,default_enabled,downgraded,disabled,deprecated,superseded "
        "default_enable=risk_tiered pilot_plus_evidence=required "
        "core_methods=CodeGraph,external_search,RAG,multi_agent_parallel "
        "capability_families=CodeGraph,Agent-Reach,Ontology,WAS,Headroom,OKF_ODF,LCX,WAES_KDS_RAG_writeback "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
