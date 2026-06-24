#!/usr/bin/env python3
"""Validate PVAOS real runtime baseline evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
EVIDENCE = ROOT / "docs/harness/PVAOS/evidence/pvaos-real-runtime-baseline-20260624.md"
README = ROOT / "docs/harness/PVAOS/README.md"
EVIDENCE_README = ROOT / "docs/harness/PVAOS/evidence/README.md"

REQUIRED_EVIDENCE_TOKENS = [
    "PVAOS 真实运行基线证据 2026-06-24",
    "pvaos/D4-release-readiness-governance",
    "npm run lint",
    "npm run validate:modules",
    "npm run typecheck",
    "npm run test",
    "npm run release:gate:local",
    "npm run check:production-domain",
    "npm run build",
    "Platform module validation passed: 50 menu ids, 50 configured modules.",
    "PASS: all domain and CORS probes are healthy.",
    "4091 modules transformed.",
    "pvaos_build_evidence = verified",
    "pvaos_domain_evidence = verified",
    "pvaos_runtime_evidence = partial_verified",
    "pvaos_repair_required = localstorage_test_environment_release_gate",
    "不登记 PVAOS 发布完成",
    "不登记 PVAOS 客户验收通过",
]

REQUIRED_REGISTER_TOKENS = [
    "pvaos-real-runtime-baseline-20260624.md",
    "pvaos_build_evidence = verified",
    "pvaos_domain_evidence = verified",
    "pvaos_runtime_evidence = partial_verified",
    "pvaos_repair_required = localstorage_test_environment_release_gate",
    "npm run check:production-domain",
    "npm run release:gate:local",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "PVAOS 发布完成",
    "PVAOS 客户验收通过",
    "PVAOS AaaS 运营闭环完成",
    "PVAOS production_ready",
    "PVAOS release gate 完成",
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
        "PVAOS evidence is partial: build/domain/lint/typecheck evidence exists, but tests, release gate, delivery, and customer acceptance remain open.",
    ]

    register_text = read(REGISTER, failures)
    evidence_text = read(EVIDENCE, failures)
    read(README, failures)
    read(EVIDENCE_README, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in PVAOS evidence: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(register_text + "\n" + evidence_text, failures)

    result = {
        "gate": "pvaos_real_runtime_evidence",
        "status": "pass" if not failures else "fail",
        "runtime_status": "partial_verified",
        "delivery_status": "repair_required",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
