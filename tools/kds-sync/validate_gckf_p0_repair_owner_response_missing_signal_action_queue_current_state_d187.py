#!/usr/bin/env python3
"""Validate D187 GCKF P0 missing repair-owner-response signal action queue."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-repair-owner-response-missing-signal-action-queue-current-state-d187-20260627.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-missing-signal-action-queue-current-state-d187-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-missing-signal-action-queue-current-state-d187-20260627.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D187-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_repair_owner_response_missing_signal_action_queue_current_state_d187=fail reason={message}")
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
    source_summary = source.get("arrivalScanSummary", {})
    require(source.get("arrivalScanStatus") == "response_arrival_scan_with_hold", "source_arrival_status_mismatch")
    require(source_summary.get("foundSignals") == 0, "source_found_signals_not_zero")
    require(source_summary.get("missingSignals") == 4, "source_missing_signals_not_four")
    require(source.get("gateAssertions", {}).get("responseIntakeAllowed") is False, "source_intake_boundary_not_false")

    require(fixture.get("actionQueueStatus") == "missing_signal_action_queue_with_hold", "action_queue_status_mismatch")
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")

    summary = fixture.get("actionQueueSummary", {})
    require(summary.get("queueItems") == 4, "queue_item_count_mismatch")
    require(summary.get("readyForExecution") == 0, "ready_for_execution_not_zero")
    require(summary.get("executedActions") == 0, "executed_actions_not_zero")
    require(summary.get("blockedByExternalInput") == 4, "blocked_count_mismatch")
    require(evidence.get("actionQueueSummary") == summary, "evidence_summary_mismatch")

    items = fixture.get("actionItems", [])
    expected_signals = {
        "real_repair_owner_response",
        "signed_response_package",
        "waes_review_note",
        "human_confirmation_record",
    }
    require(len(items) == 4, "action_item_count_mismatch")
    require({item.get("missingSignalId") for item in items} == expected_signals, "action_item_signal_ids_mismatch")
    for item in items:
        item_id = item.get("actionItemId")
        require(item.get("actionStatus") == "blocked_waiting_external_input", f"action_not_blocked:{item_id}")
        require(item.get("executionAllowed") is False, f"action_execution_allowed:{item_id}")
        require(item.get("notificationSent") is False, f"action_notification_sent:{item_id}")
        require(item.get("responseIntakeAllowed") is False, f"action_intake_allowed:{item_id}")
        require(bool(item.get("requiredNextInput")), f"action_missing_required_input:{item_id}")

    for key in (
        "actionQueueIsActualResponse",
        "externalNotificationSent",
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
    require("missing_signal_action_queue_with_hold" in evidence_md, "evidence_md_missing_status")
    require("executedActions=0" in evidence_md, "evidence_md_missing_zero_execution")
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

    print("gckf_p0_repair_owner_response_missing_signal_action_queue_current_state_d187=pass")
    print(f"action_queue_status={fixture.get('actionQueueStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"queue_items={summary.get('queueItems')}")
    print(f"ready_for_execution={summary.get('readyForExecution')}")
    print(f"executed_actions={summary.get('executedActions')}")
    print(f"blocked_by_external_input={summary.get('blockedByExternalInput')}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
