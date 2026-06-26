#!/usr/bin/env python3
"""Validate Agent-Reach P9 priority target hit-rate precheck assets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-precheck-20260626.json"
TARGETS = ROOT / "fixtures/agent-reach/green-supply-chain-priority-search-targets-20260623.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-precheck-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-precheck-20260626.md"

REQUIRED_TOPICS = {
    "green_supply_chain",
    "phosphogypsum",
    "industrial_solid_waste",
    "zero_waste_city",
}
REQUIRED_BUSINESS_FIELDS = {
    "supplier_esg",
    "green_financing_purpose",
    "solid_waste_disposal_receipt",
    "resource_utilization_product",
    "product_carbon_footprint",
    "scope3_emissions",
    "carbon_traceability",
    "zero_waste_city_indicator",
    "evidence_standard_reference",
}
REQUIRED_SECURITY_FALSE = {
    "live_external_search_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
}
REQUIRED_NON_CLAIMS = {
    "precheck_only",
    "candidate_only",
    "not_live_search_invoked",
    "not_source_of_record",
    "not_kds_canonical_written",
    "not_gfis_source_of_record_written",
    "not_accepted",
    "not_integrated",
    "not_production_ready",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_priority_target_hit_rate_precheck=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_query(topic_id: str, query: dict[str, Any], priority_domains: set[str]) -> None:
    for field in ["query_id", "channel", "query", "expected_priority_domains", "business_fields"]:
        if field not in query:
            fail(f"query_missing_field:{topic_id}:{field}")
    if query["channel"] not in {"web", "rss", "bilibili"}:
        fail(f"query_channel_out_of_scope:{query['query_id']}")
    if "site:" not in query["query"]:
        fail(f"query_missing_site_filter:{query['query_id']}")
    expected_domains = set(query.get("expected_priority_domains", []))
    if not expected_domains:
        fail(f"query_expected_domains_missing:{query['query_id']}")
    if not expected_domains <= priority_domains:
        fail(f"query_expected_domain_not_priority:{query['query_id']}")
    if not query.get("business_fields"):
        fail(f"query_business_fields_missing:{query['query_id']}")


def build_report() -> dict[str, Any]:
    precheck = load_json(PRECHECK)
    targets = load_json(TARGETS)
    if precheck.get("status") != "p9_priority_target_hit_rate_precheck_ready":
        fail("status_not_ready")
    if precheck.get("current_admission") != "limited_candidate_only":
        fail("current_admission_mismatch")
    if precheck.get("mode") != "precheck_only_no_live_search":
        fail("mode_mismatch")
    if precheck.get("requires_live_authorization_before_hit_rate_run") is not True:
        fail("live_authorization_requirement_missing")

    priority_domains_by_level = {
        "P0": {target["domain"] for target in targets.get("priority_search_targets", []) if target.get("priority") == "P0"},
        "P1": {target["domain"] for target in targets.get("priority_search_targets", []) if target.get("priority") == "P1"},
    }
    priority_domains = priority_domains_by_level["P0"] | priority_domains_by_level["P1"]
    topics = precheck.get("topics", [])
    topic_ids = {topic.get("topic_id") for topic in topics}
    if topic_ids != REQUIRED_TOPICS:
        fail(f"topic_set_mismatch:{','.join(sorted(str(item) for item in topic_ids))}")

    all_queries: list[dict[str, Any]] = []
    topic_domain_coverage: dict[str, dict[str, Any]] = {}
    for topic in topics:
        topic_id = topic["topic_id"]
        queries = topic.get("query_expansion", [])
        if len(queries) < 3:
            fail(f"topic_queries_below_3:{topic_id}")
        expected_domains: set[str] = set()
        business_fields: set[str] = set()
        for query in queries:
            validate_query(topic_id, query, priority_domains)
            expected_domains.update(query.get("expected_priority_domains", []))
            business_fields.update(query.get("business_fields", []))
            all_queries.append({**query, "topic_id": topic_id})
        p0_count = len(expected_domains & priority_domains_by_level["P0"])
        total_count = len(expected_domains)
        if p0_count < topic.get("minimum_p0_domain_hits_required", 0):
            fail(f"topic_p0_domain_requirement_not_met:{topic_id}")
        if total_count < topic.get("minimum_total_domain_hits_required", 0):
            fail(f"topic_total_domain_requirement_not_met:{topic_id}")
        topic_domain_coverage[topic_id] = {
            "expected_domain_count": total_count,
            "expected_p0_domain_count": p0_count,
            "business_fields": sorted(business_fields),
        }

    requirements = precheck.get("hit_rate_requirements", {})
    if requirements.get("topic_count") != len(topics):
        fail("topic_count_requirement_mismatch")
    if len(all_queries) < requirements.get("minimum_total_queries", 0):
        fail("total_queries_below_requirement")
    total_expected_domains = {domain for query in all_queries for domain in query["expected_priority_domains"]}
    p0_expected_domains = total_expected_domains & priority_domains_by_level["P0"]
    if len(p0_expected_domains) < requirements.get("minimum_p0_domains_covered", 0):
        fail("p0_domains_below_requirement")
    if len(total_expected_domains) < requirements.get("minimum_total_priority_domains_covered", 0):
        fail("total_priority_domains_below_requirement")

    boost = precheck.get("domain_boost_policy", {})
    if boost.get("mode") != "candidate_scoring_only":
        fail("boost_mode_mismatch")
    if boost.get("p0_domain_boost", 0) <= boost.get("p1_domain_boost", 0):
        fail("p0_boost_not_above_p1")
    if boost.get("maximum_boosted_overall_score", 0) > 1:
        fail("boost_cap_above_1")
    if boost.get("must_preserve_raw_base_score") is not True:
        fail("boost_raw_base_score_not_preserved")
    if boost.get("must_preserve_candidate_only") is not True:
        fail("boost_candidate_only_not_preserved")

    mapping = precheck.get("business_field_mapping", {})
    mapped_fields = {field for fields in mapping.values() for field in fields}
    if not REQUIRED_BUSINESS_FIELDS <= mapped_fields:
        fail("required_business_fields_missing")
    for project in ["GFIS", "WAS", "WAES", "KDS"]:
        if project not in mapping:
            fail(f"business_mapping_project_missing:{project}")

    drift = precheck.get("drift_monitoring", {})
    markdown_path = ROOT / drift.get("full_coverage_markdown", "")
    if not markdown_path.exists():
        fail("drift_markdown_missing")
    markdown = markdown_path.read_text(encoding="utf-8")
    missing_markers = [marker for marker in drift.get("required_markers", []) if marker not in markdown]
    if missing_markers:
        fail(f"drift_markers_missing:{','.join(missing_markers)}")
    if "merge_agent_reach_project_group_full_live_search_batches.py" not in drift.get("repair_command", ""):
        fail("drift_repair_command_missing_merge_runner")

    controls = precheck.get("security_controls", {})
    for field in REQUIRED_SECURITY_FALSE:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    if not REQUIRED_NON_CLAIMS <= set(precheck.get("non_claims", [])):
        fail("non_claims_missing")

    return {
        "id": "agent-reach-p9-priority-target-hit-rate-precheck-20260626",
        "date": "2026-06-26",
        "status": "p9_priority_target_hit_rate_precheck_ready",
        "current_admission": "limited_candidate_only",
        "mode": precheck["mode"],
        "topic_count": len(topics),
        "query_count": len(all_queries),
        "expected_priority_domain_count": len(total_expected_domains),
        "expected_p0_domain_count": len(p0_expected_domains),
        "topic_domain_coverage": topic_domain_coverage,
        "domain_boost_policy": boost,
        "business_field_mapping_projects": sorted(mapping),
        "drift_monitoring_markers_present": True,
        "live_authorization_required_before_hit_rate_run": True,
        "security_controls": controls,
        "non_claims": precheck["non_claims"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-PRIORITY-TARGET-HIT-RATE-PRECHECK-20260626",
            "title: Agent-Reach P9 重点对象命中率预检证据 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-precheck-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-precheck-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9 重点对象命中率预检证据 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- current_admission: `{report['current_admission']}`",
            f"- mode: `{report['mode']}`",
            f"- topic_count: `{report['topic_count']}`",
            f"- query_count: `{report['query_count']}`",
            f"- expected_priority_domain_count: `{report['expected_priority_domain_count']}`",
            f"- expected_p0_domain_count: `{report['expected_p0_domain_count']}`",
            f"- drift_monitoring_markers_present: `{report['drift_monitoring_markers_present']}`",
            f"- live_authorization_required_before_hit_rate_run: `{report['live_authorization_required_before_hit_rate_run']}`",
            "",
            "## 边界",
            "",
            "- 本证据只完成 P9 precheck，不执行真实搜索。",
            "- P9 hit-rate live run 需要单独授权。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_priority_target_hit_rate_precheck=pass "
        f"status={report['status']} topics={report['topic_count']} "
        f"queries={report['query_count']} p0_domains={report['expected_p0_domain_count']} "
        f"priority_domains={report['expected_priority_domain_count']} live_external_search_invoked=false"
    )


if __name__ == "__main__":
    main()
