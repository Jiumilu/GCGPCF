#!/usr/bin/env python3
"""Validate Agent-Reach recenter evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-recenter-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-recenter-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-RECENTER-001.md"

SOURCE_VALIDATORS = [
    "tools/kds-sync/validate_agent_reach_candidate_search_review.py",
    "tools/kds-sync/validate_agent_reach_l3_candidate_pipeline.py",
    "tools/kds-sync/validate_agent_reach_candidate_search_replay_ledger.py",
    "tools/kds-sync/validate_agent_reach_waes_kds_candidate_review_queue.py",
    "tools/kds-sync/validate_agent_reach_human_review_decisions.py",
    "tools/kds-sync/validate_agent_reach_authoritative_source_verification.py",
]


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
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence.get("evidence_id") == "AGENT-REACH-RECENTER-20260622", "invalid evidence id")
    require(evidence.get("status") == "agent_reach_mainline_recentered", "invalid status")
    require(evidence.get("scope") == "GPCF-AGENT-REACH-RECENTER-001", "invalid scope")
    require(evidence.get("next_round") == "GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001", "invalid next round")

    deviation = evidence.get("deviation_assessment", {})
    require(deviation.get("deviated") is True, "deviation must be explicit")
    require(deviation.get("direct_agent_reach_integration_completed") is False, "direct integration must remain false")
    require(deviation.get("codegraph_work_relevant_but_indirect") is True, "CodeGraph work must be indirect")

    causes = {item.get("cause") for item in evidence.get("deviation_causes", [])}
    require(causes == {
        "authorization_chain_shift",
        "latest_next_round_bias",
        "shared_governance_infrastructure_overlap",
        "declaration_boundary_created_late",
    }, "deviation cause set mismatch")

    state = evidence.get("current_agent_reach_state", {})
    require(state.get("candidate_search_review") == "ready_for_review", "candidate review state mismatch")
    require(state.get("kds_admission") == "limited_candidate_only", "KDS admission mismatch")
    require(state.get("rag_admission") == "limited", "RAG admission mismatch")
    require(state.get("accepted") is False, "accepted must remain false")
    require(state.get("integrated") is False, "integrated must remain false")
    require(state.get("production_ready") is False, "production_ready must remain false")

    controls = evidence.get("recenter_controls", {})
    require(controls.get("active_mainline") == "Agent-Reach search capability integration", "active mainline mismatch")
    require(controls.get("codegraph_watchlist_is_paused_as_primary_line") is True, "CodeGraph line must be paused as primary")
    require(controls.get("agent_reach_status_ceiling") == "limited_candidate_only", "status ceiling mismatch")

    require(evidence.get("validated_inputs") == SOURCE_VALIDATORS, "validated input list mismatch")
    validator_outputs = [run_validator(path) for path in SOURCE_VALIDATORS]

    for claim in evidence.get("non_claims", []):
        require("not" in claim or "does not" in claim, f"non-claim must be negative: {claim}")

    for phrase in [
        "是，已经偏离原始主线",
        "authorization_chain_shift",
        "latest_next_round_bias",
        "shared_governance_infrastructure_overlap",
        "declaration_boundary_created_late",
        "limited_candidate_only",
        "GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "非声明", "下一轮"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    require(any("agent_reach_authoritative_source_verification=pass" in output for output in validator_outputs), "authoritative source validator output missing")

    print(
        "agent_reach_recenter_20260622=pass "
        "deviated=true active_mainline=agent_reach_search_capability_integration "
        "kds_admission=limited_candidate_only "
        "next=GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
