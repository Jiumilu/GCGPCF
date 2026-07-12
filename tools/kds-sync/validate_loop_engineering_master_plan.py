#!/usr/bin/env python3
"""Validate the LOOP Engineering master implementation plan baseline."""

from __future__ import annotations

from pathlib import Path

import yaml

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md"
README = ROOT / "02-governance/loop/README.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
AUTONOMY = ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md"
EXECUTION = ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md"
FIVE_DIRECTION = ROOT / "02-governance/loop/LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
CAPABILITY_REGISTRY = ROOT / "02-governance/loop/LOOP_CAPABILITY_REGISTRY.md"
SESSION_MAINLINE_CONTROL = ROOT / "02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md"
PROJECT_REGISTRY = ROOT / "config/project-group-projects.yaml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_engineering_master_plan: {message}")


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
    master = read(MASTER)
    readme = read(README)
    combined_current = "\n".join([read(CONTROL_BOARD), read(LOOP_STATE)])
    autonomy = read(AUTONOMY)
    execution = read(EXECUTION)
    five_direction = read(FIVE_DIRECTION)
    capability_registry = read(CAPABILITY_REGISTRY)
    session_mainline_control = read(SESSION_MAINLINE_CONTROL)
    registry = yaml.safe_load(read(PROJECT_REGISTRY))
    projects = [item["id"] for item in registry["projects"]]

    require_controlled(master, "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md")
    require(
        f"related_projects: [{', '.join(projects)}]" in master,
        f"master plan must keep {len(projects)}-project related_projects scope",
    )

    for phrase in [
        "LOOP 工程体系整体实施规范",
        "权威整体实施基线",
        "基线目标",
        "权威文档层级",
        "体系边界",
        "运行模型",
        "会话主线与跨会话防偏离控制",
        "输出克制",
        "工程执行型 LOOP 决策基线",
        "能力纳入与治理机制",
        "版本基线",
        "路线图",
        "状态升级规则",
        "门禁链",
        "自我提升机制",
        "非声明边界",
        "v1.0 整体实施基线",
        "P0：基线立法",
        "P1：治理债务收敛",
        "P2：证据链一致性",
        "P3：项目群覆盖",
        "P4：真实业务闭环候选",
        "P5：受控自治准入",
        "GlobalCloud 项目群实施方案.md",
        "04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md",
        "04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md",
    ]:
        require(phrase in master, f"master plan missing phrase: {phrase}")

    for phrase in [
        "LOOP_CONTROL_BOARD.md",
        "LOOP_AUTONOMY_POLICY.md",
        "LOOP_EXECUTION_RULES.md",
        "LOOP_ENGINEERING_FIVE_DIRECTION_IMPLEMENTATION.md",
        "LOOP_SESSION_MAINLINE_CONTROL_PACK.md",
        "docs/harness/loop-state.md",
        "docs/harness/loops/loop-round-*.md",
        "docs/harness/evidence/*.{json,md}",
        "validate_loop_engineering_master_plan.py",
        "LOOP_CAPABILITY_REGISTRY.md",
        "validate_loop_capability_registry.py",
        "validate_loop_session_mainline_control.py",
        "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
        "globalcloud-project-group-dev-task-queue-20260626.md",
    ]:
        require(phrase in master, f"master plan missing dependency: {phrase}")

    for phrase in [
        "工程执行型 LOOP",
        "项目群级执行",
        "业务闭环优先",
        "端到端绿色供应链闭环",
        "GFIS 运行层 SOP E2E",
        "test_data_lane",
        "candidate_lane",
        "real_business_lane",
        "owner + WAES + Harness",
        "三层评分",
        "受控工程修改",
        "按任务 Git 授权",
        "当前会话主线优先",
        "handoff evidence",
        "用户确认",
        "DO NOT send optional commentary",
    ]:
        require(phrase in master, f"master plan missing decision baseline: {phrase}")

    for phrase in [
        "session_mainline",
        "owner session",
        "handoff note",
        "mainline_drift_detected",
        "scope_delta",
        "authorization_delta",
        "不得在未授权、未交接、未重新校验范围的情况下",
        "不得因另一个会话存在未完成任务而自动切换主线",
        "没有完整交接证据，只能生成建议，不能执行写入",
        "会话主线边界",
        "会话主线漂移",
        "启动/恢复前置门禁",
        "不得发送 optional commentary",
    ]:
        require(phrase in master, f"master plan missing session mainline control: {phrase}")

    for phrase in [
        "技能池",
        "工具池",
        "方法池",
        "快速准入",
        "fast_admitted",
        "default_enabled",
        "pilot` 以上状态变化必须有 evidence",
        "downgraded",
        "disabled",
        "deprecated",
        "superseded",
        "CodeGraph",
        "外部搜索/检索",
        "RAG/语义索引",
        "多智能体并行开发",
        "只读、分析、检索、规划类子能力",
        "写入、自动执行、跨仓变更、外部 API 写入",
        "@product-design",
        "WAES` 母框架复用",
        "globalcloud-ui-quality-gate",
        "Tool route",
        "Context package",
        "Prompt profile",
        "Design options",
        "Selected option",
        "WAES baseline reuse",
        "UI gate status",
    ]:
        require(phrase in master, f"master plan missing capability baseline: {phrase}")

    for phrase in [
        "source-of-record",
        "runtime primary key",
        "review queue",
        "runtime intake",
        "WAES review",
        "verified artifact",
        "project_group_current_state_baseline_refresh_20260626 = controlled",
        "development_queue_ready = true",
        "dirty_repo_count = 7",
        "trigger_layer_binding_count = 17",
        "dependency_edge_binding_count = 17",
        "accepted",
        "integrated",
        "production_ready",
        "repair_required",
    ]:
        require(phrase in master, f"master plan missing state boundary: {phrase}")

    require(
        "LOOP 工程体系整体实施规范 | 02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md" in readme,
        "loop README missing master plan entry",
    )
    require(
        "LOOP 能力注册表 | 02-governance/loop/LOOP_CAPABILITY_REGISTRY.md" in readme,
        "loop README missing capability registry entry",
    )
    require("status: controlled" in capability_registry, "capability registry missing controlled status")
    require("status: controlled" in session_mainline_control, "session mainline control pack missing controlled status")
    require("L3" in autonomy and "L4" in autonomy and "L5" in autonomy, "autonomy policy missing mode baseline")
    require("Definition of Done" in execution or "完成定义" in execution, "execution rules missing completion definition")
    require("Loop 如何运行" in five_direction and "Loop 如何验证" in five_direction, "five-direction implementation missing operation model")

    for phrase in [
        "real_business_lane=repair_required",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
    ]:
        require(phrase in combined_current, f"current control plane missing status ceiling: {phrase}")

    forbidden = [
        "本文创建 source-of-record",
        "本文创建 runtime primary key",
        "本文证明 UAT",
        "本文证明生产",
        "本文授权 production write",
        "自动标记 accepted",
        "自动标记 integrated",
    ]
    for phrase in forbidden:
        require(phrase not in master, f"forbidden claim present: {phrase}")

    print(
        "loop_engineering_master_plan=pass "
        "baseline=v1.0 authority=master_implementation_plan "
        "roadmap=P0,P1,P2,P3,P4,P5 "
        "status_ceiling=repair_required accepted_allowed=false integrated_allowed=false "
        "runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
