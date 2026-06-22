#!/usr/bin/env python3
"""Validate Agent-Reach P7 limited live-search dry-run outputs."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
DEFAULT_REPORT = ROOT / "docs/harness/evidence/agent-reach-p7-limited-live-search-dry-run-20260622.json"
DEFAULT_MARKDOWN = ROOT / "docs/harness/evidence/agent-reach-p7-limited-live-search-dry-run-20260622.md"
TOKEN_PATTERN = re.compile(r"(?i)(api[_-]?key|token|secret|authorization|cookie)[=:]\S+")
RAW_PAYLOAD_KEYS = {"raw", "raw_payload", "provider_payload", "response_body", "html", "cookie", "authorization"}
FORBIDDEN_CLAIMS = {"accepted", "integrated", "production_ready"}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p7_limited_live_search_output=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing_report:{path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing_markdown:{path}")
    return path.read_text(encoding="utf-8")


def load_runner_module():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contains_raw_payload(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in RAW_PAYLOAD_KEYS or contains_raw_payload(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_raw_payload(item) for item in value)
    return False


def validate_report(report: dict[str, Any], markdown: str, plan: dict[str, Any], runner_module) -> None:
    if report.get("status") != "limited_live_search_dry_run_completed":
        fail(f"status_not_completed:{report.get('status')}")
    if report.get("current_admission") != "limited_candidate_only":
        fail("current_admission_mismatch")
    if report.get("authorization_valid") is not True:
        fail("authorization_not_valid")
    if report.get("execution_requested") is not True:
        fail("execution_not_requested")

    controls = report.get("security_controls", {})
    if controls.get("live_external_search_invoked") is not True:
        fail("live_external_search_not_invoked")
    for field in [
        "credential_written",
        "browser_cookie_extraction_invoked",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "production_config_write_allowed",
        "global_mcp_config_write_allowed",
        "production_integration_allowed",
    ]:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")

    queries = plan.get("queries", [])
    scope = plan.get("scope", {})
    candidates = report.get("candidates", [])
    if len(queries) < plan["quality_thresholds"]["minimum_query_count"]:
        fail("query_count_below_threshold")
    if len(queries) > scope.get("max_queries", 5):
        fail("query_count_above_scope")
    if len(candidates) > len(queries) * scope.get("max_results_per_query", 10):
        fail("candidate_count_above_scope")
    query_errors = report.get("query_errors", [])
    if query_errors:
        fail(f"query_errors_present:{len(query_errors)}")

    allowed_channels = set(scope.get("allowed_channels", []))
    required_fields = set(runner_module.REQUIRED_CANDIDATE_FIELDS)
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    covered_query_ids: set[str] = set()
    covered_channels: set[str] = set()
    for candidate in candidates:
        missing = sorted(required_fields - set(candidate))
        if missing:
            fail(f"candidate_missing_fields:{candidate.get('candidate_id')}:{','.join(missing)}")
        candidate_id = candidate["candidate_id"]
        if candidate_id in seen_ids:
            fail(f"duplicate_candidate_id:{candidate_id}")
        seen_ids.add(candidate_id)
        if candidate.get("channel") not in allowed_channels:
            fail(f"candidate_channel_out_of_scope:{candidate.get('channel')}")
        covered_channels.add(candidate["channel"])
        covered_query_ids.add(candidate["query_id"])
        if not candidate.get("url"):
            fail(f"candidate_url_missing:{candidate_id}")
        if candidate["url"] in seen_urls:
            fail(f"duplicate_candidate_url:{candidate['url']}")
        seen_urls.add(candidate["url"])
        if not candidate.get("source_domain"):
            fail(f"candidate_source_domain_missing:{candidate_id}")
        if TOKEN_PATTERN.search(json.dumps(candidate, ensure_ascii=False)):
            fail(f"candidate_credential_leak:{candidate_id}")
        claims = set(candidate.get("non_claims", []))
        if FORBIDDEN_CLAIMS & claims:
            fail(f"candidate_forbidden_claim:{candidate_id}")
        for claim in ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"]:
            if claim not in claims:
                fail(f"candidate_non_claim_missing:{candidate_id}:{claim}")

    quality = report.get("quality_report", {})
    thresholds = plan.get("quality_thresholds", {})
    expected_query_ids = {query["query_id"] for query in queries}
    missing_query_ids = sorted(expected_query_ids - covered_query_ids)
    missing_channels = sorted(allowed_channels - covered_channels)
    if missing_channels:
        fail(f"channel_coverage_missing:{','.join(missing_channels)}")
    if quality.get("channel_candidate_coverage") != 1.0:
        fail("channel_candidate_coverage_not_full")
    if quality.get("missing_channels") not in ([], None):
        fail("quality_missing_channels_not_empty")
    if quality.get("duplicate_url_count") not in (0, None):
        fail("quality_duplicate_url_count_not_zero")
    if missing_query_ids:
        fail(f"query_coverage_missing:{','.join(missing_query_ids)}")
    if quality.get("query_candidate_coverage") != 1.0:
        fail("query_candidate_coverage_not_full")
    if quality.get("missing_query_ids") not in ([], None):
        fail("quality_missing_query_ids_not_empty")
    if quality.get("query_error_count") not in (0, None):
        fail("quality_query_error_count_not_zero")
    if quality.get("threshold_pass") is not True:
        fail("quality_threshold_not_passed")
    for field, threshold in [
        ("candidate_count", thresholds["minimum_candidate_count"]),
        ("required_field_coverage", thresholds["minimum_required_field_coverage"]),
        ("average_score", thresholds["minimum_average_score"]),
        ("minimum_traceability_score", thresholds["minimum_traceability_score"]),
    ]:
        if quality.get(field, 0) < threshold:
            fail(f"quality_below_threshold:{field}")
    for field, threshold in [
        ("forbidden_claim_count", thresholds["maximum_forbidden_claim_count"]),
        ("credential_leak_count", thresholds["maximum_credential_leak_count"]),
    ]:
        if quality.get(field, 0) > threshold:
            fail(f"quality_above_threshold:{field}")

    if contains_raw_payload(report):
        fail("raw_provider_payload_persisted")
    for marker in [
        "candidate-only",
        "does not claim accepted, integrated, or production_ready status",
        "Raw provider payloads are not persisted",
    ]:
        if marker not in markdown:
            fail(f"markdown_missing:{marker}")


def build_self_test_report(runner_module) -> tuple[dict[str, Any], str, dict[str, Any]]:
    plan = runner_module.load_json(runner_module.PLAN_PATH)
    candidates = []
    for query in plan["queries"]:
        candidates.extend(
            runner_module.build_candidates(
                query,
                [
                    (
                        f"{query['query']} quality traceability candidate",
                        f"https://example.com/{query['query_id']}-globalcloud-search-quality-traceability",
                        f"{query['query']} quality traceability candidate for {query['project']}.",
                    )
                ],
            )
        )
    report = {
        "id": "agent-reach-p7-limited-live-search-dry-run-runtime",
        "round": "GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001",
        "current_admission": "limited_candidate_only",
        "authorization_valid": True,
        "authorization_reasons": [],
        "execution_requested": True,
        "status": "limited_live_search_dry_run_completed",
        "security_controls": {
            "agent_reach_binary_invoked": False,
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
        "quality_report": runner_module.quality_report(plan, candidates, []),
    }
    return report, runner_module.render_markdown(report), plan


def build_negative_test_report(runner_module, case: str) -> tuple[dict[str, Any], str, dict[str, Any], str]:
    report, markdown, plan = build_self_test_report(runner_module)
    if case == "missing-query":
        missing_id = next(query["query_id"] for query in plan["queries"] if query["channel"] == "web")
        report["candidates"] = [candidate for candidate in report["candidates"] if candidate["query_id"] != missing_id]
        report["quality_report"] = runner_module.quality_report(plan, report["candidates"], [])
        return report, markdown, plan, f"query_coverage_missing:{missing_id}"
    if case == "query-error":
        report["query_errors"] = [
            {
                "query_id": plan["queries"][0]["query_id"],
                "project": plan["queries"][0]["project"],
                "channel": plan["queries"][0]["channel"],
                "error_type": "negative_fixture",
                "message": "Synthetic query error.",
            }
        ]
        report["quality_report"] = runner_module.quality_report(plan, report["candidates"], report["query_errors"])
        return report, markdown, plan, "query_errors_present:1"
    if case == "raw-payload":
        report["raw_payload"] = {"provider": "negative_fixture"}
        return report, markdown, plan, "raw_provider_payload_persisted"
    if case == "duplicate-url":
        report["candidates"][1]["url"] = report["candidates"][0]["url"]
        report["candidates"][1]["source_domain"] = report["candidates"][0]["source_domain"]
        report["quality_report"] = runner_module.quality_report(plan, report["candidates"], [])
        return report, markdown, plan, "duplicate_candidate_url:"
    if case == "missing-channel":
        missing_channel = "bilibili"
        report["candidates"] = [candidate for candidate in report["candidates"] if candidate["channel"] != missing_channel]
        report["quality_report"] = runner_module.quality_report(plan, report["candidates"], [])
        return report, markdown, plan, f"channel_coverage_missing:{missing_channel}"
    raise SystemExit(f"agent_reach_p7_limited_live_search_output=fail reason=unknown_negative_test:{case}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--self-test", action="store_true", help="Validate an in-memory positive fixture without live network reads")
    parser.add_argument(
        "--negative-test",
        choices=["missing-query", "query-error", "raw-payload", "duplicate-url", "missing-channel"],
        help="Run an in-memory negative fixture and pass only if the validator rejects it for the expected reason",
    )
    args = parser.parse_args()

    runner_module = load_runner_module()
    if args.negative_test:
        report, markdown, plan, expected_reason = build_negative_test_report(runner_module, args.negative_test)
        try:
            validate_report(report, markdown, plan, runner_module)
        except SystemExit as exc:
            message = str(exc)
            if expected_reason in message:
                print(f"agent_reach_p7_limited_live_search_output_negative=pass case={args.negative_test} expected_reason={expected_reason}")
                return
            raise
        fail(f"negative_test_unexpected_pass:{args.negative_test}")
    if args.self_test:
        report, markdown, plan = build_self_test_report(runner_module)
    else:
        report = load_json(args.report)
        markdown = read_text(args.markdown)
        plan = runner_module.load_json(runner_module.PLAN_PATH)
    validate_report(report, markdown, plan, runner_module)
    quality = report["quality_report"]
    print(
        "agent_reach_p7_limited_live_search_output=pass "
        f"status={report['status']} "
        f"candidate_count={quality['candidate_count']} "
        f"average_score={quality['average_score']} "
        f"threshold_pass={quality['threshold_pass']}"
    )


if __name__ == "__main__":
    main()
