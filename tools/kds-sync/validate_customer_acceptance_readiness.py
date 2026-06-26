#!/usr/bin/env python3
"""Validate phase-1 customer-acceptance governance boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "GlobalCloud 项目群实施方案.md"

REQUIRED_TOKENS = [
    "客户验收管理",
    "验收对象",
    "验收场景",
    "验收步骤",
    "验收人",
    "签收证据",
    "没有客户或授权人确认，不得声明 `customer_accepted`",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    text = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing customer acceptance token: {token}")

    warnings.append("phase 3 does not assert customer acceptance")

    result = {
        "gate": "customer_acceptance_readiness",
        "status": "pass" if not failures else "fail",
        "readiness": "phase_3_all_project_plans_controlled",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
