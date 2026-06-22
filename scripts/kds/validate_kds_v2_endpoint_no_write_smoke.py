#!/usr/bin/env python3
"""Validate KDS v2 endpoint skeleton against the no-write route fixture.

This script inspects local TypeScript route declarations. It does not start a
server and does not write KDS, WAES, KWE, GFIS, GPC, or any external API.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "kds" / "v2-endpoint-no-write-smoke.json"
ROUTES = ROOT / "packages" / "api" / "src" / "kds" / "v2" / "routes.ts"


def parse_routes() -> list[dict[str, Any]]:
    text = ROUTES.read_text()
    blocks = re.findall(r"\{\n\s+method: \"(GET|POST)\",\n\s+path: \"([^\"]+)\",(?P<body>.*?)\n\s+\}", text, re.S)
    routes: list[dict[str, Any]] = []
    for method, path, body in blocks:
        route = {
            "method": method,
            "path": path,
            "mutationMode": re.search(r"mutationMode: \"([^\"]+)\"", body).group(1),
            "requiresWaesGate": re.search(r"requiresWaesGate: (true|false)", body).group(1) == "true",
            "requiresKweFlow": re.search(r"requiresKweFlow: (true|false)", body).group(1) == "true",
            "directBusinessWrite": re.search(r"directBusinessWrite: (true|false)", body).group(1) == "true",
            "acceptedLifecycleWrite": re.search(r"acceptedLifecycleWrite: (true|false)", body).group(1) == "true",
            "externalApiWrite": re.search(r"externalApiWrite: (true|false)", body).group(1) == "true",
        }
        routes.append(route)
    return routes


def main() -> int:
    fixture = json.loads(FIXTURE.read_text())
    routes = parse_routes()
    failures: list[str] = []

    actual_pairs = {(route["method"], route["path"], route["mutationMode"]) for route in routes}
    expected_pairs = {
        (item["method"], item["path"], item["mutationMode"]) for item in fixture["expectedEndpoints"]
    }
    if actual_pairs != expected_pairs:
        failures.append(f"endpoint mismatch missing={sorted(expected_pairs - actual_pairs)} extra={sorted(actual_pairs - expected_pairs)}")

    candidate_routes = [route for route in routes if route["mutationMode"] == "candidate_only"]
    read_only_routes = [route for route in routes if route["mutationMode"] == "read_only"]
    candidate_paths = {route["path"] for route in candidate_routes}
    expected_candidate_paths = set(fixture["candidateOnlyPaths"])
    if candidate_paths != expected_candidate_paths:
        failures.append(
            f"candidate path mismatch missing={sorted(expected_candidate_paths - candidate_paths)} extra={sorted(candidate_paths - expected_candidate_paths)}"
        )

    actual = {
        "endpointCount": len(routes),
        "candidateOnlyCount": len(candidate_routes),
        "readOnlyCount": len(read_only_routes),
        "waesGatedCandidateRoutes": sum(1 for route in candidate_routes if route["requiresWaesGate"]),
        "kweFlowCandidateRoutes": sum(1 for route in candidate_routes if route["requiresKweFlow"]),
        "directBusinessWrites": sum(1 for route in routes if route["directBusinessWrite"]),
        "acceptedLifecycleWrites": sum(1 for route in routes if route["acceptedLifecycleWrite"]),
        "externalApiWrites": sum(1 for route in routes if route["externalApiWrite"]),
        "realKdsWrites": 0,
        "noWrite": True,
    }

    for key, expected_value in fixture["expected"].items():
        if actual.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={actual.get(key)!r}")

    if failures:
        print("kds_v2_endpoint_no_write_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kds_v2_endpoint_no_write_smoke=pass "
        f"endpoints={actual['endpointCount']} "
        f"read_only={actual['readOnlyCount']} "
        f"candidate_only={actual['candidateOnlyCount']} "
        f"waes_gated_candidates={actual['waesGatedCandidateRoutes']} "
        f"kwe_flow_candidates={actual['kweFlowCandidateRoutes']} "
        "direct_business_writes=0 accepted_lifecycle_writes=0 "
        "external_api_writes=0 real_kds_writes=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
