#!/usr/bin/env python3
"""Validate Agent-Reach human review decision evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-human-review-decisions-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-human-review-decisions-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-HUMAN-REVIEW-DECISIONS-001.md"


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
        "docs/harness/evidence/agent-reach-human-review-decisions-20260621.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-HUMAN-REVIEW-DECISIONS-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-HUMAN-REVIEW-DECISIONS-20260621", "invalid evidence id")
    require(evidence.get("status") == "pass", "decision evidence must pass")
    require(evidence.get("mode") == "human_review_decisions_accept_reject_defer", "invalid mode")
    require(evidence.get("execution_mode") == "governance_pre_review_without_external_search", "execution mode mismatch")
    require(evidence.get("external_search_invoked") is False, "external search must not be invoked")

    source = "docs/harness/evidence/agent-reach-waes-kds-candidate-review-queue-20260621.json"
    require(source in evidence.get("source_evidence", []), "missing review queue source")
    require((ROOT / source).exists(), "review queue source file missing")

    policy = evidence.get("decision_policy", {})
    require(set(policy.get("allowed_decisions", [])) == {"accept_limited", "reject", "defer"}, "allowed decisions mismatch")
    require(policy.get("auto_accept_allowed") is False, "auto accept must be false")
    require(policy.get("accept_without_authoritative_verification_allowed") is False, "accept without verification must be false")
    require(policy.get("strong_rag_upgrade_allowed") is False, "strong RAG upgrade must be false")
    require(policy.get("kds_canonical_write_allowed") is False, "KDS canonical write must be false")
    require(policy.get("production_integration_allowed") is False, "production integration must be false")

    summary = evidence.get("decision_summary", {})
    require(summary.get("item_count") == 5, "item count must be 5")
    require(summary.get("accept_limited_count") == 0, "accept count must be zero")
    require(summary.get("reject_count") == 0, "reject count must be zero")
    require(summary.get("defer_count") == 5, "defer count must be 5")
    require(summary.get("all_items_have_reason") is True, "all items must have reason")
    require(summary.get("all_items_keep_limited_admission") is True, "all items must keep limited admission")
    require(summary.get("status_upgrade_allowed") is False, "status upgrade must be false")

    decisions = evidence.get("decisions", [])
    require(isinstance(decisions, list) and len(decisions) == 5, "decision list must contain 5 items")
    for item in decisions:
        require(item.get("decision") == "defer", f"decision must be defer: {item.get('id')}")
        require(item.get("rag_admission") == "limited", f"RAG admission must remain limited: {item.get('id')}")
        require(item.get("kds_admission") == "limited_candidate_only", f"KDS admission mismatch: {item.get('id')}")
        require(isinstance(item.get("reason"), str) and len(item["reason"]) >= 20, f"missing reason: {item.get('id')}")
        require(
            isinstance(item.get("required_next_action"), str) and len(item["required_next_action"]) >= 20,
            f"missing next action: {item.get('id')}",
        )

    decision = evidence.get("admission_decision", {})
    require(decision.get("waes_review_status") == "deferred_pending_authoritative_verification", "WAES status mismatch")
    require(decision.get("kds_admission") == "limited_candidate_only", "KDS admission must remain limited")
    require(decision.get("rag_admission") == "limited", "RAG admission must remain limited")
    require(decision.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(decision.get("production_integration_allowed") is False, "production integration must be false")
    require(decision.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")
    require(decision.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")

    for phrase in [
        "5 条候选来源全部保守登记为 `defer`",
        "accept_limited_count | 0",
        "defer_count | 5",
        "不代表 WAES/KDS 已接受这些候选来源",
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
        "agent_reach_human_review_decisions=pass "
        "item_count=5 accept_limited_count=0 reject_count=0 defer_count=5 "
        "waes_review_status=deferred_pending_authoritative_verification "
        "status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
