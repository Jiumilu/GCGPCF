#!/usr/bin/env python3
"""Validate P0 closure readiness dry-run without final acceptance writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-closure-readiness-dry-run-v0.1.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_ledger = ROOT / data["sourceLedger"]
    if not source_ledger.exists():
        failures.append(f"missing source ledger: {data['sourceLedger']}")
        ledger = {}
    else:
        ledger = json.loads(source_ledger.read_text())

    if data.get("readinessStatus") != expected["readinessStatus"]:
        failures.append(
            f"readinessStatus expected={expected['readinessStatus']} actual={data.get('readinessStatus')}"
        )
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("readiness fixture must state notFinalAcceptance=true")
    if ledger.get("ledgerStatus") != expected["sourceLedgerStatus"]:
        failures.append(f"source ledger must remain {expected['sourceLedgerStatus']}")

    covered = data["coveredRounds"]
    if covered["candidateEvidenceRoundCount"] != expected["candidateEvidenceRoundCount"]:
        failures.append("candidateEvidenceRoundCount mismatch")
    if covered["firstRound"] != "GCKF-P0-D9" or covered["lastRound"] != "GCKF-P0-D19":
        failures.append("covered rounds must span D9-D19")

    ledger_entries = ledger.get("entries", [])
    if len(ledger_entries) + 1 != expected["candidateEvidenceRoundCount"]:
        failures.append(
            "candidateEvidenceRoundCount must equal D19 ledger entries plus D19 readiness input"
        )

    if len(data["remainingHumanActions"]) != expected["remainingHumanActionCount"]:
        failures.append("remainingHumanActionCount mismatch")
    open_risks = [risk for risk in data["closureRisks"] if risk.get("status") == "open"]
    if len(open_risks) != expected["openRiskCount"]:
        failures.append("openRiskCount mismatch")
    if len(data["forbiddenClosures"]) != expected["forbiddenClosureCount"]:
        failures.append("forbiddenClosureCount mismatch")

    forbidden_final_statuses = {"accepted", "integrated", "production_ready"}
    if data["readinessStatus"] in forbidden_final_statuses:
        failures.append("dry-run readiness must not use a final status")
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
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden readiness term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_closure_readiness_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_closure_readiness_dry_run=pass "
        f"status={expected['readinessStatus']} "
        f"candidate_rounds={expected['candidateEvidenceRoundCount']} "
        f"remaining_human_actions={expected['remainingHumanActionCount']} "
        f"open_risks={expected['openRiskCount']} "
        "source_ledger_status=candidate "
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
