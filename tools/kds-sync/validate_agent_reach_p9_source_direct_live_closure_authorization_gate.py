#!/usr/bin/env python3
"""Validate the P9S closure runner cannot execute live without authorization."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-authorization-gate-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-authorization-gate-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_live_closure_authorization_gate=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def probe_execute_live_without_authorization() -> dict[str, Any]:
    command = [
        "python3",
        "tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py",
        "--execute-live",
        "--write-evidence",
    ]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=120)
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0:
        fail("closure_runner_execute_live_probe_failed")
    if "live_external_fetch_invoked=true" in output:
        fail("execute_live_probe_invoked_live_fetch")
    return {
        "command": " ".join(command),
        "returncode": proc.returncode,
        "output_tail": output[-1000:],
    }


def build_report() -> dict[str, Any]:
    probe = probe_execute_live_without_authorization()
    runner = read_json(RUNNER_EVIDENCE)
    steps = [step.get("step") for step in runner.get("steps", [])]
    if runner.get("status") != "blocked_pending_p9_source_direct_authorization":
        fail(f"unexpected_runner_status:{runner.get('status')}")
    if runner.get("execution_requested") is not True:
        fail("execute_live_flag_not_recorded")
    if runner.get("authorization_valid") is not False:
        fail("authorization_valid_not_false")
    if runner.get("authorization_intake_status") != "blocked_pending_p9_source_direct_authorization":
        fail("authorization_intake_status_mismatch")
    if runner.get("live_external_fetch_invoked") is not False:
        fail("live_external_fetch_invoked_not_false")
    if runner.get("completion_claim_allowed") is not False:
        fail("completion_claim_allowed_not_false")
    if steps != ["authorization_intake"]:
        fail("authorization_gate_allowed_unexpected_steps")
    for field in [
        "credential_written",
        "browser_cookie_extraction_invoked",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "production_config_write_allowed",
        "global_mcp_config_write_allowed",
        "production_integration_allowed",
    ]:
        if runner.get("security_controls", {}).get(field) is not False:
            fail(f"security_control_not_false:{field}")
    return {
        "id": "agent-reach-p9-source-direct-live-closure-authorization-gate-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_live_closure_authorization_gate_pass",
        "current_admission": "limited_candidate_only",
        "mode": "execute_live_without_authorization_probe",
        "probe": probe,
        "runner_evidence": RUNNER_EVIDENCE.relative_to(ROOT).as_posix(),
        "blocked_status": runner.get("status"),
        "blocked_steps": steps,
        "execution_requested": runner.get("execution_requested"),
        "authorization_valid": runner.get("authorization_valid"),
        "live_external_fetch_invoked": runner.get("live_external_fetch_invoked"),
        "completion_claim_allowed": runner.get("completion_claim_allowed"),
        "security_controls": runner.get("security_controls", {}),
        "non_claims": [
            "authorization_gate_probe_only",
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
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-CLOSURE-AUTH-GATE-20260626",
            "title: Agent-Reach P9S Source Direct Live Closure Authorization Gate 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-closure-authorization-gate-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-closure-authorization-gate-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Live Closure Authorization Gate 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- blocked_status: `{report['blocked_status']}`",
            f"- blocked_steps: `{report['blocked_steps']}`",
            f"- execution_requested: `{report['execution_requested']}`",
            f"- authorization_valid: `{report['authorization_valid']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence probes execute-live without P9S authorization.",
            "- This evidence proves execute-live alone does not invoke live target-site fetch.",
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
        "agent_reach_p9_source_direct_live_closure_authorization_gate=pass "
        f"status={report['status']} execution_requested={str(report['execution_requested']).lower()} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
