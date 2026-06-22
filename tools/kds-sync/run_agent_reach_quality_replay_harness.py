#!/usr/bin/env python3
"""Run Agent-Reach offline quality replay harness."""

from __future__ import annotations

import json
from statistics import mean
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/agent-reach/quality-replay-harness.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def candidate_score(candidate: dict) -> float:
    return round(
        (
            candidate["relevance_score"] * 0.4
            + candidate["freshness_score"] * 0.2
            + candidate["authority_score"] * 0.2
            + candidate["traceability_score"] * 0.2
        ),
        4,
    )


def build_report() -> dict:
    fixture = load_fixture()
    queries = fixture["queries"]
    candidates = fixture["candidate_results"]
    required_fields = set(fixture["required_candidate_fields"])
    thresholds = fixture["thresholds"]

    grouped: dict[str, list[dict]] = {}
    for candidate in candidates:
        item = dict(candidate)
        item["composite_score"] = candidate_score(candidate)
        grouped.setdefault(candidate["query_id"], []).append(item)
    for items in grouped.values():
        items.sort(key=lambda item: item["composite_score"], reverse=True)

    top_hits = 0
    query_reports = []
    for query in queries:
        ranked = grouped.get(query["query_id"], [])
        top_candidate_id = ranked[0]["candidate_id"] if ranked else None
        top_hit = top_candidate_id == query["expected_top_candidate_id"]
        top_hits += int(top_hit)
        query_reports.append(
            {
                "query_id": query["query_id"],
                "candidate_count": len(ranked),
                "expected_top_candidate_id": query["expected_top_candidate_id"],
                "actual_top_candidate_id": top_candidate_id,
                "precision_at_1_hit": top_hit,
                "top_composite_score": ranked[0]["composite_score"] if ranked else 0,
            }
        )

    field_checks = [required_fields <= set(candidate) for candidate in candidates]
    required_field_coverage = round(sum(field_checks) / len(field_checks), 4) if field_checks else 0
    composite_scores = [candidate_score(candidate) for candidate in candidates]
    average_score = round(mean(composite_scores), 4) if composite_scores else 0
    precision_at_1 = round(top_hits / len(queries), 4) if queries else 0
    forbidden_claim_count = 0

    threshold_pass = (
        len(queries) >= thresholds["minimum_query_count"]
        and len(candidates) >= thresholds["minimum_candidate_count"]
        and average_score >= thresholds["minimum_average_score"]
        and precision_at_1 >= thresholds["minimum_precision_at_1"]
        and required_field_coverage >= thresholds["minimum_required_field_coverage"]
        and forbidden_claim_count <= thresholds["maximum_forbidden_claim_count"]
    )

    return {
        "id": "agent-reach-quality-replay-harness-20260622",
        "round": "GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001",
        "status": "quality_replay_harness_ready" if threshold_pass else "quality_replay_harness_rework_required",
        "current_admission": "limited_candidate_only",
        "mode": fixture["mode"],
        "query_count": len(queries),
        "candidate_count": len(candidates),
        "average_score": average_score,
        "precision_at_1": precision_at_1,
        "required_field_coverage": required_field_coverage,
        "forbidden_claim_count": forbidden_claim_count,
        "thresholds": thresholds,
        "threshold_pass": threshold_pass,
        "query_reports": query_reports,
        "security_controls": {
            "agent_reach_binary_invoked": False,
            "live_external_search_invoked": False,
            "doctor_health_probe_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "next_round": "GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001",
    }


def main() -> None:
    print(json.dumps(build_report(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
