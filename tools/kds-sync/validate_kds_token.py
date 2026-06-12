#!/usr/bin/env python3
"""Validate KDS development-space token configuration without leaking secrets."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def contains_token(token: str) -> list[str]:
    if not token:
        return []
    leaks = []
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if token in text:
            leaks.append(path.relative_to(ROOT).as_posix())
    return leaks


def main() -> int:
    token = os.environ.get("KDS_DEVELOPMENT_SPACE_TOKEN", "")
    owner = os.environ.get("KDS_TOKEN_OWNER", "")
    space = os.environ.get("KDS_SPACE_NAME", "")
    scope = os.environ.get("KDS_TOKEN_SCOPE", "")
    failures = []
    if not token:
        failures.append("missing KDS_DEVELOPMENT_SPACE_TOKEN")
    if owner != "lujunxiang":
        failures.append("KDS_TOKEN_OWNER must be lujunxiang")
    if space != "开发":
        failures.append("KDS_SPACE_NAME must be 开发")
    required_scopes = {"read", "write", "edit"}
    actual_scopes = {item.strip() for item in scope.split(",") if item.strip()}
    if not required_scopes.issubset(actual_scopes):
        failures.append("KDS_TOKEN_SCOPE must include read,write,edit")
    leaks = contains_token(token)
    if leaks:
        failures.append("token plaintext leaked: " + ", ".join(leaks[:20]))
    if failures:
        print("kds_token=blocked")
        for failure in failures:
            print(f"- {failure}")
        return 1
    fingerprint = hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]
    print(f"kds_token=pass fingerprint={fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

