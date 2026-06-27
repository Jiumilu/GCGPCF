#!/usr/bin/env python3
"""Validate delivery readiness boundaries for project-group master-plan governance."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-project-master-plan-control-register.md"
GOVERNANCE_DOC = ROOT / "02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md"

REQUIRED_BOUNDARY_TOKENS = [
    "不声明项目群业务实现完成",
    "不声明客户交付完成",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "accepted",
    "integrated",
    "production_ready",
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
    warnings: list[str] = []

    register_text = REGISTER.read_text(encoding="utf-8") if REGISTER.exists() else ""
    governance_text = GOVERNANCE_DOC.read_text(encoding="utf-8") if GOVERNANCE_DOC.exists() else ""
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    if not register_text:
        failures.append(f"missing register: {REGISTER}")
    if not governance_text:
        failures.append(f"missing governance doc: {GOVERNANCE_DOC}")

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in governance_text:
            failures.append(f"missing non-claim boundary token: {token}")

    if "project_master_plan_alignment = controlled" not in register_text:
        failures.append("project master-plan alignment is not controlled")

    warnings.append("delivery readiness remains partial because business implementation and customer delivery are outside document-governance completion")

    result = {
        "gate": "project_group_delivery_readiness",
        "status": "pass" if not failures else "fail",
        "readiness": "partial",
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
