#!/usr/bin/env python3
"""Validate D123 GCKF P0 closure packet precheck evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-closure-packet-precheck-d123-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-closure-packet-precheck-d123-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D123-001.md"
PILOT_CHECKLIST = ROOT / "docs/gc-knowledge-fabric/pilot-rollout-checklist-v0.1.md"


def fail(message: str) -> None:
    print(f"gckf_p0_closure_packet_precheck_d123=fail reason={message}")
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
    require(EVIDENCE_JSON.exists() and EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d123_artifacts")
    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))

    require(evidence.get("execution_mode") == "local_evidence_no_write", "execution_mode_not_no_write")
    require(evidence.get("precheck_status") == "review_ready_with_hold", "precheck_status_mismatch")

    coverage = evidence.get("task_package_coverage", {})
    require(coverage.get("covered_count") == 7, "covered_count_not_7")
    require(coverage.get("total_count") == 7, "total_count_not_7")
    require(coverage.get("covered_task_packages") == ["T0", "T1", "T2", "T3", "T4", "T5", "T6"], "covered_task_packages_mismatch")

    d122_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_skeleton_baseline_d122.py")
    require(d122_output.startswith("gckf_p0_skeleton_baseline_d122=pass"), "d122_validator_not_pass")

    d18_output = run_command("python3", "scripts/api/validate_gckf_p0_acceptance_packet_dry_run.py")
    require(d18_output.startswith("gckf_p0_acceptance_packet_dry_run=pass"), "d18_validator_not_pass")

    d19_output = run_command("python3", "scripts/api/validate_gckf_p0_acceptance_packet_ledger_dry_run.py")
    require(d19_output.startswith("gckf_p0_acceptance_packet_ledger_dry_run=pass"), "d19_validator_not_pass")

    d20_output = run_command("python3", "scripts/api/validate_gckf_p0_closure_readiness_dry_run.py")
    require(d20_output.startswith("gckf_p0_closure_readiness_dry_run=pass"), "d20_validator_not_pass")
    require("status=review_ready_candidate" in d20_output, "d20_status_not_review_ready_candidate")

    d21_output = run_command("python3", "scripts/api/validate_gckf_p0_human_review_checklist_dry_run.py")
    require(d21_output.startswith("gckf_p0_human_review_checklist_dry_run=pass"), "d21_validator_not_pass")
    require("pending_outcomes=4" in d21_output, "d21_pending_outcomes_changed")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    holds = evidence.get("hold_reasons", [])
    require(len(holds) == 4, "hold_reason_count_not_4")
    hold_ids = [item.get("id") for item in holds]
    require(hold_ids == ["H1", "H2", "H3", "H4"], "hold_ids_mismatch")

    pilot_text = read(PILOT_CHECKLIST)
    for phrase in ["| C-01 |", "| C-02 |", "| C-03 |", "| C-04 |", "| C-05 |", "| C-06 |", "| C-07 |", "待确认", "待执行"]:
        require(phrase in pilot_text, f"pilot_checklist_missing_phrase:{phrase}")

    non_claims = evidence.get("non_claims", [])
    require(len(non_claims) >= 3, "non_claims_too_short")

    print("gckf_p0_closure_packet_precheck_d123=pass")
    print(f"precheck_status={evidence.get('precheck_status')}")
    print(f"covered_task_packages={coverage.get('covered_count')}/{coverage.get('total_count')}")
    print("closure_chain=D18,D19,D20,D21,D122")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print(f"execution_mode={evidence.get('execution_mode')}")


if __name__ == "__main__":
    main()
