#!/usr/bin/env python3
"""Validate the boundary between Loop governance and implementation work."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOUNDARY_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md"
ROLE_DOC = ROOT / "02-governance/gpcf-role-boundary.md"
METRICS_DOC = ROOT / "02-governance/loop/LOOP_METRICS.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
ORCHESTRATOR_SKILL = ROOT / ".codex/skills/globalcloud-loop-orchestrator/SKILL.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def validate_controlled_doc(text: str, rel_path: str) -> None:
    require(text.startswith("---\n"), f"{rel_path} missing front matter")
    for phrase in [
        "doc_id:",
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {rel_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{rel_path} missing controlled marker: {phrase}")


def main() -> int:
    boundary = read(BOUNDARY_DOC)
    role = read(ROLE_DOC)
    metrics = read(METRICS_DOC)
    control = read(CONTROL_BOARD)
    status = read(STATUS_MATRIX)
    loop_state = read(LOOP_STATE)
    skill = read(ORCHESTRATOR_SKILL)

    validate_controlled_doc(boundary, "02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md")

    for phrase in [
        "implementation main process",
        "governance process",
        "Improve Loop quality, efficiency, safety, and self-correction",
        "Must not create or substitute real business facts",
        "must reject these patterns",
        "Request packages, templates, README files, or owner handoff packages being counted as source-of-record",
        "Batch-generated rounds",
        "Governance Definition Of Done",
        "does not mean the implementation main process has completed",
    ]:
        require(phrase in boundary, f"boundary doc missing phrase: {phrase}")

    for phrase in [
        "跨项目收口",
        "直接替代项目微循环",
        "修改项目仓业务内容",
        "未审计完成时标记 integrated",
        "任何角色不得在无 evidence 支持下升级项目状态",
        "人工确认是 accepted 状态的唯一入口",
    ]:
        require(phrase in role, f"role boundary missing phrase: {phrase}")

    for phrase in [
        "指标不得被用来掩盖未完成事实",
        "文档完整不等于 UAT、生产、外部联调或客户满意已经完成",
        "只有用户确认和 Harness 门禁共同满足时，才可能进入 `accepted` 或 `integrated`",
    ]:
        require(phrase in metrics, f"metrics doc missing phrase: {phrase}")

    for phrase in [
        "本技能是 Loop 启动与续跑入口。它只做编排",
        "实际文档治理、开发执行、验收判定仍由对应技能负责",
        "不自动标记 `accepted` 或 `integrated`",
        "默认权限：允许读取和生成建议",
        "只有用户明确授权时才修改文件",
    ]:
        require(phrase in skill, f"orchestrator skill missing phrase: {phrase}")

    combined_status = "\n".join([control, status, loop_state])
    for phrase in [
        "GFIS",
        "GPCF",
        "repair_required",
        "partial_repair",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
    ]:
        require(phrase in combined_status, f"current status missing governance-safe marker: {phrase}")

    forbidden_positive_claims = [
        "GFIS 运行层已 accepted",
        "GFIS 运行层已 integrated",
        "GFIS 运行层生产就绪",
        "GFIS SOP E2E 已完成",
        "source-record 模板等于真实源记录",
        "请求包等于真实源记录",
    ]
    for phrase in forbidden_positive_claims:
        require(phrase not in combined_status, f"forbidden positive claim present: {phrase}")

    print(
        "loop_governance_role_boundary=pass "
        "boundary_doc=controlled governance_process=bounded implementation_process=separate "
        "quality_target=present efficiency_target=present self_improvement_target=present "
        "status_ceiling=repair_or_partial accepted_integrated_claim=0 "
        "runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
