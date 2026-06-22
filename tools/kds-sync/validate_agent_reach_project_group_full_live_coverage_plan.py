#!/usr/bin/env python3
"""Validate Agent-Reach full project-group live-search coverage plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
READINESS = ROOT / "docs/harness/evidence/agent-reach-project-group-search-readiness-audit-20260622.json"
AUTH_REQUEST = ROOT / "docs/harness/evidence/agent-reach-p7-execution-authorization-request-package-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-plan-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-plan-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-PLAN-001.md"

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
FORBIDDEN_ACTIONS = {
    "credential_write",
    "browser_cookie_extraction",
    "kds_canonical_write",
    "gfis_source_of_record_write",
    "production_config_write",
    "global_mcp_config_write",
    "production_integration",
    "accepted_claim",
    "integrated_claim",
    "production_ready_claim",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_project_group_full_live_coverage_plan=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def main() -> None:
    plan = load_json(PLAN)
    readiness = load_json(READINESS)
    auth_request = load_json(AUTH_REQUEST)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    if readiness.get("status") != "search_readiness_verified_pending_p7_authorization":
        fail("readiness_not_pending_p7_authorization")
    if auth_request.get("status") != "p7_execution_authorization_request_package_ready":
        fail("p7_authorization_request_not_ready")
    if plan.get("mode") != "full_coverage_plan_only":
        fail("plan_mode_mismatch")
    if plan.get("live_external_search_invoked") is not False:
        fail("plan_live_search_invoked_not_false")
    if set(plan.get("project_scope", [])) != PROJECTS:
        fail("plan_project_scope_mismatch")
    policy = plan.get("batch_policy", {})
    if policy.get("max_queries_per_batch") != 5:
        fail("max_queries_per_batch_mismatch")
    if policy.get("max_results_per_query") != 10:
        fail("max_results_per_query_mismatch")
    if set(policy.get("allowed_channels", [])) != CHANNELS:
        fail("allowed_channels_mismatch")
    if not FORBIDDEN_ACTIONS.issubset(set(policy.get("forbidden_actions", []))):
        fail("forbidden_actions_missing")
    batches = plan.get("batches", [])
    if len(batches) != 3:
        fail("batch_count_mismatch")
    projects_seen: set[str] = set()
    query_ids: set[str] = set()
    for batch in batches:
        queries = batch.get("queries", [])
        if not 1 <= len(queries) <= 5:
            fail(f"batch_query_count_out_of_range:{batch.get('batch_id')}")
        if not str(batch.get("authorization_required_text", "")).startswith("授权执行 Agent-Reach P8 Project Group Full Live Search Batch"):
            fail(f"batch_authorization_text_missing:{batch.get('batch_id')}")
        for query in queries:
            if query.get("project") not in PROJECTS:
                fail(f"query_project_out_of_scope:{query.get('project')}")
            if query.get("channel") not in CHANNELS:
                fail(f"query_channel_out_of_scope:{query.get('channel')}")
            if not query.get("query"):
                fail(f"query_text_missing:{query.get('query_id')}")
            if query.get("query_id") in query_ids:
                fail(f"duplicate_query_id:{query.get('query_id')}")
            query_ids.add(query.get("query_id"))
            projects_seen.add(query.get("project"))
    if projects_seen != PROJECTS:
        fail("project_coverage_mismatch")
    requirements = plan.get("quality_requirements", {})
    for field in [
        "project_coverage",
        "query_candidate_coverage",
        "channel_candidate_coverage",
        "minimum_required_field_coverage",
        "minimum_traceability_score",
    ]:
        if requirements.get(field) != 1.0:
            fail(f"quality_requirement_not_one:{field}")
    if requirements.get("minimum_average_overall_score") != 0.65:
        fail("minimum_average_overall_score_mismatch")
    if requirements.get("minimum_candidate_overall_score") != 0.5:
        fail("minimum_candidate_overall_score_mismatch")
    for field in ["maximum_duplicate_url_count", "maximum_query_error_count", "maximum_credential_leak_count", "maximum_forbidden_claim_count"]:
        if requirements.get(field) != 0:
            fail(f"quality_requirement_not_zero:{field}")

    if evidence.get("status") != "full_project_group_live_coverage_plan_ready":
        fail("evidence_status_mismatch")
    if evidence.get("completion_claim_allowed") is not False:
        fail("completion_claim_allowed_not_false")
    checks = evidence.get("coverage_checks", {})
    for field in [
        "project_scope_14_covered",
        "batch_count_3",
        "max_queries_per_batch_5",
        "allowed_channels_web_rss_bilibili",
        "quality_requirements_defined",
        "separate_authorization_per_batch_required",
        "no_live_external_search_invoked",
    ]:
        if checks.get(field) is not True:
            fail(f"coverage_check_not_true:{field}")
    for marker in [
        "full_project_group_live_coverage_plan_ready",
        "14/14",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_project_group_full_live_coverage_plan=pass "
        "status=full_project_group_live_coverage_plan_ready "
        "project_coverage=14/14 batch_count=3 max_queries_per_batch=5 "
        "live_external_search_invoked=false "
        "completion_claim_allowed=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
