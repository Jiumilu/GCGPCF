#!/usr/bin/env python3
"""Run the GlobalCloud document governance command set."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

COMMANDS = [
    ["python3", "tools/kds-sync/document_control.py"],
    ["python3", "tools/kds-sync/check_document_pollution.py"],
    ["python3", "tools/kds-sync/validate_kds_token.py"],
    ["python3", "tools/kds-sync/kds_conflict_guard.py"],
    ["python3", "tools/kds-sync/loop_document_gate.py"],
]


def main() -> int:
    failures = 0
    for command in COMMANDS:
        print("$", " ".join(command))
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode != 0:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
