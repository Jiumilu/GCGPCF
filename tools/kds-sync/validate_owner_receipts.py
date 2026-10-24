#!/usr/bin/env python3
"""Validate owner confirmation receipts (routing acknowledgements, not approvals)."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "runtime/owner-receipts.yaml"
REQUIRED = ("ref", "feature", "owner", "status", "required", "evidence_paths", "signed_by", "signed_at")
STATUSES = {"pending", "approved", "rejected", "deferred"}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL validate_owner_receipts: {msg}")


def main() -> int:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    receipts = data.get("receipts")
    if not isinstance(receipts, list) or not receipts:
        fail("receipts must be non-empty list")
    seen: set[str] = set()
    counts: dict[str, int] = {}
    for i, r in enumerate(receipts):
        if not isinstance(r, dict):
            fail(f"receipts[{i}] not mapping")
        for k in REQUIRED:
            if k not in r:
                fail(f"receipts[{i}] missing {k}")
        ref = str(r["ref"])
        if ref in seen:
            fail(f"duplicate ref {ref}")
        seen.add(ref)
        status = r["status"]
        if status not in STATUSES:
            fail(f"{ref} invalid status {status}")
        counts[status] = counts.get(status, 0) + 1
        if not isinstance(r["required"], list) or not r["required"]:
            fail(f"{ref} required must be non-empty list")
        if status == "approved":
            if not str(r["signed_by"]).strip() or not str(r["signed_at"]).strip():
                fail(f"{ref} approved requires signed_by/signed_at")
            for p in r["evidence_paths"]:
                if not (ROOT / p).exists():
                    fail(f"{ref} evidence missing: {p}")
    print(f"owner_receipts=pass count={len(receipts)} statuses={counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
