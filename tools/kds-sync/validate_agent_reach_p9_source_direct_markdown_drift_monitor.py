#!/usr/bin/env python3
"""Validate P9S source-direct Markdown evidence keeps candidate-only and non-claim markers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-markdown-drift-monitor-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-markdown-drift-monitor-20260626.md"

MARKDOWN_FILES = [
    "agent-reach-p9-source-direct-precheck-20260626.md",
    "agent-reach-p9-source-direct-authorization-request-20260626.md",
    "agent-reach-p9-source-direct-runner-readiness-20260626.md",
    "agent-reach-p9-source-direct-output-quality-gate-20260626.md",
    "agent-reach-p9-source-direct-live-execution-readiness-closure-20260626.md",
    "agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626.md",
    "agent-reach-p9-source-direct-live-authorization-intake-20260626.md",
    "agent-reach-p9-source-direct-live-execution-command-pack-20260626.md",
    "agent-reach-p9-source-direct-offline-hit-rate-simulation-20260626.md",
    "agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.md",
    "agent-reach-p9-source-direct-authorization-template-20260626.md",
    "agent-reach-p9-source-direct-hit-rate-live-run-20260626.md",
]

REQUIRED_MARKER_GROUPS = {
    "kds_canonical_non_write": ["does not write KDS canonical Markdown", "不写 KDS canonical"],
    "gfis_source_record_non_write": ["does not write GFIS source-of-record", "不写 GFIS source-of-record"],
    "accepted_non_claim": ["does not claim accepted", "不声明 accepted"],
    "integrated_non_claim": ["integrated", "不声明 accepted / integrated"],
    "production_ready_non_claim": ["production_ready", "不声明 accepted / integrated / production_ready"],
}
NO_LIVE_MARKERS = [
    "does not invoke live",
    "not_live_fetch_invoked",
    "live_external_fetch_invoked: `False`",
    "live_external_fetch_invoked: `false`",
]
SOURCE_RECORD_MARKERS = [
    "does not create source-of-record",
    "not_source_of_record",
    "does not write GFIS source-of-record",
    "不写 GFIS source-of-record",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_markdown_drift_monitor=fail reason={message}")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def has_any(text: str, markers: list[str]) -> bool:
    folded = text.lower()
    return any(marker.lower() in folded for marker in markers)


def validate_markdown(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    missing: list[str] = []
    if not text.startswith("---"):
        missing.append("frontmatter")
    for marker_id, markers in REQUIRED_MARKER_GROUPS.items():
        if not has_any(text, markers):
            missing.append(marker_id)
    if not has_any(text, SOURCE_RECORD_MARKERS):
        missing.append("source_record_non_claim")
    if "live-run" not in path.name and not has_any(text, NO_LIVE_MARKERS):
        missing.append("no_live_marker")
    if missing:
        fail(f"markdown_markers_missing:{path.relative_to(ROOT)}:{','.join(missing)}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "marker_status": "pass",
        "frontmatter": True,
    }


def build_report() -> dict[str, Any]:
    file_reports = [validate_markdown(EVIDENCE_DIR / name) for name in MARKDOWN_FILES]
    return {
        "id": "agent-reach-p9-source-direct-markdown-drift-monitor-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_markdown_drift_monitor_pass",
        "current_admission": "limited_candidate_only",
        "monitored_markdown_count": len(file_reports),
        "file_reports": file_reports,
        "live_external_fetch_invoked": False,
        "completion_claim_allowed": False,
        "non_claims": [
            "drift_monitor_only",
            "not_live_fetch_invoked",
            "not_live_run_completed",
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
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-MARKDOWN-DRIFT-MONITOR-20260626",
        "title: Agent-Reach P9S Source Direct Markdown Drift Monitor 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-markdown-drift-monitor-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-markdown-drift-monitor-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct Markdown Drift Monitor 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- monitored_markdown_count: `{report['monitored_markdown_count']}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
        "",
        "## Monitored Files",
        "",
    ]
    for item in report["file_reports"]:
        lines.append(f"- `{item['path']}`: `{item['marker_status']}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This evidence is a Markdown drift monitor only.",
            "- This evidence does not invoke live target-site fetch.",
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
        "agent_reach_p9_source_direct_markdown_drift_monitor=pass "
        f"files={report['monitored_markdown_count']} live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
