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
    output = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    status = "unknown"
    for line in output:
        if line.startswith("gfis_runtime_sop_e2e="):
            status = line.split("=", 1)[1].split()[0]
            break
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
        "round_id": "GPCF-L4-CORR-001",
        "gate": gate,
        "project_group_score": score,
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
            "Run and pass the SOP E2E master path against the GFIS runtime layer.",
            "Collect KDS Gehua controlled missing_input and runtime-layer evidence before any score restoration.",
            "Keep GFIS Demo limited to display, training, traceability explanation and frontend regression.",
            "Do not mark L4 closed or 100/100 while runtime subject or E2E gates are blocked.",
            "Review Loop round efficiency debt before counting long continuous sequences as high-confidence progress.",
        ],
        "stop_type": "hard_stop" if blockers else "none",
        "substance_gate": "pass",
        "declared_rounds": "1/15",
        "substantive_rounds": "1/15",
        "generated_items": 3,
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
        f"project_group_score={score} next=GFIS-runtime-repair"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
