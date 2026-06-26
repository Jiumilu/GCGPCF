#!/usr/bin/env python3
"""Validate Agent-Reach P9 live execution readiness closure."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-live-execution-readiness-closure-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-live-execution-readiness-closure-20260626.md"

CHECKS = [
    {
        "id": "coverage_plan",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_plan.py"],
        "required": "agent_reach_project_group_full_live_coverage_plan=pass",
    },
    {
        "id": "p9_precheck",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_priority_target_hit_rate_precheck.py"],
        "required": "agent_reach_p9_priority_target_hit_rate_precheck=pass",
    },
    {
        "id": "p9_runner_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_hit_rate_runner_readiness.py"],
        "required": "agent_reach_p9_hit_rate_runner_readiness=pass",
    },
    {
        "id": "p9_output_quality_gate",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_hit_rate_output_quality_gate.py", "--gate-readiness"],
        "required": "agent_reach_p9_hit_rate_output_quality_gate=pass",
    },
    {
        "id": "full_coverage_markdown_drift_monitor",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_full_coverage_markdown_drift_monitor.py"],
        "required": "agent_reach_full_coverage_markdown_drift_monitor=pass",
    },
    {
        "id": "p9_review_queue_bridge_readiness",
        "command": ["python3", "tools/kds-sync/validate_agent_reach_p9_review_queue_bridge_readiness.py"],
        "required": "agent_reach_p9_review_queue_bridge_readiness=pass",
    },
]

REQUIRED_EVIDENCE = {
    "p9_priority_target_hit_rate_precheck_ready": ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-precheck-20260626.json",
    "p9_hit_rate_runner_readiness_ready": ROOT / "docs/harness/evidence/agent-reach-p9-hit-rate-runner-readiness-20260626.json",
    "p9_hit_rate_output_quality_gate_ready": ROOT / "docs/harness/evidence/agent-reach-p9-hit-rate-output-quality-gate-20260626.json",
    "full_coverage_markdown_drift_monitor_pass": ROOT / "docs/harness/evidence/agent-reach-full-coverage-markdown-drift-monitor-20260626.json",
    "p9_review_queue_bridge_readiness_ready": ROOT / "docs/harness/evidence/agent-reach-p9-review-queue-bridge-readiness-20260626.json",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_live_execution_readiness_closure=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_check(check: dict[str, Any]) -> dict[str, Any]:
    proc = subprocess.run(
        check["command"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=120,
    )
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


def validate_evidence_statuses() -> dict[str, Any]:
    statuses: dict[str, Any] = {}
    for expected_status, path in REQUIRED_EVIDENCE.items():
        evidence = read_json(path)
        actual = evidence.get("status")
        if actual != expected_status:
            fail(f"evidence_status_mismatch:{path.relative_to(ROOT)}:{actual}")
        if evidence.get("live_external_search_invoked") is True:
            fail(f"unexpected_live_search_in_readiness_evidence:{path.relative_to(ROOT)}")
        statuses[path.relative_to(ROOT).as_posix()] = actual
    return statuses


def build_report() -> dict[str, Any]:
    check_results = [run_check(check) for check in CHECKS]
    failed = [item for item in check_results if not item["passed"]]
    if failed:
        fail("checks_failed:" + ",".join(item["id"] for item in failed))
    evidence_statuses = validate_evidence_statuses()
    return {
        "id": "agent-reach-p9-live-execution-readiness-closure-20260626",
        "date": "2026-06-26",
        "status": "p9_live_execution_readiness_closure_ready",
        "current_admission": "limited_candidate_only",
        "mode": "authorization_pre_execution_closure",
        "live_external_search_invoked": False,
        "agent_reach_binary_invoked": False,
        "authorization_required_before_live": True,
        "p9_live_run_completed": False,
        "completion_claim_allowed": False,
        "ready_components": [
            "priority_target_hit_rate_precheck",
            "query_expansion",
            "domain_boost_source_scoring",
            "runner_authorization_gate",
            "output_quality_gate",
            "markdown_drift_monitor",
            "review_queue_bridge_preview",
        ],
        "remaining_authorization_text": "授权执行 Agent-Reach P9 Priority Target Hit-Rate Live Run",
        "required_live_command_after_authorization": "python3 tools/kds-sync/run_agent_reach_p9_priority_target_hit_rate.py --auth fixtures/agent-reach/p9-priority-target-hit-rate-authorization.local.json --execute-live --write-evidence",
        "post_live_validation_commands": [
            "python3 tools/kds-sync/validate_agent_reach_p9_hit_rate_output_quality_gate.py --validate-report",
            "python3 tools/kds-sync/validate_agent_reach_p9_review_queue_bridge_readiness.py",
            "python3 tools/kds-sync/loop_document_gate.py",
        ],
        "check_results": check_results,
        "evidence_statuses": evidence_statuses,
        "non_claims": [
            "readiness_closure_only",
            "not_live_search_invoked",
            "not_p9_live_run_completed",
            "not_review_queue_created",
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
        "doc_id: GPCF-DOC-AGENT-REACH-P9-LIVE-EXECUTION-READINESS-CLOSURE-20260626",
        "title: Agent-Reach P9 Live Execution Readiness Closure 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-live-execution-readiness-closure-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-live-execution-readiness-closure-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9 Live Execution Readiness Closure 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- mode: `{report['mode']}`",
        f"- live_external_search_invoked: `{report['live_external_search_invoked']}`",
        f"- authorization_required_before_live: `{report['authorization_required_before_live']}`",
        f"- p9_live_run_completed: `{report['p9_live_run_completed']}`",
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
            "",
            "## Boundary",
            "",
            "- This evidence is readiness closure only.",
            "- This evidence does not invoke live search.",
            "- This evidence does not create review queue items.",
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
        "agent_reach_p9_live_execution_readiness_closure=pass "
        f"status={report['status']} checks={len(report['check_results'])} "
        "authorization_required_before_live=true live_external_search_invoked=false"
    )


if __name__ == "__main__":
    sys.exit(main())
