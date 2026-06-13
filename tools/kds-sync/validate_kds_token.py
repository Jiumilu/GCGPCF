#!/usr/bin/env python3
"""Validate KDS development-space token configuration without leaking secrets."""

from __future__ import annotations

import hashlib
import os
import shlex
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_FILE = Path("/Users/lujunxiang/.globalcloud/kds.env")


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        try:
            parsed = shlex.split(value, posix=True)
        except ValueError:
            parsed = [value.strip().strip('"').strip("'")]
        os.environ[key] = parsed[0] if parsed else ""


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
    env_file = Path(os.environ.get("KDS_ENV_FILE", str(DEFAULT_ENV_FILE)))
    load_env_file(env_file)
    token = os.environ.get("KDS_DEVELOPMENT_SPACE_TOKEN", "")
    owner = os.environ.get("KDS_TOKEN_OWNER", "")
    space = os.environ.get("KDS_SPACE_NAME", "")
    scope = os.environ.get("KDS_TOKEN_SCOPE", "")
    failures = []
    if not token:
        failures.append("missing KDS_DEVELOPMENT_SPACE_TOKEN")
    elif token.startswith("REPLACE_WITH_") or token in {"TODO", "CHANGE_ME", "your-token"}:
        failures.append("KDS_DEVELOPMENT_SPACE_TOKEN is still a placeholder")
    if owner != "lujunxiang":
        failures.append("KDS_TOKEN_OWNER must be lujunxiang")
    if space != "开发":
        failures.append("KDS_SPACE_NAME must be 开发")
    required_scopes = {"read", "write", "edit"}
    forbidden_scopes = {"delete", "admin", "member_manage", "permission_manage"}
    actual_scopes = {item.strip() for item in scope.split(",") if item.strip()}
    if not required_scopes.issubset(actual_scopes):
        failures.append("KDS_TOKEN_SCOPE must include read,write,edit")
    forbidden_present = sorted(forbidden_scopes.intersection(actual_scopes))
    if forbidden_present:
        failures.append(
            "KDS_TOKEN_SCOPE must not include " + ",".join(forbidden_present)
        )
    if env_file.exists():
        mode = stat.S_IMODE(env_file.stat().st_mode)
        if mode != 0o600:
            failures.append(f"KDS_ENV_FILE permissions must be 600, got {oct(mode)}")
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
