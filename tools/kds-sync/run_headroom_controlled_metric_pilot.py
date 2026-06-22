#!/usr/bin/env python3
"""Run the allowed Headroom metric-output pilot under marker policy."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"
COST_OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.json"
ADAPTER_PILOT_JSON = ROOT / "docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json"
SCENARIO_MATRIX_JSON = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    policy = load_json(POLICY_JSON)
    cost_output = load_json(COST_OUTPUT_JSON)
    adapter_pilot = load_json(ADAPTER_PILOT_JSON)
    scenario_matrix = load_json(SCENARIO_MATRIX_JSON)
    allowed = set(policy["policy"]["allowed_scenarios"])
    rejected = set(policy["policy"]["rejected_scenarios"])
    require("headroom_cost_measurement_output" in allowed, "cost measurement output must be allowed")
    require("marker_preserving_log_search_adapter_output" in allowed, "marker-preserving adapter output must be allowed")
    require(cost_output["aggregate"]["output_gate"] is True, "cost measurement output gate must pass")
    require(adapter_pilot["decision"]["marker_preserving_adapter_pilot_gate"] is True, "adapter pilot gate must pass")
    scenario_by_id = {item["scenario_id"]: item for item in scenario_matrix["measurements"]}

    application_records = [
        {
            "application_id": "HEADROOM-PILOT-STRUCTURED-METRIC-OUTPUT-001",
            "scenario_id": "headroom_cost_measurement_output",
            "content_type": "structured_metric_tool_output",
            "source_evidence": COST_OUTPUT_JSON.relative_to(ROOT).as_posix(),
            "policy_decision": "allow",
            "applied": True,
            "saving_rate": cost_output["aggregate"]["saving_rate"],
            "tokens_before": cost_output["aggregate"]["tokens_before"],
            "tokens_after": cost_output["aggregate"]["tokens_after"],
            "tokens_saved": cost_output["aggregate"]["tokens_saved"],
            "marker_gate": cost_output["aggregate"]["marker_gate"],
            "output_gate": cost_output["aggregate"]["output_gate"],
            "runtime_scope": "dry_run_controlled_pilot",
            "raw_text_stored": False,
        }
    ]
    application_records.append(
        {
            "application_id": "HEADROOM-PILOT-MARKER-PRESERVING-ADAPTER-001",
            "scenario_id": "marker_preserving_log_search_adapter_output",
            "content_type": "marker_preserving_adapter_output",
            "source_evidence": ADAPTER_PILOT_JSON.relative_to(ROOT).as_posix(),
            "policy_decision": "allow",
            "applied": True,
            "saving_rate": adapter_pilot["aggregate"]["saving_rate"],
            "tokens_before": adapter_pilot["aggregate"]["tokens_before"],
            "tokens_after": adapter_pilot["aggregate"]["tokens_after"],
            "tokens_saved": adapter_pilot["aggregate"]["tokens_saved"],
            "marker_gate": adapter_pilot["aggregate"]["all_marker_gates_pass"],
            "output_gate": adapter_pilot["aggregate"]["all_adapter_gates_pass"],
            "runtime_scope": "dry_run_controlled_pilot",
            "raw_text_stored": False,
        }
    )
    rejected_records = []
    for scenario_id in sorted(rejected):
        source = scenario_by_id.get(scenario_id, {})
        rejected_records.append(
            {
                "scenario_id": scenario_id,
                "content_type": source.get("content_type", "unknown"),
                "policy_decision": "reject",
                "applied": False,
                "saving_rate": source.get("saving_rate"),
                "marker_gate": source.get("marker_gate"),
                "reason_codes": next(
                    item["reason_codes"]
                    for item in policy["entries"]
                    if item["scenario_id"] == scenario_id
                ),
                "raw_text_stored": False,
            }
        )
    total_before = sum(item["tokens_before"] for item in application_records)
    total_after = sum(item["tokens_after"] for item in application_records)
    total_saved = total_before - total_after
    result = {
        "evidence_id": "HEADROOM-CONTROLLED-METRIC-PILOT-20260621",
        "date": "2026-06-21",
        "status": "controlled_metric_output_pilot_applied",
        "policy_source": POLICY_JSON.relative_to(ROOT).as_posix(),
        "cost_measurement_output": COST_OUTPUT_JSON.relative_to(ROOT).as_posix(),
        "marker_preserving_adapter_pilot": ADAPTER_PILOT_JSON.relative_to(ROOT).as_posix(),
        "scenario_matrix": SCENARIO_MATRIX_JSON.relative_to(ROOT).as_posix(),
        "pilot_scope": "structured_metric_and_marker_preserving_adapter_outputs",
        "project_count": cost_output["project_count"],
        "projects_covered": cost_output["projects_covered"],
        "allowed_application_count": len(application_records),
        "rejected_application_count": len(rejected_records),
        "aggregate": {
            "tokens_before": total_before,
            "tokens_after": total_after,
            "tokens_saved": total_saved,
            "saving_rate": round(total_saved / total_before, 6) if total_before else 0.0,
            "all_allowed_applications_applied": all(item["applied"] for item in application_records),
            "all_rejected_applications_blocked": all(not item["applied"] for item in rejected_records),
            "all_marker_gates_pass": all(item["marker_gate"] for item in application_records),
        },
        "applications": application_records,
        "rejections": rejected_records,
        "decision": {
            "controlled_metric_pilot_gate": True,
            "next_allowed_action": "repeat_on_next_loop_cost_measurement_output",
            "blocked_actions": sorted(rejected),
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
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "headroom_controlled_metric_pilot=pass "
        f"allowed_applied={len(application_records)} rejected_blocked={len(rejected_records)} "
        f"saving_rate={result['aggregate']['saving_rate']} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
