#!/usr/bin/env python3
"""Assess Loop self-correction gates after false-positive closure evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")
OUT = ROOT / "docs/harness/evidence/loop_self_correction_assessment.json"


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def git_dirty(path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(path), "status", "--porcelain"],
        check=False,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_gfis_runtime_sop_validator() -> dict:
    validator = GFIS_ROOT / "scripts/validate_gfis_runtime_sop_e2e.py"
    if not validator.exists():
        return {
            "status": "missing_validator",
            "exit_code": None,
            "output": [],
        }
    result = subprocess.run(
        ["python3", str(validator.relative_to(GFIS_ROOT))],
        cwd=str(GFIS_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    output = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines() if line.strip()]
    status = "unknown"
    for line in output:
        if line.startswith("gfis_runtime_sop_e2e="):
            status = line.split("=", 1)[1].split()[0]
            break
    if status == "unknown" and result.returncode != 0:
        status = "repair_required"
    return {
        "status": status,
        "exit_code": result.returncode,
        "output": output,
    }


def run_gfis_named_validator(script_name: str) -> dict:
    validator = GFIS_ROOT / "scripts" / script_name
    if not validator.exists():
        return {
            "status": "missing_validator",
            "exit_code": None,
            "output": [],
        }
    result = subprocess.run(
        ["python3", str(validator.relative_to(GFIS_ROOT))],
        cwd=str(GFIS_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    output = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines() if line.strip()]
    status = "pass" if result.returncode == 0 else "failed"
    return {
        "status": status,
        "exit_code": result.returncode,
        "output": output,
    }


def run_loop_round_efficiency_audit() -> dict:
    validator = ROOT / "tools/kds-sync/validate_loop_round_efficiency_audit.py"
    if not validator.exists():
        return {
            "status": "missing_validator",
            "exit_code": None,
            "output": [],
            "metrics": {},
        }
    result = subprocess.run(
        ["python3", str(validator.relative_to(ROOT))],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    output = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    metrics: dict[str, str] = {}
    for line in output:
        if line.startswith("loop_round_efficiency_audit="):
            for part in line.split():
                if "=" in part:
                    key, value = part.split("=", 1)
                    metrics[key] = value
            break
    return {
        "status": metrics.get("loop_round_efficiency_audit", "failed" if result.returncode else "unknown"),
        "exit_code": result.returncode,
        "output": output,
        "metrics": metrics,
    }


def runtime_kds_source_paths_closed(runtime_sop: dict) -> bool:
    return any("missing_kds_source_paths=0" in line for line in runtime_sop.get("output", []))


def main() -> int:
    evidence_index = read(ROOT / "docs/harness/minimum-closed-loop/evidence-index.md")
    closure_matrix = read(ROOT / "docs/harness/minimum-closed-loop/l4-closure-score-matrix.md")
    gpcf_round = read(ROOT / "docs/harness/loops/loop-round-GPCF-L4-012.md")
    gfis_agents = read(GFIS_ROOT / "AGENTS.md")
    gfis_readme = read(GFIS_ROOT / "README.md")
    gfis_manifest = read(GFIS_ROOT / "PROJECT_HARNESS_MANIFEST.md")
    gfis_round = read(GFIS_ROOT / "docs/harness/loops/loop-round-GFIS-L4-008.md")
    gfis_retrieval = read(GFIS_ROOT / "docs/harness/evidence/kds-retrieval-GFIS-L4-008.json")
    gfis_last_run = load_json(GFIS_ROOT / "test-results/.last-run.json")
    runtime_sop = run_gfis_runtime_sop_validator()
    synthetic_dev_lane = run_gfis_named_validator("validate_gfis_runtime_sop_e2e_dev.py")
    real_business_lane = run_gfis_named_validator("validate_gfis_runtime_sop_e2e_real.py")
    real_source_record_intake_gate = run_gfis_named_validator("validate_gfis_real_source_record_intake_gate.py")
    pending_business_verification = run_gfis_named_validator("validate_gfis_pending_business_verification.py")
    runtime_primary_key_gate = run_gfis_named_validator("validate_gfis_runtime_primary_key_gate.py")
    review_queue_admission_gate = run_gfis_named_validator("validate_gfis_review_queue_admission_gate.py")
    runtime_intake_gate = run_gfis_named_validator("validate_gfis_runtime_intake_gate.py")
    waes_review_gate = run_gfis_named_validator("validate_gfis_waes_review_gate.py")
    verified_artifact_gate = run_gfis_named_validator("validate_gfis_verified_artifact_gate.py")
    development_ready_goal = run_gfis_named_validator("validate_gfis_development_ready_goal.py")
    test_source_record_submission_gate = run_gfis_named_validator("validate_gfis_customer_requirement_test_source_record_submission.py")
    test_data_minimum_sop_e2e = run_gfis_named_validator("validate_gfis_test_data_minimum_sop_e2e.py")
    test_data_12_stage_sop_e2e = run_gfis_named_validator("validate_gfis_test_data_12_stage_sop_e2e.py")
    test_data_12_stage_transition_gate = run_gfis_named_validator("validate_gfis_test_data_12_stage_transition_gate.py")
    test_data_12_stage_negative_transition_guard = run_gfis_named_validator("validate_gfis_test_data_12_stage_negative_transition_guard.py")
    loop_efficiency = run_loop_round_efficiency_audit()

    combined_gpcf = "\n".join([evidence_index, closure_matrix, gpcf_round])
    combined_gfis_current_boundary = "\n".join([gfis_agents, gfis_readme, gfis_manifest])
    combined_gfis_historical_evidence = "\n".join([gfis_round, gfis_retrieval])
    combined_gfis = "\n".join([combined_gfis_current_boundary, combined_gfis_historical_evidence])

    demo_path = "gcfis_demo/field_samples/gfis_l4_factory_sample_order_readonly.json"
    demo_counted_as_runtime = demo_path in combined_gpcf or demo_path in combined_gfis
    demo_currently_claimed_as_runtime = demo_path in combined_gfis_current_boundary
    runtime_boundary_declared = all(
        phrase in combined_gfis
        for phrase in [
            "GFIS 运行层",
            "GFIS Demo 只用于展示",
            "不作为 SOP 实现主体",
        ]
    )
    sop_e2e_status = gfis_last_run.get("status", "unknown")
    sop_e2e_failed = sop_e2e_status == "failed"
    runtime_sop_status = runtime_sop["status"]
    runtime_sop_repair_required = runtime_sop_status != "pass"
    gfis_dirty = git_dirty(GFIS_ROOT)

    blockers = []
    if demo_currently_claimed_as_runtime:
        blockers.append("gfis_demo_currently_counted_as_runtime_evidence")
    elif demo_counted_as_runtime:
        blockers.append("gfis_demo_historical_evidence_invalidated")
    if sop_e2e_failed:
        blockers.append("gfis_sop_e2e_failed")
    if runtime_sop_repair_required:
        blockers.append("gfis_runtime_sop_e2e_repair_required")
    if synthetic_dev_lane["exit_code"] != 0:
        blockers.append("gfis_synthetic_dev_lane_not_closed")
    if real_business_lane["exit_code"] != 0:
        blockers.append("gfis_real_business_lane_guard_failed")
    if real_source_record_intake_gate["exit_code"] != 0:
        blockers.append("gfis_real_source_record_intake_gate_failed")
    if pending_business_verification["exit_code"] != 0:
        blockers.append("gfis_pending_business_verification_gate_failed")
    if runtime_primary_key_gate["exit_code"] != 0:
        blockers.append("gfis_runtime_primary_key_gate_failed")
    if review_queue_admission_gate["exit_code"] != 0:
        blockers.append("gfis_review_queue_admission_gate_failed")
    if runtime_intake_gate["exit_code"] != 0:
        blockers.append("gfis_runtime_intake_gate_failed")
    if waes_review_gate["exit_code"] != 0:
        blockers.append("gfis_waes_review_gate_failed")
    if verified_artifact_gate["exit_code"] != 0:
        blockers.append("gfis_verified_artifact_gate_failed")
    if development_ready_goal["exit_code"] != 0:
        blockers.append("gfis_development_ready_goal_failed")
    if test_source_record_submission_gate["exit_code"] != 0:
        blockers.append("gfis_test_source_record_submission_gate_failed")
    if test_data_minimum_sop_e2e["exit_code"] != 0:
        blockers.append("gfis_test_data_minimum_sop_e2e_failed")
    if test_data_12_stage_sop_e2e["exit_code"] != 0:
        blockers.append("gfis_test_data_12_stage_sop_e2e_failed")
    if test_data_12_stage_transition_gate["exit_code"] != 0:
        blockers.append("gfis_test_data_12_stage_transition_gate_failed")
    if test_data_12_stage_negative_transition_guard["exit_code"] != 0:
        blockers.append("gfis_test_data_12_stage_negative_transition_guard_failed")
    if any("KDS coverage must not have missing controlled sources" in line for line in runtime_sop.get("output", [])):
        blockers.append("gfis_kds_controlled_sources_missing")
    if not runtime_boundary_declared:
        blockers.append("gfis_runtime_boundary_missing")
    if gfis_dirty:
        blockers.append("gfis_repo_dirty_user_work_present")
    loop_efficiency_metrics = loop_efficiency.get("metrics", {})
    if loop_efficiency.get("exit_code") != 0:
        blockers.append("loop_round_efficiency_audit_failed")
    elif loop_efficiency_metrics.get("risk") in {"watch", "review_required"}:
        blockers.append(f"loop_round_efficiency_{loop_efficiency_metrics['risk']}")

    gate = "blocked" if blockers else "pass"
    score = 79 if blockers and runtime_kds_source_paths_closed(runtime_sop) else 78 if blockers else 100
    assessment = {
        "round_id": "GPCF-L4-GFIS-TEST-12STAGE-NEGATIVE-SYNC-001",
        "gate": gate,
        "project_group_score": score,
        "development_ready": "pass" if development_ready_goal["exit_code"] == 0 else "failed",
        "test_data_minimum_sop_e2e": "pass" if test_data_minimum_sop_e2e["exit_code"] == 0 else "failed",
        "test_data_12_stage_sop_e2e": "pass" if test_data_12_stage_sop_e2e["exit_code"] == 0 else "failed",
        "test_data_12_stage_transition_gate": "pass" if test_data_12_stage_transition_gate["exit_code"] == 0 else "failed",
        "test_data_12_stage_negative_transition_guard": "pass" if test_data_12_stage_negative_transition_guard["exit_code"] == 0 else "failed",
        "synthetic_dev_lane": "dev_closed" if synthetic_dev_lane["exit_code"] == 0 else "failed",
        "real_business_lane": "repair_required",
        "business_verification_pending": True,
        "previous_l4_score_invalidated": gate == "blocked",
        "invalidated_rounds": ["GFIS-L4-008", "GPCF-L4-012"] if gate == "blocked" else [],
        "gfis": {
            "expected_subject": "GFIS运行层",
            "forbidden_subject_for_sop_acceptance": "GFIS Demo",
            "runtime_boundary_declared": runtime_boundary_declared,
            "demo_counted_as_runtime_evidence": demo_counted_as_runtime,
            "demo_currently_claimed_as_runtime": demo_currently_claimed_as_runtime,
            "current_runtime_subject": "pass" if runtime_boundary_declared and not demo_currently_claimed_as_runtime else "invalid",
            "sop_e2e_status": sop_e2e_status,
            "sop_e2e_failed_tests": gfis_last_run.get("failedTests", []),
            "runtime_sop_e2e_status": runtime_sop_status,
            "runtime_sop_e2e_exit_code": runtime_sop["exit_code"],
            "runtime_sop_e2e_output": runtime_sop["output"],
            "synthetic_dev_lane_status": synthetic_dev_lane["status"],
            "synthetic_dev_lane_exit_code": synthetic_dev_lane["exit_code"],
            "synthetic_dev_lane_output": synthetic_dev_lane["output"],
            "real_business_lane_status": "repair_required",
            "real_business_lane_exit_code": real_business_lane["exit_code"],
            "real_business_lane_output": real_business_lane["output"],
            "real_source_record_intake_gate_status": real_source_record_intake_gate["status"],
            "real_source_record_intake_gate_exit_code": real_source_record_intake_gate["exit_code"],
            "real_source_record_intake_gate_output": real_source_record_intake_gate["output"],
            "pending_business_verification_gate_status": pending_business_verification["status"],
            "pending_business_verification_gate_exit_code": pending_business_verification["exit_code"],
            "pending_business_verification_gate_output": pending_business_verification["output"],
            "runtime_primary_key_gate_status": runtime_primary_key_gate["status"],
            "runtime_primary_key_gate_exit_code": runtime_primary_key_gate["exit_code"],
            "runtime_primary_key_gate_output": runtime_primary_key_gate["output"],
            "review_queue_admission_gate_status": review_queue_admission_gate["status"],
            "review_queue_admission_gate_exit_code": review_queue_admission_gate["exit_code"],
            "review_queue_admission_gate_output": review_queue_admission_gate["output"],
            "runtime_intake_gate_status": runtime_intake_gate["status"],
            "runtime_intake_gate_exit_code": runtime_intake_gate["exit_code"],
            "runtime_intake_gate_output": runtime_intake_gate["output"],
            "waes_review_gate_status": waes_review_gate["status"],
            "waes_review_gate_exit_code": waes_review_gate["exit_code"],
            "waes_review_gate_output": waes_review_gate["output"],
            "verified_artifact_gate_status": verified_artifact_gate["status"],
            "verified_artifact_gate_exit_code": verified_artifact_gate["exit_code"],
            "verified_artifact_gate_output": verified_artifact_gate["output"],
            "development_ready_goal_status": development_ready_goal["status"],
            "development_ready_goal_exit_code": development_ready_goal["exit_code"],
            "development_ready_goal_output": development_ready_goal["output"],
            "test_source_record_submission_gate_status": test_source_record_submission_gate["status"],
            "test_source_record_submission_gate_exit_code": test_source_record_submission_gate["exit_code"],
            "test_source_record_submission_gate_output": test_source_record_submission_gate["output"],
            "test_data_minimum_sop_e2e_status": test_data_minimum_sop_e2e["status"],
            "test_data_minimum_sop_e2e_exit_code": test_data_minimum_sop_e2e["exit_code"],
            "test_data_minimum_sop_e2e_output": test_data_minimum_sop_e2e["output"],
            "test_data_12_stage_sop_e2e_status": test_data_12_stage_sop_e2e["status"],
            "test_data_12_stage_sop_e2e_exit_code": test_data_12_stage_sop_e2e["exit_code"],
            "test_data_12_stage_sop_e2e_output": test_data_12_stage_sop_e2e["output"],
            "test_data_12_stage_transition_gate_status": test_data_12_stage_transition_gate["status"],
            "test_data_12_stage_transition_gate_exit_code": test_data_12_stage_transition_gate["exit_code"],
            "test_data_12_stage_transition_gate_output": test_data_12_stage_transition_gate["output"],
            "test_data_12_stage_negative_transition_guard_status": test_data_12_stage_negative_transition_guard["status"],
            "test_data_12_stage_negative_transition_guard_exit_code": test_data_12_stage_negative_transition_guard["exit_code"],
            "test_data_12_stage_negative_transition_guard_output": test_data_12_stage_negative_transition_guard["output"],
            "git_dirty": gfis_dirty,
        },
        "loop_efficiency": {
            "status": loop_efficiency["status"],
            "exit_code": loop_efficiency["exit_code"],
            "metrics": loop_efficiency_metrics,
            "output": loop_efficiency["output"],
            "governance_meaning": (
                "Loop round records are machine-audited for truth fields, five-segment substance, "
                "batch-generated counting, duplicate fingerprints, high similarity, and long sequence risk. "
                "A review_required risk does not mean GFIS implementation completed; it means governance "
                "must keep efficiency debt visible."
            ),
        },
        "blockers": blockers,
        "required_repairs": [
            "Replace GFIS-L4-008 demo fixture evidence with GFIS runtime-layer DocType/workflow/API evidence.",
            "Run and pass the SOP E2E master path against the GFIS runtime layer after KDS missing controlled sources and valid source record inputs are resolved.",
            "Collect KDS Gehua controlled missing_input and runtime-layer evidence before any score restoration.",
            "Keep GFIS Demo limited to display, training, traceability explanation and frontend regression.",
            "Do not mark L4 closed or 100/100 while runtime subject or E2E gates are blocked.",
            "Keep CustomerRequirementOrPlatformOrder real source-of-record intake blocked until owner-confirmed customer order, platform order receipt, purchase order, customer confirmation, or equivalent formal confirmation arrives.",
            "Keep pending_business_verification quarantined until manual business verification passes; do not create runtime primary key from quotation-only, Loop document-only, Demo, mock, or fixture evidence.",
            "Keep runtime primary key creation blocked until valid_source_record and manual business verification both pass.",
            "Keep review queue admission blocked until a verified runtime primary key exists.",
            "Keep runtime intake blocked until a verified review queue item exists.",
            "Keep WAES review blocked until a verified runtime intake item exists.",
            "Keep verified artifact blocked until a real WAES review result exists.",
            "Keep development_ready separate from production_ready and accepted/integrated; development_ready only means synthetic dev lane and local E2E/display regression are auditable.",
            "Keep test_data_lane separate from real_business_lane; TEST-GFIS records must not unlock runtime primary key, review queue, runtime intake, WAES review, verified artifact, or production_ready.",
            "Keep test_data_minimum_sop_e2e separate from real SOP acceptance; it proves test-chain shape and pollution guard only.",
            "Keep test_data_12_stage_sop_e2e separate from real SOP acceptance; it proves 12-stage test-data shape and pollution guard only.",
            "Keep test_data_12_stage_transition_gate separate from real SOP acceptance; it proves test-stage transition boundaries, POD/finance manual gates, and pollution guard only.",
            "Keep test_data_12_stage_negative_transition_guard separate from real SOP acceptance; it proves invalid test transitions, bypass attempts, demo substitution, write claims, and status-upgrade claims are rejected only.",
            "Review Loop round efficiency debt before counting long continuous sequences as high-confidence progress.",
        ],
        "stop_type": "blocked_real_business_lane_after_development_ready" if blockers else "none",
        "substance_gate": "pass",
        "declared_rounds": "1/15",
        "substantive_rounds": "1/15",
        "generated_items": 5,
        "batch_generated": False,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "loop_self_correction_gate="
        f"{gate} gfis_runtime_subject="
        f"{'invalid' if demo_currently_claimed_as_runtime or not runtime_boundary_declared else 'pass'} "
        f"historical_demo_evidence={'invalidated' if demo_counted_as_runtime else 'none'} "
        f"demo_e2e={sop_e2e_status} runtime_sop_e2e={runtime_sop_status} "
        f"loop_efficiency_risk={loop_efficiency_metrics.get('risk', 'unknown')} "
        f"project_group_score={score} synthetic_dev_lane="
        f"{'dev_closed' if synthetic_dev_lane['exit_code'] == 0 else 'failed'} "
        f"development_ready={'pass' if development_ready_goal['exit_code'] == 0 else 'failed'} "
        f"test_data_minimum_sop_e2e={'pass' if test_data_minimum_sop_e2e['exit_code'] == 0 else 'failed'} "
        f"test_data_12_stage_sop_e2e={'pass' if test_data_12_stage_sop_e2e['exit_code'] == 0 else 'failed'} "
        f"test_data_12_stage_transition_gate={'pass' if test_data_12_stage_transition_gate['exit_code'] == 0 else 'failed'} "
        f"test_data_12_stage_negative_transition_guard={'pass' if test_data_12_stage_negative_transition_guard['exit_code'] == 0 else 'failed'} "
        f"real_business_lane=repair_required business_verification_pending=true "
        f"real_source_record_intake_gate={real_source_record_intake_gate['status']} "
        f"pending_business_verification_gate={pending_business_verification['status']} "
        f"runtime_primary_key_gate={runtime_primary_key_gate['status']} "
        f"review_queue_gate={review_queue_admission_gate['status']} "
        f"runtime_intake_gate={runtime_intake_gate['status']} "
        f"waes_review_gate={waes_review_gate['status']} "
        f"verified_artifact_gate={verified_artifact_gate['status']} "
        f"development_ready_goal={development_ready_goal['status']} "
        f"test_source_record_submission_gate={test_source_record_submission_gate['status']} "
        f"test_data_minimum_sop_e2e={test_data_minimum_sop_e2e['status']} "
        f"test_data_12_stage_sop_e2e={test_data_12_stage_sop_e2e['status']} "
        f"test_data_12_stage_transition_gate={test_data_12_stage_transition_gate['status']} "
        f"test_data_12_stage_negative_transition_guard={test_data_12_stage_negative_transition_guard['status']} "
        f"next=real-source-record-or-business-input-remediation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
