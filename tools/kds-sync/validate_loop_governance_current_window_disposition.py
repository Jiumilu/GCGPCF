#!/usr/bin/env python3
"""Validate the Loop governance current-window disposition evidence."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-current-window-disposition-20260619.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-current-window-disposition-20260619.md"
BACKLOG_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md"
LOCATOR = ROOT / "tools/kds-sync/validate_loop_governance_efficiency_debt_locator.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def locate_debt() -> dict:
    spec = importlib.util.spec_from_file_location("locator", LOCATOR)
    require(spec is not None and spec.loader is not None, "cannot load locator validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.locate_debt()


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    backlog = read(BACKLOG_DOC)
    located = locate_debt()

    require(
        evidence.get("evidence_id") == "LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619",
        "invalid evidence id",
    )
    require(evidence.get("status") == "review_required", "status must remain review_required")
    scope = evidence.get("scope", {})
    require(scope.get("truth_records_reviewed") == 2, "truth_records_reviewed must be 2")
    require(scope.get("five_segment_records_reviewed") == 7, "five_segment_records_reviewed must be 7")
    require(scope.get("hard_missing_truth_fields") == 0, "hard truth debt must be zero")
    require(scope.get("hard_missing_five_segment") == 0, "hard five-segment debt must be zero")
    require(scope.get("no_bulk_rewrite") is True, "no_bulk_rewrite must be true")
    require(scope.get("business_status_impact") == "none", "business_status_impact must be none")
    require(scope.get("accepted_integrated_allowed") is False, "accepted/integrated must remain disallowed")
    require(scope.get("history_rewrite_allowed") is False, "history rewrite must remain disallowed")

    require(not located["hard_truth"], "live hard-window truth debt must remain zero")
    require(not located["hard_segments"], "live hard-window five-segment debt must remain zero")
    require(len(located["truth_records"]) == 2, "live truth record count must remain 2")
    require(len(located["segment_records"]) == 7, "live five-segment record count must remain 7")

    truth = evidence.get("truth_field_dispositions", [])
    segments = evidence.get("five_segment_dispositions", [])
    require(len(truth) == 2, "truth disposition count mismatch")
    require(len(segments) == 7, "five-segment disposition count mismatch")
    require(
        {item.get("decision") for item in truth} == {"index_level_shell_exception"},
        "truth decisions must be shell exceptions",
    )
    require(
        sum(1 for item in segments if item.get("decision") == "index_level_shell_exception") == 2,
        "two five-segment records must remain shell exceptions",
    )
    require(
        sum(1 for item in segments if item.get("decision") == "targeted_annotation_ready") == 5,
        "five five-segment records must be targeted annotation candidates",
    )

    for phrase in [
        "LEDB-001-RD-005",
        "LEDB-002-RD-004",
        "current_window_disposition_recorded",
        "no_bulk_rewrite=true",
        "business_status_impact=none",
        "does not prove GFIS runtime SOP E2E passed",
        "does not authorize production write",
    ]:
        require(phrase in evidence_md or phrase in backlog, f"missing disposition phrase: {phrase}")

    print(
        "loop_governance_current_window_disposition=pass "
        "evidence=LOOP-GOV-CURRENT-WINDOW-DISPOSITION-20260619 "
        "truth_records_reviewed=2 five_segment_records_reviewed=7 "
        "shell_exceptions=2 targeted_annotation_ready=5 "
        "hard_missing_truth_fields=0 hard_missing_five_segment=0 "
        "no_bulk_rewrite=true business_status_impact=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
