#!/usr/bin/env python3
"""Validate the Loop governance round review plan and evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_ROUND_REVIEW_PLAN.md"
BACKLOG_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md"
LOCATOR_JSON = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.json"
PLAN_JSON = ROOT / "docs/harness/evidence/loop-governance-round-review-plan-20260617.json"
PLAN_MD = ROOT / "docs/harness/evidence/loop-governance-round-review-plan-20260617.md"
EVIDENCE_README = ROOT / "docs/harness/evidence/README.md"
EVIDENCE_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"
LOOP_README = ROOT / "02-governance/loop/README.md"


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


def package_by_id(plan: dict, package_id: str) -> dict:
    for package in plan.get("work_packages", []):
        if package.get("package_id") == package_id:
            return package
    raise SystemExit(f"FAIL: missing work package: {package_id}")


def main() -> int:
    plan_doc = read(PLAN_DOC)
    backlog_doc = read(BACKLOG_DOC)
    plan_md = read(PLAN_MD)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)
    loop_readme = read(LOOP_README)
    plan = load_json(PLAN_JSON)
    locator = load_json(LOCATOR_JSON)

    require_controlled(plan_doc, "02-governance/loop/LOOP_GOVERNANCE_ROUND_REVIEW_PLAN.md")
    require_controlled(plan_md, "docs/harness/evidence/loop-governance-round-review-plan-20260617.md")

    require(plan.get("evidence_id") == "LOOP-GOV-ROUND-REVIEW-PLAN-20260617", "invalid plan evidence id")
    require(plan.get("source_locator") == "LOOP-GOV-EFF-DEBT-LOCATOR-20260617", "plan must bind to locator")
    require(plan.get("status") == "review_required", "plan must remain review_required")

    controls = plan.get("controls", {})
    require(controls.get("no_bulk_rewrite") is True, "plan must forbid bulk rewrite")
    require(controls.get("business_status_impact") == "none", "plan must have no business status impact")
    require(controls.get("accepted_integrated_allowed") is False, "plan must forbid accepted/integrated")

    signal = plan.get("source_signal", {})
    locator_signal = locator.get("source_signal", {})
    for key in [
        "total_rounds",
        "audit_checked",
        "hard_checked",
        "audit_missing_truth_fields",
        "audit_missing_five_segment",
        "hard_missing_truth_fields",
        "hard_missing_five_segment",
        "duplicate_fingerprint_groups",
        "high_similarity_adjacent_pairs",
        "max_consecutive_sequence",
    ]:
        require(signal.get(key) == locator_signal.get(key), f"source signal mismatch: {key}")
    require(signal.get("risk") == "review_required", "risk must remain review_required")

    truth_package = package_by_id(plan, "LEDB-001-RP-001")
    segment_package = package_by_id(plan, "LEDB-002-RP-001")
    sequence_package = package_by_id(plan, "LEDB-003-RP-001")

    truth_rounds = [record["round"] for record in locator.get("affected_truth_field_records", [])]
    segment_rounds = [record["round"] for record in locator.get("affected_five_segment_records", [])]
    require(truth_package.get("rounds") == truth_rounds, "truth-field review package must match locator")
    require(segment_package.get("rounds") == segment_rounds, "five-segment review package must match locator")
    require(truth_package.get("count") == len(truth_rounds), "truth-field package count mismatch")
    require(segment_package.get("count") == len(segment_rounds), "five-segment package count mismatch")
    require(sequence_package.get("count") == signal.get("max_consecutive_sequence"), "sequence package count mismatch")
    require("checkpoint every 25 substantive GFIS repair rounds" in sequence_package.get("cadence", ""), "sequence cadence missing")

    for text, name in [(plan_doc, "plan doc"), (plan_md, "plan evidence")]:
        for phrase in [
            "LOOP-GOV-ROUND-REVIEW-PLAN-20260617",
            "LOOP-GOV-EFF-DEBT-LOCATOR-20260617",
            "no_bulk_rewrite",
            "business_status_impact",
            "targeted annotation",
            "index-level exception",
            "does not rewrite historical",
            "does not prove GFIS runtime SOP E2E passed",
        ]:
            require(phrase in text, f"{name} missing phrase: {phrase}")

    require("LOOP-GOV-ROUND-REVIEW-PLAN-20260617" in backlog_doc, "backlog must reference round review plan")
    require(
        "Loop Governance Round Review Plan | 02-governance/loop/LOOP_GOVERNANCE_ROUND_REVIEW_PLAN.md" in loop_readme,
        "loop README missing round review plan entry",
    )
    require(
        "Loop Governance Round Review Plan Evidence | docs/harness/evidence/loop-governance-round-review-plan-20260617.md" in evidence_readme,
        "evidence README missing round review plan entry",
    )
    require("LOOP-GOV-ROUND-REVIEW-PLAN-20260617" in evidence_index, "evidence index missing round review plan section")

    print(
        "loop_governance_round_review_plan=pass "
        "evidence=LOOP-GOV-ROUND-REVIEW-PLAN-20260617 "
        f"truth_review_rounds={len(truth_rounds)} five_segment_review_rounds={len(segment_rounds)} "
        f"sequence_checkpoint={sequence_package.get('count')} no_bulk_rewrite=true business_status_impact=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
