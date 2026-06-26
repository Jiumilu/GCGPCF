#!/usr/bin/env python3
"""Validate P9S source-direct pre-live gates before human-authorized execution."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-pre-live-preflight-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-pre-live-preflight-20260626.md"

CHECKS = [
    {
        "id": "authorization_intake_pending",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_authorization_intake.py"],
        "required": "status=blocked_pending_p9_source_direct_authorization",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "authorization_file_safety",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_authorization_file_safety.py"],
        "required": "agent_reach_p9_source_direct_authorization_file_safety=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "runner_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_runner_readiness.py"],
        "required": "agent_reach_p9_source_direct_runner_readiness=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "output_quality_gate_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_output_quality_gate.py", "--gate-readiness"],
        "required": "agent_reach_p9_source_direct_output_quality_gate=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "review_queue_bridge_preview",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_review_queue_bridge_readiness.py"],
        "required": "agent_reach_p9_source_direct_review_queue_bridge_readiness=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "authorization_negative_fixtures",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_authorization_negative_fixtures.py"],
        "required": "agent_reach_p9_source_direct_authorization_negative_fixtures=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "authorization_template",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_authorization_template.py"],
        "required": "agent_reach_p9_source_direct_authorization_template=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "offline_hit_rate_simulation",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_offline_hit_rate_simulation.py"],
        "required": "agent_reach_p9_source_direct_offline_hit_rate_simulation=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "markdown_drift_monitor",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_markdown_drift_monitor.py"],
        "required": "agent_reach_p9_source_direct_markdown_drift_monitor=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "live_execution_command_pack",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_execution_command_pack.py"],
        "required": "agent_reach_p9_source_direct_live_execution_command_pack=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "live_closure_runner_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_closure_runner_readiness.py"],
        "required": "agent_reach_p9_source_direct_live_closure_runner_readiness=pass",
        "live_external_fetch_invoked": False,
    },
    {
        "id": "live_closure_authorization_gate",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_closure_authorization_gate.py"],
        "required": "agent_reach_p9_source_direct_live_closure_authorization_gate=pass",
        "live_external_fetch_invoked": False,
    },
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_pre_live_preflight=fail reason={message}")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_check(check: dict[str, Any]) -> dict[str, Any]:
    proc = subprocess.run(check["command"], cwd=ROOT, text=True, capture_output=True, timeout=120)
    output = (proc.stdout + proc.stderr).strip()
    passed = proc.returncode == 0 and check["required"] in output and "live_external_fetch_invoked=true" not in output
    return {
        "id": check["id"],
        "command": " ".join(check["command"]),
        "returncode": proc.returncode,
        "required": check["required"],
        "passed": passed,
        "live_external_fetch_invoked": False,
        "output_tail": output[-600:],
    }


def build_report() -> dict[str, Any]:
    results = [run_check(check) for check in CHECKS]
    failed = [item["id"] for item in results if not item["passed"]]
    if failed:
        fail("checks_failed:" + ",".join(failed))
    return {
        "id": "agent-reach-p9-source-direct-pre-live-preflight-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_pre_live_preflight_pass",
        "current_admission": "limited_candidate_only",
        "mode": "pre_live_no_external_fetch",
        "check_count": len(results),
        "check_results": results,
        "authorization_required_before_live": True,
        "live_external_fetch_invoked": False,
        "completion_claim_allowed": False,
        "next_required_authorization_text": "授权执行 Agent-Reach P9S Source Direct Hit-Rate Live Run",
        "non_claims": [
            "pre_live_preflight_only",
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
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-PRE-LIVE-PREFLIGHT-20260626",
        "title: Agent-Reach P9S Source Direct Pre-Live Preflight 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-pre-live-preflight-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-pre-live-preflight-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct Pre-Live Preflight 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- check_count: `{report['check_count']}`",
        f"- authorization_required_before_live: `{report['authorization_required_before_live']}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
        "",
        "## Checks",
        "",
    ]
    for item in report["check_results"]:
        lines.append(f"- `{item['id']}`: `{item['passed']}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This evidence is pre-live preflight only.",
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
        "agent_reach_p9_source_direct_pre_live_preflight=pass "
        f"checks={report['check_count']} authorization_required_before_live=true "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
