#!/usr/bin/env python3
"""Validate Agent-Reach P9 hit-rate runner and authorization request readiness."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-authorization.request.json"
PRECHECK = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-precheck-20260626.json"
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_p9_priority_target_hit_rate.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-hit-rate-runner-readiness-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-hit-rate-runner-readiness-20260626.md"

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
    raise SystemExit(f"agent_reach_p9_hit_rate_runner_readiness=fail reason={message}")


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


def positive_authorization(query_count: int) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "authorization_id": "agent-reach-p9-priority-target-hit-rate-live-run",
        "authorization_status": "approved_for_p9_priority_target_hit_rate_live_run",
        "authorized_by": "lujunxiang",
        "authorized_at": (now - timedelta(minutes=1)).isoformat(),
        "expires_at": (now + timedelta(hours=2)).isoformat(),
        "allowed_channels": ["web", "rss", "bilibili"],
        "max_queries": query_count,
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


def validate_request(request: dict[str, Any], query_count: int) -> None:
    if request.get("status") != "p9_priority_target_hit_rate_authorization_request_ready":
        fail("request_status_mismatch")
    if request.get("required_text") != "授权执行 Agent-Reach P9 Priority Target Hit-Rate Live Run":
        fail("request_required_text_mismatch")
    fields = request.get("required_authorization_fields", {})
    if fields.get("authorization_status") != "approved_for_p9_priority_target_hit_rate_live_run":
        fail("request_authorization_status_mismatch")
    if fields.get("max_queries") != query_count:
        fail("request_max_queries_mismatch")
    if fields.get("max_results_per_query") != 5:
        fail("request_max_results_mismatch")
    if fields.get("allow_external_network") is not True:
        fail("request_external_network_not_true")
    if fields.get("allow_write_evidence_only") is not True:
        fail("request_write_scope_not_evidence_only")
    if fields.get("allow_agent_reach_binary_invocation") is not False:
        fail("request_binary_invocation_not_false")
    if not FORBIDDEN_ACTIONS.issubset(set(fields.get("forbidden_actions", []))):
        fail("request_forbidden_actions_missing")
    controls = request.get("security_controls", {})
    for field in [
        "live_external_search_invoked",
        "credential_written",
        "browser_cookie_extraction_invoked",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "production_config_write_allowed",
        "global_mcp_config_write_allowed",
        "production_integration_allowed",
    ]:
        if controls.get(field) is not False:
            fail(f"request_security_control_not_false:{field}")


def build_report() -> dict[str, Any]:
    request = load_json(REQUEST)
    precheck = load_json(PRECHECK)
    runner = load_runner()
    query_count = len(runner.planned_queries(precheck))
    validate_request(request, query_count)

    blocked = runner.build_report(ROOT / "fixtures/agent-reach/nonexistent-p9-auth.local.json", execute=False)
    if blocked.get("status") != "blocked_pending_p9_live_authorization":
        fail("missing_auth_not_blocked")
    if blocked.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("missing_auth_invoked_live_search")

    with tempfile.TemporaryDirectory() as tmpdir:
        auth_path = Path(tmpdir) / "p9-auth.local.json"
        auth_path.write_text(json.dumps(positive_authorization(query_count), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        authorized = runner.build_report(auth_path, execute=False)
    if authorized.get("status") != "authorized_execution_not_requested":
        fail("authorized_without_execute_status_mismatch")
    if authorized.get("authorization_valid") is not True:
        fail("temp_authorization_not_valid")
    if authorized.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("authorized_without_execute_invoked_live_search")

    return {
        "id": "agent-reach-p9-hit-rate-runner-readiness-20260626",
        "date": "2026-06-26",
        "status": "p9_hit_rate_runner_readiness_ready",
        "current_admission": "limited_candidate_only",
        "query_count": query_count,
        "authorization_request_ready": True,
        "runner_blocks_without_authorization": True,
        "runner_does_not_execute_live_without_execute_flag": True,
        "live_external_search_invoked": False,
        "required_text": request["required_text"],
        "next_authorization_file": request["authorization_file_to_create_after_human_approval"],
        "non_claims": [
            "runner_readiness_only",
            "not_live_search_invoked",
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
            "doc_id: GPCF-DOC-AGENT-REACH-P9-HIT-RATE-RUNNER-READINESS-20260626",
            "title: Agent-Reach P9 命中率 Runner 就绪证据 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-hit-rate-runner-readiness-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-hit-rate-runner-readiness-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9 命中率 Runner 就绪证据 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- query_count: `{report['query_count']}`",
            f"- authorization_request_ready: `{report['authorization_request_ready']}`",
            f"- runner_blocks_without_authorization: `{report['runner_blocks_without_authorization']}`",
            f"- runner_does_not_execute_live_without_execute_flag: `{report['runner_does_not_execute_live_without_execute_flag']}`",
            f"- live_external_search_invoked: `{report['live_external_search_invoked']}`",
            f"- required_text: `{report['required_text']}`",
            f"- next_authorization_file: `{report['next_authorization_file']}`",
            "",
            "## 边界",
            "",
            "- 本证据只证明 P9 runner 和授权请求就绪。",
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
        "agent_reach_p9_hit_rate_runner_readiness=pass "
        f"status={report['status']} query_count={report['query_count']} "
        "live_external_search_invoked=false"
    )


if __name__ == "__main__":
    main()
