#!/usr/bin/env python3
"""Run the P9S source-direct live closure in a fixed, authorization-gated order."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUTH_INTAKE_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-authorization-intake-20260626.json"
LIVE_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.md"

COMMANDS = {
    "authorization_intake": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_authorization_intake.py"],
    "live_run": [
        "python3",
        "tools/kds-sync/run_agent_reach_p9_source_direct_hit_rate.py",
        "--auth",
        "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json",
        "--execute-live",
        "--write-evidence",
    ],
    "output_quality_gate": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_output_quality_gate.py", "--validate-report"],
    "review_queue_bridge_preview": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_review_queue_bridge_readiness.py"],
    "document_control": ["python3", "tools/kds-sync/document_control.py"],
    "document_pollution": ["python3", "tools/kds-sync/check_document_pollution.py"],
    "kds_token": ["python3", "tools/kds-sync/validate_kds_token.py"],
    "loop_document_gate": ["python3", "tools/kds-sync/loop_document_gate.py"],
}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_step(step: str, *, timeout: int = 180) -> dict[str, Any]:
    command = COMMANDS[step]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    output = (proc.stdout + proc.stderr).strip()
    return {
        "step": step,
        "command": " ".join(command),
        "returncode": proc.returncode,
        "passed": proc.returncode == 0,
        "output_tail": output[-1000:],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "---",
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-CLOSURE-RUNNER-20260626",
        "title: Agent-Reach P9S Source Direct Live Closure Runner 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct Live Closure Runner 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- execution_requested: `{report['execution_requested']}`",
        f"- authorization_valid: `{report['authorization_valid']}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
        "",
        "## Steps",
        "",
    ]
    for item in report["steps"]:
        lines.append(f"- `{item['step']}`: `{item['passed']}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This runner stops before live fetch unless authorization intake is ready and execute-live is explicitly requested.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )
    return "\n".join(lines)


def build_report(execute_live: bool) -> dict[str, Any]:
    steps = [run_step("authorization_intake")]
    intake = read_json(AUTH_INTAKE_EVIDENCE)
    authorization_valid = intake.get("authorization_valid") is True and intake.get("ready_for_live_execution") is True
    base: dict[str, Any] = {
        "id": "agent-reach-p9-source-direct-live-closure-runner-20260626",
        "date": "2026-06-26",
        "current_admission": "limited_candidate_only",
        "execution_requested": execute_live,
        "authorization_valid": authorization_valid,
        "authorization_intake_status": intake.get("status"),
        "live_external_fetch_invoked": False,
        "completion_claim_allowed": False,
        "steps": steps,
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
            "closure_runner_only",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }
    if not authorization_valid:
        return {**base, "status": "blocked_pending_p9_source_direct_authorization"}
    if not execute_live:
        return {**base, "status": "authorized_execution_not_requested"}

    for step in [
        "live_run",
        "output_quality_gate",
        "review_queue_bridge_preview",
        "document_control",
        "document_pollution",
        "kds_token",
        "loop_document_gate",
    ]:
        result = run_step(step, timeout=300)
        steps.append(result)
        if not result["passed"]:
            live = read_json(LIVE_EVIDENCE)
            return {
                **base,
                "status": "p9_source_direct_live_closure_rework_required",
                "steps": steps,
                "live_external_fetch_invoked": live.get("security_controls", {}).get("live_external_fetch_invoked") is True,
                "live_run_status": live.get("status"),
            }

    live = read_json(LIVE_EVIDENCE)
    completed = live.get("status") == "p9_source_direct_hit_rate_completed"
    return {
        **base,
        "status": "p9_source_direct_live_closure_completed" if completed else "p9_source_direct_live_closure_rework_required",
        "steps": steps,
        "live_external_fetch_invoked": live.get("security_controls", {}).get("live_external_fetch_invoked") is True,
        "live_run_status": live.get("status"),
        "completion_claim_allowed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute-live", action="store_true")
    parser.add_argument("--write-evidence", action="store_true")
    args = parser.parse_args()
    report = build_report(args.execute_live)
    if args.write_evidence:
        write_json(EVIDENCE_JSON, report)
        EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
