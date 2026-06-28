#!/usr/bin/env python3
"""Read-only preflight for the GFIS dev-completion controlled sample."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"

SCHEMA = GFIS_ROOT / (
    "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/"
    "customer-requirement-or-platform-order/"
    "customer-requirement-platform-order.valid-source-record-index.schema.json"
)
TEMPLATE = GFIS_ROOT / (
    "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/"
    "customer-requirement-or-platform-order/"
    "customer-requirement-platform-order.valid-source-record-index.template.json"
)
FIXTURE = GFIS_ROOT / "docs/harness/sop-e2e/synthetic-fixtures/synthetic-gehu-sop-e2e-master.json"
CANDIDATE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-min-001-candidate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL build_gfis_dev_completion_controlled_sample: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected JSON object: {path}")
    return data


def main() -> int:
    schema = load_json(SCHEMA)
    template = load_json(TEMPLATE)
    fixture = load_json(FIXTURE)
    candidate = load_json(CANDIDATE)

    required_fields = schema.get("required")
    require(isinstance(required_fields, list) and required_fields, "schema.required missing")
    require(template.get("template_only") is True, "template_only must be true")
    require(template.get("not_a_source_record") is True, "template must stay non-source-record")
    require(template.get("object_family") == "CustomerRequirementOrPlatformOrder", "template object_family mismatch")
    require(schema.get("object_family", {}).get("const") == "CustomerRequirementOrPlatformOrder", "schema object_family mismatch")
    require(schema.get("preflight_policy", {}).get("copy_to_real_target_allowed_by_this_schema") is False, "schema must not allow real copy")
    require(fixture.get("classification", {}).get("synthetic") is True, "fixture must be synthetic")
    require(fixture.get("classification", {}).get("not_source_of_record") is True, "fixture must not be source-of-record")
    require(candidate.get("classification", {}).get("candidate_lane") is True, "candidate lane must be true")
    require(candidate.get("status_boundary", {}).get("status_promotion_allowed") is False, "status promotion must stay false")

    print(
        "gfis_dev_completion_controlled_sample=pass "
        "object_family=CustomerRequirementOrPlatformOrder "
        f"required_fields={len(required_fields)} "
        "template_only=true not_a_source_record=true "
        "fixture_synthetic=true fixture_not_source_of_record=true "
        "candidate_lane=true status_promotion_allowed=false "
        f"schema_path={SCHEMA.relative_to(GFIS_ROOT)} "
        f"template_path={TEMPLATE.relative_to(GFIS_ROOT)} "
        f"fixture_path={FIXTURE.relative_to(GFIS_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
