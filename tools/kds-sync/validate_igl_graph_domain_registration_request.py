#!/usr/bin/env python3
"""Validate the Industrial Green Chain graph business-domain registration request package（支持 pending/accepted 两态）。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/industrial-green-chain-graph-domain-registration-request-20261011.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/industrial-green-chain-graph-domain-registration-request-20261011.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-IGL-GRAPH-DOMAIN-REGISTRATION-REQUEST-001.md"


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

    require(evidence.get("evidence_id") == "IGL-GRAPH-DOMAIN-REGISTRATION-REQUEST-20261011", "invalid evidence id")
    require(evidence.get("status") in ("request_submitted_pending_governance_review", "request_accepted"),
            "invalid status")
    require(evidence.get("scope") == "business_domain_registration_request_only", "invalid scope")
    require(evidence.get("requested_decision") == "admit_readonly_business_domain_slice_candidate",
            "requested decision mismatch")
    decision = evidence.get("current_decision")
    require(decision in ("pending_governance_review", "accepted"), f"unknown decision state: {decision}")

    pre = evidence.get("admission_preconditions", {})
    for key in [
        "mapped_to_six_categories",
        "binds_project_group_scope",
        "no_kds_waes_loop_bypass",
        "registry_body_unmodified",
        "candidate_boundary_retained",
    ]:
        require(pre.get(key) is True, f"precondition must be true: {key}")

    mapping = evidence.get("six_category_mapping", {})
    for category in ["object", "relationship", "event", "evidence", "state", "interface"]:
        require(bool(mapping.get(category)), f"six-category mapping missing: {category}")

    attached = evidence.get("attached_requests", {})
    require("rejected" in set(attached.get("state_request", [])), "state_request:rejected missing")
    term_requests = set(attached.get("term_requests", []))
    for term in ["Project", "Person", "Equipment", "BusinessEvent", "Risk", "Decision", "DependsOn", "Blocks"]:
        require(term in term_requests, f"term request missing: {term}")

    gates = evidence.get("gates", {})
    require(gates.get("request_package_generated") is True, "request package gate must be true")
    require(gates.get("submitted") is True, "submitted gate must be true")
    if decision == "accepted":
        record = evidence.get("decision_record", {})
        require(record.get("decision") == "accepted" and record.get("date") and record.get("authority"),
                "accepted 状态需 decision_record（decision/date/authority）")
        require(gates.get("governance_reviewed") is True, "accepted 状态 governance_reviewed 必须为 true")
        require(gates.get("accepted") is True, "accepted 状态 accepted 门必须为 true")
        for key in ["registry_entry_added", "waes_authorized", "integrated", "production_ready"]:
            require(gates.get(key) is False, f"gate must be false: {key}")
    else:
        for key in ["registry_entry_added", "governance_reviewed", "waes_authorized", "accepted",
                    "integrated", "production_ready"]:
            require(gates.get(key) is False, f"gate must be false: {key}")

    phrases = [
        "IGL-GRAPH-DOMAIN-REGISTRATION-REQUEST-20261011",
        "request_package_generated | true",
        "submitted | true",
        "waes_authorized | false",
        "production_ready | false",
        "state-request:rejected",
    ]
    if decision == "accepted":
        phrases += ["governance_reviewed | true", "accepted | true", "受理记录"]
    else:
        phrases += ["registry_entry_added | false", "governance_reviewed | false",
                    "accepted | false", "pending_governance_review"]
    for phrase in phrases:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_igl_graph_domain_registration_request.py" in loop_round, "loop round missing validator")
    print(
        "igl_graph_domain_registration_request=pass "
        "requested_decision=admit_readonly_business_domain_slice_candidate "
        f"current_decision={decision} submitted=true "
        f"governance_reviewed={'true' if decision == 'accepted' else 'false'} "
        f"accepted={'true' if decision == 'accepted' else 'false'} integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
