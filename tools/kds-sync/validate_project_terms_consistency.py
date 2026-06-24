#!/usr/bin/env python3
"""Validate core WAS terminology consistency in project master plans."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1")

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

REQUIRED_TERMS = [
    "WAS",
    "Ontology",
    "XWAIL",
    "WAE",
    "WAES",
    "AaaS",
]

FORBIDDEN_TERMS = [
    "GPC-Native",
    "WAES 是业务主账",
    "WAE = 浏览器",
    "WAES = 主账",
    "协同中台",
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
        for term in REQUIRED_TERMS:
            if term not in text:
                failures.append(f"{path.name}: missing required term {term}")
        for term in FORBIDDEN_TERMS:
            if term in text:
                failures.append(f"{path.name}: forbidden term present {term}")

    result = {
        "gate": "project_terms_consistency",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
        "checked": checked,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
