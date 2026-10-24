#!/usr/bin/env python3
"""Validate token-source exception registry (design tokens, not credentials)."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "runtime/token-source-exceptions.yaml"
REQUIRED = ("id", "project", "file", "status", "reason", "owner", "evidence", "reviewer")
STATUSES = {"candidate", "approved", "unresolved"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_token_source_exceptions: {message}")


def main() -> int:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    exceptions = data.get("exceptions")
    if not isinstance(exceptions, list) or not exceptions:
        fail("exceptions list must be non-empty")
    seen: set[str] = set()
    for index, item in enumerate(exceptions):
        label = f"exceptions[{index}]"
        if not isinstance(item, dict):
            fail(f"{label} must be a mapping")
        for key in REQUIRED:
            if not str(item.get(key, "")).strip():
                fail(f"{label} missing {key}")
        exception_id = str(item["id"])
        if exception_id in seen:
            fail(f"duplicate id: {exception_id}")
        seen.add(exception_id)
        if item["status"] not in STATUSES:
            fail(f"{exception_id} invalid status: {item['status']}")
        evidence = ROOT / str(item["evidence"])
        if not evidence.exists():
            fail(f"{exception_id} evidence missing: {item['evidence']}")
    print(
        "token_source_exceptions=pass "
        f"count={len(exceptions)} statuses="
        + ",".join(sorted({str(item['status']) for item in exceptions}))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
