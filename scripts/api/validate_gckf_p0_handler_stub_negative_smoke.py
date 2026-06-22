#!/usr/bin/env python3
"""Negative smoke for the P0 handler stub without server, DB, or writes."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-handler-stub-negative-smoke-v0.1.json"


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

    request_fixture = ROOT / data["requestResponseFixture"]
    handler_stub = ROOT / data["handlerStubPath"]
    handler_map = ROOT / data["handlerMapPath"]
    temp_out_dir = Path(data["tempOutDir"])
    compiled_stub = Path(data["compiledStubPath"])
    compiled_handler_map = Path(data["compiledHandlerMapPath"])

    for label, path in (
        ("request/response fixture", request_fixture),
        ("handler stub", handler_stub),
        ("handler map", handler_map),
    ):
        if not path.exists():
            failures.append(f"missing {label}: {path}")

    negative_cases = data["negativeCases"]
    if len(negative_cases) != expected["negativeCaseCount"]:
        failures.append(
            f"negativeCaseCount expected={expected['negativeCaseCount']} actual={len(negative_cases)}"
        )
    if len({case["id"] for case in negative_cases}) != len(negative_cases):
        failures.append("negative case ids must be unique")

    if failures:
        print("gckf_p0_handler_stub_negative_smoke=fail")
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
        failures.append(f"typescript negative compile failed: {tsc.stderr or tsc.stdout}")
    if not compiled_stub.exists():
        failures.append(f"compiled handler stub missing: {compiled_stub}")
    if not compiled_handler_map.exists():
        failures.append(f"compiled handler map missing: {compiled_handler_map}")

    if not failures:
        node_source = f"""
const {{ invokeHandlerStub }} = require({json.dumps(str(compiled_stub))});
const handlerMap = require({json.dumps(str(compiled_handler_map))});
const fixture = require({json.dumps(str(request_fixture))});
const negativeCases = {json.dumps(negative_cases, ensure_ascii=False)};

const byId = new Map(fixture.cases.map((testCase) => [testCase.id, testCase]));
const summary = {{
  negativeCases: 0,
  throws: 0,
  guards: 0,
  noWriteGuards: 0,
  acceptedLifecycleBlocked: 0,
  directBusinessWriteBlocked: 0,
  externalApiWriteBlocked: 0
}};

function expectThrow(testCase, callback) {{
  try {{
    callback();
  }} catch (error) {{
    const message = String(error && error.message ? error.message : error);
    if (!message.includes(testCase.expectedMessage)) {{
      throw new Error(`${{testCase.id}} expected message ${{testCase.expectedMessage}} actual ${{message}}`);
    }}
    summary.throws += 1;
    return;
  }}
  throw new Error(`${{testCase.id}} did not throw`);
}}

