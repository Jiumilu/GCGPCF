#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
DEV_010_EVIDENCE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-dev-010-manual-submission-command-preview.json"
DEV_011_EVIDENCE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-dev-011-manual-execution-authorization-preflight.json"
DEV_011_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_011_manual_execution_authorization_preflight.py"
GFIS_REAL_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_runtime_sop_e2e_real.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_v11_gfis_authorization_boundary: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path} must be a JSON object")
    return value


def run_gfis_validator(path: Path, marker: str) -> str:
    require(path.exists(), f"missing validator: {path}")
    result = subprocess.run(
        ["python3", str(path.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"{path.name} failed: {output}")
    require(marker in output, f"{path.name} missing marker {marker}: {output}")
    return output


def require_false_flags(payload: dict[str, Any], context: str) -> None:
    non_claims = payload.get("non_claims")
    require(isinstance(non_claims, dict), f"{context} non_claims missing")
    for key in [
        "source_record_received",
        "valid_source_record_created",
        "candidate_copied_to_real_target",
        "manual_submission_command_executed",
        "manual_owner_review_completed",
        "runtime_primary_key_created",
        "review_queue_created",
        "runtime_intake_created",
        "waes_review_created",
        "verified_artifact_created",
        "accepted",
        "integrated",
        "production_ready",
        "customer_accepted",
        "production_write",
        "real_external_api_write",
        "real_kds_write",
        "real_waes_write",
        "schema_migrate",
        "bench_migrate",
        "commit",
        "push",
        "deploy",
    ]:
        require(non_claims.get(key) is False, f"{context} non_claims.{key} must be false")


def main() -> int:
    dev_010 = load_json(DEV_010_EVIDENCE)
    dev_011 = load_json(DEV_011_EVIDENCE)
    dev_011_output = run_gfis_validator(
        DEV_011_VALIDATOR,
        "gfis_dev_011_manual_execution_authorization_preflight=pass",
    )
    gfis_real_output = run_gfis_validator(
        GFIS_REAL_VALIDATOR,
        "gfis_runtime_sop_e2e_real=repair_required",
    )

    require(dev_010.get("manual_submission_command_preview_supported") is True, "DEV-010 command preview support missing")
    require(dev_010.get("command_execution_allowed") is False, "DEV-010 script command execution must be disallowed")
    require(dev_010.get("candidate_dir_must_remain_outside_real_intake") is True, "DEV-010 external candidate boundary missing")
    require_false_flags(dev_010, "DEV-010")

    require(dev_011.get("manual_execution_authorization_preflight_supported") is True, "DEV-011 authorization preflight support missing")
    require(dev_011.get("authorization_template_preview_supported") is True, "DEV-011 authorization template support missing")
    require(dev_011.get("post_submit_verification_plan_supported") is True, "DEV-011 post-submit plan support missing")
    require(dev_011.get("command_execution_allowed_for_script") is False, "DEV-011 script command execution must be disallowed")
    require(dev_011.get("candidate_dir_must_remain_outside_real_intake") is True, "DEV-011 external candidate boundary missing")
    require_false_flags(dev_011, "DEV-011")

    counts = dev_011.get("counts")
    require(isinstance(counts, dict), "DEV-011 counts missing")
    require(counts.get("post_submit_verification_plan_commands") == 7, "post-submit verification command count mismatch")
    require(counts.get("valid_authorization_preflight_ready") == 1, "valid authorization fixture must pass")
    require(counts.get("unchanged_template_preflight_ready") == 0, "unchanged authorization template must not pass")

    for phrase in [
        "authorization_template_preview_supported=true",
        "post_submit_verification_plan_supported=true",
        "post_submit_verification_plan_commands=7",
        "command_executed=false",
        "copy_to_real_target_executed=false",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
    ]:
        require(phrase in dev_011_output, f"DEV-011 output missing phrase: {phrase}")

    for phrase in [
        "real_source_records=0",
        "real_runtime_primary_keys=0",
        "real_review_queue_items=0",
        "real_runtime_intake_items=0",
        "real_waes_reviews=0",
        "real_verified_artifacts=0",
    ]:
        require(phrase in gfis_real_output, f"GFIS real output missing phrase: {phrase}")

    print(
        "loop_v11_gfis_authorization_boundary=pass "
        "dev010_command_preview=ready_no_execute "
        "dev011_authorization_preflight=ready_no_execute "
        "authorization_template_requires_human_confirmation=true "
        "post_submit_verification_plan_commands=7 "
        "manual_submission_executed=false real_target_files=0 "
        "valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 "
        "runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
