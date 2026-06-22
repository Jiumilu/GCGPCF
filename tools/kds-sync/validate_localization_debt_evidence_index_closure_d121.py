#!/usr/bin/env python3
"""Validate D121 evidence-index localization closure."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/localization-debt-evidence-index-closure-d121-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/localization-debt-evidence-index-closure-d121-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D121-001.md"


def fail(message: str) -> None:
    print(f"localization_debt_evidence_index_closure_d121=fail reason={message}")
    sys.exit(1)


def current_localization() -> dict[str, object]:
    result = subprocess.run(
        [
            sys.executable,
            "tools/kds-sync/check_chinese_localization_gate.py",
            "--json",
            "--max-findings",
            "10000",
        ],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if not result.stdout.strip():
        fail("localization_gate_no_json_output")
    return json.loads(result.stdout)


def main() -> None:
    if not EVIDENCE_JSON.exists() or not EVIDENCE_MD.exists() or not LOOP_MD.exists():
        fail("missing_d121_evidence_or_loop")

    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    if evidence.get("execution_mode") != "local_evidence_no_write":
        fail("execution_mode_not_no_write")

    boundaries = evidence.get("boundaries", {})
    for key in (
        "real_kds_api_write",
        "business_system_writeback",
        "status_upgrade",
        "accepted",
        "integrated",
        "production_ready",
    ):
        if boundaries.get(key) is not False:
            fail(f"boundary_not_false:{key}")
    if boundaries.get("gfis_real_business_lane") != "repair_required":
        fail("gfis_lane_not_repair_required")

    changed_files = evidence.get("changed_files", [])
    if changed_files != ["docs/harness/evidence/evidence-index.md"]:
        fail("changed_files_not_scoped_to_evidence_index")
    if evidence.get("changed_line_items") != 22:
        fail("changed_line_items_not_22")

    current = current_localization()
    if current.get("localization_gate") != "pass":
        fail("localization_gate_not_pass")
    if current.get("findings") != 0:
        fail("localization_findings_not_zero")
    if current.get("findings") != evidence.get("after", {}).get("all_repo_findings"):
        fail("after_all_repo_mismatch")
    if evidence.get("remaining_target_findings") != []:
        fail("remaining_target_findings_not_empty")

    print("localization_debt_evidence_index_closure_d121=pass")
    print(f"changed_files={len(changed_files)}")
    print(f"changed_line_items={evidence.get('changed_line_items')}")
    print(f"current_localization_gate={current.get('localization_gate')}")
    print(f"current_findings={current.get('findings')}")
    print(f"remaining_target_findings={len(evidence.get('remaining_target_findings', []))}")
    print(f"execution_mode={evidence.get('execution_mode')}")


if __name__ == "__main__":
    main()
