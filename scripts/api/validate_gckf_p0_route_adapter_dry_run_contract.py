#!/usr/bin/env python3
"""Validate the P0 route adapter dry-run contract without HTTP server or writes."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-route-adapter-dry-run-contract-v0.1.json"


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    route_adapter = ROOT / data["routeAdapterPath"]
    handler_stub = ROOT / data["handlerStubPath"]
    handler_map = ROOT / data["handlerMapPath"]
    temp_out_dir = Path(data["tempOutDir"])
    compiled_route_adapter = Path(data["compiledRouteAdapterPath"])

    for label, path in (
        ("route adapter", route_adapter),
        ("handler stub", handler_stub),
        ("handler map", handler_map),
    ):
        if not path.exists():
            failures.append(f"missing {label}: {path}")

    success_cases = data["successCases"]
    failure_cases = data["failureCases"]
    if len(success_cases) != expected["successCount"]:
        failures.append(f"successCount expected={expected['successCount']} actual={len(success_cases)}")
    if len(failure_cases) != expected["failureCount"]:
        failures.append(f"failureCount expected={expected['failureCount']} actual={len(failure_cases)}")
    all_case_ids = [case["id"] for case in success_cases + failure_cases]
    if len(set(all_case_ids)) != len(all_case_ids):
        failures.append("route adapter case ids must be unique")

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
    ]
    for path in (route_adapter, handler_stub, handler_map):
        if path.exists():
            text = path.read_text()
            for term in forbidden_terms:
                if term in text:
                    failures.append(f"forbidden runtime/write term {term!r} in {path}")

    if failures:
        print("gckf_p0_route_adapter_dry_run_contract=fail")
        for failure in failures:
            print(failure)
        return 1

    shutil.rmtree(temp_out_dir, ignore_errors=True)
    tsc = run_command(
        [
            "tsc",
            "-p",
            data["typescriptProject"],
            "--noEmit",
            "false",
            "--declaration",
            "false",
            "--emitDeclarationOnly",
            "false",
            "--outDir",
            str(temp_out_dir),
            "--module",
            "NodeNext",
            "--moduleResolution",
            "NodeNext",
        ],
        ROOT,
    )
    if tsc.returncode != 0:
        failures.append(f"typescript route adapter compile failed: {tsc.stderr or tsc.stdout}")
    if not compiled_route_adapter.exists():
        failures.append(f"compiled route adapter missing: {compiled_route_adapter}")

    if not failures:
        node_source = f"""
const {{
  adaptRouteDryRun,
  listRouteAdapterDryRunRoutes
}} = require({json.dumps(str(compiled_route_adapter))});
const successCases = {json.dumps(success_cases, ensure_ascii=False)};
const failureCases = {json.dumps(failure_cases, ensure_ascii=False)};

const summary = {{
  routeCount: 0,
  successCount: 0,
  failureCount: 0,
  noWriteGuards: 0,
  startsServerBlocked: 0,
  connectsDatabaseBlocked: 0,
  callsExternalApiBlocked: 0,
  businessWriteBlocked: 0,
  acceptedLifecycleBlocked: 0
}};

function assertNoWrite(testCaseId, response) {{
  if (response.noWrite !== true || response.envelope.noWrite !== true) {{
    throw new Error(`${{testCaseId}} noWrite guard failed`);
  }}
  if (response.startsServer !== false) {{
    throw new Error(`${{testCaseId}} startsServer guard failed`);
  }}
  if (response.connectsDatabase !== false) {{
    throw new Error(`${{testCaseId}} connectsDatabase guard failed`);
  }}
  if (response.callsExternalApi !== false) {{
    throw new Error(`${{testCaseId}} callsExternalApi guard failed`);
  }}
  if (response.directBusinessWrite !== false || response.envelope.directBusinessWrite !== false) {{
    throw new Error(`${{testCaseId}} directBusinessWrite guard failed`);
  }}
  if (response.acceptedLifecycleWrite !== false || response.envelope.acceptedLifecycleWrite !== false) {{
    throw new Error(`${{testCaseId}} acceptedLifecycleWrite guard failed`);
  }}
  if (response.externalApiWrite !== false || response.envelope.externalApiWrite !== false) {{
    throw new Error(`${{testCaseId}} externalApiWrite guard failed`);
  }}
  summary.noWriteGuards += 1;
  summary.startsServerBlocked += 1;
  summary.connectsDatabaseBlocked += 1;
  summary.callsExternalApiBlocked += 1;
  summary.businessWriteBlocked += 1;
  summary.acceptedLifecycleBlocked += 1;
}}

