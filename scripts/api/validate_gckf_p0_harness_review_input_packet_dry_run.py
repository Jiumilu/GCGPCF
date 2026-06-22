#!/usr/bin/env python3
"""Validate P0 Harness review input packet dry-run without final evidence writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-review-input-packet-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    checklist = load_json(data["sourceChecklist"])
    readiness = load_json(data["sourceReadiness"])
    ledger = load_json(data["sourceLedger"])

    if data.get("packetStatus") != expected["packetStatus"]:
        failures.append("packetStatus must remain candidate")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("packet must state notFinalAcceptance=true")
    if checklist.get("checklistStatus") != expected["sourceChecklistStatus"]:
        failures.append("source checklist status mismatch")
    if readiness.get("readinessStatus") != expected["sourceReadinessStatus"]:
        failures.append("source readiness status mismatch")
    if ledger.get("ledgerStatus") != expected["sourceLedgerStatus"]:
        failures.append("source ledger status mismatch")

    harness_inputs = data["harnessInputs"]
    review_items = checklist["reviewItems"]
    ledger_entries = ledger["entries"]
    if len(harness_inputs) != expected["harnessInputCount"]:
        failures.append("harnessInputCount mismatch")
    if len(review_items) != expected["reviewItemCount"]:
        failures.append("reviewItemCount mismatch")
    if len(data["riskRefs"]) != expected["riskRefCount"]:
        failures.append("riskRefCount mismatch")
    if len(ledger_entries) != expected["ledgerEntryCount"]:
        failures.append("ledgerEntryCount mismatch")
    if len(data["requiredSourceRefs"]) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    review_item_ids = {item["id"] for item in review_items}
    harness_input_ids = [item["id"] for item in harness_inputs]
    if len(set(harness_input_ids)) != len(harness_input_ids):
        failures.append("harness input ids must be unique")
    for item in harness_inputs:
        if item["fromReviewItem"] not in review_item_ids:
            failures.append(f"{item['id']} references missing review item {item['fromReviewItem']}")
        if item.get("defaultOutcome") != "pending":
            failures.append(f"{item['id']} defaultOutcome must be pending")
        if "pending" in item.get("allowedOutcomes", []):
            failures.append(f"{item['id']} must not treat pending as a final allowed outcome")

    readiness_risk_ids = {risk["id"] for risk in readiness.get("closureRisks", [])}
    for risk_ref in data["riskRefs"]:
        if risk_ref not in readiness_risk_ids:
            failures.append(f"risk ref not found in readiness source: {risk_ref}")

    for source_ref in data["requiredSourceRefs"]:
        if not (ROOT / source_ref).exists():
            failures.append(f"required source ref missing: {source_ref}")

    review_scope = data["reviewScope"]
    if review_scope.get("candidateEvidenceRoundCount") != readiness["coveredRounds"]["candidateEvidenceRoundCount"]:
        failures.append("reviewScope candidateEvidenceRoundCount mismatch")
    if review_scope.get("reviewItemCount") != len(review_items):
        failures.append("reviewScope reviewItemCount mismatch")
    if review_scope.get("riskRefCount") != len(data["riskRefs"]):
        failures.append("reviewScope riskRefCount mismatch")
    if review_scope.get("ledgerEntryCount") != len(ledger_entries):
        failures.append("reviewScope ledgerEntryCount mismatch")

    forbidden_final_statuses = {"accepted", "integrated", "production_ready", "business_write_enabled"}
    for forbidden in forbidden_final_statuses:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")
    if data["packetStatus"] in forbidden_final_statuses:
        failures.append("packetStatus must not be a final closure status")

    forbidden_terms = [
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"packetStatus\": \"accepted\"",
        "\"packetStatus\": \"integrated\"",
        "\"packetStatus\": \"production_ready\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden packet term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_harness_review_input_packet_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_harness_review_input_packet_dry_run=pass "
        f"status={expected['packetStatus']} "
        f"harness_inputs={expected['harnessInputCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        f"checklist_items={expected['reviewItemCount']} "
        f"risk_refs={expected['riskRefCount']} "
        f"ledger_entries={expected['ledgerEntryCount']} "
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
