#!/usr/bin/env python3
"""Classify the authorized P9R hit-rate rerun rework result."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RERUN_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-rerun-rework-classification-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-rerun-rework-classification-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_rerun_rework_classification=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_report() -> dict[str, Any]:
    rerun = read_json(RERUN_EVIDENCE)
    hit_rate = rerun.get("hit_rate_report", {})
    controls = rerun.get("security_controls", {})
    errors = rerun.get("query_errors", [])
    error_types = Counter(error.get("error_type", "unknown") for error in errors)
    provider_blocked = sum(1 for error in errors if "web_provider_unavailable" in error.get("message", ""))

    if rerun.get("authorization_valid") is not True:
        fail("authorization_not_valid")
    if rerun.get("execution_requested") is not True:
        fail("execution_not_requested")
    if controls.get("live_external_search_invoked") is not True:
        fail("live_external_search_not_invoked")
    if rerun.get("status") != "p9_priority_target_hit_rate_rework_required":
        fail(f"unexpected_status:{rerun.get('status')}")
    if hit_rate.get("threshold_pass") is not False:
        fail("threshold_should_not_pass")
    if hit_rate.get("candidate_count") != 0:
        fail("unexpected_candidate_count")
    if hit_rate.get("query_error_count") != rerun.get("planned_query_count"):
        fail("query_error_count_mismatch")
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
        "id": "agent-reach-p9-rerun-rework-classification-20260626",
        "date": "2026-06-26",
        "status": "p9_rerun_rework_classification_pass",
        "current_admission": "limited_candidate_only",
        "rerun_evidence": RERUN_EVIDENCE.relative_to(ROOT).as_posix(),
        "rerun_status": rerun.get("status"),
        "authorization_valid": rerun.get("authorization_valid"),
        "execution_requested": rerun.get("execution_requested"),
        "live_external_search_invoked": controls.get("live_external_search_invoked"),
        "planned_query_count": rerun.get("planned_query_count"),
        "candidate_count": hit_rate.get("candidate_count"),
        "query_error_count": hit_rate.get("query_error_count"),
        "topic_coverage": hit_rate.get("topic_coverage"),
        "threshold_pass": hit_rate.get("threshold_pass"),
        "error_type_counts": dict(sorted(error_types.items())),
        "provider_blocked_error_count": provider_blocked,
        "classification": "search_provider_path_rework_required",
        "recommended_next_path": "p9_source_direct_hit_rate_live_run_after_human_authorization",
        "security_controls": controls,
        "completion_claim_allowed": False,
        "non_claims": [
            "classification_only",
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
            "doc_id: GPCF-DOC-AGENT-REACH-P9-RERUN-REWORK-CLASSIFICATION-20260626",
            "title: Agent-Reach P9R Rerun Rework Classification 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-rerun-rework-classification-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-rerun-rework-classification-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9R Rerun Rework Classification 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- rerun_status: `{report['rerun_status']}`",
            f"- live_external_search_invoked: `{report['live_external_search_invoked']}`",
            f"- planned_query_count: `{report['planned_query_count']}`",
            f"- candidate_count: `{report['candidate_count']}`",
            f"- query_error_count: `{report['query_error_count']}`",
            f"- topic_coverage: `{report['topic_coverage']}`",
            f"- threshold_pass: `{report['threshold_pass']}`",
            f"- classification: `{report['classification']}`",
            f"- recommended_next_path: `{report['recommended_next_path']}`",
            "",
            "## Boundary",
            "",
            "- This evidence classifies the authorized rerun result only.",
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
        "agent_reach_p9_rerun_rework_classification=pass "
        f"status={report['status']} classification={report['classification']} "
        f"live_external_search_invoked={str(report['live_external_search_invoked']).lower()}"
    )


if __name__ == "__main__":
    main()
