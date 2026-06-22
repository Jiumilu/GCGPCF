#!/usr/bin/env python3
"""Validate GC-Knowledge Fabric KWE minimum workflow dry-run.

This script uses local fixtures only. It does not create real KDS facts,
KWE work items, WAES gate results, or GFIS writebacks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "kwe" / "minimum-workflow.json"


def has_refs(candidate: dict[str, Any], key: str) -> bool:
    value = candidate.get(key)
    return isinstance(value, list) and len(value) > 0


def evaluate(candidate: dict[str, Any]) -> dict[str, Any]:
    if candidate.get("waesGateStatus") == "committee_required":
        return {
            "workItemStatus": "open",
            "workType": "committee_review",
            "canCreateFact": False,
            "requiredActions": ["committee_decision"],
            "realWrites": 0,
        }

    if not has_refs(candidate, "sourceRefs") or not has_refs(candidate, "evidenceRefs"):
        return {
            "workItemStatus": "open",
            "workType": "evidence_gap",
            "canCreateFact": False,
            "requiredActions": ["register_source", "bind_evidence", "human_confirm"],
            "realWrites": 0,
        }

    if candidate.get("confirmationStatus") != "human_confirmed":
        return {
            "workItemStatus": "in_progress",
            "workType": "fact_confirmation",
            "canCreateFact": False,
            "requiredActions": ["human_confirm"],
            "realWrites": 0,
        }

    if candidate.get("waesGateStatus") == "passed":
        return {
            "workItemStatus": "approved",
            "workType": "fact_confirmation",
            "canCreateFact": True,
            "nextLifecycle": "verified",
            "realWrites": 0,
        }

    return {
        "workItemStatus": "open",
        "workType": "evidence_gap",
        "canCreateFact": False,
        "requiredActions": ["repair_waes_gate"],
        "realWrites": 0,
    }


def compare_subset(actual: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for key, expected_value in expected.items():
        actual_value = actual.get(key)
        if actual_value != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual_value!r}")
    return failures


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    failures: list[str] = []
    promotable = 0
    blocked = 0

    for workflow in data["workflows"]:
        actual = evaluate(workflow["candidate"])
        case_failures = compare_subset(actual, workflow["expected"])
        if case_failures:
            failures.extend(f"{workflow['id']} {failure}" for failure in case_failures)
        if actual["canCreateFact"]:
            promotable += 1
        else:
            blocked += 1

    if failures:
        print("kwe_minimum_workflow=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kwe_minimum_workflow=pass "
        f"workflows={len(data['workflows'])} "
        f"promotable_candidates={promotable} "
        f"blocked_or_pending_candidates={blocked} "
        "ai_direct_fact_writes=0 kds_fact_writes=0 gfis_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
