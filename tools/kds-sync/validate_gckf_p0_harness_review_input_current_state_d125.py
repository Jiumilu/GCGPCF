#!/usr/bin/env python3
"""Validate D125 GCKF P0 Harness review input current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-review-input-packet-current-state-d125-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-harness-review-input-current-state-d125-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-harness-review-input-current-state-d125-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D125-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_harness_review_input_current_state_d125=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d125_markdown_or_loop")

    expected = fixture["expectedSummary"]
    checklist = load_json(ROOT / fixture["sourceChecklist"])
    readiness = load_json(ROOT / fixture["sourceReadiness"])
    ledger = load_json(ROOT / fixture["sourceLedger"])
    closure = load_json(ROOT / fixture["sourceClosurePacketCandidate"])

    require(fixture.get("packetStatus") == expected["packetStatus"], "packet_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "packet_maximum_state_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(checklist.get("checklistStatus") == expected["sourceChecklistStatus"], "checklist_status_mismatch")
    require(readiness.get("readinessStatus") == expected["sourceReadinessStatus"], "readiness_status_mismatch")
    require(ledger.get("ledgerStatus") == expected["sourceLedgerStatus"], "ledger_status_mismatch")
    require(closure.get("closure_packet_status") == expected["sourceClosurePacketStatus"], "closure_packet_status_mismatch")
    require(closure.get("maximum_state") == expected["sourceClosurePacketMaximumState"], "closure_packet_maximum_state_mismatch")

    harness_inputs = fixture["harnessInputs"]
    review_items = checklist["reviewItems"]
    review_item_ids = {item["id"] for item in review_items}
    require(len(harness_inputs) == expected["harnessInputCount"], "harness_input_count_mismatch")
    for item in harness_inputs:
        require(item["fromReviewItem"] in review_item_ids, f"missing_review_item:{item['fromReviewItem']}")
        require(item.get("defaultOutcome") == "pending", f"default_outcome_not_pending:{item['id']}")
        require("pending" not in item.get("allowedOutcomes", []), f"pending_in_allowed_outcomes:{item['id']}")

    hold_refs = fixture["holdRefs"]
    closure_blockers = {item["id"] for item in closure["pending_and_blockers"]}
    require(len(hold_refs) == expected["holdRefCount"], "hold_ref_count_mismatch")
    for hold_ref in hold_refs:
        require(hold_ref in closure_blockers, f"missing_closure_blocker:{hold_ref}")

    scope = fixture["reviewScope"]
    require(scope["reviewItemCount"] == len(review_items) == expected["reviewItemCount"], "review_item_count_mismatch")
    require(scope["riskRefCount"] == len(fixture["riskRefs"]) == expected["riskRefCount"], "risk_ref_count_mismatch")
    require(scope["ledgerEntryCount"] == len(ledger["entries"]) == expected["ledgerEntryCount"], "ledger_entry_count_mismatch")
    require(
        scope["closurePacketCompletedItemCount"] == len(closure["completed_items"]) == expected["closurePacketCompletedItemCount"],
        "closure_completed_item_count_mismatch",
    )
    require(
        scope["closurePacketBlockerCount"] == len(closure["pending_and_blockers"]) == expected["closurePacketBlockerCount"],
        "closure_blocker_count_mismatch",
    )

    readiness_risks = {risk["id"] for risk in readiness["closureRisks"]}
    for risk_ref in fixture["riskRefs"]:
        require(risk_ref in readiness_risks, f"missing_readiness_risk:{risk_ref}")

    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")
    require(len(fixture["requiredSourceRefs"]) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")

    assertions = fixture["currentGateAssertions"]
    for key in [
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ]:
        require(assertions.get(key) is False, f"current_gate_assertion_not_false:{key}")

    require(evidence.get("current_packet_status") == "candidate_with_hold", "evidence_packet_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("review_scope", {}).get("closure_packet_blockers") == 6, "evidence_blocker_count_mismatch")
    require(evidence.get("hold_context", {}).get("formal_harness_write_allowed") is False, "evidence_formal_harness_flag_mismatch")

    d124_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_closure_packet_candidate_d124.py")
    require(d124_output.startswith("gckf_p0_closure_packet_candidate_d124=pass"), "d124_validator_not_pass")

    d22_output = run_command("python3", "scripts/api/validate_gckf_p0_harness_review_input_packet_dry_run.py")
    require(d22_output.startswith("gckf_p0_harness_review_input_packet_dry_run=pass"), "d22_validator_not_pass")

    d23_output = run_command("python3", "scripts/api/validate_gckf_p0_harness_evidence_candidate_record_dry_run.py")
    require(d23_output.startswith("gckf_p0_harness_evidence_candidate_record_dry_run=pass"), "d23_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_harness_review_input_current_state_d125=pass")
    print(f"packet_status={fixture.get('packetStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"harness_inputs={len(harness_inputs)}")
    print(f"hold_refs={len(hold_refs)}")
    print(f"required_sources={len(fixture['requiredSourceRefs'])}")
    print(f"closure_blockers={len(closure['pending_and_blockers'])}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
