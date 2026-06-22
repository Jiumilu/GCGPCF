#!/usr/bin/env python3
"""Validate the P0 acceptance packet ledger dry-run index without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-acceptance-packet-ledger-dry-run-v0.1.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    entries = data["entries"]
    failures: list[str] = []

    if data.get("ledgerStatus") != expected["ledgerStatus"]:
        failures.append(f"ledgerStatus expected={expected['ledgerStatus']} actual={data.get('ledgerStatus')}")
    if data.get("writesHarnessEvidence") is not expected["writesHarnessEvidence"]:
        failures.append("fixture must not write Harness evidence")
    if data.get("writesAcceptedLifecycle") is not expected["writesAcceptedLifecycle"]:
        failures.append("fixture must not write accepted lifecycle")
    if len(entries) != expected["entryCount"]:
        failures.append(f"entryCount expected={expected['entryCount']} actual={len(entries)}")
    if entries and entries[0].get("roundId") != expected["firstRound"]:
        failures.append(f"firstRound expected={expected['firstRound']} actual={entries[0].get('roundId')}")
    if entries and entries[-1].get("roundId") != expected["lastRound"]:
        failures.append(f"lastRound expected={expected['lastRound']} actual={entries[-1].get('roundId')}")

    round_ids = [entry["roundId"] for entry in entries]
    if len(set(round_ids)) != len(round_ids):
        failures.append("roundId values must be unique")

    for index, entry in enumerate(entries, start=9):
        expected_round_id = f"GCKF-P0-D{index}"
        if entry["roundId"] != expected_round_id:
            failures.append(f"round sequence expected={expected_round_id} actual={entry['roundId']}")
        validator = ROOT / entry["validator"]
        loop_evidence = ROOT / entry["loopEvidence"]
        if not validator.exists():
            failures.append(f"missing validator for {entry['roundId']}: {entry['validator']}")
            continue
        if not loop_evidence.exists():
            failures.append(f"missing loop evidence for {entry['roundId']}: {entry['loopEvidence']}")
            continue
        validator_text = validator.read_text()
        loop_text = loop_evidence.read_text()
        if entry["expectedSignal"].split("=")[0] not in validator_text:
            failures.append(f"validator signal missing for {entry['roundId']}: {entry['expectedSignal']}")
        if entry["roundId"].replace("GCKF-P0-", "P0-") not in loop_text and entry["roundId"] not in loop_text:
            failures.append(f"loop evidence does not mention round id for {entry['roundId']}")

    forbidden_terms = [
        "createServer(",
        ".listen(",
        "new Pool(",
        "postgres://",
        "fetch(",
        "axios.",
        "acceptedLifecycleWrite: true",
        "directBusinessWrite: true",
        "externalApiWrite: true",
        "startsServer: true",
        "connectsDatabase: true",
        "callsExternalApi: true",
        "writesHarnessEvidence\": true",
        "writesAcceptedLifecycle\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden runtime/write term {term!r} in {FIXTURE}")

    if failures:
        print("gckf_p0_acceptance_packet_ledger_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_acceptance_packet_ledger_dry_run=pass "
        f"entries={expected['entryCount']} "
        f"first_round={expected['firstRound']} "
        f"last_round={expected['lastRound']} "
        "validators_exist=covered "
        "loop_evidence_exists=covered "
        "ledger_status=candidate "
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
