#!/usr/bin/env python3
"""Validate Headroom per-project application coverage matrix."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-PROJECT-APPLICATION-COVERAGE-MATRIX-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_project_application_coverage_matrix.py"
ROUTER_JSON = ROOT / "docs/harness/evidence/headroom-project-group-application-router-20260621.json"


PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


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
    router = load_json(ROUTER_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("dry_run_routes" in runner, "runner must derive dry-run routes")
    require(evidence.get("evidence_id") == "HEADROOM-PROJECT-APPLICATION-COVERAGE-MATRIX-20260621", "invalid evidence id")
    require(evidence.get("status") == "project_application_coverage_defined", "invalid status")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    coverage = evidence.get("coverage", [])
    require(len(coverage) == 15, "coverage project count mismatch")
    require([row["project"] for row in coverage] == PROJECTS, "coverage project order mismatch")
    allowed_routes = set(router["gate"]["allowed_route_count"] for _ in [None])
    require(next(iter(allowed_routes)) == 3, "router allowed route count mismatch")
    for row in coverage:
        require(row["l2_admission_gate"] is True, f"L2 gate failed for {row['project']}")
        require(row["dry_run_route_count"] == 3, f"dry-run route count mismatch for {row['project']}")
        require(row["blocked_route_count"] == 3, f"blocked route count mismatch for {row['project']}")
        require(len(row["allowed_dry_run_routes"]) == 3, f"allowed route list mismatch for {row['project']}")
        require(len(row["blocked_routes"]) == 3, f"blocked route list mismatch for {row['project']}")
        require(row["allow_production_application"] is False, f"production application must remain false for {row['project']}")
        require(row["production_admission_gate"] is False, f"production gate must remain false for {row['project']}")
        require(row["requires_authorized_window"] is True, f"authorized window must be required for {row['project']}")
        require(row["requires_sanitized_production_token_ledger"] is True, f"sanitized ledger must be required for {row['project']}")
        require(row["raw_text_stored"] is False, f"raw text must not be stored for {row['project']}")
    gate = evidence.get("gate", {})
    require(gate.get("project_count") == 15, "gate project count mismatch")
    require(gate.get("projects_with_l2_measurement") == 15, "L2 coverage count mismatch")
    require(gate.get("projects_with_dry_run_routes") == 15, "dry-run coverage count mismatch")
    require(gate.get("projects_with_production_routes") == 0, "production route count must be zero")
    require(gate.get("all_projects_have_l2_measurement") is True, "all projects must have L2 measurement")
    require(gate.get("all_projects_have_dry_run_routes") is True, "all projects must have dry-run routes")
    require(gate.get("all_projects_block_production") is True, "all projects must block production")
    require(gate.get("dry_run_application_gate") is True, "dry-run application gate must pass")
    require(gate.get("authorization_action_queue_gate") is False, "authorization action queue must remain blocked")
    require(gate.get("project_application_coverage_gate") is True, "project application coverage gate must pass")
    require(gate.get("production_admission_gate") is False, "production admission must remain false")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-PROJECT-APPLICATION-COVERAGE-MATRIX-20260621",
        "project_application_coverage_gate | true",
        "dry_run_application_gate | true",
        "production_admission_gate | false",
        "measured_production_tokens | false",
        "project_count`: 15",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_project_application_coverage_matrix.py" in loop_round, "loop round missing runner")
    require("validate_headroom_project_application_coverage_matrix.py" in loop_round, "loop round missing validator")
    print(
        "headroom_project_application_coverage_matrix=pass "
        "project_count=15 dry_run_routes=3 blocked_routes=3 "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
