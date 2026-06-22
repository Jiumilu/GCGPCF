#!/usr/bin/env python3
"""Validate negative fixtures for Headroom production-token ledgers."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json"
EVALUATOR = ROOT / "tools/kds-sync/evaluate_headroom_production_token_ledger.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_evaluator():
    spec = importlib.util.spec_from_file_location("headroom_production_ledger_evaluator", EVALUATOR)
    require(spec is not None and spec.loader is not None, "cannot load evaluator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    require(data.get("fixture_id") == "HEADROOM-PRODUCTION-TOKEN-LEDGER-NEGATIVE-FIXTURES", "fixture id mismatch")
    cases = data.get("cases", [])
    require(isinstance(cases, list) and len(cases) >= 5, "expected at least five negative cases")
    evaluator = load_evaluator()
    rejected = 0
    for case in cases:
        expected_error = case.get("expected_error")
        try:
            evaluator.evaluate_ledger(case["ledger"])
        except SystemExit as exc:
            message = str(exc)
            require(expected_error in message, f"{case.get('case_id')} rejected for unexpected reason: {message}")
            rejected += 1
        else:
            raise SystemExit(f"FAIL: negative case was accepted: {case.get('case_id')}")
    print(
        "headroom_production_token_ledger_negative_fixtures=pass "
        f"case_count={len(cases)} rejected={rejected} "
        "production_admission_gate=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
