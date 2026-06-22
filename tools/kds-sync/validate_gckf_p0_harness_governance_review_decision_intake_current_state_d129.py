#!/usr/bin/env python3
"""Validate D129 GCKF P0 Harness Governance review decision intake current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-governance-review-decision-intake-current-state-d129-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-harness-governance-review-decision-intake-current-state-d129-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-harness-governance-review-decision-intake-current-state-d129-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D129-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_harness_governance_review_decision_intake_current_state_d129=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d129_markdown_or_loop")

    expected = fixture["expectedSummary"]
    decision_template = load_json(ROOT / fixture["sourceDecisionTemplate"])
    repair_workpack = load_json(ROOT / fixture["sourceRepairWorkpack"])
    intake = fixture["intake"]

    require(fixture.get("intakeStatus") == expected["intakeStatus"], "intake_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(intake.get("intakeType") == expected["intakeType"], "intake_type_mismatch")
    require(intake.get("intakeStatus") == expected["intakeStatus"], "nested_intake_status_mismatch")
    require(intake.get("reviewStatus") == expected["reviewStatus"], "review_status_mismatch")
    require(intake.get("requiredReviewerType") == "human_or_harness_governance", "required_reviewer_type_mismatch")

    require(decision_template.get("templateStatus") == "candidate_with_hold", "source_decision_template_status_mismatch")
    require(repair_workpack.get("workpackStatus") == "candidate_with_hold", "source_repair_workpack_status_mismatch")

    outcomes = set(intake.get("allowedDecisionOutcomes", []))
    expected_outcomes = {
        "accept_for_review",
        "return_for_packet_repair",
        "reject_candidate_packet",
        "approve_for_future_formal_write",
    }
    require(outcomes == expected_outcomes, "allowed_decision_outcomes_mismatch")
    require(len(outcomes) == expected["allowedDecisionOutcomeCount"], "allowed_decision_outcome_count_mismatch")

    required_fields = set(intake.get("requiredDecisionFields", []))
    for field in {"reviewerId", "reviewedAt", "sourcePacketRef", "decisionOutcome", "decisionRationale", "evidenceRefs", "authorityRef", "holdContextRefs"}:
        require(field in required_fields, f"missing_required_decision_field:{field}")
    require(len(required_fields) == expected["requiredDecisionFieldCount"], "required_decision_field_count_mismatch")

    guards = set(intake.get("decisionGuards", []))
    for guard in {
        "source_packet_status_is_candidate",
        "source_packet_review_status_is_pending",
        "reviewer_authority_present",
        "decision_outcome_is_allowed",
        "formal_evidence_not_written",
        "harness_evidence_not_written",
        "approval_does_not_write_evidence",
        "repair_and_rejection_require_reason",
        "future_formal_write_requires_separate_execution",
        "hold_context_present",
        "p1_admission_not_granted",
        "v1_upgrade_not_approved",
    }:
        require(guard in guards, f"missing_decision_guard:{guard}")
    require(len(guards) == expected["decisionGuardCount"], "decision_guard_count_mismatch")

    forbidden_actions = set(intake.get("forbiddenActions", []))
    for forbidden in {
        "write_formal_evidence",
        "write_harness_evidence",
        "write_kds",
        "promote_lifecycle",
        "enable_business_writeback",
        "mark_p0_accepted",
        "treat_approval_as_written_evidence",
        "grant_p1_admission",
        "approve_v1_upgrade",
    }:
        require(forbidden in forbidden_actions, f"missing_forbidden_action:{forbidden}")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    repair_workpack_hold_refs = set(repair_workpack["candidateWorkItems"][0]["holdContextRefs"])
    for hold_ref in hold_refs:
        require(hold_ref in repair_workpack_hold_refs, f"missing_hold_context_ref:{hold_ref}")

    for key in [
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ]:
        require(fixture["currentGateAssertions"].get(key) is False, f"current_gate_assertion_not_false:{key}")

    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")
    require(len(fixture["requiredSourceRefs"]) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")

    require(evidence.get("current_intake_status") == "candidate_with_hold", "evidence_intake_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("intake_scope", {}).get("allowed_decisions") == 4, "evidence_allowed_decision_count_mismatch")
    require(evidence.get("hold_context", {}).get("review_status") == "pending_with_hold", "evidence_review_status_mismatch")

    d30_output = run_command("python3", "scripts/api/validate_gckf_p0_harness_governance_review_decision_intake_dry_run.py")
    require(d30_output.startswith("gckf_p0_harness_governance_review_decision_intake_dry_run=pass"), "d30_validator_not_pass")

    d128_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_repair_path_workpack_current_state_d128.py")
    require(d128_output.startswith("gckf_p0_repair_path_workpack_current_state_d128=pass"), "d128_validator_not_pass")

    d127_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_harness_decision_template_current_state_d127.py")
    require(d127_output.startswith("gckf_p0_harness_decision_template_current_state_d127=pass"), "d127_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_harness_governance_review_decision_intake_current_state_d129=pass")
    print(f"intake_status={fixture.get('intakeStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"review_status={intake.get('reviewStatus')}")
    print(f"allowed_decisions={len(outcomes)}")
    print(f"decision_guards={len(guards)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
