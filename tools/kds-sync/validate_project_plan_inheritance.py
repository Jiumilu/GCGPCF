#!/usr/bin/env python3
"""Validate required inheritance structure in existing project master plans."""

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

REQUIRED_SECTIONS = [
    "项目定位",
    "与项目群主方案的继承关系",
    "项目群版本基线",
    "本项目权威职责",
    "本项目不承担的职责",
    "核心交付物",
    "与其他项目的接口关系",
    "技术架构现状和目标架构",
    "测试、交付和运行命令",
    "LOOP 接入",
    "风险、依赖、回滚和非声明边界",
]

REQUIRED_CONTROL_TOKENS = [
    "GPCF:01-architecture/WAS世界资产体系总体方案.md",
    "GC-WAS-PG-BASELINE-0.1.0",
    "loop_enabled: true",
    "不声明",
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
        for section in REQUIRED_SECTIONS:
            if section not in text:
                failures.append(f"{path.name}: missing section {section}")
        for token in REQUIRED_CONTROL_TOKENS:
            if token not in text:
                failures.append(f"{path.name}: missing control token {token}")

    result = {
        "gate": "project_plan_inheritance",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
        "checked": checked,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
