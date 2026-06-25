#!/usr/bin/env python3
"""Validate KDS RAG export repair evidence and project-group references."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/KDS/evidence/kds-rag-export-repair-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_EVIDENCE_TOKENS = [
    "KDS RAG export 修复证据 2026-06-25",
    "KDS-RAG-EXPORT-001",
    "TypeError: unhashable type: 'list'",
    "_governance/scripts/rag_admission_policy.py",
    "_governance/scripts/wiki_trust_audit.py",
    "allowlist_count=156",
    "manifest_count=156",
    "error_count=0",
    "warning_count=1",
    "gate_count=46",
    "issue_count=0",
    "2 passed in 4.52s",
    "gbrain search",
    "gbrain query",
    "rag_admissible_count=156",
    "kds_rag_export = verified_with_local_dev_boundary",
    "kds_status_candidate = ready_for_review",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "kds-rag-export-repair-20260625.md",
    "KDS-RAG-EXPORT-001",
    "verified_with_local_dev_boundary",
    "ready_for_review",
    "KDS -> Brain",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "KDS 真实运行闭环完成",
    "RAG 导出完成",
    "真实交付完成",
    "客户验收通过",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = [
    "不声明",
    "不得",
    "不代表",
    "不能",
    "未",
]


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
    evidence_text = read(EVIDENCE_DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in KDS RAG export repair evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in KDS references/register: {token}")

    check_forbidden(evidence_text + "\n" + refs_text, failures)

    result = {
        "gate": "kds_rag_export_repair",
        "status": "pass" if not failures else "fail",
        "repair_status": "verified_with_local_dev_boundary",
        "failures": failures,
        "warnings": [
            "This validates GPCF evidence and references; KDS runtime commands must be rerun for fresh runtime proof.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
