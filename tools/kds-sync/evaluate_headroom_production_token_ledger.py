#!/usr/bin/env python3
"""Evaluate a sanitized Headroom production-token ledger."""

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


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path} must contain JSON object")
    return data


def evaluate_entry(entry: dict) -> dict:
    for forbidden_key in ["raw_prompt", "raw_completion", "authorization_header", "provider_secret"]:
        require(forbidden_key not in entry, f"entry must not contain {forbidden_key}")
    require(entry.get("source_kind") in {"provider_billing_export", "sanitized_runtime_usage_ledger"}, "entry source_kind must be a production-safe source")
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
    require(baseline_cost > 0, "baseline_cost must be greater than zero")
    saving_rate = (baseline_cost - headroom_cost) / baseline_cost
    admission_gate = (
        entry.get("answer_equivalence") == "pass"
        and entry.get("sensitive_redaction_gate") == "pass"
        and entry.get("project_marker_gate") == "pass"
        and isinstance(entry.get("rollback_plan_id"), str)
        and bool(entry.get("rollback_plan_id"))
        and number(entry, "retrieval_miss_count") <= number(entry, "agreed_retrieval_miss_threshold")
        and saving_rate >= number(entry, "minimum_saving_rate")
    )
    require(admission_gate, f"entry admission gate failed: {entry.get('measurement_id')}")
    return {
        "measurement_id": entry.get("measurement_id"),
        "project": entry.get("project"),
        "scenario": entry.get("scenario"),
        "baseline_cost": round(baseline_cost, 6),
        "headroom_cost": round(headroom_cost, 6),
        "gross_saving": round(baseline_cost - headroom_cost, 6),
        "saving_rate": round(saving_rate, 6),
        "admission_gate": True,
    }


def evaluate_ledger(ledger: dict) -> dict:
    require(ledger.get("ledger_type") == "sanitized_production_token_usage_ledger", "invalid ledger_type")
    require(ledger.get("telemetry") == "off", "telemetry must be off")
    require(ledger.get("sensitive_raw_text_stored") is False, "raw sensitive text must not be stored")
    require(ledger.get("raw_prompt_storage") == "forbidden", "raw prompt storage must be forbidden")
    for forbidden in ["contains_provider_secret", "contains_authorization_header", "contains_raw_prompt", "contains_raw_completion"]:
        require(ledger.get(forbidden) is False, f"{forbidden} must be false")
    require(ledger.get("measured_production_tokens") is True, "production ledger must explicitly measure production tokens")
    authorization = ledger.get("authorization", {})
    require(isinstance(authorization.get("authorized_window_id"), str) and authorization["authorized_window_id"], "authorized_window_id is required")
    require(isinstance(authorization.get("authorized_by"), str) and authorization["authorized_by"], "authorized_by is required")
    require(isinstance(authorization.get("authorized_at"), str) and authorization["authorized_at"], "authorized_at is required")
    require(authorization.get("scope") == "project_group_production_token_measurement", "authorization scope mismatch")
    entries = ledger.get("entries", [])
    require(isinstance(entries, list) and entries, "ledger entries are required")
    entry_results = [evaluate_entry(entry) for entry in entries]
    baseline_cost = sum(item["baseline_cost"] for item in entry_results)
    headroom_cost = sum(item["headroom_cost"] for item in entry_results)
    gross_saving = baseline_cost - headroom_cost
    return {
        "ledger_id": ledger.get("ledger_id"),
        "entry_count": len(entry_results),
        "baseline_cost": round(baseline_cost, 6),
        "headroom_cost": round(headroom_cost, 6),
        "gross_saving": round(gross_saving, 6),
        "saving_rate": round(gross_saving / baseline_cost, 6),
        "entry_results": entry_results,
        "production_token_ledger_gate": True,
        "measured_production_tokens": True,
    }


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    require(path.exists(), f"missing ledger: {path}")
    return path


def main(argv: list[str]) -> int:
    require(len(argv) == 2, "usage: evaluate_headroom_production_token_ledger.py <ledger.json>")
    result = evaluate_ledger(load_json(resolve_path(argv[1])))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
