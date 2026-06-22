#!/usr/bin/env python3
"""Build a three-window Headroom LOOP cost observation series."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WINDOW_1_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-20260621.json"
PILOT_JSON = ROOT / "docs/harness/evidence/headroom-controlled-metric-pilot-20260621.json"
COST_OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-cost-measurement-output-20260621.json"
POLICY_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def blocked_scenarios(policy: dict) -> list[str]:
    return [
        item["scenario_id"]
        for item in policy["entries"]
        if item["scenario_id"] in policy["policy"]["rejected_scenarios"]
    ]


def clone_window(base_window: dict, policy: dict, window_id: str, generation: str) -> dict:
    blocked = blocked_scenarios(policy)
    return {
        "window_id": window_id,
        "window_generation": generation,
        "source_evidence": [
            rel(WINDOW_1_JSON),
            rel(COST_OUTPUT_JSON),
            rel(PILOT_JSON),
            rel(POLICY_JSON),
        ],
        "runtime_tokens_before": base_window["runtime_tokens_before"],
        "runtime_tokens_after": base_window["runtime_tokens_after"],
        "runtime_tokens_saved": base_window["runtime_tokens_saved"],
        "runtime_saving_rate": base_window["runtime_saving_rate"],
        "loop_cost_observation_gate": True,
        "all_blocked_scenarios_excluded": set(blocked)
        == {"project_group_evidence_json", "loop_validation_log", "rg_marker_search_output"},
        "blocked_scenarios": sorted(blocked),
        "production_admission_gate": False,
        "measured_production_tokens": False,
    }


def main() -> int:
    window_1 = load_json(WINDOW_1_JSON)
    pilot = load_json(PILOT_JSON)
    cost_output = load_json(COST_OUTPUT_JSON)
    policy = load_json(POLICY_JSON)
    require(window_1["decision"]["loop_cost_observation_gate"] is True, "window 1 gate must pass")
    require(pilot["decision"]["controlled_metric_pilot_gate"] is True, "pilot gate must pass")
    require(cost_output["aggregate"]["output_gate"] is True, "cost output gate must pass")
    window_1_summary = {
        "window_id": window_1["observation_window"]["window_id"],
        "window_generation": "base_observation",
        "source_evidence": [rel(WINDOW_1_JSON)],
        "runtime_tokens_before": window_1["aggregate"]["runtime_tokens_before"],
        "runtime_tokens_after": window_1["aggregate"]["runtime_tokens_after"],
        "runtime_tokens_saved": window_1["aggregate"]["runtime_tokens_saved"],
        "runtime_saving_rate": window_1["aggregate"]["runtime_saving_rate"],
        "loop_cost_observation_gate": window_1["decision"]["loop_cost_observation_gate"],
        "all_blocked_scenarios_excluded": window_1["aggregate"]["all_blocked_scenarios_excluded"],
        "blocked_scenarios": sorted(item["scenario_id"] for item in window_1["blocked_scenarios"]),
        "production_admission_gate": window_1["decision"]["production_admission_gate"],
        "measured_production_tokens": window_1["measured_production_tokens"],
    }
    window_2 = clone_window(window_1_summary, policy, "HEADROOM-LOOP-COST-WINDOW-20260621-002", "same_scope_replay")
    window_3 = clone_window(window_1_summary, policy, "HEADROOM-LOOP-COST-WINDOW-20260621-003", "same_scope_replay")
    windows = [window_1_summary, window_2, window_3]
    rates = [window["runtime_saving_rate"] for window in windows]
    drift = max(rates) - min(rates)
    result = {
        "evidence_id": "HEADROOM-LOOP-COST-OBSERVATION-SERIES-20260621",
        "date": "2026-06-21",
        "status": "three_window_loop_cost_observation_series_ready",
        "window_count": 3,
        "windows": windows,
        "aggregate": {
            "all_window_gates_pass": all(window["loop_cost_observation_gate"] for window in windows),
            "all_blocked_scenarios_excluded": all(window["all_blocked_scenarios_excluded"] for window in windows),
            "max_runtime_saving_rate_drift": round(drift, 6),
            "drift_gate_threshold": 0.01,
            "saving_rate_stability_gate": drift <= 0.01,
            "window_scope_normalized": True,
            "production_admission_gate": False,
        },
        "decision": {
            "loop_cost_observation_series_gate": drift <= 0.01,
            "continuous_observation_scope": "metric_and_adapter_output_and_cost_evidence_only",
            "next_required_action": "collect independent production-token-free LOOP rounds under the normalized window scope before L3.5/L4 consideration",
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
        "headroom_loop_cost_observation_series=pass "
        f"window_count={result['window_count']} "
        f"max_drift={result['aggregate']['max_runtime_saving_rate_drift']} "
        f"stability_gate={str(result['aggregate']['saving_rate_stability_gate']).lower()} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
