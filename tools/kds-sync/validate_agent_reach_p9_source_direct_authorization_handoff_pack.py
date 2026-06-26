#!/usr/bin/env python3
"""Validate the P9S source-direct authorization handoff pack."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
TEMPLATE = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.template.json"
FILE_SAFETY = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-file-safety-20260626.json"
COMMAND_PACK = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-command-pack-20260626.json"
CLOSURE_AUTH_GATE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-authorization-gate-20260626.json"
POST_LIVE_SIM = ROOT / "docs/harness/evidence/agent-reach-p9-objective-post-live-path-simulation-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-handoff-pack-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-handoff-pack-20260626.md"

REQUIRED_AUTH_TEXT = "授权执行 Agent-Reach P9S Source Direct Hit-Rate Live Run"
LOCAL_AUTH = "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json"
CLOSURE_COMMAND = "python3 tools/kds-sync/run_agent_reach_p9_source_direct_live_closure.py --execute-live --write-evidence"
ALLOWED_METHODS = [
    "target_url",
    "sitemap",
    "rss",
    "public_list_page",
    "site_search_endpoint_without_credentials",
]
FORBIDDEN_ACTIONS = [
    "credential_write",
    "browser_cookie_extraction",
    "credentialed_api",
    "login_required_page",
    "kds_canonical_write",
    "gfis_source_of_record_write",
    "production_config_write",
    "global_mcp_config_write",
    "production_integration",
    "accepted_claim",
    "integrated_claim",
    "production_ready_claim",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_authorization_handoff_pack=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_no_boundary_violation(*payloads: dict[str, Any]) -> None:
    for payload in payloads:
        controls = payload.get("security_controls", {})
        for field in [
            "credential_written",
            "browser_cookie_extraction_invoked",
            "kds_canonical_write_allowed",
            "gfis_source_of_record_write_allowed",
            "production_config_write_allowed",
            "global_mcp_config_write_allowed",
            "production_integration_allowed",
        ]:
            if controls.get(field) is True:
                fail(f"boundary_violation:{field}")
        if payload.get("completion_claim_allowed") is True:
            fail("completion_claim_allowed_detected")


def build_report() -> dict[str, Any]:
    request = read_json(REQUEST)
    template = read_json(TEMPLATE)
    file_safety = read_json(FILE_SAFETY)
    command_pack = read_json(COMMAND_PACK)
    closure_gate = read_json(CLOSURE_AUTH_GATE)
    post_live = read_json(POST_LIVE_SIM)
    validate_no_boundary_violation(request, file_safety, command_pack, closure_gate, post_live)

    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("request_not_ready")
    if request.get("required_text") != REQUIRED_AUTH_TEXT:
        fail("required_text_mismatch")
    if request.get("authorization_file_to_create_after_human_approval") != LOCAL_AUTH:
        fail("local_auth_path_mismatch")
    scope = request.get("execution_scope", {})
    if scope.get("max_targets") != 13 or scope.get("max_entrypoints_per_target") != 3 or scope.get("max_pages_per_entrypoint") != 5:
        fail("scope_limit_mismatch")
    if scope.get("allowed_methods") != ALLOWED_METHODS:
        fail("allowed_methods_mismatch")
    if scope.get("public_read_only") is not True or scope.get("write_evidence_only") is not True:
        fail("scope_boundary_mismatch")
    fields = request.get("required_authorization_fields", {})
    if fields.get("forbidden_actions") != FORBIDDEN_ACTIONS:
        fail("forbidden_actions_mismatch")
    if template.get("authorized_by") != "<required-human-name>":
        fail("template_authorized_by_placeholder_mismatch")
    if file_safety.get("status") != "p9_source_direct_authorization_file_safety_ready":
        fail("file_safety_not_ready")
    if file_safety.get("local_authorization_file_git_ignored") is not True:
        fail("local_authorization_file_not_git_ignored")
    if file_safety.get("template_authorization_valid") is not False:
        fail("template_authorization_valid")
    if command_pack.get("status") != "p9_source_direct_live_execution_command_pack_ready":
        fail("command_pack_not_ready")
    if command_pack.get("closure_runner_command") != CLOSURE_COMMAND:
        fail("closure_runner_command_mismatch")
    if closure_gate.get("status") != "p9_source_direct_live_closure_authorization_gate_pass":
        fail("closure_authorization_gate_not_pass")
    if closure_gate.get("execution_requested") is not True or closure_gate.get("live_external_fetch_invoked") is not False:
        fail("closure_authorization_gate_boundary_mismatch")
    synthetic = post_live.get("synthetic_result", {})
    if post_live.get("status") != "p9_objective_post_live_path_simulation_pass":
        fail("post_live_path_simulation_not_pass")
    if synthetic.get("source_direct_execution_mode") != "post_live_closure_completed":
        fail("post_live_execution_mode_mismatch")

    return {
        "id": "agent-reach-p9-source-direct-authorization-handoff-pack-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_authorization_handoff_pack_ready",
        "current_admission": "limited_candidate_only",
        "required_authorization_text": REQUIRED_AUTH_TEXT,
        "authorization_file_to_create_after_human_approval": LOCAL_AUTH,
        "closure_runner_command_after_authorization": CLOSURE_COMMAND,
        "execution_scope": scope,
        "required_authorization_fields": fields,
        "readiness_evidence": {
            "authorization_request": REQUEST.relative_to(ROOT).as_posix(),
            "authorization_template": TEMPLATE.relative_to(ROOT).as_posix(),
            "authorization_file_safety": FILE_SAFETY.relative_to(ROOT).as_posix(),
            "command_pack": COMMAND_PACK.relative_to(ROOT).as_posix(),
            "closure_authorization_gate": CLOSURE_AUTH_GATE.relative_to(ROOT).as_posix(),
            "post_live_path_simulation": POST_LIVE_SIM.relative_to(ROOT).as_posix(),
        },
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
            "authorization_handoff_only",
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
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-AUTH-HANDOFF-20260626",
            "title: Agent-Reach P9S Source Direct Authorization Handoff Pack 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-authorization-handoff-pack-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-authorization-handoff-pack-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Authorization Handoff Pack 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- required_authorization_text: `{report['required_authorization_text']}`",
            f"- authorization_file: `{report['authorization_file_to_create_after_human_approval']}`",
            f"- closure_runner_command: `{report['closure_runner_command_after_authorization']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence is an authorization handoff pack only.",
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
        "agent_reach_p9_source_direct_authorization_handoff_pack=pass "
        f"status={report['status']} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
