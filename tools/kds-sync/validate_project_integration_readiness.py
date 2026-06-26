#!/usr/bin/env python3
"""Validate phase-1 integration-readiness governance boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "GlobalCloud 项目群实施方案.md"

REQUIRED_TOKENS = [
    "真实集成管理",
    "调用方",
    "被调用方",
    "接口类型",
    "契约版本",
    "declared -> contracted -> mocked -> tested -> verified -> accepted",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    text = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing integration readiness token: {token}")

    warnings.append("phase 3 does not assert any cross-project integration is verified")

    result = {
        "gate": "project_integration_readiness",
        "status": "pass" if not failures else "fail",
        "readiness": "phase_3_all_project_plans_controlled",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
