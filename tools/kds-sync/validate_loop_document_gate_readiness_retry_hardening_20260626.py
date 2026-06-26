#!/usr/bin/env python3
"""Validate Loop document gate readiness retry hardening evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-loop-document-gate-readiness-retry-hardening-20260626.md"
SCRIPT = ROOT / "tools/kds-sync/loop_document_gate.py"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

REQUIRED_DOC_TOKENS = [
    "GPCF-LOOP-DOCUMENT-GATE-READINESS-RETRY-HARDENING-20260626-001",
    "loop_document_gate_readiness_retry_hardening_20260626 = controlled",
    "loop_document_gate_readiness_retry_hardening_controlled",
    "change_scope | `loop_document_gate_project_group_readiness_retry_only`",
    "retry_count | `1`",
    "gate_relaxed | `false`",
    "project_group_gate_readiness=pass checked_repos=13 passed=13 failed=0 reasons=none",
    "gate=pass",
    "不放松 missing metadata",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
]

REQUIRED_SCRIPT_TOKENS = [
    "def run_with_retry(command: list[str], retries: int = 1)",
    "checks[\"project_group_gate_readiness\"] = run_with_retry",
    "validate_loop_project_group_gate_readiness.py",
    "retries=1",
]

REFERENCE_TOKENS = [
    "GPCF-LOOP-DOCUMENT-GATE-READINESS-RETRY-HARDENING-20260626-001",
    "globalcloud-loop-document-gate-readiness-retry-hardening-20260626.md",
    "validate_loop_document_gate_readiness_retry_hardening_20260626.py",
    "loop_document_gate_readiness_retry_hardening_controlled",
]

FORBIDDEN_TOKENS = [
    "gate_relaxed | `true`",
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
    "accepted=true",
    "integrated=true",
    "production_ready=true",
    "customer_accepted=true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    script_text = read(SCRIPT, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in retry hardening evidence: {token}")

    for token in REQUIRED_SCRIPT_TOKENS:
        if token not in script_text:
            failures.append(f"missing token in loop_document_gate.py: {token}")

    for token in REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_TOKENS:
        if token in combined:
            failures.append(f"forbidden positive claim: {token}")

    result = {
        "gate": "loop_document_gate_readiness_retry_hardening_20260626",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "This validates retry hardening evidence only; it does not relax gates, execute project tasks, grant Git actions, or approve accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
