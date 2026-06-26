#!/usr/bin/env python3
"""Validate phase-1 real progress governance boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "GlobalCloud 项目群实施方案.md"
REGISTER = ROOT / "09-status/globalcloud-project-implementation-control-register.md"

REQUIRED_TOKENS = [
    "真实进度管理",
    "没有任务，不叫进度",
    "implementation_status",
    "当前里程碑",
    "证据",
    "下一步",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    text = (PLAN.read_text(encoding="utf-8") if PLAN.exists() else "") + "\n" + (
        REGISTER.read_text(encoding="utf-8") if REGISTER.exists() else ""
    )

    for token in REQUIRED_TOKENS:
        if token not in text:
            failures.append(f"missing real progress token: {token}")

    warnings.append("phase 3 validates all project implementation plans and progress governance structure, not real task completion")

    result = {
        "gate": "project_real_progress",
        "status": "pass" if not failures else "fail",
        "readiness": "phase_3_all_project_plans_controlled",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
