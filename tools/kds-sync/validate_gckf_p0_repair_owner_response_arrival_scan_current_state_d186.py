#!/usr/bin/env python3
"""Validate D186 GCKF P0 repair owner response arrival scan current state."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-repair-owner-response-arrival-scan-current-state-d186-20260627.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-arrival-scan-current-state-d186-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-arrival-scan-current-state-d186-20260627.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D186-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_repair_owner_response_arrival_scan_current_state_d186=fail reason={message}")
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


def assert_no_prior_actual_response() -> None:
    response_jsons = sorted(
        list((ROOT / "fixtures/api").glob("gckf-p0-*repair-owner-response*.json"))
        + list((ROOT / "docs/harness/evidence").glob("gckf-p0-*repair-owner-response*.json"))
        + [ROOT / "fixtures/api/gckf-p0-session-mainline-takeover-current-state-d185-20260627.json"]
        + [ROOT / "docs/harness/evidence/gckf-p0-session-mainline-takeover-current-state-d185-20260627.json"]
    )
    require(response_jsons, "no_gckf_response_chain_jsons_found")
    for path in response_jsons:
        data = load_json(path)
        if "actualRepairOwnerResponseReceived" in data:
            require(data.get("actualRepairOwnerResponseReceived") is False, f"prior_actual_response_claimed:{path.relative_to(ROOT)}")
        assertions = data.get("gateAssertions", {})
        if "responseIntakeAllowed" in assertions:
            require(assertions.get("responseIntakeAllowed") is False, f"prior_response_intake_allowed:{path.relative_to(ROOT)}")
    forbidden_intake = [
        path
        for path in list((ROOT / "fixtures/api").glob("gckf-p0-*response-intake*.json"))
        + list((ROOT / "docs/harness/evidence").glob("gckf-p0-*response-intake*.json"))
        if "headroom" not in path.name
    ]
    require(not forbidden_intake, "unexpected_gckf_response_intake_artifact:" + ",".join(path.relative_to(ROOT).as_posix() for path in forbidden_intake))


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    source = load_json(ROOT / fixture["sourceEvidence"])
    require(source.get("takeoverStatus") == "session_mainline_takeover_with_hold", "source_takeover_status_mismatch")
    source_response_received = source.get("actualRepairOwnerResponseReceived", source.get("stateBoundary", {}).get("actualRepairOwnerResponseReceived"))
    require(source_response_received is False, "source_response_boundary_not_false")
    require(source.get("gateAssertions", {}).get("responseIntakeAllowed") is False, "source_intake_boundary_not_false")

    require(fixture.get("arrivalScanStatus") == "response_arrival_scan_with_hold", "arrival_scan_status_mismatch")
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")
    summary = fixture.get("arrivalScanSummary", {})
    require(summary.get("requiredSignals") == 4, "required_signal_count_mismatch")
    require(summary.get("foundSignals") == 0, "found_signal_count_mismatch")
    require(summary.get("missingSignals") == 4, "missing_signal_count_mismatch")
    require(evidence.get("arrivalScanSummary") == summary, "evidence_summary_mismatch")

    signals = fixture.get("arrivalSignals", [])
    require(len(signals) == 4, "arrival_signal_count_mismatch")
    expected = {
        "real_repair_owner_response",
        "signed_response_package",
        "waes_review_note",
        "human_confirmation_record",
    }
    require({signal.get("signalId") for signal in signals} == expected, "arrival_signal_ids_mismatch")
    for signal in signals:
        require(signal.get("found") is False, f"arrival_signal_found:{signal.get('signalId')}")
        require(signal.get("responseIntakeAllowed") is False, f"arrival_signal_intake_allowed:{signal.get('signalId')}")
        require(bool(signal.get("missingReason")), f"missing_arrival_signal_reason:{signal.get('signalId')}")

    for key in (
        "responseArrivalConfirmed",
        "signedPackagePresent",
        "waesReviewNotePresent",
        "humanConfirmationPresent",
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

    assert_no_prior_actual_response()

    evidence_md = EVIDENCE_MD.read_text(encoding="utf-8")
    loop_md = LOOP_MD.read_text(encoding="utf-8")
    require("response_arrival_scan_with_hold" in evidence_md, "evidence_md_missing_status")
    require("foundSignals=0" in evidence_md, "evidence_md_missing_zero_found")
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

    print("gckf_p0_repair_owner_response_arrival_scan_current_state_d186=pass")
    print(f"arrival_scan_status={fixture.get('arrivalScanStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"required_signals={summary.get('requiredSignals')}")
    print(f"found_signals={summary.get('foundSignals')}")
    print(f"missing_signals={summary.get('missingSignals')}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
