#!/usr/bin/env python3
"""Validate GC-Knowledge Fabric WAES minimum dry-run gates.

This script uses local fixtures only. It does not call WAES, KDS, GFIS,
GPC, ERP, MES, or any production system.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "waes" / "minimum-gates.json"


def has_refs(obj: dict[str, Any], key: str) -> bool:
    value = obj.get(key)
    return isinstance(value, list) and len(value) > 0


def source_gate(obj: dict[str, Any]) -> str:
    if has_refs(obj, "sourceRefs"):
        return "passed"
    return "repair_required"


def evidence_gate(obj: dict[str, Any]) -> str:
    if has_refs(obj, "evidenceRefs"):
        return "passed"
    return "repair_required"


def sensitive_data_gate(obj: dict[str, Any]) -> str:
    if obj.get("sensitive") is True:
        return "metadata_only"
    return "passed"


def rag_gate(obj: dict[str, Any]) -> str:
    if obj.get("sensitive") is True:
        return "metadata_only"
    if obj.get("trustLevel") == "T5":
        return "blocked"
    if obj.get("ragAdmission") == "safe" and evidence_gate(obj) == "passed":
        return "passed"
    if obj.get("ragAdmission") == "limited" and source_gate(obj) == "passed":
        return "passed"
    if obj.get("ragAdmission") == "repair_required":
        return "repair_required"
    return "blocked"


def writeback_gate(obj: dict[str, Any]) -> str:
    if obj.get("generatedBy") == "ai" or obj.get("trustLevel") == "T5":
        return "blocked"
    if evidence_gate(obj) != "passed":
        return "repair_required"
    if obj.get("confirmationStatus") not in {"human_confirmed", "committee_confirmed"}:
        return "human_required"
    return "passed"


def revenue_gate(obj: dict[str, Any]) -> str:
    if obj.get("revenueType") == "formal_revenue":
        if obj.get("basis") == "cash_received" and evidence_gate(obj) == "passed":
            return "passed"
        return "blocked"
    if obj.get("revenueType") in {"potential_revenue", "channel_opportunity", "knowledge_potential_value"}:
        return "human_required"
    return "repair_required"


def contribution_gate(obj: dict[str, Any]) -> str:
    if obj.get("confirmationStatus") in {"human_confirmed", "committee_confirmed"}:
        return "passed"
    if obj.get("contributionStatus") == "candidate":
        return "human_required"
    return "repair_required"


GATES = {
    "source_gate": source_gate,
    "evidence_gate": evidence_gate,
    "sensitive_data_gate": sensitive_data_gate,
    "rag_gate": rag_gate,
    "writeback_gate": writeback_gate,
    "revenue_gate": revenue_gate,
    "contribution_gate": contribution_gate,
}


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    failures: list[str] = []
    passed_cases = 0
    evaluated_gates = 0

    for case in data["cases"]:
        obj = case["object"]
        expected = case["expected"]
        for gate_name, expected_status in expected.items():
            actual_status = GATES[gate_name](obj)
            evaluated_gates += 1
            if actual_status != expected_status:
                failures.append(
                    f"{case['id']} {gate_name}: expected={expected_status} actual={actual_status}"
                )
        if not failures:
            passed_cases += 1

    if failures:
        print("waes_minimum_gates=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "waes_minimum_gates=pass "
        f"cases={len(data['cases'])} "
        f"passed_cases={passed_cases} "
        f"evaluated_gates={evaluated_gates} "
        "source_gate=covered evidence_gate=covered rag_gate=covered "
        "writeback_gate=covered revenue_gate=covered contribution_gate=covered "
        "sensitive_data_gate=covered real_writes=0 external_api_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
