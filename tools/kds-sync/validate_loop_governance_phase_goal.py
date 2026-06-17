#!/usr/bin/env python3
"""Validate the active Loop governance phase goal and evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md"
BOUNDARY_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_OPERATING_BOUNDARY.md"
LOOP_README = ROOT / "02-governance/loop/README.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-phase-goal-20260617.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-phase-goal-20260617.md"
EVIDENCE_README = ROOT / "docs/harness/evidence/README.md"
EVIDENCE_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
SELF_CORRECTION = ROOT / "docs/harness/evidence/loop_self_correction_assessment.json"
EFFICIENCY_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_round_efficiency_audit.py"
SELF_CORRECTION_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_self_correction_gate.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_controlled_markers(text: str, source_path: str) -> None:
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{source_path} missing controlled marker: {phrase}")


def main() -> int:
    phase_doc = read(PHASE_DOC)
    boundary_doc = read(BOUNDARY_DOC)
    loop_readme = read(LOOP_README)
    evidence_json = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)
    combined_status = "\n".join([read(CONTROL_BOARD), read(LOOP_STATE), read(STATUS_MATRIX)])
    self_correction = load_json(SELF_CORRECTION)
    efficiency_validator = read(EFFICIENCY_VALIDATOR)
    self_correction_validator = read(SELF_CORRECTION_VALIDATOR)

    require_controlled_markers(phase_doc, "02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md")
    require_controlled_markers(evidence_md, "docs/harness/evidence/loop-governance-phase-goal-20260617.md")

    for phrase in [
        "LOOP-GOV-PHASE-20260617",
        "阶段目标",
        "本阶段具体内容",
        "Definition Of Done",
        "不替代 GFIS 或其他项目的实施主进程",
        "禁止",
        "accepted",
        "integrated",
        "repair_required",
        "validate_loop_governance_phase_goal.py",
    ]:
        require(phrase in phase_doc, f"phase goal doc missing phrase: {phrase}")

    for phrase in [
        "implementation main process",
        "governance process",
        "Must not create or substitute real business facts",
    ]:
        require(phrase in boundary_doc, f"boundary doc missing phase dependency: {phrase}")

    require(
        "Loop Governance Phase Goal | 02-governance/loop/LOOP_GOVERNANCE_PHASE_GOAL.md" in loop_readme,
        "loop README missing phase goal entry",
    )
    require(
        "Loop Governance Phase Goal Evidence | docs/harness/evidence/loop-governance-phase-goal-20260617.md" in evidence_readme,
        "evidence README missing phase evidence entry",
    )
    require("LOOP-GOV-PHASE-20260617" in evidence_index, "evidence index missing phase section")

    require(evidence_json.get("evidence_id") == "LOOP-GOV-PHASE-20260617", "invalid evidence_id")
    require(evidence_json.get("status") == "active_governance", "invalid phase status")
    require(evidence_json.get("current_status_ceiling", {}).get("accepted_integrated_allowed") is False, "accepted/integrated must be forbidden")
    for key in ["runtime_primary_key_ready", "review_queue", "runtime_intake", "waes_review", "verified"]:
        require(evidence_json.get("current_status_ceiling", {}).get(key) == 0, f"status ceiling must keep {key}=0")

    for phrase in [
        "gfis_runtime_sop_e2e | `repair_required`",
        "accepted_integrated_allowed | false",
        "This evidence does not create a runtime primary key",
    ]:
        require(phrase in evidence_md, f"phase evidence missing phrase: {phrase}")

    for phrase in [
        "runtime_sop_e2e=repair_required",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
    ]:
        require(phrase in combined_status, f"current status missing ceiling marker: {phrase}")

    loop_efficiency = self_correction.get("loop_efficiency", {})
    require(loop_efficiency, "self-correction assessment missing loop_efficiency")
    require(loop_efficiency.get("metrics", {}).get("risk") in {"watch", "review_required"}, "loop efficiency risk must remain visible")
    require("loop_efficiency_risk" in self_correction_validator, "self-correction validator must report loop_efficiency_risk")
    require("loop_round_efficiency_audit=pass" in efficiency_validator, "efficiency validator output contract missing")

    forbidden_claims = [
        "GFIS SOP E2E 已完成",
        "GFIS 运行层已 accepted",
        "GFIS 运行层已 integrated",
        "治理阶段证明业务完成",
    ]
    combined_phase = "\n".join([phase_doc, evidence_md, json.dumps(evidence_json, ensure_ascii=False)])
    for phrase in forbidden_claims:
        require(phrase not in combined_phase, f"forbidden phase claim present: {phrase}")

    print(
        "loop_governance_phase_goal=pass "
        "phase=LOOP-GOV-PHASE-20260617 status=active_governance "
        "quality_target=present efficiency_target=present self_correction_target=present "
        "boundary_safety=present evidence=present accepted_integrated_allowed=false "
        "runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
