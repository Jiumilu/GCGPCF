#!/usr/bin/env python3
"""Validate the multi-bundle OKF v0.1 collection."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BUNDLES = [
    ROOT / ".okf/bundles/kds-v0.1",
    ROOT / ".okf/bundles/governance-v0.1",
    ROOT / ".okf/bundles/architecture-v0.1",
]


def fail(reason: str) -> None:
    raise SystemExit(f"okf_collection_gate=fail reason={reason}")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def split_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def validate_bundle(bundle: Path) -> tuple[int, set[str]]:
    if not bundle.exists():
        fail(f"missing_bundle:{rel(bundle)}")
    result = subprocess.run(
        [sys.executable, "tools/kds-sync/validate_okf_bundle.py", "--bundle", str(bundle)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        fail(f"bundle_gate_failed:{rel(bundle)}:{(result.stdout + result.stderr).strip()}")
    sources: set[str] = set()
    count = 0
    for path in bundle.rglob("*.md"):
        if path.name in {"index.md", "log.md"}:
            continue
        meta = split_frontmatter(path)
        if not meta.get("type"):
            continue
        source_path = meta.get("source_path")
        if not source_path:
            fail(f"missing_source_path:{rel(path)}")
        sources.add(source_path)
        count += 1
    if count == 0:
        fail(f"empty_bundle:{rel(bundle)}")
    return count, sources


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", action="append", dest="bundles")
    args = parser.parse_args()

    bundle_paths = [Path(path) for path in args.bundles] if args.bundles else DEFAULT_BUNDLES
    total = 0
    duplicate_sources: set[str] = set()
    seen_sources: set[str] = set()
    bundle_summaries = []
    for bundle in bundle_paths:
        count, sources = validate_bundle(bundle)
        duplicate_sources |= seen_sources & sources
        seen_sources |= sources
        total += count
        bundle_summaries.append(f"{rel(bundle)}:{count}")
    print(
        "okf_collection_gate=pass "
        f"bundles={len(bundle_paths)} "
        f"concepts={total} "
        f"bundle_summaries={','.join(bundle_summaries)} "
        f"duplicate_sources={len(duplicate_sources)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
