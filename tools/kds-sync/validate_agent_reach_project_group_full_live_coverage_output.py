#!/usr/bin/env python3
"""Validate Agent-Reach P8 full project-group live-search output quality."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001.md"
DEFAULT_REPORT = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.json"
DEFAULT_MARKDOWN = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.md"

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
}
TOKEN_PATTERN = re.compile(r"(?i)(api[_-]?key|token|secret|authorization|cookie)[=:]\S+")
RAW_PAYLOAD_KEYS = {"raw", "raw_payload", "provider_payload", "response_body", "html", "cookie", "authorization"}
FORBIDDEN_CLAIMS = {"accepted", "integrated", "production_ready"}
SECURITY_FALSE_FIELDS = [
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_project_group_full_live_coverage_output=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def expected_queries(plan: dict[str, Any]) -> list[dict[str, Any]]:
    queries: list[dict[str, Any]] = []
    for batch in plan.get("batches", []):
        for query in batch.get("queries", []):
            queries.append({**query, "batch_id": batch.get("batch_id")})
    return queries


def contains_raw_payload(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in RAW_PAYLOAD_KEYS or contains_raw_payload(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_raw_payload(item) for item in value)
    return False


def compute_quality(plan: dict[str, Any], candidates: list[dict[str, Any]], query_errors: list[dict[str, Any]]) -> dict[str, Any]:
    queries = expected_queries(plan)
    expected_query_ids = {query["query_id"] for query in queries}
    covered_query_ids = {candidate.get("query_id") for candidate in candidates if candidate.get("query_id") in expected_query_ids}
    covered_projects = {candidate.get("project") for candidate in candidates if candidate.get("project") in PROJECTS}
    covered_channels = {candidate.get("channel") for candidate in candidates if candidate.get("channel") in CHANNELS}
    urls = [candidate.get("url") for candidate in candidates if candidate.get("url")]
    field_checks = [REQUIRED_CANDIDATE_FIELDS <= set(candidate) for candidate in candidates]
    overall_scores = [candidate.get("overall_score", 0) for candidate in candidates]
    traceability_scores = [candidate.get("traceability_score", 0) for candidate in candidates]
    return {
        "candidate_count": len(candidates),
        "project_coverage": round(len(covered_projects) / len(PROJECTS), 4),
        "missing_projects": sorted(PROJECTS - covered_projects),
        "query_candidate_coverage": round(len(covered_query_ids) / len(expected_query_ids), 4) if expected_query_ids else 0,
        "missing_query_ids": sorted(expected_query_ids - covered_query_ids),
        "channel_candidate_coverage": round(len(covered_channels) / len(CHANNELS), 4),
        "missing_channels": sorted(CHANNELS - covered_channels),
        "duplicate_url_count": len(urls) - len(set(urls)),
        "query_error_count": len(query_errors),
        "required_field_coverage": round(sum(field_checks) / len(field_checks), 4) if field_checks else 0,
        "average_overall_score": round(sum(overall_scores) / len(overall_scores), 4) if overall_scores else 0,
        "minimum_candidate_overall_score": min(overall_scores) if overall_scores else 0,
        "minimum_traceability_score": min(traceability_scores) if traceability_scores else 0,
        "forbidden_claim_count": sum(
            1
            for candidate in candidates
            for claim in candidate.get("non_claims", [])
            if claim in FORBIDDEN_CLAIMS
        ),
        "credential_leak_count": sum(1 for candidate in candidates if TOKEN_PATTERN.search(json.dumps(candidate, ensure_ascii=False))),
    }


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
    if not parsed.netloc:
        fail(f"candidate_url_host_missing:{candidate_id}")
    host = parsed.hostname or ""
    source_domain = str(candidate.get("source_domain", "")).lower()
    if host.lower() != source_domain:
        fail(f"candidate_source_domain_mismatch:{candidate_id}")


def validate_report(report: dict[str, Any], markdown: str, plan: dict[str, Any]) -> None:
    if report.get("status") != "full_project_group_live_coverage_completed":
        fail(f"status_not_completed:{report.get('status')}")
    if report.get("current_admission") != "limited_candidate_only":
        fail("current_admission_mismatch")
    if report.get("execution_requested") is not True:
        fail("execution_not_requested")
    controls = report.get("security_controls", {})
    if controls.get("live_external_search_invoked") is not True:
        fail("live_external_search_not_invoked")
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")

    plan_policy = plan.get("batch_policy", {})
    max_results = plan_policy.get("max_results_per_query", 10)
    candidates = report.get("candidates", [])
    query_errors = report.get("query_errors", [])
    if query_errors:
        fail(f"query_errors_present:{len(query_errors)}")
    expected = expected_queries(plan)
    expected_query_ids = {query["query_id"] for query in expected}
    expected_by_query = {query["query_id"]: query for query in expected}
    seen_candidate_ids: set[str] = set()
    seen_urls: set[str] = set()
    per_query_counts: dict[str, int] = {}
    for candidate in candidates:
        missing_fields = sorted(REQUIRED_CANDIDATE_FIELDS - set(candidate))
        if missing_fields:
            fail(f"candidate_missing_fields:{candidate.get('candidate_id')}:{','.join(missing_fields)}")
        candidate_id = candidate["candidate_id"]
        if candidate_id in seen_candidate_ids:
            fail(f"duplicate_candidate_id:{candidate_id}")
        seen_candidate_ids.add(candidate_id)
        query_id = candidate["query_id"]
        if query_id not in expected_query_ids:
            fail(f"candidate_query_out_of_scope:{query_id}")
        expected_query = expected_by_query[query_id]
        if candidate["project"] != expected_query["project"]:
            fail(f"candidate_project_mismatch:{candidate_id}")
        if candidate["channel"] != expected_query["channel"]:
            fail(f"candidate_channel_mismatch:{candidate_id}")
        per_query_counts[query_id] = per_query_counts.get(query_id, 0) + 1
        if per_query_counts[query_id] > max_results:
            fail(f"query_result_count_above_scope:{query_id}")
        if candidate["project"] not in PROJECTS:
            fail(f"candidate_project_out_of_scope:{candidate['project']}")
        if candidate["channel"] not in CHANNELS:
            fail(f"candidate_channel_out_of_scope:{candidate['channel']}")
        url = candidate["url"]
        if not url:
            fail(f"candidate_url_missing:{candidate_id}")
        if url in seen_urls:
            fail(f"duplicate_candidate_url:{url}")
        seen_urls.add(url)
        if not candidate.get("source_domain"):
            fail(f"candidate_source_domain_missing:{candidate_id}")
        validate_url(candidate)
        parse_retrieved_at(str(candidate["retrieved_at"]), candidate_id)
        if not str(candidate.get("snippet_redacted", "")).strip():
            fail(f"candidate_snippet_redacted_empty:{candidate_id}")
        if TOKEN_PATTERN.search(json.dumps(candidate, ensure_ascii=False)):
            fail(f"candidate_credential_leak:{candidate_id}")
        claims = set(candidate.get("non_claims", []))
        if FORBIDDEN_CLAIMS & claims:
            fail(f"candidate_forbidden_claim:{candidate_id}")
        for claim in ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"]:
            if claim not in claims:
                fail(f"candidate_non_claim_missing:{candidate_id}:{claim}")
        for score_field in [
            "relevance_score",
            "authority_score",
            "freshness_score",
            "traceability_score",
            "overall_score",
        ]:
            score = candidate.get(score_field)
            if not isinstance(score, (int, float)) or not 0 <= score <= 1:
                fail(f"candidate_score_out_of_range:{candidate_id}:{score_field}")

    computed = compute_quality(plan, candidates, query_errors)
    quality = report.get("quality_report", {})
    requirements = plan.get("quality_requirements", {})
    if computed["missing_projects"]:
        fail(f"project_coverage_missing:{','.join(computed['missing_projects'])}")
    if computed["missing_query_ids"]:
        fail(f"query_coverage_missing:{','.join(computed['missing_query_ids'])}")
    if computed["missing_channels"]:
        fail(f"channel_coverage_missing:{','.join(computed['missing_channels'])}")
    for field in ["project_coverage", "query_candidate_coverage", "channel_candidate_coverage", "required_field_coverage"]:
        required = requirements.get("minimum_required_field_coverage") if field == "required_field_coverage" else requirements.get(field)
        if computed[field] < required:
            fail(f"quality_below_requirement:{field}")
        if quality.get(field) != computed[field]:
            fail(f"quality_report_mismatch:{field}")
    for field, requirement_name in [
        ("average_overall_score", "minimum_average_overall_score"),
        ("minimum_candidate_overall_score", "minimum_candidate_overall_score"),
        ("minimum_traceability_score", "minimum_traceability_score"),
    ]:
        if computed[field] < requirements.get(requirement_name, 0):
            fail(f"quality_below_requirement:{field}")
        if quality.get(field) != computed[field]:
            fail(f"quality_report_mismatch:{field}")
    for field, limit_name in [
        ("duplicate_url_count", "maximum_duplicate_url_count"),
        ("query_error_count", "maximum_query_error_count"),
        ("credential_leak_count", "maximum_credential_leak_count"),
        ("forbidden_claim_count", "maximum_forbidden_claim_count"),
    ]:
        if computed[field] > requirements.get(limit_name, 0):
            fail(f"quality_above_requirement:{field}")
        if quality.get(field) != computed[field]:
            fail(f"quality_report_mismatch:{field}")
    if quality.get("threshold_pass") is not True:
        fail("quality_threshold_not_passed")
    if contains_raw_payload(report):
        fail("raw_provider_payload_persisted")
    for marker in [
        "candidate-only",
        "does not claim accepted, integrated, or production_ready status",
        "Raw provider payloads are not persisted",
    ]:
        if marker not in markdown:
            fail(f"markdown_missing:{marker}")


def build_self_test_report(plan: dict[str, Any]) -> tuple[dict[str, Any], str]:
    candidates: list[dict[str, Any]] = []
    for query in expected_queries(plan):
        candidates.append(
            {
                "candidate_id": f"{query['query_id']}-c1",
                "query_id": query["query_id"],
                "project": query["project"],
                "channel": query["channel"],
                "title": f"{query['project']} controlled public candidate",
                "url": f"https://example.com/agent-reach/{query['query_id']}",
                "source_domain": "example.com",
                "retrieved_at": "2026-06-22T00:00:00+00:00",
                "snippet_redacted": f"{query['project']} public candidate for full coverage quality validation.",
                "relevance_score": 0.9,
                "authority_score": 0.8,
                "freshness_score": 0.7,
                "traceability_score": 1.0,
                "overall_score": 0.86,
                "non_claims": ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"],
            }
        )
    quality = compute_quality(plan, candidates, [])
    quality["threshold_pass"] = True
    report = {
        "id": "agent-reach-project-group-full-live-coverage-runtime",
        "round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-001",
        "status": "full_project_group_live_coverage_completed",
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
        "query_errors": [],
        "quality_report": quality,
    }
    markdown = "\n".join(
        [
            "# Agent-Reach P8 Full Coverage Runtime",
            "",
            "This evidence is candidate-only.",
            "This evidence does not claim accepted, integrated, or production_ready status.",
            "Raw provider payloads are not persisted.",
        ]
    )
    return report, markdown


def build_negative_test_report(plan: dict[str, Any], case: str) -> tuple[dict[str, Any], str, str]:
    report, markdown = build_self_test_report(plan)
    if case == "missing-project":
        report["candidates"] = [candidate for candidate in report["candidates"] if candidate["project"] != "WAS"]
        report["quality_report"] = {**compute_quality(plan, report["candidates"], []), "threshold_pass": False}
        return report, markdown, "project_coverage_missing:WAS"
    if case == "duplicate-url":
        report["candidates"][1]["url"] = report["candidates"][0]["url"]
        report["quality_report"] = {**compute_quality(plan, report["candidates"], []), "threshold_pass": False}
        return report, markdown, "duplicate_candidate_url:"
    if case == "query-error":
        report["query_errors"] = [{"query_id": "p8-q01", "error_type": "negative_fixture"}]
        report["quality_report"] = {**compute_quality(plan, report["candidates"], report["query_errors"]), "threshold_pass": False}
        return report, markdown, "query_errors_present:1"
    if case == "raw-payload":
        report["raw_payload"] = {"html": "<html>negative fixture</html>"}
        return report, markdown, "raw_provider_payload_persisted"
    if case == "credential-leak":
        report["candidates"][0]["snippet_redacted"] = "token=abc123"
        report["quality_report"] = {**compute_quality(plan, report["candidates"], []), "threshold_pass": False}
        return report, markdown, "candidate_credential_leak:"
    if case == "forbidden-claim":
        report["candidates"][0]["non_claims"].append("accepted")
        report["quality_report"] = {**compute_quality(plan, report["candidates"], []), "threshold_pass": False}
        return report, markdown, "candidate_forbidden_claim:"
    if case == "missing-channel":
        for candidate in report["candidates"]:
            if candidate["channel"] == "bilibili":
                candidate["channel"] = "web"
        report["quality_report"] = {**compute_quality(plan, report["candidates"], []), "threshold_pass": False}
        return report, markdown, "candidate_channel_mismatch:"
    if case == "low-score":
        report["candidates"][0]["overall_score"] = 0.1
        report["quality_report"] = {**compute_quality(plan, report["candidates"], []), "threshold_pass": False}
        return report, markdown, "quality_below_requirement:minimum_candidate_overall_score"
    if case == "bad-url-scheme":
        report["candidates"][0]["url"] = "ftp://example.com/not-allowed"
        return report, markdown, "candidate_url_scheme_invalid:"
    if case == "domain-mismatch":
        report["candidates"][0]["source_domain"] = "other.example"
        return report, markdown, "candidate_source_domain_mismatch:"
    if case == "bad-retrieved-at":
        report["candidates"][0]["retrieved_at"] = "2026-06-22 00:00:00"
        return report, markdown, "candidate_retrieved_at_missing_timezone:"
    fail(f"unknown_negative_test:{case}")


def validate_gate_evidence() -> None:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    if evidence.get("status") != "full_project_group_live_coverage_output_quality_gate_ready":
        fail("evidence_status_mismatch")
    if evidence.get("live_external_search_invoked") is not False:
        fail("evidence_live_search_invoked_not_false")
    checks = evidence.get("validator_checks", {})
    for field in [
        "requires_completed_status",
        "requires_execution_requested",
        "requires_live_external_search_invoked",
        "requires_14_project_coverage",
        "requires_full_query_candidate_coverage",
        "requires_full_channel_candidate_coverage",
        "requires_zero_query_errors",
        "requires_zero_duplicate_urls",
        "requires_candidate_schema",
        "requires_candidate_score_ranges",
        "requires_minimum_average_overall_score",
        "requires_minimum_candidate_overall_score",
        "requires_minimum_traceability_score",
        "requires_result_count_within_scope",
        "blocks_raw_provider_payload_persistence",
        "blocks_credential_leak",
        "blocks_forbidden_claims",
        "self_test_passed_without_network",
        "negative_missing_project_test_passed",
        "negative_duplicate_url_test_passed",
        "negative_query_error_test_passed",
        "negative_raw_payload_test_passed",
        "negative_credential_leak_test_passed",
        "negative_forbidden_claim_test_passed",
        "negative_missing_channel_test_passed",
        "negative_low_score_test_passed",
        "requires_http_or_https_url",
        "requires_source_domain_url_host_match",
        "requires_retrieved_at_iso8601_timezone",
        "requires_non_empty_redacted_snippet",
        "negative_bad_url_scheme_test_passed",
        "negative_domain_mismatch_test_passed",
        "negative_bad_retrieved_at_test_passed",
    ]:
        if checks.get(field) is not True:
            fail(f"validator_check_not_true:{field}")
    for marker in [
        "full_project_group_live_coverage_output_quality_gate_ready",
        "14 项目",
        "project_coverage",
        "query_candidate_coverage",
        "channel_candidate_coverage",
        "duplicate_url_count",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")


def run_self_test(plan: dict[str, Any]) -> None:
    report, markdown = build_self_test_report(plan)
    validate_report(report, markdown, plan)


def run_negative_test(plan: dict[str, Any], case: str) -> None:
    report, markdown, expected_reason = build_negative_test_report(plan, case)
    try:
        validate_report(report, markdown, plan)
    except SystemExit as exc:
        if expected_reason in str(exc):
            print(f"agent_reach_project_group_full_live_coverage_output_negative=pass case={case} expected_reason={expected_reason}")
            return
        raise
    fail(f"negative_test_unexpected_pass:{case}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--negative-test",
        choices=[
            "missing-project",
            "duplicate-url",
            "query-error",
            "raw-payload",
            "credential-leak",
            "forbidden-claim",
            "missing-channel",
            "low-score",
            "bad-url-scheme",
            "domain-mismatch",
            "bad-retrieved-at",
        ],
    )
    args = parser.parse_args()
    plan = load_json(PLAN)
    if args.negative_test:
        run_negative_test(plan, args.negative_test)
        return
    if args.self_test:
        run_self_test(plan)
        print("agent_reach_project_group_full_live_coverage_output=pass status=self_test candidate_count=14 project_coverage=1.0")
        return
    if args.report.exists() or args.markdown.exists():
        validate_report(load_json(args.report), read_text(args.markdown), plan)
        print(f"agent_reach_project_group_full_live_coverage_output=pass report={args.report}")
        return
    run_self_test(plan)
    for case in [
        "missing-project",
        "duplicate-url",
        "query-error",
        "raw-payload",
        "credential-leak",
        "forbidden-claim",
        "missing-channel",
        "low-score",
        "bad-url-scheme",
        "domain-mismatch",
        "bad-retrieved-at",
    ]:
        run_negative_test(plan, case)
    validate_gate_evidence()
    print(
        "agent_reach_project_group_full_live_coverage_output=pass "
        "status=full_project_group_live_coverage_output_quality_gate_ready "
        "self_test=pass live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
