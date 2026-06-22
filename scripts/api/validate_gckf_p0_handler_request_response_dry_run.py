#!/usr/bin/env python3
"""Validate P0 handler request/response dry-run examples."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-handler-request-response-dry-run-v0.1.json"
PREFLIGHT = ROOT / "fixtures" / "api" / "gckf-p0-handler-service-preflight-v0.1.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    preflight = json.loads(PREFLIGHT.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    cases = data["cases"]
    expected_count = preflight["expectedSummary"]["endpointCount"]
    if len(cases) != expected_count:
        failures.append(f"caseCount expected={expected_count} actual={len(cases)}")
    if len(cases) != expected["caseCount"]:
        failures.append(f"expectedSummary.caseCount expected={expected['caseCount']} actual={len(cases)}")

    groups = {case["group"] for case in cases}
    if len(groups) != expected["groupCount"]:
        failures.append(f"groupCount expected={expected['groupCount']} actual={len(groups)}")

    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        failures.append("case ids must be unique")

    for case in cases:
        response = case.get("response", {})
        request = case.get("request", {})
        if request.get("dryRun") is not True:
            failures.append(f"{case['id']} request.dryRun must be true")
        for key in ("noWrite",):
            if response.get(key) is not True:
                failures.append(f"{case['id']} response.{key} must be true")
        for key in ("directBusinessWrite", "acceptedLifecycleWrite", "externalApiWrite"):
            if response.get(key) is not False:
                failures.append(f"{case['id']} response.{key} must be false")
        if response.get("writeBoundary") != case.get("writeBoundary"):
            failures.append(f"{case['id']} response writeBoundary mismatch")
        if case.get("serviceMethod") != case.get("handler"):
            failures.append(f"{case['id']} serviceMethod must match handler")

    fixture_text = FIXTURE.read_text()
    forbidden_terms = ["fetch(", "axios", "PrismaClient", "INSERT INTO", "UPDATE ", "DELETE FROM", "DROP TABLE"]
    forbidden_matches = [term for term in forbidden_terms if term.lower() in fixture_text.lower()]
    if len(forbidden_matches) != expected["forbiddenRuntimeTermMatches"]:
        failures.append(f"forbiddenRuntimeTermMatches expected=0 actual={forbidden_matches}")

    tsc = subprocess.run(
        ["tsc", "-p", "packages/api/tsconfig.json", "--noEmit"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if tsc.returncode != 0:
        failures.append(f"typescript noEmit failed: {tsc.stderr or tsc.stdout}")

    for key in (
        "startsServer",
        "connectsDatabase",
        "callsExternalApi",
        "writesKds",
        "writesBusinessSystem",
        "writesAcceptedLifecycle",
    ):
        if expected[key] is not False:
            failures.append(f"{key} must be false")
    if expected["noWrite"] is not True:
        failures.append("noWrite must be true")

    if failures:
        print("gckf_p0_handler_request_response_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_handler_request_response_dry_run=pass "
        f"cases={len(cases)} groups={len(groups)} "
        "typescript_no_emit=pass forbidden_runtime_terms=0 starts_server=0 "
        "connects_database=0 calls_external_api=0 writes_kds=0 "
        "writes_business_system=0 writes_accepted_lifecycle=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
