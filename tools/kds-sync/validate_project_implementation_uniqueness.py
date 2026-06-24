#!/usr/bin/env python3
"""Validate that project implementation plans are unique when established."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1")

EXPECTED_IMPLEMENTATION_PLANS = {
    "WAS世界资产体系": [PROJECT_ROOT / "WAS世界资产体系/docs/GlobalCloud WAS 实施方案.md"],
    "GlobalCloud XWAIL": [PROJECT_ROOT / "GlobalCloud XWAIL/GlobalCloud XWAIL 实施方案.md"],
    "GlobalCloud AaaS": [PROJECT_ROOT / "GlobalCloud AAAS/docs/GlobalCloud AaaS 实施方案.md"],
    "GlobalCloud WAES": [PROJECT_ROOT / "GlobalCloud WAES/GlobalCloud WAES 实施方案.md"],
    "GlobalCloud GFIS": [PROJECT_ROOT / "GlobalCloud GFIS/GlobalCloud GFIS 实施方案.md"],
    "GlobalCloud GPC": [PROJECT_ROOT / "GlobalCloud GPC/GlobalCloud GPC 实施方案.md"],
    "GlobalCloud PVAOS": [PROJECT_ROOT / "GlobalCloud PVAOS/GlobalCloud PVAOS 实施方案.md"],
    "GlobalCloud KDS": [PROJECT_ROOT / "GlobalCloud KDS/GlobalCloud KDS 实施方案.md"],
    "GlobalCloud Brain": [PROJECT_ROOT / "GlobalCloud Brain/GlobalCloud Brain 实施方案.md"],
    "GlobalCloud Studio": [PROJECT_ROOT / "GlobalCloud Studio/GlobalCloud Studio 实施方案.md"],
    "GlobalCloud MMC": [PROJECT_ROOT / "GlobalCloud MMC/GlobalCloud MMC 实施方案.md"],
    "GlobalCloud PKC": [PROJECT_ROOT / "GlobalCloud PKC/GlobalCloud PKC 实施方案.md"],
    "GlobalCloud SOP": [PROJECT_ROOT / "GlobalCloud SOP/GlobalCloud SOP 实施方案.md"],
    "GlobalCloud XGD": [PROJECT_ROOT / "GlobalCloud XGD/GlobalCloud XGD 实施方案.md"],
    "GlobalCloud XiaoC": [PROJECT_ROOT / "GlobalCloud XiaoC/GlobalCloud XiaoC 实施方案.md"],
    "GlobalCloud XiaoG": [PROJECT_ROOT / "GlobalCloud XiaoG/GlobalCloud XiaoG 实施方案.md"],
    "GlobalCloud GPCF": [PROJECT_ROOT / "GlobalCoud GPCF/GlobalCloud GPCF 实施方案.md"],
}

REQUIRED_PROJECTS = {
    "WAS世界资产体系",
    "GlobalCloud XWAIL",
    "GlobalCloud AaaS",
    "GlobalCloud WAES",
    "GlobalCloud GFIS",
    "GlobalCloud GPC",
    "GlobalCloud PVAOS",
    "GlobalCloud KDS",
    "GlobalCloud Brain",
    "GlobalCloud GPCF",
    "GlobalCloud Studio",
    "GlobalCloud MMC",
    "GlobalCloud PKC",
    "GlobalCloud SOP",
    "GlobalCloud XGD",
    "GlobalCloud XiaoC",
    "GlobalCloud XiaoG",
}


def is_controlled_implementation_plan(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "status: controlled" in text and "实施方案" in text


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    authoritative: dict[str, list[str]] = {}

    for project, paths in EXPECTED_IMPLEMENTATION_PLANS.items():
        existing = [str(path) for path in paths if is_controlled_implementation_plan(path)]
        authoritative[project] = existing
        if len(existing) > 1:
            failures.append(f"multiple implementation plans for {project}: {existing}")
        if not existing and project in REQUIRED_PROJECTS:
            failures.append(f"implementation plan missing: {project}")

    result = {
        "gate": "project_implementation_uniqueness",
        "status": "pass" if not failures else "fail",
        "phase": "phase_3_all_project_plans_controlled",
        "failures": failures,
        "warnings": warnings,
        "authoritative": authoritative,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
