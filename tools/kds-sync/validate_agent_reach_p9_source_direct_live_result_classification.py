#!/usr/bin/env python3
"""Classify the latest authorized P9S source-direct live result."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LIVE_REPORT = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-result-classification-20260627.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-result-classification-20260627.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_live_result_classification=fail reason={message}")


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
    topic_reports = hit_rate.get("topic_reports", {})
    failed_topics = sorted(topic_id for topic_id, item in topic_reports.items() if item.get("threshold_pass") is not True)
    critical_errors = [error for error in live.get("fetch_errors", []) if error.get("critical") is not False]
    completed = (
        live.get("status") == "p9_source_direct_hit_rate_completed"
        and hit_rate.get("threshold_pass") is True
        and hit_rate.get("topic_coverage") == 1.0
        and controls.get("live_external_fetch_invoked") is True
        and not failed_topics
    )
    if live.get("authorization_valid") is not True:
        fail("authorization_not_valid")
    if live.get("execution_requested") is not True:
        fail("execution_not_requested")
    if controls.get("live_external_fetch_invoked") is not True:
        fail("live_external_fetch_not_invoked")
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
        "id": "agent-reach-p9-source-direct-live-result-classification-20260627",
        "date": "2026-06-27",
        "status": "p9_source_direct_live_result_classification_pass",
        "current_admission": "limited_candidate_only",
        "live_report": LIVE_REPORT.relative_to(ROOT).as_posix(),
        "classification": "p9s_live_hit_rate_completed" if completed else "p9s_live_hit_rate_rework_required",
        "live_status": live.get("status"),
        "authorization_valid": live.get("authorization_valid"),
        "execution_requested": live.get("execution_requested"),
        "live_external_fetch_invoked": controls.get("live_external_fetch_invoked"),
        "candidate_count": hit_rate.get("candidate_count"),
        "topic_coverage": hit_rate.get("topic_coverage"),
        "threshold_pass": hit_rate.get("threshold_pass"),
        "failed_topics": failed_topics,
        "target_availability_warning_count": hit_rate.get("target_availability_warning_count", 0),
        "critical_fetch_errors": critical_errors,
        "completion_claim_allowed": completed,
        "security_controls": controls,
        "non_claims": [
            "result_classification_only",
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
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-RESULT-CLASSIFICATION-20260627",
            "title: Agent-Reach P9S Source Direct Live Result Classification 2026-06-27",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-result-classification-20260627.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-result-classification-20260627.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-27",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Live Result Classification 2026-06-27",
            "",
            f"- status: `{report['status']}`",
            f"- classification: `{report['classification']}`",
            f"- candidate_count: `{report['candidate_count']}`",
            f"- topic_coverage: `{report['topic_coverage']}`",
            f"- target_availability_warning_count: `{report['target_availability_warning_count']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence classifies the latest authorized P9S live result only.",
            "- This evidence does not create source-of-record.",
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
        "agent_reach_p9_source_direct_live_result_classification=pass "
        f"classification={report['classification']} "
        f"topic_coverage={report['topic_coverage']}"
    )


if __name__ == "__main__":
    main()
