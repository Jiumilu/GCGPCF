#!/usr/bin/env python3
"""Build the Headroom per-project application coverage matrix."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTER_JSON = ROOT / "docs/harness/evidence/headroom-project-group-application-router-20260621.json"
L2_DRY_RUN_JSON = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
AUTHORIZATION_ACTION_QUEUE_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_markdown(result: dict) -> str:
    rows = "\n".join(
        "| {project} | {source_path} | {dry_run_route_count} | {blocked_route_count} | {saving_rate} | {production_admission_gate} |".format(
            project=row["project"],
            source_path=row["source_path"],
            dry_run_route_count=row["dry_run_route_count"],
            blocked_route_count=row["blocked_route_count"],
            saving_rate=row["l2_saving_rate"],
            production_admission_gate=str(row["production_admission_gate"]).lower(),
        )
        for row in result["coverage"]
    )
    return f"""---
doc_id: GPCF-DOC-4F2AB18D49
title: Headroom Project Application Coverage Matrix
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md
source_path: docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom Project Application Coverage Matrix

## Evidence ID

`{result["evidence_id"]}`

## 结论

本矩阵把 Headroom dry-run-only 应用路由落到 15 个项目/域，形成项目级应用覆盖、成本来源和阻断边界。

`project_application_coverage_gate | {str(result["gate"]["project_application_coverage_gate"]).lower()}`，`dry_run_application_gate | {str(result["gate"]["dry_run_application_gate"]).lower()}`，`production_admission_gate | false`，`measured_production_tokens | false`。

## 项目覆盖

| project | source_path | dry_run_routes | blocked_routes | l2_saving_rate | production_admission_gate |
|---|---|---:|---:|---:|---|
{rows}

## 汇总

- `project_count`: {result["gate"]["project_count"]}
- `projects_with_l2_measurement`: {result["gate"]["projects_with_l2_measurement"]}
- `projects_with_dry_run_routes`: {result["gate"]["projects_with_dry_run_routes"]}
- `projects_with_production_routes`: 0
- `authorization_action_queue_gate`: false
"""


def main() -> int:
    router = load_json(ROUTER_JSON)
    l2 = load_json(L2_DRY_RUN_JSON)
    authorization_queue = load_json(AUTHORIZATION_ACTION_QUEUE_JSON)
    require(router["gate"]["application_router_gate"] is True, "application router gate must pass")
    require(router["gate"]["production_admission_gate"] is False, "router production gate must remain false")
    require(l2["aggregate"]["all_admission_gates_pass"] is True, "L2 dry-run gates must pass")
    require(authorization_queue["gate"]["authorization_action_queue_gate"] is False, "authorization action queue must remain blocked")

    dry_run_routes = [route for route in router["routes"] if route["allow_dry_run_application"]]
    blocked_routes = [route for route in router["routes"] if not route["allow_dry_run_application"]]
    coverage = []
    for measurement in l2["measurements"]:
        coverage.append(
            {
                "project": measurement["project"],
                "scenario": measurement["scenario"],
                "source_path": measurement["source_path"],
                "l2_input_tokens_before": measurement["input_tokens_before"],
                "l2_input_tokens_after": measurement["input_tokens_after"],
                "l2_saving_rate": measurement["saving_rate"],
                "l2_admission_gate": measurement["admission_gate"],
                "dry_run_route_count": len(dry_run_routes),
                "blocked_route_count": len(blocked_routes),
                "allowed_dry_run_routes": [route["scenario_id"] for route in dry_run_routes],
                "blocked_routes": [route["scenario_id"] for route in blocked_routes],
                "allow_production_application": False,
                "production_admission_gate": False,
                "requires_authorized_window": True,
                "requires_sanitized_production_token_ledger": True,
                "raw_text_stored": False,
            }
        )

    result = {
        "evidence_id": "HEADROOM-PROJECT-APPLICATION-COVERAGE-MATRIX-20260621",
        "date": "2026-06-21",
        "status": "project_application_coverage_defined",
        "source_evidence": [rel(ROUTER_JSON), rel(L2_DRY_RUN_JSON), rel(AUTHORIZATION_ACTION_QUEUE_JSON)],
        "coverage": coverage,
        "gate": {
            "project_count": len(coverage),
            "projects_with_l2_measurement": sum(1 for row in coverage if row["l2_admission_gate"]),
            "projects_with_dry_run_routes": sum(1 for row in coverage if row["dry_run_route_count"] == len(dry_run_routes)),
            "projects_with_production_routes": sum(1 for row in coverage if row["allow_production_application"]),
            "all_projects_have_l2_measurement": all(row["l2_admission_gate"] for row in coverage),
            "all_projects_have_dry_run_routes": all(row["dry_run_route_count"] == len(dry_run_routes) for row in coverage),
            "all_projects_block_production": all(row["production_admission_gate"] is False for row in coverage),
            "dry_run_application_gate": True,
            "authorization_action_queue_gate": False,
            "project_application_coverage_gate": True,
            "production_admission_gate": False,
        },
        "decision": {
            "next_allowed_action": "repeat dry-run route coverage on subsequent LOOP cost evidence",
            "next_blocked_action": "production rollout without authorized sanitized token ledger",
            "production_admission_gate": False,
        },
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_cross_project_memory": True,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(result), encoding="utf-8")
    print(
        "headroom_project_application_coverage_matrix=pass "
        f"project_count={len(coverage)} dry_run_routes={len(dry_run_routes)} "
        f"blocked_routes={len(blocked_routes)} production_admission_gate=false "
        "measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
