#!/usr/bin/env python3
"""Validate the Headroom LCX real-measurement authorization window grant evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_authorization_window_grant.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-23",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    grant = load_json(E_JSON)
    md = read(E_MD)
    loop = read(LOOP)
    runner = read(RUNNER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("build_headroom_lcx_real_measurement_authorization_window_grant" in runner, "runner must build authorization window grant")

    require(grant.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623", "invalid evidence id")
    require(grant.get("status") == "real_measurement_authorization_window_granted_precheck_only", "invalid status")
    require(grant.get("project_count") == 15, "project count mismatch")
    require(grant.get("real_measurement_window_granted") is True, "window must be granted")
    require(grant.get("real_measurement_open") is False, "real measurement must remain closed")
    require(grant.get("production_branch_blocked") is True, "production branch must remain blocked")
    require(grant.get("production_token_measurement_allowed") is False, "token measurement must remain false")
    require(grant.get("measured_production_tokens") is False, "measured tokens must remain false")
    require(grant.get("production_admission_gate") is False, "production gate must remain false")
    require(grant.get("accepted") is False, "accepted must remain false")
    require(grant.get("integrated") is False, "integrated must remain false")
    require(grant.get("production_ready") is False, "production ready must remain false")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623",
        "real_measurement_authorization_window_granted_precheck_only",
        "real_measurement_window_granted | `true`",
        "real_measurement_open | `false`",
        "production_branch_blocked | `true`",
        "production_token_measurement_allowed | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"md missing phrase: {phrase}")

    for phrase in [
        "authorization window grant",
        "build_headroom_lcx_real_measurement_authorization_window_grant.py",
        "validate_headroom_lcx_real_measurement_authorization_window_grant.py",
        "granted but still precheck-only",
    ]:
        require(phrase in loop, f"loop missing phrase: {phrase}")

    print(
        "headroom_lcx_real_measurement_authorization_window_grant=pass "
        "project_count=15 real_measurement_window_granted=true real_measurement_open=false "
        "production_branch_blocked=true production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
