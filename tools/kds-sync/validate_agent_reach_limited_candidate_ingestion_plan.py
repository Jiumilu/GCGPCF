#!/usr/bin/env python3
"""Validate Agent-Reach limited candidate ingestion plan evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-limited-candidate-ingestion-plan-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-limited-candidate-ingestion-plan-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001.md"
AUTHORITATIVE_JSON = ROOT / "docs/harness/evidence/agent-reach-authoritative-source-verification-20260621.json"
RECENTER_JSON = ROOT / "docs/harness/evidence/agent-reach-recenter-20260622.json"

UPSTREAM_VALIDATORS = [
    "tools/kds-sync/validate_agent_reach_recenter_20260622.py",
    "tools/kds-sync/validate_agent_reach_authoritative_source_verification.py",
    "tools/kds-sync/validate_agent_reach_candidate_search_replay_ledger.py",
]

ACCEPTED_IDS = {
    "knowledge_provenance_rag",
    "green_supply_chain_policy",
    "ai_agent_evidence_gate",
    "agent_reach_capability",
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
    authoritative = load_json(AUTHORITATIVE_JSON)
    recenter = load_json(RECENTER_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    upstream_outputs = [run_validator(path) for path in UPSTREAM_VALIDATORS]
    require(any("agent_reach_recenter_20260622=pass" in output for output in upstream_outputs), "recenter validator output missing")
    require(any("agent_reach_authoritative_source_verification=pass" in output for output in upstream_outputs), "authoritative validator output missing")

    require(evidence.get("evidence_id") == "AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-20260622", "invalid evidence id")
    require(evidence.get("status") == "limited_candidate_ingestion_plan_ready", "invalid status")
    require(evidence.get("scope") == "GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001", "invalid scope")
    require(evidence.get("next_round") == "GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001", "invalid next round")
    require("docs/harness/evidence/agent-reach-recenter-20260622.json" in evidence.get("source_evidence", []), "missing recenter source")
    require("docs/harness/evidence/agent-reach-authoritative-source-verification-20260621.json" in evidence.get("source_evidence", []), "missing authoritative source")

    require(recenter.get("status") == "agent_reach_mainline_recentered", "recenter status mismatch")
    require(authoritative.get("admission_decision", {}).get("kds_admission") == "limited_candidate_only", "upstream KDS admission mismatch")
    require(authoritative.get("admission_decision", {}).get("production_integration_allowed") is False, "upstream production integration must be false")

    input_status = evidence.get("input_status", {})
    require(input_status.get("accept_limited_count") == 4, "accept_limited_count must be 4")
    require(input_status.get("reject_count") == 1, "reject_count must be 1")
    require(input_status.get("kds_admission") == "limited_candidate_only", "KDS admission mismatch")
    require(input_status.get("rag_admission") == "limited", "RAG admission mismatch")
    require(input_status.get("production_integration_allowed") is False, "production integration must be false")
    require(input_status.get("kds_canonical_write_allowed") is False, "canonical write must be false")

    records = evidence.get("candidate_records", [])
    require(isinstance(records, list) and len(records) == 4, "candidate record count must be 4")
    record_ids = {record.get("id") for record in records}
    require(record_ids == ACCEPTED_IDS, "candidate record ids mismatch")
    for record in records:
        require(record.get("decision") == "accept_limited", f"candidate decision mismatch: {record.get('id')}")
        require(record.get("target_queue") == "waes_kds_limited_candidate_queue", f"target queue mismatch: {record.get('id')}")
        required_fields = record.get("required_fields", [])
        for field in ["candidate_id", "accepted_scope", "verification_reason", "rag_admission", "kds_admission", "provenance_evidence_path", "review_status"]:
            require(field in required_fields, f"missing required field {field}: {record.get('id')}")
        blocked = set(record.get("blocked_outputs", []))
        require(blocked, f"blocked outputs missing: {record.get('id')}")

    rejected = evidence.get("rejected_records", [])
    require(len(rejected) == 1, "rejected record count must be 1")
    reject = rejected[0]
    require(reject.get("id") == "factory_execution_traceability", "reject id mismatch")
    require(reject.get("decision") == "reject", "reject decision mismatch")
    require(reject.get("ingestion_allowed") is False, "reject must not be ingested")

    plan = evidence.get("dry_run_plan", {})
    require(plan.get("execution_mode") == "candidate_metadata_dry_run_only", "execution mode mismatch")
    require(plan.get("output_artifact") == "agent-reach-limited-candidate-ingestion-dry-run-ledger", "output artifact mismatch")
    blocked_targets = set(plan.get("write_targets_blocked", []))
    for target in ["KDS canonical Markdown", "GFIS source-of-record", "production configuration", "global MCP configuration", "strong RAG corpus"]:
        require(target in blocked_targets, f"missing blocked target: {target}")

    gates = evidence.get("quality_gates", {})
    require(gates.get("candidate_count") == 4, "quality gate candidate count mismatch")
    require(gates.get("rejected_count") == 1, "quality gate rejected count mismatch")
    require(gates.get("source_provenance_required") is True, "source provenance must be required")
    require(gates.get("canonical_write_allowed") is False, "canonical write must be false")
    require(gates.get("production_write_allowed") is False, "production write must be false")
    require(gates.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")

    for claim in evidence.get("non_claims", []):
        require("does not" in claim, f"non-claim must be explicit: {claim}")

    for phrase in [
        "limited_candidate_ingestion_plan_ready",
        "candidate_count 必须为 `4`",
        "rejected_count 必须为 `1`",
        "factory_execution_traceability",
        "KDS canonical Markdown",
        "GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "非声明", "下一轮"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_limited_candidate_ingestion_plan=pass "
        "candidate_count=4 rejected_count=1 "
        "kds_admission=limited_candidate_only "
        "canonical_write_allowed=false production_integration_allowed=false "
        "next=GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
