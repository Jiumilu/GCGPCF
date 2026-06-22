#!/usr/bin/env python3
"""Validate the P0 handler stub envelope contract without server, DB, or writes."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-handler-stub-envelope-contract-v0.1.json"


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

    success_cases = data["successCases"]
    failure_cases = data["failureCases"]
    if len(success_cases) != expected["successCount"]:
        failures.append(f"successCount expected={expected['successCount']} actual={len(success_cases)}")
    if len(failure_cases) != expected["failureCount"]:
        failures.append(f"failureCount expected={expected['failureCount']} actual={len(failure_cases)}")
    all_case_ids = [case["id"] for case in success_cases + failure_cases]
    if len(set(all_case_ids)) != len(all_case_ids):
        failures.append("envelope case ids must be unique")

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
    ]
    for path in (handler_stub, handler_map):
        if path.exists():
            text = path.read_text()
            for term in forbidden_terms:
                if term in text:
                    failures.append(f"forbidden runtime/write term {term!r} in {path}")

    if failures:
        print("gckf_p0_handler_stub_envelope_contract=fail")
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
        failures.append(f"typescript envelope compile failed: {tsc.stderr or tsc.stdout}")
    if not compiled_stub.exists():
        failures.append(f"compiled handler stub missing: {compiled_stub}")
    if not compiled_handler_map.exists():
        failures.append(f"compiled handler map missing: {compiled_handler_map}")

    if not failures:
        node_source = f"""
const {{ invokeHandlerStubEnvelope }} = require({json.dumps(str(compiled_stub))});
const handlerMap = require({json.dumps(str(compiled_handler_map))});
const fixture = require({json.dumps(str(request_fixture))});
const successCases = {json.dumps(success_cases, ensure_ascii=False)};
const failureCases = {json.dumps(failure_cases, ensure_ascii=False)};
const requiredEnvelopeFields = {json.dumps(data["requiredEnvelopeFields"])};
const requiredSuccessFields = {json.dumps(data["requiredSuccessFields"])};
const requiredFailureFields = {json.dumps(data["requiredFailureFields"])};

const byId = new Map(fixture.cases.map((testCase) => [testCase.id, testCase]));
const summary = {{
  successCount: 0,
  failureCount: 0,
  envelopeFields: 0,
  successFields: 0,
  failureFields: 0,
  unknownHandlerEnveloped: false,
  missingServiceMethodEnveloped: false,
  noWriteGuards: 0,
  acceptedLifecycleBlocked: 0,
  directBusinessWriteBlocked: 0,
  externalApiWriteBlocked: 0
}};

function assertFields(testCaseId, response, fields) {{
  for (const field of fields) {{
    if (!(field in response)) {{
      throw new Error(`${{testCaseId}} missing envelope field ${{field}}`);
    }}
  }}
}}

function assertNoWrite(testCaseId, response) {{
  if (response.noWrite !== true) {{
    throw new Error(`${{testCaseId}} noWrite guard failed`);
  }}
  if (response.directBusinessWrite !== false) {{
    throw new Error(`${{testCaseId}} directBusinessWrite guard failed`);
  }}
  if (response.acceptedLifecycleWrite !== false) {{
    throw new Error(`${{testCaseId}} acceptedLifecycleWrite guard failed`);
  }}
  if (response.externalApiWrite !== false) {{
    throw new Error(`${{testCaseId}} externalApiWrite guard failed`);
  }}
  summary.noWriteGuards += 1;
  summary.acceptedLifecycleBlocked += 1;
  summary.directBusinessWriteBlocked += 1;
  summary.externalApiWriteBlocked += 1;
}}

