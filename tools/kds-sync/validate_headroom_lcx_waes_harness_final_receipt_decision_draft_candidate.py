#!/usr/bin/env python3
"""Validate WAES/Harness final receipt decision draft candidate for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_draft_candidate.py"
DRAFT = ROOT / "fixtures/headroom/headroom-lcx-waes-harness-final-receipt-decision.response.draft.candidate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-23",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(E_JSON)
    draft = load_json(DRAFT)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_candidate" in builder, "builder must build candidate")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-20260623", "invalid evidence id")
    require(evidence.get("status") == "draft_candidate_ready_not_formal_decision", "invalid status")
    require(evidence.get("candidate_response") == draft, "draft fixture must match evidence candidate")
    require(draft.get("decision_value") == "admitted_for_next_precheck_only", "draft should recommend next precheck only")
    require(draft.get("can_open_real_measurement") is False, "draft must not open measurement")
    require(draft.get("accepted") is False, "draft must keep accepted false")
    require("candidate only" in draft.get("decision_maker", ""), "draft decision maker must remain candidate-marked")

    boundary = evidence.get("candidate_use_boundary", {})
    for key, value in boundary.items():
        require(value is True if key in {"candidate_only", "not_formal_response", "not_waes_harness_signed"} else value is False, f"boundary mismatch: {key}")

    for phrase in [
        "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-20260623",
        "draft_candidate_ready_not_formal_decision",
        "candidate_only | `true`",
        "real_measurement_open | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_waes_harness_final_receipt_decision_draft_candidate.py" in loop, "loop missing builder")
    require("validate_headroom_lcx_waes_harness_final_receipt_decision_draft_candidate.py" in loop, "loop missing validator")

    print(
        "headroom_lcx_waes_harness_final_receipt_decision_draft_candidate=pass "
        "status=draft_candidate_ready_not_formal_decision "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
