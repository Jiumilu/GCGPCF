#!/usr/bin/env python3
"""Validate loop gate readiness across the GPCF project group."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from hashlib import sha1
from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
PROJECT_GROUP_ROOT = ROOT.parent
GATE_PATH = Path("tools/kds-sync/loop_document_gate.py")
GATE_TIMEOUT_SECONDS = 180
GATE_MAX_ATTEMPTS = 3
REPOS = [
    ("GlobalCloud AAAS", PROJECT_GROUP_ROOT / "GlobalCloud AAAS"),
    ("GlobalCloud Brain", PROJECT_GROUP_ROOT / "GlobalCloud Brain"),
    ("GlobalCloud GFIS", PROJECT_GROUP_ROOT / "GlobalCloud GFIS"),
    ("GlobalCloud GPC", PROJECT_GROUP_ROOT / "GlobalCloud GPC"),
    ("GlobalCloud KDS", PROJECT_GROUP_ROOT / "GlobalCloud KDS"),
    ("GlobalCloud MMC", PROJECT_GROUP_ROOT / "GlobalCloud MMC"),
    ("GlobalCloud PKC", PROJECT_GROUP_ROOT / "GlobalCloud PKC"),
    ("GlobalCloud PVAOS", PROJECT_GROUP_ROOT / "GlobalCloud PVAOS"),
    ("GlobalCloud SOP", PROJECT_GROUP_ROOT / "GlobalCloud SOP"),
    ("GlobalCloud Studio", PROJECT_GROUP_ROOT / "GlobalCloud Studio"),
    ("GlobalCloud WAES", PROJECT_GROUP_ROOT / "GlobalCloud WAES"),
    ("GlobalCloud XGD", PROJECT_GROUP_ROOT / "GlobalCloud XGD"),
    ("GlobalCloud XWAIL", PROJECT_GROUP_ROOT / "GlobalCloud XWAIL"),
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
    last_reason = ""
    for attempt in range(1, GATE_MAX_ATTEMPTS + 1):
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
            last_reason = (
                f"{repo_label} loop gate timeout repo_label={repo_label} "
                f"attempt={attempt}/{GATE_MAX_ATTEMPTS} elapsed_sec={elapsed:.3f} "
                f"returncode=timeout{detail}"
            )
            continue
        elapsed = time.monotonic() - started_at
        diagnostic = (
            f"repo_label={repo_label} attempt={attempt}/{GATE_MAX_ATTEMPTS} "
            f"elapsed_sec={elapsed:.3f} returncode={result.returncode}"
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            last_reason = f"{repo_label} loop gate run failed {diagnostic}"
            if result.returncode == 143:
                continue
            if result.returncode != 0:
                return False, last_reason
            return False, f"{repo_label} loop gate output is not valid JSON {diagnostic}"
        if payload.get("gate") != "pass":
            reasons = ",".join(payload.get("gate_reasons") or []) or payload.get("gate", "unknown")
            return False, f"{repo_label} loop gate {diagnostic} status={payload.get('gate', 'unknown')} reasons={reasons}"
        if result.returncode != 0:
            last_reason = f"{repo_label} loop gate run failed {diagnostic}"
            if result.returncode == 143:
                continue
            return False, last_reason
        return True, ""
    return False, last_reason


def gate_invocation_key(repo_path: Path) -> str:
    gate_path = repo_path / GATE_PATH
    if not gate_path.exists():
        return f"missing:{repo_path}"
    try:
        content = gate_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"path:{gate_path}"
    if "Delegate project-group loop gate execution to the GPCF canonical gate" in content:
        digest = sha1(content.encode("utf-8")).hexdigest()
        return f"delegated-gpcf-canonical:{digest}"
    return f"path:{gate_path}"


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
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
    gate_cache: dict[str, tuple[bool, str]] = {}
    for label, path in REPOS:
        checked_repos += 1
        cache_key = gate_invocation_key(path)
        if cache_key in gate_cache:
            ok, cached_reason = gate_cache[cache_key]
            reason = cached_reason.replace("repo_label=", f"repo_label={label}:cached_from:", 1) if cached_reason else ""
        else:
            ok, reason = run_gate(path, label)
            gate_cache[cache_key] = (ok, reason)
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
            f"failed={len(failed)} "
            f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
            f"reasons={joined}"
        )
        return 0

    if failed:
        joined = " ; ".join(failed)
        print(
            "project_group_gate_readiness=fail "
            f"checked_repos={checked_repos} "
            f"passed={passed} "
            f"failed={len(failed)} "
            f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
            f"reasons={joined}"
        )
        return 1
    print(
        "project_group_gate_readiness=pass "
        f"checked_repos={checked_repos} "
        f"passed={passed} "
        "failed=0 "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
        "reasons=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
