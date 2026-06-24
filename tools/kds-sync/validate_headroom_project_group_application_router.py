#!/usr/bin/env python3
"""Validate the Headroom project-group application router registry."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-project-group-application-router-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-project-group-application-router-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_project_group_application_router.py"
POLICY_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"


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
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")
    require(
        "last_reviewed: 2026-06-21" in metadata
        or "last_reviewed: 2026-06-22" in metadata
        or "last_reviewed: 2026-06-23" in metadata,
        f"{path.relative_to(ROOT)} missing controlled marker: last_reviewed",
    )


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    policy = load_json(POLICY_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("route_for_entry" in runner, "runner must define route mapping")
    require(evidence.get("evidence_id") == "HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-20260621", "invalid evidence id")
    require(evidence.get("status") == "project_group_application_router_defined", "invalid status")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("measured_production_tokens") is False, "must not claim production token measurement")
    routes = evidence.get("routes", [])
    require(len(routes) == 6, "route count mismatch")
    allowed = [route for route in routes if route.get("allow_dry_run_application") is True]
    blocked = [route for route in routes if route.get("allow_dry_run_application") is False]
    require(len(allowed) == 3, "allowed route count mismatch")
    require(len(blocked) == 3, "blocked route count mismatch")
    require(
        sorted(route["scenario_id"] for route in allowed) == sorted(policy["policy"]["allowed_scenarios"]),
        "allowed route policy mismatch",
    )
    require(
        sorted(route["scenario_id"] for route in blocked) == sorted(policy["policy"]["rejected_scenarios"]),
        "blocked route policy mismatch",
    )
    for route in routes:
        require(route.get("allow_production_application") is False, "production route must remain false")
        require(route.get("allow_kds_write") is False, "KDS write route must remain false")
        require(route.get("allow_external_api_write") is False, "external write route must remain false")
        require(route.get("requires_marker_gate") is True, "marker gate must be required")
        require(route.get("requires_saving_gate") is True, "saving gate must be required")
        require(route.get("requires_answer_equivalence") is True, "answer equivalence must be required")
        require(route.get("requires_sensitive_redaction_gate") is True, "redaction gate must be required")
        require(route.get("requires_authorized_window") is True, "authorized window must be required")
        require(route.get("raw_text_stored") is False, "raw text must not be stored")
    gate = evidence.get("gate", {})
    require(gate.get("route_count") == 6, "gate route count mismatch")
    require(gate.get("allowed_route_count") == 3, "gate allowed count mismatch")
    require(gate.get("blocked_route_count") == 3, "gate blocked count mismatch")
    require(gate.get("all_allowed_routes_from_policy") is True, "allowed policy gate failed")
    require(gate.get("all_blocked_routes_from_policy") is True, "blocked policy gate failed")
    require(gate.get("dry_run_application_gate") is True, "dry-run gate must pass")
    require(gate.get("production_route_count") == 0, "production routes must be zero")
    require(gate.get("authorized_window_present") is False, "authorized window must remain false")
    require(gate.get("authorization_action_queue_gate") is False, "authorization action queue must remain blocked")
    require(gate.get("application_router_gate") is True, "application router gate must pass")
    require(gate.get("production_admission_gate") is False, "production admission must remain false")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-20260621",
        "application_router_gate | true",
        "dry_run_application_gate | true",
        "production_admission_gate | false",
        "measured_production_tokens | false",
        "authorized_window_present`: false",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_project_group_application_router.py" in loop_round, "loop round missing runner")
    require("validate_headroom_project_group_application_router.py" in loop_round, "loop round missing validator")
    print(
        "headroom_project_group_application_router=pass "
        "allowed_routes=3 blocked_routes=3 "
        "dry_run_application_gate=true production_admission_gate=false "
        "measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
