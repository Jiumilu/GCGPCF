#!/usr/bin/env python3
"""Validate Brain LOOP dashboard knowledge-closure metrics dry-run.

This script computes metrics from a local fixture only. It does not write
Brain, PKC, KDS, WAES, KWE, GFIS, GPC, revenue ledgers, or any external API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "loop-dashboard" / "knowledge-closure-metrics.json"

WEIGHTS = {
    "stateCoverageRate": 20,
    "factMaturityDqRate": 25,
    "sourceEvidenceQualifiedRate": 20,
    "registryLedgerReportConsistencyRate": 15,
    "automationEffectiveRate": 10,
    "writebackGapClosureRate": 10,
}


def rate(objects: list[dict[str, Any]], key: str) -> float:
    if not objects:
        return 0.0
    return sum(1 for item in objects if item.get(key)) / len(objects)


def status_rate(objects: list[dict[str, Any]], key: str, value: str) -> float:
    if not objects:
        return 0.0
    return sum(1 for item in objects if item.get(key) == value) / len(objects)


def conditional_status_rate(objects: list[dict[str, Any]], key: str, complete_value: str) -> float:
    relevant = [item for item in objects if item.get(key) not in {"not_required", "not_applicable"}]
    if not relevant:
        return 0.0
    return sum(1 for item in relevant if item.get(key) == complete_value) / len(relevant)


def rounded(value: float) -> float:
    return round(value, 6)


def evaluate(objects: list[dict[str, Any]]) -> dict[str, Any]:
    metric_inputs = {
        "stateCoverageRate": rate(objects, "hasState"),
        "factMaturityDqRate": rate(objects, "matureFact"),
        "sourceEvidenceQualifiedRate": rate(objects, "sourceEvidenceQualified"),
        "registryLedgerReportConsistencyRate": rate(objects, "registryLedgerReportConsistent"),
        "automationEffectiveRate": rate(objects, "automationEffective"),
        "writebackGapClosureRate": rate(objects, "writebackGapClosed"),
    }
    score = sum(metric_inputs[key] * weight for key, weight in WEIGHTS.items())
    return {
        **{key: rounded(value) for key, value in metric_inputs.items()},
        "knowledgeClosureScore": round(score),
        "ragSafeRate": rounded(status_rate(objects, "ragAdmission", "safe")),
        "blockedKnowledgeRate": rounded(status_rate(objects, "ragAdmission", "blocked")),
        "repairRequiredGapCount": sum(1 for item in objects if item.get("ragAdmission") == "repair_required"),
        "waesInterceptionCount": sum(1 for item in objects if item.get("waesBlocked")),
        "humanConfirmationCompletionRate": rounded(
            conditional_status_rate(objects, "humanConfirmationStatus", "completed")
        ),
        "committeeClosureRate": rounded(conditional_status_rate(objects, "committeeStatus", "completed")),
        "revenueCandidateToFormalRate": rounded(
            sum(1 for item in objects if item.get("revenueStatus") == "formal")
            / max(1, sum(1 for item in objects if item.get("revenueStatus") in {"formal", "candidate"}))
        ),
        "bountyClosureRate": rounded(conditional_status_rate(objects, "bountyStatus", "closed")),
        "aiCandidateAdoptionRate": rounded(status_rate(objects, "aiCandidateStatus", "adopted")),
        "externalShareViolationCount": sum(1 for item in objects if item.get("externalShareViolation")),
        "sensitiveMetadataOnlyRate": rounded(rate(objects, "sensitiveMetadataOnly")),
        "noWrite": True,
        "kdsWrites": 0,
        "waesWrites": 0,
        "kweWrites": 0,
        "businessWrites": 0,
        "externalApiWrites": 0,
    }


def compare(actual: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")
    return failures


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    actual = evaluate(data["objects"])
    failures = compare(actual, data["expected"])

    if failures:
        print("knowledge_closure_metrics=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "knowledge_closure_metrics=pass "
        f"objects={len(data['objects'])} "
        f"closure_score={actual['knowledgeClosureScore']} "
        f"rag_safe_rate={actual['ragSafeRate']} "
        f"blocked_knowledge_rate={actual['blockedKnowledgeRate']} "
        f"repair_required_gap_count={actual['repairRequiredGapCount']} "
        f"waes_interception_count={actual['waesInterceptionCount']} "
        f"human_confirmation_completion_rate={actual['humanConfirmationCompletionRate']} "
        f"committee_closure_rate={actual['committeeClosureRate']} "
        f"revenue_candidate_to_formal_rate={actual['revenueCandidateToFormalRate']} "
        f"bounty_closure_rate={actual['bountyClosureRate']} "
        f"ai_candidate_adoption_rate={actual['aiCandidateAdoptionRate']} "
        f"external_share_violation_count={actual['externalShareViolationCount']} "
        f"sensitive_metadata_only_rate={actual['sensitiveMetadataOnlyRate']} "
        "no_write=covered kds_writes=0 waes_writes=0 kwe_writes=0 "
        "business_writes=0 external_api_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
