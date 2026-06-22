#!/usr/bin/env python3
"""Validate Agent-Reach candidate quality trend baseline evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001.md"
REPLAY_JSON = ROOT / "docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.json"
DRY_RUN_JSON = ROOT / "docs/harness/evidence/agent-reach-limited-candidate-ingestion-dry-run-ledger-20260622.json"


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
    replay = load_json(REPLAY_JSON)
    dry_run = load_json(DRY_RUN_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    dry_run_output = run_validator("tools/kds-sync/validate_agent_reach_limited_candidate_ingestion_dry_run.py")
    require("agent_reach_limited_candidate_ingestion_dry_run=pass" in dry_run_output, "dry-run validator output missing")

    require(evidence.get("evidence_id") == "AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-20260622", "invalid evidence id")
    require(evidence.get("status") == "candidate_quality_trend_baseline_ready", "invalid status")
    require(evidence.get("scope") == "GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001", "invalid scope")
    require(evidence.get("execution_mode") == "read_only_quality_trend_baseline", "execution mode mismatch")
    require(evidence.get("external_search_invoked") is False, "external search must not be invoked")
    require(evidence.get("agent_reach_runtime_invoked") is False, "Agent-Reach runtime must not be invoked")
    require(evidence.get("next_round") == "GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001", "invalid next round")

    replay_summary = replay.get("ledger_summary", {})
    baseline = evidence.get("search_replay_baseline", {})
    for key in ["entry_count", "successful_entry_count", "search_success_rate", "source_provenance_rate", "duplicate_rate", "latency_p50_seconds", "latency_p95_seconds", "review_status"]:
        require(baseline.get(key) == replay_summary.get(key), f"search replay baseline mismatch: {key}")

    dry_summary = dry_run.get("quality_summary", {})
    ingestion = evidence.get("ingestion_dry_run_baseline", {})
    require(ingestion.get("candidate_count") == dry_summary.get("candidate_count") == 4, "candidate count mismatch")
    require(ingestion.get("rejected_count") == dry_summary.get("rejected_count") == 1, "rejected count mismatch")
    require(ingestion.get("accepted_limited_rate") == 0.8, "accepted limited rate mismatch")
    for key in [
        "rejected_records_ingested",
        "all_candidates_have_source_provenance",
        "all_candidates_have_review_status",
        "all_candidates_keep_limited_admission",
        "canonical_write_count",
        "production_write_count",
        "credential_leakage_count",
    ]:
        require(ingestion.get(key) == dry_summary.get(key), f"ingestion baseline mismatch: {key}")

    metrics = {item.get("metric"): item for item in evidence.get("trend_metrics", [])}
    require(set(metrics) == {
        "search_success_rate",
        "source_provenance_rate",
        "duplicate_rate",
        "latency_p50_seconds",
        "latency_p95_seconds",
        "accepted_limited_rate",
        "canonical_write_count",
        "production_write_count",
    }, "trend metric set mismatch")
    require(metrics["search_success_rate"]["baseline_value"] == 1.0, "search success metric mismatch")
    require(metrics["source_provenance_rate"]["guardrail"] == "must_remain_1.0_for_candidate_admission", "source provenance guardrail mismatch")
    require(metrics["canonical_write_count"]["baseline_value"] == 0, "canonical write metric mismatch")
    require(metrics["production_write_count"]["baseline_value"] == 0, "production write metric mismatch")

    status = evidence.get("quality_status", {})
    require(status.get("candidate_search_quality") == "baseline_pass", "candidate search status mismatch")
    require(status.get("candidate_ingestion_quality") == "baseline_pass", "candidate ingestion status mismatch")
    require(status.get("safety_quality") == "baseline_pass", "safety status mismatch")
    require(status.get("kds_admission") == "limited_candidate_only", "KDS admission mismatch")
    require(status.get("rag_admission") == "limited", "RAG admission mismatch")
    require(status.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(status.get("production_integration_allowed") is False, "production integration must be false")
    require(status.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")

    controls = evidence.get("continuous_evolution_controls", [])
    require(len(controls) == 5, "continuous controls count mismatch")
    require(any("source provenance rate at 1.0" in item for item in controls), "source provenance control missing")
    require(any("canonical and production write counts at 0" in item for item in controls), "write-count control missing")

    for claim in evidence.get("non_claims", []):
        require("does not" in claim, f"non-claim must be explicit: {claim}")

    for phrase in [
        "candidate_quality_trend_baseline_ready",
        "search_success_rate | `1.0`",
        "candidate_count | `4`",
        "canonical_write_count | `0`",
        "source provenance rate 必须保持 `1.0`",
        "GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈", "非声明", "下一轮"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_candidate_quality_trend_baseline=pass "
        "search_success_rate=1.0 source_provenance_rate=1.0 duplicate_rate=0.0 "
        "candidate_count=4 rejected_count=1 canonical_write_count=0 "
        "next=GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
