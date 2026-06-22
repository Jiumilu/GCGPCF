#!/usr/bin/env python3
"""Validate the P0 acceptance packet dry-run contract without Harness writes."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-acceptance-packet-dry-run-v0.1.json"


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

    acceptance_packet = ROOT / data["acceptancePacketPath"]
    route_adapter = ROOT / data["routeAdapterPath"]
    temp_out_dir = Path(data["tempOutDir"])
    compiled_acceptance_packet = Path(data["compiledAcceptancePacketPath"])

    for label, path in (
        ("acceptance packet", acceptance_packet),
        ("route adapter", route_adapter),
    ):
        if not path.exists():
            failures.append(f"missing {label}: {path}")

    packet_cases = data["packetCases"]
    evidence_refs = data["evidenceRefs"]
    if len(packet_cases) != expected["packetCount"]:
        failures.append(f"packetCount expected={expected['packetCount']} actual={len(packet_cases)}")
    if len(evidence_refs) != expected["evidenceRefCount"]:
        failures.append(f"evidenceRefCount expected={expected['evidenceRefCount']} actual={len(evidence_refs)}")
    if len({case["id"] for case in packet_cases}) != len(packet_cases):
        failures.append("packet case ids must be unique")
    for evidence in evidence_refs:
        ref_path = ROOT / evidence["ref"]
        if not ref_path.exists():
            failures.append(f"missing evidence ref {evidence['kind']}: {evidence['ref']}")

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
        "writesHarnessEvidence: true",
    ]
    for path in (acceptance_packet, route_adapter):
        if path.exists():
            text = path.read_text()
            for term in forbidden_terms:
                if term in text:
                    failures.append(f"forbidden runtime/write term {term!r} in {path}")

    if failures:
        print("gckf_p0_acceptance_packet_dry_run=fail")
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
        failures.append(f"typescript acceptance packet compile failed: {tsc.stderr or tsc.stdout}")
    if not compiled_acceptance_packet.exists():
        failures.append(f"compiled acceptance packet missing: {compiled_acceptance_packet}")

    if not failures:
        node_source = f"""
const {{
  createAcceptancePacketDryRun
}} = require({json.dumps(str(compiled_acceptance_packet))});
const packetCases = {json.dumps(packet_cases, ensure_ascii=False)};
const evidenceRefs = {json.dumps(evidence_refs, ensure_ascii=False)};

const summary = {{
  packetCount: 0,
  readyForReviewCount: 0,
  repairRequiredCount: 0,
  noWriteGuards: 0,
  startsServerBlocked: 0,
  connectsDatabaseBlocked: 0,
  callsExternalApiBlocked: 0,
  businessWriteBlocked: 0,
  acceptedLifecycleBlocked: 0,
  requiresHumanReview: 0,
  requiresHarnessEvidence: 0
}};

function assertNoWrite(testCaseId, packet) {{
  if (packet.noWrite !== true) {{
    throw new Error(`${{testCaseId}} noWrite guard failed`);
  }}
  if (packet.startsServer !== false) {{
    throw new Error(`${{testCaseId}} startsServer guard failed`);
  }}
  if (packet.connectsDatabase !== false) {{
    throw new Error(`${{testCaseId}} connectsDatabase guard failed`);
  }}
  if (packet.callsExternalApi !== false) {{
    throw new Error(`${{testCaseId}} callsExternalApi guard failed`);
  }}
  if (packet.directBusinessWrite !== false) {{
    throw new Error(`${{testCaseId}} directBusinessWrite guard failed`);
  }}
  if (packet.acceptedLifecycleWrite !== false) {{
    throw new Error(`${{testCaseId}} acceptedLifecycleWrite guard failed`);
  }}
  if (packet.externalApiWrite !== false) {{
    throw new Error(`${{testCaseId}} externalApiWrite guard failed`);
  }}
  for (const routeResult of packet.routeResults) {{
    if (routeResult.noWrite !== true || routeResult.envelope.noWrite !== true) {{
      throw new Error(`${{testCaseId}} route noWrite guard failed`);
    }}
  }}
  summary.noWriteGuards += 1;
  summary.startsServerBlocked += 1;
  summary.connectsDatabaseBlocked += 1;
  summary.callsExternalApiBlocked += 1;
  summary.businessWriteBlocked += 1;
  summary.acceptedLifecycleBlocked += 1;
}}

