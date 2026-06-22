#!/usr/bin/env python3
"""Validate Agent-Reach L3 candidate pipeline evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GOAL_DOC = ROOT / "02-governance/loop/LOOP_AGENT_REACH_L3_CANDIDATE_PIPELINE.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-L3-CANDIDATE-PIPELINE-001.md"


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


def require_frontmatter(path: Path, text: str, source_path: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    metadata = text[:end]
    for key in [
        "doc_id:",
        "title:",
        "project:",
        "related_projects:",
        "domain:",
        "status:",
        "version:",
        "owner:",
        "kds_space:",
        "kds_path:",
        "source_path:",
        "sync_direction:",
        "last_reviewed:",
        "supersedes:",
        "superseded_by:",
    ]:
        require(key in metadata, f"{path.relative_to(ROOT)} missing front matter key {key}")
    require(f"source_path: {source_path}" in metadata, f"{path.relative_to(ROOT)} source_path mismatch")


def main() -> int:
    goal_doc = read(GOAL_DOC)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(GOAL_DOC, goal_doc, "02-governance/loop/LOOP_AGENT_REACH_L3_CANDIDATE_PIPELINE.md")
    require_frontmatter(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-L3-CANDIDATE-PIPELINE-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-L3-CANDIDATE-PIPELINE-20260621", "invalid evidence id")
    require(evidence.get("status") == "pass", "pipeline evidence must pass")
    require(evidence.get("mode") == "l3_candidate_pipeline_definition", "invalid mode")
    require(evidence.get("execution_mode") == "read_only_replay_plan", "execution mode must be read-only replay")
    require(evidence.get("external_search_invoked") is False, "external search must not be invoked")

    source_evidence = evidence.get("source_evidence", [])
    for source in [
        "docs/harness/evidence/agent-reach-zero-config-repair-20260620.json",
        "docs/harness/evidence/agent-reach-exa-local-pilot-20260620.json",
        "docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.json",
        "docs/harness/evidence/agent-reach-candidate-search-review-20260620.json",
    ]:
        require(source in source_evidence, f"missing source evidence: {source}")
        require((ROOT / source).exists(), f"source evidence file missing: {source}")

    pipeline = evidence.get("pipeline", {})
    require(pipeline.get("id") == "GPCF-AGENT-REACH-L3-CANDIDATE-PIPELINE-001", "pipeline id mismatch")
    require(pipeline.get("scope") == "project_group_candidate_search", "pipeline scope mismatch")
    require(pipeline.get("output") == "waes_kds_review_queue_item", "pipeline output mismatch")
    require(pipeline.get("admission") == "limited_candidate_only", "pipeline admission mismatch")
    require(len(pipeline.get("stages", [])) == 5, "pipeline must contain five stages")

    targets = evidence.get("quality_targets", {})
    require(targets.get("source_provenance_rate") == 1.0, "target provenance must be 1.0")
    require(targets.get("minimum_search_success_rate") == 0.8, "minimum success rate target mismatch")
    require(targets.get("maximum_duplicate_rate") == 0.2, "duplicate rate target mismatch")
    require(targets.get("credential_leakage_count") == 0, "credential leakage target must be zero")
    require(targets.get("production_write_count") == 0, "production write target must be zero")
    require(targets.get("kds_canonical_write_count") == 0, "KDS canonical write target must be zero")

    metrics = evidence.get("current_verified_metrics", {})
    require(metrics.get("exa_fixed_query_count") == 5, "query count must be 5")
    require(metrics.get("exa_fixed_success_count") == 5, "success count must be 5")
    require(metrics.get("exa_fixed_query_success_rate") == 1.0, "success rate must be 1.0")
    require(metrics.get("source_provenance_rate") == 1.0, "source provenance must be 1.0")
    require(metrics.get("rollback_verified") is True, "rollback must be verified")

    decision = evidence.get("admission_decision", {})
    require(decision.get("waes_review_status") == "ready_for_review", "WAES review status mismatch")
    require(decision.get("kds_admission") == "limited_candidate_only", "KDS admission must remain limited")
    require(decision.get("rag_admission") == "limited", "RAG admission must remain limited")
    require(decision.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(decision.get("production_integration_allowed") is False, "production integration must be false")
    require(decision.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")

    improvement = evidence.get("continuous_improvement", {})
    require(improvement.get("replay_required") is True, "replay must be required")
    require(improvement.get("next_required_artifact") == "candidate_search_replay_ledger", "next artifact mismatch")

    for text, path_text in [
        (goal_doc, "goal document"),
        (evidence_md, "evidence markdown"),
        (loop_round, "loop round"),
    ]:
        for phrase in [
            "不证明 Agent-Reach 已生产集成",
            "不写 KDS canonical",
            "不创建 GFIS source-of-record",
            "不升级",
        ]:
            require(phrase in text, f"{path_text} missing phrase: {phrase}")

    for phrase in [
        "本轮不调用新的外部搜索",
        "candidate_search_replay_ledger",
        "stop_type | authorization_boundary",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_l3_candidate_pipeline=pass "
        "execution_mode=read_only_replay_plan external_search_invoked=false "
        "kds_admission=limited_candidate_only rag_admission=limited "
        "next_gate=candidate_search_replay_ledger status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
