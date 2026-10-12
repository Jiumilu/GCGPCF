#!/usr/bin/env python3
"""Validate project-group baseline and compatibility declarations."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1")
BASELINE = "GC-WAS-PG-BASELINE-0.1.0"

PLAN_PATHS = [
    PROJECT_ROOT / "WAS世界资产体系/docs/GlobalCloud WAS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud XWAIL/GlobalCloud XWAIL 总体方案.md",
    PROJECT_ROOT / "GlobalCloud AAAS/docs/GlobalCloud AaaS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud GPC/GlobalCloud GPC 总体方案.md",
    PROJECT_ROOT / "GlobalCloud WAES/GlobalCloud WAES 总体方案.md",
    PROJECT_ROOT / "GlobalCloud GFIS/GlobalCloud GFIS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud PVAOS/GlobalCloud PVAOS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud KDS/GlobalCloud KDS 总体方案.md",
    PROJECT_ROOT / "GlobalCloud Brain/GlobalCloud Brain 总体方案.md",
    PROJECT_ROOT / "GlobalCloud Studio/GlobalCloud Studio 总体方案.md",
    PROJECT_ROOT / "GlobalCloud MMC/GlobalCloud MMC 总体方案.md",
    PROJECT_ROOT / "GlobalCloud PKC/GlobalCloud PKC 总体方案.md",
    PROJECT_ROOT / "GlobalCloud SOP/GlobalCloud SOP 总体方案.md",
    PROJECT_ROOT / "GlobalCloud XGD/GlobalCloud XGD 总体方案.md",
    PROJECT_ROOT / "GlobalCloud XiaoC/GlobalCloud XiaoC 总体方案.md",
    PROJECT_ROOT / "GlobalCloud XiaoG/GlobalCloud XiaoG 总体方案.md",
    PROJECT_ROOT / "GlobalCoud GPCF/GlobalCloud GPCF 总体方案.md",
]

REQUIRED_COMPATIBILITY_TERMS = [
    BASELINE,
    "项目群版本基线",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    for path in PLAN_PATHS:
        if not path.exists():
            warnings.append(f"missing project master plan: {path}")
            continue
        checked.append(str(path))
        text = path.read_text(encoding="utf-8")
        for token in REQUIRED_COMPATIBILITY_TERMS:
            if token not in text:
                failures.append(f"{path.name}: missing version compatibility token {token}")

    result = {
        "gate": "project_version_compatibility",
        "status": "pass" if not failures else "fail",
        "baseline": BASELINE,
        "failures": failures,
        "warnings": warnings,
        "checked": checked,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
