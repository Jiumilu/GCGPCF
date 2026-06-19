#!/usr/bin/env python3
"""Validate GlobalCloud Loop governance control documents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


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


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing required json: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def frontmatter(path: Path, text: str) -> str:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    return text[:end]


def validate_frontmatter(path: Path, text: str) -> None:
    metadata = frontmatter(path, text)
    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in metadata, f"{path.relative_to(ROOT)} missing front matter key {key}")
    require("kds_space: 开发" in metadata, f"{path.relative_to(ROOT)} must use KDS 开发 space")


def require_frontmatter_value(path: Path, text: str, key: str, expected: str) -> None:
    metadata = frontmatter(path, text)
    phrase = f"{key}: {expected}"
    require(phrase in metadata, f"{path.relative_to(ROOT)} front matter must contain {phrase}")


def require_json_value(data: dict[str, Any], dotted_key: str, expected: Any, label: str) -> None:
    current: Any = data
    for key in dotted_key.split("."):
        require(isinstance(current, dict) and key in current, f"{label} missing JSON field {dotted_key}")
        current = current[key]
    require(current == expected, f"{label} JSON field {dotted_key} expected {expected!r}, got {current!r}")


def require_json_list_contains(data: dict[str, Any], key: str, expected_fragment: str, label: str) -> None:
    values = data.get(key)
    require(isinstance(values, list), f"{label} JSON field {key} must be a list")
    require(
        any(isinstance(value, str) and expected_fragment in value for value in values),
        f"{label} JSON field {key} missing fragment {expected_fragment!r}",
    )


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
    phase_goal_json = load_json(ROOT / "docs/harness/evidence/loop-governance-phase-goal-20260617.json")
    require_json_value(phase_goal_json, "evidence_id", "LOOP-GOV-PHASE-20260617", "phase goal evidence")
    require_json_value(
        phase_goal_json,
        "current_status_ceiling.accepted_integrated_allowed",
        False,
        "phase goal evidence",
    )
    require_json_value(
        phase_goal_json,
        "current_status_ceiling.runtime_primary_key_ready",
        0,
        "phase goal evidence",
    )
    require_json_value(phase_goal_json, "current_status_ceiling.review_queue", 0, "phase goal evidence")
    require_json_value(phase_goal_json, "current_status_ceiling.runtime_intake", 0, "phase goal evidence")
    require_json_list_contains(
        phase_goal_json,
        "non_claims",
        "does not create source-of-record",
        "phase goal evidence",
    )
    require_json_list_contains(
        phase_goal_json,
        "non_claims",
        "accepted, or integrated status",
        "phase goal evidence",
    )

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
    dashboard_json = load_json(ROOT / "docs/harness/evidence/loop-governance-dashboard-20260617.json")
    require_json_value(dashboard_json, "evidence_id", "LOOP-GOV-DASHBOARD-20260617", "dashboard evidence")
    require_json_value(dashboard_json, "phase_goal", "LOOP-GOV-PHASE-20260617", "dashboard evidence")
    require_json_value(dashboard_json, "metrics.accepted_integrated_allowed", False, "dashboard evidence")
    require_json_value(dashboard_json, "metrics.runtime_primary_key_ready", 0, "dashboard evidence")
    require_json_value(dashboard_json, "metrics.review_queue", 0, "dashboard evidence")
    require_json_value(dashboard_json, "metrics.runtime_intake", 0, "dashboard evidence")
    require_json_list_contains(
        dashboard_json,
        "non_claims",
        "does not prove source-of-record receipt",
        "dashboard evidence",
    )
    require_json_list_contains(
        dashboard_json,
        "non_claims",
        "accepted, or integrated completion",
        "dashboard evidence",
    )

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
        "truth_field_debt=",
        "five_segment_debt=",
        "dispositions=",
        "bulk_rewrite_allowed=false",
    ]:
        require(phrase in efficiency_backlog_guard, f"validate_loop_governance_efficiency_backlog.py missing phrase: {phrase}")
    efficiency_backlog_json = load_json(ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.json")
    require_json_value(
        efficiency_backlog_json,
        "evidence_id",
        "LOOP-GOV-EFF-DEBT-20260617",
        "efficiency backlog evidence",
    )
    require_json_value(
        efficiency_backlog_json,
        "disposition_template.business_status_impact_required",
        "none",
        "efficiency backlog evidence",
    )
    backlog_item_ids = {item.get("id") for item in efficiency_backlog_json.get("items", [])}
    require(
        {"LEDB-001", "LEDB-002", "LEDB-003", "LEDB-004"}.issubset(backlog_item_ids),
        "efficiency backlog evidence missing required backlog item ids",
    )
    backlog_disposition_ids = {
        item.get("disposition_id") for item in efficiency_backlog_json.get("review_dispositions", [])
    }
    require(
        {"LEDB-001-RD-003", "LEDB-002-RD-002", "LEDB-003-RD-002"}.issubset(backlog_disposition_ids),
        "efficiency backlog evidence missing required review disposition ids",
    )
    require_json_list_contains(
        efficiency_backlog_json,
        "non_claims",
        "does not prove GFIS runtime SOP E2E passed",
        "efficiency backlog evidence",
    )
    require_json_list_contains(
        efficiency_backlog_json,
        "non_claims",
        "accepted, or integrated status",
        "efficiency backlog evidence",
    )

    efficiency_locator_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_efficiency_debt_locator.py")
    for phrase in [
        "Validate the Loop governance efficiency debt locator evidence",
        "LOOP-GOV-EFF-DEBT-LOCATOR-20260617",
        "truth_records=",
        "five_segment_records=",
        "business_status_impact=none",
    ]:
        require(phrase in efficiency_locator_guard, f"validate_loop_governance_efficiency_debt_locator.py missing phrase: {phrase}")
    efficiency_locator_json = load_json(ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.json")
    require_json_value(
        efficiency_locator_json,
        "evidence_id",
        "LOOP-GOV-EFF-DEBT-LOCATOR-20260617",
        "efficiency debt locator evidence",
    )
    require_json_value(
        efficiency_locator_json,
        "scope.no_bulk_rewrite",
        True,
        "efficiency debt locator evidence",
    )
    require_json_value(
        efficiency_locator_json,
        "scope.business_status_impact",
        "none",
        "efficiency debt locator evidence",
    )
    require_json_value(
        efficiency_locator_json,
        "source_signal.max_consecutive_sequence",
        186,
        "efficiency debt locator evidence",
    )
    require_json_list_contains(
        efficiency_locator_json,
        "non_claims",
        "does not prove GFIS runtime SOP E2E passed",
        "efficiency debt locator evidence",
    )
    require_json_list_contains(
        efficiency_locator_json,
        "non_claims",
        "accepted, or integrated status",
        "efficiency debt locator evidence",
    )

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
        "sequence_checkpoint=",
        "business_status_impact=none",
    ]:
        require(phrase in round_review_plan_guard, f"validate_loop_governance_round_review_plan.py missing phrase: {phrase}")
    round_review_plan_json = load_json(ROOT / "docs/harness/evidence/loop-governance-round-review-plan-20260617.json")
    require_json_value(
        round_review_plan_json,
        "evidence_id",
        "LOOP-GOV-ROUND-REVIEW-PLAN-20260617",
        "round review plan evidence",
    )
    require_json_value(
        round_review_plan_json,
        "source_locator",
        "LOOP-GOV-EFF-DEBT-LOCATOR-20260617",
        "round review plan evidence",
    )
    require_json_value(
        round_review_plan_json,
        "controls.no_bulk_rewrite",
        True,
        "round review plan evidence",
    )
    require_json_value(
        round_review_plan_json,
        "controls.business_status_impact",
        "none",
        "round review plan evidence",
    )
    work_package_ids = {item.get("package_id") for item in round_review_plan_json.get("work_packages", [])}
    require(
        {"LEDB-001-RP-001", "LEDB-002-RP-001", "LEDB-003-RP-001"}.issubset(work_package_ids),
        "round review plan evidence missing required work package ids",
    )
    require_json_list_contains(
        round_review_plan_json,
        "non_claims",
        "does not prove GFIS runtime SOP E2E passed",
        "round review plan evidence",
    )
    require_json_list_contains(
        round_review_plan_json,
        "non_claims",
        "accepted, or integrated status",
        "round review plan evidence",
    )

    five_segment_review_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_five_segment_review.py")
    for phrase in [
        "Validate the Loop governance five-segment review evidence",
        "LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617",
        "LEDB-002-RD-002",
        "reviewed_rounds=5",
        "targeted_annotation_ready=3",
        "business_status_impact=none",
    ]:
        require(phrase in five_segment_review_guard, f"validate_loop_governance_five_segment_review.py missing phrase: {phrase}")
    five_segment_review_json = load_json(ROOT / "docs/harness/evidence/loop-governance-five-segment-review-20260617.json")
    require_json_value(
        five_segment_review_json,
        "evidence_id",
        "LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617",
        "five-segment review evidence",
    )
    require_json_value(five_segment_review_json, "disposition_id", "LEDB-002-RD-002", "five-segment review evidence")
    require_json_value(five_segment_review_json, "scope.reviewed_rounds", 5, "five-segment review evidence")
    require_json_value(five_segment_review_json, "scope.no_bulk_rewrite", True, "five-segment review evidence")
    require_json_value(
        five_segment_review_json,
        "scope.business_status_impact",
        "none",
        "five-segment review evidence",
    )
    five_segment_decisions = {item.get("decision") for item in five_segment_review_json.get("round_dispositions", [])}
    require(
        {"targeted_annotation_ready", "index_level_exception"}.issubset(five_segment_decisions),
        "five-segment review evidence missing required disposition decisions",
    )
    require_json_list_contains(
        five_segment_review_json,
        "non_claims",
        "does not prove GFIS runtime SOP E2E passed",
        "five-segment review evidence",
    )
    require_json_list_contains(
        five_segment_review_json,
        "non_claims",
        "accepted, or integrated status",
        "five-segment review evidence",
    )

    truth_field_review_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_truth_field_review.py")
    for phrase in [
        "Validate the Loop governance truth-field review evidence",
        "LOOP-GOV-TRUTH-FIELD-REVIEW-20260617",
        "LEDB-001-RD-003",
        "reviewed_rounds=6",
        "index_level_exception=5",
        "historical_annotation_present=1",
        "hard_missing_truth_fields=0",
        "business_status_impact=none",
    ]:
        require(phrase in truth_field_review_guard, f"validate_loop_governance_truth_field_review.py missing phrase: {phrase}")
    truth_field_review_json = load_json(ROOT / "docs/harness/evidence/loop-governance-truth-field-review-20260617.json")
    require_json_value(
        truth_field_review_json,
        "evidence_id",
        "LOOP-GOV-TRUTH-FIELD-REVIEW-20260617",
        "truth-field review evidence",
    )
    require_json_value(truth_field_review_json, "disposition_id", "LEDB-001-RD-003", "truth-field review evidence")
    require_json_value(truth_field_review_json, "scope.reviewed_rounds", 6, "truth-field review evidence")
    require_json_value(truth_field_review_json, "scope.no_bulk_rewrite", True, "truth-field review evidence")
    require_json_value(
        truth_field_review_json,
        "scope.business_status_impact",
        "none",
        "truth-field review evidence",
    )
    truth_field_decisions = {item.get("decision") for item in truth_field_review_json.get("round_dispositions", [])}
    require(
        {"index_level_exception", "historical_annotation_present"}.issubset(truth_field_decisions),
        "truth-field review evidence missing required disposition decisions",
    )
    require_json_list_contains(
        truth_field_review_json,
        "non_claims",
        "does not prove GFIS runtime SOP E2E passed",
        "truth-field review evidence",
    )
    require_json_list_contains(
        truth_field_review_json,
        "non_claims",
        "accepted, or integrated status",
        "truth-field review evidence",
    )

    sequence_checkpoint_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_sequence_checkpoint.py")
    for phrase in [
        "Validate the Loop governance long-sequence checkpoint evidence",
        "LOOP-GOV-SEQUENCE-CHECKPOINT-20260619",
        "LEDB-003-RD-002",
        "checkpoint_interval_rounds=25",
        "next_required_checkpoint_at=200",
        "business_status_impact=none",
    ]:
        require(phrase in sequence_checkpoint_guard, f"validate_loop_governance_sequence_checkpoint.py missing phrase: {phrase}")
    sequence_checkpoint_json = load_json(ROOT / "docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.json")
    require_json_value(
        sequence_checkpoint_json,
        "evidence_id",
        "LOOP-GOV-SEQUENCE-CHECKPOINT-20260619",
        "sequence checkpoint evidence",
    )
    require_json_value(sequence_checkpoint_json, "disposition_id", "LEDB-003-RD-002", "sequence checkpoint evidence")
    require_json_value(
        sequence_checkpoint_json,
        "checkpoint_policy.checkpoint_interval_rounds",
        25,
        "sequence checkpoint evidence",
    )
    require_json_value(
        sequence_checkpoint_json,
        "checkpoint_policy.next_required_checkpoint_at",
        200,
        "sequence checkpoint evidence",
    )
    require_json_value(sequence_checkpoint_json, "scope.no_bulk_rewrite", True, "sequence checkpoint evidence")
    require_json_value(
        sequence_checkpoint_json,
        "scope.business_status_impact",
        "none",
        "sequence checkpoint evidence",
    )
    require_json_list_contains(
        sequence_checkpoint_json,
        "non_claims",
        "does not prove GFIS runtime SOP E2E passed",
        "sequence checkpoint evidence",
    )
    require_json_list_contains(
        sequence_checkpoint_json,
        "non_claims",
        "accepted, or integrated status",
        "sequence checkpoint evidence",
    )

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

    loop_document_gate = read(ROOT / "tools/kds-sync/loop_document_gate.py")
    for phrase in [
        "Evaluate the Loop document governance gate",
        "--check-only",
        "--no-write-report",
        "count_unique_mirror_docs",
        "local_mirror_unique_docs",
        "kds_md < local_mirror_unique_docs",
        "write_report(summary, command_results)",
    ]:
        require(phrase in loop_document_gate, f"loop_document_gate.py missing phrase: {phrase}")

    evidence_discovery_chain = read(ROOT / "tools/kds-sync/validate_evidence_discovery_chain.py")
    for phrase in [
        "Report evidence discovery drift across README, local index, and KDS mirror",
        "TRACKED_PREFIXES",
        "missing_local=",
        "missing_mirror=",
        "business_status_impact=none",
        "does_not_prove_real_kds_writeback_or_accepted_integrated",
    ]:
        require(phrase in evidence_discovery_chain, f"validate_evidence_discovery_chain.py missing phrase: {phrase}")

    current_window_disposition_guard = read(ROOT / "tools/kds-sync/validate_loop_governance_current_window_disposition.py")
    for phrase in [
        "Validate the Loop governance current-window disposition evidence",
        "LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619",
        "LEDB-001-RD-005",
        "LEDB-002-RD-004",
        "index_level_shell_exception",
        "targeted_annotation_ready",
        "business_status_impact=none",
        "loop_governance_current_window_disposition=pass",
    ]:
        require(
            phrase in current_window_disposition_guard,
            f"validate_loop_governance_current_window_disposition.py missing phrase: {phrase}",
        )

    current_window_review_path = ROOT / "docs/harness/evidence/loop-governance-current-window-review-20260619.md"
    current_window_review = read(current_window_review_path)
    require_frontmatter_value(
        current_window_review_path,
        current_window_review,
        "source_path",
        "docs/harness/evidence/loop-governance-current-window-review-20260619.md",
    )
    current_window_review_json = load_json(ROOT / "docs/harness/evidence/loop-governance-current-window-review-20260619.json")
    require_json_value(
        current_window_review_json,
        "evidence_id",
        "LOOP-GOV-CURRENT-WINDOW-REVIEW-20260619",
        "current-window review evidence",
    )
    require_json_value(current_window_review_json, "controls.no_bulk_rewrite", True, "current-window review evidence")
    require_json_value(
        current_window_review_json,
        "controls.business_status_impact",
        "none",
        "current-window review evidence",
    )
    require(
        len(current_window_review_json.get("affected_truth_field_records", [])) == 2,
        "current-window review evidence must list 2 affected truth-field records",
    )
    require(
        len(current_window_review_json.get("affected_five_segment_records", [])) == 7,
        "current-window review evidence must list 7 affected five-segment records",
    )
    review_disposition_ids = {
        item.get("disposition_id") for item in current_window_review_json.get("review_dispositions", [])
    }
    require(
        {"LEDB-001-RD-004", "LEDB-002-RD-003"}.issubset(review_disposition_ids),
        "current-window review evidence missing required disposition ids",
    )
    require(
        "does not prove GFIS runtime SOP E2E passed" in current_window_review,
        "current-window review evidence missing GFIS non-claim",
    )

    current_window_disposition_path = ROOT / "docs/harness/evidence/loop-governance-current-window-disposition-20260619.md"
    current_window_disposition = read(current_window_disposition_path)
    require_frontmatter_value(
        current_window_disposition_path,
        current_window_disposition,
        "source_path",
        "docs/harness/evidence/loop-governance-current-window-disposition-20260619.md",
    )
    current_window_disposition_json = load_json(
        ROOT / "docs/harness/evidence/loop-governance-current-window-disposition-20260619.json"
    )
    require_json_value(
        current_window_disposition_json,
        "evidence_id",
        "LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619",
        "current-window disposition evidence",
    )
    require_json_value(
        current_window_disposition_json,
        "scope.truth_records_reviewed",
        2,
        "current-window disposition evidence",
    )
    require_json_value(
        current_window_disposition_json,
        "scope.five_segment_records_reviewed",
        7,
        "current-window disposition evidence",
    )
    require_json_value(
        current_window_disposition_json,
        "scope.no_bulk_rewrite",
        True,
        "current-window disposition evidence",
    )
    require_json_value(
        current_window_disposition_json,
        "scope.business_status_impact",
        "none",
        "current-window disposition evidence",
    )
    disposition_ids = {
        item.get("disposition_id") for item in current_window_disposition_json.get("review_dispositions", [])
    }
    require(
        {"LEDB-001-RD-005", "LEDB-002-RD-004"}.issubset(disposition_ids),
        "current-window disposition evidence missing required disposition ids",
    )
    disposition_decisions = {
        item.get("decision")
        for item in (
            current_window_disposition_json.get("truth_field_dispositions", [])
            + current_window_disposition_json.get("five_segment_dispositions", [])
        )
    }
    require(
        {"index_level_shell_exception", "targeted_annotation_ready"}.issubset(disposition_decisions),
        "current-window disposition evidence missing required disposition decisions",
    )
    require(
        "does not prove GFIS runtime SOP E2E passed" in current_window_disposition,
        "current-window disposition evidence missing GFIS non-claim",
    )

    evidence_index = read(ROOT / "docs/harness/evidence/evidence-index.md")
    for phrase in [
        "Base Knowledge / ODF Evidence Registry",
        "base-knowledge-closure-score-dry-run-summary-20260618.md",
        "base-knowledge-writeback-candidate-ledger-20260618.md",
        "base-knowledge-committee-review-queue-20260619.md",
        "base-knowledge-human-confirmation-queue-20260619.md",
        "kds-md-okf-odf-full-closure-report-20260619.md",
        "odf-phase6-manual-confirmation-workbench-20260618.md",
        "odf-phase7-small-batch-ledger-20260619.md",
        "odf-phase8-drift-monitoring-report-20260619.md",
        "odf-phase9-dynamic-source-stabilization-report-20260619.md",
        "does not perform or prove real KDS API writeback",
        "accepted, or integrated status",
    ]:
        require(phrase in evidence_index, f"evidence-index.md missing Base Knowledge / ODF registry phrase: {phrase}")

    print("loop governance docs validation passed")
    print(f"docs={len(REQUIRED_DOCS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
