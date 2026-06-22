#!/usr/bin/env python3
"""Validate P0 human review checklist dry-run without final acceptance writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-human-review-checklist-dry-run-v0.1.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    readiness_path = ROOT / data["sourceReadiness"]
    if not readiness_path.exists():
        failures.append(f"missing source readiness: {data['sourceReadiness']}")
        readiness = {}
    else:
        readiness = json.loads(readiness_path.read_text())

    if data.get("checklistStatus") != expected["checklistStatus"]:
        failures.append("checklistStatus must remain candidate")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("checklist must state notFinalAcceptance=true")
    if readiness.get("readinessStatus") != expected["sourceReadinessStatus"]:
        failures.append("source readiness status mismatch")

    review_items = data["reviewItems"]
    if len(review_items) != expected["reviewItemCount"]:
        failures.append("reviewItemCount mismatch")
    if len(data["riskRefs"]) != expected["riskRefCount"]:
        failures.append("riskRefCount mismatch")
    if len(data["forbiddenClosures"]) != expected["forbiddenClosureCount"]:
        failures.append("forbiddenClosureCount mismatch")

    item_ids = [item["id"] for item in review_items]
    if len(set(item_ids)) != len(item_ids):
        failures.append("review item ids must be unique")
    pending = [item for item in review_items if item.get("defaultOutcome") == "pending"]
    if len(pending) != expected["pendingOutcomeCount"]:
        failures.append("all review items must remain pending by default")

    source_actions = readiness.get("remainingHumanActions", [])
    for item in review_items:
        action_index = item["sourceActionIndex"]
        if action_index >= len(source_actions):
            failures.append(f"{item['id']} references missing source action index {action_index}")
        if not item.get("requiredEvidence"):
            failures.append(f"{item['id']} missing requiredEvidence")
        if "pending" in item.get("allowedOutcomes", []):
            failures.append(f"{item['id']} must not treat pending as a final allowed outcome")
        if item.get("defaultOutcome") != "pending":
            failures.append(f"{item['id']} defaultOutcome must be pending")

    readiness_risk_ids = {risk["id"] for risk in readiness.get("closureRisks", [])}
    for risk_ref in data["riskRefs"]:
        if risk_ref not in readiness_risk_ids:
            failures.append(f"risk ref not found in readiness source: {risk_ref}")

    forbidden_final_statuses = {"accepted", "integrated", "production_ready"}
    for forbidden in forbidden_final_statuses:
        if forbidden not in data["forbiddenClosures"]:
            failures.append(f"missing forbidden closure marker: {forbidden}")

    forbidden_terms = [
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"checklistStatus\": \"accepted\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden checklist term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_human_review_checklist_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_human_review_checklist_dry_run=pass "
        f"status={expected['checklistStatus']} "
        f"review_items={expected['reviewItemCount']} "
        f"pending_outcomes={expected['pendingOutcomeCount']} "
        f"risk_refs={expected['riskRefCount']} "
        "source_readiness_status=review_ready_candidate "
        "not_final_acceptance=covered "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
