#!/usr/bin/env python3
"""Validate KWE endpoint skeleton against the no-write route fixture.

This script inspects local TypeScript route declarations. It does not start a
server and does not write KWE, KDS, WAES, GFIS, GPC, ledgers, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "kwe" / "endpoint-no-write-smoke.json"
ROUTES = ROOT / "packages" / "api" / "src" / "kwe" / "routes.ts"


def parse_routes() -> list[dict[str, Any]]:
    text = ROUTES.read_text()
    blocks = re.findall(r"\{\n\s+method: \"(GET|POST)\",\n\s+path: \"([^\"]+)\",(?P<body>.*?)\n\s+\}", text, re.S)
    routes: list[dict[str, Any]] = []
    for method, path, body in blocks:
        routes.append(
            {
                "method": method,
                "path": path,
                "routeMode": re.search(r"routeMode: \"([^\"]+)\"", body).group(1),
                "requiresWaesGate": re.search(r"requiresWaesGate: (true|false)", body).group(1) == "true",
                "requiresHumanOrCommitteeForFinality": re.search(
                    r"requiresHumanOrCommitteeForFinality: (true|false)", body
                ).group(1)
                == "true",
                "writesAcceptedFact": re.search(r"writesAcceptedFact: (true|false)", body).group(1) == "true",
                "writesBusinessSystem": re.search(r"writesBusinessSystem: (true|false)", body).group(1) == "true",
                "writesRevenueDistribution": re.search(r"writesRevenueDistribution: (true|false)", body).group(1)
                == "true",
                "writesExternalApi": re.search(r"writesExternalApi: (true|false)", body).group(1) == "true",
            }
        )
    return routes


def main() -> int:
    fixture = json.loads(FIXTURE.read_text())
    routes = parse_routes()
    failures: list[str] = []

    actual_triples = {(route["method"], route["path"], route["routeMode"]) for route in routes}
    expected_triples = {
        (item["method"], item["path"], item["routeMode"]) for item in fixture["expectedEndpoints"]
    }
    if actual_triples != expected_triples:
        failures.append(
            f"endpoint mismatch missing={sorted(expected_triples - actual_triples)} extra={sorted(actual_triples - expected_triples)}"
        )

    actual = {
        "endpointCount": len(routes),
        "readOnlyCount": sum(1 for route in routes if route["routeMode"] == "read_only"),
        "workRequestCount": sum(1 for route in routes if route["routeMode"] == "work_request"),
        "waesGatedRequestCount": sum(1 for route in routes if route["requiresWaesGate"]),
        "humanOrCommitteeFinalityCount": sum(1 for route in routes if route["requiresHumanOrCommitteeForFinality"]),
        "writesAcceptedFact": sum(1 for route in routes if route["writesAcceptedFact"]),
        "writesBusinessSystem": sum(1 for route in routes if route["writesBusinessSystem"]),
        "writesRevenueDistribution": sum(1 for route in routes if route["writesRevenueDistribution"]),
        "writesExternalApi": sum(1 for route in routes if route["writesExternalApi"]),
        "noWrite": True,
    }

    for key, expected_value in fixture["expected"].items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("kwe_endpoint_no_write_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kwe_endpoint_no_write_smoke=pass "
        f"endpoints={actual['endpointCount']} "
        f"read_only={actual['readOnlyCount']} "
        f"work_request={actual['workRequestCount']} "
        f"waes_gated_requests={actual['waesGatedRequestCount']} "
        f"human_or_committee_finality={actual['humanOrCommitteeFinalityCount']} "
        "writes_accepted_fact=0 writes_business_system=0 "
        "writes_revenue_distribution=0 writes_external_api=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
