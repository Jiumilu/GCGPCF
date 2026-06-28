#!/usr/bin/env python3
"""Validate that GFIS real-fact entry remains blocked while real inputs are zero.

This is a GPCF-side aggregation gate. It does not create GFIS facts, KDS facts,
review items, runtime intake records, WAES reviews, or verified artifacts.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"

GFIS_VALIDATORS = [
    "validate_gfis_real_source_record_intake_gate.py",
    "validate_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py",
    "validate_gfis_pending_business_verification.py",
    "validate_gfis_runtime_primary_key_gate.py",
    "validate_gfis_review_queue_admission_gate.py",
    "validate_gfis_runtime_intake_gate.py",
    "validate_gfis_waes_review_gate.py",
    "validate_gfis_verified_artifact_gate.py",
    "validate_gfis_runtime_sop_e2e_real.py",
]

ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "real_runtime_primary_keys",
    "real_review_queue_items",
    "real_runtime_intake_items",
    "real_waes_reviews",
    "real_verified_artifacts",
]

EXPECTED_BY_VALIDATOR = {
    "validate_gfis_real_source_record_intake_gate.py": {
        "real_source_records": "0",
        "real_runtime_primary_keys": "0",
        "real_review_queue_items": "0",
        "real_runtime_intake_items": "0",
        "real_waes_reviews": "0",
        "real_verified_artifacts": "0",
    },
    "validate_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py": {
        "formal": "0",
        "runtime_sop_e2e": "repair_required",
    },
    "validate_gfis_pending_business_verification.py": {
        "pending_business_verification_submissions": "0",
        "real_source_records": "0",
        "runtime_primary_key_ready": "0",
        "review_queue": "0",
        "runtime_intake": "0",
        "waes_review": "0",
        "verified": "0",
    },
    "validate_gfis_runtime_primary_key_gate.py": {
        "valid_source_records": "0",
        "runtime_primary_key_ready": "0",
        "real_runtime_primary_keys": "0",
        "review_queue": "0",
        "runtime_intake": "0",
        "waes_review": "0",
        "verified": "0",
    },
    "validate_gfis_review_queue_admission_gate.py": {
        "runtime_primary_key_ready": "0",
        "review_queue": "0",
        "runtime_intake": "0",
        "waes_review": "0",
        "verified": "0",
    },
    "validate_gfis_runtime_intake_gate.py": {
        "review_queue": "0",
        "runtime_intake": "0",
        "waes_review": "0",
        "verified": "0",
    },
    "validate_gfis_waes_review_gate.py": {
        "runtime_intake": "0",
        "waes_review": "0",
        "verified": "0",
    },
    "validate_gfis_verified_artifact_gate.py": {
        "waes_review": "0",
        "verified": "0",
    },
    "validate_gfis_runtime_sop_e2e_real.py": {
        "gfis_runtime_sop_e2e_real": "repair_required",
        "synthetic_rejected_by_real_lane": "1",
        "real_source_records": "0",
        "real_runtime_primary_keys": "0",
        "real_review_queue_items": "0",
        "real_runtime_intake_items": "0",
        "real_waes_reviews": "0",
        "real_verified_artifacts": "0",
    },
}

STATUS_DOCS = [
    ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md",
    ROOT / "09-status/gpcf-project-status-matrix.md",
    ROOT / "09-status/globalcloud-project-implementation-control-register.md",
    ROOT / "docs/harness/loop-state.md",
]

STATUS_BOUNDARY_PHRASES = [
    "real_source_records=0",
    "valid_source_records=0",
    "formal_confirmation_files=0",
    "development_lane=continue_allowed",
    "real_business_validation_lane=pending_source_of_record",
    "real_source_records_zero_is_not_dev_blocker=true",
    "real_business_lane=repair_required",
    "runtime_primary_key_ready=0",
    "review_queue=0",
    "runtime_intake=0",
    "waes_review=0",
    "verified=0",
    "accepted=false",
    "integrated=false",
    "production_ready=false",
    "customer_accepted=false",
]

GPCF_READONLY_PATHS = [
    "tools/kds-sync/validate_gfis_real_fact_entry_gate.py",
    "tools/kds-sync/loop_document_gate.py",
]

GFIS_DEV_DRY_RUN_RESULT = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dev-dry-run-result.json"
GFIS_REAL_INTAKE_DIRS = [
    GFIS_ROOT / "docs/harness/sop-e2e/intake",
    GFIS_ROOT / "docs/harness/sop-e2e/intake-submissions",
    GFIS_ROOT / "docs/harness/sop-e2e/submissions",
]
GFIS_SYNTHETIC_TOKENS = ["SYN-GFIS-DEV-", "synthetic_dev_lane"]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_gfis_real_fact_entry_gate: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run_gfis_validator(script_name: str) -> str:
    script = GFIS_ROOT / "scripts" / script_name
    require(script.exists(), f"missing GFIS validator: {script}")
    try:
        result = subprocess.run(
            ["python3", str(script.relative_to(GFIS_ROOT))],
            cwd=GFIS_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        fail(f"GFIS validator timed out: {script_name}\n{output}")
    require(result.returncode == 0, f"GFIS validator failed: {script_name}\n{result.stdout}")
    output = result.stdout.strip()
    require(output, f"GFIS validator produced no output: {script_name}")
    return output


def load_gfis_json(path: Path) -> dict[str, object]:
    require(path.exists(), f"missing GFIS evidence: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"GFIS evidence must be JSON object: {path}")
    return data


def scan_gfis_real_intake_pollution() -> list[str]:
    polluted: list[str] = []
    for directory in GFIS_REAL_INTAKE_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix not in {".json", ".md", ".txt", ".yaml", ".yml"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(token in text for token in GFIS_SYNTHETIC_TOKENS):
                polluted.append(str(path.relative_to(GFIS_ROOT)))
    return polluted


def validate_runtime_sop_e2e_real_readonly() -> str:
    result = load_gfis_json(GFIS_DEV_DRY_RUN_RESULT)
    counts = result.get("counts")
    require(isinstance(counts, dict), "GFIS dev dry-run counts must be object")
    require(result.get("real_business_lane") == "repair_required", "GFIS real business lane must remain repair_required")
    require(result.get("runtime_sop_e2e_real") == "repair_required", "GFIS real runtime SOP must remain repair_required")
    for key in [
        "real_source_records",
        "real_runtime_primary_keys",
        "real_review_queue_items",
        "real_runtime_intake_items",
        "real_waes_reviews",
        "real_verified_artifacts",
        "real_kds_writes",
        "real_waes_writes",
        "production_writes",
        "real_external_api_writes",
    ]:
        require(counts.get(key) == 0, f"GFIS real count must remain 0: {key}")
    polluted = scan_gfis_real_intake_pollution()
    require(not polluted, "synthetic data leaked into real intake dirs: " + ", ".join(polluted))
    return (
        "gfis_runtime_sop_e2e_real=repair_required "
        "synthetic_rejected_by_real_lane=1 synthetic_pollution_files=0 "
        "real_source_records=0 real_runtime_primary_keys=0 real_review_queue_items=0 "
        "real_runtime_intake_items=0 real_waes_reviews=0 real_verified_artifacts=0"
    )


def git_status_snapshot(path: Path, pathspecs: list[str] | None = None) -> str:
    command = ["git", "status", "--porcelain"]
    if pathspecs:
        command.extend(["--", *pathspecs])
    result = subprocess.run(
        command,
        cwd=path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    require(result.returncode == 0, f"git status failed for {path}: {result.stdout}")
    return result.stdout


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def run_self_test() -> int:
    sample = parse_kv_output(
        "gate=pass invalid_source_records=0 real_source_records=0 "
        "valid_source_records=1 runtime_primary_key_ready=0"
    )
    require(sample.get("real_source_records") == "0", "self-test failed real_source_records parse")
    require(sample.get("valid_source_records") == "1", "self-test failed exact valid_source_records parse")
    require("invalid_source_records" in sample, "self-test failed invalid_source_records parse")
    require(
        sample.get("valid_source_records") != sample.get("invalid_source_records"),
        "self-test failed to distinguish valid_source_records from invalid_source_records",
    )
    print("gfis_real_fact_entry_gate_self_test=pass exact_key_parser=true")
    return 0


def require_expected_values(script: str, parsed: dict[str, str]) -> None:
    expected = EXPECTED_BY_VALIDATOR.get(script, {})
    require(expected, f"missing expected-key contract for GFIS validator: {script}")
    for key, value in expected.items():
        require(
            parsed.get(key) == value,
            f"{script} must report {key}={value}, got {parsed.get(key)!r}",
        )


def read_status_text() -> str:
    missing = [path.relative_to(ROOT).as_posix() for path in STATUS_DOCS if not path.exists()]
    require(not missing, "missing status documents: " + ", ".join(missing))
    return "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in STATUS_DOCS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run parser self-test only")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()

    gpcf_status_before = git_status_snapshot(ROOT, GPCF_READONLY_PATHS)
    gfis_status_before = git_status_snapshot(GFIS_ROOT)

    outputs = {
        script: (
            validate_runtime_sop_e2e_real_readonly()
            if script == "validate_gfis_runtime_sop_e2e_real.py"
            else run_gfis_validator(script)
        )
        for script in GFIS_VALIDATORS
    }

    require(
        git_status_snapshot(ROOT, GPCF_READONLY_PATHS) == gpcf_status_before,
        "GPCF real-fact entry gate files changed while running validator",
    )
    require(
        git_status_snapshot(GFIS_ROOT) == gfis_status_before,
        "GFIS worktree changed while running real-fact entry gate",
    )

    parsed_outputs = {script: parse_kv_output(output) for script, output in outputs.items()}
    merged_values: dict[str, set[str]] = {}
    for parsed in parsed_outputs.values():
        for key, value in parsed.items():
            merged_values.setdefault(key, set()).add(value)

    for script, output in outputs.items():
        parsed = parsed_outputs[script]
        require_expected_values(script, parsed)
        if script == "validate_gfis_runtime_sop_e2e_real.py":
            require(
                parsed.get("gfis_runtime_sop_e2e_real") == "repair_required",
                "real runtime SOP must remain repair_required while real facts are zero",
            )
        elif script == "validate_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py":
            require(parsed.get("formal") == "0", "formal confirmation candidates must remain zero")
            require(
                parsed.get("runtime_sop_e2e") == "repair_required",
                "formal confirmation candidate scan must keep runtime SOP repair_required",
            )
        else:
            first_key = output.split()[0].split("=", 1)[0]
            require(parsed.get(first_key) == "pass", f"blocking gate must pass structurally: {script}")
            require(
                parsed.get("real_business_lane") == "repair_required",
                f"GFIS gate must preserve repair_required: {script}",
            )
            require(
                parsed.get("business_verification_pending") == "true",
                f"GFIS gate must preserve pending manual/business verification: {script}",
            )

    for key in ZERO_KEYS:
        require("0" in merged_values.get(key, set()), f"GFIS validator output missing exact zero key: {key}=0")

    require(
        parsed_outputs["validate_gfis_runtime_sop_e2e_real.py"].get("synthetic_rejected_by_real_lane") == "1",
        "real lane must continue rejecting synthetic/dev-only evidence",
    )
    require(
        parsed_outputs["validate_gfis_liaoning_yuanhang_quotation_confirmation_candidates.py"].get("formal") == "0",
        "formal confirmation candidates must remain zero",
    )

    status_text = read_status_text()
    for phrase in STATUS_BOUNDARY_PHRASES:
        require(phrase in status_text, f"status control documents missing boundary phrase: {phrase}")

    for forbidden_claim in [
        "accepted=true",
        "integrated=true",
        "production_ready=true",
        "customer_accepted=true",
    ]:
        require(forbidden_claim not in status_text, f"forbidden status claim present: {forbidden_claim}")

    print(
        "gfis_real_fact_entry_gate=pass strong_block=true "
        "read_only_verified=true "
        "development_lane=continue_allowed "
        "real_business_validation_lane=pending_source_of_record "
        "real_source_records_zero_is_not_dev_blocker=true "
        "real_business_validation_block=true status_promotion_block=true "
        "real_source_records=0 valid_source_records=0 formal_confirmation_files=0 runtime_primary_key_ready=0 "
        "review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "manual_business_verification_pending=true real_business_lane=repair_required "
        "status_ceiling=repair_required "
        "next_required_input=real_source_record_or_equivalent_formal_confirmation "
        "accepted=false integrated=false production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
