#!/usr/bin/env python3
"""Read-only gate for frontmatter integrity in the KDS sync chain."""

from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNERSHIP_DOC = ROOT / "tools" / "kds-sync" / "FRONTMATTER_OWNERSHIP.md"

CRITICAL_KEYS = [
    "doc_id",
    "title",
    "project",
    "related_projects",
    "domain",
    "status",
    "version",
    "owner",
    "kds_space",
    "kds_path",
    "source_path",
    "sync_direction",
    "last_reviewed",
    "supersedes",
    "superseded_by",
]

FALLBACK_PROTECTED_PATH_GLOBS = [
    "09-status/globalcloud-document-control-register.md",
    "09-status/kds-development-space-sync-register.md",
    "09-status/document-deprecation-register.md",
    "09-status/globalcloud-document-health-report.md",
    ".kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-control-register.md",
    ".kds/development-space/开发/91-治理与验收/09-status/kds-development-space-sync-register.md",
    ".kds/development-space/开发/91-治理与验收/09-status/document-deprecation-register.md",
    ".kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-health-report.md",
]
OWNERSHIP_PATH_ROW_RE = re.compile(r"^\|\s*([^|]+)\s*\|")


def load_owned_frontmatter_paths() -> list[str]:
    try:
        text = OWNERSHIP_DOC.read_text(encoding="utf-8")
    except FileNotFoundError:
        return FALLBACK_PROTECTED_PATH_GLOBS.copy()

    in_ownership_table = False
    collected: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        if not in_ownership_table:
            if line.strip().startswith("| 路径 |"):
                in_ownership_table = True
            continue

        if line.startswith("| ---"):
            continue
        if not line.startswith("|"):
            if collected:
                break
            continue

        match = OWNERSHIP_PATH_ROW_RE.match(line)
        if not match:
            continue
        raw_path = match.group(1).strip()
        if not raw_path:
            continue
        cleaned_path = raw_path.strip("`")
        if cleaned_path and cleaned_path not in seen:
            collected.append(cleaned_path)
            seen.add(cleaned_path)

    if not collected:
        return FALLBACK_PROTECTED_PATH_GLOBS.copy()
    return collected


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        return ""
    return result.stdout


def changed_paths(base_ref: str) -> set[str]:
    tracked = run(["git", "-C", str(ROOT), "diff", "--name-only", base_ref, "--", "*.md"]).splitlines()
    untracked = run(["git", "-C", str(ROOT), "ls-files", "--others", "--exclude-standard", "--", "*.md"]).splitlines()
    return set(p for p in tracked + untracked if p)


def read_frontmatter_from_text(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    block = text[4:end]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def frontmatter_of(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    return read_frontmatter_from_text(text)


def frontmatter_of_ref(base_ref: str, relpath: str) -> dict[str, str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{base_ref}:{relpath}"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return {}
    return read_frontmatter_from_text(result.stdout)


def protected_match(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def critical_diff(current: dict[str, str], base: dict[str, str]) -> list[str]:
    return [key for key in CRITICAL_KEYS if current.get(key) != base.get(key)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-ref",
        default="HEAD",
        help="Git base reference for drift comparison (default: HEAD).",
    )
    parser.add_argument(
        "--changed-file-list",
        default="",
        help="Optional file containing one changed path per line.",
    )
    parser.add_argument(
        "--allowed-frontmatter-write",
        action="append",
        default=[],
        help="Glob that allows frontmatter drift on protected paths.",
    )
    parser.add_argument(
        "--emit-protected-paths",
        action="store_true",
        help="Print controlled frontmatter paths and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    allowed = args.allowed_frontmatter_write
    protected_globs = load_owned_frontmatter_paths()

    if args.emit_protected_paths:
        for pattern in protected_globs:
            print(pattern)
        return 0

    if args.changed_file_list:
        changed = {line.strip() for line in Path(args.changed_file_list).read_text(encoding="utf-8").splitlines() if line.strip()}
    else:
        changed = changed_paths(args.base_ref)

    if not changed:
        print("frontmatter_gate=pass")
        return 0

    failures: list[str] = []
    for rel in sorted(changed):
        cur = frontmatter_of(ROOT / rel)
        base = frontmatter_of_ref(args.base_ref, rel)
        is_protected = protected_match(rel, protected_globs)
        if not is_protected:
            continue
        drift = critical_diff(cur, base)
        if not drift:
            continue
        if any(fnmatch.fnmatch(rel, pattern) for pattern in allowed):
            continue
        failures.append(f"{rel}: protected frontmatter drift -> {drift}")

    if failures:
        print("frontmatter_gate=rework_required")
        print("protected_frontmatter_drift:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("frontmatter_gate=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
