#!/usr/bin/env python3
"""Validate Governance endpoint skeleton against no-write route fixture.

This script inspects local TypeScript route declarations. It does not start a
server and does not write governance ledgers, KDS, WAES, KWE, GFIS, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "governance" / "endpoint-no-write-smoke.json"
ROUTES = ROOT / "packages" / "api" / "src" / "governance" / "routes.ts"


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
                "requiresEvidenceBoundary": re.search(r"requiresEvidenceBoundary: (true|false)", body).group(1)
                == "true",
                "dryRunOnly": re.search(r"dryRunOnly: (true|false)", body).group(1) == "true",
                "writesBusinessSystem": re.search(r"writesBusinessSystem: (true|false)", body).group(1) == "true",
                "writesAcceptedFact": re.search(r"writesAcceptedFact: (true|false)", body).group(1) == "true",
                "writesRevenueDistribution": re.search(r"writesRevenueDistribution: (true|false)", body).group(1)
                == "true",
                "writesQuotaMutation": re.search(r"writesQuotaMutation: (true|false)", body).group(1) == "true",
                "writesBountySettlement": re.search(r"writesBountySettlement: (true|false)", body).group(1)
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
        "loopRecordRequestCount": sum(1 for route in routes if route["routeMode"] == "loop_record_request"),
        "evidenceRequestCount": sum(1 for route in routes if route["routeMode"] == "evidence_request"),
        "knowledgeCiDryRunCount": sum(1 for route in routes if route["routeMode"] == "knowledge_ci_dry_run"),
        "routesRequiringEvidenceBoundary": sum(1 for route in routes if route["requiresEvidenceBoundary"]),
        "dryRunOnlyCount": sum(1 for route in routes if route["dryRunOnly"]),
        "writesBusinessSystem": sum(1 for route in routes if route["writesBusinessSystem"]),
        "writesAcceptedFact": sum(1 for route in routes if route["writesAcceptedFact"]),
        "writesRevenueDistribution": sum(1 for route in routes if route["writesRevenueDistribution"]),
        "writesQuotaMutation": sum(1 for route in routes if route["writesQuotaMutation"]),
        "writesBountySettlement": sum(1 for route in routes if route["writesBountySettlement"]),
        "writesExternalApi": sum(1 for route in routes if route["writesExternalApi"]),
        "noWrite": True,
    }

    for key, expected_value in fixture["expected"].items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("governance_endpoint_no_write_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "governance_endpoint_no_write_smoke=pass "
        f"endpoints={actual['endpointCount']} "
        f"read_only={actual['readOnlyCount']} "
        f"loop_record_request={actual['loopRecordRequestCount']} "
        f"evidence_request={actual['evidenceRequestCount']} "
        f"knowledge_ci_dry_run={actual['knowledgeCiDryRunCount']} "
        f"evidence_boundary={actual['routesRequiringEvidenceBoundary']} "
        f"dry_run_only={actual['dryRunOnlyCount']} "
        "writes_business_system=0 writes_accepted_fact=0 writes_revenue_distribution=0 "
        "writes_quota_mutation=0 writes_bounty_settlement=0 writes_external_api=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
