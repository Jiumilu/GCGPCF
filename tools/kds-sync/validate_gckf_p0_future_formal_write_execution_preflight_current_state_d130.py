#!/usr/bin/env python3
"""Validate D130 GCKF P0 future formal write execution preflight current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-future-formal-write-execution-preflight-current-state-d130-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-future-formal-write-execution-preflight-current-state-d130-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-future-formal-write-execution-preflight-current-state-d130-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D130-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_future_formal_write_execution_preflight_current_state_d130=fail reason={message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run_command(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        fail(f"command_failed:{' '.join(args)}:{stderr}")
    return result.stdout.strip()


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d130_markdown_or_loop")

    expected = fixture["expectedSummary"]
    historical_preflight = load_json(ROOT / fixture["sourceHistoricalPreflight"])
    current_intake = load_json(ROOT / fixture["sourceCurrentReviewIntake"])
    preflight = fixture["executionPreflight"]
    intake = current_intake["intake"]

    require(fixture.get("executionPreflightStatus") == expected["executionPreflightStatus"], "execution_preflight_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(preflight.get("preflightType") == expected["preflightType"], "preflight_type_mismatch")
    require(preflight.get("executionStatus") == expected["executionStatus"], "execution_status_mismatch")
    require(preflight.get("sourceIntakeId") == intake.get("id"), "source_intake_id_mismatch")

    require(historical_preflight.get("executionPreflightStatus") == "candidate", "historical_preflight_status_mismatch")
    require(historical_preflight["executionPreflight"].get("executionStatus") == "candidate", "historical_execution_status_mismatch")
    require(current_intake.get("intakeStatus") == expected["sourceIntakeStatus"], "source_intake_status_mismatch")
    require(intake.get("reviewStatus") == expected["sourceIntakeReviewStatus"], "source_intake_review_status_mismatch")
    require(fixture.get("coveredDecisionOutcome") == expected["coveredDecisionOutcome"], "covered_decision_outcome_mismatch")
    require(fixture["coveredDecisionOutcome"] in intake.get("allowedDecisionOutcomes", []), "covered_decision_not_allowed")

    required_inputs = set(preflight.get("requiredInputs", []))
    require(len(required_inputs) == expected["requiredInputCount"], "required_input_count_mismatch")
    for field in {
        "reviewerId",
        "reviewedAt",
        "sourcePacketRef",
        "approvalDecisionRef",
        "authorityRef",
        "evidenceRefs",
        "holdContextRefs",
        "idempotencyKey",
        "duplicateCheckRef",
        "rollbackPlanRef",
        "executionLockRef",
        "auditTrailRef",
    }:
        require(field in required_inputs, f"missing_required_input:{field}")

    checks = set(preflight.get("preflightChecks", []))
    require(len(checks) == expected["preflightCheckCount"], "preflight_check_count_mismatch")
    for check in {
        "source_intake_status_is_candidate_with_hold",
        "source_intake_review_status_is_pending_with_hold",
        "decision_outcome_is_approve_for_future_formal_write",
        "approval_decision_ref_present",
        "authority_ref_present",
        "hold_context_refs_present",
        "idempotency_key_present",
        "duplicate_formal_evidence_absent",
        "rollback_plan_present",
        "execution_lock_present",
        "audit_trail_ref_present",
        "formal_write_requires_next_explicit_execution",
        "p1_admission_not_granted",
        "v1_upgrade_not_approved",
    }:
        require(check in checks, f"missing_preflight_check:{check}")

    forbidden_actions = set(preflight.get("forbiddenActions", []))
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    for forbidden in {
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "skip_execution_preflight",
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(current_intake.get("holdContextRefs", []))
    for hold_ref in hold_refs:
        require(hold_ref in source_hold_refs, f"missing_hold_context_ref:{hold_ref}")

    for key in [
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ]:
        require(fixture["currentGateAssertions"].get(key) is False, f"current_gate_assertion_not_false:{key}")

    require(len(fixture.get("requiredSourceRefs", [])) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")

    require(evidence.get("current_execution_preflight_status") == "candidate_with_hold", "evidence_execution_preflight_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("preflight_scope", {}).get("required_inputs") == 12, "evidence_required_input_count_mismatch")
    require(evidence.get("hold_context", {}).get("source_intake_review_status") == "pending_with_hold", "evidence_source_review_status_mismatch")

    d31_output = run_command("python3", "scripts/api/validate_gckf_p0_future_formal_write_execution_preflight_dry_run.py")
    require(d31_output.startswith("gckf_p0_future_formal_write_execution_preflight_dry_run=pass"), "d31_validator_not_pass")

    d129_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_harness_governance_review_decision_intake_current_state_d129.py")
    require(d129_output.startswith("gckf_p0_harness_governance_review_decision_intake_current_state_d129=pass"), "d129_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_future_formal_write_execution_preflight_current_state_d130=pass")
    print(f"execution_preflight_status={fixture.get('executionPreflightStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"execution_status={preflight.get('executionStatus')}")
    print(f"required_inputs={len(required_inputs)}")
    print(f"preflight_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
