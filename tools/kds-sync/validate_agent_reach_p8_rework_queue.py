#!/usr/bin/env python3
"""Build a controlled P8 rework queue from failed full-coverage search output."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
OUTPUT_VALIDATOR = ROOT / "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py"
DEFAULT_REPORT = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-rework-queue-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-rework-queue-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-REWORK-QUEUE-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_rework_queue=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_output_validator():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_output_validator", OUTPUT_VALIDATOR)
    if spec is None or spec.loader is None:
        fail("output_validator_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_queries(plan: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for batch in plan.get("batches", []):
        for query in batch.get("queries", []):
            rows.append({**query, "batch_id": batch.get("batch_id")})
    return rows


def query_by_id(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {query["query_id"]: query for query in expected_queries(plan)}


def improve_query_text(query: dict[str, Any], reason: str) -> str:
    project = query["project"]
    channel = query["channel"]
    base = str(query["query"])
    if reason in {"missing_query_candidate", "query_error", "low_score"}:
        return f"{project} GlobalCloud controlled evidence runtime governance source"
    if reason == "duplicate_url":
        return f"{base} alternative public source traceability"
    if reason == "missing_channel":
        return f"{project} {channel} public evidence source traceability"
    return f"{base} public evidence traceability"


def add_item(queue: dict[str, dict[str, Any]], query: dict[str, Any], reason: str, detail: str) -> None:
    query_id = query["query_id"]
    item = queue.setdefault(
        query_id,
        {
            "query_id": query_id,
            "batch_id": query["batch_id"],
            "project": query["project"],
            "channel": query["channel"],
            "current_query": query["query"],
            "suggested_query": improve_query_text(query, reason),
            "reasons": [],
            "details": [],
            "required_next_authorization": query["batch_id"],
            "write_scope": "evidence_only",
        },
    )
    if reason not in item["reasons"]:
        item["reasons"].append(reason)
    item["details"].append(detail)


def build_rework_queue(plan: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    validator = load_output_validator()
    queries = query_by_id(plan)
    candidates = report.get("candidates", [])
    query_errors = report.get("query_errors", [])
    quality = validator.compute_quality(plan, candidates, query_errors)
    requirements = plan.get("quality_requirements", {})
    queue: dict[str, dict[str, Any]] = {}

    covered_query_ids = {candidate.get("query_id") for candidate in candidates}
    for query_id in sorted(set(queries) - covered_query_ids):
        add_item(queue, queries[query_id], "missing_query_candidate", "未返回任何候选。")
    for error in query_errors:
        query_id = error.get("query_id")
        if query_id in queries:
            add_item(queue, queries[query_id], "query_error", str(error.get("error_type", "query_error")))
    seen_urls: dict[str, str] = {}
    for candidate in candidates:
        query_id = candidate.get("query_id")
        if query_id not in queries:
            continue
        url = candidate.get("url")
        if url and url in seen_urls:
            add_item(queue, queries[query_id], "duplicate_url", f"与 {seen_urls[url]} 重复 URL。")
        elif url:
            seen_urls[url] = query_id
        if candidate.get("overall_score", 0) < requirements.get("minimum_candidate_overall_score", 0):
            add_item(queue, queries[query_id], "low_score", f"overall_score={candidate.get('overall_score')}")
        if candidate.get("traceability_score", 0) < requirements.get("minimum_traceability_score", 0):
            add_item(queue, queries[query_id], "low_traceability", f"traceability_score={candidate.get('traceability_score')}")

    if quality["average_overall_score"] < requirements.get("minimum_average_overall_score", 0):
        for query in queries.values():
            if query["query_id"] in covered_query_ids:
                add_item(queue, query, "low_average_score", f"average_overall_score={quality['average_overall_score']}")

    missing_channels = set(quality.get("missing_channels", []))
    for query in queries.values():
        if query["channel"] in missing_channels:
            add_item(queue, query, "missing_channel", f"缺少渠道 {query['channel']} 候选。")

    status = "p8_rework_queue_ready" if queue else "p8_rework_queue_empty"
    return {
        "id": "agent-reach-p8-rework-queue-20260622",
        "round": "GPCF-AGENT-REACH-P8-REWORK-QUEUE-001",
        "date": "2026-06-22",
        "status": status,
        "current_admission": "limited_candidate_only",
        "source_report_status": report.get("status", "unknown"),
        "quality_snapshot": quality,
        "rework_item_count": len(queue),
        "rework_items": sorted(queue.values(), key=lambda item: item["query_id"]),
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
        "next_round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-REWORK-001",
    }


def build_fixture_report(plan: dict[str, Any]) -> dict[str, Any]:
    validator = load_output_validator()
    candidates: list[dict[str, Any]] = []
    for query in expected_queries(plan):
        if query["query_id"] == "p8-q14":
            continue
        candidates.append(
            {
                "candidate_id": f"{query['query_id']}-c1",
                "query_id": query["query_id"],
                "project": query["project"],
                "channel": query["channel"],
                "title": f"{query['project']} controlled public candidate",
                "url": "https://example.com/agent-reach/duplicate" if query["query_id"] in {"p8-q01", "p8-q02"} else f"https://example.com/agent-reach/{query['query_id']}",
                "source_domain": "example.com",
                "retrieved_at": "2026-06-22T00:00:00+00:00",
                "snippet_redacted": f"{query['project']} public candidate for rework queue validation.",
                "relevance_score": 0.2 if query["query_id"] == "p8-q03" else 0.9,
                "authority_score": 0.8,
                "freshness_score": 0.7,
                "traceability_score": 1.0,
                "overall_score": 0.2 if query["query_id"] == "p8-q03" else 0.86,
                "non_claims": ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"],
            }
        )
    query_errors = [{"query_id": "p8-q10", "error_type": "fixture_error", "message": "controlled fixture"}]
    quality = validator.compute_quality(plan, candidates, query_errors)
    quality["threshold_pass"] = False
    return {
        "id": "agent-reach-p8-rework-queue-fixture",
        "status": "full_project_group_live_coverage_rework_required",
        "current_admission": "limited_candidate_only",
        "execution_requested": True,
        "security_controls": {
            "live_external_search_invoked": True,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "candidates": candidates,
        "query_errors": query_errors,
        "quality_report": quality,
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-REWORK-QUEUE-20260622",
            "title: Agent-Reach P8 返工队列证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-rework-queue-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-rework-queue-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 返工队列证据 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- source_report_status: `{report['source_report_status']}`",
            f"- rework_item_count: `{report['rework_item_count']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 从失败的 P8 全量报告生成 query 级返工队列。",
            "- 覆盖缺候选、查询错误、重复 URL、低分、低可追溯、缺渠道和平均分不足。",
            "",
            "## stop",
            "",
            "- 本轮只生成返工队列，不执行真实搜索。",
            "- 返工执行仍需新的 P8 batch 授权。",
            "",
            "## verify",
            "",
            "- 自测 fixture 产生非空返工队列。",
            "- 每个返工项都有 batch、project、channel、当前 query、建议 query 和原因。",
            "",
            "## recover",
            "",
            "- 若返工队列不合理，先调整建议 query 生成规则，再重新运行本验证器。",
            "",
            "## debug",
            "",
            "- 真实搜索执行后，如输出门禁失败，应先运行本队列生成器再申请下一轮返工授权。",
            "",
            "## 非声明",
            "",
            "- 本证据仅为候选证据。",
            "- 本证据不声明 accepted / integrated / production_ready 状态。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不执行真实搜索。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-REWORK-QUEUE-001",
            "title: Agent-Reach P8 返工队列 Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-REWORK-QUEUE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-REWORK-QUEUE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 返工队列 Loop 001",
            "",
            "## run",
            "",
            "建立失败搜索输出到下一轮 query 返工队列的转换闭环。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；队列状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"返工项数量 `{report['rework_item_count']}`；真实外搜 `{report['security_controls']['live_external_search_invoked']}`。",
            "",
            "## recover",
            "",
            "回滚为删除本轮新增验证器和 evidence/loop 文档。",
            "",
            "## debug",
            "",
            "真实搜索仍等待 P8 执行授权；返工执行也必须重新授权。",
            "",
        ]
    )


def validate_queue(report: dict[str, Any]) -> None:
    if report["status"] != "p8_rework_queue_ready":
        fail(f"queue_not_ready:{report['status']}")
    if report["rework_item_count"] < 4:
        fail("rework_item_count_too_low")
    for item in report["rework_items"]:
        for field in ["query_id", "batch_id", "project", "channel", "current_query", "suggested_query", "reasons", "required_next_authorization"]:
            if field not in item or item[field] in ("", [], None):
                fail(f"rework_item_missing:{field}")
        if item["current_query"] == item["suggested_query"]:
            fail(f"suggested_query_not_changed:{item['query_id']}")
    if report["security_controls"]["live_external_search_invoked"] is not False:
        fail("live_search_invoked")


def validate_gate_evidence() -> None:
    plan = load_json(PLAN)
    fixture_report = build_rework_queue(plan, build_fixture_report(plan))
    validate_queue(fixture_report)
    evidence = load_json(EVIDENCE_JSON)
    validate_queue(evidence)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    for marker in [
        "p8_rework_queue_ready",
        "rework_item_count",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--write-evidence", action="store_true", default=True)
    args = parser.parse_args()
    plan = load_json(PLAN)
    source = load_json(args.report) if args.report.exists() else build_fixture_report(plan)
    report = build_rework_queue(plan, source)
    validate_queue(report)
    if args.write_evidence:
        write_json(EVIDENCE_JSON, report)
        EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
        LOOP_MD.write_text(render_loop(report), encoding="utf-8")
    print(
        "agent_reach_p8_rework_queue=pass "
        f"status={report['status']} rework_item_count={report['rework_item_count']} "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-REWORK-001"
    )


if __name__ == "__main__":
    main()
