#!/usr/bin/env python3
"""Validate coverage of the GFIS real-fact entry aggregation gate."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from validate_gfis_real_fact_entry_gate import EXPECTED_BY_VALIDATOR, GFIS_VALIDATORS, parse_kv_output


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_ENTRY_COVERAGE = {
    "real_source_record": {
        "validate_gfis_real_source_record_intake_gate.py": {"real_source_records": "0"},
        "validate_gfis_runtime_primary_key_gate.py": {"valid_source_records": "0"},
    },
    "equivalent_formal_confirmation_file": {
        "validate_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py": {"formal": "0"},
    },
    "manual_business_verification": {
        "validate_gfis_pending_business_verification.py": {"pending_business_verification_submissions": "0"},
    },
    "runtime_primary_key": {
        "validate_gfis_runtime_primary_key_gate.py": {"runtime_primary_key_ready": "0"},
    },
    "review_queue": {
        "validate_gfis_review_queue_admission_gate.py": {"review_queue": "0"},
    },
    "runtime_intake": {
        "validate_gfis_runtime_intake_gate.py": {"runtime_intake": "0"},
    },
    "waes_review": {
        "validate_gfis_waes_review_gate.py": {"waes_review": "0"},
    },
    "verified_artifact": {
        "validate_gfis_verified_artifact_gate.py": {"verified": "0"},
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_gfis_real_fact_entry_coverage: {message}")


def main() -> int:
    for entry, validator_contracts in REQUIRED_ENTRY_COVERAGE.items():
        for script, expected_keys in validator_contracts.items():
            require(script in GFIS_VALIDATORS, f"{entry} missing validator in aggregation list: {script}")
            contract = EXPECTED_BY_VALIDATOR.get(script, {})
            require(contract, f"{entry} missing expected-value contract: {script}")
            for key, value in expected_keys.items():
                require(
                    contract.get(key) == value,
                    f"{entry} must require {script}:{key}={value}, got {contract.get(key)!r}",
                )

    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        output = cached
    else:
        result = subprocess.run(
            [sys.executable, "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        require(result.returncode == 0, result.stdout.strip())
        output = result.stdout
    values = parse_kv_output(output)
    for key in [
        "real_source_records",
        "valid_source_records",
        "formal_confirmation_files",
        "runtime_primary_key_ready",
        "review_queue",
        "runtime_intake",
        "waes_review",
        "verified",
    ]:
        require(values.get(key) == "0", f"aggregate output must keep {key}=0")
    require(values.get("manual_business_verification_pending") == "true", "manual verification must remain pending")
    require(values.get("status_ceiling") == "repair_required", "status ceiling must remain repair_required")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        require(values.get(key) == "false", f"{key} must remain false")

    print(
        "gfis_real_fact_entry_coverage=pass "
        f"covered_entries={len(REQUIRED_ENTRY_COVERAGE)} "
        "real_source_record=0 equivalent_formal_confirmation_file=0 "
        "manual_business_verification=pending runtime_primary_key=0 "
        "review_queue=0 runtime_intake=0 waes_review=0 verified_artifact=0 "
        "status_ceiling=repair_required "
        "accepted=false integrated=false production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
