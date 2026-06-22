#!/usr/bin/env python3
"""Validate the Agent-Reach P7 execution authorization request package."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-authorization.request.json"
LOCAL_AUTH = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json"
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
P7_AUTH_PRECHECK = ROOT / "docs/harness/evidence/agent-reach-p7-authorization-precheck-20260622.json"
READINESS_AUDIT = ROOT / "docs/harness/evidence/agent-reach-project-group-search-readiness-audit-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-execution-authorization-request-package-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p7-execution-authorization-request-package-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-EXECUTION-AUTHORIZATION-REQUEST-PACKAGE-001.md"

ALLOWED_CHANNELS = {"web", "rss", "bilibili"}
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
REDACTION_FIELDS = {
    "redact_tokens",
    "redact_cookies",
    "redact_authorization_headers",
    "redact_query_personal_data",
    "persist_redacted_snippets_only",
}
SECURITY_FALSE_FIELDS = [
    "agent_reach_binary_invoked",
    "live_external_search_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p7_execution_authorization_request_package=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def load_runner_report() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_report(LOCAL_AUTH, execute=False)


def validate_required_fields(fields: dict[str, Any]) -> None:
    if fields.get("authorization_status") != "approved_for_p7_limited_live_search_dry_run":
        fail("required_status_mismatch")
    if fields.get("authorized_by") != "lujunxiang":
        fail("required_authorized_by_mismatch")
    if set(fields.get("allowed_channels", [])) != ALLOWED_CHANNELS:
        fail("required_allowed_channels_mismatch")
    if fields.get("max_queries") != 5:
        fail("required_max_queries_mismatch")
    if fields.get("max_results_per_query") != 10:
        fail("required_max_results_per_query_mismatch")
    if fields.get("allow_agent_reach_binary_invocation") is not False:
        fail("binary_invocation_must_remain_false")
    if fields.get("allow_external_network") is not True:
        fail("external_network_not_requested")
    if fields.get("allow_write_evidence_only") is not True:
        fail("write_scope_not_evidence_only")
    if not FORBIDDEN_ACTIONS.issubset(set(fields.get("forbidden_actions", []))):
        fail("required_forbidden_actions_missing")
    redaction = fields.get("logging_redaction", {})
    for field in REDACTION_FIELDS:
        if redaction.get(field) is not True:
            fail(f"required_redaction_not_true:{field}")


def main() -> None:
    request = load_json(REQUEST)
    p7_auth_precheck = load_json(P7_AUTH_PRECHECK)
    readiness = load_json(READINESS_AUDIT)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    runner_report = load_runner_report()

    if request.get("required_text") != "授权执行 Agent-Reach P7 Limited Live Search Dry Run":
        fail("required_text_mismatch")
    if request.get("authorization_status") != "pending_human_authorization":
        fail("request_status_mismatch")
    if request.get("generated_local_authorization_file") is not False:
        fail("request_generated_local_auth_not_false")
    if request.get("execution_allowed_now") is not False:
        fail("request_execution_allowed_not_false")
    if request.get("authorization_file_to_create_after_human_approval") != "fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json":
        fail("local_auth_path_mismatch")
    validate_required_fields(request.get("required_authorization_fields", {}))
    if LOCAL_AUTH.exists():
        fail("local_authorization_file_exists_before_human_approval")
    if runner_report.get("status") != "blocked_pending_execution_authorization":
        fail("runner_default_not_blocked")
    if "authorization_file_missing" not in runner_report.get("authorization_reasons", []):
        fail("runner_missing_authorization_reason_absent")
    if runner_report.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("runner_live_search_invoked")
    if p7_auth_precheck.get("status") != "p7_authorization_precheck_ready":
        fail("p7_authorization_precheck_not_ready")
    if readiness.get("status") != "search_readiness_verified_pending_p7_authorization":
        fail("readiness_status_mismatch")

    if evidence.get("status") != "p7_execution_authorization_request_package_ready":
        fail("evidence_status_mismatch")
    if evidence.get("completion_claim_allowed") is not False:
        fail("completion_claim_allowed_not_false")
    checks = evidence.get("request_checks", {})
    for field in [
        "request_package_created",
        "required_text_fixed",
        "local_authorization_file_not_created",
        "default_runner_blocks_without_authorization",
        "required_fields_machine_validatable",
        "execution_command_documented_after_authorization",
    ]:
        if checks.get(field) is not True:
            fail(f"request_check_not_true:{field}")
    controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    for marker in [
        "p7_execution_authorization_request_package_ready",
        "authorization_file_missing",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p7_execution_authorization_request_package=pass "
        "status=p7_execution_authorization_request_package_ready "
        "local_authorization_file_created=false "
        "default_without_authorization=blocked "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001"
    )


if __name__ == "__main__":
    main()
