#!/usr/bin/env python3
"""Validate P0 handler-to-service dry-run preflight mapping.

This validator checks static TypeScript files and runs TypeScript noEmit only.
It does not start an API server, connect databases, mutate KDS, write business
systems, run migrations, or call external APIs.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-handler-service-preflight-v0.1.json"


def read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def route_handlers(route_text: str) -> list[str]:
    return re.findall(r'handler:\s*"([^"]+)"', route_text)


def service_methods(service_text: str) -> set[str]:
    return set(re.findall(r"\n\s{2}([A-Za-z0-9_]+)\(", service_text))


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    handler_map_path = ROOT / data["handlerMapPath"]
    index_path = ROOT / data["indexPath"]
    if not handler_map_path.exists():
        failures.append(f"missing handler map: {data['handlerMapPath']}")
    if not index_path.exists():
        failures.append(f"missing API index: {data['indexPath']}")

    handler_map_text = handler_map_path.read_text() if handler_map_path.exists() else ""
    index_text = index_path.read_text() if index_path.exists() else ""

    if 'export * from "./handler-map";' not in index_text:
        failures.append("missing index export: ./handler-map")

    for flag in data["requiredMapFlags"]:
        if flag not in handler_map_text:
            failures.append(f"missing handler map no-write flag: {flag}")

    all_handlers: list[str] = []
    service_coverage = 0
    groups = data["groups"]
    if len(groups) != expected["groupCount"]:
        failures.append(f"groupCount expected={expected['groupCount']} actual={len(groups)}")

    for group in groups:
        route_file = ROOT / group["routeFile"]
        service_file = ROOT / group["serviceFile"]
        if not route_file.exists():
            failures.append(f"missing route file: {group['routeFile']}")
            continue
        if not service_file.exists():
            failures.append(f"missing service file: {group['serviceFile']}")
            continue

        handlers = route_handlers(route_file.read_text())
        methods = service_methods(service_file.read_text())
        all_handlers.extend(handlers)
        if len(handlers) != group["expectedEndpointCount"]:
            failures.append(
                f"{group['group']} endpointCount expected={group['expectedEndpointCount']} actual={len(handlers)}"
            )

        if f'group: "{group["group"]}"' not in handler_map_text:
            failures.append(f"missing handler map group: {group['group']}")
        if f'serviceName: "{group["serviceName"]}"' not in handler_map_text:
            failures.append(f"missing handler map serviceName: {group['serviceName']}")

        for handler in handlers:
            if handler in methods:
                service_coverage += 1
            else:
                failures.append(f"missing service method implementation: {handler}")

    endpoint_count = len(all_handlers)
    if endpoint_count != expected["endpointCount"]:
        failures.append(f"endpointCount expected={expected['endpointCount']} actual={endpoint_count}")
    if len(set(all_handlers)) != endpoint_count:
        failures.append("handler names must be unique across P0 routes")

    required_spreads = {
        "kds_v2": "...KDS_V2_ENDPOINTS.map(mapKdsEndpoint)",
        "waes": "...WAES_ENDPOINTS.map(mapWaesEndpoint)",
        "kwe": "...KWE_ENDPOINTS.map(mapKweEndpoint)",
        "gfis_assistant": "...GFIS_ENDPOINTS.map(mapGfisEndpoint)",
        "governance_loop": "...GOVERNANCE_ENDPOINTS.map(mapGovernanceEndpoint)",
    }
    for group_name, spread in required_spreads.items():
        if spread not in handler_map_text:
            failures.append(f"missing handler map spread: {group_name}")
    if "handler: endpoint.handler" not in handler_map_text:
        failures.append("handler map must preserve endpoint.handler")
    if "serviceMethod: endpoint.handler" not in handler_map_text:
        failures.append("handler map must preserve serviceMethod endpoint.handler")
    map_count = endpoint_count if not [spread for spread in required_spreads.values() if spread not in handler_map_text] else 0
    if map_count != expected["handlerMapCount"]:
        failures.append(f"handlerMapCount expected={expected['handlerMapCount']} actual={map_count}")
    if service_coverage != expected["serviceCoverageCount"]:
        failures.append(f"serviceCoverageCount expected={expected['serviceCoverageCount']} actual={service_coverage}")

    checked_paths = [data["handlerMapPath"], data["indexPath"]]
    checked_paths.extend(path for group in groups for path in (group["routeFile"], group["serviceFile"]))
    checked_text = "\n".join(read_text(path) for path in checked_paths if (ROOT / path).exists())
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
        print("gckf_p0_handler_service_preflight=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_handler_service_preflight=pass "
        f"groups={expected['groupCount']} endpoints={endpoint_count} "
        f"handler_maps={map_count} service_coverage={service_coverage} "
        "typescript_no_emit=pass forbidden_runtime_terms=0 starts_server=0 "
        "connects_database=0 calls_external_api=0 writes_kds=0 "
        "writes_business_system=0 writes_accepted_lifecycle=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
