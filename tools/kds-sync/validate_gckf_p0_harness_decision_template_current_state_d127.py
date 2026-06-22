#!/usr/bin/env python3
"""Validate D127 GCKF P0 Harness decision template current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-decision-template-current-state-d127-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-harness-decision-template-current-state-d127-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-harness-decision-template-current-state-d127-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D127-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_harness_decision_template_current_state_d127=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d127_markdown_or_loop")

    expected = fixture["expectedSummary"]
    source_candidate = load_json(ROOT / fixture["sourceCandidateRecord"])
    source_record = source_candidate["candidateRecord"]
    template = fixture["decisionTemplate"]
    decision_cases = template["decisionCases"]

    require(fixture.get("templateStatus") == expected["templateStatus"], "template_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")
    require(template.get("templateType") == expected["templateType"], "template_type_mismatch")
    require(source_candidate.get("candidateRecordStatus") == expected["sourceCandidateRecordStatus"], "source_candidate_record_status_mismatch")
    require(source_candidate.get("maximumState") == expected["maximumState"], "source_candidate_maximum_state_mismatch")
    require(source_record.get("reviewStatus") == expected["sourceCandidateReviewStatus"], "source_candidate_review_status_mismatch")

    require(template.get("defaultDecisionStatus") == "pending_with_hold", "default_decision_status_mismatch")
    require(template.get("requiredReviewerType") == expected["requiredReviewerType"], "required_reviewer_type_mismatch")
    require(template.get("requiresHumanReview") is expected["requiresHumanReview"], "requires_human_review_mismatch")
    require(template.get("requiresHarnessGovernance") is expected["requiresHarnessGovernance"], "requires_harness_governance_mismatch")
    require(template.get("holdContextRequired") is expected["holdContextRequired"], "hold_context_required_mismatch")
    require(template.get("writesFormalEvidence") is expected["writesFormalEvidence"], "writes_formal_evidence_mismatch")
    require(template.get("writesAcceptedLifecycle") is expected["writesAcceptedLifecycle"], "writes_accepted_lifecycle_mismatch")

    expected_outcomes = set(source_record["allowedDecisionOutcomes"])
    actual_outcomes = {case["outcome"] for case in decision_cases}
    require(len(decision_cases) == expected["decisionCaseCount"], "decision_case_count_mismatch")
    require(actual_outcomes == expected_outcomes, "decision_case_outcomes_mismatch")

    required_common_fields = {"reviewerId", "reviewedAt", "decisionRationale", "holdContextRefs"}
    for case in decision_cases:
        required_fields = set(case.get("requiredFields", []))
        require(required_common_fields.issubset(required_fields), f"missing_common_fields:{case['outcome']}")
        require(bool(case.get("requiredEvidenceRefs")), f"missing_required_evidence_refs:{case['outcome']}")
        forbidden_actions = set(case.get("forbiddenActions", []))
        require("write_formal_evidence" in forbidden_actions, f"missing_write_formal_evidence_forbid:{case['outcome']}")
        require("promote_lifecycle" in forbidden_actions, f"missing_promote_lifecycle_forbid:{case['outcome']}")
        require("grant_p1_admission" in forbidden_actions, f"missing_p1_admission_forbid:{case['outcome']}")
        require("approve_v1_upgrade" in forbidden_actions, f"missing_v1_upgrade_forbid:{case['outcome']}")

    hold_refs = fixture["holdContextRefs"]
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    source_hold_refs = set(source_candidate["holdContextRefs"])
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

    for forbidden in ["accepted", "integrated", "production_ready", "business_write_enabled", "kds_write_enabled", "p1_admission_granted", "v1_upgrade_approved"]:
        require(forbidden in fixture["forbiddenOutputs"], f"missing_forbidden_output:{forbidden}")

    require(evidence.get("current_template_status") == "candidate_with_hold", "evidence_template_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("template_scope", {}).get("decision_cases") == 4, "evidence_decision_case_count_mismatch")
    require(evidence.get("hold_context", {}).get("default_decision_status") == "pending_with_hold", "evidence_default_decision_status_mismatch")

    for source_ref in fixture["requiredSourceRefs"]:
        require((ROOT / source_ref).exists(), f"missing_required_source_ref:{source_ref}")
    require(len(fixture["requiredSourceRefs"]) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")

    d24_output = run_command("python3", "scripts/api/validate_gckf_p0_harness_decision_template_dry_run.py")
    require(d24_output.startswith("gckf_p0_harness_decision_template_dry_run=pass"), "d24_validator_not_pass")

    d126_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_harness_evidence_candidate_current_state_d126.py")
    require(d126_output.startswith("gckf_p0_harness_evidence_candidate_current_state_d126=pass"), "d126_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_harness_decision_template_current_state_d127=pass")
    print(f"template_status={fixture.get('templateStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"default_decision_status={template.get('defaultDecisionStatus')}")
    print(f"decision_cases={len(decision_cases)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
