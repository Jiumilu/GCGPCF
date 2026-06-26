#!/usr/bin/env python3
"""Validate D184 GCKF P0 repair owner response negative fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-repair-owner-response-negative-fixtures-current-state-d184-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-negative-fixtures-current-state-d184-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-negative-fixtures-current-state-d184-20260626.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D184-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_repair_owner_response_negative_fixtures_current_state_d184=fail reason={message}")
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


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    source_evidence = load_json(ROOT / fixture["sourceEvidence"])
    require(source_evidence.get("collectionChecklistStatus") == "response_collection_checklist_with_hold", "source_status_mismatch")
    require(source_evidence.get("executionMode") == "local_evidence_no_write", "source_execution_mode_mismatch")
    require(source_evidence.get("actualRepairOwnerResponseReceived") is False, "source_response_boundary_not_false")
    source_gates = source_evidence.get("gateAssertions", {})
    require(source_gates.get("collectionChecklistIsActualResponse") is False, "source_checklist_boundary_not_false")
    require(source_gates.get("responseIntakeAllowed") is False, "source_intake_boundary_not_false")
    require(source_gates.get("p1AdmissionAllowed") is False, "source_p1_boundary_not_false")

    negative_fixtures = fixture.get("negativeFixtures", [])
    summary = fixture.get("negativeFixtureSummary", {})
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("negativeFixtureStatus") == "response_intake_negative_fixtures_with_hold", "negative_fixture_status_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")
    require(len(negative_fixtures) == 4, "negative_fixture_count_mismatch")
    require(summary.get("negativeFixtureCount") == 4, "summary_negative_fixture_count_mismatch")
    require(summary.get("rejectedNegativeFixtures") == 4, "summary_rejected_count_mismatch")
    require(summary.get("acceptedNegativeFixtures") == 0, "summary_accepted_count_mismatch")
    require(evidence.get("packageScope", {}).get("negativeFixtures") == 4, "evidence_negative_fixture_count_mismatch")
    require(evidence.get("packageScope", {}).get("rejectedNegativeFixtures") == 4, "evidence_rejected_count_mismatch")
    require(evidence.get("packageScope", {}).get("acceptedNegativeFixtures") == 0, "evidence_accepted_count_mismatch")

    fixture_ids = set()
    for item in negative_fixtures:
        fixture_ids.add(item.get("fixtureId"))
        require(item.get("expectedDecision") == "reject", f"negative_fixture_not_rejected:{item.get('fixtureId')}")
        require(item.get("responseIntakeAllowed") is False, f"negative_fixture_intake_allowed:{item.get('fixtureId')}")
        require(bool(item.get("rejectedReason")), f"missing_rejected_reason:{item.get('fixtureId')}")
    require(fixture_ids == {"D184-NEG-001", "D184-NEG-002", "D184-NEG-003", "D184-NEG-004"}, "fixture_ids_mismatch")

    for key in (
        "collectionChecklistIsActualResponse",
        "unsignedPackageAccepted",
        "waesReviewBypassed",
        "humanConfirmationBypassed",
        "responseIntakeAllowed",
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ):
        require(fixture.get("gateAssertions", {}).get(key) is False, f"fixture_gate_not_false:{key}")
        require(evidence.get("gateAssertions", {}).get(key) is False, f"evidence_gate_not_false:{key}")

    evidence_md = EVIDENCE_MD.read_text(encoding="utf-8")
    loop_md = LOOP_MD.read_text(encoding="utf-8")
    require("response_intake_negative_fixtures_with_hold" in evidence_md, "evidence_md_missing_status")
    require("acceptedNegativeFixtures=0" in evidence_md, "evidence_md_missing_acceptance_boundary")
    for marker in ("## LOOP 运行控制闭环", "### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in loop_md, f"loop_control_marker_missing:{marker}")
    require("hold_required" in loop_md, "loop_md_missing_hold_required")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")
    require(run_command("python3", "tools/kds-sync/check_document_pollution.py") == "document_pollution=pass", "document_pollution_not_pass")
    require(run_command("python3", "tools/kds-sync/validate_kds_token.py").startswith("kds_token=pass"), "kds_token_not_pass")
    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_repair_owner_response_negative_fixtures_current_state_d184=pass")
    print(f"negative_fixture_status={fixture.get('negativeFixtureStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"negative_fixtures={len(negative_fixtures)}")
    print(f"rejected_negative_fixtures={summary.get('rejectedNegativeFixtures')}")
    print(f"accepted_negative_fixtures={summary.get('acceptedNegativeFixtures')}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
