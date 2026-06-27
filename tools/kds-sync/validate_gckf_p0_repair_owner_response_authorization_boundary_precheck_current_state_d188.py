#!/usr/bin/env python3
"""Validate D188 GCKF P0 repair owner response authorization boundary precheck."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-repair-owner-response-authorization-boundary-precheck-current-state-d188-20260627.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-authorization-boundary-precheck-current-state-d188-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-authorization-boundary-precheck-current-state-d188-20260627.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D188-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_repair_owner_response_authorization_boundary_precheck_current_state_d188=fail reason={message}")
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


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    source = load_json(ROOT / fixture["sourceEvidence"])
    source_summary = source.get("actionQueueSummary", {})
    require(source.get("actionQueueStatus") == "missing_signal_action_queue_with_hold", "source_action_queue_status_mismatch")
    require(source_summary.get("queueItems") == 4, "source_queue_item_count_mismatch")
    require(source_summary.get("readyForExecution") == 0, "source_ready_for_execution_not_zero")
    require(source_summary.get("executedActions") == 0, "source_executed_actions_not_zero")
    require(source_summary.get("blockedByExternalInput") == 4, "source_blocked_count_mismatch")
    require(source.get("gateAssertions", {}).get("responseIntakeAllowed") is False, "source_intake_boundary_not_false")

    require(fixture.get("authorizationBoundaryStatus") == "authorization_boundary_precheck_with_hold", "authorization_boundary_status_mismatch")
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")

    summary = fixture.get("authorizationBoundarySummary", {})
    require(summary.get("requiredAuthorizationSignals") == 4, "required_authorization_signal_count_mismatch")
    require(summary.get("satisfiedAuthorizationSignals") == 0, "satisfied_authorization_signal_count_mismatch")
    require(summary.get("missingAuthorizationSignals") == 4, "missing_authorization_signal_count_mismatch")
    require(summary.get("queueItemsExecutable") == 0, "queue_items_executable_not_zero")
    require(summary.get("responseIntakeEligible") is False, "response_intake_eligible_not_false")
    require(evidence.get("authorizationBoundarySummary") == summary, "evidence_summary_mismatch")

    signals = fixture.get("authorizationSignals", [])
    expected_signals = {
        "controlled_repair_owner_response",
        "signed_response_package",
        "waes_review_note",
        "human_confirmation_record",
    }
    require(len(signals) == 4, "authorization_signal_count_mismatch")
    require({signal.get("signalId") for signal in signals} == expected_signals, "authorization_signal_ids_mismatch")
    for signal in signals:
        signal_id = signal.get("signalId")
        require(signal.get("satisfied") is False, f"authorization_signal_satisfied:{signal_id}")
        require(signal.get("sourceActionItemStatus") == "blocked_waiting_external_input", f"source_action_status_mismatch:{signal_id}")
        require(signal.get("intakeUnlockAllowed") is False, f"intake_unlock_allowed:{signal_id}")
        require(bool(signal.get("requiredEvidence")), f"missing_required_evidence:{signal_id}")

    for key in (
        "authorizationBoundaryIsActualResponse",
        "externalNotificationSent",
        "actionQueueExecutionAllowed",
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
    require("authorization_boundary_precheck_with_hold" in evidence_md, "evidence_md_missing_status")
    require("satisfiedAuthorizationSignals=0" in evidence_md, "evidence_md_missing_zero_satisfied")
    require("responseIntakeEligible=false" in evidence_md, "evidence_md_missing_intake_boundary")
    for marker in ("## LOOP 运行控制闭环", "### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in loop_md, f"loop_control_marker_missing:{marker}")
    require("authorization_boundary" in loop_md, "loop_md_missing_authorization_boundary")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")
    require(run_command("python3", "tools/kds-sync/check_document_pollution.py") == "document_pollution=pass", "document_pollution_not_pass")
    require(run_command("python3", "tools/kds-sync/validate_kds_token.py").startswith("kds_token=pass"), "kds_token_not_pass")
    loop_gate = run_delegated_loop_gate()
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_repair_owner_response_authorization_boundary_precheck_current_state_d188=pass")
    print(f"authorization_boundary_status={fixture.get('authorizationBoundaryStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"required_authorization_signals={summary.get('requiredAuthorizationSignals')}")
    print(f"satisfied_authorization_signals={summary.get('satisfiedAuthorizationSignals')}")
    print(f"missing_authorization_signals={summary.get('missingAuthorizationSignals')}")
    print(f"queue_items_executable={summary.get('queueItemsExecutable')}")
    print(f"response_intake_eligible={summary.get('responseIntakeEligible')}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
