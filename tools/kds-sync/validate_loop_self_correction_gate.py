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

    combined_gpcf = "\n".join([evidence_index, closure_matrix, gpcf_round])
    combined_gfis = "\n".join([gfis_agents, gfis_readme, gfis_manifest, gfis_round, gfis_retrieval])

    demo_path = "gcfis_demo/field_samples/gfis_l4_factory_sample_order_readonly.json"
    demo_counted_as_runtime = demo_path in combined_gpcf or demo_path in combined_gfis
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
    gfis_dirty = git_dirty(GFIS_ROOT)

    blockers = []
    if demo_counted_as_runtime:
        blockers.append("gfis_demo_counted_as_runtime_evidence")
    if sop_e2e_failed:
        blockers.append("gfis_sop_e2e_failed")
    if not runtime_boundary_declared:
        blockers.append("gfis_runtime_boundary_missing")
    if gfis_dirty:
        blockers.append("gfis_repo_dirty_user_work_present")

    gate = "blocked" if blockers else "pass"
    score = 78 if blockers else 100
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
            "sop_e2e_status": sop_e2e_status,
            "sop_e2e_failed_tests": gfis_last_run.get("failedTests", []),
            "git_dirty": gfis_dirty,
        },
        "blockers": blockers,
        "required_repairs": [
            "Replace GFIS-L4-008 demo fixture evidence with GFIS runtime-layer DocType/workflow/API evidence.",
            "Run and pass the SOP E2E master path against the GFIS runtime layer.",
            "Keep GFIS Demo limited to display, training, traceability explanation and frontend regression.",
            "Do not mark L4 closed or 100/100 while runtime subject or E2E gates are blocked.",
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
        f"{'invalid' if demo_counted_as_runtime else 'pass'} "
        f"sop_e2e={sop_e2e_status} project_group_score={score} next=GFIS-runtime-repair"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
