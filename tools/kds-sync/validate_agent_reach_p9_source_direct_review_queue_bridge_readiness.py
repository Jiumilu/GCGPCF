#!/usr/bin/env python3
"""Validate Agent-Reach P9S source-direct candidate-to-review-queue bridge readiness."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626.md"

REQUIRED_TOPICS = {"green_supply_chain", "phosphogypsum", "industrial_solid_waste", "zero_waste_city"}
REQUIRED_OBJECTIVE_FIELDS = {
    "supplier_esg",
    "solid_waste_disposal_receipt",
    "resource_utilization_product",
    "product_carbon_footprint",
    "zero_waste_city_indicator",
    "green_financing_purpose",
}
REQUIRED_PROJECTS = {"GFIS", "WAS", "WAES", "KDS"}
FIELD_PROJECT_ROUTES = {
    "supplier_esg": ["GFIS", "WAES", "KDS"],
    "green_supply_chain_registry": ["GFIS", "WAES", "KDS"],
    "product_carbon_footprint": ["GFIS", "WAS", "WAES", "KDS"],
    "carbon_traceability": ["GFIS", "WAS", "KDS"],
    "solid_waste_disposal_receipt": ["GFIS", "WAS", "KDS"],
    "solid_waste_resource_utilization": ["GFIS", "WAS", "WAES", "KDS"],
    "resource_utilization_product": ["GFIS", "WAS", "WAES", "KDS"],
    "pollution_control_standard": ["WAES", "KDS"],
    "industrial_solid_waste_policy": ["GFIS", "WAES", "KDS"],
    "zero_waste_city_indicator": ["GFIS", "WAS", "WAES", "KDS"],
    "zero_waste_city_case": ["GFIS", "WAS", "KDS"],
    "green_financing_purpose": ["GFIS", "WAS", "KDS"],
    "use_of_proceeds_tracking": ["GFIS", "WAS", "KDS"],
    "policy_evidence": ["WAES", "KDS"],
    "evidence_standard_reference": ["WAES", "KDS"],
    "scope3_emissions": ["GFIS", "WAS", "WAES", "KDS"],
}
REQUIRED_ITEM_FIELDS = {
    "preview_item_id",
    "queue_status",
    "admission",
    "source_target_id",
    "source_domain",
    "priority",
    "topics",
    "entrypoint_methods",
    "business_fields",
    "route_projects",
    "review_lanes",
    "review_decision_required",
    "source_record_promotion_allowed",
    "non_claims",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_review_queue_bridge_readiness=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def review_lanes_for(projects: list[str]) -> list[str]:
    lanes: list[str] = []
    if "GFIS" in projects:
        lanes.append("gfis_business_owner_review")
    if "WAS" in projects:
        lanes.append("was_asset_evidence_review")
    if "WAES" in projects:
        lanes.append("waes_policy_and_compliance_review")
    if "KDS" in projects:
        lanes.append("kds_traceability_review")
    return lanes


def route_projects_for(fields: list[str]) -> list[str]:
    projects = {"KDS"}
    for field in fields:
        projects.update(FIELD_PROJECT_ROUTES.get(field, ["KDS"]))
    return sorted(projects)


def validate_precheck(precheck: dict[str, Any]) -> None:
    if precheck.get("status") != "p9_source_direct_hit_rate_precheck_ready":
        fail("precheck_status_not_ready")
    if precheck.get("current_admission") != "limited_candidate_only":
        fail("current_admission_mismatch")
    targets = precheck.get("source_direct_targets", [])
    if len(targets) != 13:
        fail("target_count_mismatch")
    topics = {topic for target in targets for topic in target.get("topics", [])}
    if topics != REQUIRED_TOPICS:
        fail("topic_set_mismatch")
    fields = {field for target in targets for field in target.get("business_fields", [])}
    if not REQUIRED_OBJECTIVE_FIELDS <= fields:
        fail("objective_business_fields_missing")


def build_preview_items(precheck: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for target in precheck.get("source_direct_targets", []):
        projects = route_projects_for(target["business_fields"])
        items.append(
            {
                "preview_item_id": f"p9s-review-preview-{target['target_id']}",
                "queue_status": "review_queue_preview_only",
                "admission": "candidate_only_review_candidate",
                "source_target_id": target["target_id"],
                "source_domain": target["domain"],
                "priority": target["priority"],
                "topics": target["topics"],
                "entrypoint_methods": sorted({entrypoint["method"] for entrypoint in target["entrypoints"]}),
                "business_fields": target["business_fields"],
                "route_projects": projects,
                "review_lanes": review_lanes_for(projects),
                "review_decision_required": True,
                "source_record_promotion_allowed": False,
                "non_claims": [
                    "preview_only",
                    "candidate_only",
                    "not_review_queue_created",
                    "not_runtime_intake_created",
                    "not_waes_review_created",
                    "not_verified",
                    "not_source_of_record",
                    "not_accepted",
                    "not_integrated",
                    "not_production_ready",
                ],
            }
        )
    return items


def validate_items(items: list[dict[str, Any]], precheck: dict[str, Any]) -> dict[str, Any]:
    targets = precheck.get("source_direct_targets", [])
    target_ids = {target["target_id"] for target in targets}
    item_target_ids = {item.get("source_target_id") for item in items}
    if item_target_ids != target_ids:
        fail("preview_item_target_coverage_mismatch")
    topic_coverage = {topic for item in items for topic in item.get("topics", [])}
    if topic_coverage != REQUIRED_TOPICS:
        fail("preview_item_topic_coverage_mismatch")
    field_coverage = {field for item in items for field in item.get("business_fields", [])}
    if not REQUIRED_OBJECTIVE_FIELDS <= field_coverage:
        fail("preview_item_objective_field_coverage_missing")
    project_coverage = {project for item in items for project in item.get("route_projects", [])}
    if not REQUIRED_PROJECTS <= project_coverage:
        fail("preview_item_project_coverage_missing")
    p0_topic_coverage = {
        topic
        for item in items
        if item["priority"] == "P0"
        for topic in item.get("topics", [])
    }
    if p0_topic_coverage != REQUIRED_TOPICS:
        fail("p0_topic_coverage_missing")
    for item in items:
        missing = sorted(REQUIRED_ITEM_FIELDS - set(item))
        if missing:
            fail(f"preview_item_missing_fields:{item.get('preview_item_id')}:{','.join(missing)}")
        if item["queue_status"] != "review_queue_preview_only":
            fail(f"preview_item_queue_status_mismatch:{item['preview_item_id']}")
        if item["admission"] != "candidate_only_review_candidate":
            fail(f"preview_item_admission_mismatch:{item['preview_item_id']}")
        if item["review_decision_required"] is not True:
            fail(f"preview_item_review_decision_not_required:{item['preview_item_id']}")
        if item["source_record_promotion_allowed"] is not False:
            fail(f"preview_item_source_record_promotion_allowed:{item['preview_item_id']}")
        if not item["review_lanes"]:
            fail(f"preview_item_review_lanes_missing:{item['preview_item_id']}")
        for claim in [
            "not_review_queue_created",
            "not_runtime_intake_created",
            "not_waes_review_created",
            "not_verified",
            "not_source_of_record",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ]:
            if claim not in item["non_claims"]:
                fail(f"preview_item_non_claim_missing:{item['preview_item_id']}:{claim}")
    return {
        "preview_item_count": len(items),
        "target_coverage": round(len(item_target_ids) / len(target_ids), 4),
        "topic_coverage": round(len(topic_coverage) / len(REQUIRED_TOPICS), 4),
        "p0_topic_coverage": round(len(p0_topic_coverage) / len(REQUIRED_TOPICS), 4),
        "objective_business_field_coverage": sorted(REQUIRED_OBJECTIVE_FIELDS & field_coverage),
        "route_project_coverage": sorted(project_coverage),
        "threshold_pass": True,
    }


def build_report() -> dict[str, Any]:
    precheck = load_json(PRECHECK)
    validate_precheck(precheck)
    items = build_preview_items(precheck)
    coverage = validate_items(items, precheck)
    return {
        "id": "agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_review_queue_bridge_readiness_ready",
        "current_admission": "limited_candidate_only",
        "mode": "source_direct_review_queue_bridge_preview_only",
        "live_external_fetch_invoked": False,
        "review_queue_created": False,
        "runtime_intake_created": False,
        "waes_review_created": False,
        "verified_artifact_created": False,
        "source_record_promotion_allowed": False,
        "precheck_source": PRECHECK.relative_to(ROOT).as_posix(),
        "coverage": coverage,
        "preview_items": items,
        "validator_checks": {
            "requires_13_preview_items": coverage["preview_item_count"] == 13,
            "requires_full_target_coverage": coverage["target_coverage"] == 1.0,
            "requires_four_topic_coverage": coverage["topic_coverage"] == 1.0,
            "requires_p0_topic_coverage": coverage["p0_topic_coverage"] == 1.0,
            "requires_objective_business_fields": set(coverage["objective_business_field_coverage"]) == REQUIRED_OBJECTIVE_FIELDS,
            "requires_gfis_was_waes_kds_routes": REQUIRED_PROJECTS <= set(coverage["route_project_coverage"]),
            "requires_candidate_only_admission": True,
            "blocks_source_record_promotion": True,
            "blocks_real_review_queue_creation": True,
        },
        "non_claims": [
            "bridge_readiness_only",
            "preview_only",
            "not_live_fetch_invoked",
            "not_review_queue_created",
            "not_runtime_intake_created",
            "not_waes_review_created",
            "not_verified",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    coverage = report["coverage"]
    lines = [
        "---",
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-REVIEW-QUEUE-BRIDGE-READINESS-20260626",
        "title: Agent-Reach P9S Source Direct Review Queue Bridge 就绪证据 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct Review Queue Bridge 就绪证据 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- mode: `{report['mode']}`",
        f"- preview_item_count: `{coverage['preview_item_count']}`",
        f"- target_coverage: `{coverage['target_coverage']}`",
        f"- topic_coverage: `{coverage['topic_coverage']}`",
        f"- p0_topic_coverage: `{coverage['p0_topic_coverage']}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        f"- review_queue_created: `{report['review_queue_created']}`",
        f"- source_record_promotion_allowed: `{report['source_record_promotion_allowed']}`",
        "",
        "## 业务字段覆盖",
        "",
    ]
    for field in coverage["objective_business_field_coverage"]:
        lines.append(f"- `{field}`")
    lines.extend(["", "## 路由项目", ""])
    for project in coverage["route_project_coverage"]:
        lines.append(f"- `{project}`")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 本证据只证明 P9S source-direct candidate 到人工 review queue 的字段和路由已准备。",
            "- 本证据不创建真实 review queue、runtime intake、WAES review 或 verified artifact。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    failed = [key for key, value in report["validator_checks"].items() if value is not True]
    if failed:
        fail(f"validator_checks_failed:{','.join(failed)}")
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_review_queue_bridge_readiness=pass "
        f"status={report['status']} preview_items={report['coverage']['preview_item_count']} "
        "target_coverage=1.0 topic_coverage=1.0 review_queue_created=false"
    )


if __name__ == "__main__":
    main()
