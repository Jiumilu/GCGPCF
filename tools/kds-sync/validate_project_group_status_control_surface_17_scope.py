#!/usr/bin/env python3
"""Validate 17-project status scope across the GPCF control surface."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
CURRENT_STATE = ROOT / "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md"
DEV_QUEUE = ROOT / "docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md"

REQUIRED_FILES = {
    "status_matrix": STATUS_MATRIX,
    "control_board": CONTROL_BOARD,
    "core_register": CORE_REGISTER,
    "current_state": CURRENT_STATE,
    "dev_queue": DEV_QUEUE,
}

REQUIRED_SHARED_TOKENS = [
    "GPCF-PROJECT-STATUS-MATRIX-17-SCOPE-001",
    "validate_gpcf_project_status_matrix_17_project_scope.py",
    "ready_for_review=12",
    "partial_verified=1",
    "repair_required=3",
    "owner_review_required=1",
]

FILE_SPECIFIC_TOKENS = {
    "status_matrix": [
        "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
        "globalcloud-project-group-dev-task-queue-20260626.md",
        "development_queue_ready = true",
        "current_state_baseline_refresh_controlled",
    ],
    "control_board": [
        "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
        "globalcloud-project-group-dev-task-queue-20260626.md",
        "development_queue_ready = true",
        "dirty_repo_count = 7",
        "trigger_layer_binding_count = 17",
        "dependency_edge_binding_count = 17",
    ],
    "core_register": [
        "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
        "globalcloud-project-group-dev-task-queue-20260626.md",
        "development_queue_ready = true",
        "dirty_repo_count = 7",
        "trigger_layer_binding_count = 17",
        "dependency_edge_binding_count = 17",
    ],
    "current_state": [
        "project_group_current_state_baseline_refresh_20260626 = controlled",
        "development_queue_ready = true",
        "dirty_repo_count = 3",
        "trigger_layer_binding_count = 17",
        "dependency_edge_binding_count = 17",
    ],
    "dev_queue": [
        "development_queue_ready = true",
        "trigger_layer_binding_count = 17",
        "dependency_edge_binding_count = 17",
    ],
}

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

GFIS_ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "formal_confirmation_files",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing_file:{path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def validate_gfis_real_fact_entry(failures: list[str]) -> dict[str, str]:
    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        values = parse_kv_output(cached)
    else:
        result = subprocess.run(
            ["python3", "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        values = parse_kv_output(result.stdout)
        if result.returncode != 0:
            failures.append("GFIS real-fact entry gate failed: " + result.stdout.strip())
            return values
    if values.get("strong_block") != "true":
        failures.append("GFIS real-fact entry gate must keep strong_block=true")
    if values.get("status_ceiling") != "repair_required":
        failures.append("GFIS real-fact entry status ceiling must remain repair_required")
    for key in GFIS_ZERO_KEYS:
        if values.get(key) != "0":
            failures.append(f"GFIS real-fact entry must keep {key}=0, got {values.get(key)!r}")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


def main() -> int:
    failures: list[str] = []
    texts = {name: read(path, failures) for name, path in REQUIRED_FILES.items()}
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    for token in REQUIRED_SHARED_TOKENS:
        for name in ("status_matrix", "control_board", "core_register"):
            text = texts[name]
            if token not in text:
                failures.append(f"{name}:missing_shared_token:{token}")

    for name, tokens in FILE_SPECIFIC_TOKENS.items():
        text = texts[name]
        for token in tokens:
            if token not in text:
                failures.append(f"{name}:missing_file_specific_token:{token}")

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
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates control-surface consistency only; it does not execute project tasks or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
