#!/usr/bin/env python3
"""Build the Headroom project-group application router registry."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"
CONTROLLED_PILOT_JSON = ROOT / "docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json"
LOOP_OBSERVATION_SERIES_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json"
AUTHORIZATION_ACTION_QUEUE_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-project-group-application-router-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-project-group-application-router-20260621.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def route_for_entry(entry: dict) -> dict:
    scenario_id = entry["scenario_id"]
    allowed = entry["allow_runtime_application"] is True
    route_mode = "dry_run_apply" if allowed else "blocked"
    if scenario_id == "marker_preserving_log_search_adapter_output":
        route_mode = "adapter_only_dry_run_apply"
    return {
        "scenario_id": scenario_id,
        "content_type": entry["content_type"],
        "route_mode": route_mode,
        "allow_dry_run_application": allowed,
        "allow_production_application": False,
        "allow_kds_write": False,
        "allow_external_api_write": False,
        "requires_marker_gate": True,
        "requires_saving_gate": True,
        "requires_answer_equivalence": True,
        "requires_sensitive_redaction_gate": True,
        "requires_authorized_window": True,
        "saving_rate": entry["saving_rate"],
        "minimum_saving_rate": entry["minimum_saving_rate"],
        "marker_gate": entry["marker_gate"],
        "scenario_gate": entry["scenario_gate"],
        "reason_codes": entry["reason_codes"],
        "raw_text_stored": False,
    }


def build_markdown(result: dict) -> str:
    rows = "\n".join(
        "| {scenario_id} | {content_type} | {route_mode} | {allow_dry_run_application} | {allow_production_application} | {saving_rate} |".format(
            scenario_id=route["scenario_id"],
            content_type=route["content_type"],
            route_mode=route["route_mode"],
            allow_dry_run_application=str(route["allow_dry_run_application"]).lower(),
            allow_production_application=str(route["allow_production_application"]).lower(),
            saving_rate=route["saving_rate"],
        )
        for route in result["routes"]
    )
    return f"""---
doc_id: GPCF-DOC-8AB5E5E3B6
title: Headroom Project Group Application Router Evidence
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-project-group-application-router-20260621.md
source_path: docs/harness/evidence/headroom-project-group-application-router-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom Project Group Application Router Evidence

## Evidence ID

`{result["evidence_id"]}`

## 结论

本轮将 Headroom marker policy、controlled pilot 和 LOOP cost observation series 固化为项目群应用路由注册表。

`application_router_gate | {str(result["gate"]["application_router_gate"]).lower()}`，`dry_run_application_gate | {str(result["gate"]["dry_run_application_gate"]).lower()}`，`production_admission_gate | false`，`measured_production_tokens | false`。

当前路由只允许 dry-run 应用到通过 marker 与 saving 门禁的结构化输出；生产应用、真实 KDS 写入和真实外部 API 写入全部保持 false。

## 路由表

| scenario_id | content_type | route_mode | dry_run | production | saving_rate |
|---|---|---|---|---|---:|
{rows}

## 路由边界

- `project_count`: {result["project_count"]}
- `allowed_route_count`: {result["gate"]["allowed_route_count"]}
- `blocked_route_count`: {result["gate"]["blocked_route_count"]}
- `production_route_count`: 0
- `authorized_window_present`: false
- `authorization_action_queue_gate`: false
"""


def main() -> int:
    policy = load_json(POLICY_JSON)
    controlled_pilot = load_json(CONTROLLED_PILOT_JSON)
    observation_series = load_json(LOOP_OBSERVATION_SERIES_JSON)
    authorization_queue = load_json(AUTHORIZATION_ACTION_QUEUE_JSON)
    require(policy["decision"]["policy_gate"] is True, "marker policy gate must pass")
    require(controlled_pilot["decision"]["controlled_metric_pilot_gate"] is True, "controlled pilot gate must pass")
    require(observation_series["decision"]["loop_cost_observation_series_gate"] is True, "loop observation series gate must pass")
    require(authorization_queue["gate"]["authorization_action_queue_gate"] is False, "production authorization must remain blocked")

    routes = [route_for_entry(entry) for entry in policy["entries"]]
    allowed_routes = [route for route in routes if route["allow_dry_run_application"]]
    blocked_routes = [route for route in routes if not route["allow_dry_run_application"]]
    result = {
        "evidence_id": "HEADROOM-PROJECT-GROUP-APPLICATION-ROUTER-20260621",
        "date": "2026-06-21",
        "status": "project_group_application_router_defined",
        "source_evidence": [
            rel(POLICY_JSON),
            rel(CONTROLLED_PILOT_JSON),
            rel(LOOP_OBSERVATION_SERIES_JSON),
            rel(AUTHORIZATION_ACTION_QUEUE_JSON),
        ],
        "project_count": controlled_pilot["project_count"],
        "projects_covered": controlled_pilot["projects_covered"],
        "routes": routes,
        "gate": {
            "route_count": len(routes),
            "allowed_route_count": len(allowed_routes),
            "blocked_route_count": len(blocked_routes),
            "all_allowed_routes_from_policy": sorted(route["scenario_id"] for route in allowed_routes)
            == sorted(policy["policy"]["allowed_scenarios"]),
            "all_blocked_routes_from_policy": sorted(route["scenario_id"] for route in blocked_routes)
            == sorted(policy["policy"]["rejected_scenarios"]),
            "dry_run_application_gate": True,
            "production_route_count": 0,
            "authorized_window_present": False,
            "authorization_action_queue_gate": False,
            "application_router_gate": True,
            "production_admission_gate": False,
        },
        "decision": {
            "next_allowed_action": "use router only for dry-run metric and marker-preserving adapter outputs",
            "blocked_actions": [
                "production_proxy",
                "real_external_api_write",
                "real_kds_write",
                "raw_markdown_or_direct_conversation_compression",
                "accepted_integrated_or_production_ready_upgrade",
            ],
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
        "headroom_project_group_application_router=pass "
        f"allowed_routes={len(allowed_routes)} blocked_routes={len(blocked_routes)} "
        "dry_run_application_gate=true production_admission_gate=false "
        "measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
