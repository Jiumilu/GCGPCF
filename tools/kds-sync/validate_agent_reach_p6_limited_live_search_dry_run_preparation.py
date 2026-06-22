#!/usr/bin/env python3
"""Validate Agent-Reach P6 limited live-search dry-run preparation artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-preparation-20260622.json"
P5B_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p5b-live-search-precheck-corrected-authorization-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p6-limited-live-search-dry-run-preparation-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p6-limited-live-search-dry-run-preparation-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001.md"

ALLOWED_CHANNELS = {"web", "rss", "bilibili"}
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
SECURITY_FALSE_FIELDS = [
    "agent_reach_binary_invoked",
    "live_external_search_invoked",
    "doctor_health_probe_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p6_limited_live_search_dry_run_preparation=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def main() -> None:
    fixture = load_json(FIXTURE)
    p5b = load_json(P5B_EVIDENCE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    if p5b.get("status") != "live_search_precheck_pass_with_watch":
        fail("p5b_status_mismatch")
    if p5b.get("live_search_authorized_for_next_round_candidate") is not True:
        fail("p5b_next_round_candidate_not_true")
    if fixture.get("mode") != "preparation_only":
        fail("fixture_mode_mismatch")
    if fixture.get("execution_authorization_required_before_live") is not True:
        fail("execution_authorization_not_required")
    if fixture.get("live_external_search_invoked") is not False:
        fail("fixture_live_search_invoked_not_false")
    if fixture.get("agent_reach_binary_invoked") is not False:
        fail("fixture_binary_invoked_not_false")

    scope = fixture.get("scope", {})
    if set(scope.get("allowed_channels", [])) != ALLOWED_CHANNELS:
        fail("allowed_channels_mismatch")
    if scope.get("max_queries") != 5:
        fail("max_queries_mismatch")
    if scope.get("max_results_per_query") != 10:
        fail("max_results_per_query_mismatch")
    queries = fixture.get("queries", [])
    if len(queries) != 5:
        fail("query_count_mismatch")
    query_ids = {item.get("query_id") for item in queries}
    if query_ids != {"q1", "q2", "q3", "q4", "q5"}:
        fail("query_ids_mismatch")
    if any(item.get("channel") not in ALLOWED_CHANNELS for item in queries):
        fail("query_channel_out_of_scope")

    output_contract = fixture.get("output_contract", {})
    if set(output_contract.get("candidate_schema_required_fields", [])) != REQUIRED_CANDIDATE_FIELDS:
        fail("candidate_schema_fields_mismatch")
    thresholds = fixture.get("quality_thresholds", {})
    if thresholds.get("minimum_required_field_coverage") != 1.0:
        fail("field_coverage_threshold_mismatch")
    if thresholds.get("maximum_forbidden_claim_count") != 0:
        fail("forbidden_claim_threshold_mismatch")
    if thresholds.get("maximum_credential_leak_count") != 0:
        fail("credential_leak_threshold_mismatch")
    redaction = fixture.get("logging_redaction", {})
    for field in ["redact_tokens", "redact_cookies", "redact_authorization_headers", "redact_query_personal_data", "persist_redacted_snippets_only"]:
        if redaction.get(field) is not True:
            fail(f"redaction_not_true:{field}")
    if not fixture.get("rollback_plan", {}).get("delete_p7_outputs"):
        fail("rollback_outputs_missing")
    template = fixture.get("p7_execution_authorization_template", {})
    if template.get("required_text") != "授权执行 Agent-Reach P7 Limited Live Search Dry Run":
        fail("p7_authorization_text_mismatch")
    if "allow_agent_reach_binary_invocation" not in template.get("required_fields", []):
        fail("p7_binary_authorization_field_missing")

    if evidence.get("status") != "limited_live_search_dry_run_preparation_ready":
        fail("evidence_status_mismatch")
    if evidence.get("mode") != "preparation_only":
        fail("evidence_mode_mismatch")
    checks = evidence.get("preparation_checks", {})
    if checks.get("query_count") != 5:
        fail("evidence_query_count_mismatch")
    if checks.get("p7_execution_authorization_required") is not True:
        fail("evidence_p7_authorization_not_required")
    controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    if evidence.get("next_round") != "GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001":
        fail("next_round_mismatch")

    for marker in [
        "limited_live_search_dry_run_preparation_ready",
        "P7 执行前必须收到明确",
        "不声明真实搜索已调用",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p6_limited_live_search_dry_run_preparation=pass "
        "status=limited_live_search_dry_run_preparation_ready "
        "mode=preparation_only query_count=5 allowed_channels=web,rss,bilibili "
        "live_external_search_invoked=false "
        "agent_reach_binary_invoked=false "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
