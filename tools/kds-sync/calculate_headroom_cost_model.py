#!/usr/bin/env python3
"""Calculate Headroom cost-model metrics from a measurement JSON fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def number(data: dict, key: str) -> float:
    value = data.get(key)
    require(isinstance(value, (int, float)), f"{key} must be numeric")
    require(value >= 0, f"{key} must be non-negative")
    return float(value)


def main(argv: list[str]) -> int:
    require(len(argv) == 2, "usage: calculate_headroom_cost_model.py <measurement.json>")
    path = Path(argv[1])
    if not path.is_absolute():
        path = ROOT / path
    require(path.exists(), f"missing measurement file: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "measurement must be a JSON object")
    require(data.get("telemetry") == "off", "telemetry must be off")
    require(data.get("sensitive_raw_text_stored") is False, "raw sensitive text must not be stored")

    baseline_cost = (
        number(data, "input_tokens_before") * number(data, "P_in")
        + number(data, "output_tokens_before") * number(data, "P_out")
        + number(data, "cache_write_tokens_before") * number(data, "P_cache_write")
        + number(data, "cache_read_tokens_before") * number(data, "P_cache_read")
    )
    headroom_cost = (
        number(data, "input_tokens_after") * number(data, "P_in")
        + number(data, "output_tokens_after") * number(data, "P_out")
        + number(data, "cache_write_tokens_after") * number(data, "P_cache_write")
        + number(data, "cache_read_tokens_after") * number(data, "P_cache_read")
        + number(data, "P_runtime")
    )
    require(baseline_cost > 0, "baseline_cost must be greater than zero")

    gross_saving = baseline_cost - headroom_cost
    saving_rate = gross_saving / baseline_cost
    admission_gate = (
        data.get("answer_equivalence") == "pass"
        and data.get("sensitive_redaction_gate") == "pass"
        and number(data, "retrieval_miss_count") <= number(data, "agreed_retrieval_miss_threshold")
        and saving_rate >= number(data, "minimum_saving_rate")
    )

    result = {
        "measurement_id": data.get("measurement_id"),
        "project": data.get("project"),
        "scenario": data.get("scenario"),
        "baseline_cost": round(baseline_cost, 6),
        "headroom_cost": round(headroom_cost, 6),
        "gross_saving": round(gross_saving, 6),
        "saving_rate": round(saving_rate, 6),
        "admission_gate": admission_gate,
        "measured_project_group_tokens": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
