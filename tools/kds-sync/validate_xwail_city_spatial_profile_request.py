#!/usr/bin/env python3
"""Validate the XWAIL City/Spatial Profile initiation request package（支持 pending/accepted 两态）。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.json"
EVIDENCE_MD = ROOT / "docs/harness/XWAIL/evidence/xwail-city-spatial-profile-request-20261011.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-XWAIL-CITY-SPATIAL-PROFILE-REQUEST-001.md"
KEEP_FALSE_AFTER_ACCEPT = ["waes_authorized", "published", "integrated", "production_ready"]


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
    require(evidence.get("status") in ("request_submitted_pending_governance_review", "request_accepted"),
            "invalid status")
    require(evidence.get("scope") == "xwail_city_spatial_profile_initiation_request_only", "invalid scope")
    require(evidence.get("requested_decision") == "initiate_xwail_city_spatial_profile", "requested decision mismatch")
    decision = evidence.get("current_decision")
    require(decision in ("pending_governance_review", "accepted"), f"unknown decision state: {decision}")

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
    if decision == "accepted":
        record = evidence.get("decision_record", {})
        require(record.get("decision") == "accepted" and record.get("date") and record.get("authority"),
                "accepted 状态需 decision_record（decision/date/authority）")
        require(gates.get("governance_reviewed") is True, "accepted 状态 governance_reviewed 必须为 true")
        require(gates.get("accepted") is True, "accepted 状态 accepted 门必须为 true")
        for key in KEEP_FALSE_AFTER_ACCEPT:
            require(gates.get(key) is False, f"gate must be false: {key}")
    else:
        for key in ["governance_reviewed"] + KEEP_FALSE_AFTER_ACCEPT + ["accepted"]:
            require(gates.get(key) is False, f"gate must be false: {key}")

    phrases = [
        "XWAIL-CITY-SPATIAL-PROFILE-REQUEST-20261011",
        "request_package_generated | true",
        "submitted | true",
        "waes_authorized | false",
        "production_ready | false",
    ]
    if decision == "accepted":
        phrases += ["governance_reviewed | true", "accepted | true", "受理记录"]
    else:
        phrases += ["governance_reviewed | false", "accepted | false", "pending_governance_review"]
    for phrase in phrases:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_xwail_city_spatial_profile_request.py" in loop_round, "loop round missing validator")
    print(
        "xwail_city_spatial_profile_request=pass "
        "requested_decision=initiate_xwail_city_spatial_profile "
        f"current_decision={decision} submitted=true "
        f"governance_reviewed={'true' if decision == 'accepted' else 'false'} "
        f"accepted={'true' if decision == 'accepted' else 'false'} integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
