#!/usr/bin/env python3
"""Validate D124 GCKF P0 closure packet candidate evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-closure-packet-candidate-d124-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-closure-packet-candidate-d124-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D124-001.md"
PILOT_CHECKLIST = ROOT / "docs/gc-knowledge-fabric/pilot-rollout-checklist-v0.1.md"
REQUIREMENTS_DOC = ROOT / "docs/gc-knowledge-fabric/requirements-confirmation-and-p0-p2-implementation-plan-v0.1.md"
SCHEDULE_DOC = ROOT / "docs/gc-knowledge-fabric/p0-two-week-execution-schedule-v0.1.md"


def fail(message: str) -> None:
    print(f"gckf_p0_closure_packet_candidate_d124=fail reason={message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


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


def main() -> None:
    require(EVIDENCE_JSON.exists() and EVIDENCE_MD.exists() and LOOP_MD.exists(), "missing_d124_artifacts")
    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))

    require(evidence.get("execution_mode") == "local_evidence_no_write", "execution_mode_not_no_write")
    require(evidence.get("closure_packet_status") == "candidate_with_hold", "closure_packet_status_mismatch")
    require(evidence.get("maximum_state") == "review_ready_with_hold", "maximum_state_mismatch")

    required_sections = evidence.get("required_closure_packet_sections", [])
    require(
        required_sections
        == [
            "completed_items",
            "pending_and_blockers",
            "validator_bundle",
            "no_write_assertion",
            "sensitive_material_handling",
            "p1_admission_judgement",
            "p2_preparation_state",
            "v1_upgrade_recommendation",
        ],
        "required_closure_packet_sections_mismatch",
    )
    for section in required_sections:
        require(section in evidence, f"missing_section:{section}")

    completed_ids = [item.get("id") for item in evidence.get("completed_items", [])]
    require(completed_ids == ["C1", "C2", "C3", "C4", "C5", "C6", "C7"], "completed_item_ids_mismatch")

    blocker_ids = [item.get("id") for item in evidence.get("pending_and_blockers", [])]
    require(blocker_ids == ["B1", "B2", "B3", "B4", "B5", "B6"], "blocker_ids_mismatch")

    d123_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_closure_packet_precheck_d123.py")
    require(d123_output.startswith("gckf_p0_closure_packet_precheck_d123=pass"), "d123_validator_not_pass")
    require("precheck_status=review_ready_with_hold" in d123_output, "d123_precheck_status_changed")

    d18_output = run_command("python3", "scripts/api/validate_gckf_p0_acceptance_packet_dry_run.py")
    require(d18_output.startswith("gckf_p0_acceptance_packet_dry_run=pass"), "d18_validator_not_pass")
    require("no_write=covered" in d18_output, "d18_no_write_not_covered")

    d19_output = run_command("python3", "scripts/api/validate_gckf_p0_acceptance_packet_ledger_dry_run.py")
    require(d19_output.startswith("gckf_p0_acceptance_packet_ledger_dry_run=pass"), "d19_validator_not_pass")
    require("ledger_status=candidate" in d19_output, "d19_ledger_status_changed")

    d20_output = run_command("python3", "scripts/api/validate_gckf_p0_closure_readiness_dry_run.py")
    require(d20_output.startswith("gckf_p0_closure_readiness_dry_run=pass"), "d20_validator_not_pass")
    require("status=review_ready_candidate" in d20_output, "d20_status_changed")
    require("remaining_human_actions=4" in d20_output, "d20_remaining_human_actions_changed")

    d21_output = run_command("python3", "scripts/api/validate_gckf_p0_human_review_checklist_dry_run.py")
    require(d21_output.startswith("gckf_p0_human_review_checklist_dry_run=pass"), "d21_validator_not_pass")
    require("pending_outcomes=4" in d21_output, "d21_pending_outcomes_changed")

    d122_output = run_command("python3", "tools/kds-sync/validate_gckf_p0_skeleton_baseline_d122.py")
    require(d122_output.startswith("gckf_p0_skeleton_baseline_d122=pass"), "d122_validator_not_pass")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")

    document_pollution = run_command("python3", "tools/kds-sync/check_document_pollution.py")
    require(document_pollution == "document_pollution=pass", "document_pollution_not_pass")

    kds_token = run_command("python3", "tools/kds-sync/validate_kds_token.py")
    require(kds_token.startswith("kds_token=pass"), "kds_token_not_pass")

    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    no_write = evidence.get("no_write_assertion", {})
    require(no_write.get("status") == "confirmed", "no_write_status_mismatch")
    for key in [
        "starts_server",
        "connects_database",
        "calls_external_api",
        "writes_kds",
        "writes_business_system",
        "writes_accepted_lifecycle",
        "writes_harness_evidence",
    ]:
        require(no_write.get(key) is False, f"no_write_flag_not_false:{key}")

    sensitive = evidence.get("sensitive_material_handling", {})
    require(sensitive.get("status") == "guarded_by_policy", "sensitive_material_status_mismatch")
    require(sensitive.get("raw_sensitive_material_written") is False, "sensitive_material_write_mismatch")
    require(len(sensitive.get("controls", [])) == 4, "sensitive_control_count_mismatch")

    p1 = evidence.get("p1_admission_judgement", {})
    require(p1.get("status") == "not_admitted_hold", "p1_status_mismatch")

    p2 = evidence.get("p2_preparation_state", {})
    require(p2.get("status") == "parallel_preparation_only", "p2_status_mismatch")

    upgrade = evidence.get("v1_upgrade_recommendation", {})
    require(upgrade.get("status") == "not_recommended", "upgrade_status_mismatch")
    require(upgrade.get("recommended_version") == "keep_v0.1_controlled", "upgrade_version_mismatch")

    pilot_text = read(PILOT_CHECKLIST)
    for phrase in ["| C-01 |", "| C-02 |", "| C-03 |", "| C-04 |", "| C-05 |", "| C-06 |", "| C-07 |", "待确认", "待执行"]:
        require(phrase in pilot_text, f"pilot_checklist_missing_phrase:{phrase}")

    requirements_text = read(REQUIREMENTS_DOC)
    for phrase in ["合同、金融、POD、质量争议默认 metadata-only 或 blocked", "P2 不依赖 GFIS 深度闭环"]:
        require(phrase in requirements_text, f"requirements_missing_phrase:{phrase}")

    schedule_text = read(SCHEDULE_DOC)
    for phrase in [
        "P0 完成项清单",
        "未完成项和阻塞项",
        "所有 validator 结果",
        "no-write 断言",
        "敏感资料处理结果",
        "葛化 P1 admission 判断",
        "湖北磷材 P2 准备状态",
        "是否建议 v0.1 升级 v1.0",
    ]:
        require(phrase in schedule_text, f"schedule_missing_phrase:{phrase}")

    print("gckf_p0_closure_packet_candidate_d124=pass")
    print(f"closure_packet_status={evidence.get('closure_packet_status')}")
    print(f"maximum_state={evidence.get('maximum_state')}")
    print(f"completed_items={len(evidence.get('completed_items', []))}")
    print(f"blockers={len(evidence.get('pending_and_blockers', []))}")
    print(f"p1_admission={p1.get('status')}")
    print(f"p2_state={p2.get('status')}")
    print(f"v1_upgrade={upgrade.get('status')}")
    print(f"localization_gate={localization.get('localization_gate')}")
    print(f"loop_document_gate={loop_gate.get('gate')}")
    print(f"execution_mode={evidence.get('execution_mode')}")


if __name__ == "__main__":
    main()
