#!/usr/bin/env python3
"""Validate GlobalCloud Loop governance control documents."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DOCS = [
    ROOT / "02-governance/loop/README.md",
    ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md",
    ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md",
    ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md",
    ROOT / "02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md",
    ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md",
    ROOT / "02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md",
    ROOT / "02-governance/loop/LOOP_GOVERNANCE_ROUND_REVIEW_PLAN.md",
    ROOT / "02-governance/loop/LOOP_RISK_GATE.md",
    ROOT / "02-governance/loop/LOOP_METRICS.md",
    ROOT / "templates/LOOP_ROUND_TEMPLATE.md",
    ROOT / "templates/LOOP_EVIDENCE_TEMPLATE.md",
    ROOT / "templates/LOOP_HANDOFF_TEMPLATE.md",
]

REQUIRED_FRONTMATTER_KEYS = [
    "doc_id:",
    "title:",
    "project:",
    "related_projects:",
    "domain:",
    "status:",
    "version:",
    "owner:",
    "kds_space:",
    "kds_path:",
    "source_path:",
    "sync_direction:",
    "last_reviewed:",
    "supersedes:",
    "superseded_by:",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing required doc: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def validate_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    frontmatter = text[:end]
    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in frontmatter, f"{path.relative_to(ROOT)} missing front matter key {key}")
    require("kds_space: 开发" in frontmatter, f"{path.relative_to(ROOT)} must use KDS 开发 space")


def main() -> int:
    texts: dict[Path, str] = {}
    for path in REQUIRED_DOCS:
        text = read(path)
        validate_frontmatter(path, text)
        texts[path] = text

    policy = texts[ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md"]
    for phrase in [
        "最多 15 轮或 2 小时",
        "L3 final answer guard",
        "3/15",
        "stop_type=none",
        "substantive_rounds",
        "generated_items",
        "batch_generated",
        "substance_gate",
        "Git push",
        "真实 API 写入",
        "真实 KDS TOKEN 写入",
        "accepted",
        "integrated",
    ]:
        require(phrase in policy, f"LOOP_AUTONOMY_POLICY.md missing phrase: {phrase}")

    control = texts[ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"]
    for phrase in [
        "当前 Loop 模式",
        "当前轮次",
        "当前允许动作",
        "当前禁止动作",
        "下一轮候选任务队列",
    ]:
        require(phrase in control, f"LOOP_CONTROL_BOARD.md missing phrase: {phrase}")

    execution = texts[ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md"]
    for phrase in ["AGENTS.md", "LOOP_CONTROL_BOARD.md", "LOOP_AUTONOMY_POLICY.md", "Definition of Done"]:
        require(phrase in execution, f"LOOP_EXECUTION_RULES.md missing phrase: {phrase}")

    round_template = texts[ROOT / "templates/LOOP_ROUND_TEMPLATE.md"]
    for phrase in ["Round ID", "授权边界", "验证命令", "Evidence 清单", "状态判定", "轮次真实性检查", "substantive_round"]:
        require(phrase in round_template, f"LOOP_ROUND_TEMPLATE.md missing phrase: {phrase}")

    skill = read(ROOT / ".codex/skills/globalcloud-loop-orchestrator/SKILL.md")
    for phrase in ["LOOP_CONTROL_BOARD.md", "LOOP_AUTONOMY_POLICY.md", "L3 托管冲刺模式", "validate_l3_continuation_guard.py", "validate_continuous_round_substance.py", "substantive_rounds"]:
        require(phrase in skill, f"loop orchestrator skill missing phrase: {phrase}")

    l3_guard = read(ROOT / "tools/kds-sync/validate_l3_continuation_guard.py")
    for phrase in ["L3 continuation guard", "stop_type", "3/15", "不得 final 收口"]:
        require(phrase in l3_guard, f"validate_l3_continuation_guard.py missing phrase: {phrase}")

    self_correction_guard = read(ROOT / "tools/kds-sync/validate_loop_self_correction_gate.py")
    for phrase in [
        "run_loop_round_efficiency_audit",
        "loop_efficiency",
        "loop_round_efficiency_audit_failed",
        "loop_efficiency_risk",
        "Review Loop round efficiency debt",
    ]:
        require(phrase in self_correction_guard, f"validate_loop_self_correction_gate.py missing phrase: {phrase}")

    phase_goal = texts[ROOT / "02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md"]
    for phrase in [
        "LOOP-GOV-PHASE-20260617",
        "阶段目标",
        "Definition Of Done",
        "validate_loop_governance_phase_goal.py",
        "不替代 GFIS 或其他项目的实施主进程",
        "accepted",
        "integrated",
    ]:
        require(phrase in phase_goal, f"LOOP_GOVERNANCE_PHASE_GOAL.md missing phrase: {phrase}")

    phase_goal_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_phase_goal.py")
    for phrase in [
        "Validate the active Loop governance phase goal and evidence",
        "LOOP-GOV-PHASE-20260617",
        "accepted_integrated_allowed",
        "runtime_primary_key_ready=0",
        "loop_governance_phase_goal=pass",
    ]:
        require(phrase in phase_goal_guard, f"validate_loop_governance_phase_goal.py missing phrase: {phrase}")

    dashboard = texts[ROOT / "02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md"]
    for phrase in [
        "Loop Governance Dashboard",
        "quality_gate",
        "efficiency_risk",
        "self_correction_gate",
        "status_ceiling",
        "This dashboard does not prove source-of-record receipt",
    ]:
        require(phrase in dashboard, f"LOOP_GOVERNANCE_DASHBOARD.md missing phrase: {phrase}")

    dashboard_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_dashboard.py")
    for phrase in [
        "Validate the Loop governance dashboard and dashboard evidence",
        "LOOP-GOV-DASHBOARD-20260617",
        "efficiency_risk",
        "runtime_primary_key_ready=0",
        "loop_governance_dashboard=pass",
    ]:
        require(phrase in dashboard_guard, f"validate_loop_governance_dashboard.py missing phrase: {phrase}")

    efficiency_backlog = texts[ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md"]
    for phrase in [
        "Loop Governance Efficiency Debt Backlog",
        "LEDB-001",
        "LEDB-002",
        "LEDB-003",
        "Review Disposition Template",
        "LEDB-001-RD-001",
        "LOOP-GOV-EFF-DEBT-LOCATOR-20260617",
        "business_status_impact",
        "does not rewrite historical round records in bulk",
        "Closing Conditions",
    ]:
        require(phrase in efficiency_backlog, f"LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md missing phrase: {phrase}")

    efficiency_backlog_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_efficiency_backlog.py")
    for phrase in [
        "Validate the Loop governance efficiency debt backlog",
        "LOOP-GOV-EFF-DEBT-20260617",
        "truth_field_debt=2",
        "five_segment_debt=18",
        "dispositions=",
        "bulk_rewrite_allowed=false",
    ]:
        require(phrase in efficiency_backlog_guard, f"validate_loop_governance_efficiency_backlog.py missing phrase: {phrase}")

    efficiency_locator_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_efficiency_debt_locator.py")
    for phrase in [
        "Validate the Loop governance efficiency debt locator evidence",
        "LOOP-GOV-EFF-DEBT-LOCATOR-20260617",
        "truth_records=",
        "five_segment_records=",
        "business_status_impact=none",
    ]:
        require(phrase in efficiency_locator_guard, f"validate_loop_governance_efficiency_debt_locator.py missing phrase: {phrase}")

    round_review_plan = texts[ROOT / "02-governance/loop/LOOP_GOVERNANCE_ROUND_REVIEW_PLAN.md"]
    for phrase in [
        "Loop Governance Round Review Plan",
        "LOOP-GOV-ROUND-REVIEW-PLAN-20260617",
        "LEDB-001-RP-001",
        "LEDB-002-RP-001",
        "LEDB-003-RP-001",
        "targeted annotation",
        "index-level exception",
        "no_bulk_rewrite",
        "business_status_impact",
        "does not rewrite historical Loop round records in bulk",
    ]:
        require(phrase in round_review_plan, f"LOOP_GOVERNANCE_ROUND_REVIEW_PLAN.md missing phrase: {phrase}")

    round_review_plan_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_round_review_plan.py")
    for phrase in [
        "Validate the Loop governance round review plan and evidence",
        "LOOP-GOV-ROUND-REVIEW-PLAN-20260617",
        "LEDB-001-RP-001",
        "LEDB-002-RP-001",
        "sequence_checkpoint=184",
        "business_status_impact=none",
    ]:
        require(phrase in round_review_plan_guard, f"validate_loop_governance_round_review_plan.py missing phrase: {phrase}")

    substance_guard = read(ROOT / "tools/kds-sync/validate_continuous_round_substance.py")
    for phrase in ["continuous Loop modes L3/L3.5/L4/L5", "substantive_rounds", "generated_items", "batch_generated", "authorization_boundary"]:
        require(phrase in substance_guard, f"validate_continuous_round_substance.py missing phrase: {phrase}")

    efficiency_audit = read(ROOT / "tools/kds-sync/validate_loop_round_efficiency_audit.py")
    for phrase in [
        "Audit Loop round efficiency and substance signals",
        "TRUTH_FIELDS",
        "FIVE_SEGMENT_MARKERS",
        "batch_generated=true rounds counted as substantive",
        "loop_round_efficiency_audit=pass",
    ]:
        require(phrase in efficiency_audit, f"validate_loop_round_efficiency_audit.py missing phrase: {phrase}")

    print("loop governance docs validation passed")
    print(f"docs={len(REQUIRED_DOCS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
