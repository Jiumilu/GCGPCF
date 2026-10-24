#!/usr/bin/env python3
"""Deterministic goal-health snapshot: gates, features, metrics."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATES = [
    "loop_document_gate.py",
    "validate_contract_matrix.py",
    "validate_xap_error_code_registry.py",
    "validate_contract_version_drift.py",
    "validate_event_package_ref.py",
    "validate_gpcf_2_feature_workspace.py",
    "validate_project_group_caliber_baseline.py",
    "validate_project_group_single_authorization_ledger.py",
    "validate_evidence_rule_version.py",
    "validate_vu_ledger.py",
    "validate_asset_reuse.py",
    "validate_token_source_exceptions.py",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    # loop gate 依赖 live_status 快照；先重建，避免首跑竞态误报
    snapshot_script = ROOT / "tools/kds-sync/build_project_group_live_status_current.py"
    for _ in range(2):
        subprocess.run([sys.executable, str(snapshot_script)], cwd=ROOT, capture_output=True, check=False)

    gate_rows = []
    for name in GATES:
        started = time.time()
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/kds-sync" / name)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        gate_rows.append(
            {
                "gate": name,
                "ok": result.returncode == 0,
                "seconds": round(time.time() - started, 1),
            }
        )

    state = json.loads((ROOT / "runtime/state.json").read_text(encoding="utf-8"))
    queue = json.loads((ROOT / "runtime/queue.json").read_text(encoding="utf-8"))["queue"]
    closed = sum(1 for item in queue if item.get("status") == "closed")

    render = subprocess.run(
        [sys.executable, str(ROOT / "tools/kds-sync/render_project_group_completion.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    match = re.search(r"C_dev\s*=\s*([0-9.]+)%", render.stdout + render.stderr)
    c_dev = float(match.group(1)) if match else None

    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "gates": gate_rows,
        "gates_pass": sum(1 for row in gate_rows if row["ok"]),
        "gates_total": len(gate_rows),
        "active_feature_count": state.get("active_feature_count"),
        "closed_feature_count": closed,
        "C_dev": c_dev,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    return 0 if payload["gates_pass"] == payload["gates_total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
