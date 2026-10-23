#!/usr/bin/env python3
"""Scan active features for close candidates using gpcf_check_evidence --check-only."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts/gpcf_check_evidence.py"
ACTIVE = ROOT / "features/active"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates-only", action="store_true")
    args = parser.parse_args()

    rows = []
    for feature_dir in sorted(ACTIVE.glob("F-*")):
        feature_id = "-".join(feature_dir.name.split("-")[:2])
        result = subprocess.run(
            [sys.executable, str(CHECK), "--check-only", feature_id],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        output = (result.stdout + result.stderr).strip().splitlines()
        line = output[-1] if output else ""
        match = re.search(r"close_candidate=(true|false)", line)
        candidate = bool(match and match.group(1) == "true")
        reasons = ""
        if "reasons=" in line:
            reasons = line.split("reasons=", 1)[1].strip()
        rows.append(
            {
                "id": feature_id,
                "dir": feature_dir.name,
                "close_candidate": candidate,
                "reasons": reasons,
            }
        )

    if args.candidates_only:
        rows = [row for row in rows if row["close_candidate"]]
    print(json.dumps({"count": len(rows), "features": rows}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
