#!/usr/bin/env python3
"""Guard against uncontrolled Git/KDS mirror divergence."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KDS_ROOT = ROOT / ".kds/development-space"
SYNC_REGISTER = ROOT / "09-status/kds-development-space-sync-register.md"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_register() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if not SYNC_REGISTER.exists():
        return rows
    for line in SYNC_REGISTER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| GPCF-DOC-"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 3:
            rows.append((cells[1], cells[2]))
    return rows


def main() -> int:
    missing = []
    mismatch = []
    for source_rel, kds_rel in parse_register():
        source = ROOT / source_rel
        mirror = KDS_ROOT / kds_rel
        if not source.exists():
            missing.append(f"missing source: {source_rel}")
            continue
        if not mirror.exists():
            missing.append(f"missing mirror: {kds_rel}")
            continue
        if sha(source) != sha(mirror):
            mismatch.append(f"{source_rel} != {kds_rel}")
    if missing or mismatch:
        print("kds_conflict_guard=blocked")
        for item in missing[:50]:
            print(item)
        for item in mismatch[:50]:
            print(item)
        return 1
    print("kds_conflict_guard=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

