#!/usr/bin/env python3
"""Validate D189 GCKF P0 no-write continuity guard current state."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-no-write-continuity-guard-current-state-d189-20260627.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-no-write-continuity-guard-current-state-d189-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-no-write-continuity-guard-current-state-d189-20260627.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D189-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_no_write_continuity_guard_current_state_d189=fail reason={message}")
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
    for attempt in range(1, 4):
        result = subprocess.run(
            ("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"),
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )
        last_output = (result.stderr.strip() or result.stdout.strip())
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        if result.returncode != 143:
            break
    fail(f"delegated_loop_document_gate_failed:{last_output}")


def assert_prior_chain_boundaries(expected_chain: list[str]) -> None:
    for item in expected_chain:
        data = load_json(ROOT / item)
        state_boundary = data.get("stateBoundary", {})
        gate_assertions = data.get("gateAssertions", {})
        maximum_state = data.get("maximumState", state_boundary.get("maximumState"))
        hold_required = data.get("holdRequired", state_boundary.get("holdRequired"))
        actual_response = data.get("actualRepairOwnerResponseReceived", state_boundary.get("actualRepairOwnerResponseReceived"))
        require(maximum_state == "review_ready_with_hold", f"prior_maximum_state_mismatch:{item}")
        require(hold_required is True, f"prior_hold_not_true:{item}")
        require(actual_response is False, f"prior_actual_response_not_false:{item}")
        require(gate_assertions.get("responseIntakeAllowed") is False, f"prior_response_intake_allowed:{item}")
        require(gate_assertions.get("kdsApiWriteExecuted") is False, f"prior_kds_write_claimed:{item}")
        require(gate_assertions.get("acceptedOrIntegratedAllowed") is False, f"prior_promotion_allowed:{item}")


def assert_no_response_intake_artifacts() -> None:
    candidates = []
    for base in (ROOT / "fixtures/api", ROOT / "docs/harness/evidence", ROOT / "docs/harness/loops"):
        candidates.extend(base.glob("gckf-p0-*response-intake*"))
        candidates.extend(base.glob("loop-round-GPCF-GCKF-P0-*RESPONSE-INTAKE*"))
    allowed = []
    unexpected = [path for path in candidates if path.name not in allowed]
    require(
        not unexpected,
        "unexpected_response_intake_artifact:" + ",".join(path.relative_to(ROOT).as_posix() for path in unexpected),
    )


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    source = load_json(ROOT / fixture["sourceEvidence"])
    source_summary = source.get("authorizationBoundarySummary", {})
    require(source.get("authorizationBoundaryStatus") == "authorization_boundary_precheck_with_hold", "source_authorization_status_mismatch")
    require(source_summary.get("satisfiedAuthorizationSignals") == 0, "source_authorization_signals_not_zero")
    require(source_summary.get("responseIntakeEligible") is False, "source_intake_eligible_not_false")
    require(source.get("gateAssertions", {}).get("responseIntakeAllowed") is False, "source_intake_boundary_not_false")

    require(fixture.get("continuityGuardStatus") == "no_write_continuity_guard_with_hold", "continuity_guard_status_mismatch")
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")

    summary = fixture.get("continuitySummary", {})
    require(summary.get("chainEvidenceItems") == 4, "chain_evidence_count_mismatch")
    require(summary.get("responseIntakeArtifacts") == 0, "response_intake_artifacts_not_zero")
    require(summary.get("kdsApiWrites") == 0, "kds_api_writes_not_zero")
    require(summary.get("runtimeWritebacks") == 0, "runtime_writebacks_not_zero")
    require(summary.get("lifecyclePromotions") == 0, "lifecycle_promotions_not_zero")
    require(evidence.get("continuitySummary") == summary, "evidence_summary_mismatch")

    expected_chain = fixture.get("chainEvidence", [])
    require(len(expected_chain) == 4, "chain_evidence_list_count_mismatch")
    assert_prior_chain_boundaries(expected_chain)
    assert_no_response_intake_artifacts()

    for key in (
        "continuityGuardIsActualResponse",
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
    require("no_write_continuity_guard_with_hold" in evidence_md, "evidence_md_missing_status")
    require("responseIntakeArtifacts=0" in evidence_md, "evidence_md_missing_zero_intake_artifacts")
    require("lifecyclePromotions=0" in evidence_md, "evidence_md_missing_zero_promotions")
    for marker in ("## LOOP 运行控制闭环", "### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in loop_md, f"loop_control_marker_missing:{marker}")
    require("no_write_continuity_guard" in loop_md, "loop_md_missing_continuity_guard")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")
    require(run_command("python3", "tools/kds-sync/check_document_pollution.py") == "document_pollution=pass", "document_pollution_not_pass")
    require(run_command("python3", "tools/kds-sync/validate_kds_token.py").startswith("kds_token=pass"), "kds_token_not_pass")
    loop_gate = run_delegated_loop_gate()
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_no_write_continuity_guard_current_state_d189=pass")
    print(f"continuity_guard_status={fixture.get('continuityGuardStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"chain_evidence_items={summary.get('chainEvidenceItems')}")
    print(f"response_intake_artifacts={summary.get('responseIntakeArtifacts')}")
    print(f"kds_api_writes={summary.get('kdsApiWrites')}")
    print(f"runtime_writebacks={summary.get('runtimeWritebacks')}")
    print(f"lifecycle_promotions={summary.get('lifecyclePromotions')}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