const routes = listRouteAdapterDryRunRoutes();
summary.routeCount = routes.length;
if (routes.length !== {expected["routeCount"]}) {{
  throw new Error(`route count expected {expected["routeCount"]} actual ${{routes.length}}`);
}}
const routeKeys = new Set(routes.map((route) => `${{route.method}} ${{route.path}}`));
if (routeKeys.size !== routes.length) {{
  throw new Error("route adapter contains duplicate method/path entries");
}}

for (const testCase of successCases) {{
  const response = adaptRouteDryRun({{
    method: testCase.method,
    path: testCase.path,
    body: {{ dryRunPayload: testCase.id }},
    query: {{ tenantId: "tenant-gckf-p0" }},
    requestId: `${{testCase.id}}-request`,
    traceId: `${{testCase.id}}-trace`,
    dryRun: true
  }});
  assertNoWrite(testCase.id, response);
  if (response.ok !== true || response.envelope.ok !== true) {{
    throw new Error(`${{testCase.id}} expected ok=true`);
  }}
  if (response.statusCode !== testCase.expectedStatusCode) {{
    throw new Error(`${{testCase.id}} expected status ${{testCase.expectedStatusCode}} actual ${{response.statusCode}}`);
  }}
  if (response.handler !== testCase.expectedHandler || response.envelope.handler !== testCase.expectedHandler) {{
    throw new Error(`${{testCase.id}} handler mismatch`);
  }}
  if (response.envelope.candidateOnly !== testCase.expectedCandidateOnly) {{
    throw new Error(`${{testCase.id}} candidateOnly mismatch`);
  }}
  if (response.requestId !== `${{testCase.id}}-request` || response.traceId !== `${{testCase.id}}-trace`) {{
    throw new Error(`${{testCase.id}} did not preserve request metadata`);
  }}
  summary.successCount += 1;
}}

for (const testCase of failureCases) {{
  const response = adaptRouteDryRun({{
    method: testCase.method,
    path: testCase.path,
    body: {{ dryRunPayload: testCase.id }},
    requestId: `${{testCase.id}}-request`,
    traceId: `${{testCase.id}}-trace`,
    dryRun: true
  }});
  assertNoWrite(testCase.id, response);
  if (response.ok !== false || response.envelope.ok !== false) {{
    throw new Error(`${{testCase.id}} expected ok=false`);
  }}
  if (response.statusCode !== testCase.expectedStatusCode) {{
    throw new Error(`${{testCase.id}} expected status ${{testCase.expectedStatusCode}} actual ${{response.statusCode}}`);
  }}
  if (response.envelope.errorCode !== testCase.expectedErrorCode) {{
    throw new Error(`${{testCase.id}} expected errorCode ${{testCase.expectedErrorCode}} actual ${{response.envelope.errorCode}}`);
  }}
  summary.failureCount += 1;
}}

console.log(JSON.stringify(summary));
"""
        node = run_command(["node", "-e", node_source], ROOT)
        if node.returncode != 0:
            failures.append(f"route adapter dry-run invocation failed: {node.stderr or node.stdout}")
        else:
            try:
                summary = json.loads(node.stdout)
            except json.JSONDecodeError as exc:
                failures.append(f"route adapter summary was not JSON: {exc}: {node.stdout}")
                summary = {}

            if summary.get("routeCount") != expected["routeCount"]:
                failures.append(f"routeCount expected={expected['routeCount']} actual={summary.get('routeCount')}")
            if summary.get("successCount") != expected["successCount"]:
                failures.append(f"successCount expected={expected['successCount']} actual={summary.get('successCount')}")
            if summary.get("failureCount") != expected["failureCount"]:
                failures.append(f"failureCount expected={expected['failureCount']} actual={summary.get('failureCount')}")
            total_cases = expected["successCount"] + expected["failureCount"]
            for key in (
                "noWriteGuards",
                "startsServerBlocked",
                "connectsDatabaseBlocked",
                "callsExternalApiBlocked",
                "businessWriteBlocked",
                "acceptedLifecycleBlocked",
            ):
                if summary.get(key) != total_cases:
                    failures.append(f"{key} expected={total_cases} actual={summary.get(key)}")

    if failures:
        print("gckf_p0_route_adapter_dry_run_contract=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_route_adapter_dry_run_contract=pass "
        f"routes={expected['routeCount']} "
        f"success_cases={expected['successCount']} "
        f"failure_cases={expected['failureCount']} "
        "typescript_route_compile=pass "
        "adapt_route_dry_run=pass "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
