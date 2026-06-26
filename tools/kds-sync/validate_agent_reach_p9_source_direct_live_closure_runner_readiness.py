#!/usr/bin/env python3
"""Validate P9S source-direct live closure runner readiness without live fetch."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py"
RUNNER_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-readiness-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-readiness-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_live_closure_runner_readiness=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_blocked_probe() -> dict[str, Any]:
    proc = subprocess.run(
        ["python3", "tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py", "--write-evidence"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=120,
    )
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0:
        fail("closure_runner_probe_failed")
    if "live_external_fetch_invoked=true" in output:
        fail("closure_runner_probe_invoked_live_fetch")
    return {
        "command": "python3 tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py --write-evidence",
        "returncode": proc.returncode,
        "output_tail": output[-800:],
    }


def build_report() -> dict[str, Any]:
    if not RUNNER.exists():
        fail("closure_runner_missing")
    probe = run_blocked_probe()
    runner = read_json(RUNNER_EVIDENCE)
    steps = [step.get("step") for step in runner.get("steps", [])]
    if runner.get("status") != "blocked_pending_p9_source_direct_authorization":
        fail(f"unexpected_runner_status:{runner.get('status')}")
    if runner.get("execution_requested") is not False:
        fail("execution_requested_not_false")
    if runner.get("authorization_valid") is not False:
        fail("authorization_valid_not_false")
    if runner.get("authorization_intake_status") != "blocked_pending_p9_source_direct_authorization":
        fail("authorization_intake_status_mismatch")
    if runner.get("live_external_fetch_invoked") is not False:
        fail("live_external_fetch_invoked_not_false")
    if runner.get("completion_claim_allowed") is not False:
        fail("completion_claim_allowed_not_false")
    if steps != ["authorization_intake"]:
        fail("blocked_runner_executed_unexpected_steps")
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
        "id": "agent-reach-p9-source-direct-live-closure-runner-readiness-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_live_closure_runner_readiness_pass",
        "current_admission": "limited_candidate_only",
        "mode": "blocked_probe_without_live_fetch",
        "runner": RUNNER.relative_to(ROOT).as_posix(),
        "runner_evidence": RUNNER_EVIDENCE.relative_to(ROOT).as_posix(),
        "probe": probe,
        "blocked_status": runner.get("status"),
        "blocked_steps": steps,
        "authorization_valid": runner.get("authorization_valid"),
        "execution_requested": runner.get("execution_requested"),
        "live_external_fetch_invoked": runner.get("live_external_fetch_invoked"),
        "completion_claim_allowed": runner.get("completion_claim_allowed"),
        "security_controls": runner.get("security_controls", {}),
        "non_claims": [
            "closure_runner_readiness_only",
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
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-CLOSURE-RUNNER-READINESS-20260626",
            "title: Agent-Reach P9S Source Direct Live Closure Runner Readiness 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-readiness-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-readiness-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Live Closure Runner Readiness 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- blocked_status: `{report['blocked_status']}`",
            f"- blocked_steps: `{report['blocked_steps']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence probes the closure runner without execute-live.",
            "- This evidence does not invoke live target-site fetch.",
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
        "agent_reach_p9_source_direct_live_closure_runner_readiness=pass "
        f"status={report['status']} blocked_status={report['blocked_status']} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
