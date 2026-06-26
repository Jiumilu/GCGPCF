#!/usr/bin/env python3
"""Build and validate Agent-Reach P9S source-direct live execution command pack."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
CLOSURE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-readiness-closure-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-command-pack-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-command-pack-20260626.md"

COMMANDS = [
    {
        "step": "authorization_intake",
        "command": "python3 tools/kds-sync/validate_agent_reach_p9_source_direct_live_authorization_intake.py",
        "live_external_fetch_invoked": False,
        "required_before_next": True,
    },
    {
        "step": "live_run",
        "command": "python3 tools/kds-sync/run_agent_reach_p9_source_direct_hit_rate.py --auth fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json --execute-live --write-evidence",
        "live_external_fetch_invoked": True,
        "required_before_next": True,
    },
    {
        "step": "output_quality_gate",
        "command": "python3 tools/kds-sync/validate_agent_reach_p9_source_direct_output_quality_gate.py --validate-report",
        "live_external_fetch_invoked": False,
        "required_before_next": True,
    },
    {
        "step": "review_queue_bridge_preview",
        "command": "python3 tools/kds-sync/validate_agent_reach_p9_source_direct_review_queue_bridge_readiness.py",
        "live_external_fetch_invoked": False,
        "required_before_next": True,
    },
    {
        "step": "document_control",
        "command": "python3 tools/kds-sync/document_control.py",
        "live_external_fetch_invoked": False,
        "required_before_next": True,
    },
    {
        "step": "loop_document_gate",
        "command": "python3 tools/kds-sync/loop_document_gate.py",
        "live_external_fetch_invoked": False,
        "required_before_next": True,
    },
]

CLOSURE_RUNNER_COMMAND = (
    "python3 tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py "
    "--execute-live --write-evidence"
)


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_live_execution_command_pack=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_sources(request: dict[str, Any], closure: dict[str, Any]) -> None:
    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("authorization_request_status_mismatch")
    if request.get("required_text") != "授权执行 Agent-Reach P9S Source Direct Hit-Rate Live Run":
        fail("required_text_mismatch")
    scope = request.get("execution_scope", {})
    if scope.get("max_targets") != 13:
        fail("max_targets_mismatch")
    if scope.get("max_entrypoints_per_target") != 3:
        fail("max_entrypoints_per_target_mismatch")
    if scope.get("max_pages_per_entrypoint") != 5:
        fail("max_pages_per_entrypoint_mismatch")
    if closure.get("status") != "p9_source_direct_live_execution_readiness_closure_ready":
        fail("closure_status_mismatch")
    if closure.get("completion_claim_allowed") is not False:
        fail("closure_completion_claim_not_false")
    if closure.get("live_external_fetch_invoked") is not False:
        fail("closure_live_fetch_not_false")


def validate_commands(request: dict[str, Any], closure: dict[str, Any]) -> None:
    steps = [command["step"] for command in COMMANDS]
    if steps != [
        "authorization_intake",
        "live_run",
        "output_quality_gate",
        "review_queue_bridge_preview",
        "document_control",
        "loop_document_gate",
    ]:
        fail("command_order_mismatch")
    live_commands = [command for command in COMMANDS if command["live_external_fetch_invoked"] is True]
    if len(live_commands) != 1 or live_commands[0]["step"] != "live_run":
        fail("live_command_scope_mismatch")
    expected_live = closure.get("required_live_command_after_authorization")
    if live_commands[0]["command"] != expected_live:
        fail("live_command_mismatch")
    auth_file = request.get("authorization_file_to_create_after_human_approval")
    if auth_file not in live_commands[0]["command"]:
        fail("authorization_file_not_referenced")
    for command in COMMANDS:
        if not command["command"].startswith("python3 tools/kds-sync/"):
            fail(f"command_path_out_of_scope:{command['step']}")
        if command["step"] != "live_run" and command["live_external_fetch_invoked"] is not False:
            fail(f"non_live_command_fetch_flag_mismatch:{command['step']}")
    if not (ROOT / "tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py").exists():
        fail("closure_runner_missing")


def build_report() -> dict[str, Any]:
    request = read_json(REQUEST)
    closure = read_json(CLOSURE)
    validate_sources(request, closure)
    validate_commands(request, closure)
    return {
        "id": "agent-reach-p9-source-direct-live-execution-command-pack-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_live_execution_command_pack_ready",
        "current_admission": "limited_candidate_only",
        "mode": "post_authorization_command_pack",
        "required_authorization_text": request["required_text"],
        "authorization_file": request["authorization_file_to_create_after_human_approval"],
        "authorization_intake_status": closure.get("authorization_intake_evidence", {}).get("status"),
        "completion_claim_allowed": False,
        "live_external_fetch_invoked": False,
        "commands": COMMANDS,
        "closure_runner_command": CLOSURE_RUNNER_COMMAND,
        "closure_runner_evidence": "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.json",
        "post_live_success_criteria": [
            "authorization_intake status is p9_source_direct_live_authorization_intake_ready",
            "live run status is p9_source_direct_hit_rate_completed",
            "output quality gate passes with --validate-report",
            "review queue bridge remains preview-only",
            "loop_document_gate passes",
        ],
        "non_claims": [
            "command_pack_only",
            "not_live_fetch_invoked",
            "not_live_run_completed",
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
        "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-EXECUTION-COMMAND-PACK-20260626",
        "title: Agent-Reach P9S Source Direct Live Execution Command Pack 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-execution-command-pack-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-execution-command-pack-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9S Source Direct Live Execution Command Pack 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- mode: `{report['mode']}`",
        f"- authorization_file: `{report['authorization_file']}`",
        f"- closure_runner_command: `{report['closure_runner_command']}`",
        f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
        f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
        "",
        "## Commands",
        "",
    ]
    for index, command in enumerate(report["commands"], start=1):
        lines.append(f"{index}. `{command['step']}`: `{command['command']}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This evidence is a command pack only.",
            "- This evidence does not invoke live target-site fetch.",
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
        "agent_reach_p9_source_direct_live_execution_command_pack=pass "
        f"status={report['status']} commands={len(report['commands'])} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
