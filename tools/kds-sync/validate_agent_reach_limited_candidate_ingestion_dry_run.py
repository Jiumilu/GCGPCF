#!/usr/bin/env python3
"""Validate Agent-Reach limited candidate ingestion dry-run ledger."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-limited-candidate-ingestion-dry-run-ledger-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-limited-candidate-ingestion-dry-run-ledger-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001.md"
PLAN_JSON = ROOT / "docs/harness/evidence/agent-reach-limited-candidate-ingestion-plan-20260622.json"
AUTHORITATIVE_JSON = ROOT / "docs/harness/evidence/agent-reach-authoritative-source-verification-20260621.json"

EXPECTED_ACCEPTED = {
    "knowledge_provenance_rag": "rag_governance_context_only",
    "green_supply_chain_policy": "official_standard_metadata_reference",
    "ai_agent_evidence_gate": "open_source_tool_candidate_only",
    "agent_reach_capability": "agent_reach_capability_metadata_only",
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
    plan = load_json(PLAN_JSON)
    authoritative = load_json(AUTHORITATIVE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    plan_output = run_validator("tools/kds-sync/validate_agent_reach_limited_candidate_ingestion_plan.py")
    require("agent_reach_limited_candidate_ingestion_plan=pass" in plan_output, "plan validator output missing")

    require(evidence.get("evidence_id") == "AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-LEDGER-20260622", "invalid evidence id")
    require(evidence.get("status") == "limited_candidate_ingestion_dry_run_complete", "invalid status")
    require(evidence.get("scope") == "GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001", "invalid scope")
    require(evidence.get("execution_mode") == "candidate_metadata_dry_run_only", "execution mode mismatch")
    require(evidence.get("external_search_invoked") is False, "external search must not be invoked")
    require(evidence.get("agent_reach_runtime_invoked") is False, "Agent-Reach runtime must not be invoked")
    require(evidence.get("kds_canonical_write_count") == 0, "KDS canonical writes must be zero")
    require(evidence.get("gfis_source_of_record_write_count") == 0, "GFIS source-of-record writes must be zero")
    require(evidence.get("production_config_write_count") == 0, "production config writes must be zero")
    require(evidence.get("strong_rag_write_count") == 0, "strong RAG writes must be zero")
    require(evidence.get("next_round") == "GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001", "invalid next round")

    require(plan.get("status") == "limited_candidate_ingestion_plan_ready", "plan status mismatch")
    require(authoritative.get("decision_summary", {}).get("accept_limited_count") == 4, "authoritative accepted count mismatch")
    require(authoritative.get("decision_summary", {}).get("reject_count") == 1, "authoritative reject count mismatch")

    records = evidence.get("candidate_records", [])
    require(isinstance(records, list) and len(records) == 4, "candidate count must be 4")
    record_map = {record.get("source_id"): record for record in records}
    require(set(record_map) == set(EXPECTED_ACCEPTED), "candidate source ids mismatch")
    for source_id, accepted_scope in EXPECTED_ACCEPTED.items():
        record = record_map[source_id]
        require(record.get("decision") == "accept_limited", f"decision mismatch: {source_id}")
        require(record.get("accepted_scope") == accepted_scope, f"accepted scope mismatch: {source_id}")
        require(record.get("rag_admission") == "limited", f"RAG admission mismatch: {source_id}")
        require(record.get("kds_admission") == "limited_candidate_only", f"KDS admission mismatch: {source_id}")
        require(record.get("provenance_evidence_path") == "docs/harness/evidence/agent-reach-authoritative-source-verification-20260621.json", f"provenance mismatch: {source_id}")
        require(record.get("review_status") == "dry_run_candidate_recorded", f"review status mismatch: {source_id}")
        require(isinstance(record.get("verification_reason"), str) and len(record["verification_reason"]) >= 20, f"reason missing: {source_id}")
        require(record.get("blocked_outputs"), f"blocked outputs missing: {source_id}")

    rejected = evidence.get("rejected_records", [])
    require(len(rejected) == 1, "rejected count must be 1")
    reject = rejected[0]
    require(reject.get("source_id") == "factory_execution_traceability", "reject source mismatch")
    require(reject.get("decision") == "reject", "reject decision mismatch")
    require(reject.get("ingestion_allowed") is False, "reject must not be ingested")

    summary = evidence.get("quality_summary", {})
    require(summary.get("candidate_count") == 4, "summary candidate count mismatch")
    require(summary.get("rejected_count") == 1, "summary rejected count mismatch")
    require(summary.get("all_candidates_have_source_provenance") is True, "source provenance summary mismatch")
    require(summary.get("all_candidates_have_review_status") is True, "review status summary mismatch")
    require(summary.get("all_candidates_keep_limited_admission") is True, "limited admission summary mismatch")
    require(summary.get("rejected_records_ingested") == 0, "reject ingestion summary mismatch")
    require(summary.get("credential_leakage_count") == 0, "credential leakage must be zero")
    require(summary.get("canonical_write_count") == 0, "canonical write count must be zero")
    require(summary.get("production_write_count") == 0, "production write count must be zero")
    require(summary.get("status_upgrade_allowed") is False, "status upgrade must be false")

    rollback = evidence.get("rollback", {})
    require(rollback.get("mode") == "remove_dry_run_artifacts_only", "rollback mode mismatch")
    require(rollback.get("canonical_data_touched") is False, "canonical data must not be touched")
    require(rollback.get("production_config_touched") is False, "production config must not be touched")

    for claim in evidence.get("non_claims", []):
        require("does not" in claim, f"non-claim must be explicit: {claim}")

    for phrase in [
        "limited_candidate_ingestion_dry_run_complete",
        "candidate_count | `4`",
        "rejected_records_ingested | `0`",
        "remove_dry_run_artifacts_only",
        "GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "非声明", "下一轮"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_limited_candidate_ingestion_dry_run=pass "
        "candidate_count=4 rejected_count=1 rejected_records_ingested=0 "
        "kds_canonical_write_count=0 production_config_write_count=0 "
        "next=GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
