#!/usr/bin/env python3
"""Validate the batch-2 project master-plan authorization request."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTH_DOC = ROOT / "02-governance/project-master-plan-batch-2-authorization-request.md"

REQUIRED_TOKENS = [
    "项目总体方案第二批批量更新授权请求",
    "authorization_status: confirmed_by_user",
    "GlobalCloud MMC",
    "GlobalCloud PKC",
    "GlobalCloud SOP",
    "GlobalCloud XGD",
    "GlobalCloud XiaoC",
    "GlobalCloud XiaoG",
    "是否需要用户确认",
    "我确认开始第二批项目总体方案批量建立",
    "确认时间：2026-06-24",
    "不等于项目群总体方案治理完成",
]

EXPECTED_PATHS = [
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/GlobalCloud MMC 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC/GlobalCloud PKC 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud SOP/AGENTS.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud SOP/GlobalCloud SOP 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD/GlobalCloud XGD 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC/GlobalCloud XiaoC 总体方案.md",
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/GlobalCloud XiaoG 总体方案.md",
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
        failures.append("batch-2 authorization still declares pending_user_confirmation after user confirmation")

    result = {
        "gate": "project_master_plan_batch_2_authorization",
        "status": "pass" if not failures else "fail",
        "authorization_status": "confirmed_by_user",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