for (const testCase of negativeCases) {{
  summary.negativeCases += 1;
  if (testCase.type === "throws") {{
    expectThrow(testCase, () => invokeHandlerStub({{ handler: testCase.handler, request: {{ dryRun: true }} }}));
    continue;
  }}

  if (testCase.type === "throws_after_mapping_injection") {{
    handlerMap.HANDLER_PREFLIGHT_MAPPINGS.unshift({{
      group: "kds_v2",
      method: "GET",
      path: "/negative-smoke/missing-service-method",
      handler: testCase.handler,
      serviceName: testCase.serviceName,
      serviceMethod: testCase.serviceMethod,
      writeBoundary: testCase.writeBoundary,
      requiresWaesGate: false,
      requiresKweFlow: false,
      requiresHumanOrCommitteeForFinality: false,
      directBusinessWrite: false,
      acceptedLifecycleWrite: false,
      externalApiWrite: false,
      noWrite: true
    }});
    expectThrow(testCase, () => invokeHandlerStub({{ handler: testCase.handler, request: {{ dryRun: true }} }}));
    continue;
  }}

  const sourceCase = byId.get(testCase.sourceCaseId);
  if (!sourceCase) {{
    throw new Error(`${{testCase.id}} missing source case ${{testCase.sourceCaseId}}`);
  }}
  const response = invokeHandlerStub({{ handler: sourceCase.handler, request: sourceCase.request }});
  if (response.ok !== true || response.noWrite !== true || response.preview.noWrite !== true) {{
    throw new Error(`${{testCase.id}} did not preserve noWrite response`);
  }}
  if (response.directBusinessWrite !== false || response.preview.writesBusinessSystem !== false) {{
    throw new Error(`${{testCase.id}} business write guard failed`);
  }}
  if (response.acceptedLifecycleWrite !== false || response.preview.writesAcceptedLifecycle !== false) {{
    throw new Error(`${{testCase.id}} accepted lifecycle guard failed`);
  }}
  if (response.externalApiWrite !== false || response.preview.callsExternalApi !== false) {{
    throw new Error(`${{testCase.id}} external API guard failed`);
  }}

  if (testCase.type === "boundary_guard") {{
    if (response.mapping.writeBoundary === testCase.forbiddenWriteBoundary) {{
      throw new Error(`${{testCase.id}} used forbidden writeBoundary ${{testCase.forbiddenWriteBoundary}}`);
    }}
    if (response.preview.operation === testCase.forbiddenWriteBoundary) {{
      throw new Error(`${{testCase.id}} preview used forbidden operation ${{testCase.forbiddenWriteBoundary}}`);
    }}
  }} else if (testCase.type === "candidate_no_write_guard") {{
    if (response.mapping.writeBoundary !== testCase.requiredWriteBoundary) {{
      throw new Error(`${{testCase.id}} mapping did not preserve candidate_request boundary`);
    }}
    if (response.preview.operation !== testCase.requiredWriteBoundary) {{
      throw new Error(`${{testCase.id}} preview did not preserve candidate_request operation`);
    }}
    if (response.mapping.requiresWaesGate !== true || response.mapping.requiresKweFlow !== true) {{
      throw new Error(`${{testCase.id}} candidate route did not preserve WAES/KWE finality guard`);
    }}
  }} else if (testCase.type === "accepted_lifecycle_guard") {{
    if (response.acceptedLifecycleWrite !== false || response.preview.writesAcceptedLifecycle !== false) {{
      throw new Error(`${{testCase.id}} accepted lifecycle write was not blocked`);
    }}
  }} else {{
    throw new Error(`${{testCase.id}} unsupported negative case type ${{testCase.type}}`);
  }}

  summary.guards += 1;
  summary.noWriteGuards += 1;
  summary.acceptedLifecycleBlocked += 1;
  summary.directBusinessWriteBlocked += 1;
  summary.externalApiWriteBlocked += 1;
}}

console.log(JSON.stringify(summary));
"""
        node = run_command(["node", "-e", node_source], ROOT)
        if node.returncode != 0:
            failures.append(f"handler stub negative invocation failed: {node.stderr or node.stdout}")
        else:
            try:
                summary = json.loads(node.stdout)
            except json.JSONDecodeError as exc:
                failures.append(f"negative summary was not JSON: {exc}: {node.stdout}")
                summary = {}

            if summary.get("negativeCases") != expected["negativeCaseCount"]:
                failures.append(
                    f"negativeCaseCount expected={expected['negativeCaseCount']} actual={summary.get('negativeCases')}"
                )
            if summary.get("throws") != expected["throwsCount"]:
                failures.append(f"throwsCount expected={expected['throwsCount']} actual={summary.get('throws')}")
            if summary.get("guards") != expected["guardCount"]:
                failures.append(f"guardCount expected={expected['guardCount']} actual={summary.get('guards')}")
            for key in (
                "noWriteGuards",
                "acceptedLifecycleBlocked",
                "directBusinessWriteBlocked",
                "externalApiWriteBlocked",
            ):
                if summary.get(key) != expected["guardCount"]:
                    failures.append(f"{key} expected={expected['guardCount']} actual={summary.get(key)}")

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
    if expected["compiled"] is not True or expected["invoked"] is not True:
        failures.append("compiled and invoked must both be true")
    if expected["noWrite"] is not True:
        failures.append("noWrite must be true")

    if failures:
        print("gckf_p0_handler_stub_negative_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_handler_stub_negative_smoke=pass "
        f"negative_cases={expected['negativeCaseCount']} throws={expected['throwsCount']} "
        f"guards={expected['guardCount']} typescript_negative_compile=pass "
        "unknown_handler=blocked missing_service_method=blocked "
        "boundary_guards=pass starts_server=0 connects_database=0 "
        "calls_external_api=0 writes_kds=0 writes_business_system=0 "
        "writes_accepted_lifecycle=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
