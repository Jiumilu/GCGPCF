#!/usr/bin/env python3
"""Validate Agent-Reach P4 live search authorization pack artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "fixtures/agent-reach/live-search-authorization-pack.template.json"
NEGATIVE_FIXTURES = ROOT / "fixtures/agent-reach/live-search-authorization-negative-fixtures.json"
AUTH_MD = ROOT / "third_party/agent-reach/LIVE_SEARCH_AUTHORIZATION.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001.md"

REQUIRED_TEMPLATE_FIELDS = {
    "authorization_id",
    "authorization_status",
    "live_search_authorized",
    "authorized_by",
    "authorized_at",
    "expires_at",
    "scope",
    "limits",
    "credential_boundary",
    "network_boundary",
    "logging_redaction",
    "rollback_plan",
    "acceptance_metrics",
    "evidence_output_paths",
    "non_claims",
}

FORBIDDEN_ACTIONS = {
    "credential_write",
    "browser_cookie_extraction",
    "kds_canonical_write",
    "gfis_source_of_record_write",
    "production_config_write",
    "global_mcp_config_write",
    "production_integration",
}

SECURITY_FALSE_FIELDS = [
    "agent_reach_binary_invoked",
    "live_external_search_invoked",
    "doctor_health_probe_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p4_live_search_authorization_pack=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def ensure_markers(text: str, markers: list[str], label: str) -> None:
    for marker in markers:
        if marker not in text:
            fail(f"{label}_missing:{marker}")


def main() -> None:
    template = load_json(TEMPLATE)
    negative = load_json(NEGATIVE_FIXTURES)
    evidence = load_json(EVIDENCE_JSON)
    auth_md = read_text(AUTH_MD)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    missing = sorted(REQUIRED_TEMPLATE_FIELDS - set(template))
    if missing:
        fail(f"template_missing_fields:{','.join(missing)}")
    if template.get("authorization_status") != "pending_human_authorization":
        fail("template_authorization_status_mismatch")
    if template.get("live_search_authorized") is not False:
        fail("template_live_search_authorized_not_false")
    scope = template.get("scope", {})
    if set(scope.get("forbidden_actions", [])) != FORBIDDEN_ACTIONS:
        fail("template_forbidden_actions_mismatch")
    if any(action in scope.get("allowed_actions", []) for action in FORBIDDEN_ACTIONS):
        fail("template_forbidden_action_allowed")
    if template.get("limits", {}).get("max_queries") != 5:
        fail("template_max_queries_mismatch")
    if template.get("limits", {}).get("dry_run_before_live") is not True:
        fail("template_dry_run_before_live_not_true")
    credential_boundary = template.get("credential_boundary", {})
    if credential_boundary.get("store_credentials") is not False:
        fail("template_store_credentials_not_false")
    if credential_boundary.get("write_env_files") is not False:
        fail("template_write_env_files_not_false")
    if credential_boundary.get("read_browser_cookies") is not False:
        fail("template_read_browser_cookies_not_false")
    if template.get("network_boundary", {}).get("external_network_allowed") is not False:
        fail("template_external_network_allowed_not_false")
    if template.get("network_boundary", {}).get("require_host_allowlist_before_live") is not True:
        fail("template_host_allowlist_not_required")
    redaction = template.get("logging_redaction", {})
    for field in ["redact_tokens", "redact_cookies", "redact_authorization_headers", "redact_query_personal_data"]:
        if redaction.get(field) is not True:
            fail(f"template_redaction_not_true:{field}")

    fixtures = negative.get("fixtures", [])
    if len(fixtures) != 8:
        fail("negative_fixture_count_mismatch")
    if negative.get("expected_decision") != "all_rejected":
        fail("negative_expected_decision_mismatch")
    for fixture in fixtures:
        if fixture.get("expected_decision") != "reject":
            fail(f"negative_fixture_not_rejected:{fixture.get('case_id')}")

    if evidence.get("status") != "live_search_authorization_pack_ready":
        fail("evidence_status_mismatch")
    if evidence.get("current_admission") != "limited_candidate_only":
        fail("evidence_current_admission_mismatch")
    if evidence.get("authorization_status") != "pending_human_authorization":
        fail("evidence_authorization_status_mismatch")
    if evidence.get("live_search_authorized") is not False:
        fail("evidence_live_search_authorized_not_false")
    checks = evidence.get("negative_fixture_checks", {})
    if checks.get("negative_fixture_count") != 8:
        fail("evidence_negative_fixture_count_mismatch")
    if checks.get("rejected_negative_fixtures") != 8:
        fail("evidence_rejected_negative_fixtures_mismatch")
    controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    if evidence.get("next_round") != "GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001":
        fail("evidence_next_round_mismatch")

    ensure_markers(
        auth_md,
        [
            "doc_id:",
            "status: controlled",
            "kds_space: 开发",
            "source_path: third_party/agent-reach/LIVE_SEARCH_AUTHORIZATION.md",
            "live_search_authorized | `false`",
            "不得执行真实搜索",
        ],
        "auth_md",
    )
    ensure_markers(
        evidence_md,
        [
            "不声明真实搜索已授权",
            "不声明真实搜索已调用",
            "不声明 accepted / integrated / production_ready",
        ],
        "evidence_md",
    )
    for section in ["输入", "动作", "输出", "检查", "反馈", "下一轮"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p4_live_search_authorization_pack=pass "
        "status=live_search_authorization_pack_ready "
        "authorization_status=pending_human_authorization "
        "live_search_authorized=false "
        "negative_fixture_count=8 "
        "rejected_negative_fixtures=8 "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
