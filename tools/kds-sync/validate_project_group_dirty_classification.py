#!/usr/bin/env python3
"""Validate project-group dirty change classification evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-dirty-classification-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_DOC_TOKENS = [
    "GlobalCloud 项目群 Dirty 变更分类证据 2026-06-25",
    "GPCF-GIT-DIRTY-CLASSIFY-001",
    "project_group_dirty_classification = controlled",
    "project_group_git_clean = blocked",
    "historical_project_group_git_clean_20260625 = partial",
    "live_recheck_gate_20260628 = blocked",
    "WAS世界资产体系",
    "system_noise / not_business_change",
    "GlobalCloud GPC",
    "GPC-EVIDENCE-BROWSER-001",
    "GlobalCoud GPCF",
    "GPCF 真实执行治理包",
    "GlobalCloud KDS",
    "external_business_report_update / owner_confirmation_required",
    "GlobalCloud PVAOS",
    "PVAOS-RELEASE-GATE-001",
    "GlobalCloud SOP",
    "scenario_plan_generated_output / owner_confirmation_required",
    "npm run quality:repo = pass",
    "npm run test:e2e = pass, 20 passed",
    "npm run release:gate:local = pass",
    "document_control.py",
    "commit_ready = false",
    "push_ready = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-GIT-DIRTY-CLASSIFY-001",
    "globalcloud-project-group-dirty-classification-20260625.md",
    "validate_project_group_dirty_classification.py",
    "project_group_dirty_classification = controlled",
    "project_group_git_clean = blocked",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "项目群 Git 全量 clean",
    "项目群可提交",
    "项目群可推送",
    "项目群可验收",
    "KDS/SOP 业务内容已确认",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = ["不声明", "不得", "false", "待", "需要", "不能"]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def check_forbidden(text: str, failures: list[str]) -> None:
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        start = 0
        while True:
            idx = text.find(token, start)
            if idx == -1:
                break
            line_start = text.rfind("\n", 0, idx) + 1
            line_end = text.find("\n", idx)
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end]
            if not any(context in line for context in ALLOWED_CONTEXTS):
                failures.append(f"forbidden positive claim without boundary: {line}")
            start = idx + len(token)


def main() -> int:
    failures: list[str] = []
    doc_text = read(EVIDENCE_DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in dirty classification evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    check_forbidden(doc_text + "\n" + refs_text, failures)

    result = {
        "gate": "project_group_dirty_classification",
        "status": "pass" if not failures else "fail",
        "classification": "controlled",
        "failures": failures,
        "warnings": [
            "This validates dirty change classification only; it does not approve deletion, commit, push, or merge.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