for (const testCase of successCases) {{
  const sourceCase = byId.get(testCase.sourceCaseId);
  if (!sourceCase) {{
    throw new Error(`${{testCase.id}} missing source case ${{testCase.sourceCaseId}}`);
  }}
  const requestId = `${{testCase.id}}-request`;
  const traceId = `${{testCase.id}}-trace`;
  const response = invokeHandlerStubEnvelope({{
    handler: sourceCase.handler,
    request: sourceCase.request,
    requestId,
    traceId,
    dryRun: true
  }});
  assertFields(testCase.id, response, requiredEnvelopeFields);
  assertFields(testCase.id, response, requiredSuccessFields);
  assertNoWrite(testCase.id, response);
  if (response.ok !== true) {{
    throw new Error(`${{testCase.id}} expected ok=true`);
  }}
  if (response.requestId !== requestId || response.traceId !== traceId || response.dryRun !== true) {{
    throw new Error(`${{testCase.id}} did not preserve request metadata`);
  }}
  if (response.handler !== sourceCase.handler) {{
    throw new Error(`${{testCase.id}} did not preserve handler`);
  }}
  if (response.writeBoundary !== testCase.expectedBoundary) {{
    throw new Error(`${{testCase.id}} expected boundary ${{testCase.expectedBoundary}} actual ${{response.writeBoundary}}`);
  }}
  if (response.candidateOnly !== testCase.candidateOnly) {{
    throw new Error(`${{testCase.id}} expected candidateOnly ${{testCase.candidateOnly}} actual ${{response.candidateOnly}}`);
  }}
  const mapping = handlerMap.HANDLER_PREFLIGHT_MAPPINGS.find((item) => item.handler === sourceCase.handler);
  if (!mapping) {{
    throw new Error(`${{testCase.id}} missing handler mapping`);
  }}
  if (
    response.group !== mapping.group ||
    response.method !== mapping.method ||
    response.path !== mapping.path ||
    response.gateRequired !== mapping.requiresWaesGate ||
    response.kweRequired !== mapping.requiresKweFlow ||
    response.humanOrCommitteeRequired !== mapping.requiresHumanOrCommitteeForFinality
  ) {{
    throw new Error(`${{testCase.id}} envelope did not mirror mapping flags`);
  }}
  if (!response.preview || response.preview.noWrite !== true) {{
    throw new Error(`${{testCase.id}} missing no-write preview`);
  }}
  summary.successCount += 1;
  summary.envelopeFields += requiredEnvelopeFields.length;
  summary.successFields += requiredSuccessFields.length;
}}

for (const testCase of failureCases) {{
  if (testCase.expectedErrorCode === "MISSING_SERVICE_METHOD") {{
    handlerMap.HANDLER_PREFLIGHT_MAPPINGS.unshift({{
      group: "kds_v2",
      method: "GET",
      path: "/envelope/missing-service-method",
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
  }}
  const response = invokeHandlerStubEnvelope({{
    handler: testCase.handler,
    request: {{ dryRun: true }},
    requestId: `${{testCase.id}}-request`,
    traceId: `${{testCase.id}}-trace`,
    dryRun: true
  }});
  assertFields(testCase.id, response, requiredEnvelopeFields);
  assertFields(testCase.id, response, requiredFailureFields);
  assertNoWrite(testCase.id, response);
  if (response.ok !== false) {{
    throw new Error(`${{testCase.id}} expected ok=false`);
  }}
  if (response.errorCode !== testCase.expectedErrorCode) {{
    throw new Error(`${{testCase.id}} expected errorCode ${{testCase.expectedErrorCode}} actual ${{response.errorCode}}`);
  }}
  if (!response.errorMessage || typeof response.errorMessage !== "string") {{
    throw new Error(`${{testCase.id}} missing errorMessage`);
  }}
  if (response.errorCode === "UNKNOWN_HANDLER") {{
    summary.unknownHandlerEnveloped = true;
  }}
  if (response.errorCode === "MISSING_SERVICE_METHOD") {{
    summary.missingServiceMethodEnveloped = true;
  }}
  summary.failureCount += 1;
  summary.envelopeFields += requiredEnvelopeFields.length;
  summary.failureFields += requiredFailureFields.length;
}}

console.log(JSON.stringify(summary));
"""
        node = run_command(["node", "-e", node_source], ROOT)
        if node.returncode != 0:
            failures.append(f"handler stub envelope invocation failed: {node.stderr or node.stdout}")
        else:
            try:
                summary = json.loads(node.stdout)
            except json.JSONDecodeError as exc:
                failures.append(f"envelope summary was not JSON: {exc}: {node.stdout}")
                summary = {}

            if summary.get("successCount") != expected["successCount"]:
                failures.append(f"successCount expected={expected['successCount']} actual={summary.get('successCount')}")
            if summary.get("failureCount") != expected["failureCount"]:
                failures.append(f"failureCount expected={expected['failureCount']} actual={summary.get('failureCount')}")
            if summary.get("unknownHandlerEnveloped") is not expected["unknownHandlerEnveloped"]:
                failures.append("unknown handler was not enveloped")
            if summary.get("missingServiceMethodEnveloped") is not expected["missingServiceMethodEnveloped"]:
                failures.append("missing service method was not enveloped")
            for key in (
                "noWriteGuards",
                "acceptedLifecycleBlocked",
                "directBusinessWriteBlocked",
                "externalApiWriteBlocked",
            ):
                if summary.get(key) != expected["successCount"] + expected["failureCount"]:
                    failures.append(
                        f"{key} expected={expected['successCount'] + expected['failureCount']} actual={summary.get(key)}"
                    )

    if failures:
        print("gckf_p0_handler_stub_envelope_contract=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_handler_stub_envelope_contract=pass "
        f"success_cases={expected['successCount']} "
        f"failure_cases={expected['failureCount']} "
        "typescript_envelope_compile=pass "
        "invoke_handler_stub_envelope=pass "
        "unknown_handler=enveloped "
        "missing_service_method=enveloped "
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
