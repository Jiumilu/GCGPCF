#!/usr/bin/env python3
"""Validate Agent-Reach WAES/KDS candidate review queue evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-waes-kds-candidate-review-queue-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-waes-kds-candidate-review-queue-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-WAES-KDS-CANDIDATE-REVIEW-QUEUE-001.md"


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
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(
        EVIDENCE_MD,
        evidence_md,
        "docs/harness/evidence/agent-reach-waes-kds-candidate-review-queue-20260621.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-WAES-KDS-CANDIDATE-REVIEW-QUEUE-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-WAES-KDS-CANDIDATE-REVIEW-QUEUE-20260621", "invalid evidence id")
    require(evidence.get("status") == "pass", "queue evidence must pass")
    require(evidence.get("mode") == "waes_kds_candidate_review_queue", "invalid mode")
    require(evidence.get("execution_mode") == "read_only_queue_from_replay_ledger", "execution mode mismatch")
    require(evidence.get("external_search_invoked") is False, "external search must not be invoked")
    require(evidence.get("queue_status") == "ready_for_human_review", "queue status mismatch")

    source = "docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.json"
    require(source in evidence.get("source_evidence", []), "missing replay ledger source")
    require((ROOT / source).exists(), "replay ledger source file missing")

    policy = evidence.get("review_policy", {})
    require(policy.get("default_decision") == "pending", "default decision must be pending")
    require(policy.get("auto_accept_allowed") is False, "auto accept must be false")
    require(policy.get("strong_rag_upgrade_allowed") is False, "strong RAG upgrade must be false")
    require(policy.get("kds_canonical_write_allowed") is False, "KDS canonical write must be false")
    require(policy.get("production_integration_allowed") is False, "production integration must be false")
    require(set(policy.get("allowed_decisions", [])) == {"accept_limited", "reject", "defer"}, "allowed decisions mismatch")

    summary = evidence.get("queue_summary", {})
    require(summary.get("item_count") == 5, "item count must be 5")
    require(summary.get("pending_count") == 5, "pending count must be 5")
    require(summary.get("accepted_count") == 0, "accepted count must be zero")
    require(summary.get("rejected_count") == 0, "rejected count must be zero")
    require(summary.get("deferred_count") == 0, "deferred count must be zero")
    require(summary.get("source_provenance_rate") == 1.0, "source provenance must be 1.0")
    require(summary.get("rag_admission") == "limited", "RAG admission must be limited")
    require(summary.get("kds_admission") == "limited_candidate_only", "KDS admission must be limited candidate only")

    items = evidence.get("items", [])
    require(isinstance(items, list) and len(items) == 5, "queue must contain 5 items")
    for item in items:
        require(item.get("review_decision") == "pending", f"item decision must be pending: {item.get('id')}")
        require(item.get("rag_admission") == "limited", f"item admission must be limited: {item.get('id')}")
        require(item.get("channel") == "exa_search", f"item channel mismatch: {item.get('id')}")
        require(isinstance(item.get("first_url"), str) and item["first_url"].startswith("https://"), f"invalid first_url: {item.get('id')}")
        require(len(item.get("required_review_checks", [])) >= 4, f"item needs review checks: {item.get('id')}")
        require(len(item.get("risk_flags", [])) >= 1, f"item needs risk flags: {item.get('id')}")

    decision = evidence.get("admission_decision", {})
    require(decision.get("waes_review_status") == "ready_for_human_review", "WAES review status mismatch")
    require(decision.get("kds_admission") == "limited_candidate_only", "KDS admission must remain limited")
    require(decision.get("rag_admission") == "limited", "RAG admission must remain limited")
    require(decision.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(decision.get("production_integration_allowed") is False, "production integration must be false")
    require(decision.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")
    require(decision.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")

    for phrase in [
        "ready_for_human_review",
        "auto_accept_allowed | false",
        "pending_count | 5",
        "不代表 WAES/KDS 已人工接受这些候选来源",
        "不写 KDS canonical",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "stop_type | authorization_boundary",
        "本轮不自动 accept 任何候选来源",
        "本轮不升级任何项目状态",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_waes_kds_candidate_review_queue=pass "
        "queue_status=ready_for_human_review item_count=5 pending_count=5 "
        "auto_accept_allowed=false kds_admission=limited_candidate_only "
        "status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
