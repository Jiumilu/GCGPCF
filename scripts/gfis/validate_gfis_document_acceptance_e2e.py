#!/usr/bin/env python3
"""Validate GFIS document acceptance candidate-fact E2E dry-run.

This script uses local fixtures only. It does not write GFIS, KDS, WAES,
GPC, ERP, MES, or any external API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "gfis" / "document-acceptance-e2e.json"


MISSING_FIELD_TO_GAP = {
    "pod_record": "missing_pod",
    "finance_proof": "missing_finance_proof",
    "source_record": "missing_source",
    "evidence": "missing_evidence",
    "quality_record": "missing_quality_record",
}


def infer_fact_type(source: dict[str, Any]) -> str:
    if source.get("sensitiveClass") == "finance_voucher" or source.get("sourceKind") == "cash_receipt":
        return "finance_fact"
    return "order_fact"


def infer_gate_status(source: dict[str, Any]) -> str:
    if source.get("trustLevel") == "T5":
        return "blocked"
    if source.get("sensitiveClass") == "finance_voucher":
        return "metadata_only"
    if source.get("missingFields"):
        return "human_required"
    return "passed"


def evaluate(source: dict[str, Any]) -> dict[str, Any]:
    gaps = [MISSING_FIELD_TO_GAP[item] for item in source.get("missingFields", []) if item in MISSING_FIELD_TO_GAP]
    gate_status = infer_gate_status(source)
    return {
        "factCandidates": 1,
        "factTypes": [infer_fact_type(source)],
        "gaps": gaps,
        "waesGateStatuses": [gate_status],
        "requiresHumanConfirmation": gate_status != "passed",
        "requiresCommittee": False,
        "writebackStatuses": ["candidate"],
        "noWrite": True,
        "businessWrites": 0,
        "kdsFactWrites": 0,
    }


def compare(actual: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")
    return failures


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    failures: list[str] = []
    total_candidates = 0
    total_gaps = 0
    blocked_or_human = 0

    for case in data["cases"]:
        actual = evaluate(case["source"])
        total_candidates += actual["factCandidates"]
        total_gaps += len(actual["gaps"])
        if actual["requiresHumanConfirmation"]:
            blocked_or_human += 1
        for failure in compare(actual, case["expected"]):
            failures.append(f"{case['id']} {failure}")

    if failures:
        print("gfis_document_acceptance_e2e=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_document_acceptance_e2e=pass "
        f"cases={len(data['cases'])} "
        f"fact_candidates={total_candidates} "
        f"gaps={total_gaps} "
        f"human_or_blocked_cases={blocked_or_human} "
        "writeback_candidates_only=1 business_writes=0 kds_fact_writes=0 external_api_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
