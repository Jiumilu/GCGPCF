#!/usr/bin/env python3
"""Validate the GlobalCloud project-group dependency execution matrix."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

EDGES = [
    "WAES -> XWAIL",
    "XWAIL -> AaaS",
    "WAES -> AaaS",
    "KDS -> Brain",
    "GFIS -> GPC",
    "GPC -> PVAOS",
    "PVAOS -> SCaaS",
    "GFIS/GPC/PVAOS -> SCaaS",
    "WAS -> Ontology -> XWAIL",
    "GPCF -> all projects",
    "Studio -> GPCF/WAES",
    "PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-DEPENDENCY-MATRIX-001",
    "dependency_execution_matrix = controlled",
    "dependency_edge_count = 12",
    "project_group_git_clean = partial",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "状态传导规则",
    "dependency_review_required",
    "必须另行人工确认",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-DEPENDENCY-MATRIX-001",
    "globalcloud-project-group-dependency-execution-matrix-20260625.md",
    "validate_project_group_dependency_execution_matrix.py",
    "dependency_execution_matrix = controlled",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "project_group_git_clean = pass",
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
            failures.append(f"missing token in dependency matrix: {token}")

    for edge in EDGES:
        rows = []
        for line in doc_text.splitlines():
            if not line.startswith("|") or f"`{edge}`" not in line:
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) == 12 and columns[1] == f"`{edge}`":
                rows.append(line)
        if len(rows) != 1:
            failures.append(f"dependency edge must have exactly one row: {edge}")
            continue
        columns = [part.strip() for part in rows[0].strip().strip("|").split("|")]
        if len(columns) != 12:
            failures.append(f"dependency row must have 12 columns: {edge}")
            continue
        required_columns = {
            "upstream_evidence": columns[5],
            "downstream_task": columns[6],
            "propagation_gate": columns[7],
            "blocker_or_risk": columns[8],
            "rollback_or_downgrade": columns[9],
            "forbidden_claims": columns[11],
        }
        for name, value in required_columns.items():
            if not value or value == "-":
                failures.append(f"dependency row missing {name}: {edge}")
        if "gate" not in columns[7]:
            failures.append(f"dependency row gate column must include gate wording: {edge}")
        if "不声明" not in columns[11]:
            failures.append(f"dependency row forbidden claims must include 不声明: {edge}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "project_group_dependency_execution_matrix",
        "status": "pass" if not failures else "fail",
        "dependency_edge_count": len(EDGES),
        "failures": failures,
        "warnings": [
            "This validates dependency control only; it does not execute project tasks or grant accepted, integrated, production, customer acceptance, commit, push, deploy, or release authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
