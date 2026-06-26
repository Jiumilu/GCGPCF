#!/usr/bin/env python3
"""Validate Agent-Reach P9S source-direct live execution readiness closure."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-readiness-closure-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-readiness-closure-20260626.md"

CHECKS = [
    {
        "id": "coverage_plan",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_plan.py"],
        "required": "agent_reach_project_group_full_live_coverage_plan=pass",
    },
    {
        "id": "p9s_precheck",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_precheck.py"],
        "required": "agent_reach_p9_source_direct_precheck=pass",
    },
    {
        "id": "p9s_authorization_request",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_authorization_request.py"],
        "required": "agent_reach_p9_source_direct_authorization_request=pass",
    },
    {
        "id": "p9s_live_authorization_intake",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_authorization_intake.py"],
        "required": "agent_reach_p9_source_direct_live_authorization_intake=pass",
    },
    {
        "id": "p9s_authorization_file_safety",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_authorization_file_safety.py"],
        "required": "agent_reach_p9_source_direct_authorization_file_safety=pass",
    },
    {
        "id": "p9s_runner_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_runner_readiness.py"],
        "required": "agent_reach_p9_source_direct_runner_readiness=pass",
    },
    {
        "id": "p9s_output_quality_gate",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_output_quality_gate.py", "--gate-readiness"],
        "required": "agent_reach_p9_source_direct_output_quality_gate=pass",
    },
    {
        "id": "p9s_review_queue_bridge_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_review_queue_bridge_readiness.py"],
        "required": "agent_reach_p9_source_direct_review_queue_bridge_readiness=pass",
    },
    {
        "id": "p9s_live_execution_command_pack",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_execution_command_pack.py"],
        "required": "agent_reach_p9_source_direct_live_execution_command_pack=pass",
    },
    {
        "id": "p9s_live_closure_runner_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_closure_runner_readiness.py"],
        "required": "agent_reach_p9_source_direct_live_closure_runner_readiness=pass",
    },
    {
        "id": "p9s_live_closure_authorization_gate",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_live_closure_authorization_gate.py"],
        "required": "agent_reach_p9_source_direct_live_closure_authorization_gate=pass",
    },
    {
        "id": "p9_objective_post_live_path_simulation",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_objective_post_live_path_simulation.py"],
        "required": "agent_reach_p9_objective_post_live_path_simulation=pass",
    },
    {
        "id": "p9s_authorization_handoff_pack",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_source_direct_authorization_handoff_pack.py"],
        "required": "agent_reach_p9_source_direct_authorization_handoff_pack=pass",
    },
    {
        "id": "full_coverage_markdown_drift_monitor",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_full_coverage_markdown_drift_monitor.py"],
        "required": "agent_reach_full_coverage_markdown_drift_monitor=pass",
    },
]

REQUIRED_EVIDENCE = {
    "p9_source_direct_precheck_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-precheck-20260626.json",
    "p9_source_direct_authorization_request_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-request-20260626.json",
    "p9_source_direct_runner_readiness_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-runner-readiness-20260626.json",
    "p9_source_direct_output_quality_gate_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-output-quality-gate-20260626.json",
    "p9_source_direct_review_queue_bridge_readiness_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626.json",
    "p9_source_direct_live_execution_command_pack_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-command-pack-20260626.json",
    "p9_source_direct_authorization_file_safety_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-file-safety-20260626.json",
    "p9_source_direct_live_closure_runner_readiness_pass": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-readiness-20260626.json",
    "p9_source_direct_live_closure_authorization_gate_pass": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-authorization-gate-20260626.json",
    "p9_objective_post_live_path_simulation_pass": ROOT / "docs/harness/evidence/agent-reach-p9-objective-post-live-path-simulation-20260626.json",
    "p9_source_direct_authorization_handoff_pack_ready": ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-handoff-pack-20260626.json",
}
AUTHORIZATION_INTAKE_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-authorization-intake-20260626.json"
BLOCKED_LIVE_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.json"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_live_execution_readiness_closure=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_check(check: dict[str, Any]) -> dict[str, Any]:
    proc = subprocess.run(check["command"], cwd=ROOT, text=True, capture_output=True, timeout=120)
    output = (proc.stdout + proc.stderr).strip()
    passed = proc.returncode == 0 and check["required"] in output
    return {
        "id": check["id"],
        "command": " ".join(check["command"]),
        "returncode": proc.returncode,
        "required": check["required"],
        "passed": passed,
        "output_tail": output[-600:],
    }


def validate_readiness_evidence() -> dict[str, str]:
    statuses: dict[str, str] = {}
    for expected_status, path in REQUIRED_EVIDENCE.items():
        evidence = read_json(path)
        actual = evidence.get("status")
        if actual != expected_status:
            fail(f"evidence_status_mismatch:{path.relative_to(ROOT)}:{actual}")
        if evidence.get("live_external_fetch_invoked") is True:
            fail(f"unexpected_live_fetch_in_readiness_evidence:{path.relative_to(ROOT)}")
        statuses[path.relative_to(ROOT).as_posix()] = actual
    return statuses


def validate_authorization_intake() -> dict[str, Any]:
    evidence = read_json(AUTHORIZATION_INTAKE_EVIDENCE)
    status = evidence.get("status")
    if status not in {"blocked_pending_p9_source_direct_authorization", "p9_source_direct_live_authorization_intake_ready"}:
        fail(f"authorization_intake_status_mismatch:{status}")
    if evidence.get("live_external_fetch_invoked") is not False:
        fail("authorization_intake_live_fetch_not_false")
    if status == "blocked_pending_p9_source_direct_authorization":
        if evidence.get("authorization_valid") is not False:
            fail("authorization_intake_pending_valid_not_false")
        if evidence.get("ready_for_live_execution") is not False:
            fail("authorization_intake_pending_ready_not_false")
    if status == "p9_source_direct_live_authorization_intake_ready":
        if evidence.get("authorization_valid") is not True:
            fail("authorization_intake_ready_valid_not_true")
        if evidence.get("ready_for_live_execution") is not True:
            fail("authorization_intake_ready_not_true")
    return {
        "path": AUTHORIZATION_INTAKE_EVIDENCE.relative_to(ROOT).as_posix(),
        "status": status,
        "authorization_valid": evidence.get("authorization_valid"),
        "ready_for_live_execution": evidence.get("ready_for_live_execution"),
        "live_external_fetch_invoked": evidence.get("live_external_fetch_invoked"),
    }


def validate_blocked_live_evidence() -> dict[str, Any]:
    evidence = read_json(BLOCKED_LIVE_EVIDENCE)
    if evidence.get("status") != "blocked_pending_p9_source_direct_authorization":
        fail(f"blocked_live_status_mismatch:{evidence.get('status')}")
    if evidence.get("authorization_valid") is not False:
        fail("blocked_live_authorization_not_false")
    if evidence.get("execution_requested") is not False:
        fail("blocked_live_execution_requested_not_false")
    if evidence.get("security_controls", {}).get("live_external_fetch_invoked") is not False:
        fail("blocked_live_fetch_invoked_not_false")
    if evidence.get("hit_rate_report", {}).get("threshold_pass") is not False:
        fail("blocked_live_threshold_not_false")
    return {
        "path": BLOCKED_LIVE_EVIDENCE.relative_to(ROOT).as_posix(),
        "status": evidence["status"],
        "authorization_valid": evidence["authorization_valid"],
        "execution_requested": evidence["execution_requested"],
        "live_external_fetch_invoked": evidence["security_controls"]["live_external_fetch_invoked"],
        "threshold_pass": evidence["hit_rate_report"]["threshold_pass"],
    }


def build_report() -> dict[str, Any]:
    check_results = [run_check(check) for check in CHECKS]
    failed = [item for item in check_results if not item["passed"]]
    if failed:
        fail("checks_failed:" + ",".join(item["id"] for item in failed))
    evidence_statuses = validate_readiness_evidence()
    authorization_intake = validate_authorization_intake()
    blocked_live = validate_blocked_live_evidence()
    return {
        "id": "agent-reach-p9-source-direct-live-execution-readiness-closure-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_live_execution_readiness_closure_ready",
        "current_admission": "limited_candidate_only",
        "mode": "authorization_pre_execution_closure",
        "live_external_fetch_invoked": False,
        "agent_reach_binary_invoked": False,
        "authorization_required_before_live": True,
        "p9_source_direct_live_run_completed": False,
        "completion_claim_allowed": False,
        "ready_components": [
            "source_direct_precheck",
            "source_direct_authorization_request",
            "source_direct_live_authorization_intake",
            "source_direct_authorization_file_safety",
            "source_direct_runner_authorization_gate",
            "source_direct_same_domain_discovery",
            "source_direct_charset_fallback",
            "source_direct_redirect_guard",
            "source_direct_login_guard",
            "source_direct_content_type_guard",
            "source_direct_transient_retry_policy",
            "source_direct_output_quality_gate",
            "source_direct_review_queue_bridge_preview",
            "source_direct_live_execution_command_pack",
            "source_direct_live_closure_runner_readiness",
            "source_direct_live_closure_authorization_gate",
            "source_direct_authorization_handoff_pack",
            "p9_objective_post_live_path_simulation",
            "source_direct_blocked_live_placeholder",
            "full_coverage_markdown_drift_monitor",
        ],
        "remaining_authorization_text": "授权执行 Agent-Reach P9S Source Direct Hit-Rate Live Run",
        "required_live_command_after_authorization": "python3 tools/kds-sync/run_agent_reach_p9_source_direct_hit_rate.py --auth fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json --execute-live --write-evidence",
        "required_closure_command_after_authorization": "python3 tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py --execute-live --write-evidence",
        "post_live_validation_commands": [
            "python3 tools/kds-sync/validate_agent_reach_p9_source_direct_output_quality_gate.py --validate-report",
            "python3 tools/kds-sync/validate_agent_reach_p9_objective_completion_audit.py",
            "python3 tools/kds-sync/loop_document_gate.py",
        ],
        "check_results": check_results,
        "evidence_statuses": evidence_statuses,
        "authorization_intake_evidence": authorization_intake,
        "blocked_live_evidence": blocked_live,
        "non_claims": [
            "readiness_closure_only",
            "not_live_fetch_invoked",
            "not_p9_source_direct_live_run_completed",
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
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-EXECUTION-READINESS-CLOSURE-20260626",
        "title: Agent-Reach P9S Source Direct Live Execution Readiness Closure 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-execution-readiness-closure-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-execution-readiness-closure-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct Live Execution Readiness Closure 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- mode: `{report['mode']}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        f"- authorization_required_before_live: `{report['authorization_required_before_live']}`",
        f"- p9_source_direct_live_run_completed: `{report['p9_source_direct_live_run_completed']}`",
        f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
        "",
        "## Ready Components",
        "",
    ]
    for component in report["ready_components"]:
        lines.append(f"- `{component}`")
    lines.extend(
        [
            "",
            "## Remaining Authorization",
            "",
        f"- required_text: `{report['remaining_authorization_text']}`",
        f"- live_command_after_authorization: `{report['required_live_command_after_authorization']}`",
        f"- closure_command_after_authorization: `{report['required_closure_command_after_authorization']}`",
        "",
            "## Boundary",
            "",
            "- This evidence is readiness closure only.",
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
        "agent_reach_p9_source_direct_live_execution_readiness_closure=pass "
        f"status={report['status']} checks={len(report['check_results'])} "
        "authorization_required_before_live=true live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    sys.exit(main())
