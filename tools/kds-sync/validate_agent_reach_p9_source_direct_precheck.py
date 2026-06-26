#!/usr/bin/env python3
"""Validate Agent-Reach P9S source-direct hit-rate precheck."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-precheck-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-precheck-20260626.md"

REQUIRED_TOPICS = {"green_supply_chain", "phosphogypsum", "industrial_solid_waste", "zero_waste_city"}
ALLOWED_METHODS = {"target_url", "sitemap", "rss", "public_list_page", "site_search_endpoint_without_credentials"}
REQUIRED_FALSE_CONTROLS = {
    "live_external_fetch_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_precheck=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_entrypoint(target: dict[str, Any], entrypoint: dict[str, Any]) -> None:
    method = entrypoint.get("method")
    if method not in ALLOWED_METHODS:
        fail(f"entrypoint_method_not_allowed:{target.get('target_id')}:{method}")
    url = entrypoint.get("url", "")
    parsed = urlparse(url)
    if parsed.scheme != "https":
        fail(f"entrypoint_not_https:{target.get('target_id')}")
    if not parsed.netloc.endswith(target["domain"]):
        fail(f"entrypoint_domain_mismatch:{target.get('target_id')}:{parsed.netloc}")


def build_report() -> dict[str, Any]:
    precheck = load_json(PRECHECK)
    if precheck.get("status") != "p9_source_direct_hit_rate_precheck_ready":
        fail("status_mismatch")
    if precheck.get("mode") != "source_direct_precheck_only_no_live_fetch":
        fail("mode_mismatch")
    prior = load_json(ROOT / precheck["prior_rework_evidence"])
    if prior.get("status") != "p9_priority_target_hit_rate_rework_required":
        fail("prior_rework_status_mismatch")
    targets = precheck.get("source_direct_targets", [])
    requirements = precheck.get("coverage_requirements", {})
    if len(targets) != requirements.get("target_count"):
        fail("target_count_mismatch")
    topics: set[str] = set()
    domains: set[str] = set()
    p0_domains: set[str] = set()
    target_ids: set[str] = set()
    for target in targets:
        for field in ["target_id", "domain", "priority", "topics", "entrypoints", "business_fields"]:
            if field not in target:
                fail(f"target_missing_field:{field}")
        if target["target_id"] in target_ids:
            fail(f"duplicate_target_id:{target['target_id']}")
        target_ids.add(target["target_id"])
        if target["priority"] not in {"P0", "P1"}:
            fail(f"target_priority_invalid:{target['target_id']}")
        if not set(target["topics"]) <= REQUIRED_TOPICS:
            fail(f"target_topic_out_of_scope:{target['target_id']}")
        if not target["entrypoints"]:
            fail(f"target_entrypoints_missing:{target['target_id']}")
        for entrypoint in target["entrypoints"]:
            validate_entrypoint(target, entrypoint)
        if not target["business_fields"]:
            fail(f"target_business_fields_missing:{target['target_id']}")
        topics.update(target["topics"])
        domains.add(target["domain"])
        if target["priority"] == "P0":
            p0_domains.add(target["domain"])
    if topics != REQUIRED_TOPICS:
        fail("topic_coverage_mismatch")
    if len(p0_domains) < requirements.get("minimum_p0_domain_count", 0):
        fail("p0_domain_count_below_requirement")
    if len(domains) < requirements.get("minimum_total_domain_count", 0):
        fail("domain_count_below_requirement")
    for field in REQUIRED_FALSE_CONTROLS:
        if precheck.get("security_controls", {}).get(field) is not False:
            fail(f"security_control_not_false:{field}")
    for claim in [
        "source_direct_precheck_only",
        "candidate_only",
        "not_live_fetch_invoked",
        "not_source_of_record",
        "not_kds_canonical_written",
        "not_gfis_source_of_record_written",
        "not_accepted",
        "not_integrated",
        "not_production_ready",
    ]:
        if claim not in precheck.get("non_claims", []):
            fail(f"non_claim_missing:{claim}")
    return {
        "id": "agent-reach-p9-source-direct-precheck-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_precheck_ready",
        "current_admission": "limited_candidate_only",
        "target_count": len(targets),
        "domain_count": len(domains),
        "p0_domain_count": len(p0_domains),
        "topic_coverage": sorted(topics),
        "allowed_source_direct_methods": precheck["allowed_source_direct_methods"],
        "prior_rework_evidence": precheck["prior_rework_evidence"],
        "live_external_fetch_invoked": False,
        "non_claims": precheck["non_claims"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-PRECHECK-20260626",
            "title: Agent-Reach P9S Source Direct 预检证据 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-precheck-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-precheck-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct 预检证据 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- target_count: `{report['target_count']}`",
            f"- domain_count: `{report['domain_count']}`",
            f"- p0_domain_count: `{report['p0_domain_count']}`",
            f"- topic_coverage: `{', '.join(report['topic_coverage'])}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            "",
            "## 边界",
            "",
            "- 本证据只完成 source-direct precheck。",
            "- 本证据不执行目标站点直连读取。",
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
        "agent_reach_p9_source_direct_precheck=pass "
        f"status={report['status']} targets={report['target_count']} "
        f"domains={report['domain_count']} p0_domains={report['p0_domain_count']} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
