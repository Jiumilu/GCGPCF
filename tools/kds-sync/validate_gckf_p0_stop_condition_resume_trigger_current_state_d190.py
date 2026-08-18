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
D186_FIXTURE = ROOT / "fixtures/api/gckf-p0-repair-owner-response-arrival-scan-current-state-d186-20260627.json"
D186_EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-arrival-scan-current-state-d186-20260627.json"
ROLE_VIEW_VALIDATOR = "tools/kds-sync/validate_green_supply_chain_role_view_kds_entity_20260701.py"
PRIOR_VALIDATORS = {
    "D185": "tools/kds-sync/validate_gckf_p0_session_mainline_takeover_current_state_d185.py",
    "D186": "tools/kds-sync/validate_gckf_p0_repair_owner_response_arrival_scan_current_state_d186.py",
    "D187": "tools/kds-sync/validate_gckf_p0_repair_owner_response_missing_signal_action_queue_current_state_d187.py",
    "D188": "tools/kds-sync/validate_gckf_p0_repair_owner_response_authorization_boundary_precheck_current_state_d188.py",
    "D189": "tools/kds-sync/validate_gckf_p0_no_write_continuity_guard_current_state_d189.py",
}
PRIOR_PASS_KEYS = {
    "D185": "gckf_p0_session_mainline_takeover_current_state_d185",
    "D186": "gckf_p0_repair_owner_response_arrival_scan_current_state_d186",
    "D187": "gckf_p0_repair_owner_response_missing_signal_action_queue_current_state_d187",
    "D188": "gckf_p0_repair_owner_response_authorization_boundary_precheck_current_state_d188",
    "D189": "gckf_p0_no_write_continuity_guard_current_state_d189",
}


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


def parse_key_value_output(output: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return values


def run_prior_chain() -> dict[str, dict[str, str]]:
    outputs: dict[str, dict[str, str]] = {}
    for round_id, validator in PRIOR_VALIDATORS.items():
        values = parse_key_value_output(run_command("python3", validator))
        require(values.get(PRIOR_PASS_KEYS[round_id]) == "pass", f"prior_validator_not_pass:{round_id}")
        outputs[round_id] = values
    require(outputs["D185"].get("dks_baseline_mirror_matches") == "10", "d185_mirror_matches_not_ten")
    require(outputs["D186"].get("true_trigger_claims") == "0", "d186_true_trigger_claims_not_zero")
    require(outputs["D187"].get("ready_for_execution") == "0", "d187_ready_for_execution_not_zero")
    require(outputs["D187"].get("executed_actions") == "0", "d187_executed_actions_not_zero")
    require(outputs["D188"].get("satisfied_authorization_signals") == "0", "d188_satisfied_authorization_signals_not_zero")
    require(outputs["D188"].get("queue_items_executable") == "0", "d188_queue_items_executable_not_zero")
    require(outputs["D189"].get("positive_no_write_claims") == "0", "d189_positive_no_write_claims_not_zero")
    require(outputs["D189"].get("kds_api_writes") == "0", "d189_kds_api_writes_not_zero")
    require(outputs["D189"].get("runtime_writebacks") == "0", "d189_runtime_writebacks_not_zero")
    require(outputs["D189"].get("lifecycle_promotions") == "0", "d189_lifecycle_promotions_not_zero")
    return outputs


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    arrival_fixture = load_json(D186_FIXTURE)
    arrival_evidence = load_json(D186_EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    prior_chain = run_prior_chain()
    arrival_scan = prior_chain["D186"]
    require(int(arrival_scan.get("arrival_claim_files_scanned", "0")) > 0, "arrival_scan_file_count_not_positive")
    role_view = parse_key_value_output(run_command("python3", ROLE_VIEW_VALIDATOR))
    require(role_view.get("green_supply_chain_role_view_entity_gate") == "pass", "role_view_entity_gate_not_pass")
    require(role_view.get("entity_id") == "KDS-GSC-ROLE-VIEW-20260701", "role_view_entity_id_mismatch")
    require(role_view.get("engineering_domain") == "GKE-001", "role_view_engineering_domain_mismatch")
    require(role_view.get("gckf_resume_triggers") == "0/4", "role_view_resume_triggers_not_zero")

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

    arrival_summary = arrival_fixture.get("arrivalScanSummary", {})
    require(arrival_summary.get("requiredSignals") == 4, "arrival_required_signal_count_mismatch")
    require(arrival_summary.get("foundSignals") == 0, "arrival_found_signal_count_mismatch")
    require(arrival_summary.get("missingSignals") == 4, "arrival_missing_signal_count_mismatch")
    require(arrival_evidence.get("arrivalScanSummary") == arrival_summary, "arrival_evidence_summary_mismatch")
    arrival_aliases = {
        "real_repair_owner_response": "controlled_repair_owner_response",
        "signed_response_package": "signed_response_package",
        "waes_review_note": "waes_review_note",
        "human_confirmation_record": "human_confirmation_record",
    }
    arrival_signals = arrival_fixture.get("arrivalSignals", [])
    require(len(arrival_signals) == 4, "arrival_signal_count_mismatch")
    require({signal.get("signalId") for signal in arrival_signals} == set(arrival_aliases), "arrival_signal_ids_mismatch")
    trigger_by_id = {trigger.get("triggerId"): trigger for trigger in triggers}
    for signal in arrival_signals:
        signal_id = signal.get("signalId")
        trigger_id = arrival_aliases[signal_id]
        require(signal.get("found") is False, f"arrival_signal_found:{signal_id}")
        require(trigger_by_id[trigger_id].get("satisfied") is False, f"arrival_trigger_state_mismatch:{trigger_id}")

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
    for marker in (
        "2026-08-10 GKE-001 A6 后置复放",
        "technical_revalidation_passed_governance_pending",
        "gckf_resume_triggers=0/4",
        "角色视图 KDS 实体门禁",
        "9 项治理 blocker",
        "D185-D189 五个前置 validator",
        "本次不创建 D191",
    ):
        require(marker in evidence_md, f"evidence_md_missing_current_replay:{marker}")
    for marker in ("## LOOP 运行控制闭环", "### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in loop_md, f"loop_control_marker_missing:{marker}")
    require("authorization_boundary" in loop_md, "loop_md_missing_authorization_boundary")
    for marker in (
        "technical_revalidation_passed_governance_pending",
        "四项 resume triggers 仍为 `0/4`",
        "`nextExecutableRounds=0`",
        "D185-D189 五个前置 validator",
        "角色视图实体门禁",
        "不创建 D191",
    ):
        require(marker in loop_md, f"loop_md_missing_current_replay:{marker}")

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
    print(f"arrival_signal_aliases={len(arrival_aliases)}")
    print(f"arrival_scan_found_signals={arrival_summary.get('foundSignals')}")
    print(f"arrival_claim_files_scanned={arrival_scan.get('arrival_claim_files_scanned')}")
    print(f"true_trigger_claims={arrival_scan.get('true_trigger_claims')}")
    print(f"prior_chain_validators={len(prior_chain)}")
    print(f"positive_no_write_claims={prior_chain['D189'].get('positive_no_write_claims')}")
    print(f"role_view_entity_gate={role_view.get('green_supply_chain_role_view_entity_gate')}")
    print(f"role_view_resume_triggers={role_view.get('gckf_resume_triggers')}")


if __name__ == "__main__":
    main()
