#!/usr/bin/env python3
"""Validate P8 planned queries before spending live-search authorization."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-query-quality-preflight-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-query-quality-preflight-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-QUERY-QUALITY-PREFLIGHT-001.md"

PROJECTS = {
    "GPCF",
    "KDS",
    "WAES",
    "Brain",
    "GFIS",
    "GPC",
    "PVAOS",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
}
CHANNELS = {"web", "rss", "bilibili"}
INTENT_TERMS = {
    "admission",
    "assistant",
    "control",
    "controlled",
    "evidence",
    "governance",
    "harness",
    "knowledge",
    "ontology",
    "quality",
    "record",
    "runtime",
    "search",
    "source",
    "workbench",
}
GENERIC_ONLY_TERMS = {"project", "globalcloud", "search", "quality", "governance", "evidence"}
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_query_quality_preflight=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalized_query(query: str) -> str:
    return " ".join(TOKEN_RE.findall(query.lower()))


def tokens(query: str) -> list[str]:
    return TOKEN_RE.findall(query)


def planned_queries(plan: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for batch in plan.get("batches", []):
        for query in batch.get("queries", []):
            rows.append({**query, "batch_id": batch.get("batch_id")})
    return rows


def query_score(row: dict[str, Any]) -> dict[str, Any]:
    query = str(row.get("query", ""))
    token_list = tokens(query)
    token_set = {token.lower() for token in token_list}
    project = str(row.get("project", ""))
    project_token_present = project.lower() in token_set
    intent_term_count = len(token_set & INTENT_TERMS)
    non_generic_count = len(token_set - GENERIC_ONLY_TERMS)
    reasons: list[str] = []
    if not 4 <= len(token_list) <= 9:
        reasons.append("token_count_outside_4_to_9")
    if not project_token_present:
        reasons.append("project_token_missing")
    if intent_term_count < 2:
        reasons.append("intent_terms_below_2")
    if non_generic_count < 2:
        reasons.append("too_generic")
    if row.get("channel") not in CHANNELS:
        reasons.append("channel_out_of_scope")
    if row.get("project") not in PROJECTS:
        reasons.append("project_out_of_scope")
    return {
        "query_id": row.get("query_id"),
        "project": project,
        "channel": row.get("channel"),
        "query": query,
        "token_count": len(token_list),
        "project_token_present": project_token_present,
        "intent_term_count": intent_term_count,
        "non_generic_count": non_generic_count,
        "threshold_pass": not reasons,
        "reasons": reasons,
    }


def build_report() -> dict[str, Any]:
    plan = load_json(PLAN)
    rows = planned_queries(plan)
    scores = [query_score(row) for row in rows]
    normalized = [normalized_query(str(row.get("query", ""))) for row in rows]
    duplicate_normalized_count = len(normalized) - len(set(normalized))
    projects = {row.get("project") for row in rows}
    channels = {row.get("channel") for row in rows}
    failing = [score for score in scores if not score["threshold_pass"]]
    status = "p8_query_quality_preflight_pass" if not failing and duplicate_normalized_count == 0 else "p8_query_quality_preflight_rework_required"
    return {
        "id": "agent-reach-p8-query-quality-preflight-20260622",
        "round": "GPCF-AGENT-REACH-P8-QUERY-QUALITY-PREFLIGHT-001",
        "date": "2026-06-22",
        "status": status,
        "current_admission": "limited_candidate_only",
        "query_count": len(rows),
        "project_coverage": round(len(projects & PROJECTS) / len(PROJECTS), 4),
        "channel_coverage": round(len(channels & CHANNELS) / len(CHANNELS), 4),
        "duplicate_normalized_query_count": duplicate_normalized_count,
        "failing_query_count": len(failing),
        "query_scores": scores,
        "security_controls": {
            "live_external_search_invoked": False,
            "agent_reach_binary_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "non_claims": [
            "not_live_search_invoked",
            "not_full_project_group_live_coverage_completed",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
        "next_round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001",
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-QUERY-QUALITY-PREFLIGHT-20260622",
            "title: Agent-Reach P8 查询质量预检证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-query-quality-preflight-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-query-quality-preflight-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 查询质量预检证据 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- query_count: `{report['query_count']}`",
            f"- project_coverage: `{report['project_coverage']}`",
            f"- channel_coverage: `{report['channel_coverage']}`",
            f"- duplicate_normalized_query_count: `{report['duplicate_normalized_query_count']}`",
            f"- failing_query_count: `{report['failing_query_count']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 对 P8 三批 14 条计划查询执行离线质量预检。",
            "- 检查项目词、意图词、非泛化词、长度、重复查询和渠道范围。",
            "",
            "## stop",
            "",
            "- 本轮只校验查询计划，不执行真实搜索。",
            "- 若后续修改查询计划，必须重新运行本预检。",
            "",
            "## verify",
            "",
            "- 14/14 项目仍在计划覆盖内。",
            "- web/rss/bilibili 三类渠道仍在计划覆盖内。",
            "- 预检不创建授权文件，不调用外部网络。",
            "",
            "## recover",
            "",
            "- 若预检失败，优先修订对应 query 文本，不扩大 batch 数量或授权范围。",
            "",
            "## debug",
            "",
            "- 下一步仍需 P8 三批执行授权，授权后才能运行真实搜索 pipeline。",
            "",
            "## 非声明",
            "",
            "- 本证据仅为候选证据。",
            "- 本证据不声明 accepted / integrated / production_ready 状态。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不持久化 raw provider payload。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-QUERY-QUALITY-PREFLIGHT-001",
            "title: Agent-Reach P8 查询质量预检 Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-QUERY-QUALITY-PREFLIGHT-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-QUERY-QUALITY-PREFLIGHT-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 查询质量预检 Loop 001",
            "",
            "## run",
            "",
            "执行 P8 查询计划离线质量预检，减少真实搜索授权后的低质量查询风险。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；预检状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"查询数 `{report['query_count']}`；失败查询数 `{report['failing_query_count']}`；重复标准化查询数 `{report['duplicate_normalized_query_count']}`。",
            "",
            "## recover",
            "",
            "回滚为恢复 P8 查询计划文本，并删除本轮预检 evidence/loop 文档。",
            "",
            "## debug",
            "",
            "真实搜索仍等待 P8 Batch 1、Batch 2、Batch 3 执行授权。",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    if report["project_coverage"] != 1.0:
        fail("project_coverage_not_full")
    if report["channel_coverage"] != 1.0:
        fail("channel_coverage_not_full")
    if report["duplicate_normalized_query_count"] != 0:
        fail("duplicate_normalized_query")
    if report["failing_query_count"] != 0:
        failing_ids = ",".join(score["query_id"] for score in report["query_scores"] if not score["threshold_pass"])
        fail(f"query_quality_failed:{failing_ids}")
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    LOOP_MD.write_text(render_loop(report), encoding="utf-8")
    print(
        "agent_reach_p8_query_quality_preflight=pass "
        "status=p8_query_quality_preflight_pass "
        "query_count=14 project_coverage=1.0 channel_coverage=1.0 "
        "duplicate_normalized_query_count=0 failing_query_count=0 "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
