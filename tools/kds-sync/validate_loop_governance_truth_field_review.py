#!/usr/bin/env python3
"""Validate the Loop governance truth-field review evidence."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-truth-field-review-20260617.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-truth-field-review-20260617.md"
BACKLOG_DOC = ROOT / "02-governance/loop/LOOP_GOVERNANCE_EFFICIENCY_DEBT_BACKLOG.md"
EVIDENCE_README = ROOT / "docs/harness/evidence/README.md"
EVIDENCE_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"
LOCATOR_GUARD = ROOT / "tools/kds-sync/validate_loop_governance_efficiency_debt_locator.py"


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


def locate_current_debt() -> dict:
    spec = importlib.util.spec_from_file_location("loop_efficiency_locator", LOCATOR_GUARD)
    require(spec and spec.loader, "cannot load efficiency debt locator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.locate_debt()


def has_truth_fields(text: str) -> bool:
    return all(
        field in text
        for field in [
            "declared_rounds",
            "substantive_rounds",
            "generated_items",
            "batch_generated",
            "substance_gate",
            "stop_type",
        ]
    )


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    backlog = read(BACKLOG_DOC)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)
    current = locate_current_debt()

    require_controlled(evidence_md, "docs/harness/evidence/loop-governance-truth-field-review-20260617.md")
    require(evidence.get("evidence_id") == "LOOP-GOV-TRUTH-FIELD-REVIEW-20260617", "invalid evidence id")
    require(evidence.get("disposition_id") == "LEDB-001-RD-003", "invalid disposition id")
    require(evidence.get("backlog_item") == "LEDB-001", "invalid backlog item")
    scope = evidence.get("scope", {})
    require(scope.get("reviewed_rounds") == 6, "reviewed round count mismatch")
    require(scope.get("no_bulk_rewrite") is True, "review must forbid bulk rewrite")
    require(scope.get("business_status_impact") == "none", "review must not change business status")
    require(scope.get("accepted_integrated_allowed") is False, "review must forbid accepted/integrated")
    require(not current["hard_truth"], "hard window truth-field debt must remain zero")

    dispositions = evidence.get("round_dispositions", [])
    require(len(dispositions) == 6, "must review six rounds")
    decisions = [item.get("decision") for item in dispositions]
    require(decisions.count("index_level_exception") == 5, "five truth shell records must remain index-level exceptions")
    require(decisions.count("historical_annotation_present") == 1, "one reviewed record must have historical annotation present")
    for item in dispositions:
        path = ROOT / item.get("path", "")
        text = read(path)
        require(text.startswith("---\n"), f"{item.get('path')} missing front matter")
        body = text.split("\n---\n", 2)[-1].strip()
        if item.get("decision") == "index_level_exception":
            require(not body, f"{item.get('path')} is no longer a shell record")
        else:
            require(body, f"{item.get('path')} missing historical annotation body")
            require(has_truth_fields(text), f"{item.get('path')} missing truth fields after annotation")

    for phrase in [
        "LOOP-GOV-TRUTH-FIELD-REVIEW-20260617",
        "LEDB-001-RD-003",
        "reviewed_rounds | 6",
        "index_level_exception",
        "historical_annotation_present",
        "no_bulk_rewrite",
        "business_status_impact",
        "does not rewrite historical round records",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("LEDB-001-RD-003" in backlog, "backlog missing LEDB-001-RD-003")
    require(
        "Loop Governance Truth Field Review Evidence | docs/harness/evidence/loop-governance-truth-field-review-20260617.md"
        in evidence_readme,
        "evidence README missing truth-field review entry",
    )
    require("LOOP-GOV-TRUTH-FIELD-REVIEW-20260617" in evidence_index, "evidence index missing truth-field review section")

    print(
        "loop_governance_truth_field_review=pass "
        "evidence=LOOP-GOV-TRUTH-FIELD-REVIEW-20260617 disposition=LEDB-001-RD-003 "
        "reviewed_rounds=6 index_level_exception=5 historical_annotation_present=1 "
        "hard_missing_truth_fields=0 no_bulk_rewrite=true business_status_impact=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
