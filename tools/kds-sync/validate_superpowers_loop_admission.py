#!/usr/bin/env python3
"""Validate Superpowers as a candidate LOOP execution discipline."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "02-governance/loop/LOOP_CAPABILITY_REGISTRY.md"
PROJECT_GROUP_GATE = ROOT / "tools/kds-sync/validate_loop_project_group_gate_readiness.py"
PROJECT_GROUP_GATE_TIMEOUT_SECONDS = 180

REQUIRED_REGISTRY_PHRASES = [
    "method.superpowers.loop_execution_discipline",
    "method/skill wrapper",
    "candidate",
    "medium",
    "SOP + GPCF",
    "planning,tdd,debugging,verification,review,independent_subtasks",
    "auto_commit,auto_push,production_write,cross_repo_write,status_promotion,release,deployment",
    "validate_superpowers_loop_admission.py + validate_loop_project_group_gate_readiness.py",
    "disabled / repair_required",
]

FORBIDDEN_CLAIMS = [
    "能力登记授权 commit",
    "能力登记授权 push",
    "能力登记授权 production write",
    "能力登记授权 external API write",
    "能力登记授权 schema sync",
    "能力登记授权 deployment",
    "能力登记授权 accepted",
    "能力登记授权 integrated",
    "default_enabled: true",
    "auto_commit_allowed: true",
    "auto_push_allowed: true",
    "production_write_allowed: true",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_superpowers_loop_admission: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def validate_registry() -> None:
    registry = read(REGISTRY)
    for phrase in REQUIRED_REGISTRY_PHRASES:
        require(phrase in registry, f"registry missing phrase: {phrase}")
    for phrase in FORBIDDEN_CLAIMS:
        require(phrase not in registry, f"registry contains forbidden claim: {phrase}")


def run_project_group_gate() -> None:
    require(PROJECT_GROUP_GATE.exists(), f"missing project group gate: {PROJECT_GROUP_GATE}")
    started_at = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_GROUP_GATE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=PROJECT_GROUP_GATE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started_at
        output = ((exc.stdout or "") + (exc.stderr or "")).strip()
        detail = f" output={output[:300]}" if output else ""
        raise SystemExit(
            "FAIL validate_superpowers_loop_admission: "
            "project group gate failed:\n"
            f"project_group_gate_readiness=fail elapsed_sec={elapsed:.3f} "
            f"returncode=timeout{detail}"
        )
    elapsed = time.monotonic() - started_at
    output = (result.stdout + result.stderr).strip()
    diagnostic = f"elapsed_sec={elapsed:.3f} returncode={result.returncode}"
    require(result.returncode == 0, f"project group gate failed:\n{output}\n{diagnostic}")
    require(
        "project_group_gate_readiness=pass" in output,
        f"project group gate did not pass:\n{output}\n{diagnostic}",
    )
    print(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-group-gate", action="store_true")
    args = parser.parse_args()

    validate_registry()
    if args.project_group_gate:
        run_project_group_gate()
    print("superpowers_loop_admission=pass status=candidate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
