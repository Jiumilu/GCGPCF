#!/usr/bin/env python3
"""Validate the Loop governance long-sequence checkpoint evidence."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.md"
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


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    backlog = read(BACKLOG_DOC)
    evidence_readme = read(EVIDENCE_README)
    evidence_index = read(EVIDENCE_INDEX)
    current = locate_current_debt()

    require_controlled(evidence_md, "docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.md")
    require(evidence.get("evidence_id") == "LOOP-GOV-SEQUENCE-CHECKPOINT-20260619", "invalid evidence id")
    require(evidence.get("disposition_id") == "LEDB-003-RD-002", "invalid disposition id")
    require(evidence.get("backlog_item") == "LEDB-003", "invalid backlog item")
    require(evidence.get("status") == "watch", "sequence checkpoint must remain watch")
    scope = evidence.get("scope", {})
    require(scope.get("no_bulk_rewrite") is True, "checkpoint must forbid bulk rewrite")
    require(scope.get("business_status_impact") == "none", "checkpoint must not change business status")
    require(scope.get("accepted_integrated_allowed") is False, "checkpoint must forbid accepted/integrated")
    require(not current["hard_truth"], "hard window truth-field debt must remain zero")
    require(not current["hard_segments"], "hard window five-segment debt must remain zero")

    policy = evidence.get("checkpoint_policy", {})
    require(policy.get("sequence_prefix") == "GPCF-L4-GFIS-REPAIR", "invalid sequence prefix")
    require(policy.get("checkpoint_interval_rounds") == 25, "checkpoint interval mismatch")
    require(policy.get("latest_sequence_length") <= current["max_consecutive_sequence"], "current sequence below checkpoint baseline")
    require(policy.get("last_required_checkpoint_floor") == 175, "last checkpoint floor mismatch")
    require(policy.get("next_required_checkpoint_at") == 200, "next checkpoint mismatch")

    decision = evidence.get("decision", {})
    require(decision.get("type") == "checkpoint_cadence_defined", "invalid decision type")
    require(decision.get("current_action") == "keep_watch_until_next_checkpoint", "invalid current action")

    for phrase in [
        "LOOP-GOV-SEQUENCE-CHECKPOINT-20260619",
        "LEDB-003-RD-002",
        "checkpoint_interval_rounds | 25",
        "next_required_checkpoint_at | 200",
        "business_status_impact | none",
        "does not close `LEDB-003`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("LEDB-003-RD-002" in backlog, "backlog missing LEDB-003-RD-002")
    require(
        "Loop Governance Sequence Checkpoint Evidence | docs/harness/evidence/loop-governance-sequence-checkpoint-20260619.md"
        in evidence_readme,
        "evidence README missing sequence checkpoint entry",
    )
    require("LOOP-GOV-SEQUENCE-CHECKPOINT-20260619" in evidence_index, "evidence index missing sequence checkpoint section")

    print(
        "loop_governance_sequence_checkpoint=pass "
        "evidence=LOOP-GOV-SEQUENCE-CHECKPOINT-20260619 disposition=LEDB-003-RD-002 "
        f"max_consecutive_sequence={current['max_consecutive_sequence']} "
        "checkpoint_interval_rounds=25 next_required_checkpoint_at=200 "
        "hard_missing_truth_fields=0 hard_missing_five_segment=0 "
        "no_bulk_rewrite=true business_status_impact=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
