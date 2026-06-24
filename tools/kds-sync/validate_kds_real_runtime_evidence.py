#!/usr/bin/env python3
"""Validate KDS real runtime baseline evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
EVIDENCE = ROOT / "docs/harness/KDS/evidence/kds-real-runtime-baseline-20260624.md"

REQUIRED_EVIDENCE_TOKENS = [
    "KDS 真实运行基线证据 2026-06-24",
    "python3 -m pytest tests/test_api_smoke.py",
    "2 passed in 3.85s",
    "kds_loop_harness = verified",
    "kds_l4_sample_knowledge_index = ready_for_review",
    "kds_evidence_gate = verified",
    "kds_gbrain_search = partial_verified",
    "kds_rag_export = repair_required",
    "不登记 KDS 真实运行闭环完成",
    "不登记 KDS 客户验收通过",
]

REQUIRED_REGISTER_TOKENS = [
    "kds-real-runtime-baseline-20260624.md",
    "kds_rag_export",
    "ready_for_review",
    "repair_required",
    "gbrain search",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "KDS 真实运行闭环完成",
    "KDS 真实集成完成",
    "KDS 真实交付完成",
    "KDS 客户验收通过",
]

ALLOWED_NEGATION_CONTEXTS = [
    "不声明",
    "不登记",
    "不得",
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
            if not any(context in line for context in ALLOWED_NEGATION_CONTEXTS):
                failures.append(f"forbidden positive claim appears without boundary: {line}")
            start = idx + len(token)


def main() -> int:
    failures: list[str] = []
    warnings = [
        "KDS RAG export is repair_required; ready_for_review is not customer acceptance.",
    ]

    register_text = read(REGISTER, failures)
    evidence_text = read(EVIDENCE, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in KDS evidence: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(register_text + "\n" + evidence_text, failures)

    result = {
        "gate": "kds_real_runtime_evidence",
        "status": "pass" if not failures else "fail",
        "runtime_status": "repair_required",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

