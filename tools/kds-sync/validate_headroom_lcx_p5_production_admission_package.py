#!/usr/bin/env python3
"""Validate Headroom LCX P5 production admission request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_p5_production_admission_package.py"

PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
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
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("REQUIRED_AUTHORIZATION_ITEMS" in runner, "runner must define required authorization items")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(len(evidence.get("evidence_chain", [])) == 8, "P0-P4 and authorization evidence chain must be present")
    require(evidence.get("pending_action_count") == 6, "pending action count must be 6")
    admission = evidence.get("admission_decision", {})
    require(admission.get("request_package_generated") is True, "request package must be generated")
    require(admission.get("p5_request_package_gate") is True, "P5 package gate must pass")
    require(admission.get("production_admission_gate") is False, "production admission must remain false")
    gates = evidence.get("gates", {})
    for key in [
        "p5_production_admission_package_gate",
        "request_package_generated",
        "prior_p0_p4_evidence_present",
        "pending_actions_registered",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "authorization_window_present",
        "sanitized_production_token_ledger_present",
        "rollback_plan_present",
        "waes_harness_admission_decision_present",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    for phrase in [
        "HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-20260621",
        "p5_production_admission_package_gate | true",
        "pending_action_count | 6",
        "authorization_window_present | false",
        "sanitized_production_token_ledger_present | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_p5_production_admission_package.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_p5_production_admission_package.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_p5_production_admission_package=pass "
        "project_count=15 pending_action_count=6 request_package_generated=true "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
