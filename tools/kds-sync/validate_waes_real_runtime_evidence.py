#!/usr/bin/env python3
"""Validate WAES real runtime baseline evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
EVIDENCE = ROOT / "docs/harness/WAES/evidence/waes-real-runtime-baseline-20260624.md"

REQUIRED_EVIDENCE_TOKENS = [
    "WAES 真实运行基线证据 2026-06-24",
    "waes/integration-release",
    "node_modules_present",
    "npm run check",
    "npm run typecheck",
    "npm run test",
    "npm run build",
    "npm run check:wasm",
    "waes_runtime_evidence = partial_verified",
    "waes_repair_required = lint_parse_errors",
    "不登记 WAES 真实运行闭环完成",
    "不登记客户验收通过",
]

REQUIRED_REGISTER_TOKENS = [
    "waes-real-runtime-baseline-20260624.md",
    "partial_verified",
    "repair_required",
    "lint_parse_errors",
    "typecheck/test/build/check:wasm",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "WAES 真实运行闭环完成",
    "WAES 真实集成完成",
    "WAES 真实交付完成",
    "WAES 客户验收通过",
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
        "WAES evidence is partial; lint repair is required before runtime status can advance.",
    ]

    register_text = read(REGISTER, failures)
    evidence_text = read(EVIDENCE, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in WAES evidence: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(register_text + "\n" + evidence_text, failures)

    result = {
        "gate": "waes_real_runtime_evidence",
        "status": "pass" if not failures else "fail",
        "runtime_status": "repair_required",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
