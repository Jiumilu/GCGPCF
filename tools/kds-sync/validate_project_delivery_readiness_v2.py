#!/usr/bin/env python3
"""Validate phase-1 delivery-readiness governance boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "01-architecture/GlobalCloud项目群实施方案.md"

REQUIRED_TOKENS = [
    "真实交付管理",
    "交付说明",
    "部署说明",
    "运行说明",
    "测试报告",
    "回滚说明",
    "验收清单",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    text = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing delivery readiness token: {token}")

    warnings.append("phase 3 does not assert any project is delivered to a customer")

    result = {
        "gate": "project_delivery_readiness_v2",
        "status": "pass" if not failures else "fail",
        "readiness": "phase_3_all_project_plans_controlled",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
