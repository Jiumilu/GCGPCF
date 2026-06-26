#!/usr/bin/env python3
"""Validate the GlobalCloud project-group status advancement matrix."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

PROJECTS = [
    "GlobalCloud AAAS",
    "GlobalCloud Brain",
    "WAS世界资产体系",
    "GlobalCloud XiaoC",
    "GlobalCloud WAES",
    "GlobalCloud GPC",
    "GlobalCloud Studio",
    "GlobalCoud GPCF",
    "GlobalCloud XWAIL",
    "GlobalCloud GFIS",
    "GlobalCloud MMC",
    "GlobalCloud KDS",
    "GlobalCloud XiaoG",
    "GlobalCloud PVAOS",
    "GlobalCloud SOP",
    "GlobalCloud PKC",
    "GlobalCloud XGD",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-STATUS-ADVANCEMENT-001",
    "status_advancement_matrix = controlled",
    "project_status_rule_count = 17",
    "ready_for_review_requires_gate = true",
    "accepted_requires_human_confirmation = true",
    "integrated_requires_human_confirmation = true",
    "customer_accepted_requires_human_confirmation = true",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "全局升级规则",
    "禁止升级条件",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-STATUS-ADVANCEMENT-001",
    "globalcloud-project-group-status-advancement-matrix-20260625.md",
    "validate_project_group_status_advancement_matrix.py",
    "status_advancement_matrix = controlled",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
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
            failures.append(f"missing token in status advancement matrix: {token}")

    for project in PROJECTS:
        rows = []
        for line in doc_text.splitlines():
            if not line.startswith("|") or f"| {project} |" not in line:
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) == 11 and columns[1] == project:
                rows.append(line)
        if len(rows) != 1:
            failures.append(f"project must have exactly one status advancement row: {project}")
            continue
        columns = [part.strip() for part in rows[0].strip().strip("|").split("|")]
        required_columns = {
            "current_status": columns[2],
            "target_status": columns[3],
            "task": columns[4],
            "required_evidence": columns[5],
            "required_gate": columns[6],
            "blocker": columns[7],
            "rollback_or_downgrade": columns[8],
            "forbidden_claims": columns[10],
        }
        for name, value in required_columns.items():
            if not value or value == "-":
                failures.append(f"status row missing {name}: {project}")
        if "gate" not in columns[6]:
            failures.append(f"status row gate column must include gate wording: {project}")
        if "不声明" not in columns[10]:
            failures.append(f"status row forbidden claims must include 不声明: {project}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "project_group_status_advancement_matrix",
        "status": "pass" if not failures else "fail",
        "project_status_rule_count": len(PROJECTS),
        "failures": failures,
        "warnings": [
            "This validates advancement criteria only; it does not execute tasks or grant accepted, integrated, production, customer acceptance, commit, push, deploy, or release authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
