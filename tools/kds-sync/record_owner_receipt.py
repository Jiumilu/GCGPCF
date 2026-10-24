#!/usr/bin/env python3
"""Record an owner receipt into runtime/owner-receipts.yaml (no fabrication; requires signer)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "runtime/owner-receipts.yaml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True)
    parser.add_argument("--status", required=True, choices=["pending", "approved", "rejected", "deferred"])
    parser.add_argument("--signed-by", default="")
    parser.add_argument("--signed-at", default="")
    parser.add_argument("--evidence", default="", help="comma-separated repo-relative paths")
    parser.add_argument("--note", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    receipts = data.get("receipts", [])
    target = next((r for r in receipts if r.get("ref") == args.ref), None)
    if target is None:
        raise SystemExit(f"FAIL: unknown ref {args.ref}")
    if args.status == "approved" and not (args.signed_by.strip() and args.signed_at.strip()):
        raise SystemExit("FAIL: approved requires --signed-by and --signed-at")
    evidence = [p.strip() for p in args.evidence.split(",") if p.strip()]
    for p in evidence:
        if not (ROOT / p).exists():
            raise SystemExit(f"FAIL: evidence missing {p}")
    target.update({"status": args.status, "signed_by": args.signed_by, "signed_at": args.signed_at,
                   "evidence_paths": evidence})
    if args.note:
        target["note"] = args.note
    text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if args.dry_run:
        print(text)
        return 0
    REGISTRY.write_text(text, encoding="utf-8")
    result = subprocess.run([sys.executable, str(ROOT / "tools/kds-sync/validate_owner_receipts.py")], cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
