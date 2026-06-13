#!/usr/bin/env python3
"""Validate GPCF L3 governance rounds CF-LR-002 through CF-LR-016."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs/harness/evidence/gpcf_l3_governance_rounds_lr002_lr016.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    require(DATA.exists(), f"missing data: {DATA}")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rounds = data.get("rounds", [])
    require(len(rounds) == 15, "expected 15 GPCF L3 governance rounds")
    expected_ids = [f"GPCF-CF-LR-{number:03d}" for number in range(2, 17)]
    require([item.get("round_id") for item in rounds] == expected_ids, "round ids must be CF-LR-002 through CF-LR-016")

    for item in rounds:
        round_id = item["round_id"]
        doc = ROOT / item["doc"]
        require(doc.exists(), f"missing doc: {doc}")
        text = doc.read_text(encoding="utf-8")
        require(round_id in text, f"doc missing round id: {round_id}")
        require("Current state remains `partial`" in text, f"doc must cap state: {round_id}")
        require("真实 KDS TOKEN 写入" in text, f"doc missing KDS token boundary: {round_id}")
        require("accepted/integrated" in text, f"doc missing status upgrade boundary: {round_id}")
        loop_doc = ROOT / "docs/harness/loops" / f"loop-round-{round_id}.md"
        require(loop_doc.exists(), f"missing loop record: {loop_doc}")

    for flag in [
        "kds_token_configured",
        "kds_api_sync_completed",
        "git_push_authorized",
        "production_write_allowed",
        "runtime_write_api_authorized",
        "bench_migrate_authorized",
        "accepted_or_integrated_allowed",
        "strategic_position_change_allowed",
        "ready_to_execute_external_write",
    ]:
        require(data.get(flag) is False, f"{flag} must be false")

    session = data.get("l3_session", {})
    require(session.get("mode") == "L3", "session mode must be L3")
    require(session.get("completed_rounds") == 15, "L3 completed rounds must be 15")
    require(session.get("round_limit") == 15, "L3 round limit must be 15")
    require(session.get("remaining_rounds") == 0, "L3 remaining rounds must be 0")
    require(session.get("stop_type") == "budget_exhausted", "L3 stop type must be budget_exhausted")

    forbidden_actions = "\n".join(data.get("forbidden_actions", []))
    for forbidden in ["Git push", "真实 KDS TOKEN 写入", "bench migrate", "accepted/integrated"]:
        require(forbidden in forbidden_actions, f"forbidden action missing: {forbidden}")

    print("gpcf L3 governance rounds validation passed")
    print("rounds=15 completed=15 remaining=0 stop_type=budget_exhausted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
