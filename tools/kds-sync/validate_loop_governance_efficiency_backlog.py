#!/usr/bin/env python3
"""Validate the Loop governance efficiency debt backlog."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKLOG_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md"
DASHBOARD_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md"
LOOP_README = ROOT / "02-governance/loop/README.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.md"
LOCATOR_JSON = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.json"
LOCATOR_MD = ROOT / "docs/harness/evidence/loop-governance-efficiency-debt-locator-20260617.md"
EVIDENCE_README = ROOT / "docs/harness/evidence/README.md"
EVIDENCE_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"
EFFICIENCY_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_round_efficiency_audit.py"
LOCATOR_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_governance_efficiency_debt_locator.py"


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


def main() -> int:
    backlog = read(BACKLOG_DOC)
    dashboard = read(DASHBOARD_DOC)
    loop_readme = read(LOOP_README)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    locator = load_json(LOCATOR_JSON)
    locator_md = read(LOCATOR_MD)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)
    efficiency_validator = read(EFFICIENCY_VALIDATOR)
    locator_validator = read(LOCATOR_VALIDATOR)

    require_controlled(backlog, "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md")
    require_controlled(evidence_md, "docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.md")

    for phrase in [
        "LEDB-001",
        "LEDB-002",
        "LEDB-003",
        "LEDB-004",
        "audit_missing_truth_fields=2",
        "audit_missing_five_segment=18",
        "max_consecutive_sequence=184",
        "LOOP-GOV-EFF-DEBT-LOCATOR-20260617",
        "does not rewrite historical round records in bulk",
        "Review Disposition Template",
        "LEDB-001-RD-001",
        "business_status_impact",
        "Closing Conditions",
    ]:
        require(phrase in backlog, f"backlog doc missing phrase: {phrase}")

    require(
        "Loop Governance Efficiency Debt Backlog | 02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md" in loop_readme,
        "loop README missing efficiency backlog entry",
    )
    require(
        "Loop Governance Efficiency Debt Backlog Evidence | docs/harness/evidence/loop-governance-efficiency-debt-backlog-20260617.md" in evidence_readme,
        "evidence README missing efficiency backlog evidence entry",
    )
    require("LOOP-GOV-EFF-DEBT-20260617" in evidence_index, "evidence index missing efficiency backlog section")
    require("LEDB-001" in dashboard, "dashboard must point to efficiency backlog")

    require(evidence.get("evidence_id") == "LOOP-GOV-EFF-DEBT-20260617", "invalid evidence id")
    require(evidence.get("status") == "review_required", "backlog evidence must remain review_required")
    signal = evidence.get("source_signal", {})
    require(signal.get("audit_missing_truth_fields") == 2, "truth-field debt count mismatch")
    require(signal.get("audit_missing_five_segment") == 18, "five-segment debt count mismatch")
    require(signal.get("hard_missing_truth_fields") == 0, "hard truth field window must stay clean")
    require(signal.get("hard_missing_five_segment") == 0, "hard five-segment window must stay clean")
    require(signal.get("max_consecutive_sequence") == 184, "long sequence count mismatch")
    require(signal.get("risk") == "review_required", "risk must remain review_required")

    item_ids = {item.get("id") for item in evidence.get("items", [])}
    require({"LEDB-001", "LEDB-002", "LEDB-003", "LEDB-004"}.issubset(item_ids), "missing backlog item ids")
    dispositions = evidence.get("review_dispositions", [])
    require(len(dispositions) >= 5, "review disposition queue must contain initial records and RD-002")
    disposition_items = {item.get("backlog_item") for item in dispositions}
    require({"LEDB-001", "LEDB-002", "LEDB-003", "LEDB-004"} == disposition_items, "review dispositions must cover all backlog items")
    for disposition in dispositions:
        require(disposition.get("no_bulk_rewrite") is True, "review disposition must keep no_bulk_rewrite=true")
        require(disposition.get("business_status_impact") == "none", "review disposition must not change business status")
        require(
            disposition.get("disposition_id", "").endswith("-RD-001")
            or disposition.get("disposition_id") == "LEDB-001-RD-002",
            "disposition id must use an approved review disposition id",
        )
    template = evidence.get("disposition_template", {})
    require(template.get("business_status_impact_required") == "none", "disposition template must require no business impact")
    require("loop_round_efficiency_audit=pass" in efficiency_validator, "efficiency validator output contract missing")
    require(locator.get("evidence_id") == "LOOP-GOV-EFF-DEBT-LOCATOR-20260617", "invalid locator evidence id")
    require(len(locator.get("affected_truth_field_records", [])) == 2, "locator truth record count mismatch")
    require(len(locator.get("affected_five_segment_records", [])) == 18, "locator five-segment record count mismatch")
    require(locator.get("scope", {}).get("no_bulk_rewrite") is True, "locator must forbid bulk rewrite")
    require(locator.get("scope", {}).get("business_status_impact") == "none", "locator must have no business impact")
    require("loop_governance_efficiency_debt_locator=pass" in locator_validator, "locator validator output contract missing")
    require("LEDB-001 | 2" in locator_md, "locator markdown missing LEDB-001 count")
    require("LEDB-002 | 18" in locator_md, "locator markdown missing LEDB-002 count")

    for phrase in [
        "Review Disposition Template",
        "LEDB-001-RD-001",
        "business_status_impact",
        "does not rewrite historical round records in bulk",
        "does not prove GFIS runtime SOP E2E passed",
        "does not create source-of-record",
    ]:
        require(phrase in evidence_md, f"backlog evidence missing non-claim: {phrase}")

    print(
        "loop_governance_efficiency_backlog=pass "
        "evidence=LOOP-GOV-EFF-DEBT-20260617 status=review_required "
        f"items=4 dispositions={len(dispositions)} truth_field_debt=2 five_segment_debt=18 max_consecutive_sequence=184 "
        "hard_missing_truth_fields=0 hard_missing_five_segment=0 bulk_rewrite_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
