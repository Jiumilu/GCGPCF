#!/usr/bin/env python3
"""Validate the batch-1 project master-plan authorization request."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTH_DOC = ROOT / "02-governance/project-master-plan-batch-1-authorization-request.md"

REQUIRED_TOKENS = [
    "项目总体方案第一批批量更新授权请求",
    "authorization_status: confirmed_by_user",
    "GlobalCloud WAES",
    "GlobalCloud GFIS",
    "GlobalCloud PVAOS",
    "GlobalCloud KDS",
    "GlobalCloud Brain",
    "GlobalCloud Studio",
    "是否需要用户确认",
    "我确认开始第一批项目总体方案批量建立",
    "确认时间：2026-06-24",
    "不等于项目群总体方案治理完成",
]

EXPECTED_PATHS = [
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES/GlobalCloud WAES 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/GlobalCloud GFIS 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS/GlobalCloud PVAOS 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/GlobalCloud KDS 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain/GlobalCloud Brain 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/GlobalCloud Studio 总体方案.md",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    if not AUTH_DOC.exists():
        failures.append(f"missing authorization doc: {AUTH_DOC}")
        text = ""
    else:
        text = AUTH_DOC.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing required token: {token}")

    for expected_path in EXPECTED_PATHS:
        if expected_path not in text:
            failures.append(f"missing expected path: {expected_path}")

    if "authorization_status: pending_user_confirmation" in text:
        failures.append("authorization is still pending")

    result = {
        "gate": "project_master_plan_batch_1_authorization",
        "status": "pass" if not failures else "fail",
        "authorization_status": "confirmed_by_user",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
