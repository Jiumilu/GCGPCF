#!/usr/bin/env python3
"""Validate P0 handler stub preview boundary."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-handler-stub-preview-v0.1.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    stub_path = ROOT / data["handlerStubPath"]
    map_path = ROOT / data["handlerMapPath"]
    index_path = ROOT / data["indexPath"]
    request_fixture_path = ROOT / data["requestResponseFixture"]
    for label, path in (
        ("handler stub", stub_path),
        ("handler map", map_path),
        ("index", index_path),
        ("request/response fixture", request_fixture_path),
    ):
        if not path.exists():
            failures.append(f"missing {label}: {path.relative_to(ROOT)}")

    stub_text = stub_path.read_text() if stub_path.exists() else ""
    map_text = map_path.read_text() if map_path.exists() else ""
    index_text = index_path.read_text() if index_path.exists() else ""
    request_fixture = json.loads(request_fixture_path.read_text()) if request_fixture_path.exists() else {"cases": []}

    for term in data["requiredStubTerms"]:
        if term not in stub_text:
            failures.append(f"missing stub term: {term}")
    if 'export * from "./handler-stub";' not in index_text:
        failures.append("missing index export: ./handler-stub")

    cases = request_fixture["cases"]
    if len(cases) != expected["caseCount"]:
        failures.append(f"caseCount expected={expected['caseCount']} actual={len(cases)}")
    handlers = [case["handler"] for case in cases]
    if len(handlers) != len(set(handlers)):
        failures.append("handler fixture names must be unique")

    service_names = {case["serviceName"] for case in cases}
    for service_name in service_names:
        if f"{service_name}:" not in stub_text:
            failures.append(f"missing service registry entry: {service_name}")

    for case in cases:
        if case["serviceMethod"] != case["handler"]:
            failures.append(f"{case['id']} serviceMethod must equal handler")
        response = case["response"]
        if response["noWrite"] is not True:
            failures.append(f"{case['id']} response.noWrite must be true")
        for key in ("directBusinessWrite", "acceptedLifecycleWrite", "externalApiWrite"):
            if response[key] is not False:
                failures.append(f"{case['id']} response.{key} must be false")

    spread_count = len(re.findall(r"\.\.\.[A-Z0-9_]+_ENDPOINTS\.map\(", map_text))
    if spread_count != 5:
        failures.append(f"handler map must preserve 5 endpoint spreads, actual={spread_count}")

    checked_text = "\n".join(
        path.read_text()
        for path in (stub_path, map_path, index_path)
        if path.exists()
    )
    forbidden_matches = [term for term in data["forbiddenRuntimeTerms"] if term.lower() in checked_text.lower()]
    if len(forbidden_matches) != expected["forbiddenRuntimeTermMatches"]:
        failures.append(f"forbiddenRuntimeTermMatches expected=0 actual={forbidden_matches}")

    tsc = subprocess.run(
        ["tsc", "-p", data["typescriptProject"], "--noEmit"],
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
    if expected["typescriptNoEmit"] is not True:
        failures.append("typescriptNoEmit must be true")
    if expected["noWrite"] is not True:
        failures.append("noWrite must be true")

    if failures:
        print("gckf_p0_handler_stub_preview=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_handler_stub_preview=pass "
        f"cases={len(cases)} service_registry={len(service_names)} "
        "typescript_no_emit=pass forbidden_runtime_terms=0 starts_server=0 "
        "connects_database=0 calls_external_api=0 writes_kds=0 "
        "writes_business_system=0 writes_accepted_lifecycle=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
