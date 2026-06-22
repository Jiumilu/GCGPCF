#!/usr/bin/env python3
"""Validate Brain and PKC endpoint skeletons against no-write route fixture.

This script inspects local TypeScript route declarations. It does not start a
server and does not write KDS, WAES, KWE, business systems, ledgers, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "brain-pkc" / "endpoint-no-write-smoke.json"
BRAIN_ROUTES = ROOT / "packages" / "api" / "src" / "brain" / "routes.ts"
PKC_ROUTES = ROOT / "packages" / "api" / "src" / "pkc" / "routes.ts"


def parse_routes(path: Path, mode_key: str) -> list[dict[str, Any]]:
    text = path.read_text()
    blocks = re.findall(r"\{\n\s+method: \"(GET|POST)\",\n\s+path: \"([^\"]+)\",(?P<body>.*?)\n\s+\}", text, re.S)
    routes: list[dict[str, Any]] = []
    for method, route_path, body in blocks:
        route = {
            "method": method,
            "path": route_path,
            "routeMode": re.search(r"routeMode: \"([^\"]+)\"", body).group(1),
            "aggregatesKds": re.search(r"aggregatesKds: (true|false)", body).group(1) == "true",
            "aggregatesKwe": re.search(r"aggregatesKwe: (true|false)", body).group(1) == "true",
            "aggregatesGovernance": re.search(r"aggregatesGovernance: (true|false)", body).group(1) == "true",
            "writesKds": re.search(r"writesKds: (true|false)", body).group(1) == "true",
            "writesWaes": re.search(r"writesWaes: (true|false)", body).group(1) == "true",
            "writesKwe": re.search(r"writesKwe: (true|false)", body).group(1) == "true",
            "writesBusinessSystem": re.search(r"writesBusinessSystem: (true|false)", body).group(1) == "true",
            "writesRevenueDistribution": re.search(r"writesRevenueDistribution: (true|false)", body).group(1)
            == "true",
            "writesExternalApi": re.search(r"writesExternalApi: (true|false)", body).group(1) == "true",
        }
        if mode_key == "brain":
            route["aggregatesWaes"] = re.search(r"aggregatesWaes: (true|false)", body).group(1) == "true"
        else:
            route["aggregatesWaes"] = False
        routes.append(route)
    return routes


def assert_expected(label: str, routes: list[dict[str, Any]], expected_items: list[dict[str, str]]) -> list[str]:
    actual = {(route["method"], route["path"], route["routeMode"]) for route in routes}
    expected = {(item["method"], item["path"], item["routeMode"]) for item in expected_items}
    if actual == expected:
        return []
    return [f"{label} endpoint mismatch missing={sorted(expected - actual)} extra={sorted(actual - expected)}"]


def main() -> int:
    fixture = json.loads(FIXTURE.read_text())
    brain_routes = parse_routes(BRAIN_ROUTES, "brain")
    pkc_routes = parse_routes(PKC_ROUTES, "pkc")
    routes = brain_routes + pkc_routes
    failures: list[str] = []
    failures.extend(assert_expected("brain", brain_routes, fixture["expectedBrainEndpoints"]))
    failures.extend(assert_expected("pkc", pkc_routes, fixture["expectedPkcEndpoints"]))

    actual = {
        "brainEndpointCount": len(brain_routes),
        "pkcEndpointCount": len(pkc_routes),
        "aggregateReadCount": sum(1 for route in brain_routes if route["routeMode"] == "aggregate_read"),
        "dashboardReadCount": sum(1 for route in brain_routes if route["routeMode"] == "dashboard_read"),
        "governanceReadCount": sum(1 for route in brain_routes if route["routeMode"] == "governance_read"),
        "consoleReadCount": sum(1 for route in pkc_routes if route["routeMode"] == "console_read"),
        "taskReadCount": sum(1 for route in pkc_routes if route["routeMode"] == "task_read"),
        "ledgerReadCount": sum(1 for route in pkc_routes if route["routeMode"] == "ledger_read"),
        "routesAggregatingKds": sum(1 for route in routes if route["aggregatesKds"]),
        "routesAggregatingKwe": sum(1 for route in routes if route["aggregatesKwe"]),
        "routesAggregatingGovernance": sum(1 for route in routes if route["aggregatesGovernance"]),
        "writesKds": sum(1 for route in routes if route["writesKds"]),
        "writesWaes": sum(1 for route in routes if route["writesWaes"]),
        "writesKwe": sum(1 for route in routes if route["writesKwe"]),
        "writesBusinessSystem": sum(1 for route in routes if route["writesBusinessSystem"]),
        "writesRevenueDistribution": sum(1 for route in routes if route["writesRevenueDistribution"]),
        "writesExternalApi": sum(1 for route in routes if route["writesExternalApi"]),
        "noWrite": True,
    }

    for key, expected_value in fixture["expected"].items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("brain_pkc_endpoint_no_write_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "brain_pkc_endpoint_no_write_smoke=pass "
        f"brain_endpoints={actual['brainEndpointCount']} "
        f"pkc_endpoints={actual['pkcEndpointCount']} "
        f"aggregate_read={actual['aggregateReadCount']} "
        f"dashboard_read={actual['dashboardReadCount']} "
        f"governance_read={actual['governanceReadCount']} "
        f"console_read={actual['consoleReadCount']} "
        f"task_read={actual['taskReadCount']} "
        f"ledger_read={actual['ledgerReadCount']} "
        f"aggregates_kds={actual['routesAggregatingKds']} "
        f"aggregates_kwe={actual['routesAggregatingKwe']} "
        f"aggregates_governance={actual['routesAggregatingGovernance']} "
        "writes_kds=0 writes_waes=0 writes_kwe=0 writes_business_system=0 "
        "writes_revenue_distribution=0 writes_external_api=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
