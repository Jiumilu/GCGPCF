#!/usr/bin/env python3
"""Validate the XWAIL City/Spatial Profile initiation request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.json"
EVIDENCE_MD = ROOT / "docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-XWAIL-CITY-SPATIAL-PROFILE-REQUEST-001.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-10-11",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "XWAIL-CITY-SPATIAL-PROFILE-REQUEST-20261011", "invalid evidence id")
    require(evidence.get("status") == "request_submitted_pending_governance_review", "invalid status")
    require(evidence.get("scope") == "xwail_city_spatial_profile_initiation_request_only", "invalid scope")
    require(evidence.get("requested_decision") == "initiate_xwail_city_spatial_profile", "requested decision mismatch")
    require(evidence.get("current_decision") == "pending_governance_review", "current decision must stay pending")

    pre = evidence.get("admission_preconditions", {})
    for key in [
        "was_ontology_registry_pass",
        "xwail_mapping_candidate_exists",
        "no_xwail_repo_modification",
        "no_waes_bypass",
        "candidate_boundary_retained",
    ]:
        require(pre.get(key) is True, f"precondition must be true: {key}")

    boundary = evidence.get("requested_boundary", {})
    forbidden = set(boundary.get("forbidden", []))
    for item in [
        "xwail_repo_direct_modification_outside_governance",
        "waes_publication_claim",
        "production_ready_claim",
        "customer_acceptance_claim",
    ]:
        require(item in forbidden, f"forbidden item missing: {item}")

    gates = evidence.get("gates", {})
    require(gates.get("request_package_generated") is True, "request package gate must be true")
    require(gates.get("submitted") is True, "submitted gate must be true")
    for key in ["governance_reviewed", "waes_authorized", "published", "accepted", "integrated", "production_ready"]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "XWAIL-CITY-SPATIAL-PROFILE-REQUEST-20261011",
        "request_package_generated | true",
        "submitted | true",
        "governance_reviewed | false",
        "waes_authorized | false",
        "accepted | false",
        "production_ready | false",
        "pending_governance_review",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_xwail_city_spatial_profile_request.py" in loop_round, "loop round missing validator")
    print(
        "xwail_city_spatial_profile_request=pass "
        "requested_decision=initiate_xwail_city_spatial_profile current_decision=pending_governance_review "
        "submitted=true governance_reviewed=false waes_authorized=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
