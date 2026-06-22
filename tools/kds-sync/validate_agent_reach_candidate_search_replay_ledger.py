#!/usr/bin/env python3
"""Validate Agent-Reach candidate search replay ledger evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-001.md"


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
        "docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-20260621", "invalid evidence id")
    require(evidence.get("status") == "pass", "ledger evidence must pass")
    require(evidence.get("mode") == "candidate_search_replay_ledger", "invalid mode")
    require(evidence.get("execution_mode") == "read_only_replay_from_existing_evidence", "execution mode mismatch")
    require(evidence.get("external_search_invoked") is False, "external search must not be invoked")

    for source in [
        "docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.json",
        "docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.json",
    ]:
        require(source in evidence.get("source_evidence", []), f"missing source evidence: {source}")
        require((ROOT / source).exists(), f"source evidence file missing: {source}")

    summary = evidence.get("ledger_summary", {})
    require(summary.get("entry_count") == 5, "entry count must be 5")
    require(summary.get("successful_entry_count") == 5, "successful entry count must be 5")
    require(summary.get("search_success_rate") == 1.0, "search success rate must be 1.0")
    require(summary.get("source_provenance_rate") == 1.0, "source provenance must be 1.0")
    require(summary.get("duplicate_rate") == 0.0, "duplicate rate must be 0.0")
    require(summary.get("review_status") == "pending_waes_kds_review", "review status mismatch")

    entries = evidence.get("entries", [])
    require(isinstance(entries, list), "entries must be a list")
    require(len(entries) == 5, "entries must contain 5 records")
    seen_urls: set[str] = set()
    for entry in entries:
        require(entry.get("success") is True, f"entry must succeed: {entry.get('id')}")
        require(entry.get("channel") == "exa_search", f"entry channel mismatch: {entry.get('id')}")
        require(entry.get("result_url_count", 0) >= 1, f"entry missing URL count: {entry.get('id')}")
        require(entry.get("source_provenance_present") is True, f"entry missing provenance: {entry.get('id')}")
        require(entry.get("rag_admission") == "limited", f"entry admission must be limited: {entry.get('id')}")
        require(entry.get("review_status") == "pending_waes_kds_review", f"entry review status mismatch: {entry.get('id')}")
        url = entry.get("first_url")
        require(isinstance(url, str) and url.startswith("https://"), f"entry first_url invalid: {entry.get('id')}")
        require(url not in seen_urls, f"duplicate first_url: {url}")
        seen_urls.add(url)

    decision = evidence.get("admission_decision", {})
    require(decision.get("kds_admission") == "limited_candidate_only", "KDS admission must remain limited")
    require(decision.get("rag_admission") == "limited", "RAG admission must remain limited")
    require(decision.get("waes_review_status") == "pending_waes_kds_review", "WAES review status mismatch")
    require(decision.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(decision.get("production_integration_allowed") is False, "production integration must be false")
    require(decision.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")

    safety = evidence.get("safety", {})
    require(safety.get("credential_leakage_count") == 0, "credential leakage must be zero")
    require(safety.get("production_write_count") == 0, "production write must be zero")
    require(safety.get("kds_canonical_write_count") == 0, "KDS canonical write must be zero")
    require(safety.get("external_platform_write_count") == 0, "external platform write must be zero")

    for phrase in [
        "external_search_invoked=false",
        "pending_waes_kds_review",
        "limited_candidate_only",
        "不写 KDS canonical",
        "不证明 Agent-Reach 已生产集成",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "stop_type | authorization_boundary",
        "本轮不调用新的外部搜索",
        "本轮不升级任何项目状态",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_candidate_search_replay_ledger=pass "
        "entry_count=5 search_success_rate=1.0 source_provenance_rate=1.0 "
        "duplicate_rate=0.0 review_status=pending_waes_kds_review "
        "external_search_invoked=false status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
