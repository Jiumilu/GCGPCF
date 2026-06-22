#!/usr/bin/env python3
"""Validate Agent-Reach candidate quality regression gate evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-candidate-quality-regression-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-candidate-quality-regression-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001.md"
BASELINE_JSON = ROOT / "docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.json"

EXPECTED_GATES = {
    "search_success_rate_gate": ("search_success_rate", ">=", 0.8),
    "source_provenance_rate_gate": ("source_provenance_rate", "==", 1.0),
    "duplicate_rate_gate": ("duplicate_rate", "<=", 0.2),
    "latency_p50_gate": ("latency_p50_seconds", "<=", 10),
    "latency_p95_gate": ("latency_p95_seconds", "<=", 30),
    "canonical_write_gate": ("canonical_write_count", "==", 0),
    "production_write_gate": ("production_write_count", "==", 0),
    "limited_admission_gate": ("kds_admission", "==", "limited_candidate_only"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def run_validator(path: str) -> str:
    result = subprocess.run(["python3", path], cwd=ROOT, text=True, capture_output=True, check=False)
    require(result.returncode == 0, f"{path} failed: {result.stdout}{result.stderr}")
    return result.stdout.strip()


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    baseline = load_json(BASELINE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    baseline_output = run_validator("tools/kds-sync/validate_agent_reach_candidate_quality_trend_baseline.py")
    require("agent_reach_candidate_quality_trend_baseline=pass" in baseline_output, "baseline validator output missing")

    require(evidence.get("evidence_id") == "AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-20260622", "invalid evidence id")
    require(evidence.get("status") == "candidate_quality_regression_gate_ready", "invalid status")
    require(evidence.get("scope") == "GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001", "invalid scope")
    require(evidence.get("execution_mode") == "read_only_regression_gate_definition", "execution mode mismatch")
    require(evidence.get("external_search_invoked") is False, "external search must not be invoked")
    require(evidence.get("agent_reach_runtime_invoked") is False, "Agent-Reach runtime must not be invoked")
    require(evidence.get("next_round") == "GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-FIXTURE-REPLAY-001", "invalid next round")
    require("docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.json" in evidence.get("source_evidence", []), "missing baseline source")

    require(baseline.get("status") == "candidate_quality_trend_baseline_ready", "baseline status mismatch")
    gates = {gate.get("gate_id"): gate for gate in evidence.get("regression_gates", [])}
    require(set(gates) == set(EXPECTED_GATES), "regression gate set mismatch")
    for gate_id, (metric, operator, threshold) in EXPECTED_GATES.items():
        gate = gates[gate_id]
        require(gate.get("metric") == metric, f"metric mismatch: {gate_id}")
        require(gate.get("operator") == operator, f"operator mismatch: {gate_id}")
        require(gate.get("threshold") == threshold, f"threshold mismatch: {gate_id}")
        require("failure_action" in gate and gate["failure_action"], f"failure action missing: {gate_id}")

    fixture_ids = {fixture.get("fixture_id") for fixture in evidence.get("negative_fixtures", [])}
    require(fixture_ids == {
        "missing_source_provenance",
        "duplicate_rate_regression",
        "canonical_write_attempt",
        "production_write_attempt",
        "unauthorized_status_upgrade",
    }, "negative fixture set mismatch")
    for fixture in evidence.get("negative_fixtures", []):
        require(fixture.get("expected_result") == "fail", f"fixture must fail: {fixture.get('fixture_id')}")
        require(fixture.get("expected_gate") in gates, f"fixture expected gate missing: {fixture.get('fixture_id')}")

    status = evidence.get("quality_status", {})
    require(status.get("regression_gate_count") == 8, "regression gate count mismatch")
    require(status.get("negative_fixture_count") == 5, "negative fixture count mismatch")
    require(status.get("baseline_pass_required") is True, "baseline pass required mismatch")
    require(status.get("all_negative_fixtures_must_fail") is True, "negative fixture rule mismatch")
    require(status.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(status.get("production_integration_allowed") is False, "production integration must be false")
    require(status.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")
    require(evidence.get("positive_baseline_expected_result") == "pass", "positive baseline expected result mismatch")

    for claim in evidence.get("non_claims", []):
        require("does not" in claim, f"non-claim must be explicit: {claim}")

    for phrase in [
        "candidate_quality_regression_gate_ready",
        "regression_gate_count | `8`",
        "negative_fixture_count | `5`",
        "source_provenance_rate_gate",
        "canonical_write_gate",
        "GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-FIXTURE-REPLAY-001",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "非声明", "下一轮"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_candidate_quality_regression_gate=pass "
        "regression_gate_count=8 negative_fixture_count=5 "
        "baseline_required=true all_negative_fixtures_must_fail=true "
        "next=GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-FIXTURE-REPLAY-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
