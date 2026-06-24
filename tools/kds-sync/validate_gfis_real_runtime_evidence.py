#!/usr/bin/env python3
"""Validate GFIS real runtime baseline evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
EVIDENCE = ROOT / "docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md"
README = ROOT / "docs/harness/GFIS/README.md"
EVIDENCE_README = ROOT / "docs/harness/GFIS/evidence/README.md"

REQUIRED_EVIDENCE_TOKENS = [
    "GFIS 真实运行基线证据 2026-06-24",
    "GCFIS desk reachable: http://localhost:8080/desk",
    "gcfis API contract validation passed",
    "gcfis core flow validation passed",
    "gcfis external contract smoke passed",
    "gfis work-order API contract validation passed",
    "gfis WAES gate event validation passed",
    "npm run quality:100",
    "npm run quality:repo",
    "npm run test:e2e",
    "npm run test:coverage",
    "npm run quality:ops",
    "gfis_runtime_evidence = partial_verified",
    "gfis_interface_evidence = partial_verified",
    "gfis_repair_required = external_evidence_branding_browser_ops_drill",
    "不登记 GFIS 真实交付完成",
    "不登记 GFIS 客户验收通过",
]

REQUIRED_REGISTER_TOKENS = [
    "gfis-real-runtime-baseline-20260624.md",
    "gfis_runtime_evidence = partial_verified",
    "gfis_interface_evidence = partial_verified",
    "gfis_repair_required = external_evidence_branding_browser_ops_drill",
    "npm run check:js",
    "npm run quality:100",
    "npm run quality:repo",
    "npm run test:e2e",
    "npm run test:coverage",
    "npm run quality:ops",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "GFIS 真实交付完成",
    "GFIS 外部绿色供应链与金融联调完成",
    "GFIS 客户验收通过",
    "GFIS production_ready",
    "GFIS 现场样本真实提交完成",
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
        "GFIS evidence is partial: runtime/API evidence exists, but external evidence, browser dependencies, branding mapping, ops drill, delivery, and customer acceptance remain open.",
    ]

    register_text = read(REGISTER, failures)
    evidence_text = read(EVIDENCE, failures)
    read(README, failures)
    read(EVIDENCE_README, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in GFIS evidence: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(register_text + "\n" + evidence_text, failures)

    result = {
        "gate": "gfis_real_runtime_evidence",
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
