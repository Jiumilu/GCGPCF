#!/usr/bin/env python3
"""Validate PVAOS release gate repair evidence and references."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/PVAOS/evidence/pvaos-release-gate-repair-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_EVIDENCE_TOKENS = [
    "PVAOS Release Gate 修复与本地发布准入证据 2026-06-25",
    "PVAOS-RELEASE-GATE-001",
    "pvaos/D4-release-readiness-governance",
    "vitest.config.ts",
    "package.json",
    "package-lock.json",
    "setupFiles: ['./src/app/tests/setup.ts']",
    "dompurify",
    "3.4.11",
    "npx playwright install chromium",
    "npm run lint",
    "npm run validate:modules",
    "npm run typecheck",
    "npm run test",
    "npm run build",
    "npm audit --audit-level=moderate --registry=https://registry.npmjs.org",
    "npm run test:e2e",
    "npm run check:production-domain",
    "npm run release:gate:local",
    "Test Files 80 passed (80)",
    "Tests 547 passed (547)",
    "found 0 vulnerabilities",
    "50 passed",
    "4 skipped",
    "PASS all local release readiness checks",
    "pvaos_release_gate = verified_with_local_release_gate_boundary",
    "pvaos_status_candidate = ready_for_review",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "pvaos-release-gate-repair-20260625.md",
    "PVAOS-RELEASE-GATE-001",
    "verified_with_local_release_gate_boundary",
    "GFIS/GPC/PVAOS -> SCaaS",
    "ready_for_review",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "远程 CI 完成",
    "PR 完成",
    "merge 完成",
    "生产发布完成",
    "客户验收完成",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = ["不声明", "未", "没有", "不得", "no ", "false"]


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
            failures.append(f"missing token in PVAOS release gate evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in PVAOS references/register: {token}")

    check_forbidden(evidence_text + "\n" + refs_text, failures)

    result = {
        "gate": "pvaos_release_gate_repair",
        "status": "pass" if not failures else "fail",
        "runtime_status": "verified_with_local_release_gate_boundary",
        "failures": failures,
        "warnings": [
            "This validates local PVAOS release gate evidence only; it does not prove remote CI, PR, merge, production release, or customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
