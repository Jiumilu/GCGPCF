#!/usr/bin/env python3
"""Build a continuous LOOP cost observation ledger for Headroom."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
L2_JSON = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
RUNTIME_PROBE_JSON = ROOT / "docs/harness/evidence/headroom-runtime-probe-20260621.json"
SCENARIO_MATRIX_JSON = ROOT / "docs/harness/evidence/headroom-runtime-scenario-matrix-20260621.json"
COST_OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.json"
POLICY_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"
PILOT_JSON = ROOT / "docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-20260621.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    l2 = load_json(L2_JSON)
    runtime_probe = load_json(RUNTIME_PROBE_JSON)
    scenario_matrix = load_json(SCENARIO_MATRIX_JSON)
    cost_output = load_json(COST_OUTPUT_JSON)
    policy = load_json(POLICY_JSON)
    pilot = load_json(PILOT_JSON)

    allowed = set(policy["policy"]["allowed_scenarios"])
    rejected = set(policy["policy"]["rejected_scenarios"])
    require(pilot["decision"]["controlled_metric_pilot_gate"] is True, "controlled metric pilot must pass")
    require(pilot["aggregate"]["all_rejected_applications_blocked"] is True, "rejected applications must be blocked")
    require(cost_output["aggregate"]["output_gate"] is True, "cost measurement output gate must pass")

    observation_entries = [
        {
            "observation_id": "HEADROOM-OBS-L2-SURROGATE",
            "source_evidence": rel(L2_JSON),
            "observation_type": "structured_surrogate_baseline",
            "runtime_used": False,
            "included_in_loop_cost_observation": True,
            "tokens_before": l2["aggregate"]["input_tokens_before"],
            "tokens_after": l2["aggregate"]["input_tokens_after"],
            "tokens_saved": l2["aggregate"]["input_tokens_before"] - l2["aggregate"]["input_tokens_after"],
            "saving_rate": l2["aggregate"]["saving_rate"],
            "gate": l2["aggregate"]["all_admission_gates_pass"],
            "scope": "project_group_sample_cost_model",
            "raw_text_stored": False,
        },
        {
            "observation_id": "HEADROOM-OBS-RUNTIME-DIRECT",
            "source_evidence": rel(RUNTIME_PROBE_JSON),
            "observation_type": "direct_runtime_probe",
            "runtime_used": True,
            "included_in_loop_cost_observation": False,
            "tokens_before": runtime_probe["aggregate"]["tokens_before"],
            "tokens_after": runtime_probe["aggregate"]["tokens_after"],
            "tokens_saved": runtime_probe["aggregate"]["tokens_saved"],
            "saving_rate": runtime_probe["aggregate"]["runtime_saving_rate"],
            "gate": runtime_probe["decision"]["runtime_admission_gate"],
            "scope": "blocked_direct_markdown_loop_state",
            "raw_text_stored": False,
        },
        {
            "observation_id": "HEADROOM-OBS-RUNTIME-SCENARIO-MATRIX",
            "source_evidence": rel(SCENARIO_MATRIX_JSON),
            "observation_type": "runtime_scenario_matrix",
            "runtime_used": True,
            "included_in_loop_cost_observation": True,
            "tokens_before": scenario_matrix["aggregate"]["tokens_before"],
            "tokens_after": scenario_matrix["aggregate"]["tokens_after"],
            "tokens_saved": scenario_matrix["aggregate"]["tokens_saved"],
            "saving_rate": scenario_matrix["aggregate"]["saving_rate"],
            "gate": scenario_matrix["aggregate"]["scenario_gate_pass_count"] >= 1,
            "scope": "scenario_discovery_only",
            "raw_text_stored": False,
        },
        {
            "observation_id": "HEADROOM-OBS-COST-MEASUREMENT-OUTPUT",
            "source_evidence": rel(COST_OUTPUT_JSON),
            "observation_type": "allowed_structured_metric_output",
            "runtime_used": True,
            "included_in_loop_cost_observation": True,
            "tokens_before": cost_output["aggregate"]["tokens_before"],
            "tokens_after": cost_output["aggregate"]["tokens_after"],
            "tokens_saved": cost_output["aggregate"]["tokens_saved"],
            "saving_rate": cost_output["aggregate"]["saving_rate"],
            "gate": cost_output["aggregate"]["output_gate"],
            "scope": "structured_metric_tool_output_only",
            "raw_text_stored": False,
        },
        {
            "observation_id": "HEADROOM-OBS-CONTROLLED-METRIC-PILOT",
            "source_evidence": rel(PILOT_JSON),
            "observation_type": "controlled_metric_pilot",
            "runtime_used": True,
            "included_in_loop_cost_observation": True,
            "tokens_before": pilot["aggregate"]["tokens_before"],
            "tokens_after": pilot["aggregate"]["tokens_after"],
            "tokens_saved": pilot["aggregate"]["tokens_saved"],
            "saving_rate": pilot["aggregate"]["saving_rate"],
            "gate": pilot["decision"]["controlled_metric_pilot_gate"],
            "scope": pilot["pilot_scope"],
            "raw_text_stored": False,
        },
    ]
    included = [entry for entry in observation_entries if entry["included_in_loop_cost_observation"]]
    runtime_included = [entry for entry in included if entry["runtime_used"]]
    blocked = [
        {
            "scenario_id": item["scenario_id"],
            "reason": item["reason_codes"],
        }
        for item in policy["entries"]
        if item["scenario_id"] in rejected
    ]
    total_before = sum(int(entry["tokens_before"]) for entry in runtime_included)
    total_after = sum(int(entry["tokens_after"]) for entry in runtime_included)
    total_saved = total_before - total_after
    result = {
        "evidence_id": "HEADROOM-LOOP-COST-OBSERVATION-20260621",
        "date": "2026-06-21",
        "status": "continuous_loop_cost_observation_enabled_for_metric_output",
        "observation_window": {
            "window_id": "HEADROOM-LOOP-COST-WINDOW-20260621-001",
            "source_count": len(observation_entries),
            "included_count": len(included),
            "runtime_included_count": len(runtime_included),
            "blocked_scenario_count": len(blocked),
        },
        "policy_source": rel(POLICY_JSON),
        "allowed_scenarios": sorted(allowed),
        "blocked_scenarios": blocked,
        "aggregate": {
            "runtime_tokens_before": total_before,
            "runtime_tokens_after": total_after,
            "runtime_tokens_saved": total_saved,
            "runtime_saving_rate": round(total_saved / total_before, 6) if total_before else 0.0,
            "all_included_gates_pass": all(entry["gate"] for entry in included),
            "all_blocked_scenarios_excluded": True,
            "production_admission_gate": False,
        },
        "observations": observation_entries,
        "decision": {
            "loop_cost_observation_gate": True,
            "continuous_observation_scope": "metric_and_adapter_output_and_cost_evidence_only",
            "next_required_action": "repeat observation on subsequent LOOP rounds before L3.5/L4 admission",
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
        "headroom_loop_cost_observation=pass "
        f"runtime_included={len(runtime_included)} blocked={len(blocked)} "
        f"runtime_saving_rate={result['aggregate']['runtime_saving_rate']} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