for (const testCase of packetCases) {{
  const packet = createAcceptancePacketDryRun({{
    packetId: testCase.packetId,
    title: testCase.title,
    routeRequests: testCase.routeRequests.map((routeRequest, index) => ({{
      ...routeRequest,
      body: {{ dryRunPayload: `${{testCase.id}}:${{index + 1}}` }},
      query: {{ tenantId: "tenant-gckf-p0" }},
      requestId: `${{testCase.id}}:route:${{index + 1}}`,
      traceId: `${{testCase.id}}:trace`,
      dryRun: true
    }})),
    evidenceRefs,
    requestedBy: "gckf-p0-loop",
    requestId: `${{testCase.id}}:packet`,
    traceId: `${{testCase.id}}:trace`,
    dryRun: true
  }});

  assertNoWrite(testCase.id, packet);
  if (packet.packetId !== testCase.packetId || packet.title !== testCase.title) {{
    throw new Error(`${{testCase.id}} did not preserve packet metadata`);
  }}
  if (packet.status !== testCase.expectedStatus || packet.ok !== testCase.expectedOk) {{
    throw new Error(`${{testCase.id}} expected status ${{testCase.expectedStatus}} ok ${{testCase.expectedOk}} actual status ${{packet.status}} ok ${{packet.ok}}`);
  }}
  if (packet.routeCount !== testCase.routeRequests.length || packet.routeResults.length !== testCase.routeRequests.length) {{
    throw new Error(`${{testCase.id}} route count mismatch`);
  }}
  if (packet.gateEvidenceRefs.length !== evidenceRefs.length) {{
    throw new Error(`${{testCase.id}} evidence refs mismatch`);
  }}
  if (packet.requiredHumanReview !== true) {{
    throw new Error(`${{testCase.id}} missing human review requirement`);
  }}
  if (packet.requiredHarnessEvidence !== true) {{
    throw new Error(`${{testCase.id}} missing Harness evidence requirement`);
  }}
  if (packet.status === "ready_for_review") {{
    if (packet.failureCount !== 0 || packet.successCount !== packet.routeCount) {{
      throw new Error(`${{testCase.id}} ready packet counts mismatch`);
    }}
    summary.readyForReviewCount += 1;
  }}
  if (packet.status === "repair_required") {{
    if (packet.failureCount < 1) {{
      throw new Error(`${{testCase.id}} repair packet did not preserve failure count`);
    }}
    summary.repairRequiredCount += 1;
  }}
  summary.requiresHumanReview += 1;
  summary.requiresHarnessEvidence += 1;
  summary.packetCount += 1;
}}

console.log(JSON.stringify(summary));
"""
        node = run_command(["node", "-e", node_source], ROOT)
        if node.returncode != 0:
            failures.append(f"acceptance packet dry-run invocation failed: {node.stderr or node.stdout}")
        else:
            try:
                summary = json.loads(node.stdout)
            except json.JSONDecodeError as exc:
                failures.append(f"acceptance packet summary was not JSON: {exc}: {node.stdout}")
                summary = {}

            if summary.get("packetCount") != expected["packetCount"]:
                failures.append(f"packetCount expected={expected['packetCount']} actual={summary.get('packetCount')}")
            if summary.get("readyForReviewCount") != expected["readyForReviewCount"]:
                failures.append(
                    f"readyForReviewCount expected={expected['readyForReviewCount']} actual={summary.get('readyForReviewCount')}"
                )
            if summary.get("repairRequiredCount") != expected["repairRequiredCount"]:
                failures.append(
                    f"repairRequiredCount expected={expected['repairRequiredCount']} actual={summary.get('repairRequiredCount')}"
                )
            for key in (
                "noWriteGuards",
                "startsServerBlocked",
                "connectsDatabaseBlocked",
                "callsExternalApiBlocked",
                "businessWriteBlocked",
                "acceptedLifecycleBlocked",
                "requiresHumanReview",
                "requiresHarnessEvidence",
            ):
                if summary.get(key) != expected["packetCount"]:
                    failures.append(f"{key} expected={expected['packetCount']} actual={summary.get(key)}")

    if failures:
        print("gckf_p0_acceptance_packet_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_acceptance_packet_dry_run=pass "
        f"packets={expected['packetCount']} "
        f"ready_for_review={expected['readyForReviewCount']} "
        f"repair_required={expected['repairRequiredCount']} "
        "typescript_acceptance_compile=pass "
        "create_acceptance_packet_dry_run=pass "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "requires_human_review=covered "
        "requires_harness_evidence=covered "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
