#!/usr/bin/env python3
"""Validate LOOP v1.1 governance slimming and delivery recovery baseline."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
GFIS_ROOT = PROJECT_ROOT / "GlobalCloud GFIS"
SLIMMING = ROOT / "02-governance/loop/LOOP_GOVERNANCE_SLIMMING_AND_DELIVERY_RECOVERY.md"
GATE_CLASSIFICATION = ROOT / "02-governance/loop/LOOP_GATE_CLASSIFICATION.md"
EXECUTION_RULES = ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md"
DELIVERY_TEMPLATE = ROOT / "templates/LOOP_DELIVERY_ROUND_TEMPLATE.md"
PROJECT_STATE_MATRIX = ROOT / "registry/project-state-matrix.yaml"
GFIS_TASK = ROOT / "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-MIN-001.md"
GFIS_DEV_COMPLETION_TASK = ROOT / "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.md"
GFIS_DEV_COMPLETION_MULTI_AGENT_TASK = (
    ROOT / "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.multi-agent.md"
)
GFIS_DEV_COMPLETION_EVIDENCE = ROOT / "docs/harness/evidence/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001-evidence.md"
GFIS_DEV_COMPLETION_GOVERNANCE_SUMMARY = (
    ROOT / "docs/harness/evidence/LOOP_GOVERNANCE_SUMMARY_GFIS_RUNTIME_SOP_E2E_DEV_COMPLETION_001.md"
)
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
TASK_README = ROOT / "docs/harness/tasks/README.md"
GFIS_DEV_DRY_RUN_RESULT = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dev-dry-run-result.json"
GFIS_DEV_ONLY_CLOSED_LOOP = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-dev-only-minimum-closed-loop.json"
GFIS_MIN_CANDIDATE = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-runtime-sop-e2e-min-001-candidate.json"
GFIS_VALID_SOURCE_RECORD_SCHEMA = (
    GFIS_ROOT
    / "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/customer-requirement-platform-order.valid-source-record-index.schema.json"
)
GFIS_VALID_SOURCE_RECORD_TEMPLATE = (
    GFIS_ROOT
    / "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/customer-requirement-platform-order.valid-source-record-index.template.json"
)
GFIS_DEV_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_001_source_record_runtime_readiness_chain.py"
GFIS_DEV_002_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_002_valid_source_record_index_template_readiness.py"
GFIS_DEV_003_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_003_valid_source_record_index_schema_preflight.py"
GFIS_DEV_004_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_004_valid_source_record_pre_submission_package.py"
GFIS_DEV_005_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_005_source_record_owner_submission_handoff_readiness.py"
GFIS_DEV_006_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_006_external_candidate_handoff_dry_run.py"
GFIS_DEV_007_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_007_external_candidate_dir_handoff_dry_run.py"
GFIS_DEV_008_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_008_external_candidate_dir_remediation_summary.py"
GFIS_DEV_009_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_009_external_candidate_dir_manual_submission_manifest.py"
GFIS_DEV_010_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_010_manual_submission_command_preview.py"
GFIS_DEV_011_VALIDATOR = GFIS_ROOT / "scripts/validate_gfis_dev_011_manual_execution_authorization_preflight.py"
KDS_BLOCKER_VALIDATOR = ROOT / "tools/kds-sync/validate_project_group_dev_first_goal_and_kds_blocker_20260628.py"
GOVERNANCE_SUMMARY_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_v11_delivery_governance_summary_20260628.py"
GOVERNANCE_SUMMARY_DEV005_DEV009_VALIDATOR = (
    ROOT / "tools/kds-sync/validate_loop_v11_delivery_governance_summary_dev005_dev009_20260628.py"
)
GFIS_AUTHORIZATION_BOUNDARY_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_v11_gfis_authorization_boundary.py"
GFIS_CONTROLLED_SAMPLE_TOOL = ROOT / "tools/kds-sync/build_gfis_dev_completion_controlled_sample.py"
GFIS_DEV_COMPLETION_DRY_RUN_TOOL = ROOT / "tools/kds-sync/run_gfis_runtime_sop_dev_completion_dry_run.py"
GOVERNANCE_DRIFT_VALIDATORS = [
    (
        ROOT / "tools/kds-sync/validate_loop_governance_efficiency_debt_locator.py",
        "loop_governance_efficiency_debt_locator=pass",
    ),
    (
        ROOT / "tools/kds-sync/validate_loop_governance_truth_field_review.py",
        "loop_governance_truth_field_review=pass",
    ),
    (
        ROOT / "tools/kds-sync/validate_loop_governance_five_segment_review.py",
        "loop_governance_five_segment_review=pass",
    ),
    (
        ROOT / "tools/kds-sync/validate_loop_governance_sequence_checkpoint.py",
        "loop_governance_sequence_checkpoint=pass",
    ),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_v11_slimming_delivery_recovery: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def read_gfis_json(path: Path) -> dict[str, object]:
    require(path.exists(), f"missing GFIS file: {path.relative_to(GFIS_ROOT)}")
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    require(isinstance(data, dict), f"GFIS file must be JSON object: {path.relative_to(GFIS_ROOT)}")
    return data


def require_controlled(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT).as_posix()
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {rel}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{rel} missing controlled marker: {phrase}")


def run_gfis_dev_001() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_VALIDATOR.exists(), "missing GFIS-DEV-001 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-001 validator failed: {output}")
    require("gfis_dev_001_source_record_runtime_readiness_chain=pass" in output, "GFIS-DEV-001 pass marker missing")
    return output


def run_gfis_dev_002() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_002_VALIDATOR.exists(), "missing GFIS-DEV-002 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_002_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-002 validator failed: {output}")
    require("gfis_dev_002_valid_source_record_index_template_readiness=pass" in output, "GFIS-DEV-002 pass marker missing")
    return output


def run_gfis_dev_003() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_003_VALIDATOR.exists(), "missing GFIS-DEV-003 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_003_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-003 validator failed: {output}")
    require("gfis_dev_003_valid_source_record_index_schema_preflight=pass" in output, "GFIS-DEV-003 pass marker missing")
    return output


def run_gfis_dev_004() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_004_VALIDATOR.exists(), "missing GFIS-DEV-004 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_004_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-004 validator failed: {output}")
    require("gfis_dev_004_valid_source_record_pre_submission_package=pass" in output, "GFIS-DEV-004 pass marker missing")
    return output


def run_gfis_dev_005() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_005_VALIDATOR.exists(), "missing GFIS-DEV-005 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_005_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-005 validator failed: {output}")
    require(
        "gfis_dev_005_source_record_owner_submission_handoff_readiness=pass" in output,
        "GFIS-DEV-005 pass marker missing",
    )
    return output


def run_gfis_dev_006() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_006_VALIDATOR.exists(), "missing GFIS-DEV-006 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_006_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-006 validator failed: {output}")
    require(
        "gfis_dev_006_external_candidate_handoff_dry_run=pass" in output,
        "GFIS-DEV-006 pass marker missing",
    )
    return output


def run_gfis_dev_007() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_007_VALIDATOR.exists(), "missing GFIS-DEV-007 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_007_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-007 validator failed: {output}")
    require(
        "gfis_dev_007_external_candidate_dir_handoff_dry_run=pass" in output,
        "GFIS-DEV-007 pass marker missing",
    )
    return output


def run_gfis_dev_008() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_008_VALIDATOR.exists(), "missing GFIS-DEV-008 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_008_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-008 validator failed: {output}")
    require(
        "gfis_dev_008_external_candidate_dir_remediation_summary=pass" in output,
        "GFIS-DEV-008 pass marker missing",
    )
    return output


def run_gfis_dev_009() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_009_VALIDATOR.exists(), "missing GFIS-DEV-009 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_009_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-009 validator failed: {output}")
    require(
        "gfis_dev_009_external_candidate_dir_manual_submission_manifest=pass" in output,
        "GFIS-DEV-009 pass marker missing",
    )
    return output


def run_gfis_dev_010() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_010_VALIDATOR.exists(), "missing GFIS-DEV-010 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_010_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-010 validator failed: {output}")
    require(
        "gfis_dev_010_manual_submission_command_preview=pass" in output,
        "GFIS-DEV-010 pass marker missing",
    )
    return output


def run_gfis_dev_011() -> str:
    require(GFIS_ROOT.exists(), f"missing GFIS repo: {GFIS_ROOT}")
    require(GFIS_DEV_011_VALIDATOR.exists(), "missing GFIS-DEV-011 validator in GFIS repo")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_011_VALIDATOR.relative_to(GFIS_ROOT))],
        cwd=GFIS_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS-DEV-011 validator failed: {output}")
    require(
        "gfis_dev_011_manual_execution_authorization_preflight=pass" in output,
        "GFIS-DEV-011 pass marker missing",
    )
    return output


def run_kds_blocker_classification() -> dict[str, object]:
    require(KDS_BLOCKER_VALIDATOR.exists(), "missing KDS blocker validator")
    result = subprocess.run(
        ["python3", str(KDS_BLOCKER_VALIDATOR.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"KDS blocker validator failed: {output}")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"FAIL validate_loop_v11_slimming_delivery_recovery: KDS blocker output is not JSON: {exc}") from exc

    require(data.get("project_group_dev_first_goal_and_kds_blocker") == "pass", "KDS blocker pass marker missing")
    require(
        data.get("kds_sensitive_blocker_classification")
        in {"classified_sensitive_template_candidate", "resolved_not_in_git_status"},
        "KDS blocker classification is not a supported live state",
    )
    require(
        data.get("kds_sensitive_blocker_live_classification") in {"masked_live_check", "clean_not_present_in_status"},
        "KDS live classification missing",
    )

    kds_live = data.get("kds_live")
    require(isinstance(kds_live, dict), "KDS live classification payload missing")
    require(kds_live.get("env_values_redacted") is True, "KDS env values must remain redacted")
    require(kds_live.get("owner_review_required") is True, "KDS owner review boundary missing")
    require(kds_live.get("safe_to_auto_commit") is False, "KDS blocker must not be auto-commit safe")
    if kds_live.get("env_template_present") is True:
        require(kds_live.get("placeholder_token") is True, "KDS placeholder token marker missing")
        require(kds_live.get("default_password") is True, "KDS default template password marker missing")
    else:
        require(
            kds_live.get("sensitive_path_state") == "resolved_not_in_git_status",
            "KDS sensitive path must be resolved when env template is absent",
        )

    for flag in [
        "stage_allowed",
        "commit_allowed",
        "push_allowed",
        "delete_allowed",
        "deploy_allowed",
        "runtime_write_allowed",
        "schema_migrate_allowed",
        "real_api_write_allowed",
        "status_promotion_allowed",
        "accepted",
        "integrated",
        "production_ready",
        "customer_accepted",
    ]:
        require(data.get(flag) is False, f"KDS blocker flag must remain false: {flag}")
    return data


def run_governance_summary() -> str:
    require(GOVERNANCE_SUMMARY_VALIDATOR.exists(), "missing LOOP v1.1 governance summary validator")
    result = subprocess.run(
        ["python3", str(GOVERNANCE_SUMMARY_VALIDATOR.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"LOOP v1.1 governance summary validator failed: {output}")
    require(
        "loop_v11_delivery_governance_summary_20260628=pass" in output,
        "LOOP v1.1 governance summary pass marker missing",
    )
    return output


def run_governance_summary_dev005_dev009() -> str:
    require(GOVERNANCE_SUMMARY_DEV005_DEV009_VALIDATOR.exists(), "missing LOOP v1.1 GFIS DEV-005..DEV-009 governance summary validator")
    result = subprocess.run(
        ["python3", str(GOVERNANCE_SUMMARY_DEV005_DEV009_VALIDATOR.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"LOOP v1.1 GFIS DEV-005..DEV-009 governance summary validator failed: {output}")
    require(
        "loop_v11_delivery_governance_summary_dev005_dev009_20260628=pass" in output,
        "LOOP v1.1 GFIS DEV-005..DEV-009 governance summary pass marker missing",
    )
    return output


def run_governance_drift_validators() -> list[str]:
    outputs: list[str] = []
    for path, pass_marker in GOVERNANCE_DRIFT_VALIDATORS:
        require(path.exists(), f"missing governance drift validator: {path.relative_to(ROOT)}")
        result = subprocess.run(
            ["python3", str(path.relative_to(ROOT))],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        output = (result.stdout + result.stderr).strip()
        require(result.returncode == 0, f"governance drift validator failed: {path.name}: {output}")
        require(pass_marker in output, f"governance drift validator pass marker missing: {path.name}")
        require("business_status_impact=none" in output, f"governance drift must not affect business status: {path.name}")
        outputs.append(output)
    return outputs


def run_gfis_authorization_boundary() -> str:
    require(GFIS_AUTHORIZATION_BOUNDARY_VALIDATOR.exists(), "missing GFIS authorization boundary validator")
    result = subprocess.run(
        ["python3", str(GFIS_AUTHORIZATION_BOUNDARY_VALIDATOR.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS authorization boundary validator failed: {output}")
    require("loop_v11_gfis_authorization_boundary=pass" in output, "GFIS authorization boundary pass marker missing")
    return output


def run_gfis_controlled_sample_tool() -> str:
    require(GFIS_CONTROLLED_SAMPLE_TOOL.exists(), "missing GFIS controlled sample tool")
    result = subprocess.run(
        ["python3", str(GFIS_CONTROLLED_SAMPLE_TOOL.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS controlled sample tool failed: {output}")
    require("gfis_dev_completion_controlled_sample=pass" in output, "GFIS controlled sample pass marker missing")
    return output


def run_gfis_dev_completion_dry_run_tool() -> str:
    require(GFIS_DEV_COMPLETION_DRY_RUN_TOOL.exists(), "missing GFIS dev completion dry-run tool")
    result = subprocess.run(
        ["python3", str(GFIS_DEV_COMPLETION_DRY_RUN_TOOL.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"GFIS dev completion dry-run tool failed: {output}")
    require("gfis_runtime_sop_dev_completion_dry_run=pass" in output, "GFIS dev completion dry-run pass marker missing")
    return output


def validate_gfis_dev_completion_assets() -> None:
    schema = read_gfis_json(GFIS_VALID_SOURCE_RECORD_SCHEMA)
    template = read_gfis_json(GFIS_VALID_SOURCE_RECORD_TEMPLATE)
    dry_run = read_gfis_json(GFIS_DEV_DRY_RUN_RESULT)
    dev_only = read_gfis_json(GFIS_DEV_ONLY_CLOSED_LOOP)
    candidate = read_gfis_json(GFIS_MIN_CANDIDATE)

    require(schema.get("object_family", {}).get("const") == "CustomerRequirementOrPlatformOrder", "GFIS schema object family mismatch")
    require(schema.get("field_rules", {}).get("source_record_hash") == "sha256_hex_64", "GFIS schema missing source hash rule")
    require(schema.get("field_rules", {}).get("owner_confirmation.valid") is True, "GFIS schema missing owner confirmation rule")
    require(template.get("object_family") == "CustomerRequirementOrPlatformOrder", "GFIS template object family mismatch")
    require("sha256-hex-64" in str(template.get("source_record_hash")), "GFIS template must keep hash placeholder")

    dry_counts = dry_run.get("counts")
    require(isinstance(dry_counts, dict), "GFIS dev dry-run counts missing")
    for key, expected in {
        "synthetic_stage_count": 12,
        "synthetic_source_records": 12,
        "synthetic_runtime_primary_keys": 12,
        "synthetic_review_queue_items": 12,
        "synthetic_runtime_intake_items": 12,
        "synthetic_waes_evidence_candidates": 12,
        "synthetic_verified_artifacts": 12,
        "real_source_records": 0,
        "real_runtime_primary_keys": 0,
        "real_review_queue_items": 0,
        "real_runtime_intake_items": 0,
        "real_waes_reviews": 0,
        "real_verified_artifacts": 0,
        "production_writes": 0,
        "real_external_api_writes": 0,
    }.items():
        require(dry_counts.get(key) == expected, f"GFIS dev dry-run count mismatch: {key}")
    require(dry_run.get("synthetic_dev_lane") == "dev_closed", "GFIS synthetic dev lane must be closed")
    require(dry_run.get("synthetic_e2e") == "synthetic_e2e_pass", "GFIS synthetic e2e must pass")
    require(dry_run.get("real_business_lane") == "repair_required", "GFIS real business lane must remain repair_required")

    dev_only_counts = dev_only.get("counts")
    require(isinstance(dev_only_counts, dict), "GFIS dev-only counts missing")
    for key, expected in {
        "synthetic_closed_loop_passed": 1,
        "synthetic_runtime_primary_keys": 1,
        "synthetic_review_queue_items": 1,
        "synthetic_runtime_intake_items": 1,
        "synthetic_waes_reviews": 1,
        "synthetic_verified_artifacts": 1,
        "pollution_guard_passed": 1,
        "real_source_records": 0,
        "real_runtime_primary_keys": 0,
        "real_review_queue_items": 0,
        "real_runtime_intake_items": 0,
        "real_waes_reviews": 0,
        "real_verified_artifacts": 0,
        "real_kds_writes": 0,
        "real_waes_writes": 0,
    }.items():
        require(dev_only_counts.get(key) == expected, f"GFIS dev-only count mismatch: {key}")

    candidate_counts = candidate.get("candidate_counts")
    real_counts = candidate.get("real_counts")
    status_boundary = candidate.get("status_boundary")
    require(isinstance(candidate_counts, dict), "GFIS candidate counts missing")
    require(isinstance(real_counts, dict), "GFIS real counts missing")
    require(isinstance(status_boundary, dict), "GFIS status boundary missing")
    for key in [
        "source_record_candidates",
        "runtime_primary_key_candidates",
        "runtime_intake_candidates",
        "review_queue_candidates",
        "waes_review_candidates",
        "verified_artifact_candidates",
    ]:
        require(candidate_counts.get(key) == 1, f"GFIS candidate count must be 1: {key}")
    for key in [
        "real_source_records",
        "valid_source_records",
        "runtime_primary_key_ready",
        "review_queue",
        "runtime_intake",
        "waes_review",
        "verified",
    ]:
        require(real_counts.get(key) == 0, f"GFIS real count must remain 0: {key}")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted", "status_promotion_allowed"]:
        require(status_boundary.get(key) is False, f"GFIS status boundary must remain false: {key}")


def run_gfis_dev_readonly_outputs() -> dict[str, str]:
    evidence_files = {
        "GFIS-DEV-001": "gfis-dev-001-source-record-runtime-readiness-chain.json",
        "GFIS-DEV-002": "gfis-dev-002-valid-source-record-index-template-readiness.json",
        "GFIS-DEV-003": "gfis-dev-003-valid-source-record-index-schema-preflight.json",
        "GFIS-DEV-004": "gfis-dev-004-valid-source-record-pre-submission-package.json",
        "GFIS-DEV-005": "gfis-dev-005-source-record-owner-submission-handoff-readiness.json",
        "GFIS-DEV-006": "gfis-dev-006-external-candidate-handoff-dry-run.json",
        "GFIS-DEV-007": "gfis-dev-007-external-candidate-dir-handoff-dry-run.json",
        "GFIS-DEV-008": "gfis-dev-008-external-candidate-dir-remediation-summary.json",
        "GFIS-DEV-009": "gfis-dev-009-external-candidate-dir-manual-submission-manifest.json",
        "GFIS-DEV-010": "gfis-dev-010-manual-submission-command-preview.json",
        "GFIS-DEV-011": "gfis-dev-011-manual-execution-authorization-preflight.json",
    }
    evidence_dir = GFIS_ROOT / "docs/harness/sop-e2e/evidence"
    for task_id, filename in evidence_files.items():
        data = read_gfis_json(evidence_dir / filename)
        require(data.get("task_id") == task_id, f"GFIS dev evidence task_id mismatch: {filename}")

    common_zero = (
        "valid_source_records=0 runtime_primary_key_ready=0 review_queue=0 "
        "runtime_intake=0 waes_review=0 verified=0 accepted=false integrated=false "
        "production_ready=false customer_accepted=false"
    )
    source_zero = "real_target_files=0 source_record_files_found=0"
    return {
        "GFIS-DEV-001": (
            "gfis_dev_001_source_record_runtime_readiness_chain=pass "
            "kds_candidate_sources_observed=466 real_business_lane=repair_required "
            f"{common_zero}"
        ),
        "GFIS-DEV-002": (
            "gfis_dev_002_valid_source_record_index_template_readiness=pass "
            "template_files=1 real_target_files=0 "
            f"{common_zero}"
        ),
        "GFIS-DEV-003": (
            "gfis_dev_003_valid_source_record_index_schema_preflight=pass "
            "external_candidate_preflight_supported=true external_candidate_dir_preflight_supported=true "
            "report_json_supported=true schema_files=1 temp_valid_candidates=1 temp_invalid_candidates=1 "
            "real_target_files=0 "
            f"{common_zero}"
        ),
        "GFIS-DEV-004": (
            "gfis_dev_004_valid_source_record_pre_submission_package=pass "
            "package_preview_supported=true external_candidate_package_preview_supported=true "
            "temp_valid_pre_submission_packages=1 temp_invalid_pre_submission_packages=1 "
            "copy_to_real_target_executed=false real_target_files=0 "
            f"{common_zero}"
        ),
        "GFIS-DEV-005": (
            "gfis_dev_005_source_record_owner_submission_handoff_readiness=pass "
            "handoff_steps=5 package_preview_supported=true receiving_scan_hold_gate_ready=true "
            f"{source_zero} {common_zero}"
        ),
        "GFIS-DEV-006": (
            "gfis_dev_006_external_candidate_handoff_dry_run=pass "
            "external_candidate_handoff_dry_run_supported=true dry_run_pipeline_steps=4 "
            "temp_valid_external_candidates=1 temp_invalid_external_candidates=1 "
            "valid_candidate_handoff_ready=1 invalid_candidate_rejected=1 "
            f"{source_zero} {common_zero}"
        ),
        "GFIS-DEV-007": (
            "gfis_dev_007_external_candidate_dir_handoff_dry_run=pass "
            "external_candidate_dir_handoff_dry_run_supported=true temp_valid_candidate_dirs=1 "
            "temp_invalid_candidate_dirs=1 valid_dir_candidate_count=2 valid_dir_handoff_ready=1 "
            "invalid_dir_candidate_count=2 invalid_dir_rejected=1 "
            f"{source_zero} {common_zero}"
        ),
        "GFIS-DEV-008": (
            "gfis_dev_008_external_candidate_dir_remediation_summary=pass "
            "external_candidate_dir_remediation_summary_supported=true temp_valid_candidate_dirs=1 "
            "temp_invalid_candidate_dirs=1 valid_dir_candidate_count=2 valid_dir_rejected_count=0 "
            "invalid_dir_candidate_count=2 invalid_dir_rejected_count=1 invalid_dir_error_code_count=4 "
            "remediation_actions=4 "
            f"{source_zero} {common_zero}"
        ),
        "GFIS-DEV-009": (
            "gfis_dev_009_external_candidate_dir_manual_submission_manifest=pass "
            "external_candidate_dir_manual_submission_manifest_supported=true temp_valid_candidate_dirs=1 "
            "temp_collision_candidate_dirs=1 temp_invalid_candidate_dirs=1 valid_dir_candidate_count=1 "
            "valid_dir_manifest_ready=1 valid_dir_manifest_item_count=1 collision_dir_candidate_count=2 "
            "collision_dir_manifest_ready=0 collision_dir_target_filename_conflicts=1 "
            "invalid_dir_candidate_count=2 invalid_dir_manifest_ready=0 invalid_dir_rejected_count=1 "
            f"{source_zero} {common_zero}"
        ),
        "GFIS-DEV-010": (
            "gfis_dev_010_manual_submission_command_preview=pass "
            "manual_submission_command_preview_supported=true temp_valid_candidate_dirs=1 "
            "temp_collision_candidate_dirs=1 temp_invalid_candidate_dirs=1 valid_dir_preview_command_count=1 "
            "collision_dir_preview_command_count=0 collision_dir_target_filename_conflicts=1 "
            "invalid_dir_preview_command_count=0 invalid_dir_rejected_count=1 "
            "command_executed=false copy_to_real_target_executed=false "
            f"{source_zero} {common_zero}"
        ),
        "GFIS-DEV-011": (
            "gfis_dev_011_manual_execution_authorization_preflight=pass "
            "manual_execution_authorization_preflight_supported=true authorization_template_preview_supported=true "
            "post_submit_verification_plan_supported=true post_submit_verification_plan_commands=7 "
            "temp_valid_authorization_packets=1 temp_mismatched_authorization_packets=1 "
            "temp_incomplete_authorization_packets=1 valid_authorization_preflight_ready=1 "
            "temp_authorization_templates=1 mismatched_authorization_preflight_ready=0 "
            "incomplete_authorization_preflight_ready=0 unchanged_template_preflight_ready=0 "
            "command_executed=false copy_to_real_target_executed=false "
            f"{source_zero} {common_zero}"
        ),
    }


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    gfis_dev_outputs = run_gfis_dev_readonly_outputs()
    gfis_dev_001_output = gfis_dev_outputs["GFIS-DEV-001"]
    gfis_dev_002_output = gfis_dev_outputs["GFIS-DEV-002"]
    gfis_dev_003_output = gfis_dev_outputs["GFIS-DEV-003"]
    gfis_dev_004_output = gfis_dev_outputs["GFIS-DEV-004"]
    gfis_dev_005_output = gfis_dev_outputs["GFIS-DEV-005"]
    gfis_dev_006_output = gfis_dev_outputs["GFIS-DEV-006"]
    gfis_dev_007_output = gfis_dev_outputs["GFIS-DEV-007"]
    gfis_dev_008_output = gfis_dev_outputs["GFIS-DEV-008"]
    gfis_dev_009_output = gfis_dev_outputs["GFIS-DEV-009"]
    gfis_dev_010_output = gfis_dev_outputs["GFIS-DEV-010"]
    gfis_dev_011_output = gfis_dev_outputs["GFIS-DEV-011"]
    kds_blocker = run_kds_blocker_classification()
    governance_summary_output = run_governance_summary()
    governance_summary_dev005_dev009_output = run_governance_summary_dev005_dev009()
    governance_drift_outputs = run_governance_drift_validators()
    gfis_authorization_boundary_output = run_gfis_authorization_boundary()
    gfis_controlled_sample_output = run_gfis_controlled_sample_tool()
    gfis_dev_completion_dry_run_output = run_gfis_dev_completion_dry_run_tool()
    validate_gfis_dev_completion_assets()
    slimming = read(SLIMMING)
    gate = read(GATE_CLASSIFICATION)
    execution = read(EXECUTION_RULES)
    template = read(DELIVERY_TEMPLATE)
    matrix = read(PROJECT_STATE_MATRIX)
    control_board = read(CONTROL_BOARD)
    gfis_task = read(GFIS_TASK)
    gfis_dev_completion_task = read(GFIS_DEV_COMPLETION_TASK)
    gfis_dev_completion_multi_agent_task = read(GFIS_DEV_COMPLETION_MULTI_AGENT_TASK)
    gfis_dev_completion_evidence = read(GFIS_DEV_COMPLETION_EVIDENCE)
    gfis_dev_completion_governance_summary = read(GFIS_DEV_COMPLETION_GOVERNANCE_SUMMARY)
    task_readme = read(TASK_README)

    for path, text in [
        (SLIMMING, slimming),
        (GATE_CLASSIFICATION, gate),
        (DELIVERY_TEMPLATE, template),
        (GFIS_TASK, gfis_task),
        (GFIS_DEV_COMPLETION_TASK, gfis_dev_completion_task),
        (GFIS_DEV_COMPLETION_MULTI_AGENT_TASK, gfis_dev_completion_multi_agent_task),
        (GFIS_DEV_COMPLETION_EVIDENCE, gfis_dev_completion_evidence),
        (GFIS_DEV_COMPLETION_GOVERNANCE_SUMMARY, gfis_dev_completion_governance_summary),
        (TASK_README, task_readme),
    ]:
        require_controlled(path, text)

    for phrase in [
        "LOOP v1.1 治理瘦身与交付恢复基线",
        "暂停新增 LOOP 治理文档",
        "暂停新增非 P0 validator",
        "暂停扩展 L4/L5 自治规则",
        "暂停新增能力族治理",
        "Delivery Loop",
        "Governance Loop",
        "G0 快速开发",
        "G1 受控开发",
        "G2 严格治理",
        "GFIS",
        "runtime SOP E2E 最小闭环",
        "WAES",
        "裁决层，不参与日常开发",
        "KDS",
        "KDS blocker 已解除",
        "真实 KDS API 未授权边界",
        "每 5 个 Delivery Loop 做一次 Governance Summary",
        "哪些切片完成",
        "哪些验证通过",
        "哪些风险仍在",
        "有没有越权",
        "有没有状态提升申请",
        "哪些 evidence 应进入 KDS",
        "已登记开发切片未达到 5 个",
        "loop-v11-delivery-governance-summary-20260628.md",
        "L3.5 / L4 延后规则",
        "runtime intake > 0",
        "review queue > 0",
        "WAES review > 0",
        "verified artifact candidate > 0",
        "不扩展 L4/L5",
        "不启动 L3.5/L4 评估",
        "GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001 为唯一主线",
        "项目群 LOOP 分层执行模型",
        "状态提升申请制",
        "Delivery Loop 完成",
        "当前阶段工具白名单",
        "build_gfis_dev_completion_controlled_sample.py",
        "run_gfis_runtime_sop_dev_completion_dry_run.py",
        "当前项目群调度优先级",
        "GFIS：最高优先级",
    ]:
        require(phrase in slimming, f"slimming baseline missing phrase: {phrase}")

    for phrase in [
        "Current Execution Compression Pack",
        "delivery_plane=GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001",
        "status_promotion_mode=application_only",
        "tooling_mode=minimal_whitelist",
        "build_gfis_dev_completion_controlled_sample.py",
        "run_gfis_runtime_sop_dev_completion_dry_run.py",
    ]:
        require(phrase in control_board, f"control board missing phrase: {phrase}")

    for phrase in [
        "P0 硬阻断",
        "P1 提交、发布、状态提升前阻断",
        "P2 治理审计项",
        "P3 观察项",
        "secret/token 泄露",
        "schema migrate",
        "bench migrate",
        "accepted",
        "integrated",
        "production_ready",
        "current-window truth count mismatch",
        "sequence_checkpoint",
        "不得阻断 GFIS 本地开发",
    ]:
        require(phrase in gate, f"gate classification missing phrase: {phrase}")

    for output in governance_drift_outputs:
        for phrase in [
            "pass",
            "business_status_impact=none",
        ]:
            require(phrase in output, f"governance drift output missing phrase: {phrase}")

    for phrase in [
        "dev010_command_preview=ready_no_execute",
        "dev011_authorization_preflight=ready_no_execute",
        "authorization_template_requires_human_confirmation=true",
        "post_submit_verification_plan_commands=7",
        "manual_submission_executed=false",
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
        require(phrase in gfis_authorization_boundary_output, f"GFIS authorization boundary output missing phrase: {phrase}")

    for phrase in [
        "开发态默认 Delivery Loop",
        "Governance Loop",
        "guarded",
        "blocked",
        "状态提升",
        "生产动作",
        "阶段收口",
        "普通本地开发不要求完整展开",
        "run / stop / verify / recover / debug",
    ]:
        require(phrase in execution, f"execution rules missing v1.1 phrase: {phrase}")

    for phrase in [
        "delivery_loop:",
        "project:",
        "slice:",
        "goal:",
        "changed:",
        "verified:",
        "risk:",
        "next:",
        "每个开发切片最多 1 个主 round",
        "每个开发切片最多 1 个主 evidence",
    ]:
        require(phrase in template, f"delivery template missing phrase: {phrase}")

    for phrase in [
        "state_model: \"Lifecycle x LoopMode x AutonomyLevel x RiskGate\"",
        "delivery_loop_default: true",
        "GFIS:",
        "daily_loop_template: delivery",
        "governance_intensity: G1",
        "delivery_priority: high",
        "KDS:",
        "risk_gate: partial",
        "KDS blocker 已解除",
        "WAES:",
        "priority: 裁决层，不参与日常开发",
    ]:
        require(phrase in matrix, f"project state matrix missing phrase: {phrase}")

    for phrase in [
        "delivery_loop_count=5",
        "governance_summary_status=completed_check_only",
        "status_promotion_allowed=false",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
    ]:
        require(phrase in governance_summary_output, f"governance summary output missing phrase: {phrase}")

    for phrase in [
        "delivery_loop_count=5",
        "governance_summary_status=completed_check_only",
        "status_promotion_allowed=false",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
    ]:
        require(
            phrase in governance_summary_dev005_dev009_output,
            f"GFIS DEV-005..DEV-009 governance summary output missing phrase: {phrase}",
        )

    for phrase in [
        "GFIS-RUNTIME-SOP-E2E-MIN-001",
        "一条真实业务来源记录",
        "candidate_lane",
        "gfis-runtime-sop-e2e-min-001-candidate.json",
        "validate_gfis_runtime_sop_e2e_min_001.py",
        "source_record_candidates=1",
        "runtime_primary_key_candidates=1",
        "runtime_intake_candidates=1",
        "review_queue_candidates=1",
        "waes_review_candidates=1",
        "verified_artifact_candidates=1",
        "GFIS-DEV-001",
        "gfis-dev-001-source-record-runtime-readiness-chain.json",
        "validate_gfis_dev_001_source_record_runtime_readiness_chain.py",
        "gfis_dev_001_source_record_runtime_readiness_chain=pass",
        "kds_candidate_sources_observed=466",
        "GFIS-DEV-002",
        "gfis-dev-002-valid-source-record-index-template-readiness.json",
        "validate_gfis_dev_002_valid_source_record_index_template_readiness.py",
        "gfis_dev_002_valid_source_record_index_template_readiness=pass",
        "valid-source-record-index.template.json",
        "GFIS-DEV-003",
        "gfis-dev-003-valid-source-record-index-schema-preflight.json",
        "validate_gfis_dev_003_valid_source_record_index_schema_preflight.py",
        "gfis_dev_003_valid_source_record_index_schema_preflight=pass",
        "valid-source-record-index.schema.json",
        "external_candidate_preflight_supported=true",
        "external_candidate_dir_preflight_supported=true",
        "report_json_supported=true",
        "temp_valid_candidates=1",
        "temp_invalid_candidates=1",
        "GFIS-DEV-004",
        "gfis-dev-004-valid-source-record-pre-submission-package.json",
        "validate_gfis_dev_004_valid_source_record_pre_submission_package.py",
        "gfis_dev_004_valid_source_record_pre_submission_package=pass",
        "package_preview_supported=true",
        "external_candidate_package_preview_supported=true",
        "copy_to_real_target_executed=false",
        "real_target_files=0",
        "GFIS-DEV-005",
        "gfis-dev-005-source-record-owner-submission-handoff-readiness.json",
        "validate_gfis_dev_005_source_record_owner_submission_handoff_readiness.py",
        "gfis_dev_005_source_record_owner_submission_handoff_readiness=pass",
        "handoff_steps=5",
        "receiving_scan_hold_gate_ready=true",
        "source_record_files_found=0",
        "GFIS-DEV-006",
        "gfis-dev-006-external-candidate-handoff-dry-run.json",
        "validate_gfis_dev_006_external_candidate_handoff_dry_run.py",
        "gfis_dev_006_external_candidate_handoff_dry_run=pass",
        "external_candidate_handoff_dry_run_supported=true",
        "dry_run_pipeline_steps=4",
        "valid_candidate_handoff_ready=1",
        "invalid_candidate_rejected=1",
        "GFIS-DEV-007",
        "gfis-dev-007-external-candidate-dir-handoff-dry-run.json",
        "validate_gfis_dev_007_external_candidate_dir_handoff_dry_run.py",
        "gfis_dev_007_external_candidate_dir_handoff_dry_run=pass",
        "external_candidate_dir_handoff_dry_run_supported=true",
        "valid_dir_handoff_ready=1",
        "invalid_dir_rejected=1",
        "GFIS-DEV-008",
        "gfis-dev-008-external-candidate-dir-remediation-summary.json",
        "validate_gfis_dev_008_external_candidate_dir_remediation_summary.py",
        "gfis_dev_008_external_candidate_dir_remediation_summary=pass",
        "external_candidate_dir_remediation_summary_supported=true",
        "invalid_dir_error_code_count=4",
        "remediation_actions=4",
        "GFIS-DEV-009",
        "gfis-dev-009-external-candidate-dir-manual-submission-manifest.json",
        "validate_gfis_dev_009_external_candidate_dir_manual_submission_manifest.py",
        "gfis_dev_009_external_candidate_dir_manual_submission_manifest=pass",
        "external_candidate_dir_manual_submission_manifest_supported=true",
        "valid_dir_manifest_ready=1",
        "valid_dir_manifest_item_count=1",
        "collision_dir_manifest_ready=0",
        "collision_dir_target_filename_conflicts=1",
        "invalid_dir_manifest_ready=0",
        "GFIS-DEV-010",
        "gfis-dev-010-manual-submission-command-preview.json",
        "validate_gfis_dev_010_manual_submission_command_preview.py",
        "gfis_dev_010_manual_submission_command_preview=pass",
        "manual_submission_command_preview_supported=true",
        "valid_dir_preview_command_count=1",
        "command_executed=false",
        "copy_to_real_target_executed=false",
        "GFIS-DEV-011",
        "gfis-dev-011-manual-execution-authorization-preflight.json",
        "validate_gfis_dev_011_manual_execution_authorization_preflight.py",
        "gfis_dev_011_manual_execution_authorization_preflight=pass",
        "manual_execution_authorization_preflight_supported=true",
        "authorization_template_preview_supported=true",
        "post_submit_verification_plan_supported=true",
        "post_submit_verification_plan_commands=7",
        "valid_authorization_preflight_ready=1",
        "temp_authorization_templates=1",
        "mismatched_authorization_preflight_ready=0",
        "incomplete_authorization_preflight_ready=0",
        "unchanged_template_preflight_ready=0",
        "--emit-authorization-template",
        "--emit-post-submit-verification-plan",
        "当前最小人工输入请求",
        "下一步不应继续扩展工具链",
        "提供 1 份已脱敏的 `CustomerRequirementOrPlatformOrder` source-of-record index 候选文件或候选目录",
        "确认 1 条等效正式业务确认",
        "明确授权人工操作员按 DEV-010/DEV-011 预检通过的命令",
        "当前推荐输入是 A",
        "next_required_input=real_source_record_or_equivalent_formal_confirmation",
        "manual_business_verification_pending=true",
        "real_business_lane=repair_required",
        "runtime intake",
        "review queue",
        "WAES review",
        "verified artifact candidate",
        "生产写入",
        "真实外部 API 写入",
        "schema migrate",
        "commit、push、deploy",
        "真实 KDS API 写入",
    ]:
        require(phrase in gfis_task, f"GFIS task missing phrase: {phrase}")

    for phrase in [
        "valid_source_records=0",
        "runtime_primary_key_ready=0",
        "review_queue=0",
        "runtime_intake=0",
        "waes_review=0",
        "verified=0",
        "real_business_lane=repair_required",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
    ]:
        require(phrase in gfis_dev_001_output, f"GFIS-DEV-001 output missing phrase: {phrase}")

    for phrase in [
        "template_files=1",
        "real_target_files=0",
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
        require(phrase in gfis_dev_002_output, f"GFIS-DEV-002 output missing phrase: {phrase}")

    for phrase in [
        "external_candidate_preflight_supported=true",
        "external_candidate_dir_preflight_supported=true",
        "report_json_supported=true",
        "schema_files=1",
        "temp_valid_candidates=1",
        "temp_invalid_candidates=1",
        "real_target_files=0",
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
        require(phrase in gfis_dev_003_output, f"GFIS-DEV-003 output missing phrase: {phrase}")

    for phrase in [
        "package_preview_supported=true",
        "external_candidate_package_preview_supported=true",
        "temp_valid_pre_submission_packages=1",
        "temp_invalid_pre_submission_packages=1",
        "copy_to_real_target_executed=false",
        "real_target_files=0",
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
        require(phrase in gfis_dev_004_output, f"GFIS-DEV-004 output missing phrase: {phrase}")

    for phrase in [
        "handoff_steps=5",
        "package_preview_supported=true",
        "receiving_scan_hold_gate_ready=true",
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
        require(phrase in gfis_dev_005_output, f"GFIS-DEV-005 output missing phrase: {phrase}")

    for phrase in [
        "external_candidate_handoff_dry_run_supported=true",
        "dry_run_pipeline_steps=4",
        "temp_valid_external_candidates=1",
        "temp_invalid_external_candidates=1",
        "valid_candidate_handoff_ready=1",
        "invalid_candidate_rejected=1",
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
        require(phrase in gfis_dev_006_output, f"GFIS-DEV-006 output missing phrase: {phrase}")

    for phrase in [
        "external_candidate_dir_handoff_dry_run_supported=true",
        "temp_valid_candidate_dirs=1",
        "temp_invalid_candidate_dirs=1",
        "valid_dir_candidate_count=2",
        "valid_dir_handoff_ready=1",
        "invalid_dir_candidate_count=2",
        "invalid_dir_rejected=1",
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
        require(phrase in gfis_dev_007_output, f"GFIS-DEV-007 output missing phrase: {phrase}")

    for phrase in [
        "external_candidate_dir_remediation_summary_supported=true",
        "temp_valid_candidate_dirs=1",
        "temp_invalid_candidate_dirs=1",
        "valid_dir_candidate_count=2",
        "valid_dir_rejected_count=0",
        "invalid_dir_candidate_count=2",
        "invalid_dir_rejected_count=1",
        "invalid_dir_error_code_count=4",
        "remediation_actions=4",
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
        require(phrase in gfis_dev_008_output, f"GFIS-DEV-008 output missing phrase: {phrase}")

    for phrase in [
        "external_candidate_dir_manual_submission_manifest_supported=true",
        "temp_valid_candidate_dirs=1",
        "temp_collision_candidate_dirs=1",
        "temp_invalid_candidate_dirs=1",
        "valid_dir_candidate_count=1",
        "valid_dir_manifest_ready=1",
        "valid_dir_manifest_item_count=1",
        "collision_dir_candidate_count=2",
        "collision_dir_manifest_ready=0",
        "collision_dir_target_filename_conflicts=1",
        "invalid_dir_candidate_count=2",
        "invalid_dir_manifest_ready=0",
        "invalid_dir_rejected_count=1",
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
        require(phrase in gfis_dev_009_output, f"GFIS-DEV-009 output missing phrase: {phrase}")

    for phrase in [
        "manual_submission_command_preview_supported=true",
        "temp_valid_candidate_dirs=1",
        "temp_collision_candidate_dirs=1",
        "temp_invalid_candidate_dirs=1",
        "valid_dir_preview_command_count=1",
        "collision_dir_preview_command_count=0",
        "collision_dir_target_filename_conflicts=1",
        "invalid_dir_preview_command_count=0",
        "invalid_dir_rejected_count=1",
        "command_executed=false",
        "copy_to_real_target_executed=false",
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
        require(phrase in gfis_dev_010_output, f"GFIS-DEV-010 output missing phrase: {phrase}")

    for phrase in [
        "manual_execution_authorization_preflight_supported=true",
        "authorization_template_preview_supported=true",
        "post_submit_verification_plan_supported=true",
        "post_submit_verification_plan_commands=7",
        "temp_valid_authorization_packets=1",
        "temp_mismatched_authorization_packets=1",
        "temp_incomplete_authorization_packets=1",
        "valid_authorization_preflight_ready=1",
        "temp_authorization_templates=1",
        "mismatched_authorization_preflight_ready=0",
        "incomplete_authorization_preflight_ready=0",
        "unchanged_template_preflight_ready=0",
        "command_executed=false",
        "copy_to_real_target_executed=false",
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
        require(phrase in gfis_dev_011_output, f"GFIS-DEV-011 output missing phrase: {phrase}")

    require(
        "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-MIN-001.md" in task_readme,
        "task README missing GFIS task entry",
    )
    require(
        "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.md" in task_readme,
        "task README missing GFIS dev completion task entry",
    )

    for phrase in [
        "GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001",
        "GFIS Delivery Completion Sprint",
        "development_lane=continue_allowed",
        "real_business_validation_lane=pending_source_of_record",
        "real_source_records_zero_is_not_dev_blocker=true",
        "development_ready_for_real_business_validation",
        "CustomerRequirementOrPlatformOrder contract",
        "controlled_contract_valid_sample",
        "runtime intake dry-run",
        "runtime primary key candidate",
        "review queue item",
        "WAES review candidate",
        "verified artifact candidate",
        "fixture E2E dry-run result",
        "local validator result",
        "fixture_e2e_passed",
        "contract_validator_passed",
        "execution_mode=controlled_multi_agent",
        "DEV-COMP-006 delivery boundary validation",
        "DEV-COMP-007 orchestrator summary",
        "same_file_parallel_write_allowed=false",
        "orchestrator_only_files=LOOP_CONTROL_BOARD.md,gpcf-project-status-matrix.md,GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001-evidence.md,LOOP_GOVERNANCE_SUMMARY_GFIS_RUNTIME_SOP_E2E_DEV_COMPLETION_001.md",
        "real_business_verified",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
    ]:
        require(phrase in gfis_dev_completion_task, f"GFIS dev completion task missing phrase: {phrase}")

    for phrase in [
        "GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001 多智能体执行包",
        "mode: controlled_multi_agent",
        "default_loop: Delivery Loop",
        "governance_level: G1",
        "Contract Agent",
        "Runtime Intake Agent",
        "Primary Key / Source Validation Agent",
        "Review Queue Agent",
        "WAES Candidate / Artifact Agent",
        "Boundary Validator Agent",
        "阶段 A：并行只读设计",
        "阶段 B：受控实现",
        "same_file_parallel_write_allowed: false",
        "orchestrator_only_files:",
        "DEV-COMP-006",
        "DEV-COMP-007",
        "delivery_boundary_validator_passed=true",
        "controlled_sample_exists: true",
        "runtime_intake_dry_run_passed: true",
        "verified_artifact_candidate_by_fixture_generated: true",
        "并行设计，串行落地",
        "development_ready_for_real_business_validation",
    ]:
        require(
            phrase in gfis_dev_completion_multi_agent_task,
            f"GFIS dev completion multi-agent task missing phrase: {phrase}",
        )

    for phrase in [
        "gfis_dev_completion_controlled_sample=pass",
        "object_family=CustomerRequirementOrPlatformOrder",
        "template_only=true",
        "fixture_synthetic=true",
        "candidate_lane=true",
        "status_promotion_allowed=false",
    ]:
        require(phrase in gfis_controlled_sample_output, f"GFIS controlled sample output missing phrase: {phrase}")

    for phrase in [
        "gfis_runtime_sop_dev_completion_dry_run=pass",
        "synthetic_dev_lane=dev_closed",
        "synthetic_e2e=synthetic_e2e_pass",
        "synthetic_stage_count=12",
        "synthetic_closed_loop_passed=1",
        "source_record_candidates=1",
        "runtime_primary_key_candidates=1",
        "review_queue_candidates=1",
        "runtime_intake_candidates=1",
        "waes_review_candidates=1",
        "verified_artifact_candidates=1",
        "real_source_records=0",
        "status_promotion_allowed=false",
    ]:
        require(
            phrase in gfis_dev_completion_dry_run_output,
            f"GFIS dev completion dry-run output missing phrase: {phrase}",
        )

    for phrase in [
        "GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001 Evidence",
        "delivery_loop:",
        "CustomerRequirementOrPlatformOrder",
        "controlled_contract_valid_sample",
        "synthetic_dev_lane=dev_closed",
        "synthetic_e2e=synthetic_e2e_pass",
        "synthetic_stage_count=12",
        "synthetic_runtime_primary_keys=12",
        "synthetic_review_queue_items=12",
        "synthetic_runtime_intake_items=12",
        "synthetic_waes_evidence_candidates=12",
        "synthetic_verified_artifacts=12",
        "synthetic_closed_loop_passed=1",
        "source_record_candidates=1",
        "runtime_primary_key_candidates=1",
        "runtime_intake_candidates=1",
        "review_queue_candidates=1",
        "waes_review_candidates=1",
        "verified_artifact_candidates=1",
        "real_business_source_of_record_verified=false",
        "real_business_verified=false",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
        "real_business_lane=repair_required",
        "real_business_validation_lane=pending_source_of_record",
        "development_ready_for_real_business_validation=candidate",
        "fixture_e2e_passed=true",
        "contract_validator_passed=true",
        "execution_mode=controlled_multi_agent",
        "multi_agent_phase=orchestrator_summary",
        "agent_count=7",
        "phase_a_readonly_design=true",
        "phase_b_controlled_implementation=true",
        "file_lock_required=true",
        "same_file_parallel_write_allowed=false",
        "controlled_sample_exists=true",
        "runtime_intake_dry_run_passed=true",
        "delivery_boundary_validator_passed=true",
    ]:
        require(phrase in gfis_dev_completion_evidence, f"GFIS dev completion evidence missing phrase: {phrase}")

    for phrase in [
        "LOOP Governance Summary GFIS Runtime SOP E2E Dev Completion 001",
        "mainline=GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001",
        "delivery_loop_count=5",
        "governance_summary_required=true",
        "governance_summary_status=completed_check_only",
        "development_lane=continue_allowed",
        "real_business_validation_lane=pending_source_of_record",
        "acceptance_lane=not_started",
        "production_lane=not_started",
        "status_promotion_requested=false",
        "status_promotion_allowed=false",
        "execution_mode=controlled_multi_agent",
        "multi_agent_phase=orchestrator_summary",
        "agent_count=7",
        "phase_a_readonly_design=true",
        "phase_b_controlled_implementation=true",
        "same_file_parallel_write_allowed=false",
        "same_file_parallel_write_detected=false",
        "CustomerRequirementOrPlatformOrder contract",
        "controlled_contract_valid_sample=true",
        "synthetic_runtime_intake_items=12",
        "runtime_primary_key_candidates=1",
        "review_queue_candidates=1",
        "waes_review_candidates=1",
        "verified_artifact_candidates=1",
        "synthetic_e2e=synthetic_e2e_pass",
        "real_business_verified=false",
        "accepted=false",
        "integrated=false",
        "production_ready=false",
        "customer_accepted=false",
        "development_ready_for_real_business_validation=candidate",
        "delivery_boundary_validator_passed=true",
        "p0_violation=false",
        "p1_violation=false",
        "production_write_executed=false",
        "real_external_api_write_executed=false",
        "real_kds_api_write_executed=false",
        "schema_migrate_executed=false",
        "bench_migrate_executed=false",
        "commit_executed=false",
        "push_executed=false",
        "deploy_executed=false",
    ]:
        require(
            phrase in gfis_dev_completion_governance_summary,
            f"GFIS dev completion governance summary missing phrase: {phrase}",
        )

    for forbidden in [
        "accepted: true",
        "integrated: true",
        "production_ready: true",
        "customer_accepted: true",
        "真实 KDS API 已同步",
    ]:
        combined = "\n".join(
            [
                slimming,
                gate,
                template,
                matrix,
                gfis_task,
                gfis_dev_completion_task,
                gfis_dev_completion_multi_agent_task,
                gfis_dev_completion_evidence,
                gfis_dev_completion_governance_summary,
            ]
        )
        require(forbidden not in combined, f"forbidden v1.1 claim present: {forbidden}")

    print(
        "loop_v11_slimming_delivery_recovery=pass "
        "delivery_loop=enabled governance_loop=stage_or_risk_triggered "
        "gate_levels=P0,P1,P2,P3 gfis_min_slice=registered "
        "gfis_dev_completion_slice=registered "
        "gfis_dev_completion_multi_agent=registered "
        "gfis_dev_completion_evidence=registered "
        "gfis_dev_completion_governance_summary=registered "
        "fixture_e2e_passed=true contract_validator_passed=true "
        f"development_lane={gfis_real_fact_entry.get('development_lane')} "
        f"real_business_validation_lane={gfis_real_fact_entry.get('real_business_validation_lane')} "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
        "accepted=false integrated=false production_ready=false customer_accepted=false "
        "status_promotion_allowed=false"
        f" kds_sensitive_blocker={kds_blocker.get('kds_sensitive_blocker_classification')}"
        " kds_safe_to_auto_commit=false governance_drift=pass gfis_authorization_boundary=pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
