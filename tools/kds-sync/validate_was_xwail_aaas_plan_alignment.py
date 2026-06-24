#!/usr/bin/env python3
"""Validate WAS/XWAIL/AaaS plan alignment guardrails."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent

FILES = {
    "was_master_plan": PROJECT_ROOT / "WAS世界资产体系/docs/GlobalCloud WAS 总体方案.md",
    "was_plan": PROJECT_ROOT / "WAS世界资产体系/docs/GlobalCloud-WAS总体方案V1.2-GPCF统一重构版.md",
    "xwail_master_plan": PROJECT_ROOT / "GlobalCloud XWAIL/GlobalCloud XWAIL 总体方案.md",
    "xwail_plan": PROJECT_ROOT / "GlobalCloud XWAIL/XWAIL实施方案.md",
    "aaas_master_plan": PROJECT_ROOT / "GlobalCloud AAAS/docs/GlobalCloud AaaS 总体方案.md",
    "aaas_plan": PROJECT_ROOT / "GlobalCloud AAAS/docs/AaaS总体方案_GPCF对齐版.md",
    "was_agents": PROJECT_ROOT / "WAS世界资产体系/AGENTS.md",
    "xwail_agents": PROJECT_ROOT / "GlobalCloud XWAIL/AGENTS.md",
    "aaas_agents": PROJECT_ROOT / "GlobalCloud AAAS/AGENTS.md",
    "alignment_doc": ROOT / "01-architecture/WAS-XWAIL-AaaS三主项目方案协同矩阵与门禁.md",
}

REQUIRED = {
    "was_master_plan": [
        "GlobalCloud WAS 总体方案",
        "与项目群主方案的继承关系",
        "WAS 定义体系",
        "Ontology 定义语义",
        "XWAIL 定义契约",
        "本项目权威职责",
        "本项目不承担的职责",
        "LOOP 接入",
    ],
    "was_plan": [
        "WAS 定义体系",
        "XWAIL 定义契约",
        "WAES 负责治理",
        "AaaS",
        "不声明生产上线",
        "项目群映射",
    ],
    "xwail_master_plan": [
        "GlobalCloud XWAIL 总体方案",
        "与项目群主方案的继承关系",
        "WAS 定义体系，Ontology 定义语义，XWAIL 定义契约",
        "本项目权威职责",
        "本项目不承担的职责",
        "WAES",
        "AaaS",
        "LOOP 接入",
    ],
    "xwail_plan": [
        "WAS 是语义来源",
        "XWAIL 是机器可读表达",
        "AaaS 是服务封装",
        "不得重定义核心标签",
        "GPCF V1.2",
        "WAES",
    ],
    "aaas_master_plan": [
        "GlobalCloud AaaS 总体方案",
        "与项目群主方案的继承关系",
        "仓库目录 `GlobalCloud AAAS`",
        "ServicePackage",
        "Metering",
        "SLA",
        "WAES",
        "LOOP 接入",
    ],
    "aaas_plan": [
        "AaaS 不以“再造系统”为目标",
        "通过 XWAIL 契约",
        "WAES",
        "AaaS 不能突破上述边界",
        "GPCF V1.2",
        "GlobalCloud AaaS",
    ],
    "was_agents": [
        "WAS defines the system",
        "Main project ownership is fixed",
        "Drift Prevention Rules",
        "Required Cross-Project Change Protocol",
    ],
    "xwail_agents": [
        "main project for XWAIL",
        "XWAIL defines contracts",
        "Required Compatibility Matrix",
        "Drift Prevention Rules",
    ],
    "aaas_agents": [
        "GlobalCloud AaaS",
        "AaaS operationalizes service packages",
        "Required Compatibility Matrix",
        "Drift Prevention Rules",
    ],
    "alignment_doc": [
        "三主项目职责矩阵",
        "交付物依赖矩阵",
        "版本兼容矩阵",
        "冲突判定规则",
    ],
}

FORBIDDEN_WITHOUT_CONTEXT = {
    "xwail_plan": [
        ("XWAIL 1.1", "V1.2 协同补充"),
    ],
    "aaas_plan": [
        ("WAS 总体规划 V1.0", "GPCF V1.2"),
        ("AION-C", "Brain/WAES"),
    ],
}


def main() -> int:
    failures: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    for name, path in FILES.items():
        if not path.exists():
            failures.append({"file": name, "reason": f"missing: {path}"})
            continue
        text = path.read_text(encoding="utf-8")
        for token in REQUIRED.get(name, []):
            if token not in text:
                failures.append({"file": name, "reason": f"missing required token: {token}"})
        for legacy, context in FORBIDDEN_WITHOUT_CONTEXT.get(name, []):
            if legacy in text and context not in text:
                failures.append({
                    "file": name,
                    "reason": f"legacy token without migration context: {legacy}",
                })
            elif legacy in text:
                warnings.append({
                    "file": name,
                    "reason": f"legacy token retained with context: {legacy}",
                })

    status = "pass" if not failures else "fail"
    print(json.dumps({
        "gate": "was_xwail_aaas_plan_alignment",
        "status": status,
        "failures": failures,
        "warnings": warnings,
        "checked_files": {name: str(path) for name, path in FILES.items()},
    }, ensure_ascii=False, indent=2))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
