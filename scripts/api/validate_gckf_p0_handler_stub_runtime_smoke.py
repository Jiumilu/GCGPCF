#!/usr/bin/env python3
"""Runtime smoke for the P0 handler stub without server, DB, or writes."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-handler-stub-runtime-smoke-v0.1.json"


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
    temp_out_dir = Path(data["tempOutDir"])
    compiled_stub = Path(data["compiledStubPath"])

    for label, path in (
        ("request/response fixture", request_fixture),
        ("handler stub", handler_stub),
    ):
        if not path.exists():
            failures.append(f"missing {label}: {path}")

    if failures:
        print("gckf_p0_handler_stub_runtime_smoke=fail")
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
        failures.append(f"typescript runtime compile failed: {tsc.stderr or tsc.stdout}")
    if not compiled_stub.exists():
        failures.append(f"compiled handler stub missing: {compiled_stub}")

    if not failures:
        node_source = f"""
const {{ invokeHandlerStub }} = require({json.dumps(str(compiled_stub))});
const fixture = require({json.dumps(str(request_fixture))});

const summary = {{
  cases: 0,
  groups: {{}},
  operations: {{}},
  noWrite: 0,
  directBusinessWriteFalse: 0,
  acceptedLifecycleWriteFalse: 0,
  externalApiWriteFalse: 0,
  connectsDatabaseFalse: 0,
  callsExternalApiFalse: 0,
  writesKdsFalse: 0,
  writesBusinessSystemFalse: 0,
  writesAcceptedLifecycleFalse: 0
}};

for (const testCase of fixture.cases) {{
  const response = invokeHandlerStub({{
    handler: testCase.handler,
    request: testCase.request
  }});

  if (response.ok !== true) {{
    throw new Error(`${{testCase.id}} did not return ok=true`);
  }}
  if (response.mapping.handler !== testCase.handler) {{
    throw new Error(`${{testCase.id}} handler mapping mismatch`);
  }}
  if (response.mapping.group !== testCase.group) {{
    throw new Error(`${{testCase.id}} group mapping mismatch`);
  }}
  if (response.mapping.serviceName !== testCase.serviceName) {{
    throw new Error(`${{testCase.id}} serviceName mapping mismatch`);
  }}
  if (response.mapping.serviceMethod !== testCase.serviceMethod) {{
    throw new Error(`${{testCase.id}} serviceMethod mapping mismatch`);
  }}
  if (response.mapping.writeBoundary !== testCase.writeBoundary) {{
    throw new Error(`${{testCase.id}} writeBoundary mapping mismatch`);
  }}
  if (response.preview.operation !== testCase.writeBoundary) {{
    throw new Error(`${{testCase.id}} preview operation mismatch`);
  }}

  summary.cases += 1;
  summary.groups[testCase.group] = (summary.groups[testCase.group] || 0) + 1;
  summary.operations[response.preview.operation] = (summary.operations[response.preview.operation] || 0) + 1;
  if (response.noWrite === true && response.preview.noWrite === true) summary.noWrite += 1;
  if (response.directBusinessWrite === false) summary.directBusinessWriteFalse += 1;
  if (response.acceptedLifecycleWrite === false) summary.acceptedLifecycleWriteFalse += 1;
  if (response.externalApiWrite === false) summary.externalApiWriteFalse += 1;
  if (response.preview.connectsDatabase === false) summary.connectsDatabaseFalse += 1;
  if (response.preview.callsExternalApi === false) summary.callsExternalApiFalse += 1;
  if (response.preview.writesKds === false) summary.writesKdsFalse += 1;
  if (response.preview.writesBusinessSystem === false) summary.writesBusinessSystemFalse += 1;
  if (response.preview.writesAcceptedLifecycle === false) summary.writesAcceptedLifecycleFalse += 1;
}}

console.log(JSON.stringify(summary));
"""
        node = run_command(["node", "-e", node_source], ROOT)
        if node.returncode != 0:
            failures.append(f"handler stub runtime invocation failed: {node.stderr or node.stdout}")
        else:
            try:
                summary = json.loads(node.stdout)
            except json.JSONDecodeError as exc:
                failures.append(f"runtime summary was not JSON: {exc}: {node.stdout}")
                summary = {}

            case_count = summary.get("cases")
            group_count = len(summary.get("groups", {}))
            if case_count != expected["caseCount"]:
                failures.append(f"caseCount expected={expected['caseCount']} actual={case_count}")
            if group_count != expected["groupCount"]:
                failures.append(f"groupCount expected={expected['groupCount']} actual={group_count}")
            for key in (
                "noWrite",
                "directBusinessWriteFalse",
                "acceptedLifecycleWriteFalse",
                "externalApiWriteFalse",
                "connectsDatabaseFalse",
                "callsExternalApiFalse",
                "writesKdsFalse",
                "writesBusinessSystemFalse",
                "writesAcceptedLifecycleFalse",
            ):
                if summary.get(key) != expected["caseCount"]:
                    failures.append(f"{key} expected={expected['caseCount']} actual={summary.get(key)}")

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
        print("gckf_p0_handler_stub_runtime_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_handler_stub_runtime_smoke=pass "
        f"cases={expected['caseCount']} groups={expected['groupCount']} "
        "typescript_runtime_compile=pass invoke_handler_stub=pass "
        "starts_server=0 connects_database=0 calls_external_api=0 "
        "writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
