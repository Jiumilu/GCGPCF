#!/usr/bin/env python3
"""Validate GPC evidence/browser repair evidence and references."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/GPC/evidence/gpc-evidence-browser-repair-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_EVIDENCE_TOKENS = [
    "GPC Evidence/Browser 修复与边界证据 2026-06-25",
    "GPC-EVIDENCE-BROWSER-001",
    "gpc_browser_quality_repo = verified_with_external_runtime_evidence_required",
    "partial_verified_browser_repaired_external_runtime_evidence_required",
    "README.md missing docs/18-gcfis-quality-execution-closure.md",
    "GCFIS Demo v0.1",
    "L4_blocked",
    "README.md",
    "tests/e2e/gcfis-core-flow.spec.js",
    "docs/26-gcfis-100-external-evidence-register.md",
    "npm run quality:repo",
    "gcfis delivery readiness validation passed",
    "npm run test:e2e",
    "20 passed",
    "npm run quality:100",
    "failed=2",
    "production_environment_confirmation.json",
    "external_integration_joint_test.json",
    "npm run quality:ops",
    "GCFIS desk not reachable",
    "runtime GCFIS language asset not reachable",
    "gpc_quality_100 = failed_external_evidence_required",
    "gpc_quality_ops = failed_runtime_surface_required",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "gpc-evidence-browser-repair-20260625.md",
    "GPC-EVIDENCE-BROWSER-001",
    "verified_with_external_runtime_evidence_required",
    "partial_verified_browser_repaired_external_runtime_evidence_required",
    "validate_gpc_evidence_browser_repair.py",
    "GFIS/GPC/PVAOS -> SCaaS",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "真实交付完成",
    "外部绿色供应链或金融联调完成",
    "生产环境确认完成",
    "GCFIS runtime desk 可达",
    "客户验收通过",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = ["不声明", "不得", "不能", "仍缺", "failed", "false", "未"]


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
            failures.append(f"missing token in GPC evidence/browser repair evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in GPC references/register: {token}")

    check_forbidden(evidence_text + "\n" + refs_text, failures)

    result = {
        "gate": "gpc_evidence_browser_repair",
        "status": "pass" if not failures else "fail",
        "runtime_status": "verified_with_external_runtime_evidence_required",
        "failures": failures,
        "warnings": [
            "This validates GPC README/browser quality repair only; it does not prove production confirmation, external joint test, GCFIS runtime desk availability, delivery, or customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
