#!/usr/bin/env python3
"""Validate GlobalCloud next executable task packs for all projects."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

TASKS = [
    "AAAS-WAES-BINDING-PRECHECK-001",
    "BRAIN-HUMAN-REVIEW-DECISION-001",
    "WAS-XWAIL-ONTOLOGY-MAPPING-001",
    "XIAOC-MODEL-ROUTING-DRYRUN-001",
    "WAES-LINT-RUNTIME-001",
    "GPC-EXTERNAL-RUNTIME-EVIDENCE-001",
    "STUDIO-WORKFLOW-PERMISSIONS-001",
    "GPCF-AUTHORIZATION-PACKAGE-ROUTING-001",
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "GPCF-LOOP-DOCUMENT-GATE-READINESS-RETRY-HARDENING-20260626-001",
    "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001",
    "GFIS-REAL-SOR-001",
    "MMC-GOVERNANCE-TEMPLATE-SMOKE-001",
    "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
    "XIAOG-LIVE-API-AUTH-PACK-001",
    "PVAOS-RELEASE-REVIEW-001",
    "SOP-SCENARIO-OWNER-REVIEW-001",
    "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001",
    "XGD-TICK-BRAIN-SMOKE-001",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-NEXT-TASK-PACKS-001",
    "next_executable_task_packs = controlled",
    "project_task_pack_count = 17",
    "project_group_git_clean = partial",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "Wave 1",
    "Wave 2",
    "Wave 3",
    "Governance",
    "需要真实业务 owner",
    "stage、commit、push、delete、deploy、release、merge",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-NEXT-TASK-PACKS-001",
    "globalcloud-project-group-next-executable-task-packs-20260625.md",
    "validate_project_group_next_executable_task_packs.py",
    "next_executable_task_packs = controlled",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in next task packs: {token}")

    for task in TASKS:
        rows = []
        for line in doc_text.splitlines():
            if not line.startswith("|") or f"`{task}`" not in line:
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) >= 2 and columns[1] == f"`{task}`":
                rows.append(line)
        if len(rows) != 1:
            failures.append(f"task must have exactly one row: {task}")
            continue
        row = rows[0]
        columns = [part.strip() for part in row.strip().strip("|").split("|")]
        if len(columns) != 12:
            failures.append(f"task row must have 12 columns: {task}")
            continue
        required_columns = {
            "commands": columns[5],
            "expected_evidence": columns[6],
            "gate": columns[7],
            "rollback_boundary": columns[8],
            "dependency_impact": columns[9],
            "forbidden_claims": columns[11],
        }
        for name, value in required_columns.items():
            if not value or value == "-":
                failures.append(f"task row missing {name}: {task}")
        if ".md" not in columns[6]:
            failures.append(f"task expected evidence must be markdown evidence: {task}")
        if "gate" not in columns[7]:
            failures.append(f"task gate column must include gate wording: {task}")
        if "不声明" not in columns[11]:
            failures.append(f"task forbidden claims column must include 不声明: {task}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "project_group_next_executable_task_packs",
        "status": "pass" if not failures else "fail",
        "task_pack_count": len(TASKS),
        "failures": failures,
        "warnings": [
            "This validates task-pack control fields only; it does not execute project tasks or grant commit, push, accepted, integrated, production, or customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
