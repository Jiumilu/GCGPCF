#!/usr/bin/env python3
"""Validate loop gate readiness across the GPCF project group."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_GROUP_ROOT = ROOT.parent
GATE_PATH = Path("tools/kds-sync/loop_document_gate.py")
GATE_TIMEOUT_SECONDS = 90
REPOS = [
    ("GlobalCloud Brain", PROJECT_GROUP_ROOT / "GlobalCloud Brain"),
    ("GlobalCloud GFIS", PROJECT_GROUP_ROOT / "GlobalCloud GFIS"),
    ("GlobalCloud GPC", PROJECT_GROUP_ROOT / "GlobalCloud GPC"),
    ("GlobalCloud KDS", PROJECT_GROUP_ROOT / "GlobalCloud KDS"),
    ("GlobalCloud MMC", PROJECT_GROUP_ROOT / "GlobalCloud MMC"),
    ("GlobalCloud PKC", PROJECT_GROUP_ROOT / "GlobalCloud PKC"),
    ("GlobalCloud PVAOS", PROJECT_GROUP_ROOT / "GlobalCloud PVAOS"),
    ("GlobalCloud Studio", PROJECT_GROUP_ROOT / "GlobalCloud Studio"),
    ("GlobalCloud WAES", PROJECT_GROUP_ROOT / "GlobalCloud WAES"),
    ("GlobalCloud XGD", PROJECT_GROUP_ROOT / "GlobalCloud XGD"),
    ("GlobalCloud XiaoC", PROJECT_GROUP_ROOT / "GlobalCloud XiaoC"),
    ("GlobalCloud XiaoG", PROJECT_GROUP_ROOT / "GlobalCloud XiaoG"),
    ("GlobalCoud GPCF", PROJECT_GROUP_ROOT / "GlobalCoud GPCF"),
    ("WAS世界资产体系", PROJECT_GROUP_ROOT / "WAS世界资产体系"),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def run_gate(repo_path: Path, repo_label: str) -> tuple[bool, str]:
    gate_path = repo_path / GATE_PATH
    if not gate_path.exists():
        return False, f"{repo_label} missing {GATE_PATH.as_posix()}"
    env = os.environ.copy()
    env["GPCF_PROJECT_GROUP_GATE_DELEGATED"] = "1"
    started_at = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, "tools/kds-sync/loop_document_gate.py", "--check-only"],
            cwd=repo_path,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=GATE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started_at
        output = ((exc.stdout or "") + (exc.stderr or "")).strip()
        detail = f" output={output[:300]}" if output else ""
        return (
            False,
            f"{repo_label} loop gate timeout repo_label={repo_label} "
            f"elapsed_sec={elapsed:.3f} returncode=timeout{detail}",
        )
    elapsed = time.monotonic() - started_at
    diagnostic = f"repo_label={repo_label} elapsed_sec={elapsed:.3f} returncode={result.returncode}"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        if result.returncode != 0:
            return False, f"{repo_label} loop gate run failed {diagnostic}"
        return False, f"{repo_label} loop gate output is not valid JSON {diagnostic}"
    if payload.get("gate") != "pass":
        reasons = ",".join(payload.get("gate_reasons") or []) or payload.get("gate", "unknown")
        return False, f"{repo_label} loop gate {diagnostic} status={payload.get('gate', 'unknown')} reasons={reasons}"
    if result.returncode != 0:
        return False, f"{repo_label} loop gate run failed {diagnostic}"
    return True, ""


def main() -> int:
    failed: list[str] = []
    watch_only: list[str] = []
    checked_repos = 0
    passed = 0
    watchable_reasons = {
        "missing_metadata",
        "localization_debt",
        "hard_failure:loop_engineering_five_direction",
        "hard_failure:kds_mirror_coverage_gap",
        "kds_mirror_coverage_gap",
    }
    for label, path in REPOS:
        if path == ROOT:
            continue
        checked_repos += 1
        ok, reason = run_gate(path, label)
        if ok:
            passed += 1
        else:
            failed.append(reason)
            payload = reason.split("reasons=", 1)[-1]
            parts = set(part.strip() for part in payload.split(",") if part.strip())
            if parts and parts.issubset(watchable_reasons):
                watch_only.append(reason)

    if failed and len(failed) == len(watch_only):
        joined = " ; ".join(failed)
        print(
            "project_group_gate_readiness=watch_required "
            f"checked_repos={checked_repos} "
            f"passed={passed} "
            f"failed={len(failed)} reasons={joined}"
        )
        return 0

    if failed:
        joined = " ; ".join(failed)
        print(
            "project_group_gate_readiness=fail "
            f"checked_repos={checked_repos} "
            f"passed={passed} "
            f"failed={len(failed)} reasons={joined}"
        )
        return 1
    print(
        "project_group_gate_readiness=pass "
        f"checked_repos={checked_repos} "
        f"passed={passed} "
        "failed=0 reasons=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
