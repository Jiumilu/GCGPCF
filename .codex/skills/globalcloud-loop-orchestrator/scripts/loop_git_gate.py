#!/usr/bin/env python3
"""Git gate for GlobalCloud Loop rounds."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SENSITIVE_PATTERNS = [
    re.compile(r"(^|/)\.env($|\.)"),
    re.compile(r"TOKEN", re.IGNORECASE),
    re.compile(r"SECRET", re.IGNORECASE),
    re.compile(r"\.(pem|key|p12)$", re.IGNORECASE),
    re.compile(r"(^|/)id_rsa"),
]

SENSITIVE_ALLOW = {".env.example"}

SENSITIVE_PATH_ALLOW_PATTERNS = [
    # Controlled fixture/evidence files that document sanitized-token checks.
    # This only avoids filename false positives; real token/secret paths remain blocked.
    re.compile(r"(^|/)headroom-lcx-sanitized-token-fixture-extension-\d{8}\.(md|json)$"),
]


def run(repo: Path, args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def git(repo: Path, args: list[str]) -> str:
    return run(repo, args)[1]


def is_sensitive(path: str) -> bool:
    normalized_path = path.strip('"')
    name = Path(normalized_path).name
    if name in SENSITIVE_ALLOW:
        return False
    if any(pattern.search(normalized_path) for pattern in SENSITIVE_PATH_ALLOW_PATTERNS):
        return False
    return any(pattern.search(normalized_path) for pattern in SENSITIVE_PATTERNS)


def ahead_behind(repo: Path, upstream: str) -> tuple[int | None, int | None]:
    if not upstream:
        return None, None
    code, out, _ = run(repo, ["rev-list", "--left-right", "--count", f"HEAD...{upstream}"])
    if code != 0 or not out:
        return None, None
    left, right = out.split()[:2]
    return int(left), int(right)


def inspect(repo: Path) -> dict[str, object]:
    repo = repo.resolve()
    inside = run(repo, ["rev-parse", "--is-inside-work-tree"])[1] == "true"
    if not inside:
        return {"repo": str(repo), "gate": "blocked", "reason": "not a git repository"}

    branch = git(repo, ["branch", "--show-current"]) or "(detached)"
    head = git(repo, ["rev-parse", "--short", "HEAD"])
    upstream = git(repo, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    status_lines = git(repo, ["status", "--porcelain"]).splitlines()
    untracked = [line[3:] for line in status_lines if line.startswith("?? ")]
    sensitive = [path for path in untracked if is_sensitive(path)]
    ahead, behind = ahead_behind(repo, upstream)
    diff_check_code, diff_check_out, diff_check_err = run(repo, ["diff", "--check", "--", "."])

    dirty = bool(status_lines)
    gate = "pass"
    reasons: list[str] = []
    if sensitive:
        gate = "blocked"
        reasons.append("untracked sensitive files present")
    elif diff_check_code != 0:
        gate = "rework_required"
        reasons.append("git diff --check failed")
    elif dirty:
        gate = "partial"
        reasons.append("working tree dirty")
    elif ahead and ahead > 0:
        gate = "partial"
        reasons.append("local commits not pushed")
    if behind and behind > 0:
        gate = "blocked"
        reasons.append("branch is behind upstream")

    return {
        "repo": str(repo),
        "branch": branch,
        "upstream": upstream or None,
        "head": head,
        "dirty": dirty,
        "ahead": ahead,
        "behind": behind,
        "untracked_sensitive": sensitive,
        "diff_check": "pass" if diff_check_code == 0 else "fail",
        "diff_check_output": "\n".join(x for x in [diff_check_out, diff_check_err] if x),
        "gate": gate,
        "reasons": reasons,
    }


def main(argv: list[str]) -> int:
    repo = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    result = inspect(repo)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("gate") in {"pass", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
