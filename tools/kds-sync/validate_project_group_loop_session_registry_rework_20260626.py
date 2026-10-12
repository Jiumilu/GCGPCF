#!/usr/bin/env python3
"""Validate the project-group Loop session registry rework evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-loop-session-registry-rework-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

FAILED_PROJECTS = [
    "GlobalCloud Brain",
    "GlobalCloud GFIS",
    "GlobalCloud GPC",
    "GlobalCloud KDS",
    "GlobalCloud MMC",
    "GlobalCloud PKC",
    "GlobalCloud PVAOS",
    "GlobalCloud Studio",
    "GlobalCloud WAES",
    "GlobalCloud XGD",
    "GlobalCloud XiaoC",
    "GlobalCloud XiaoG",
    "WAS世界资产体系",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-LOOP-SESSION-REGISTRY-REWORK-20260626-001",
    "project_group_loop_session_registry_rework_20260626 = controlled",
    "loop_session_registry_rework_required",
    "readiness_gate | `fail`",
    "checked_repos | `13`",
    "failed_repos | `13`",
    "hard_failure:loop_session_registry",
    "project_group_loop_document_gate | `rework_required`",
    "LOOP-SESSION-REGISTRY-BOOTSTRAP-001",
    "LOOP-SESSION-REGISTRY-SCOPE-AUTH-001",
    "authorization_boundary",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
]

REFERENCE_TOKENS = [
    "GPCF-LOOP-SESSION-REGISTRY-REWORK-20260626-001",
    "globalcloud-project-group-loop-session-registry-rework-20260626.md",
    "validate_project_group_loop_session_registry_rework_20260626.py",
    "loop_session_registry_rework_required",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "readiness_gate | `pass`",
    "project_group_loop_document_gate | `pass`",
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def current_readiness_output() -> tuple[int, str]:
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
            failures.append(f"missing token in loop session registry rework evidence: {token}")

    for project in FAILED_PROJECTS:
        if project not in doc_text:
            failures.append(f"missing failed project in rework evidence: {project}")

    for token in REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive claim: {token}")

    rc, output = current_readiness_output()
    if rc == 0:
        failures.append("readiness gate now passes; rework evidence should be retired or superseded")
    for token in [
        "project_group_gate_readiness=fail",
        "checked_repos=13",
        "failed=13",
        "hard_failure:loop_session_registry",
    ]:
        if token not in output:
            failures.append(f"current readiness output missing expected token: {token}")

    result = {
        "gate": "project_group_loop_session_registry_rework_20260626",
        "status": "pass" if not failures else "fail",
        "readiness_returncode": rc,
        "failed_project_count": len(FAILED_PROJECTS),
        "failures": failures,
        "warnings": [
            "This validates the rework evidence only; it intentionally confirms the current project-group readiness failure and does not repair project repositories or grant write/status authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
