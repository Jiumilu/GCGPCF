#!/usr/bin/env python3
"""Validate that each GlobalCloud project has at most one authoritative master plan."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1")

PROJECT_PLAN_CANDIDATES = {
    "WAS世界资产体系": [PROJECT_ROOT / "WAS世界资产体系/docs/GlobalCloud WAS 总体方案.md"],
    "GlobalCloud XWAIL": [PROJECT_ROOT / "GlobalCloud XWAIL/GlobalCloud XWAIL 总体方案.md"],
    "GlobalCloud AaaS": [PROJECT_ROOT / "GlobalCloud AAAS/docs/GlobalCloud AaaS 总体方案.md"],
    "GlobalCloud WAES": [PROJECT_ROOT / "GlobalCloud WAES/GlobalCloud WAES 总体方案.md"],
    "GlobalCloud GFIS": [PROJECT_ROOT / "GlobalCloud GFIS/GlobalCloud GFIS 总体方案.md"],
    "GlobalCloud GPC": [PROJECT_ROOT / "GlobalCloud GPC/GlobalCloud GPC 总体方案.md"],
    "GlobalCloud PVAOS": [PROJECT_ROOT / "GlobalCloud PVAOS/GlobalCloud PVAOS 总体方案.md"],
    "GlobalCloud KDS": [PROJECT_ROOT / "GlobalCloud KDS/GlobalCloud KDS 总体方案.md"],
    "GlobalCloud Brain": [PROJECT_ROOT / "GlobalCloud Brain/GlobalCloud Brain 总体方案.md"],
    "GlobalCloud Studio": [PROJECT_ROOT / "GlobalCloud Studio/GlobalCloud Studio 总体方案.md"],
    "GlobalCloud MMC": [PROJECT_ROOT / "GlobalCloud MMC/GlobalCloud MMC 总体方案.md"],
    "GlobalCloud PKC": [PROJECT_ROOT / "GlobalCloud PKC/GlobalCloud PKC 总体方案.md"],
    "GlobalCloud SOP": [PROJECT_ROOT / "GlobalCloud SOP/GlobalCloud SOP 总体方案.md"],
    "GlobalCloud XGD": [PROJECT_ROOT / "GlobalCloud XGD/GlobalCloud XGD 总体方案.md"],
    "GlobalCloud XiaoC": [PROJECT_ROOT / "GlobalCloud XiaoC/GlobalCloud XiaoC 总体方案.md"],
    "GlobalCloud XiaoG": [PROJECT_ROOT / "GlobalCloud XiaoG/GlobalCloud XiaoG 总体方案.md"],
    "GlobalCoud GPCF": [PROJECT_ROOT / "GlobalCoud GPCF/GlobalCloud GPCF 总体方案.md"],
}


def is_controlled_plan(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "status: controlled" in text and "总体方案" in text


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    authoritative: dict[str, list[str]] = {}

    for project, paths in PROJECT_PLAN_CANDIDATES.items():
        existing = [str(path) for path in paths if is_controlled_plan(path)]
        authoritative[project] = existing
        if len(existing) > 1:
            failures.append(f"multiple authoritative master plans for {project}: {existing}")
        if not existing:
            warnings.append(f"missing authoritative master plan: {project}")

    result = {
        "gate": "project_master_plan_uniqueness",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
        "authoritative": authoritative,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
