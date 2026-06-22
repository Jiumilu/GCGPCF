#!/usr/bin/env python3
"""Validate P0 shared types and API contract alignment.

This is a static local validator. It checks files and fixture declarations only.
It does not start an API server, call external APIs, mutate KDS, write business
systems, or promote lifecycle state.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-shared-types-api-contract-alignment-v0.1.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    api_matrix = json.loads((ROOT / data["apiMatrixRef"]).read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    groups = data["groups"]
    if len(groups) != expected["groupCount"]:
        failures.append(f"groupCount expected={expected['groupCount']} actual={len(groups)}")

    if len(api_matrix["routeGroups"]) != expected["apiMatrixGroupCount"]:
        failures.append(
            f"apiMatrixGroupCount expected={expected['apiMatrixGroupCount']} actual={len(api_matrix['routeGroups'])}"
        )

    endpoint_count = sum(group["expectedEndpointCount"] for group in groups)
    api_endpoint_count = sum(group["endpointCount"] for group in api_matrix["routeGroups"])
    if endpoint_count != expected["endpointCount"]:
        failures.append(f"endpointCount expected={expected['endpointCount']} actual={endpoint_count}")
    if api_endpoint_count != expected["apiMatrixEndpointCount"]:
        failures.append(
            f"apiMatrixEndpointCount expected={expected['apiMatrixEndpointCount']} actual={api_endpoint_count}"
        )

    matrix_groups = {group["group"]: group["endpointCount"] for group in api_matrix["routeGroups"]}
    for group in groups:
        name = group["group"]
        if matrix_groups.get(name) != group["expectedEndpointCount"]:
            failures.append(
                f"{name} endpoint mismatch expected={group['expectedEndpointCount']} actual={matrix_groups.get(name)}"
            )
        for key in ("requiredSharedTypes", "requiredApiContracts", "requiredRoutes", "requiredValidators"):
            for rel_path in group[key]:
                if not (ROOT / rel_path).exists():
                    failures.append(f"missing {key}: {rel_path}")

    validator_count = len({path for group in groups for path in group["requiredValidators"]})
    contract_count = len({path for group in groups for path in group["requiredApiContracts"]})
    route_count = len({path for group in groups for path in group["requiredRoutes"]})
    if validator_count != expected["validatorCount"]:
        failures.append(f"validatorCount expected={expected['validatorCount']} actual={validator_count}")
    if contract_count != expected["contractFileCount"]:
        failures.append(f"contractFileCount expected={expected['contractFileCount']} actual={contract_count}")
    if route_count != expected["routeFileCount"]:
        failures.append(f"routeFileCount expected={expected['routeFileCount']} actual={route_count}")

    forbidden_total = sum(api_matrix["forbiddenMutations"].values())
    if forbidden_total != expected["forbiddenMutationTotal"]:
        failures.append(
            f"forbiddenMutationTotal expected={expected['forbiddenMutationTotal']} actual={forbidden_total}"
        )

    for key in ("startsServer", "callsExternalApi", "writesKds", "writesBusinessSystem"):
        if expected[key] is not False:
            failures.append(f"{key} must be false")
    if expected["noWrite"] is not True:
        failures.append("noWrite must be true")

    if failures:
        print("gckf_p0_shared_types_api_contract_alignment=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_shared_types_api_contract_alignment=pass "
        f"groups={expected['groupCount']} endpoints={expected['endpointCount']} "
        f"validators={validator_count} contracts={contract_count} routes={route_count} "
        "forbidden_mutations=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
