#!/usr/bin/env python3
"""Validate Agent-Reach L2 isolated PoC evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-l2-poc-20260620.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-l2-poc-20260620.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-L2-001.md"


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
        "docs/harness/evidence/agent-reach-l2-poc-20260620.md",
    )
    require_frontmatter(
        LOOP_ROUND,
        loop_round,
        "docs/harness/loops/loop-round-GPCF-AGENT-REACH-L2-001.md",
    )

    require(evidence.get("evidence_id") == "AGENT-REACH-L2-POC-20260620", "invalid evidence id")
    require(evidence.get("status") == "partial", "L2 PoC must remain partial")
    require(evidence.get("mode") == "L2_isolated_poc", "invalid mode")
    require(evidence.get("installation_persisted_to_project") is False, "project install must be false")
    require(evidence.get("credentials_written") is False, "credentials must not be written")
    require(evidence.get("cookies_configured") is False, "cookies must not be configured")
    require(evidence.get("mcp_configuration_changed") is False, "MCP config must remain unchanged")
    require(evidence.get("production_write_count") == 0, "production write count must be zero")
    require(evidence.get("kds_canonical_write_count") == 0, "KDS canonical write count must be zero")
    require(evidence.get("external_platform_write_count") == 0, "external platform write count must be zero")
    require(evidence.get("credential_leakage_count") == 0, "credential leakage count must be zero")
    require(evidence.get("doctor_ok_channels") == 4, "doctor ok channel count changed unexpectedly")
    require(evidence.get("doctor_total_channels") == 13, "doctor total channel count changed unexpectedly")
    require(evidence.get("benchmark_case_count") == 4, "benchmark case count must be 4")
    require(evidence.get("benchmark_success_count") == 2, "benchmark success count must be 2")
    require(evidence.get("search_success_rate") == 0.5, "search success rate must remain partial")
    require(evidence.get("next_gate") == "semantic_search_requires_mcporter_authorization", "invalid next gate")

    cases = evidence.get("cases", [])
    require(isinstance(cases, list), "cases must be a list")
    by_channel = {case.get("channel"): case for case in cases}
    require(by_channel.get("github", {}).get("success") is True, "github benchmark must pass")
    require(by_channel.get("rss", {}).get("success") is True, "rss benchmark must pass")
    require(by_channel.get("web", {}).get("success") is False, "web benchmark must be failed in this evidence")
    require(by_channel.get("exa_search", {}).get("success") is False, "exa benchmark must be failed without authorization")

    for phrase in [
        "结论为 `partial`",
        "不得作为可用能力声明",
        "Cookie 配置 | 否",
        "MCP 配置修改 | 否",
        "生产写入 | 0",
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
        "不进入 L3",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "agent_reach_l2_poc=pass "
        "status=partial doctor_ok_channels=4/13 benchmark_success=2/4 "
        "credentials_written=false mcp_configuration_changed=false "
        "production_write_count=0 kds_canonical_write_count=0 "
        "next_gate=semantic_search_requires_mcporter_authorization"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
