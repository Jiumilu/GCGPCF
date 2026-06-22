#!/usr/bin/env python3
"""Read-only precheck for scoped LOOP baseline document-control sync."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_CONTROL = ROOT / "tools/kds-sync/document_control.py"
README = ROOT / "02-governance/loop/README.md"

TARGET_DOCS = [
    "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md",
    "02-governance/loop/LOOP_CAPABILITY_REGISTRY.md",
]

TARGET_VALIDATORS = [
    "tools/kds-sync/validate_loop_engineering_master_plan.py",
    "tools/kds-sync/validate_loop_capability_registry.py",
]

SCOPE_PATHS = TARGET_DOCS + [
    "02-governance/loop/README.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_baseline_sync_readiness: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    require(result.returncode == 0, f"command failed: {' '.join(command)}\n{result.stdout}{result.stderr}")
    return (result.stdout + result.stderr).strip()


def require_controlled_doc(source_path: str) -> None:
    text = read(ROOT / source_path)
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{source_path} missing controlled marker: {phrase}")


def main() -> int:
    document_control = read(DOCUMENT_CONTROL)
    readme = read(README)

    require("SCOPE_ENV = \"DOCUMENT_CONTROL_SCOPE\"" in document_control, "document_control missing scoped env support")
    require("parse_scope_paths()" in document_control, "document_control missing scoped path parser")
    require("mirror_scope_to_kds(scoped_records + register_records)" in document_control, "document_control missing scoped mirror call")
    require("mirror_to_kds(records)" in document_control, "document_control full sync path must remain detectable")

    for source_path in TARGET_DOCS:
        require_controlled_doc(source_path)
        require(source_path in readme, f"README missing target doc entry: {source_path}")

    validator_outputs = [run([sys.executable, validator]) for validator in TARGET_VALIDATORS]

    scope_value = ",".join(SCOPE_PATHS)
    print(
        "loop_baseline_sync_readiness=pass "
        "mode=read_only "
        f"scope={scope_value} "
        "authorization_required=true "
        "full_document_control_allowed=false "
        "next_command='DOCUMENT_CONTROL_SCOPE=\""
        f"{scope_value}"
        "\" python3 tools/kds-sync/document_control.py' "
        f"validators={' | '.join(validator_outputs)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
