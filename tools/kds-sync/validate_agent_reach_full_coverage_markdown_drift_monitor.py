#!/usr/bin/env python3
"""Validate Agent-Reach full coverage Markdown non-claim marker drift."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-precheck-20260626.json"
FULL_COVERAGE_MD = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-full-coverage-markdown-drift-monitor-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-full-coverage-markdown-drift-monitor-20260626.md"

FORBIDDEN_MARKERS = [
    "source-of-record created",
    "KDS canonical written",
    "GFIS source-of-record written",
    "production_ready: true",
    "integrated: true",
    "accepted: true",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_full_coverage_markdown_drift_monitor=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def required_markers(precheck: dict[str, Any]) -> list[str]:
    drift = precheck.get("drift_monitoring", {})
    markers = drift.get("required_markers", [])
    if not markers:
        fail("required_markers_missing_from_precheck")
    return markers


def marker_report(markdown: str, markers: list[str]) -> dict[str, Any]:
    missing = [marker for marker in markers if marker not in markdown]
    forbidden_hits = [marker for marker in FORBIDDEN_MARKERS if marker in markdown]
    return {
        "required_marker_count": len(markers),
        "present_marker_count": len(markers) - len(missing),
        "missing_markers": missing,
        "forbidden_marker_hits": forbidden_hits,
        "marker_coverage": round((len(markers) - len(missing)) / len(markers), 4) if markers else 0,
        "threshold_pass": not missing and not forbidden_hits,
    }


def validate_negative_cases(markers: list[str]) -> dict[str, bool]:
    positive = "\n".join(markers)
    missing_case = positive.replace(markers[0], "")
    forbidden_case = positive + "\naccepted: true\n"
    if marker_report(missing_case, markers)["threshold_pass"] is not False:
        fail("negative_missing_marker_unexpected_pass")
    if marker_report(forbidden_case, markers)["threshold_pass"] is not False:
        fail("negative_forbidden_marker_unexpected_pass")
    return {
        "negative_missing_marker_test_passed": True,
        "negative_forbidden_marker_test_passed": True,
    }


def build_report() -> dict[str, Any]:
    precheck = load_json(PRECHECK)
    markdown = read_text(FULL_COVERAGE_MD)
    markers = required_markers(precheck)
    report = marker_report(markdown, markers)
    if not report["threshold_pass"]:
        fail(
            "marker_gate_failed:"
            f"missing={','.join(report['missing_markers']) or 'none'}:"
            f"forbidden={','.join(report['forbidden_marker_hits']) or 'none'}"
        )
    negative = validate_negative_cases(markers)
    return {
        "id": "agent-reach-full-coverage-markdown-drift-monitor-20260626",
        "date": "2026-06-26",
        "status": "full_coverage_markdown_drift_monitor_pass",
        "current_admission": "limited_candidate_only",
        "source_markdown": FULL_COVERAGE_MD.relative_to(ROOT).as_posix(),
        "precheck_source": PRECHECK.relative_to(ROOT).as_posix(),
        "live_external_search_invoked": False,
        "agent_reach_binary_invoked": False,
        "required_markers": markers,
        "forbidden_markers": FORBIDDEN_MARKERS,
        "marker_report": report,
        "validator_checks": {
            "requires_candidate_only_marker": True,
            "requires_non_claim_marker": True,
            "requires_raw_payload_not_persisted_marker": True,
            "blocks_accepted_integrated_production_ready_claims": True,
            "self_test_passed_without_network": True,
            **negative,
        },
        "non_claims": [
            "drift_monitor_only",
            "not_live_search_invoked",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "---",
        "doc_id: GPCF-DOC-AGENT-REACH-FULL-COVERAGE-MARKDOWN-DRIFT-MONITOR-20260626",
        "title: Agent-Reach Full Coverage Markdown 漂移监控 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-full-coverage-markdown-drift-monitor-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-full-coverage-markdown-drift-monitor-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach Full Coverage Markdown 漂移监控 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- source_markdown: `{report['source_markdown']}`",
        f"- marker_coverage: `{report['marker_report']['marker_coverage']}`",
        f"- threshold_pass: `{report['marker_report']['threshold_pass']}`",
        f"- live_external_search_invoked: `{report['live_external_search_invoked']}`",
        "",
        "## Required Markers",
        "",
    ]
    for marker in report["required_markers"]:
        lines.append(f"- `{marker}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This evidence is candidate-only.",
            "- This evidence does not create source-of-record.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_full_coverage_markdown_drift_monitor=pass "
        f"status={report['status']} marker_coverage={report['marker_report']['marker_coverage']} "
        "live_external_search_invoked=false"
    )


if __name__ == "__main__":
    main()
