#!/usr/bin/env python3
"""Validate that the GPCF project status matrix covers all 17 projects."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"

REQUIRED_PROJECT_ROWS = {
    "GlobalCloud GFIS": ["repair_required", "真实 source-of-record", "均未完成/未授权"],
    "GlobalCloud GPC": ["partial_verified", "external_runtime_evidence_required", "不得声明外部联调完成"],
    "GlobalCloud PVAOS": ["ready_for_review", "L3 Ready", "WAES/GPC dependency dry-run"],
    "GlobalCloud WAES": ["repair_required", "authorization_required", "不得声明治理运行闭环"],
    "GlobalCloud KDS": ["ready_for_review", "KDS Token", "只允许本机私有文件"],
    "GlobalCloud Brain": ["ready_for_review", "L3 Ready", "lint"],
    "GlobalCloud PKC": ["ready_for_review", "KDS/Brain", "体验验证"],
    "GlobalCloud XiaoC": ["ready_for_review", "Wrangler", "真实部署证据"],
    "GlobalCloud XGD": ["ready_for_review", "TICK loop dry-run", "Brain UI/ACUI"],
    "GlobalCloud XiaoG": ["ready_for_review", "XiaoG-L4-011", "未 live API"],
    "GlobalCloud MMC": ["ready_for_review", "L3 Ready", "治理模板复用"],
    "GlobalCoud GPCF": ["repair_required", "partial_repair", "不恢复 100/100"],
    "GlobalCloud Studio": ["ready_for_review", "review_required_before_commit", "不发布、不推送"],
    "WAS 世界资产体系": ["ready_for_review", "semantic_foundation_candidate / not_accepted", "MONITOR-101"],
    "GlobalCloud XWAIL": ["ready_for_review", "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001", "不证明完整 XWAIL 工具链"],
    "GlobalCloud AaaS / AAAS": ["ready_for_review", "AAAS-WAES-BINDING-PRECHECK-001", "不证明真实计费"],
    "GlobalCloud SOP": ["owner_review_required", "SOP-SCENARIO-OWNER-REVIEW-001", "不证明场景方案已确认"],
}

REQUIRED_SUMMARY_TOKENS = [
    "状态：v5.75",
    "项目群状态矩阵补齐为 17 项目口径",
    "| ready_for_review | 12 |",
    "| partial_verified | 1 | GPC |",
    "| repair_required | 3 | GFIS、WAES、GPCF |",
    "| owner_review_required | 1 | SOP |",
    "GPCF-PROJECT-STATUS-MATRIX-17-SCOPE-001",
    "accepted",
    "integrated",
    "customer_accepted",
]

FORBIDDEN_COMPLETION_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def main() -> int:
    failures: list[str] = []
    text = STATUS_MATRIX.read_text(encoding="utf-8") if STATUS_MATRIX.exists() else ""
    if not text:
        failures.append(f"missing_status_matrix:{STATUS_MATRIX}")

    table_rows = [
        line for line in text.splitlines()
        if line.startswith("| ") and " | GlobalCloud " in line or " | WAS 世界资产体系 |" in line or " | GlobalCoud GPCF |" in line
    ]

    for project, tokens in REQUIRED_PROJECT_ROWS.items():
        rows = [line for line in table_rows if f"| {project} |" in line]
        if len(rows) != 1:
            failures.append(f"project_row_count:{project}:{len(rows)}")
            continue
        row = rows[0]
        for token in tokens:
            if token not in row:
                failures.append(f"project_row_missing_token:{project}:{token}")

    for token in REQUIRED_SUMMARY_TOKENS:
        if token not in text:
            failures.append(f"missing_summary_token:{token}")

    for token in FORBIDDEN_COMPLETION_CLAIMS:
        if token in text:
            failures.append(f"forbidden_completion_claim:{token}")

    result = {
        "gate": "gpcf_project_status_matrix_17_project_scope",
        "status": "pass" if not failures else "fail",
        "projects_checked": len(REQUIRED_PROJECT_ROWS),
        "failures": failures,
        "warnings": [
            "This validates status matrix coverage only; it does not upgrade project status or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
