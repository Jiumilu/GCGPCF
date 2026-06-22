#!/usr/bin/env python3
"""Validate D90 scoped GCKF heading localization repair."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/localization-debt-gckf-heading-repair-d90-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/localization-debt-gckf-heading-repair-d90-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D90-001.md"


def fail(message: str) -> None:
    print(f"localization_debt_gckf_heading_repair_d90=fail reason={message}")
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
        fail("missing_d90_evidence_or_loop")

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
    if len(changed_files) != 10:
        fail("changed_file_count_not_10")

    current = current_localization()
    current_keys = {
        (finding.get("path"), finding.get("line"))
        for finding in current.get("sample_findings", [])
        if isinstance(finding, dict)
    }

    for source_path in changed_files:
        path = ROOT / source_path
        if not path.exists():
            fail(f"missing_changed_file:{source_path}")
        heading = next((line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("# ")), "")
        if not heading:
            fail(f"missing_h1:{source_path}")
        if not has_chinese(heading):
            fail(f"h1_not_chinese:{source_path}")
        if (source_path, 19) in current_keys:
            fail(f"localization_still_flags_h1:{source_path}")

    delta = evidence.get("delta", {})
    if delta.get("findings") != -10 or delta.get("docs_gc_knowledge_fabric_findings") != -10:
        fail("unexpected_delta")

    print("localization_debt_gckf_heading_repair_d90=pass")
    print(f"changed_files={len(changed_files)}")
    print(f"current_localization_gate={current.get('localization_gate')}")
    print(f"current_findings={current.get('findings')}")
    print(f"execution_mode={evidence.get('execution_mode')}")


if __name__ == "__main__":
    main()
