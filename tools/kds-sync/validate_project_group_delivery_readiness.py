#!/usr/bin/env python3
"""Validate delivery readiness boundaries for project-group master-plan governance."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-project-master-plan-control-register.md"
GOVERNANCE_DOC = ROOT / "02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md"

REQUIRED_BOUNDARY_TOKENS = [
    "不声明项目群业务实现完成",
    "不声明客户交付完成",
    "accepted",
    "integrated",
    "production_ready",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    register_text = REGISTER.read_text(encoding="utf-8") if REGISTER.exists() else ""
    governance_text = GOVERNANCE_DOC.read_text(encoding="utf-8") if GOVERNANCE_DOC.exists() else ""

    if not register_text:
        failures.append(f"missing register: {REGISTER}")
    if not governance_text:
        failures.append(f"missing governance doc: {GOVERNANCE_DOC}")

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in governance_text:
            failures.append(f"missing non-claim boundary token: {token}")

    if "project_master_plan_alignment = controlled" not in register_text:
        failures.append("project master-plan alignment is not controlled")

    warnings.append("delivery readiness remains partial because business implementation and customer delivery are outside document-governance completion")

    result = {
        "gate": "project_group_delivery_readiness",
        "status": "pass" if not failures else "fail",
        "readiness": "partial",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
