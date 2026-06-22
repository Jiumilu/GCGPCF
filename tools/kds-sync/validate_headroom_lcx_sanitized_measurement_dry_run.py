#!/usr/bin/env python3
"""Validate Headroom LCX sanitized measurement dry-run evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_sanitized_measurement_dry_run.py"

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
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require("--check-only is required" in runner, "runner must require --check-only")
    require("production_proxy_started" in runner, "runner must record production proxy gate")
    require("not_calculated" in runner, "runner must not calculate saving rate")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-20260622", "invalid evidence id")
    require(evidence.get("status") == "check_only_dry_run_ready_no_measurement", "invalid status")
    require(evidence.get("scope") == "sanitized_ledger_metadata_check_only", "invalid scope")
    require(evidence.get("project_count") == 15 and evidence.get("projects") == PROJECTS, "project scope mismatch")
    require(evidence.get("entry_count") == 1, "entry count mismatch")
    require(evidence.get("missing_entry_fields") == [], "ledger entry fields must be complete")
    require(evidence.get("calculation", {}).get("saving_rate") == "not_calculated", "saving rate must not be calculated")
    require(evidence.get("calculation", {}).get("tokens_saved") == "not_calculated", "tokens saved must not be calculated")

    boundary = evidence.get("boundary_checks", {})
    for key in [
        "telemetry_off",
        "sensitive_raw_text_stored",
        "contains_raw_prompt",
        "contains_raw_completion",
        "contains_customer_contract_text",
        "contains_provider_secret",
        "contains_authorization_header",
        "ledger_production_measurement_allowed",
        "ledger_measured_production_tokens",
        "waes_harness_admitted",
        "authorized_precheck_gate",
    ]:
        require(boundary.get(key) is True, f"boundary check must be true: {key}")

    gates = evidence.get("gates", {})
    require(gates.get("sanitized_measurement_dry_run_gate") is True, "dry-run gate must be true")
    require(gates.get("check_only") is True, "check_only gate must be true")
    require(gates.get("waes_harness_admitted") is True, "WAES/Harness admission must be true")
    require(gates.get("authorized_precheck_gate") is True, "authorized precheck must be true")
    for key in [
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-20260622",
        "sanitized_measurement_dry_run_gate | true",
        "check_only | true",
        "waes_harness_admitted | true",
        "authorized_precheck_gate | true",
        "saving_rate | not_calculated",
        "tokens_saved | not_calculated",
        "production_token_measurement_allowed | false",
        "measured_production_tokens | false",
        "production_proxy_started | false",
        "kds_api_write | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_sanitized_measurement_dry_run.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_sanitized_measurement_dry_run.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_sanitized_measurement_dry_run=pass_check_only "
        "project_count=15 entry_count=1 check_only=true saving_rate=not_calculated "
        "measured_production_tokens=false production_token_measurement_allowed=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
