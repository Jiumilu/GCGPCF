#!/usr/bin/env python3
"""Validate D190 GCKF P0 stop condition and resume trigger current state."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-stop-condition-resume-trigger-current-state-d190-20260627.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-stop-condition-resume-trigger-current-state-d190-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-stop-condition-resume-trigger-current-state-d190-20260627.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D190-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_stop_condition_resume_trigger_current_state_d190=fail reason={message}")
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
    last_output = ""
    for _ in range(3):
        result = subprocess.run(
            ("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"),
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )
        last_output = result.stderr.strip() or result.stdout.strip()
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        if result.returncode != 143:
            break
    fail(f"delegated_loop_document_gate_failed:{last_output}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    source = load_json(ROOT / fixture["sourceEvidence"])
    source_summary = source.get("continuitySummary", {})
    require(source.get("continuityGuardStatus") == "no_write_continuity_guard_with_hold", "source_continuity_status_mismatch")
    require(source_summary.get("responseIntakeArtifacts") == 0, "source_response_intake_artifacts_not_zero")
    require(source_summary.get("kdsApiWrites") == 0, "source_kds_writes_not_zero")
    require(source_summary.get("runtimeWritebacks") == 0, "source_runtime_writebacks_not_zero")
    require(source_summary.get("lifecyclePromotions") == 0, "source_lifecycle_promotions_not_zero")
    require(source.get("gateAssertions", {}).get("responseIntakeAllowed") is False, "source_intake_boundary_not_false")

    require(fixture.get("stopConditionStatus") == "authorization_boundary_stop_condition_with_resume_trigger", "stop_condition_status_mismatch")
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("stopType") == "authorization_boundary", "stop_type_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")

    summary = fixture.get("resumeTriggerSummary", {})
    require(summary.get("requiredResumeTriggers") == 4, "required_resume_trigger_count_mismatch")
    require(summary.get("satisfiedResumeTriggers") == 0, "satisfied_resume_trigger_count_mismatch")
    require(summary.get("missingResumeTriggers") == 4, "missing_resume_trigger_count_mismatch")
    require(summary.get("nextExecutableRounds") == 0, "next_executable_rounds_not_zero")
    require(summary.get("resumeAllowed") is False, "resume_allowed_not_false")
    require(evidence.get("resumeTriggerSummary") == summary, "evidence_summary_mismatch")

    triggers = fixture.get("resumeTriggers", [])
    expected = {
        "controlled_repair_owner_response",
        "signed_response_package",
        "waes_review_note",
        "human_confirmation_record",
    }
    require(len(triggers) == 4, "resume_trigger_count_mismatch")
    require({trigger.get("triggerId") for trigger in triggers} == expected, "resume_trigger_ids_mismatch")
    for trigger in triggers:
        trigger_id = trigger.get("triggerId")
        require(trigger.get("satisfied") is False, f"resume_trigger_satisfied:{trigger_id}")
        require(bool(trigger.get("requiredEvidence")), f"missing_required_evidence:{trigger_id}")
        require(trigger.get("arrivalScanRefreshRequired") is True, f"arrival_scan_refresh_not_required:{trigger_id}")

    for key in (
        "stopConditionIsActualResponse",
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
    require("authorization_boundary_stop_condition_with_resume_trigger" in evidence_md, "evidence_md_missing_status")
    require("nextExecutableRounds=0" in evidence_md, "evidence_md_missing_zero_next_rounds")
    require("resumeAllowed=false" in evidence_md, "evidence_md_missing_resume_boundary")
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

    print("gckf_p0_stop_condition_resume_trigger_current_state_d190=pass")
    print(f"stop_condition_status={fixture.get('stopConditionStatus')}")
    print(f"stop_type={fixture.get('stopType')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"required_resume_triggers={summary.get('requiredResumeTriggers')}")
    print(f"satisfied_resume_triggers={summary.get('satisfiedResumeTriggers')}")
    print(f"missing_resume_triggers={summary.get('missingResumeTriggers')}")
    print(f"next_executable_rounds={summary.get('nextExecutableRounds')}")
    print(f"resume_allowed={summary.get('resumeAllowed')}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
