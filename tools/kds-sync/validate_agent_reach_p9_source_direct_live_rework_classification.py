#!/usr/bin/env python3
"""Classify the authorized P9S source-direct live rework result."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LIVE_REPORT = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-rework-classification-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-rework-classification-20260627.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_live_rework_classification=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_report() -> dict[str, Any]:
    live = read_json(LIVE_REPORT)
    hit_rate = live.get("hit_rate_report", {})
    controls = live.get("security_controls", {})
    topics = hit_rate.get("topic_reports", {})
    failed_topics = sorted(topic_id for topic_id, item in topics.items() if item.get("threshold_pass") is not True)
    passed_topics = sorted(topic_id for topic_id, item in topics.items() if item.get("threshold_pass") is True)
    critical_errors = [error for error in live.get("fetch_errors", []) if error.get("critical") is not False]

    if live.get("authorization_valid") is not True:
        fail("authorization_not_valid")
    if live.get("execution_requested") is not True:
        fail("execution_not_requested")
    if controls.get("live_external_fetch_invoked") is not True:
        fail("live_external_fetch_not_invoked")
    if live.get("status") != "p9_source_direct_hit_rate_rework_required":
        fail(f"unexpected_live_status:{live.get('status')}")
    if hit_rate.get("threshold_pass") is not False:
        fail("threshold_should_not_pass")
    if not failed_topics and not critical_errors:
        fail("rework_reason_missing")
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
            fail(f"boundary_violation:{field}")

    return {
        "id": "agent-reach-p9-source-direct-live-rework-classification-20260627",
        "date": "2026-06-27",
        "status": "p9_source_direct_live_rework_classification_pass",
        "current_admission": "limited_candidate_only",
        "live_report": LIVE_REPORT.relative_to(ROOT).as_posix(),
        "live_status": live.get("status"),
        "authorization_valid": live.get("authorization_valid"),
        "execution_requested": live.get("execution_requested"),
        "live_external_fetch_invoked": controls.get("live_external_fetch_invoked"),
        "candidate_count": hit_rate.get("candidate_count"),
        "fetch_error_count": hit_rate.get("fetch_error_count"),
        "critical_fetch_error_count": hit_rate.get("critical_fetch_error_count"),
        "noncritical_fetch_error_count": hit_rate.get("noncritical_fetch_error_count"),
        "topic_coverage": hit_rate.get("topic_coverage"),
        "threshold_pass": hit_rate.get("threshold_pass"),
        "passed_topics": passed_topics,
        "failed_topics": failed_topics,
        "critical_fetch_errors": critical_errors,
        "classification": "p9s_live_hit_rate_rework_required",
        "rework_reason": (
            "topic_threshold_gap_and_critical_fetch_errors"
            if failed_topics and critical_errors
            else "topic_threshold_gap"
            if failed_topics
            else "critical_fetch_errors_only"
        ),
        "recommended_rework_focus": (
            [
                "critical_entrypoint_fetch_errors",
                "target_availability_or_alternate_entrypoint_review",
            ]
            if critical_errors and not failed_topics
            else [
                "industrial_solid_waste_keyword_hit_gap",
                "critical_entrypoint_fetch_errors",
                "source_direct_discovery_filter_for_non_html_assets",
            ]
        ),
        "security_controls": controls,
        "completion_claim_allowed": False,
        "non_claims": [
            "rework_classification_only",
            "not_hit_rate_completed",
            "not_source_of_record",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-REWORK-CLASSIFICATION-20260627",
            "title: Agent-Reach P9S Source Direct Live Rework Classification 2026-06-27",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-rework-classification-20260627.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-rework-classification-20260627.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-27",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Live Rework Classification 2026-06-27",
            "",
            f"- status: `{report['status']}`",
            f"- live_status: `{report['live_status']}`",
            f"- candidate_count: `{report['candidate_count']}`",
            f"- topic_coverage: `{report['topic_coverage']}`",
            f"- passed_topics: `{report['passed_topics']}`",
            f"- failed_topics: `{report['failed_topics']}`",
            f"- critical_fetch_error_count: `{report['critical_fetch_error_count']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence classifies the authorized P9S live rework result only.",
            "- This evidence does not convert rework into completion.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_live_rework_classification=pass "
        f"status={report['status']} topic_coverage={report['topic_coverage']} "
        f"failed_topics={','.join(report['failed_topics'])}"
    )


if __name__ == "__main__":
    main()
