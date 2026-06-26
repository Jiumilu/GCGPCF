#!/usr/bin/env python3
"""Validate project-group pre-commit review package evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-review-packages-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_DOC_TOKENS = [
    "GlobalCloud 项目群提交前 Review 分组证据 2026-06-25",
    "GPCF-REVIEW-PACKAGE-001",
    "project_group_review_packages = controlled",
    "PKG-GPC-EVIDENCE-BROWSER-20260625",
    "PKG-PVAOS-RELEASE-GATE-20260625",
    "PKG-GPCF-GOVERNANCE-EVIDENCE-20260625",
    "PKG-GPCF-KDS-MIRROR-20260625",
    "HOLD-WAS-SYSTEM-NOISE-20260625",
    "HOLD-KDS-FUNDING-REPORT-20260625",
    "HOLD-SOP-WUHAN-SCENARIO-20260625",
    "npm run quality:repo = pass",
    "npm run test:e2e = pass, 20 passed",
    "npm run release:gate:local = pass",
    "loop_document_gate.py = pass",
    "不能证明真实 KDS API 已同步",
    "review_package_count = 7",
    "review_ready_packages = 4",
    "hold_packages = 3",
    "commit_ready = false",
    "push_ready = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-REVIEW-PACKAGE-001",
    "globalcloud-project-group-review-packages-20260625.md",
    "validate_project_group_review_packages.py",
    "project_group_review_packages = controlled",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "项目群可提交",
    "项目群可推送",
    "项目群可验收",
    "真实 KDS API 已同步",
    "KDS/SOP hold 包业务内容已确认",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = ["不声明", "不能", "false", "等待", "需要", "不得"]


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
            failures.append(f"missing token in review package evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    check_forbidden(doc_text + "\n" + refs_text, failures)

    result = {
        "gate": "project_group_review_packages",
        "status": "pass" if not failures else "fail",
        "review_packages": "controlled",
        "failures": failures,
        "warnings": [
            "This validates pre-commit review grouping only; it does not stage, commit, push, merge, or approve any package.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
