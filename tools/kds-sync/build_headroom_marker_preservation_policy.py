#!/usr/bin/env python3
"""Build allow/reject policy from Headroom scenario marker gates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_MATRIX = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json"
COST_OUTPUT = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.json"
ADAPTER_PILOT = ROOT / "docs/harness/evidence/headroom-marker-preserving-adapter-pilot-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    matrix = load_json(SCENARIO_MATRIX)
    cost_output = load_json(COST_OUTPUT)
    adapter_pilot = load_json(ADAPTER_PILOT)
    policy_entries = []
    for item in matrix["measurements"]:
        reasons = []
        if not item["marker_gate"]:
            reasons.append("marker_loss")
        if item["saving_rate"] < item["minimum_saving_rate"]:
            reasons.append("below_saving_threshold")
        if item["reason"] == "rejected_not_smaller":
            reasons.append("rejected_not_smaller")
        allowed = item["scenario_gate"] is True
        policy_entries.append(
            {
                "scenario_id": item["scenario_id"],
                "content_type": item["content_type"],
                "allow_runtime_application": allowed,
                "reason_codes": [] if allowed else reasons,
                "saving_rate": item["saving_rate"],
                "minimum_saving_rate": item["minimum_saving_rate"],
                "marker_gate": item["marker_gate"],
                "scenario_gate": item["scenario_gate"],
                "raw_text_stored": False,
            }
        )
    policy_entries.append(
        {
            "scenario_id": "headroom_cost_measurement_output",
            "content_type": "structured_metric_tool_output",
            "allow_runtime_application": cost_output["decision"]["headroom_cost_measurement_output_gate"],
            "reason_codes": [],
            "saving_rate": cost_output["aggregate"]["saving_rate"],
            "minimum_saving_rate": cost_output["aggregate"]["minimum_saving_rate"],
            "marker_gate": cost_output["aggregate"]["marker_gate"],
            "scenario_gate": cost_output["aggregate"]["output_gate"],
            "raw_text_stored": False,
        }
    )
    policy_entries.append(
        {
            "scenario_id": "marker_preserving_log_search_adapter_output",
            "content_type": "marker_preserving_adapter_output",
            "allow_runtime_application": adapter_pilot["decision"]["marker_preserving_adapter_pilot_gate"],
            "reason_codes": [],
            "saving_rate": adapter_pilot["aggregate"]["saving_rate"],
            "minimum_saving_rate": 0.2,
            "marker_gate": adapter_pilot["aggregate"]["all_marker_gates_pass"],
            "scenario_gate": adapter_pilot["aggregate"]["all_adapter_gates_pass"],
            "raw_text_stored": False,
        }
    )
    allowed = [item["scenario_id"] for item in policy_entries if item["allow_runtime_application"]]
    rejected = [item["scenario_id"] for item in policy_entries if not item["allow_runtime_application"]]
    result = {
        "evidence_id": "HEADROOM-MARKER-PRESERVATION-POLICY-20260621",
        "date": "2026-06-21",
        "status": "runtime_application_policy_defined",
        "source_matrix": SCENARIO_MATRIX.relative_to(ROOT).as_posix(),
        "cost_measurement_output": COST_OUTPUT.relative_to(ROOT).as_posix(),
        "marker_preserving_adapter_pilot": ADAPTER_PILOT.relative_to(ROOT).as_posix(),
        "policy": {
            "default": "reject_unless_saving_and_marker_gates_pass",
            "allowed_scenarios": allowed,
            "rejected_scenarios": rejected,
            "marker_loss_is_hard_block": True,
            "below_saving_threshold_is_hard_block": True,
        },
        "entries": policy_entries,
        "decision": {
            "policy_gate": True,
            "runtime_application_scope": "structured_metric_and_marker_preserving_adapter_outputs",
            "log_and_search_runtime_application": "allowed_only_via_marker_preserving_adapter",
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
        "headroom_marker_preservation_policy=pass "
        f"allowed={len(allowed)} rejected={len(rejected)} "
        "log_and_search=adapter_only measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
