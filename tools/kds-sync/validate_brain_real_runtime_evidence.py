#!/usr/bin/env python3
"""Validate Brain real runtime baseline evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
EVIDENCE = ROOT / "docs/harness/Brain/evidence/brain-real-runtime-baseline-20260624.md"

REQUIRED_EVIDENCE_TOKENS = [
    "Brain 真实运行基线证据 2026-06-24",
    "node_modules_present",
    "npm run lint",
    "npm run typecheck",
    "npm run test",
    "208 passed (208)",
    "npm run build",
    "ECONNREFUSED 127.0.0.1:5175",
    "brain_status=200",
    "kds_total_pages=2732",
    "brain_runtime_health = verified",
    "brain_target_panel_runtime_matrix = verified",
    "brain_target_panel_data_quality = verified",
    "brain_format_check = verified",
    "brain_browser_user_flow = verified_with_boundaries",
    "brain_read_closure_matrix = verified_with_boundaries",
    "brain_chinese_gates = verified_with_boundaries",
    "brain_completion_matrix = repair_required",
    "brain_chrome_browser_visible_signals = confirmed",
    "brain_team_authorization_contract = confirmed_c_read_write_split",
    "brain_browser_runtime_smoke = verified_with_boundaries",
    "Chrome Playwright live browser observation",
    "brain_harness_evidence = repair_required",
    "不登记 Brain 真实运行闭环完成",
    "不登记 Brain 客户验收通过",
]

REQUIRED_REGISTER_TOKENS = [
    "brain-real-runtime-baseline-20260624.md",
    "brain_runtime_health",
    "brain_status=200",
    "208 tests",
    "format:check",
    "validate:browser-user-flow",
    "validate:read-closure-matrix",
    "validate:chinese-gates",
    "brain_chrome_browser_visible_signals",
    "team authorization",
    "repair_required",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "Brain 真实运行闭环完成",
    "Brain 真实集成完成",
    "Brain 真实交付完成",
    "Brain 客户验收通过",
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
        "Brain runtime-health, browser smoke, browser user-flow, read-closure, and Chinese gates are verified with boundaries; status-audit, bulk-fix execution, authorized prompt, harness, delivery, and customer acceptance remain repair_required/not_collected.",
    ]

    register_text = read(REGISTER, failures)
    evidence_text = read(EVIDENCE, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in Brain evidence: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(register_text + "\n" + evidence_text, failures)

    result = {
        "gate": "brain_real_runtime_evidence",
        "status": "pass" if not failures else "fail",
        "runtime_status": "repair_required",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
