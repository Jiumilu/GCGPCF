#!/usr/bin/env python3
"""Validate Brain review handoff evidence and project-group references."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HANDOFF_DOC = ROOT / "docs/harness/Brain/evidence/brain-review-handoff-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_HANDOFF_TOKENS = [
    "Brain 人工审查移交包 2026-06-25",
    "BRAIN-REVIEW-HANDOFF-001",
    "brain-authorized-closure-refresh-execution-20260625.md",
    "kds-rag-export-repair-20260625.md",
    "connect ECONNREFUSED 127.0.0.1:5175",
    "npm run dev:local",
    "npm run validate:completion-matrix",
    "requirements=11 achieved=11 blockers=0",
    "completion_status=not_complete",
    "npm run validate:harness-evidence",
    "test_count=208 test_passed=208",
    "runtime_brain_status=200",
    "runtime_kds_total_pages=2732",
    "npm run validate:loop-harness",
    "npm run validate:local-action-boundaries",
    "npm run format:check",
    "brain_review_handoff = ready_for_human_review",
    "brain_status = ready_for_review / authorization_boundary",
    "kds_rag_export = verified_with_local_dev_boundary",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "brain-review-handoff-20260625.md",
    "BRAIN-REVIEW-HANDOFF-001",
    "ready_for_human_review",
    "ready_for_review / authorization_boundary",
    "KDS -> Brain",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "Brain 已 accepted",
    "Brain 已 integrated",
    "客户验收通过",
]

ALLOWED_CONTEXTS = ["不声明", "不得", "不自动", "只有用户明确确认", "当前无"]


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
    handoff_text = read(HANDOFF_DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_HANDOFF_TOKENS:
        if token not in handoff_text:
            failures.append(f"missing token in Brain review handoff evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in Brain references/register: {token}")

    check_forbidden(handoff_text + "\n" + refs_text, failures)

    result = {
        "gate": "brain_review_handoff",
        "status": "pass" if not failures else "fail",
        "handoff_status": "ready_for_human_review",
        "failures": failures,
        "warnings": [
            "This validates the handoff package and references; it does not grant accepted, integrated, production_ready, or customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
