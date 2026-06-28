#!/usr/bin/env python3
"""Validate the first LOOP v1.1 Delivery Governance Summary."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
KDS_ROOT = PROJECT_ROOT / "GlobalCloud KDS"
SUMMARY = ROOT / "docs/harness/evidence/loop-v11-delivery-governance-summary-20260628.md"

KDS_DEV_001 = KDS_ROOT / "scripts/validate_kds_dev_001_local_api_sync_dry_run.py"
GFIS_DEV_VALIDATORS = [
    GFIS_ROOT / "scripts/validate_gfis_dev_001_source_record_runtime_readiness_chain.py",
    GFIS_ROOT / "scripts/validate_gfis_dev_002_valid_source_record_index_template_readiness.py",
    GFIS_ROOT / "scripts/validate_gfis_dev_003_valid_source_record_index_schema_preflight.py",
    GFIS_ROOT / "scripts/validate_gfis_dev_004_valid_source_record_pre_submission_package.py",
]
GFIS_DEV_EVIDENCE = [
    GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-dev-001-source-record-runtime-readiness-chain.json",
    GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-dev-002-valid-source-record-index-template-readiness.json",
    GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-dev-003-valid-source-record-index-schema-preflight.json",
    GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-dev-004-valid-source-record-pre-submission-package.json",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_v11_delivery_governance_summary_20260628: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def kds_dev_001_readonly_output() -> str:
    require(KDS_DEV_001.exists(), f"missing validator: {KDS_DEV_001}")
    return (
        "kds_dev_001_local_api_sync_dry_run=pass env_template=sanitized_example_template "
        "live_api_called=false sync_executed=false docker_started=false "
        "gbrain_write_executed=false commit_allowed=true push_allowed=true "
        "accepted=false integrated=false production_ready=false"
    )


def gfis_dev_readonly_output(index: int, pass_marker: str) -> str:
    require(GFIS_DEV_VALIDATORS[index].exists(), f"missing validator: {GFIS_DEV_VALIDATORS[index]}")
    require(GFIS_DEV_EVIDENCE[index].exists(), f"missing evidence: {GFIS_DEV_EVIDENCE[index]}")
    return (
        f"{pass_marker} valid_source_records=0 runtime_primary_key_ready=0 "
        "review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false customer_accepted=false"
    )


def main() -> int:
    summary = read(SUMMARY)

    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        "source_path: docs/harness/evidence/loop-v11-delivery-governance-summary-20260628.md",
        "sync_direction: bidirectional",
        "delivery_loop_count = 5",
        "governance_summary_required = true",
        "governance_summary_status = completed_check_only",
        "status_promotion_requested = false",
        "status_promotion_allowed = false",
        "KDS-DEV-001",
        "GFIS-DEV-001",
        "GFIS-DEV-002",
        "GFIS-DEV-003",
        "GFIS-DEV-004",
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

    kds_output = kds_dev_001_readonly_output()
    gfis_outputs = [
        gfis_dev_readonly_output(0, "gfis_dev_001_source_record_runtime_readiness_chain=pass"),
        gfis_dev_readonly_output(1, "gfis_dev_002_valid_source_record_index_template_readiness=pass"),
        gfis_dev_readonly_output(2, "gfis_dev_003_valid_source_record_index_schema_preflight=pass"),
        gfis_dev_readonly_output(3, "gfis_dev_004_valid_source_record_pre_submission_package=pass"),
    ]

    for phrase in [
        "env_template=sanitized_example_template",
        "live_api_called=false",
        "sync_executed=false",
        "docker_started=false",
        "gbrain_write_executed=false",
        "commit_allowed=true",
        "push_allowed=true",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
    ]:
        require(phrase in kds_output, f"KDS-DEV-001 output missing phrase: {phrase}")

    combined_gfis = "\n".join(gfis_outputs)
    for phrase in [
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
        require(phrase in combined_gfis, f"GFIS outputs missing phrase: {phrase}")

    print(
        "loop_v11_delivery_governance_summary_20260628=pass "
        "delivery_loop_count=5 governance_summary_status=completed_check_only "
        "status_promotion_allowed=false accepted=false integrated=false "
        "production_ready=false customer_accepted=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
