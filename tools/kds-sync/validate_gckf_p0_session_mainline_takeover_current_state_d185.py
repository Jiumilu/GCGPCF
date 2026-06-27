#!/usr/bin/env python3
"""Validate D185 GCKF P0 session mainline takeover current state."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-session-mainline-takeover-current-state-d185-20260627.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-session-mainline-takeover-current-state-d185-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-session-mainline-takeover-current-state-d185-20260627.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D185-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_session_mainline_takeover_current_state_d185=fail reason={message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        fail(f"command_failed:{' '.join(args)}:{result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def run_delegated_loop_gate() -> dict:
    env = os.environ.copy()
    env["GPCF_PROJECT_GROUP_GATE_DELEGATED"] = "1"
    result = subprocess.run(
        ("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"),
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
        env=env,
    )
    if result.returncode != 0:
        fail(f"delegated_loop_document_gate_failed:{result.stderr.strip() or result.stdout.strip()}")
    return json.loads(result.stdout.strip())


def require_controlled_markdown(path: Path) -> None:
    require(path.exists(), f"missing_dks_baseline:{path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    require("status: controlled" in text, f"dks_baseline_not_controlled:{path.relative_to(ROOT)}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    source_evidence = load_json(ROOT / fixture["sourceEvidence"])
    require(source_evidence.get("roundId") == "GPCF-GCKF-P0-D184-001", "source_round_mismatch")
    require(source_evidence.get("executionMode") == "local_evidence_no_write", "source_execution_mode_mismatch")
    require(source_evidence.get("sourceGckfBoundary", {}).get("acceptedNegativeFixtures", 0) == 0 or source_evidence.get("packageScope", {}).get("acceptedNegativeFixtures", 0) == 0, "source_negative_fixture_boundary_mismatch")
    require(source_evidence.get("gateAssertions", {}).get("responseIntakeAllowed") is False, "source_intake_boundary_not_false")

    require(fixture.get("primaryInheritedThreadId") == "019eede2-75a3-7943-9a77-a210a40a569b", "primary_thread_mismatch")
    require(fixture.get("mergedPreconditionThreadId") == "019ed328-556e-7f83-a9b2-ace87c16acdb", "merged_thread_mismatch")
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("takeoverStatus") == "session_mainline_takeover_with_hold", "takeover_status_mismatch")
    require(fixture.get("dksBaselineStatus") == "merged_precondition_controlled", "dks_baseline_status_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")
    require(evidence.get("takeoverStatus") == fixture.get("takeoverStatus"), "evidence_takeover_status_mismatch")
    require(evidence.get("stateBoundary", {}).get("holdRequired") is True, "evidence_hold_required_not_true")
    require(evidence.get("stateBoundary", {}).get("businessCompletionClaimed") is False, "business_completion_claimed")
    require(evidence.get("stateBoundary", {}).get("kdsApiWriteExecuted") is False, "kds_api_write_claimed")

    dks_baseline = fixture.get("mergedDksBaseline", [])
    require(len(dks_baseline) == 10, "dks_baseline_count_mismatch")
    for item in dks_baseline:
        require_controlled_markdown(ROOT / item)

    for key in (
        "dksBaselineIsBusinessCompletion",
        "sessionTakeoverIsResponseIntake",
        "responseIntakeAllowed",
        "formalHarnessWriteAllowed",
        "runtimeWritebackAllowed",
        "kdsApiWriteExecuted",
        "lifecyclePromotionAllowed",
        "acceptedOrIntegratedAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ):
        require(fixture.get("gateAssertions", {}).get(key) is False, f"fixture_gate_not_false:{key}")
        require(evidence.get("gateAssertions", {}).get(key) is False, f"evidence_gate_not_false:{key}")

    evidence_md = EVIDENCE_MD.read_text(encoding="utf-8")
    loop_md = LOOP_MD.read_text(encoding="utf-8")
    require("session_mainline_takeover_with_hold" in evidence_md, "evidence_md_missing_status")
    require("responseIntakeAllowed=false" in evidence_md, "evidence_md_missing_intake_boundary")
    for marker in ("## LOOP 运行控制闭环", "### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in loop_md, f"loop_control_marker_missing:{marker}")
    require("hold_required" in loop_md, "loop_md_missing_hold_required")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")
    require(run_command("python3", "tools/kds-sync/check_document_pollution.py") == "document_pollution=pass", "document_pollution_not_pass")
    require(run_command("python3", "tools/kds-sync/validate_kds_token.py").startswith("kds_token=pass"), "kds_token_not_pass")
    loop_gate = run_delegated_loop_gate()
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_session_mainline_takeover_current_state_d185=pass")
    print(f"takeover_status={fixture.get('takeoverStatus')}")
    print(f"dks_baseline_status={fixture.get('dksBaselineStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"dks_baseline_items={len(dks_baseline)}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
