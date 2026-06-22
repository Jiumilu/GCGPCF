#!/usr/bin/env python3
"""Validate Agent-Reach authoritative source verification evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-authoritative-source-verification-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-authoritative-source-verification-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-AUTHORITATIVE-SOURCE-VERIFICATION-001.md"


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
        "docs/harness/evidence/agent-reach-authoritative-source-verification-20260621.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-AUTHORITATIVE-SOURCE-VERIFICATION-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-AUTHORITATIVE-SOURCE-VERIFICATION-20260621", "invalid evidence id")
    require(evidence.get("status") == "pass", "verification evidence must pass")
    require(evidence.get("mode") == "authoritative_source_verification_for_deferred_items", "invalid mode")
    require(evidence.get("agent_reach_search_invoked") is False, "Agent-Reach search must not be invoked")
    require(evidence.get("external_source_verification_performed") is True, "external source verification must be true")

    source = "docs/harness/evidence/agent-reach-human-review-decisions-20260621.json"
    require(source in evidence.get("source_evidence", []), "missing human review decisions source")
    require((ROOT / source).exists(), "human review decisions source file missing")

    summary = evidence.get("decision_summary", {})
    require(summary.get("item_count") == 5, "item count must be 5")
    require(summary.get("accept_limited_count") == 4, "accept_limited count must be 4")
    require(summary.get("reject_count") == 1, "reject count must be 1")
    require(summary.get("defer_count") == 0, "defer count must be 0")
    require(summary.get("all_items_have_reason") is True, "all items must have reason")
    require(summary.get("all_items_keep_limited_admission") is True, "all items must keep limited admission")
    require(summary.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")
    require(summary.get("status_upgrade_allowed") is False, "status upgrade must be false")

    verifications = evidence.get("verifications", [])
    require(isinstance(verifications, list) and len(verifications) == 5, "verification list must contain 5 items")
    decisions = {item.get("id"): item.get("decision") for item in verifications}
    require(decisions == {
        "knowledge_provenance_rag": "accept_limited",
        "green_supply_chain_policy": "accept_limited",
        "factory_execution_traceability": "reject",
        "ai_agent_evidence_gate": "accept_limited",
        "agent_reach_capability": "accept_limited",
    }, "decision map mismatch")
    for item in verifications:
        require(item.get("rag_admission") == "limited", f"RAG admission must remain limited: {item.get('id')}")
        require(item.get("kds_admission") == "limited_candidate_only", f"KDS admission mismatch: {item.get('id')}")
        require(isinstance(item.get("reason"), str) and len(item["reason"]) >= 20, f"missing reason: {item.get('id')}")
        require(len(item.get("verification_sources", [])) >= 1, f"missing verification source: {item.get('id')}")

    decision = evidence.get("admission_decision", {})
    require(decision.get("waes_review_status") == "limited_verification_complete", "WAES status mismatch")
    require(decision.get("kds_admission") == "limited_candidate_only", "KDS admission must remain limited")
    require(decision.get("rag_admission") == "limited", "RAG admission must remain limited")
    require(decision.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(decision.get("production_integration_allowed") is False, "production integration must be false")
    require(decision.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")
    require(decision.get("strong_rag_upgrade_allowed") is False, "strong RAG upgrade must be false")
    require(decision.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")

    for phrase in [
        "4 条进入 `accept_limited`，1 条登记为 `reject`",
        "accept_limited_count | 4",
        "reject_count | 1",
        "不写 KDS canonical",
        "不代表 WAES/KDS 已将这些来源写入主知识库",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "stop_type | authorization_boundary",
        "本轮不写 KDS canonical",
        "本轮不升级任何项目状态",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_authoritative_source_verification=pass "
        "accept_limited_count=4 reject_count=1 defer_count=0 "
        "kds_admission=limited_candidate_only rag_admission=limited "
        "status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
