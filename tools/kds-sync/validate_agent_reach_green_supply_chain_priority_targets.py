#!/usr/bin/env python3
"""Validate Agent-Reach green supply-chain priority search targets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / "fixtures/agent-reach/green-supply-chain-priority-search-targets-20260623.json"
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-green-supply-chain-priority-search-targets-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-green-supply-chain-priority-search-targets-20260623.md"

REQUIRED_TARGET_FIELDS = {
    "target_id",
    "priority",
    "name",
    "domain",
    "url",
    "target_type",
    "recommended_queries",
    "reason",
}
REQUIRED_DOMAINS = {
    "greenscs.com",
    "gmpsp.org.cn",
    "miit.gov.cn",
    "samr.gov.cn",
    "mee.gov.cn",
    "pbc.gov.cn",
    "ghgprotocol.org",
    "commission.europa.eu",
    "meescc.cn",
    "ndrc.gov.cn",
}
REQUIRED_TYPES = {
    "public_platform",
    "government_policy",
    "government_standard",
    "government_environment_policy",
    "green_finance_policy",
    "international_standard",
    "international_due_diligence_policy",
    "government_solid_waste_standard",
    "government_zero_waste_city_policy",
    "technical_center_zero_waste_city",
    "government_industrial_solid_waste_policy",
    "government_circular_economy_policy",
}
REQUIRED_NON_CLAIMS = {
    "candidate_priority_targets_only",
    "not_source_of_record",
    "not_kds_canonical_written",
    "not_gfis_source_of_record_written",
    "not_accepted",
    "not_integrated",
    "not_production_ready",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_green_supply_chain_priority_targets=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_target(target: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_TARGET_FIELDS - set(target))
    if missing:
        fail(f"target_missing_fields:{target.get('target_id')}:{','.join(missing)}")
    if target["priority"] not in {"P0", "P1"}:
        fail(f"target_priority_out_of_scope:{target['target_id']}")
    parsed = urlparse(target["url"])
    if parsed.scheme != "https":
        fail(f"target_url_not_https:{target['target_id']}")
    if target["domain"] not in parsed.netloc:
        fail(f"target_domain_url_mismatch:{target['target_id']}")
    queries = target.get("recommended_queries", [])
    if len(queries) < 2:
        fail(f"target_queries_too_few:{target['target_id']}")
    if not all("site:" in query for query in queries):
        fail(f"target_query_missing_site_filter:{target['target_id']}")


def build_report() -> dict[str, Any]:
    data = load_json(TARGETS)
    plan = load_json(PLAN)
    targets = data.get("priority_search_targets", [])
    if data.get("status") != "candidate_priority_targets_ready":
        fail("status_not_ready")
    if data.get("current_admission") != "limited_candidate_only":
        fail("current_admission_mismatch")
    if len(targets) < 13:
        fail("target_count_below_13")
    for target in targets:
        validate_target(target)
    domains = {target["domain"] for target in targets}
    target_types = {target["target_type"] for target in targets}
    priorities = {target["priority"] for target in targets}
    missing_domains = sorted(REQUIRED_DOMAINS - domains)
    if missing_domains:
        fail(f"required_domains_missing:{','.join(missing_domains)}")
    missing_types = sorted(REQUIRED_TYPES - target_types)
    if missing_types:
        fail(f"required_types_missing:{','.join(missing_types)}")
    if not {"P0", "P1"} <= priorities:
        fail("priority_levels_missing")
    policy = data.get("usage_policy", {})
    for field in [
        "must_not_treat_as_source_of_record",
        "must_not_write_kds_canonical",
        "must_not_write_gfis_source_of_record",
        "must_not_claim_accepted_integrated_or_production_ready",
    ]:
        if policy.get(field) is not True:
            fail(f"usage_policy_not_true:{field}")
    controls = data.get("security_controls", {})
    for field in [
        "live_external_search_invoked_by_this_file",
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
    if not REQUIRED_NON_CLAIMS <= set(data.get("non_claims", [])):
        fail("non_claims_missing")
    refs = plan.get("priority_target_refs", [])
    if not any(ref.get("fixture") == "fixtures/agent-reach/green-supply-chain-priority-search-targets-20260623.json" for ref in refs):
        fail("plan_priority_ref_missing")
    return {
        "id": "agent-reach-green-supply-chain-priority-search-targets-20260623",
        "date": "2026-06-23",
        "status": "green_supply_chain_priority_targets_ready",
        "current_admission": "limited_candidate_only",
        "target_count": len(targets),
        "p0_count": sum(1 for target in targets if target["priority"] == "P0"),
        "p1_count": sum(1 for target in targets if target["priority"] == "P1"),
        "domains": sorted(domains),
        "target_types": sorted(target_types),
        "plan_priority_ref_present": True,
        "security_controls": controls,
        "non_claims": data["non_claims"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-GREEN-SUPPLY-CHAIN-PRIORITY-TARGETS-20260623",
            "title: Agent-Reach 绿色供应链重点搜索对象证据 2026-06-23",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-green-supply-chain-priority-search-targets-20260623.md",
            "source_path: docs/harness/evidence/agent-reach-green-supply-chain-priority-search-targets-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach 绿色供应链重点搜索对象证据 2026-06-23",
            "",
            f"- status: `{report['status']}`",
            f"- current_admission: `{report['current_admission']}`",
            f"- target_count: `{report['target_count']}`",
            f"- p0_count: `{report['p0_count']}`",
            f"- p1_count: `{report['p1_count']}`",
            f"- plan_priority_ref_present: `{report['plan_priority_ref_present']}`",
            "",
            "## 覆盖域名",
            "",
            *[f"- `{domain}`" for domain in report["domains"]],
            "",
            "## 边界",
            "",
            "- 本证据仅定义 candidate priority targets。",
            "- 本证据不将任何网站声明为 source-of-record。",
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
        "agent_reach_green_supply_chain_priority_targets=pass "
        f"status={report['status']} target_count={report['target_count']} "
        f"p0_count={report['p0_count']} p1_count={report['p1_count']} "
        "current_admission=limited_candidate_only"
    )


if __name__ == "__main__":
    main()
