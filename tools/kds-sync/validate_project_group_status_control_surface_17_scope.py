#!/usr/bin/env python3
"""Validate 17-project status scope across the GPCF control surface."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_FILES = {
    "status_matrix": STATUS_MATRIX,
    "control_board": CONTROL_BOARD,
    "core_register": CORE_REGISTER,
}

REQUIRED_SHARED_TOKENS = [
    "GPCF-PROJECT-STATUS-MATRIX-17-SCOPE-001",
    "validate_gpcf_project_status_matrix_17_project_scope.py",
    "ready_for_review=12",
    "partial_verified=1",
    "repair_required=3",
    "owner_review_required=1",
]

REQUIRED_PROJECT_TOKENS = [
    "XWAIL",
    "AaaS",
    "AAAS",
    "SOP",
    "WAES",
    "GPC",
    "GFIS",
]

REQUIRED_BOUNDARY_TOKENS = [
    "accepted",
    "integrated",
    "customer",
]

FORBIDDEN_TRUE_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing_file:{path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    texts = {name: read(path, failures) for name, path in REQUIRED_FILES.items()}

    for token in REQUIRED_SHARED_TOKENS:
        for name, text in texts.items():
            if token not in text:
                failures.append(f"{name}:missing_shared_token:{token}")

    for token in REQUIRED_PROJECT_TOKENS:
        if token not in texts["control_board"]:
            failures.append(f"control_board:missing_project_token:{token}")
        if token not in texts["status_matrix"]:
            failures.append(f"status_matrix:missing_project_token:{token}")

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in texts["core_register"]:
            failures.append(f"core_register:missing_boundary_token:{token}")

    for name, text in texts.items():
        for token in FORBIDDEN_TRUE_CLAIMS:
            if token in text:
                failures.append(f"{name}:forbidden_true_claim:{token}")

    result = {
        "gate": "project_group_status_control_surface_17_scope",
        "status": "pass" if not failures else "fail",
        "files_checked": len(REQUIRED_FILES),
        "failures": failures,
        "warnings": [
            "This validates control-surface consistency only; it does not execute project tasks or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
