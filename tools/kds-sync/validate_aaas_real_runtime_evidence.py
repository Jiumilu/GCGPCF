#!/usr/bin/env python3
"""Validate AaaS real runtime baseline evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
EVIDENCE = ROOT / "docs/harness/AaaS/evidence/aaas-real-runtime-baseline-20260624.md"
README = ROOT / "docs/harness/AaaS/README.md"
EVIDENCE_README = ROOT / "docs/harness/AaaS/evidence/README.md"

REQUIRED_EVIDENCE_TOKENS = [
    "AaaS 真实运行基线证据 2026-06-24",
    "main",
    "missing scripts/validate_service_package.py",
    "missing scripts/validate_metering.py",
    "missing scripts/validate_sla.py",
    "missing scripts/verify_evidence_requirements.py",
    "validate_project_implementation_inheritance.py",
    "validate_project_terms_consistency.py",
    "validate_project_version_compatibility.py",
    "validate_was_xwail_aaas_plan_alignment.py",
    "aaas_governance_evidence = verified",
    "aaas_runtime_evidence = repair_required",
    "aaas_repair_required = service_package_metering_sla_commands_missing",
    "不登记 AaaS 服务包已实现",
    "不登记任何客户验收通过",
]

REQUIRED_REGISTER_TOKENS = [
    "aaas-real-runtime-baseline-20260624.md",
    "aaas_governance_evidence = verified",
    "aaas_runtime_evidence = repair_required",
    "aaas_repair_required = service_package_metering_sla_commands_missing",
    "scripts/validate_service_package.py",
    "scripts/validate_metering.py",
    "scripts/validate_sla.py",
    "scripts/verify_evidence_requirements.py",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "AaaS 服务包已实现",
    "AaaS 计量或 SLA 已真实运行",
    "客户可订阅状态达成",
    "客户验收通过",
    "商业交付完成",
]

ALLOWED_NEGATION_CONTEXTS = [
    "不声明",
    "不登记",
    "不证明",
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
        "AaaS evidence proves governance alignment and missing service validation commands; service package runtime remains pending.",
    ]

    register_text = read(REGISTER, failures)
    evidence_text = read(EVIDENCE, failures)
    read(README, failures)
    read(EVIDENCE_README, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in AaaS evidence: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(register_text + "\n" + evidence_text, failures)

    result = {
        "gate": "aaas_real_runtime_evidence",
        "status": "pass" if not failures else "fail",
        "runtime_status": "repair_required",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
