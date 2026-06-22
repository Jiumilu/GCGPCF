#!/usr/bin/env python3
"""Validate P0 repository/service dry-run skeletons.

This validator checks local TypeScript files and runs TypeScript noEmit only.
It does not start servers, connect databases, mutate KDS, write business
systems, run migrations, or call external APIs.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-repository-service-dry-run-v0.1.json"


def read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    common_contract = ROOT / data["commonContract"]
    index_path = ROOT / data["indexPath"]
    if not common_contract.exists():
        failures.append(f"missing common contract: {data['commonContract']}")
    if not index_path.exists():
        failures.append(f"missing API index: {data['indexPath']}")

    common_text = common_contract.read_text() if common_contract.exists() else ""
    for flag in data["requiredCommonFlags"]:
        if flag not in common_text:
            failures.append(f"missing common no-write flag: {flag}")

    index_text = index_path.read_text() if index_path.exists() else ""
    repository_count = 0
    service_count = 0
    operation_count = 0
    index_export_count = 0
    forbidden_matches: list[str] = []

    groups = data["groups"]
    if len(groups) != expected["groupCount"]:
        failures.append(f"groupCount expected={expected['groupCount']} actual={len(groups)}")

    for group in groups:
        repository_path = ROOT / group["repository"]
        service_path = ROOT / group["service"]
        if repository_path.exists():
            repository_count += 1
        else:
            failures.append(f"missing repository: {group['repository']}")
        if service_path.exists():
            service_count += 1
        else:
            failures.append(f"missing service: {group['service']}")

        service_text = service_path.read_text() if service_path.exists() else ""
        operation_count += service_text.count(".preview(")
        for export_path in group["requiredExports"]:
            if f'export * from "{export_path}";' in index_text:
                index_export_count += 1
            else:
                failures.append(f"missing index export: {export_path}")

        if service_text.count(".preview(") != group["expectedOperationCount"]:
            failures.append(
                f"{group['group']} operationCount expected={group['expectedOperationCount']} "
                f"actual={service_text.count('.preview(')}"
            )

    if repository_count != expected["repositoryCount"]:
        failures.append(f"repositoryCount expected={expected['repositoryCount']} actual={repository_count}")
    if service_count != expected["serviceCount"]:
        failures.append(f"serviceCount expected={expected['serviceCount']} actual={service_count}")
    if operation_count != expected["operationCount"]:
        failures.append(f"operationCount expected={expected['operationCount']} actual={operation_count}")
    if index_export_count != expected["indexExportCount"]:
        failures.append(f"indexExportCount expected={expected['indexExportCount']} actual={index_export_count}")

    checked_paths = [data["commonContract"], data["indexPath"]]
    checked_paths.extend(path for group in groups for path in (group["repository"], group["service"]))
    checked_text = "\n".join(read_text(path) for path in checked_paths if (ROOT / path).exists())
    for term in data["forbiddenRuntimeTerms"]:
        if term.lower() in checked_text.lower():
            forbidden_matches.append(term)
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
        print("gckf_p0_repository_service_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_repository_service_dry_run=pass "
        f"groups={expected['groupCount']} repositories={repository_count} services={service_count} "
        f"operations={operation_count} index_exports={index_export_count} "
        "typescript_no_emit=pass forbidden_runtime_terms=0 "
        "starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 "
        "writes_business_system=0 writes_accepted_lifecycle=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
