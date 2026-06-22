#!/usr/bin/env python3
"""Validate D122 GCKF P0 skeleton baseline evidence."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-skeleton-baseline-d122-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-skeleton-baseline-d122-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D122-001.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
HEALTH_REPORT = ROOT / "09-status/globalcloud-document-health-report.md"


def fail(message: str) -> None:
    print(f"gckf_p0_skeleton_baseline_d122=fail reason={message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def run_command(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        fail(f"command_failed:{' '.join(args)}:{stderr}")
    return result.stdout.strip()


def main() -> None:
    require(EVIDENCE_JSON.exists() and EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d122_artifacts")

    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    require(evidence.get("execution_mode") == "local_evidence_no_write", "execution_mode_not_no_write")

    task_packages = evidence.get("task_packages", {})
    require(set(task_packages.keys()) == {"T0", "T1", "T2", "T3", "T4", "T5", "T6"}, "task_package_set_mismatch")
    for task_id, payload in task_packages.items():
        artifacts = payload.get("representative_artifacts", [])
        require(artifacts, f"empty_artifacts:{task_id}")
        for rel_path in artifacts:
            require((ROOT / rel_path).exists(), f"missing_task_artifact:{task_id}:{rel_path}")

    status_text = read(STATUS_MATRIX)
    health_text = read(HEALTH_REPORT)
    require("GlobalCoud GPCF" in status_text and "repair_required" in status_text, "status_matrix_missing_gpcf_repair_required")
    require("localization_gate=pass" in health_text, "health_report_missing_localization_pass")

    coverage_output = run_command("python3", "scripts/coverage/validate_okf_types_api_validator_coverage.py")
    require(coverage_output.startswith("okf_types_api_validator_coverage=pass"), "coverage_validator_not_pass")
    match = re.search(r"coverage_items=(\d+)", coverage_output)
    require(match is not None, "coverage_items_missing")
    coverage_items = int(match.group(1))
    require(coverage_items >= 199, "coverage_items_below_current_baseline")

    master_output = run_command("python3", "tools/kds-sync/validate_loop_engineering_master_plan.py")
    require(master_output.startswith("loop_engineering_master_plan=pass"), "master_plan_validator_not_pass")

    five_direction_output = run_command("python3", "tools/kds-sync/validate_loop_engineering_five_direction_implementation.py")
    require(
        five_direction_output.startswith("loop_engineering_five_direction_implementation=pass"),
        "five_direction_validator_not_pass",
    )

    localization_output = run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000")
    localization = json.loads(localization_output)
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution_output = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution_output == "document_pollution=pass", "document_pollution_not_pass")

    kds_token_output = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token_output.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate_output = run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only")
    loop_gate = json.loads(loop_gate_output)
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    verification_snapshot = evidence.get("verification_snapshot", {})
    require(verification_snapshot.get("localization_gate") == "pass", "evidence_localization_snapshot_mismatch")
    require(verification_snapshot.get("document_pollution") == "pass", "evidence_document_pollution_snapshot_mismatch")
    require(str(verification_snapshot.get("kds_token", "")).startswith("pass"), "evidence_kds_token_snapshot_mismatch")
    require(verification_snapshot.get("loop_document_gate") == "pass", "evidence_loop_gate_snapshot_mismatch")

    state_ceiling = evidence.get("state_ceiling", {})
    require(state_ceiling.get("gpcf_status_ceiling") == "repair_required", "gpcf_status_ceiling_mismatch")
    require(state_ceiling.get("gfis_real_business_lane") == "repair_required", "gfis_lane_ceiling_mismatch")
    require(state_ceiling.get("accepted") is False, "accepted_boundary_not_false")
    require(state_ceiling.get("integrated") is False, "integrated_boundary_not_false")
    require(state_ceiling.get("production_ready") is False, "production_ready_boundary_not_false")

    print("gckf_p0_skeleton_baseline_d122=pass")
    print(f"task_packages={len(task_packages)}")
    print(f"coverage_items={coverage_items}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print(f"execution_mode={evidence.get('execution_mode')}")


if __name__ == "__main__":
    main()
