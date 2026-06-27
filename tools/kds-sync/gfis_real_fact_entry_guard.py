#!/usr/bin/env python3
"""Shared guard for GFIS real-fact entry status."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


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


def require_gfis_real_fact_entry(root: Path) -> dict[str, str]:
    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        values = parse_kv_output(cached)
    else:
        result = subprocess.run(
            ["python3", "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        values = parse_kv_output(result.stdout)
        if result.returncode != 0:
            raise SystemExit("FAIL gfis_real_fact_entry_guard: " + result.stdout.strip())

    if values.get("strong_block") != "true":
        raise SystemExit("FAIL gfis_real_fact_entry_guard: strong_block must remain true")
    if values.get("status_ceiling") != "repair_required":
        raise SystemExit("FAIL gfis_real_fact_entry_guard: status_ceiling must remain repair_required")
    for key in GFIS_ZERO_KEYS:
        if values.get(key) != "0":
            raise SystemExit(f"FAIL gfis_real_fact_entry_guard: {key} must remain 0")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        if values.get(key) != "false":
            raise SystemExit(f"FAIL gfis_real_fact_entry_guard: {key} must remain false")
    return values
