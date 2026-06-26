#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group Loop gate readiness pass evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-loop-gate-readiness-pass-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

REQUIRED_DOC_TOKENS = [
    "GPCF-LOOP-GATE-READINESS-PASS-20260626-001",
    "project_group_loop_gate_readiness_20260626 = pass",
    "loop_gate_readiness_pass",
    "readiness_gate | `pass`",
    "checked_repos | `13`",
    "passed_repos | `13`",
    "failed_repos | `0`",
    "gate_reasons | `none`",
    "project_group_gate_readiness=pass checked_repos=13 passed=13 failed=0 reasons=none",
    "Git clean 门禁仍为 `partial`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
]

REFERENCE_TOKENS = [
    "GPCF-LOOP-GATE-READINESS-PASS-20260626-001",
    "globalcloud-project-group-loop-gate-readiness-pass-20260626.md",
    "validate_project_group_loop_gate_readiness_pass_20260626.py",
    "loop_gate_readiness_pass",
]

FORBIDDEN_CLAIMS = [
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
    "项目群 Git 全量 clean = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def readiness_output() -> tuple[int, str]:
    result = subprocess.run(
        ["python3", "tools/kds-sync/validate_loop_project_group_gate_readiness.py"],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.returncode, result.stdout.strip()


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(STATUS, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in readiness pass evidence: {token}")

    for token in REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden claim: {token}")

    rc, output = readiness_output()
    if rc != 0:
        failures.append(f"readiness command failed: rc={rc} output={output}")
    if "project_group_gate_readiness=pass checked_repos=13 passed=13 failed=0 reasons=none" not in output:
        failures.append(f"unexpected readiness output: {output}")

    result = {
        "gate": "project_group_loop_gate_readiness_pass_20260626",
        "status": "pass" if not failures else "fail",
        "readiness_returncode": rc,
        "failures": failures,
        "warnings": [
            "This validates project-group Loop gate readiness only; Git clean, stage, commit, push, integrated, accepted, production, and customer acceptance remain outside this pass.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
