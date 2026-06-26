#!/usr/bin/env python3
"""Validate the P9 objective audit post-live source-direct path with synthetic evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUDIT_SCRIPT = ROOT / "tools/kds-sync/validate_agent_reach_p9_objective_completion_audit.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-objective-post-live-path-simulation-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-objective-post-live-path-simulation-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_objective_post_live_path_simulation=fail reason={message}")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def synthetic_post_live_inputs() -> dict[str, Any]:
    return {
        "p9s_live": {
            "status": "p9_source_direct_hit_rate_completed",
            "hit_rate_report": {"threshold_pass": True, "topic_coverage": 1.0},
            "security_controls": {"live_external_fetch_invoked": True},
        },
        "command_pack": {"status": "p9_source_direct_live_execution_command_pack_ready"},
        "closure_runner": {
            "status": "p9_source_direct_live_closure_completed",
            "live_external_fetch_invoked": True,
        },
    }


def evaluate_post_live_path(inputs: dict[str, Any]) -> dict[str, Any]:
    p9s_live = inputs["p9s_live"]
    command_pack = inputs["command_pack"]
    closure_runner = inputs["closure_runner"]
    live_hit_rate = p9s_live["hit_rate_report"]
    live_completed = (
        p9s_live.get("status") == "p9_source_direct_hit_rate_completed"
        and live_hit_rate.get("threshold_pass") is True
        and live_hit_rate.get("topic_coverage") == 1.0
        and p9s_live.get("security_controls", {}).get("live_external_fetch_invoked") is True
    )
    post_live_source_direct_completed = (
        live_completed
        and command_pack.get("status") == "p9_source_direct_live_execution_command_pack_ready"
        and closure_runner.get("status") == "p9_source_direct_live_closure_completed"
        and closure_runner.get("live_external_fetch_invoked") is True
    )
    return {
        "live_completed": live_completed,
        "post_live_source_direct_completed": post_live_source_direct_completed,
        "source_direct_execution_mode": "post_live_closure_completed" if post_live_source_direct_completed else "not_ready",
        "authorization_boundary_status": "complete" if live_completed else "pending_human_authorization",
    }


def build_report() -> dict[str, Any]:
    audit_source = AUDIT_SCRIPT.read_text(encoding="utf-8")
    for required in [
        "post_live_source_direct_completed",
        "p9_source_direct_live_closure_completed",
        "post_live_closure_completed",
    ]:
        if required not in audit_source:
            fail(f"audit_script_missing_marker:{required}")
    inputs = synthetic_post_live_inputs()
    result = evaluate_post_live_path(inputs)
    if result["live_completed"] is not True:
        fail("synthetic_live_completed_false")
    if result["post_live_source_direct_completed"] is not True:
        fail("synthetic_post_live_source_direct_completed_false")
    if result["source_direct_execution_mode"] != "post_live_closure_completed":
        fail("synthetic_execution_mode_mismatch")
    if result["authorization_boundary_status"] != "complete":
        fail("synthetic_authorization_boundary_not_complete")
    return {
        "id": "agent-reach-p9-objective-post-live-path-simulation-20260626",
        "date": "2026-06-26",
        "status": "p9_objective_post_live_path_simulation_pass",
        "current_admission": "limited_candidate_only",
        "mode": "offline_synthetic_no_live_fetch",
        "audit_script": AUDIT_SCRIPT.relative_to(ROOT).as_posix(),
        "synthetic_result": result,
        "live_external_fetch_invoked": False,
        "completion_claim_allowed": False,
        "security_controls": {
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "non_claims": [
            "offline_simulation_only",
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
    result = report["synthetic_result"]
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-OBJECTIVE-POST-LIVE-PATH-SIM-20260626",
            "title: Agent-Reach P9 Objective Post-Live Path Simulation 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-objective-post-live-path-simulation-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-objective-post-live-path-simulation-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9 Objective Post-Live Path Simulation 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- source_direct_execution_mode: `{result['source_direct_execution_mode']}`",
            f"- authorization_boundary_status: `{result['authorization_boundary_status']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence uses synthetic offline inputs only.",
            "- This evidence does not invoke live target-site fetch.",
            "- This evidence does not complete the real P9 objective.",
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
        "agent_reach_p9_objective_post_live_path_simulation=pass "
        f"status={report['status']} "
        f"mode={report['synthetic_result']['source_direct_execution_mode']} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
