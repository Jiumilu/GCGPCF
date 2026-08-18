#!/usr/bin/env python3
"""Emit the deterministic GKE-001 Release 0 KDS operation matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml


def normalized_matrix(path: Path) -> bytes:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    rows = []
    for declared in document["x-kds-canonical-operations"]:
        method = declared["method"]
        route = declared["path"]
        operation = document["paths"][route][method.lower()]
        rows.append(
            {
                "method": method,
                "path": route,
                "request": operation["requestBody"]["content"]["application/json"]["schema"],
                "response": operation["responses"]["200"]["content"]["application/json"]["schema"],
            }
        )
    return json.dumps(rows, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--sha256", action="store_true")
    parser.add_argument("--expect-sha256")
    args = parser.parse_args()

    payload = normalized_matrix(args.candidate)
    digest = hashlib.sha256(payload).hexdigest()
    if args.expect_sha256 and digest != args.expect_sha256:
        parser.error(f"matrix SHA-256 mismatch: {digest}")
    print(digest if args.sha256 else payload.decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
