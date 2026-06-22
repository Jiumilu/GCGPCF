#!/usr/bin/env python3
"""Validate Agent-Reach Exa fixed query benchmark evidence."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-FIXED-BENCHMARK-001.md"


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
        "docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-FIXED-BENCHMARK-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-EXA-FIXED-BENCHMARK-20260620", "invalid evidence id")
    require(evidence.get("status") == "pass", "benchmark must pass")
    require(evidence.get("query_count") == 5, "query count must be 5")
    require(evidence.get("success_count") == 5, "success count must be 5")
    require(evidence.get("exa_search_test_success_rate") == 1.0, "success rate must be 1.0")
    require(evidence.get("source_provenance_rate") == 1.0, "source provenance must be complete")
    require(evidence.get("all_results_rag_admission") == "limited", "RAG admission must remain limited")
    require(evidence.get("global_npm_install_performed") is False, "global npm install must be false")
    require(evidence.get("project_dependency_changed") is False, "project dependency changed must be false")
    require(evidence.get("mcp_configuration_scope") == "temporary_home_only", "MCP scope must be temporary")
    require(evidence.get("cookies_configured") is False, "cookies must be false")
    require(evidence.get("production_write_count") == 0, "production write must be zero")
    require(evidence.get("kds_canonical_write_count") == 0, "KDS canonical write must be zero")
    require(evidence.get("credential_leakage_count") == 0, "credential leakage must be zero")
    require(evidence.get("rollback_verified") is True, "rollback must be verified")
    require(evidence.get("mcporter_still_available_after_rollback") is False, "mcporter must not remain available")
    require(evidence.get("temporary_npm_prefix_exists_after_rollback") is False, "temporary prefix must be removed")
    require(evidence.get("temporary_home_exists_after_rollback") is False, "temporary home must be removed")
    require(evidence.get("status_upgrade_allowed") is False, "status upgrade must be false")

    queries = evidence.get("queries", [])
    require(isinstance(queries, list), "queries must be a list")
    require(len(queries) == 5, "queries list must contain 5 entries")
    for query in queries:
        require(query.get("success") is True, f"query failed: {query.get('id')}")
        require(query.get("result_url_count", 0) >= 1, f"query missing URL: {query.get('id')}")
        require(query.get("rag_admission") == "limited", f"query admission must remain limited: {query.get('id')}")

    for phrase in [
        "结论为 `pass`，但只证明 Exa 在 5 个固定公开查询上的候选搜索质量可评估",
        "不得转成强引用",
        "不写 KDS canonical",
        "RAG Admission=limited",
        "不升级任何项目状态",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "stop_type | authorization_boundary",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    require(shutil.which("mcporter") is None, "mcporter must not remain available after rollback")

    print(
        "agent_reach_exa_fixed_benchmark=pass "
        "query_count=5 success_count=5 exa_search_test_success_rate=1.0 "
        "source_provenance_rate=1.0 rag_admission=limited "
        "rollback_verified=true status_upgrade_allowed=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
