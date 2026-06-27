#!/usr/bin/env python3
"""Validate project-group readiness gate timeout can cover the canonical loop gate."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/kds-sync/validate_loop_project_group_gate_readiness.py"


def load_module():
    spec = importlib.util.spec_from_file_location("readiness", SCRIPT)
    if spec is None or spec.loader is None:
        raise SystemExit("FAIL: cannot load readiness script")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    timeout = getattr(module, "GATE_TIMEOUT_SECONDS", 0)
    if timeout < 180:
        print(
            "loop_project_group_gate_readiness_timeout_budget_20260627=fail "
            f"expected_min_timeout=180 actual_timeout={timeout}"
        )
        return 1
    print("loop_project_group_gate_readiness_timeout_budget_20260627=pass")
    print(f"gate_timeout_seconds={timeout}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
