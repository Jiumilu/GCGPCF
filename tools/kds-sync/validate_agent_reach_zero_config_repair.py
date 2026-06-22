#!/usr/bin/env python3
"""Validate Agent-Reach zero-config repair evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-zero-config-repair-20260620.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-zero-config-repair-20260620.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-L2-ZERO-CONFIG-REPAIR-001.md"


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
        "docs/harness/evidence/agent-reach-zero-config-repair-20260620.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-L2-ZERO-CONFIG-REPAIR-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-ZERO-CONFIG-REPAIR-20260620", "invalid evidence id")
    require(evidence.get("status") == "pass", "zero-config repair must pass")
    require(evidence.get("mode") == "L2_zero_config_repair", "invalid mode")
    require(evidence.get("benchmark_case_count") == 4, "benchmark case count must be 4")
    require(evidence.get("benchmark_success_count") == 4, "benchmark success count must be 4")
    require(evidence.get("zero_config_success_rate") == 1.0, "zero-config success rate must be 1.0")
    require(evidence.get("cookies_configured") is False, "cookies must not be configured")
    require(evidence.get("mcp_configuration_changed") is False, "MCP config must remain unchanged")
    require(evidence.get("production_write_count") == 0, "production write count must be zero")
    require(evidence.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")
    require(evidence.get("external_platform_write_count") == 0, "external platform write count must be zero")
    require(evidence.get("credential_leakage_count") == 0, "credential leakage count must be zero")
    require(evidence.get("next_gate") == "mcporter_exa_requires_explicit_authorization", "invalid next gate")

    channels = {case.get("channel") for case in evidence.get("cases", [])}
    require({"web", "github", "rss"}.issubset(channels), "required zero-config channels missing")
    for case in evidence.get("cases", []):
        require(case.get("success") is True, f"case failed: {case.get('name')}")
        require(case.get("rag_admission") == "limited", f"case must remain limited: {case.get('name')}")

    for phrase in [
        "结论为 `pass`，但只限零配置公开渠道",
        "不能替代 Exa 语义搜索",
        "Cookie 配置 | 否",
        "MCP 配置修改 | 否",
        "KDS canonical 写入 | 0",
        "不声明",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in [
        "输入",
        "动作",
        "输出",
        "检查",
        "反馈",
        "stop_type=authorization_boundary",
        "authorization_required",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_zero_config_repair=pass "
        "status=pass zero_config_success=4/4 "
        "cookies_configured=false mcp_configuration_changed=false "
        "production_write_count=0 kds_canonical_write_count=0 "
        "next_gate=mcporter_exa_requires_explicit_authorization"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
