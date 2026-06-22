#!/usr/bin/env python3
"""Validate D128 GCKF P0 repair path workpack current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-repair-path-workpack-current-state-d128-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-repair-path-workpack-current-state-d128-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-repair-path-workpack-current-state-d128-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D128-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_repair_path_workpack_current_state_d128=fail reason={message}")
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
    require(EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d128_markdown_or_loop")

    expected = fixture["expectedSummary"]
    decision_template = load_json(ROOT / fixture["sourceDecisionTemplate"])
    template = decision_template["decisionTemplate"]
    decision_cases = {case["outcome"]: case for case in template["decisionCases"]}

    require(fixture.get("workpackStatus") == expected["workpackStatus"], "workpack_status_mismatch")
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(decision_template.get("templateStatus") == expected["sourceDecisionTemplateStatus"], "source_template_status_mismatch")
    require(template.get("defaultDecisionStatus") == expected["sourceDecisionDefaultStatus"], "source_template_default_status_mismatch")
    require(fixture.get("notFinalAcceptance") is expected["notFinalAcceptance"], "not_final_acceptance_mismatch")

    covered = fixture["coveredDecisionOutcomes"]
    excluded = fixture["excludedDecisionOutcomes"]
    work_items = fixture["candidateWorkItems"]
    require(len(covered) == expected["coveredDecisionOutcomeCount"], "covered_decision_count_mismatch")
    require(len(excluded) == expected["excludedDecisionOutcomeCount"], "excluded_decision_count_mismatch")
    require(len(work_items) == expected["candidateWorkItemCount"], "candidate_work_item_count_mismatch")
    require(set(covered) == {"repair_required", "scope_violation_found"}, "covered_decisions_mismatch")
    require(set(excluded) == {"approved_for_formal_harness_evidence", "rejected"}, "excluded_decisions_mismatch")
    require(set(covered).isdisjoint(set(excluded)), "covered_excluded_overlap")

    for outcome in covered + excluded:
        require(outcome in decision_cases, f"missing_decision_case:{outcome}")

    for item in work_items:
        require(item["sourceDecisionOutcome"] in covered, f"invalid_source_decision:{item['id']}")
        require(item.get("targetStatus") == "candidate_with_hold", f"target_status_mismatch:{item['id']}")
        require(bool(item.get("requiredActions")), f"missing_required_actions:{item['id']}")
        require(bool(item.get("requiredRefs")), f"missing_required_refs:{item['id']}")
        require(len(item.get("holdContextRefs", [])) == expected["holdContextRefCount"], f"hold_context_ref_count_mismatch:{item['id']}")
        forbidden_actions = set(item.get("forbiddenActions", []))
        require("write_formal_evidence" in forbidden_actions, f"missing_write_formal_evidence_forbid:{item['id']}")
        require("promote_lifecycle" in forbidden_actions, f"missing_promote_lifecycle_forbid:{item['id']}")
        require("grant_p1_admission" in forbidden_actions, f"missing_p1_admission_forbid:{item['id']}")
        require("approve_v1_upgrade" in forbidden_actions, f"missing_v1_upgrade_forbid:{item['id']}")

    engines = {item["targetEngine"] for item in work_items}
    require(engines == {"KWE", "LOOP"}, "target_engine_set_mismatch")
    priorities = {item["sourceDecisionOutcome"]: item["priority"] for item in work_items}
    require(priorities.get("scope_violation_found") == "P0", "scope_violation_priority_mismatch")
    require(priorities.get("repair_required") == "P1", "repair_required_priority_mismatch")

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

    require(evidence.get("current_workpack_status") == "candidate_with_hold", "evidence_workpack_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "evidence_maximum_state_mismatch")
    require(evidence.get("workpack_scope", {}).get("candidate_work_items") == 2, "evidence_candidate_work_item_count_mismatch")
    require(evidence.get("hold_context", {}).get("formal_harness_write_allowed") is False, "evidence_formal_harness_flag_mismatch")

    d25_output = run_command("python3", "scripts/api/validate_gckf_p0_repair_path_workpack_dry_run.py")
    require(d25_output.startswith("gckf_p0_repair_path_workpack_dry_run=pass"), "d25_validator_not_pass")

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

    print("gckf_p0_repair_path_workpack_current_state_d128=pass")
    print(f"workpack_status={fixture.get('workpackStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"covered_decisions={len(covered)}")
    print(f"candidate_work_items={len(work_items)}")
    print(f"hold_context_refs={expected['holdContextRefCount']}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
