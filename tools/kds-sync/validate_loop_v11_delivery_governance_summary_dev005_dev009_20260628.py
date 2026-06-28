#!/usr/bin/env python3
"""Validate the GFIS DEV-005..DEV-009 LOOP v1.1 Delivery Governance Summary."""

from __future__ import annotations

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
SUMMARY = ROOT / "docs/harness/evidence/loop-v11-delivery-governance-summary-dev005-dev009-20260628.md"

GFIS_DEV_VALIDATORS = [
    GFIS_ROOT / "scripts/validate_gfis_dev_005_source_record_owner_submission_handoff_readiness.py",
    GFIS_ROOT / "scripts/validate_gfis_dev_006_external_candidate_handoff_dry_run.py",
    GFIS_ROOT / "scripts/validate_gfis_dev_007_external_candidate_dir_handoff_dry_run.py",
    GFIS_ROOT / "scripts/validate_gfis_dev_008_external_candidate_dir_remediation_summary.py",
    GFIS_ROOT / "scripts/validate_gfis_dev_009_external_candidate_dir_manual_submission_manifest.py",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_v11_delivery_governance_summary_dev005_dev009_20260628: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def run_validator(path: Path, pass_marker: str) -> str:
    require(path.exists(), f"missing validator: {path}")
    result = subprocess.run(
        ["python3", str(path.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"validator failed: {path.name}: {output}")
    require(pass_marker in output, f"missing pass marker {pass_marker}: {output}")
    return output


def main() -> int:
    summary = read(SUMMARY)

    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        "source_path: docs/harness/evidence/loop-v11-delivery-governance-summary-dev005-dev009-20260628.md",
        "sync_direction: bidirectional",
        "delivery_loop_count = 5",
        "governance_summary_required = true",
        "governance_summary_status = completed_check_only",
        "status_promotion_requested = false",
        "status_promotion_allowed = false",
        "GFIS-DEV-005",
        "GFIS-DEV-006",
        "GFIS-DEV-007",
        "GFIS-DEV-008",
        "GFIS-DEV-009",
        "production_write_executed=false",
        "real_external_api_write_executed=false",
        "schema_migrate_executed=false",
        "bench_migrate_executed=false",
        "deploy_executed=false",
        "commit_executed=false",
        "push_executed=false",
        "real_kds_api_write_executed=false",
        "waes_write_executed=false",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
    ]:
        require(phrase in summary, f"summary missing phrase: {phrase}")

    outputs = [
        run_validator(
            GFIS_DEV_VALIDATORS[0],
            "gfis_dev_005_source_record_owner_submission_handoff_readiness=pass",
        ),
        run_validator(
            GFIS_DEV_VALIDATORS[1],
            "gfis_dev_006_external_candidate_handoff_dry_run=pass",
        ),
        run_validator(
            GFIS_DEV_VALIDATORS[2],
            "gfis_dev_007_external_candidate_dir_handoff_dry_run=pass",
        ),
        run_validator(
            GFIS_DEV_VALIDATORS[3],
            "gfis_dev_008_external_candidate_dir_remediation_summary=pass",
        ),
        run_validator(
            GFIS_DEV_VALIDATORS[4],
            "gfis_dev_009_external_candidate_dir_manual_submission_manifest=pass",
        ),
    ]

    combined = "\n".join(outputs)
    for phrase in [
        "real_target_files=0",
        "source_record_files_found=0",
        "valid_source_records=0",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
    ]:
        require(phrase in combined, f"GFIS outputs missing phrase: {phrase}")

    print(
        "loop_v11_delivery_governance_summary_dev005_dev009_20260628=pass "
        "delivery_loop_count=5 governance_summary_status=completed_check_only "
        "status_promotion_allowed=false accepted=false integrated=false "
        "production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
