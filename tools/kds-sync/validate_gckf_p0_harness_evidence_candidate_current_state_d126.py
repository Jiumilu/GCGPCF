#!/usr/bin/env python3
"""Validate D126 GCKF P0 Harness evidence candidate current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-evidence-candidate-record-current-state-d126-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-harness-evidence-candidate-current-state-d126-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-harness-evidence-candidate-current-state-d126-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D126-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_harness_evidence_candidate_current_state_d126=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d126_markdown_or_loop")

    expected = fixture["expectedSummary"]
    source_packet = load_json(ROOT / fixture["sourceHarnessInputPacket"])

    require(fixture.get("candidateRecordStatus") == expected["candidateRecordStatus"], "candidate_record_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(source_packet.get("packetStatus") == expected["sourceHarnessInputPacketStatus"], "source_packet_status_mismatch")
    require(source_packet.get("maximumState") == expected["sourceHarnessInputPacketMaximumState"], "source_packet_maximum_state_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")

    candidate = fixture["candidateRecord"]
    require(candidate.get("recordType") == expected["recordType"], "record_type_mismatch")
    require(candidate.get("reviewStatus") == expected["reviewStatus"], "review_status_mismatch")
    require(candidate.get("defaultDecisionOutcome") == "pending", "default_decision_outcome_not_pending")
    require("pending" not in candidate.get("allowedDecisionOutcomes", []), "pending_in_allowed_outcomes")
    require(candidate.get("requiresHumanReview") is expected["requiresHumanReview"], "requires_human_review_mismatch")
    require(candidate.get("requiresHarnessGovernance") is expected["requiresHarnessGovernance"], "requires_harness_governance_mismatch")
    require(candidate.get("holdContextRequired") is expected["holdContextRequired"], "hold_context_required_mismatch")
    require(candidate.get("writesFormalEvidence") is expected["writesFormalEvidence"], "writes_formal_evidence_mismatch")
    require(candidate.get("writesAcceptedLifecycle") is expected["writesAcceptedLifecycle"], "writes_accepted_lifecycle_mismatch")

    source_input_ids = {item["id"] for item in source_packet["harnessInputs"]}
    for input_ref in fixture["sourceReviewInputs"]:
        require(input_ref in source_input_ids, f"missing_source_review_input:{input_ref}")
    require(len(fixture["sourceReviewInputs"]) == expected["sourceReviewInputCount"], "source_review_input_count_mismatch")

    source_risk_refs = set(source_packet["riskRefs"])
    for risk_ref in fixture["sourceRiskRefs"]:
        require(risk_ref in source_risk_refs, f"missing_source_risk_ref:{risk_ref}")
    require(len(fixture["sourceRiskRefs"]) == expected["sourceRiskRefCount"], "source_risk_ref_count_mismatch")

    source_hold_refs = set(source_packet["holdRefs"])
    for hold_ref in fixture["holdContextRefs"]:
        require(hold_ref in source_hold_refs, f"missing_hold_context_ref:{hold_ref}")
    require(len(fixture["holdContextRefs"]) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    closure = load_json(ROOT / "docs/harness/evidence/gckf-p0-closure-packet-candidate-d124-20260622.json")
    closure_completed = {item["id"] for item in closure["completed_items"]}
    for completed_ref in fixture["sourceCompletedItemRefs"]:
        require(completed_ref in closure_completed, f"missing_completed_item_ref:{completed_ref}")
    require(len(fixture["sourceCompletedItemRefs"]) == expected["sourceCompletedItemRefCount"], "source_completed_item_ref_count_mismatch")

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

    require(evidence.get("current_record_status") == "candidate_with_hold", "evidence_record_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("record_scope", {}).get("hold_context_refs") == 6, "evidence_hold_ref_count_mismatch")
    require(evidence.get("hold_context", {}).get("review_status") == "pending_with_hold", "evidence_review_status_mismatch")

    d23_output = run_command("python3", "scripts/api/validate_gckf_p0_harness_evidence_candidate_record_dry_run.py")
    require(d23_output.startswith("gckf_p0_harness_evidence_candidate_record_dry_run=pass"), "d23_validator_not_pass")

    d24_output = run_command("python3", "scripts/api/validate_gckf_p0_harness_decision_template_dry_run.py")
    require(d24_output.startswith("gckf_p0_harness_decision_template_dry_run=pass"), "d24_validator_not_pass")

    d125_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_harness_review_input_current_state_d125.py")
    require(d125_output.startswith("gckf_p0_harness_review_input_current_state_d125=pass"), "d125_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_harness_evidence_candidate_current_state_d126=pass")
    print(f"candidate_record_status={fixture.get('candidateRecordStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"review_status={candidate.get('reviewStatus')}")
    print(f"hold_context_refs={len(fixture['holdContextRefs'])}")
    print(f"source_completed_item_refs={len(fixture['sourceCompletedItemRefs'])}")
    print(f"required_sources={len(fixture['requiredSourceRefs'])}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
