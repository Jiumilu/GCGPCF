#!/usr/bin/env python3
"""Validate Agent-Reach P9S source-direct hit-rate output quality."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json"
DEFAULT_REPORT = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.json"
DEFAULT_MARKDOWN = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-output-quality-gate-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-output-quality-gate-20260626.md"

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
    "target_id",
    "source_domain",
    "priority",
    "topics",
    "business_fields",
    "entrypoint_method",
    "discovery_rank",
    "requested_url",
    "url",
    "final_url",
    "content_type",
    "retry_count",
    "http_status",
    "retrieved_at",
    "title",
    "snippet_redacted",
    "topic_keyword_hits",
    "relevance_score",
    "authority_score",
    "freshness_score",
    "traceability_score",
    "overall_score",
    "non_claims",
    "candidate_only",
}
RAW_PAYLOAD_KEYS = {"raw", "raw_payload", "provider_payload", "response_body", "html", "cookie", "authorization"}
TOKEN_PATTERN = re.compile(r"(?i)(api[_-]?key|token|secret|authorization|cookie)[=:]\S+")
FORBIDDEN_CLAIMS = {"accepted", "integrated", "production_ready"}
ALLOWED_CONTENT_TYPE_PREFIXES = (
    "text/html",
    "text/plain",
    "text/xml",
    "application/xml",
    "application/rss+xml",
    "application/atom+xml",
    "application/json",
)


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_output_quality_gate=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def targets_by_id(precheck: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {target["target_id"]: target for target in precheck.get("source_direct_targets", [])}


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


def validate_url(candidate: dict[str, Any], target: dict[str, Any]) -> None:
    candidate_id = candidate["candidate_id"]
    parsed = urlparse(candidate["url"])
    if parsed.scheme != "https":
        fail(f"candidate_url_scheme_invalid:{candidate_id}")
    if not parsed.hostname:
        fail(f"candidate_url_host_missing:{candidate_id}")
    if not parsed.hostname.endswith(target["domain"]):
        fail(f"candidate_url_domain_mismatch:{candidate_id}")
    if candidate["source_domain"] != target["domain"]:
        fail(f"candidate_source_domain_mismatch:{candidate_id}")
    requested = urlparse(candidate["requested_url"])
    final = urlparse(candidate["final_url"])
    if requested.scheme != "https" or not requested.hostname or not requested.hostname.endswith(target["domain"]):
        fail(f"candidate_requested_url_domain_mismatch:{candidate_id}")
    if final.scheme != "https" or not final.hostname or not final.hostname.endswith(target["domain"]):
        fail(f"candidate_final_url_domain_mismatch:{candidate_id}")
    if candidate["url"] != candidate["final_url"]:
        fail(f"candidate_url_final_url_mismatch:{candidate_id}")


def compute_hit_rate(precheck: dict[str, Any], candidates: list[dict[str, Any]], fetch_errors: list[dict[str, Any]]) -> dict[str, Any]:
    topic_reports: dict[str, Any] = {}
    critical_errors = [error for error in fetch_errors if error.get("critical") is not False]
    for topic_id in sorted(TOPICS):
        topic_targets = [target for target in precheck["source_direct_targets"] if topic_id in target["topics"]]
        topic_candidates = [candidate for candidate in candidates if topic_id in candidate.get("topics", [])]
        p0_hits = {candidate["source_domain"] for candidate in topic_candidates if candidate["priority"] == "P0"}
        total_hits = {candidate["source_domain"] for candidate in topic_candidates}
        keyword_hit_candidates = {
            candidate["target_id"]
            for candidate in topic_candidates
            if candidate.get("topic_keyword_hits", {}).get(topic_id)
        }
        topic_reports[topic_id] = {
            "target_count": len(topic_targets),
            "candidate_count": len(topic_candidates),
            "p0_domain_hit_count": len(p0_hits),
            "total_domain_hit_count": len(total_hits),
            "keyword_hit_candidate_count": len(keyword_hit_candidates),
            "target_coverage": round(len({candidate["target_id"] for candidate in topic_candidates}) / len(topic_targets), 4) if topic_targets else 0,
            "threshold_pass": bool(p0_hits) and bool(total_hits) and bool(keyword_hit_candidates),
        }
    return {
        "candidate_count": len(candidates),
        "fetch_error_count": len(fetch_errors),
        "critical_fetch_error_count": len(critical_errors),
        "noncritical_fetch_error_count": len(fetch_errors) - len(critical_errors),
        "target_availability_warning_count": len(critical_errors),
        "topic_reports": topic_reports,
        "topic_coverage": round(sum(1 for item in topic_reports.values() if item["threshold_pass"]) / len(topic_reports), 4),
        "threshold_pass": bool(topic_reports) and all(item["threshold_pass"] for item in topic_reports.values()),
    }


def validate_report(report: dict[str, Any], markdown: str, precheck: dict[str, Any]) -> None:
    if report.get("status") != "p9_source_direct_hit_rate_completed":
        fail(f"status_not_completed:{report.get('status')}")
    if report.get("current_admission") != "limited_candidate_only":
        fail("current_admission_mismatch")
    if report.get("authorization_valid") is not True:
        fail("authorization_not_valid")
    if report.get("execution_requested") is not True:
        fail("execution_not_requested")
    if report.get("planned_target_count") != len(precheck.get("source_direct_targets", [])):
        fail("planned_target_count_mismatch")
    controls = report.get("security_controls", {})
    if controls.get("live_external_fetch_invoked") is not True:
        fail("live_external_fetch_not_invoked")
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    if contains_raw_payload(report):
        fail("raw_payload_persisted")

    expected_targets = targets_by_id(precheck)
    seen_candidate_ids: set[str] = set()
    for candidate in report.get("candidates", []):
        missing = sorted(REQUIRED_CANDIDATE_FIELDS - set(candidate))
        if missing:
            fail(f"candidate_missing_fields:{candidate.get('candidate_id')}:{','.join(missing)}")
        candidate_id = candidate["candidate_id"]
        if candidate_id in seen_candidate_ids:
            fail(f"duplicate_candidate_id:{candidate_id}")
        seen_candidate_ids.add(candidate_id)
        target = expected_targets.get(candidate["target_id"])
        if target is None:
            fail(f"candidate_target_out_of_scope:{candidate_id}")
        if candidate["priority"] != target["priority"]:
            fail(f"candidate_priority_mismatch:{candidate_id}")
        if set(candidate["topics"]) != set(target["topics"]):
            fail(f"candidate_topics_mismatch:{candidate_id}")
        if not set(target["business_fields"]) <= set(candidate["business_fields"]):
            fail(f"candidate_business_fields_missing:{candidate_id}")
        validate_url(candidate, target)
        parse_retrieved_at(str(candidate["retrieved_at"]), candidate_id)
        if not str(candidate["snippet_redacted"]).strip():
            fail(f"candidate_snippet_redacted_empty:{candidate_id}")
        if TOKEN_PATTERN.search(json.dumps(candidate, ensure_ascii=False)):
            fail(f"candidate_credential_leak:{candidate_id}")
        if candidate["candidate_only"] is not True:
            fail(f"candidate_only_not_true:{candidate_id}")
        if FORBIDDEN_CLAIMS & set(candidate["non_claims"]):
            fail(f"candidate_forbidden_claim:{candidate_id}")
        for claim in ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"]:
            if claim not in set(candidate["non_claims"]):
                fail(f"candidate_non_claim_missing:{candidate_id}:{claim}")
        for field in ["relevance_score", "authority_score", "freshness_score", "traceability_score", "overall_score"]:
            score = candidate[field]
            if not isinstance(score, (int, float)) or not 0 <= score <= 1:
                fail(f"candidate_score_out_of_range:{candidate_id}:{field}")
        if not isinstance(candidate["discovery_rank"], int) or candidate["discovery_rank"] < 0 or candidate["discovery_rank"] > 4:
            fail(f"candidate_discovery_rank_invalid:{candidate_id}")
        if not any(str(candidate["content_type"]).lower().startswith(prefix) for prefix in ALLOWED_CONTENT_TYPE_PREFIXES):
            fail(f"candidate_content_type_not_allowed:{candidate_id}")
        if not isinstance(candidate["retry_count"], int) or candidate["retry_count"] < 0 or candidate["retry_count"] > 1:
            fail(f"candidate_retry_count_invalid:{candidate_id}")

    computed = compute_hit_rate(precheck, report.get("candidates", []), report.get("fetch_errors", []))
    if computed != report.get("hit_rate_report"):
        fail("hit_rate_report_mismatch")
    if computed["topic_coverage"] != 1.0 or computed["threshold_pass"] is not True:
        fail("hit_rate_threshold_not_passed")
    if set(computed["topic_reports"]) != TOPICS:
        fail("topic_set_mismatch")
    for topic_id, topic_report in computed["topic_reports"].items():
        if topic_report["p0_domain_hit_count"] < 1:
            fail(f"topic_p0_hit_missing:{topic_id}")
        if topic_report["keyword_hit_candidate_count"] < 1:
            fail(f"topic_keyword_hit_missing:{topic_id}")
    for marker in ["candidate-only", "does not create source-of-record", "does not claim accepted, integrated, or production_ready status"]:
        if marker not in markdown:
            fail(f"markdown_missing:{marker}")


def build_self_test_report(precheck: dict[str, Any]) -> tuple[dict[str, Any], str]:
    topic_seen: set[str] = set()
    candidates: list[dict[str, Any]] = []
    for target in precheck["source_direct_targets"]:
        selected_topics = [topic for topic in target["topics"] if topic not in topic_seen] or target["topics"][:1]
        topic_seen.update(selected_topics)
        candidates.append(
            {
                "candidate_id": f"p9s-fixture-{target['target_id']}",
                "target_id": target["target_id"],
                "source_domain": target["domain"],
                "priority": target["priority"],
                "topics": target["topics"],
                "business_fields": target["business_fields"],
                "entrypoint_method": target["entrypoints"][0]["method"],
                "discovery_rank": 0,
                "requested_url": target["entrypoints"][0]["url"],
                "url": target["entrypoints"][0]["url"],
                "final_url": target["entrypoints"][0]["url"],
                "content_type": "text/html",
                "retry_count": 0,
                "http_status": 200,
                "retrieved_at": "2026-06-26T00:00:00+00:00",
                "title": "Agent-Reach P9S fixture",
                "snippet_redacted": "绿色供应链 磷石膏 工业固废 无废城市 综合利用 指标体系 candidate-only fixture.",
                "topic_keyword_hits": {topic: ["fixture"] for topic in target["topics"]},
                "relevance_score": 0.86,
                "authority_score": 0.92 if target["priority"] == "P0" else 0.82,
                "freshness_score": 0.7,
                "traceability_score": 1.0,
                "overall_score": 0.88,
                "non_claims": ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"],
                "candidate_only": True,
            }
        )
    report = {
        "id": "agent-reach-p9-source-direct-hit-rate-live-run-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_hit_rate_completed",
        "current_admission": "limited_candidate_only",
        "authorization_valid": True,
        "authorization_reasons": [],
        "authorization_path": "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json",
        "execution_requested": True,
        "planned_target_count": len(precheck["source_direct_targets"]),
        "planned_entrypoint_count": len(precheck["source_direct_targets"]),
        "security_controls": {
            "live_external_fetch_invoked": True,
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
        "fetch_errors": [],
    }
    report["hit_rate_report"] = compute_hit_rate(precheck, candidates, [])
    markdown = "\n".join(
        [
            "# Agent-Reach P9S Source Direct Hit Rate",
            "This evidence is candidate-only.",
            "This evidence does not create source-of-record.",
            "This evidence does not claim accepted, integrated, or production_ready status.",
        ]
    )
    return report, markdown


def build_negative_test_report(precheck: dict[str, Any], case: str) -> tuple[dict[str, Any], str, str]:
    report, markdown = build_self_test_report(precheck)
    if case == "status":
        report["status"] = "p9_source_direct_hit_rate_rework_required"
        return report, markdown, "status_not_completed"
    if case == "fetch-error":
        report["fetch_errors"] = [{"target_id": "fixture", "discovery_rank": 0, "critical": True, "error_type": "negative_fixture"}]
        report["hit_rate_report"] = compute_hit_rate(precheck, report["candidates"], report["fetch_errors"])
        return report, markdown, "negative_test_unexpected_pass"
    if case == "noncritical-fetch-error":
        report["fetch_errors"] = [{"target_id": "fixture", "discovery_rank": 1, "critical": False, "error_type": "negative_fixture"}]
        report["hit_rate_report"] = compute_hit_rate(precheck, report["candidates"], report["fetch_errors"])
        return report, markdown, "negative_test_unexpected_pass"
    if case == "missing-topic-hit":
        report["candidates"] = [candidate for candidate in report["candidates"] if "zero_waste_city" not in candidate["topics"]]
        report["hit_rate_report"] = compute_hit_rate(precheck, report["candidates"], [])
        return report, markdown, "hit_rate_threshold_not_passed"
    if case == "credential-leak":
        report["candidates"][0]["snippet_redacted"] = "token=abc123"
        return report, markdown, "candidate_credential_leak"
    if case == "raw-payload":
        report["raw_payload"] = {"html": "<html>negative fixture</html>"}
        return report, markdown, "raw_payload_persisted"
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


def build_gate_report(precheck: dict[str, Any]) -> dict[str, Any]:
    validate_report(*build_self_test_report(precheck), precheck)
    for case in ["status", "missing-topic-hit", "credential-leak", "raw-payload", "forbidden-claim", "missing-marker"]:
        run_negative_test(precheck, case)
    validate_report(*build_negative_test_report(precheck, "fetch-error")[:2], precheck)
    validate_report(*build_negative_test_report(precheck, "noncritical-fetch-error")[:2], precheck)
    return {
        "id": "agent-reach-p9-source-direct-output-quality-gate-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_output_quality_gate_ready",
        "current_admission": "limited_candidate_only",
        "planned_target_count": len(precheck["source_direct_targets"]),
        "topics": sorted(TOPICS),
        "live_external_fetch_invoked": False,
        "validator_checks": {
            "requires_completed_status": True,
            "requires_authorization_valid": True,
            "requires_execution_requested": True,
            "requires_live_external_fetch_invoked": True,
            "requires_four_topic_reports": True,
            "requires_topic_coverage_one": True,
            "allows_critical_target_availability_warnings_when_topic_threshold_passes": True,
            "allows_noncritical_discovery_fetch_errors_when_threshold_passes": True,
            "requires_p0_hit_per_topic": True,
            "requires_keyword_hit_per_topic": True,
            "requires_source_direct_candidate_schema": True,
            "requires_discovery_rank": True,
            "requires_requested_and_final_url": True,
            "requires_allowed_content_type": True,
            "requires_retry_count": True,
            "requires_business_field_mapping": True,
            "requires_candidate_only_non_claims": True,
            "blocks_raw_payload_persistence": True,
            "blocks_credential_leak": True,
            "blocks_forbidden_claims": True,
            "requires_markdown_candidate_only_marker": True,
            "requires_markdown_non_claim_marker": True,
            "self_test_passed_without_network": True,
        },
        "non_claims": ["gate_readiness_only", "not_live_fetch_invoked", "not_kds_canonical_written", "not_gfis_source_of_record_written", "not_accepted", "not_integrated", "not_production_ready"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    checks = report["validator_checks"]
    lines = [
        "---",
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-OUTPUT-QUALITY-GATE-20260626",
        "title: Agent-Reach P9S Source Direct 输出质量门禁 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-output-quality-gate-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-output-quality-gate-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct 输出质量门禁 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- planned_target_count: `{report['planned_target_count']}`",
        f"- topics: `{', '.join(report['topics'])}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        "",
        "## 校验范围",
        "",
        "- 要求 P9S live 输出状态为 `p9_source_direct_hit_rate_completed`。",
        "- 要求绿色供应链、磷石膏、工业固废、无废城市 4 个主题全部达到 P0 命中和关键词命中。",
        "- critical fetch error 作为 target availability warning 保留，不抹除目标可用性风险。",
        "- 校验 source scoring、GFIS/WAS/WAES/KDS 业务字段映射和 candidate-only non-claim。",
        "- 阻断 raw payload、credential/cookie 泄漏、accepted / integrated / production_ready 声明。",
        "- 本门禁不执行真实目标站读取，只校验已有输出或离线自测 fixture。",
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
            "agent_reach_p9_source_direct_output_quality_gate=pass "
            f"status={report['status']} planned_target_count={report['planned_target_count']} "
            "self_test=pass live_external_fetch_invoked=false"
        )
        return
    if args.validate_report or args.report.exists() or args.markdown.exists():
        validate_report(load_json(args.report), read_text(args.markdown), precheck)
        print(f"agent_reach_p9_source_direct_output_quality_gate=pass report={args.report}")
        return
    report = build_gate_report(precheck)
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_output_quality_gate=pass "
        f"status={report['status']} planned_target_count={report['planned_target_count']} "
        "self_test=pass live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
