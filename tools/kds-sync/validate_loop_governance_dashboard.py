#!/usr/bin/env python3
"""Validate the Loop governance dashboard and dashboard evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md"
PHASE_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md"
LOOP_README = ROOT / "02-governance/loop/README.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-dashboard-20260617.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-dashboard-20260617.md"
EVIDENCE_README = ROOT / "docs/harness/evidence/README.md"
EVIDENCE_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"
EFFICIENCY_BACKLOG = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.json"
SELF_CORRECTION = ROOT / "docs/harness/evidence/loop_self_correction_assessment.json"
PHASE_EVIDENCE = ROOT / "docs/harness/evidence/loop-governance-phase-goal-20260617.json"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_controlled(text: str, source_path: str) -> None:
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{source_path} missing controlled marker: {phrase}")


def self_correction_efficiency_risk(self_correction: dict) -> str | None:
    risk = self_correction.get("loop_efficiency", {}).get("metrics", {}).get("risk")
    if risk:
        return risk
    loop_efficiency = self_correction.get("loop_efficiency", {})
    meaning = loop_efficiency.get("governance_meaning", "")
    blockers = set(self_correction.get("blockers", []))
    if self_correction.get("gate") == "blocked" and (
        "review_required" in meaning
        or "loop_round_efficiency_audit_failed" in blockers
        or "loop_round_efficiency_review_required" in blockers
    ):
        return "review_required"
    return None


def main() -> int:
    dashboard = read(DASHBOARD_DOC)
    phase = read(PHASE_DOC)
    loop_readme = read(LOOP_README)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)
    efficiency_backlog = load_json(EFFICIENCY_BACKLOG)
    self_correction = load_json(SELF_CORRECTION)
    phase_evidence = load_json(PHASE_EVIDENCE)
    combined_status = "\n".join([read(CONTROL_BOARD), read(LOOP_STATE), read(STATUS_MATRIX)])

    require_controlled(dashboard, "02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md")
    require_controlled(evidence_md, "docs/harness/evidence/loop-governance-dashboard-20260617.md")

    for phrase in [
        "Loop Governance Dashboard",
        "quality_gate",
        "efficiency_risk",
        "self_correction_gate",
        "boundary_safety",
        "status_ceiling",
        "reproducibility",
        "This dashboard does not prove source-of-record receipt",
        "validate_loop_governance_dashboard.py",
    ]:
        require(phrase in dashboard, f"dashboard missing phrase: {phrase}")

    require("LOOP-GOV-PHASE-20260617" in phase, "phase goal missing active phase")
    require("Loop Governance Dashboard | 02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md" in loop_readme, "loop README missing dashboard entry")
    require(
        "Loop Governance Dashboard Evidence | docs/harness/evidence/loop-governance-dashboard-20260617.md" in evidence_readme,
        "evidence README missing dashboard evidence entry",
    )
    require("LOOP-GOV-DASHBOARD-20260617" in evidence_index, "evidence index missing dashboard section")

    require(evidence.get("evidence_id") == "LOOP-GOV-DASHBOARD-20260617", "invalid dashboard evidence_id")
    require(evidence.get("status") == "active_governance_dashboard", "invalid dashboard status")
    require(evidence.get("phase_goal") == "LOOP-GOV-PHASE-20260617", "dashboard must link phase goal")
    require(evidence.get("signals", {}).get("efficiency_risk") == "review_required", "efficiency risk must remain visible")
    require(evidence.get("signals", {}).get("status_ceiling") == "partial_repair", "status ceiling must remain partial_repair")

    metrics = evidence.get("metrics", {})
    for key in ["runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]:
        require(metrics.get(key) == 0, f"dashboard metric must keep {key}=0")
    require(metrics.get("runtime_sop_e2e") == "repair_required", "runtime_sop_e2e must remain repair_required")
    require(metrics.get("accepted_integrated_allowed") is False, "accepted/integrated must remain forbidden")
    require(metrics.get("efficiency_backlog_status") == "review_required", "efficiency backlog must remain review_required")
    require(metrics.get("efficiency_backlog_items") == 4, "efficiency backlog item count must be 4")
    require(metrics.get("hard_window_truth_fields_missing") == 0, "hard window truth fields must remain 0")
    require(metrics.get("hard_window_five_segment_missing") == 0, "hard window five-segment missing must remain 0")
    require(metrics.get("audit_window_truth_fields_missing", 0) >= 1, "historical truth-field debt must remain visible")
    require(metrics.get("audit_window_five_segment_missing", 0) >= 1, "historical five-segment debt must remain visible")

    require(self_correction_efficiency_risk(self_correction) == "review_required", "self-correction efficiency risk must match dashboard")
    require(phase_evidence.get("current_status_ceiling", {}).get("accepted_integrated_allowed") is False, "phase evidence must forbid accepted/integrated")
    require(efficiency_backlog.get("status") == "review_required", "efficiency backlog evidence must stay review_required")

    for phrase in [
        "runtime_sop_e2e=repair_required",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
    ]:
        require(phrase in combined_status, f"current status missing marker: {phrase}")

    forbidden_claims = [
        "GFIS SOP E2E 已完成",
        "GFIS 运行层已 accepted",
        "GFIS 运行层已 integrated",
        "dashboard proves business completion",
    ]
    combined = "\n".join([dashboard, evidence_md, json.dumps(evidence, ensure_ascii=False)])
    for phrase in forbidden_claims:
        require(phrase not in combined, f"forbidden dashboard claim present: {phrase}")

    print(
        "loop_governance_dashboard=pass "
        "phase=LOOP-GOV-PHASE-20260617 dashboard=LOOP-GOV-DASHBOARD-20260617 "
        "quality_gate=repair_ceiling_enforced efficiency_risk=review_required "
        "self_correction_gate=blocked_expected boundary_safety=pass "
        "status_ceiling=partial_repair runtime_primary_key_ready=0 review_queue=0 "
        "runtime_intake=0 waes_review=0 verified=0 accepted_integrated_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
