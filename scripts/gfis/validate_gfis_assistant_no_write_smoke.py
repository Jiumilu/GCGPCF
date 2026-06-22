#!/usr/bin/env python3
"""Validate GFIS Assistant no-write contract smoke fixtures.

This script verifies local response contracts only. It does not call GFIS,
KDS, WAES, GPC, ERP, MES, or any external API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "gfis" / "assistant-no-write-smoke.json"
ASSISTANTS = {"knowledge", "usage", "document_acceptance", "writeback_candidate"}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def validate_run(run: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    response = run.get("response", {})
    assistant = run.get("assistant")

    require(assistant in ASSISTANTS, f"{run.get('id')} unknown assistant={assistant!r}", failures)
    require(response.get("noWrite") is True, f"{run.get('id')} noWrite must be true", failures)
    require(response.get("businessWrites") == 0, f"{run.get('id')} businessWrites must be 0", failures)
    require(response.get("externalApiWrites") == 0, f"{run.get('id')} externalApiWrites must be 0", failures)

    if assistant == "knowledge":
        require(bool(response.get("citations")), f"{run.get('id')} must include citations", failures)
        require("answer" in response, f"{run.get('id')} must include answer", failures)
    if assistant == "usage":
        require(bool(response.get("manualConfirmationPoints")), f"{run.get('id')} must include manual confirmation points", failures)
    if assistant == "document_acceptance":
        require(bool(response.get("factCandidates")), f"{run.get('id')} must include fact candidates", failures)
        require(response.get("requiresHumanConfirmation") is True, f"{run.get('id')} must require human confirmation", failures)
    if assistant == "writeback_candidate":
        require(response.get("approvedForBusinessWrite") is False, f"{run.get('id')} must not approve business write", failures)

    return failures


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    failures: list[str] = []
    assistant_counts = {name: 0 for name in ASSISTANTS}

    for run in data["assistantRuns"]:
        assistant_counts[run["assistant"]] += 1
        failures.extend(validate_run(run))

    missing_assistants = [name for name, count in assistant_counts.items() if count == 0]
    if missing_assistants:
        failures.append("missing assistants: " + ",".join(sorted(missing_assistants)))

    if failures:
        print("gfis_assistant_no_write_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_assistant_no_write_smoke=pass "
        f"runs={len(data['assistantRuns'])} "
        "knowledge=covered usage=covered document_acceptance=covered writeback_candidate=covered "
        "business_writes=0 external_api_writes=0 kds_writes=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
