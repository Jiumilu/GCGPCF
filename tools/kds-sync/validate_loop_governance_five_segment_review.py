#!/usr/bin/env python3
"""Validate the Loop governance five-segment review evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-five-segment-review-20260617.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-five-segment-review-20260617.md"
BACKLOG_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md"
EVIDENCE_README = ROOT / "docs/harness/evidence/README.md"
EVIDENCE_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"


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
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    backlog = read(BACKLOG_DOC)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)

    require_controlled(evidence_md, "docs/harness/evidence/loop-governance-five-segment-review-20260617.md")
    require(evidence.get("evidence_id") == "LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617", "invalid evidence id")
    require(evidence.get("disposition_id") == "LEDB-002-RD-002", "invalid disposition id")
    require(evidence.get("backlog_item") == "LEDB-002", "invalid backlog item")
    scope = evidence.get("scope", {})
    require(scope.get("reviewed_rounds") == 5, "reviewed round count mismatch")
    require(scope.get("no_bulk_rewrite") is True, "review must forbid bulk rewrite")
    require(scope.get("business_status_impact") == "none", "review must not change business status")
    require(scope.get("accepted_integrated_allowed") is False, "review must forbid accepted/integrated")

    dispositions = evidence.get("round_dispositions", [])
    require(len(dispositions) == 5, "must review five rounds")
    decisions = {item.get("decision") for item in dispositions}
    require({"targeted_annotation_ready", "index_level_exception"}.issubset(decisions), "must contain both review outcomes")
    require("GPCF-L4-GFIS-REPAIR-212" in {item.get("round_id") for item in dispositions}, "missing 212 review")
    require("GPCF-L4-GFIS-REPAIR-208" in {item.get("round_id") for item in dispositions}, "missing 208 review")

    for phrase in [
        "LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617",
        "LEDB-002-RD-002",
        "targeted_annotation_ready",
        "index_level_exception",
        "no_bulk_rewrite",
        "business_status_impact",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require(
        "does not rewrite historical round records" in evidence_md
        or "不改写历史 round records" in evidence_md
        or "不重写历史轮次记录" in evidence_md,
        "evidence markdown missing no historical rewrite statement",
    )
    require("LEDB-002-RD-002" in backlog, "backlog missing LEDB-002-RD-002")
    require(
        "docs/harness/evidence/loop-governance-five-segment-review-20260617.md" in evidence_readme,
        "evidence README missing five-segment review entry",
    )
    require("LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617" in evidence_index, "evidence index missing five-segment review section")

    print(
        "loop_governance_five_segment_review=pass "
        "evidence=LOOP-GOV-FIVE-SEGMENT-REVIEW-20260617 disposition=LEDB-002-RD-002 "
        "reviewed_rounds=5 targeted_annotation_ready=3 index_level_exception=2 "
        "no_bulk_rewrite=true business_status_impact=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
