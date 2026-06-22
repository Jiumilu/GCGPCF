#!/usr/bin/env python3
"""Validate D113 scoped agent safety matrix localization repair."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/localization-debt-agent-safety-matrix-repair-d113-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/localization-debt-agent-safety-matrix-repair-d113-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D113-001.md"


def fail(message: str) -> None:
    print(f"localization_debt_agent_safety_matrix_repair_d113=fail reason={message}")
    sys.exit(1)


def has_chinese(value: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in value)


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
        fail("missing_d113_evidence_or_loop")

    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    if evidence.get("execution_mode") != "local_evidence_no_write":
        fail("execution_mode_not_no_write")

    boundaries = evidence.get("boundaries", {})
    for key in ("real_kds_api_write", "business_system_writeback", "status_upgrade", "accepted", "integrated", "production_ready"):
        if boundaries.get(key) is not False:
            fail(f"boundary_not_false:{key}")
    if boundaries.get("gfis_real_business_lane") != "repair_required":
        fail("gfis_lane_not_repair_required")

    changed_files = evidence.get("changed_files", [])
    if len(changed_files) != 1:
        fail("changed_file_count_not_1")
    if evidence.get("changed_line_items") != 17:
        fail("changed_line_items_not_17")

    source_path = changed_files[0]
    path = ROOT / source_path
    if not path.exists():
        fail(f"missing_changed_file:{source_path}")
    heading = next((line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("# ")), "")
    if not heading or not has_chinese(heading):
        fail(f"h1_not_chinese:{source_path}")

    current = current_localization()
    target_findings = [
        finding
        for finding in current.get("sample_findings", [])
        if isinstance(finding, dict)
        and finding.get("path") == source_path
    ]
    if target_findings:
        fail("target_findings_remaining")

    if evidence.get("remaining_target_findings") != []:
        fail("remaining_target_findings_not_empty")

    delta = evidence.get("delta", {})
    if delta.get("target_file_findings") != -3:
        fail("unexpected_target_delta")
    if delta.get("all_repo_findings") != 0:
        fail("unexpected_all_repo_delta")
    after = evidence.get("after", {})
    if after.get("target_file_findings") != 0:
        fail("after_target_not_zero")
    if current.get("findings", 0) != after.get("all_repo_findings", 0):
        fail("after_all_repo_mismatch")

    print("localization_debt_agent_safety_matrix_repair_d113=pass")
    print(f"changed_files={len(changed_files)}")
    print(f"changed_line_items={evidence.get('changed_line_items')}")
    print(f"current_localization_gate={current.get('localization_gate')}")
    print(f"current_findings={current.get('findings')}")
    print(f"target_findings={len(target_findings)}")
    print(f"execution_mode={evidence.get('execution_mode')}")


if __name__ == "__main__":
    main()
