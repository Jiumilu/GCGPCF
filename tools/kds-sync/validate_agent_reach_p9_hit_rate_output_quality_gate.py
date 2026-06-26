#!/usr/bin/env python3
"""Validate Agent-Reach P9 priority target hit-rate live output quality."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-precheck-20260626.json"
DEFAULT_REPORT = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-live-run-20260626.json"
DEFAULT_MARKDOWN = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-live-run-20260626.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-hit-rate-output-quality-gate-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-hit-rate-output-quality-gate-20260626.md"

TOPICS = {"green_supply_chain", "phosphogypsum", "industrial_solid_waste", "zero_waste_city"}
SECURITY_FALSE_FIELDS = [
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]
REQUIRED_CANDIDATE_FIELDS = {
    "candidate_id",
    "query_id",
    "project",
    "channel",
    "title",
    "url",
    "source_domain",
    "retrieved_at",
    "snippet_redacted",
    "relevance_score",
    "authority_score",
    "freshness_score",
    "traceability_score",
    "overall_score",
    "non_claims",
    "topic_id",
    "topic_label",
    "expected_priority_domains",
    "business_fields",
    "raw_overall_score",
    "domain_boost",
    "boosted_overall_score",
    "priority_domain_level",
    "expected_priority_domain_hit",
}
RAW_PAYLOAD_KEYS = {"raw", "raw_payload", "provider_payload", "response_body", "html", "cookie", "authorization"}
TOKEN_PATTERN = re.compile(r"(?i)(api[_-]?key|token|secret|authorization|cookie)[=:]\S+")
FORBIDDEN_CLAIMS = {"accepted", "integrated", "production_ready"}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_hit_rate_output_quality_gate=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def planned_queries(precheck: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for topic in precheck.get("topics", []):
        for query in topic.get("query_expansion", []):
            rows.append({**query, "topic_id": topic["topic_id"], "topic_label": topic["label"]})
    return rows


def contains_raw_payload(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in RAW_PAYLOAD_KEYS or contains_raw_payload(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_raw_payload(item) for item in value)
    return False


def parse_retrieved_at(value: str, candidate_id: str) -> None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        fail(f"candidate_retrieved_at_invalid_iso8601:{candidate_id}")
    if parsed.tzinfo is None:
        fail(f"candidate_retrieved_at_missing_timezone:{candidate_id}")


def validate_url(candidate: dict[str, Any]) -> None:
    candidate_id = candidate["candidate_id"]
    parsed = urlparse(candidate["url"])
    if parsed.scheme not in {"http", "https"}:
        fail(f"candidate_url_scheme_invalid:{candidate_id}")
    if not parsed.hostname:
        fail(f"candidate_url_host_missing:{candidate_id}")
    if parsed.hostname.lower() != str(candidate["source_domain"]).lower():
        fail(f"candidate_source_domain_mismatch:{candidate_id}")


def expected_boost(domain: str, precheck: dict[str, Any]) -> tuple[str, float]:
    policy = precheck["domain_boost_policy"]
    p0_domains = set(policy["priority_domains"]["P0"])
    p1_domains = set(policy["priority_domains"]["P1"])
    level = "none"
    boost = 0.0
    if domain in p0_domains:
        level = "P0"
        boost += policy["p0_domain_boost"]
    elif domain in p1_domains:
        level = "P1"
        boost += policy["p1_domain_boost"]
    if domain.endswith(".gov.cn") or domain in {"mee.gov.cn", "miit.gov.cn", "ndrc.gov.cn", "pbc.gov.cn"}:
        boost += policy["official_government_domain_boost"]
    return level, round(boost, 4)


def compute_topic_report(precheck: dict[str, Any], candidates: list[dict[str, Any]], query_errors: list[dict[str, Any]]) -> dict[str, Any]:
    topic_reports: dict[str, Any] = {}
    p0_domains = set(precheck["domain_boost_policy"]["priority_domains"]["P0"])
    for topic in precheck["topics"]:
        topic_id = topic["topic_id"]
        topic_candidates = [candidate for candidate in candidates if candidate.get("topic_id") == topic_id]
        hit_domains = {candidate["source_domain"] for candidate in topic_candidates if candidate.get("expected_priority_domain_hit")}
        p0_hit_domains = hit_domains & p0_domains
        expected_query_ids = {query["query_id"] for query in topic["query_expansion"]}
        covered_query_ids = {candidate["query_id"] for candidate in topic_candidates}
        missing_query_ids = sorted(expected_query_ids - covered_query_ids)
        topic_reports[topic_id] = {
            "candidate_count": len(topic_candidates),
            "expected_priority_domain_hit_count": len(hit_domains),
            "expected_p0_domain_hit_count": len(p0_hit_domains),
            "query_candidate_coverage": round(len(covered_query_ids) / len(expected_query_ids), 4),
            "missing_query_ids": missing_query_ids,
            "threshold_pass": (
                len(p0_hit_domains) >= topic["minimum_p0_domain_hits_required"]
                and len(hit_domains) >= topic["minimum_total_domain_hits_required"]
                and not missing_query_ids
            ),
        }
    return {
        "candidate_count": len(candidates),
        "query_error_count": len(query_errors),
        "topic_reports": topic_reports,
        "topic_coverage": round(sum(1 for item in topic_reports.values() if item["threshold_pass"]) / len(topic_reports), 4),
        "threshold_pass": bool(topic_reports) and all(item["threshold_pass"] for item in topic_reports.values()) and not query_errors,
    }


def validate_report(report: dict[str, Any], markdown: str, precheck: dict[str, Any]) -> None:
    if report.get("status") != "p9_priority_target_hit_rate_completed":
        fail(f"status_not_completed:{report.get('status')}")
    if report.get("current_admission") != "limited_candidate_only":
        fail("current_admission_mismatch")
    if report.get("execution_requested") is not True:
        fail("execution_not_requested")
    if report.get("planned_query_count") != len(planned_queries(precheck)):
        fail("planned_query_count_mismatch")

    controls = report.get("security_controls", {})
    if controls.get("live_external_search_invoked") is not True:
        fail("live_external_search_not_invoked")
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    if report.get("query_errors"):
        fail(f"query_errors_present:{len(report['query_errors'])}")
    if contains_raw_payload(report):
        fail("raw_provider_payload_persisted")

    expected_query_ids = {query["query_id"] for query in planned_queries(precheck)}
    expected_by_query = {query["query_id"]: query for query in planned_queries(precheck)}
    seen_candidate_ids: set[str] = set()
    policy = precheck["domain_boost_policy"]
    max_boosted = policy["maximum_boosted_overall_score"]
    for candidate in report.get("candidates", []):
        missing = sorted(REQUIRED_CANDIDATE_FIELDS - set(candidate))
        if missing:
            fail(f"candidate_missing_fields:{candidate.get('candidate_id')}:{','.join(missing)}")
        candidate_id = candidate["candidate_id"]
        if candidate_id in seen_candidate_ids:
            fail(f"duplicate_candidate_id:{candidate_id}")
        seen_candidate_ids.add(candidate_id)
        if candidate["query_id"] not in expected_query_ids:
            fail(f"candidate_query_out_of_scope:{candidate['query_id']}")
        query = expected_by_query[candidate["query_id"]]
        if candidate["topic_id"] != query["topic_id"]:
            fail(f"candidate_topic_mismatch:{candidate_id}")
        if candidate["topic_label"] != query["topic_label"]:
            fail(f"candidate_topic_label_mismatch:{candidate_id}")
        if candidate["channel"] != query["channel"]:
            fail(f"candidate_channel_mismatch:{candidate_id}")
        if set(candidate["expected_priority_domains"]) != set(query["expected_priority_domains"]):
            fail(f"candidate_expected_domains_mismatch:{candidate_id}")
        if not set(candidate["business_fields"]).issubset(set(query["business_fields"])):
            fail(f"candidate_business_fields_mismatch:{candidate_id}")
        validate_url(candidate)
        parse_retrieved_at(str(candidate["retrieved_at"]), candidate_id)
        if not str(candidate["snippet_redacted"]).strip():
            fail(f"candidate_snippet_redacted_empty:{candidate_id}")
        if TOKEN_PATTERN.search(json.dumps(candidate, ensure_ascii=False)):
            fail(f"candidate_credential_leak:{candidate_id}")
        if FORBIDDEN_CLAIMS & set(candidate["non_claims"]):
            fail(f"candidate_forbidden_claim:{candidate_id}")
        for claim in ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"]:
            if claim not in set(candidate["non_claims"]):
                fail(f"candidate_non_claim_missing:{candidate_id}:{claim}")
        for field in ["relevance_score", "authority_score", "freshness_score", "traceability_score", "overall_score", "raw_overall_score", "domain_boost", "boosted_overall_score"]:
            score = candidate[field]
            if not isinstance(score, (int, float)) or not 0 <= score <= 1:
                fail(f"candidate_score_out_of_range:{candidate_id}:{field}")
        level, boost = expected_boost(candidate["source_domain"], precheck)
        if candidate["priority_domain_level"] != level:
            fail(f"candidate_priority_level_mismatch:{candidate_id}")
        if candidate["domain_boost"] != boost:
            fail(f"candidate_domain_boost_mismatch:{candidate_id}")
        if candidate["boosted_overall_score"] != min(max_boosted, round(candidate["raw_overall_score"] + boost, 4)):
            fail(f"candidate_boosted_score_mismatch:{candidate_id}")
        if candidate["boosted_overall_score"] < candidate["raw_overall_score"]:
            fail(f"candidate_boosted_below_raw:{candidate_id}")
        if candidate["expected_priority_domain_hit"] != (candidate["source_domain"] in set(query["expected_priority_domains"])):
            fail(f"candidate_expected_hit_mismatch:{candidate_id}")

    computed = compute_topic_report(precheck, report.get("candidates", []), report.get("query_errors", []))
    if computed != report.get("hit_rate_report"):
        fail("hit_rate_report_mismatch")
    if computed["topic_coverage"] != 1.0 or computed["threshold_pass"] is not True:
        fail("hit_rate_threshold_not_passed")
    if set(computed["topic_reports"]) != TOPICS:
        fail("topic_set_mismatch")
    for topic_id, topic_report in computed["topic_reports"].items():
        if topic_report["missing_query_ids"]:
            fail(f"topic_missing_query_ids:{topic_id}")
        if topic_report["query_candidate_coverage"] != 1.0:
            fail(f"topic_query_candidate_coverage_below_one:{topic_id}")

    for marker in [
        "candidate-only",
        "does not create source-of-record",
        "does not claim accepted, integrated, or production_ready status",
    ]:
        if marker not in markdown:
            fail(f"markdown_missing:{marker}")


def build_self_test_report(precheck: dict[str, Any]) -> tuple[dict[str, Any], str]:
    candidates: list[dict[str, Any]] = []
    for query in planned_queries(precheck):
        domain = query["expected_priority_domains"][0]
        level, boost = expected_boost(domain, precheck)
        raw = 0.74
        candidates.append(
            {
                "candidate_id": f"{query['query_id']}-p9-c1",
                "query_id": query["query_id"],
                "project": "GFIS",
                "channel": query["channel"],
                "title": f"{query['topic_label']} priority target candidate",
                "url": f"https://{domain}/agent-reach/{query['query_id']}",
                "source_domain": domain,
                "retrieved_at": "2026-06-26T00:00:00+00:00",
                "snippet_redacted": f"{query['topic_label']} public candidate for priority hit-rate validation.",
                "relevance_score": 0.82,
                "authority_score": 0.86,
                "freshness_score": 0.72,
                "traceability_score": 1.0,
                "overall_score": raw,
                "non_claims": ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"],
                "topic_id": query["topic_id"],
                "topic_label": query["topic_label"],
                "expected_priority_domains": query["expected_priority_domains"],
                "business_fields": query["business_fields"],
                "raw_overall_score": raw,
                "domain_boost": boost,
                "boosted_overall_score": min(precheck["domain_boost_policy"]["maximum_boosted_overall_score"], round(raw + boost, 4)),
                "priority_domain_level": level,
                "expected_priority_domain_hit": True,
            }
        )
    report = {
        "id": "agent-reach-p9-priority-target-hit-rate-live-run-20260626",
        "date": "2026-06-26",
        "status": "p9_priority_target_hit_rate_completed",
        "current_admission": "limited_candidate_only",
        "authorization_valid": True,
        "authorization_reasons": [],
        "authorization_path": "fixtures/agent-reach/p9-priority-target-hit-rate-authorization.local.json",
        "execution_requested": True,
        "planned_query_count": len(planned_queries(precheck)),
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
        "non_claims": ["candidate_only", "not_source_of_record", "not_kds_canonical_written", "not_gfis_source_of_record_written", "not_accepted", "not_integrated", "not_production_ready"],
        "candidates": candidates,
        "query_errors": [],
    }
    report["hit_rate_report"] = compute_topic_report(precheck, candidates, [])
    markdown = "\n".join(
        [
            "# Agent-Reach P9 Priority Hit Rate",
            "This evidence is candidate-only.",
            "This evidence does not create source-of-record.",
            "This evidence does not claim accepted, integrated, or production_ready status.",
        ]
    )
    return report, markdown


def build_negative_test_report(precheck: dict[str, Any], case: str) -> tuple[dict[str, Any], str, str]:
    report, markdown = build_self_test_report(precheck)
    if case == "status":
        report["status"] = "p9_priority_target_hit_rate_rework_required"
        return report, markdown, "status_not_completed"
    if case == "query-error":
        report["query_errors"] = [{"query_id": "p9-gsc-q01", "error_type": "negative_fixture"}]
        report["hit_rate_report"] = compute_topic_report(precheck, report["candidates"], report["query_errors"])
        return report, markdown, "query_errors_present:1"
    if case == "missing-topic-query":
        report["candidates"] = [candidate for candidate in report["candidates"] if candidate["query_id"] != "p9-gsc-q01"]
        report["hit_rate_report"] = compute_topic_report(precheck, report["candidates"], [])
        return report, markdown, "hit_rate_threshold_not_passed"
    if case == "bad-boost":
        report["candidates"][0]["domain_boost"] = 0
        report["hit_rate_report"] = compute_topic_report(precheck, report["candidates"], [])
        return report, markdown, "candidate_domain_boost_mismatch"
    if case == "raw-payload":
        report["raw_payload"] = {"html": "<html>negative fixture</html>"}
        return report, markdown, "raw_provider_payload_persisted"
    if case == "credential-leak":
        report["candidates"][0]["snippet_redacted"] = "token=abc123"
        return report, markdown, "candidate_credential_leak"
    if case == "forbidden-claim":
        report["candidates"][0]["non_claims"].append("accepted")
        return report, markdown, "candidate_forbidden_claim"
    if case == "missing-marker":
        return report, "candidate-only", "markdown_missing:does not create source-of-record"
    fail(f"unknown_negative_test:{case}")


def run_negative_test(precheck: dict[str, Any], case: str) -> None:
    report, markdown, expected = build_negative_test_report(precheck, case)
    try:
        validate_report(report, markdown, precheck)
    except SystemExit as exc:
        if expected in str(exc):
            return
        raise
    fail(f"negative_test_unexpected_pass:{case}")


def render_markdown(report: dict[str, Any]) -> str:
    checks = report["validator_checks"]
    lines = [
        "---",
        "doc_id: GPCF-DOC-AGENT-REACH-P9-HIT-RATE-OUTPUT-QUALITY-GATE-20260626",
        "title: Agent-Reach P9 命中率输出质量门禁 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-hit-rate-output-quality-gate-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-hit-rate-output-quality-gate-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9 命中率输出质量门禁 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- planned_query_count: `{report['planned_query_count']}`",
        f"- topics: `{', '.join(report['topics'])}`",
        f"- self_test_passed_without_network: `{checks['self_test_passed_without_network']}`",
        f"- live_external_search_invoked: `{report['live_external_search_invoked']}`",
        "",
        "## 校验范围",
        "",
        "- 要求 P9 live 输出状态为 `p9_priority_target_hit_rate_completed`。",
        "- 要求 4 个主题全部达到 query coverage 与 P0/P1 重点域名命中阈值。",
        "- 校验 domain boost、source scoring、GFIS/WAS/WAES/KDS 业务字段映射和 candidate-only non-claim。",
        "- 阻断 raw provider payload、credential/cookie 泄漏、accepted / integrated / production_ready 声明。",
        "- 本门禁不执行真实搜索，只校验已有输出或离线自测 fixture。",
        "",
        "## Validator Checks",
        "",
    ]
    for key in sorted(checks):
        lines.append(f"- {key}: `{checks[key]}`")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- This evidence is candidate-only.",
            "- This evidence does not create source-of-record.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )
    return "\n".join(lines)


def build_gate_report(precheck: dict[str, Any]) -> dict[str, Any]:
    validate_report(*build_self_test_report(precheck), precheck)
    for case in ["status", "query-error", "missing-topic-query", "bad-boost", "raw-payload", "credential-leak", "forbidden-claim", "missing-marker"]:
        run_negative_test(precheck, case)
    return {
        "id": "agent-reach-p9-hit-rate-output-quality-gate-20260626",
        "date": "2026-06-26",
        "status": "p9_hit_rate_output_quality_gate_ready",
        "current_admission": "limited_candidate_only",
        "planned_query_count": len(planned_queries(precheck)),
        "topics": sorted(TOPICS),
        "live_external_search_invoked": False,
        "validator_checks": {
            "requires_completed_status": True,
            "requires_execution_requested": True,
            "requires_live_external_search_invoked": True,
            "requires_planned_query_count_20": True,
            "requires_four_topic_reports": True,
            "requires_topic_coverage_one": True,
            "requires_zero_query_errors": True,
            "requires_query_candidate_coverage_one_per_topic": True,
            "requires_priority_domain_threshold_pass": True,
            "requires_p9_candidate_schema": True,
            "requires_domain_boost_consistency": True,
            "requires_boosted_score_cap": True,
            "requires_candidate_only_non_claims": True,
            "requires_business_field_mapping": True,
            "blocks_raw_provider_payload_persistence": True,
            "blocks_credential_leak": True,
            "blocks_forbidden_claims": True,
            "requires_markdown_candidate_only_marker": True,
            "requires_markdown_non_claim_marker": True,
            "self_test_passed_without_network": True,
            "negative_status_test_passed": True,
            "negative_query_error_test_passed": True,
            "negative_missing_topic_query_test_passed": True,
            "negative_bad_boost_test_passed": True,
            "negative_raw_payload_test_passed": True,
            "negative_credential_leak_test_passed": True,
            "negative_forbidden_claim_test_passed": True,
            "negative_missing_marker_test_passed": True,
        },
        "non_claims": ["gate_readiness_only", "not_live_search_invoked", "not_kds_canonical_written", "not_gfis_source_of_record_written", "not_accepted", "not_integrated", "not_production_ready"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--validate-report", action="store_true")
    parser.add_argument("--gate-readiness", action="store_true")
    args = parser.parse_args()

    precheck = load_json(PRECHECK)
    if args.gate_readiness:
        report = build_gate_report(precheck)
        write_json(EVIDENCE_JSON, report)
        EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
        print(
            "agent_reach_p9_hit_rate_output_quality_gate=pass "
            f"status={report['status']} planned_query_count={report['planned_query_count']} "
            "self_test=pass live_external_search_invoked=false"
        )
        return

    if args.validate_report or args.report.exists() or args.markdown.exists():
        validate_report(load_json(args.report), read_text(args.markdown), precheck)
        print(f"agent_reach_p9_hit_rate_output_quality_gate=pass report={args.report}")
        return

    report = build_gate_report(precheck)
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_hit_rate_output_quality_gate=pass "
        f"status={report['status']} planned_query_count={report['planned_query_count']} "
        "self_test=pass live_external_search_invoked=false"
    )


if __name__ == "__main__":
    main()
