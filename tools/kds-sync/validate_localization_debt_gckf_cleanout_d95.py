#!/usr/bin/env python3
"""Validate D95 scoped GCKF localization debt cleanout."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/localization-debt-gckf-cleanout-d95-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/localization-debt-gckf-cleanout-d95-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D95-001.md"


def fail(message: str) -> None:
    print(f"localization_debt_gckf_cleanout_d95=fail reason={message}")
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
        fail("missing_d95_evidence_or_loop")

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
    if len(changed_files) != 2:
        fail("changed_file_count_not_2")
    if evidence.get("changed_line_items") != 8:
        fail("changed_line_items_not_8")

    for source_path in changed_files:
        path = ROOT / source_path
        if not path.exists():
            fail(f"missing_changed_file:{source_path}")

    current = current_localization()
    gckf_findings = [
        finding
        for finding in current.get("sample_findings", [])
        if isinstance(finding, dict)
        and str(finding.get("path", "")).startswith("docs/gc-knowledge-fabric/")
    ]
    if gckf_findings:
        fail("gckf_findings_remaining")

    delta = evidence.get("delta", {})
    if delta.get("docs_gc_knowledge_fabric_findings") != -5:
        fail("unexpected_gckf_delta")
    after = evidence.get("after", {})
    if after.get("docs_gc_knowledge_fabric_findings") != 0:
        fail("after_gckf_not_zero")

    print("localization_debt_gckf_cleanout_d95=pass")
    print(f"changed_files={len(changed_files)}")
    print(f"changed_line_items={evidence.get('changed_line_items')}")
    print(f"current_localization_gate={current.get('localization_gate')}")
    print(f"current_findings={current.get('findings')}")
    print(f"current_gckf_findings={len(gckf_findings)}")
    print(f"execution_mode={evidence.get('execution_mode')}")


if __name__ == "__main__":
    main()
