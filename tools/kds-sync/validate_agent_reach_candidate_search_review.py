#!/usr/bin/env python3
"""Validate Agent-Reach candidate search review evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-candidate-search-review-20260620.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-candidate-search-review-20260620.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-SEARCH-REVIEW-001.md"


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
        "docs/harness/evidence/agent-reach-candidate-search-review-20260620.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-SEARCH-REVIEW-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-CANDIDATE-SEARCH-REVIEW-20260620", "invalid evidence id")
    require(evidence.get("status") == "ready_for_review", "review status must be ready_for_review")
    require(evidence.get("mode") == "candidate_search_capability_review", "invalid mode")

    source_evidence = evidence.get("source_evidence", [])
    require(isinstance(source_evidence, list), "source evidence must be a list")
    for source in [
        "docs/harness/evidence/agent-reach-zero-config-repair-20260620.json",
        "docs/harness/evidence/agent-reach-exa-local-pilot-20260620.json",
        "docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.json",
    ]:
        require(source in source_evidence, f"missing source evidence: {source}")
        require((ROOT / source).exists(), f"source evidence file missing: {source}")

    capability = evidence.get("capability_summary", {})
    require(capability.get("exa_search") == "local_pilot_pass_and_fixed_benchmark_pass", "Exa capability mismatch")
    require(capability.get("cookie_or_login_channels") == "not_admitted", "cookie channels must not be admitted")
    require(capability.get("production_integration") == "not_authorized", "production integration must not be authorized")
    require(set(capability.get("zero_config_channels", [])) == {"web", "github", "rss"}, "zero-config channels mismatch")

    metrics = evidence.get("quality_metrics", {})
    require(metrics.get("zero_config_success_rate") == 1.0, "zero-config success rate must be 1.0")
    require(metrics.get("exa_fixed_query_success_rate") == 1.0, "Exa benchmark success rate must be 1.0")
    require(metrics.get("source_provenance_rate") == 1.0, "source provenance must be 1.0")
    require(metrics.get("credential_leakage_count") == 0, "credential leakage must be zero")
    require(metrics.get("production_write_count") == 0, "production write must be zero")
    require(metrics.get("kds_canonical_write_count") == 0, "KDS canonical write must be zero")
    require(metrics.get("rollback_verified") is True, "rollback must be verified")

    decision = evidence.get("admission_decision", {})
    require(decision.get("waes_review_status") == "ready_for_review", "WAES review status mismatch")
    require(decision.get("kds_admission") == "limited_candidate_only", "KDS admission must remain limited")
    require(decision.get("rag_admission") == "limited", "RAG admission must remain limited")
    require(decision.get("status_upgrade_allowed") is False, "status upgrade must be false")
    require(decision.get("production_integration_allowed") is False, "production integration must be false")
    require(decision.get("accepted_or_integrated_claim_allowed") is False, "accepted/integrated claim must be false")

    controls = evidence.get("continuous_improvement_controls", [])
    require(isinstance(controls, list), "continuous improvement controls must be a list")
    require(len(controls) >= 5, "continuous improvement controls are incomplete")

    for phrase in [
        "状态为 `ready_for_review`",
        "limited_candidate_only",
        "rag_admission | `limited`",
        "status_upgrade_allowed | false",
        "production_integration_allowed | false",
        "不写 KDS canonical Markdown",
        "不把 Exa 结果转成强 RAG 引用",
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
        "agent_reach_candidate_search_review=pass "
        "waes_review_status=ready_for_review kds_admission=limited_candidate_only "
        "rag_admission=limited source_provenance_rate=1.0 "
        "rollback_verified=true status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
