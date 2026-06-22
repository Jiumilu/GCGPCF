#!/usr/bin/env python3
"""Generate P0 handler request/response dry-run fixture.

The generator derives examples from route files only. It does not start an API
server, connect databases, mutate KDS, write business systems, or call external
APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "fixtures" / "api" / "gckf-p0-handler-request-response-dry-run-v0.1.json"

GROUPS = [
    {
        "group": "kds_v2",
        "routeFile": "packages/api/src/kds/v2/routes.ts",
        "serviceName": "kdsV2Service",
    },
    {
        "group": "waes",
        "routeFile": "packages/api/src/waes/routes.ts",
        "serviceName": "waesService",
    },
    {
        "group": "kwe",
        "routeFile": "packages/api/src/kwe/routes.ts",
        "serviceName": "kweService",
    },
    {
        "group": "gfis_assistant",
        "routeFile": "packages/api/src/gfis/routes.ts",
        "serviceName": "gfisService",
    },
    {
        "group": "governance_loop",
        "routeFile": "packages/api/src/governance/routes.ts",
        "serviceName": "governanceService",
    },
]


def parse_endpoint_blocks(route_text: str) -> list[dict[str, str]]:
    blocks = re.findall(r"\{\n(.*?)\n\s*\}", route_text, re.S)
    endpoints: list[dict[str, str]] = []
    for block in blocks:
        method = re.search(r'method:\s*"([^"]+)"', block)
        path = re.search(r'path:\s*"([^"]+)"', block)
        handler = re.search(r'handler:\s*"([^"]+)"', block)
        if method and path and handler:
            endpoints.append(
                {
                    "method": method.group(1),
                    "path": path.group(1),
                    "handler": handler.group(1),
                    "block": block,
                }
            )
    return endpoints


def boundary_for(group: str, handler: str, block: str) -> str:
    if group == "waes":
        return "gate_check"
    if group == "kwe":
        return "read_only" if 'routeMode: "read_only"' in block else "work_request"
    if group == "gfis_assistant":
        return "read_only" if "query" in handler.lower() else "candidate_request"
    if group == "governance_loop":
        if "Ledger" in handler:
            return "ledger_read"
        if handler == "runKnowledgeCiDryRun" or handler == "getLoopRecord":
            return "read_only"
        return "governance_evidence_request"
    candidate_handlers = {
        "importSourceCandidate",
        "createFactCandidate",
        "createSopCandidate",
        "createWritebackCandidate",
    }
    return "candidate_request" if handler in candidate_handlers else "read_only"


def request_body(group: str, handler: str, boundary: str) -> dict[str, object]:
    base: dict[str, object] = {
        "tenantId": "tenant-gckf-p0",
        "requestId": f"REQ-{handler}",
        "dryRun": True,
    }
    if boundary == "read_only":
        base["query"] = f"dry-run {handler}"
    elif boundary == "candidate_request":
        base["candidate"] = {"id": f"CAND-{handler}", "lifecycle": "candidate"}
    elif boundary == "gate_check":
        base["objectId"] = f"OBJ-{handler}"
        base["gateTypes"] = ["RAG"]
    elif boundary == "work_request":
        base["workItem"] = {"id": f"KWE-{handler}", "status": "open"}
    elif boundary == "governance_evidence_request":
        base["evidence"] = {"id": f"EVD-{handler}", "status": "draft"}
    elif boundary == "ledger_read":
        base["ledgerScope"] = group
    return base


def main() -> int:
    cases = []
    for group in GROUPS:
        route_text = (ROOT / group["routeFile"]).read_text()
        for endpoint in parse_endpoint_blocks(route_text):
            boundary = boundary_for(group["group"], endpoint["handler"], endpoint["block"])
            cases.append(
                {
                    "id": f"{group['group']}:{endpoint['handler']}",
                    "group": group["group"],
                    "method": endpoint["method"],
                    "path": endpoint["path"],
                    "handler": endpoint["handler"],
                    "serviceName": group["serviceName"],
                    "serviceMethod": endpoint["handler"],
                    "writeBoundary": boundary,
                    "request": request_body(group["group"], endpoint["handler"], boundary),
                    "response": {
                        "ok": True,
                        "handler": endpoint["handler"],
                        "writeBoundary": boundary,
                        "candidateOnly": boundary in {"candidate_request", "work_request", "governance_evidence_request"},
                        "requiresGateOrReview": boundary in {
                            "candidate_request",
                            "gate_check",
                            "work_request",
                            "governance_evidence_request",
                        },
                        "noWrite": True,
                        "directBusinessWrite": False,
                        "acceptedLifecycleWrite": False,
                        "externalApiWrite": False,
                    },
                }
            )

    fixture = {
        "id": "gckf-p0-handler-request-response-dry-run-v0.1",
        "description": "P0-D12 generated request/response dry-run examples for all route handlers. Generated from route skeletons only.",
        "version": "v0.1",
        "generatedBy": "scripts/api/generate_gckf_p0_handler_request_response_fixture.py",
        "handlerMapRef": "fixtures/api/gckf-p0-handler-service-preflight-v0.1.json",
        "cases": cases,
        "expectedSummary": {
            "caseCount": len(cases),
            "groupCount": len(GROUPS),
            "forbiddenRuntimeTermMatches": 0,
            "startsServer": False,
            "connectsDatabase": False,
            "callsExternalApi": False,
            "writesKds": False,
            "writesBusinessSystem": False,
            "writesAcceptedLifecycle": False,
            "noWrite": True,
        },
    }
    OUTPUT.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n")
    print(f"generated {OUTPUT.relative_to(ROOT)} cases={len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
