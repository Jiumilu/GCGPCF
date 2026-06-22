#!/usr/bin/env python3
"""Validate Agent-Reach Loop admission planning document."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "03-data-ai-knowledge/GlobalCloud-Agent-Reach搜索能力Loop接入方案.md"

REQUIRED_FRONTMATTER_KEYS = [
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
]

REQUIRED_METRICS = [
    "doctor_available_channel_rate",
    "search_success_rate",
    "citation_validity_rate",
    "source_provenance_rate",
    "duplicate_rate",
    "latency_p50_seconds",
    "latency_p95_seconds",
    "fallback_success_rate",
    "credential_leakage_count",
    "production_write_count",
]

REQUIRED_BOUNDARY_PHRASES = [
    "candidate_search_capability",
    "research_input",
    "不得直接升级为 KDS canonical Markdown",
    "GFIS source-of-record",
    "WAES accepted evidence",
    "GPCF integrated 状态",
    "禁止把 Cookie、Token、代理账号、浏览器登录态导出内容写入 Git",
    "不得替代 KDS、Brain、WAES、GFIS、GPC",
    "不写真实外部平台",
    "不写生产系统",
    "不写真实 KDS API",
]

REQUIRED_ROUNDS = [
    "GPCF-AGENT-REACH-L1-001",
    "GPCF-AGENT-REACH-L2-001",
    "GPCF-AGENT-REACH-BENCH-001",
    "GPCF-AGENT-REACH-GOV-001",
]

FORBIDDEN_PHRASES = [
    "Agent-Reach 已安装到 GlobalCloud 运行环境。",
    "Agent-Reach 已接入真实 KDS",
    "任何登录平台 Cookie 已配置。",
    "GFIS runtime SOP E2E 已通过。",
    "GPCF L4 聚合门禁已修复。",
    "production_ready。",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def frontmatter(path: Path, text: str) -> str:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    return text[:end]


def main() -> int:
    plan = read(PLAN)
    metadata = frontmatter(PLAN, plan)

    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in metadata, f"plan missing front matter key {key}")

    for phrase in [
        "kds_space: 开发",
        "source_path: 03-data-ai-knowledge/GlobalCloud-Agent-Reach搜索能力Loop接入方案.md",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"plan missing controlled marker: {phrase}")
    require(
        "status: draft" in metadata or "status: controlled" in metadata,
        "plan status must be draft or controlled",
    )

    for metric in REQUIRED_METRICS:
        require(metric in plan, f"plan missing metric: {metric}")

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        require(phrase in plan, f"plan missing boundary phrase: {phrase}")

    for round_id in REQUIRED_ROUNDS:
        require(round_id in plan, f"plan missing next round: {round_id}")

    non_claims_start = plan.find("## 10. 非声明")
    require(non_claims_start > 0, "plan missing non-claims section")
    non_claims = plan[non_claims_start:]
    for phrase in FORBIDDEN_PHRASES:
        require(phrase in non_claims, f"non-claims missing phrase: {phrase}")

    print(
        "agent_reach_loop_admission=pass "
        "status=controlled_or_draft candidate_search_capability=true "
        "installation_performed=false credentials_written=false "
        "production_write=false kds_canonical_write=false "
        "status_upgrade_allowed=false next=L2_authorization_required"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
