#!/usr/bin/env python3
"""Validate Agent-Reach P9R live rerun authorization request package."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-rerun-authorization.request.json"
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_p9_priority_target_hit_rate.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-rerun-authorization-request-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-rerun-authorization-request-20260626.md"

FORBIDDEN_ACTIONS = {
    "credential_write",
    "browser_cookie_extraction",
    "kds_canonical_write",
    "gfis_source_of_record_write",
    "production_config_write",
    "global_mcp_config_write",
    "production_integration",
    "accepted_claim",
    "integrated_claim",
    "production_ready_claim",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_rerun_authorization_request=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p9_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def positive_authorization() -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "authorization_id": "agent-reach-p9-priority-target-hit-rate-live-run",
        "authorization_status": "approved_for_p9_priority_target_hit_rate_live_run",
        "authorized_by": "lujunxiang",
        "authorized_at": (now - timedelta(minutes=1)).isoformat(),
        "expires_at": (now + timedelta(hours=2)).isoformat(),
        "allowed_channels": ["web", "rss", "bilibili"],
        "max_queries": 20,
        "max_results_per_query": 5,
        "allow_agent_reach_binary_invocation": False,
        "allow_external_network": True,
        "allow_write_evidence_only": True,
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "logging_redaction": {
            "redact_tokens": True,
            "redact_cookies": True,
            "redact_authorization_headers": True,
            "redact_query_personal_data": True,
            "persist_redacted_snippets_only": True,
        },
    }


def validate_runner_accepts_rerun_auth_path() -> None:
    runner = load_runner()
    with tempfile.TemporaryDirectory() as tmpdir:
        auth_path = Path(tmpdir) / "p9-rerun-auth.local.json"
        auth_path.write_text(json.dumps(positive_authorization(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report = runner.build_report(auth_path, execute=False)
    if report.get("authorization_valid") is not True:
        fail("runner_rejects_rerun_auth_path")
    if report.get("status") != "authorized_execution_not_requested":
        fail("runner_rerun_auth_execute_false_status_mismatch")
    if report.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("runner_rerun_auth_execute_false_invoked_live")


def validate_request(request: dict[str, Any]) -> None:
    if request.get("status") != "p9_priority_target_hit_rate_rerun_authorization_request_ready":
        fail("request_status_mismatch")
    if request.get("required_text") != "授权执行 Agent-Reach P9R Priority Target Hit-Rate Live Rerun":
        fail("required_text_mismatch")
    prior = load_json(ROOT / request["prior_rework_evidence"])
    if prior.get("status") != "p9_priority_target_hit_rate_rework_required":
        fail("prior_rework_status_mismatch")
    if prior.get("execution_requested") is not True:
        fail("prior_rework_not_executed")
    if prior.get("planned_query_count") != 20:
        fail("prior_rework_query_count_mismatch")
    repair = load_json(ROOT / request["repair_evidence"])
    if repair.get("status") != "p9_web_provider_fallback_offline_validated":
        fail("repair_evidence_status_mismatch")
    if repair.get("live_external_search_invoked") is not False:
        fail("repair_evidence_invoked_live")

    fields = request.get("required_authorization_fields", {})
    if fields.get("authorization_id") != "agent-reach-p9-priority-target-hit-rate-live-run":
        fail("authorization_id_mismatch")
    if fields.get("authorization_status") != "approved_for_p9_priority_target_hit_rate_live_run":
        fail("authorization_status_mismatch")
    if fields.get("max_queries") != 20:
        fail("max_queries_mismatch")
    if fields.get("max_results_per_query") != 5:
        fail("max_results_mismatch")
    if set(fields.get("allowed_channels", [])) != {"web", "rss", "bilibili"}:
        fail("allowed_channels_mismatch")
    if fields.get("allow_external_network") is not True:
        fail("external_network_not_allowed")
    if fields.get("allow_write_evidence_only") is not True:
        fail("write_scope_not_evidence_only")
    if fields.get("allow_agent_reach_binary_invocation") is not False:
        fail("binary_invocation_not_false")
    if not FORBIDDEN_ACTIONS <= set(fields.get("forbidden_actions", [])):
        fail("forbidden_actions_missing")
    for field in [
        "redact_tokens",
        "redact_cookies",
        "redact_authorization_headers",
        "redact_query_personal_data",
        "persist_redacted_snippets_only",
    ]:
        if fields.get("logging_redaction", {}).get(field) is not True:
            fail(f"redaction_not_true:{field}")
    scope = request.get("execution_scope", {})
    if scope.get("query_count") != 20 or scope.get("max_results_per_query") != 5:
        fail("execution_scope_limit_mismatch")
    if scope.get("rerun_after_repair") is not True:
        fail("rerun_after_repair_not_true")
    if request.get("rerun_output_json") != "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json":
        fail("rerun_output_json_mismatch")
    if request.get("rerun_output_md") != "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.md":
        fail("rerun_output_md_mismatch")
    command = request.get("runner_command_after_human_approval", "")
    for marker in [
        "--output-json docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json",
        "--output-md docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.md",
    ]:
        if marker not in command:
            fail(f"runner_command_missing:{marker}")
    post_live = request.get("post_live_validation_commands", [])
    if len(post_live) != 3:
        fail("post_live_validation_command_count_mismatch")
    if "--report docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json" not in post_live[0]:
        fail("post_live_output_gate_report_not_rerun")
    if "--markdown docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.md" not in post_live[0]:
        fail("post_live_output_gate_markdown_not_rerun")
    if "validate_agent_reach_p9_review_queue_bridge_readiness.py" not in post_live[1]:
        fail("post_live_review_bridge_missing")
    if "loop_document_gate.py" not in post_live[2]:
        fail("post_live_loop_gate_missing")
    for field in request.get("security_controls", {}):
        if request["security_controls"][field] is not False:
            fail(f"security_control_not_false:{field}")


def build_report() -> dict[str, Any]:
    request = load_json(REQUEST)
    validate_request(request)
    validate_runner_accepts_rerun_auth_path()
    return {
        "id": "agent-reach-p9-rerun-authorization-request-20260626",
        "date": "2026-06-26",
        "status": "p9_rerun_authorization_request_ready",
        "current_admission": "limited_candidate_only",
        "required_text": request["required_text"],
        "authorization_file_to_create_after_human_approval": request["authorization_file_to_create_after_human_approval"],
        "rerun_output_json": request["rerun_output_json"],
        "rerun_output_md": request["rerun_output_md"],
        "runner_command_after_human_approval": request["runner_command_after_human_approval"],
        "post_live_validation_commands": request["post_live_validation_commands"],
        "prior_rework_evidence": request["prior_rework_evidence"],
        "repair_evidence": request["repair_evidence"],
        "max_queries": request["required_authorization_fields"]["max_queries"],
        "max_results_per_query": request["required_authorization_fields"]["max_results_per_query"],
        "live_external_search_invoked": False,
        "runner_accepts_rerun_authorization_file": True,
        "non_claims": request["non_claims"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-RERUN-AUTHORIZATION-REQUEST-20260626",
            "title: Agent-Reach P9R Live Rerun 授权请求 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-rerun-authorization-request-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-rerun-authorization-request-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9R Live Rerun 授权请求 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- required_text: `{report['required_text']}`",
            f"- max_queries: `{report['max_queries']}`",
            f"- max_results_per_query: `{report['max_results_per_query']}`",
            f"- live_external_search_invoked: `{report['live_external_search_invoked']}`",
            f"- runner_accepts_rerun_authorization_file: `{report['runner_accepts_rerun_authorization_file']}`",
            f"- authorization_file: `{report['authorization_file_to_create_after_human_approval']}`",
            f"- rerun_output_json: `{report['rerun_output_json']}`",
            f"- rerun_output_md: `{report['rerun_output_md']}`",
            f"- runner_command: `{report['runner_command_after_human_approval']}`",
            "",
            "## Post-live validation",
            "",
            *[f"- `{command}`" for command in report["post_live_validation_commands"]],
            "",
            "## 边界",
            "",
            "- 本证据只准备 P9R rerun 授权请求。",
            "- 本证据不执行真实搜索。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_rerun_authorization_request=pass "
        f"status={report['status']} max_queries={report['max_queries']} "
        "live_external_search_invoked=false"
    )


if __name__ == "__main__":
    main()
