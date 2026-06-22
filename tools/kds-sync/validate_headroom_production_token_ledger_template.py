#!/usr/bin/env python3
"""Validate the Headroom sanitized production-token ledger template."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "fixtures/headroom/headroom-production-token-ledger-template.json"
INTAKE_GATE = ROOT / "docs/harness/evidence/headroom-production-token-intake-gate-20260621.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def number(data: dict, key: str) -> float:
    value = data.get(key)
    require(isinstance(value, (int, float)), f"{key} must be numeric")
    require(value >= 0, f"{key} must be non-negative")
    return float(value)


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def evaluate_entry(entry: dict) -> dict:
    baseline_cost = (
        number(entry, "input_tokens_before") * number(entry, "P_in")
        + number(entry, "output_tokens_before") * number(entry, "P_out")
        + number(entry, "cache_write_tokens_before") * number(entry, "P_cache_write")
        + number(entry, "cache_read_tokens_before") * number(entry, "P_cache_read")
    )
    headroom_cost = (
        number(entry, "input_tokens_after") * number(entry, "P_in")
        + number(entry, "output_tokens_after") * number(entry, "P_out")
        + number(entry, "cache_write_tokens_after") * number(entry, "P_cache_write")
        + number(entry, "cache_read_tokens_after") * number(entry, "P_cache_read")
        + number(entry, "P_runtime")
    )
    saving_rate = 0.0 if baseline_cost == 0 else (baseline_cost - headroom_cost) / baseline_cost
    admission_gate = (
        baseline_cost > 0
        and entry.get("answer_equivalence") == "pass"
        and entry.get("sensitive_redaction_gate") == "pass"
        and entry.get("project_marker_gate") == "pass"
        and entry.get("rollback_plan_id") is not None
        and number(entry, "retrieval_miss_count") <= number(entry, "agreed_retrieval_miss_threshold")
        and saving_rate >= number(entry, "minimum_saving_rate")
    )
    return {
        "measurement_id": entry.get("measurement_id"),
        "baseline_cost": round(baseline_cost, 6),
        "headroom_cost": round(headroom_cost, 6),
        "saving_rate": round(saving_rate, 6),
        "admission_gate": admission_gate,
    }


def main() -> int:
    ledger = load_json(LEDGER)
    intake_gate = load_json(INTAKE_GATE)
    require(intake_gate["gate"]["production_token_intake_gate"] is False, "intake gate must remain blocked")
    require(ledger.get("ledger_id") == "HEADROOM-PRODUCTION-TOKEN-LEDGER-TEMPLATE", "ledger id mismatch")
    require(ledger.get("ledger_type") == "sanitized_production_token_usage_ledger", "ledger type mismatch")
    require(ledger.get("telemetry") == "off", "telemetry must be off")
    require(ledger.get("sensitive_raw_text_stored") is False, "raw sensitive text must not be stored")
    require(ledger.get("raw_prompt_storage") == "forbidden", "raw prompt storage must be forbidden")
    for forbidden in ["contains_provider_secret", "contains_authorization_header", "contains_raw_prompt", "contains_raw_completion"]:
        require(ledger.get(forbidden) is False, f"{forbidden} must be false")
    require(ledger.get("measured_production_tokens") is False, "template must not claim measured production tokens")
    authorization = ledger.get("authorization", {})
    require(authorization.get("authorized_window_id") is None, "template must not claim authorized window")
    require(authorization.get("scope") == "not_authorized_template", "authorization scope must be template-only")

    entries = ledger.get("entries", [])
    require(isinstance(entries, list) and len(entries) == 1, "template must contain one placeholder entry")
    results = [evaluate_entry(entry) for entry in entries]
    require(results[0]["baseline_cost"] == 0.0, "placeholder baseline cost must be zero")
    require(results[0]["admission_gate"] is False, "placeholder admission gate must remain false")
    print(
        "headroom_production_token_ledger_template=pass "
        "entries=1 measured_production_tokens=false "
        "admission_gate=false production_admission_gate=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
