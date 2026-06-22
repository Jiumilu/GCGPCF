#!/usr/bin/env python3
"""Validate the Agent-Reach P7 live-search execution authorization gate."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
PLAN = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-preparation-20260622.json"
AUTH_TEMPLATE = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-authorization.template.json"
DEFAULT_AUTH = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-authorization-precheck-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p7-authorization-precheck-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-AUTHORIZATION-PRECHECK-001.md"

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
REQUIRED_REDACTION = {
    "redact_tokens",
    "redact_cookies",
    "redact_authorization_headers",
    "redact_query_personal_data",
    "persist_redacted_snippets_only",
}
PLACEHOLDER_RE = re.compile(r"<[^>]+>")
SECRET_RE = re.compile(r"(?i)(api[_-]?key|token|secret|authorization|cookie)[=:]\S+")


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p7_authorization_precheck=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def load_runner_module():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or PLACEHOLDER_RE.search(value):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def positive_authorization() -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        "authorization_id": "GPCF-AGENT-REACH-P7-LIVE-SEARCH-SELF-TEST",
        "authorization_status": "approved_for_p7_limited_live_search_dry_run",
        "authorized_by": "lujunxiang",
        "authorized_at": now.isoformat(),
        "expires_at": (now + timedelta(hours=2)).isoformat(),
        "allowed_channels": ["web", "rss", "bilibili"],
        "max_queries": 5,
        "max_results_per_query": 10,
        "allow_agent_reach_binary_invocation": False,
        "allow_external_network": True,
        "allow_write_evidence_only": True,
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "logging_redaction": {field: True for field in sorted(REQUIRED_REDACTION)},
    }


def write_temp_auth(auth: dict[str, Any]) -> Path:
    tmp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False)
    with tmp:
        json.dump(auth, tmp, ensure_ascii=False, indent=2, sort_keys=True)
        tmp.write("\n")
    return Path(tmp.name)


def validate_auth_object(auth: dict[str, Any], plan: dict[str, Any], runner_module, *, strict_time: bool = True) -> list[str]:
    reasons: list[str] = []
    tmp_path = write_temp_auth(auth)
    try:
        runner_ok, runner_reasons, _ = runner_module.validate_authorization(tmp_path, plan)
    finally:
        tmp_path.unlink(missing_ok=True)
    if not runner_ok:
        reasons.extend(runner_reasons)
    auth_text = json.dumps(auth, ensure_ascii=False, sort_keys=True)
    if PLACEHOLDER_RE.search(auth_text):
        reasons.append("authorization_contains_placeholder")
    if SECRET_RE.search(auth_text):
        reasons.append("authorization_contains_credential_like_text")
    if auth.get("authorization_status") != "approved_for_p7_limited_live_search_dry_run":
        reasons.append("authorization_status_not_approved")
    if not isinstance(auth.get("authorized_by"), str) or not auth["authorized_by"].strip():
        reasons.append("authorized_by_missing")
    authorized_at = parse_time(auth.get("authorized_at"))
    expires_at = parse_time(auth.get("expires_at"))
    if authorized_at is None:
        reasons.append("authorized_at_invalid_or_placeholder")
    if expires_at is None:
        reasons.append("expires_at_invalid_or_placeholder")
    if authorized_at and expires_at and expires_at <= authorized_at:
        reasons.append("expires_at_not_after_authorized_at")
    if strict_time and expires_at and datetime.now(timezone.utc) > expires_at.astimezone(timezone.utc):
        reasons.append("authorization_expired")
    if set(auth.get("allowed_channels", [])) != ALLOWED_CHANNELS:
        reasons.append("allowed_channels_mismatch")
    scope = plan.get("scope", {})
    if auth.get("max_queries") != scope.get("max_queries"):
        reasons.append("max_queries_mismatch")
    if auth.get("max_results_per_query") != scope.get("max_results_per_query"):
        reasons.append("max_results_per_query_mismatch")
    if auth.get("allow_agent_reach_binary_invocation") is not False:
        reasons.append("agent_reach_binary_invocation_not_allowed_for_current_gate")
    if auth.get("allow_external_network") is not True:
        reasons.append("external_network_not_allowed")
    if auth.get("allow_write_evidence_only") is not True:
        reasons.append("write_scope_not_evidence_only")
    if not FORBIDDEN_ACTIONS.issubset(set(auth.get("forbidden_actions", []))):
        reasons.append("forbidden_actions_missing")
    redaction = auth.get("logging_redaction", {})
    for field in sorted(REQUIRED_REDACTION):
        if redaction.get(field) is not True:
            reasons.append(f"redaction_not_true:{field}")
    return sorted(set(reasons))


def run_self_test(plan: dict[str, Any], runner_module) -> dict[str, Any]:
    cases: dict[str, tuple[dict[str, Any], str]] = {
        "missing-status": ({**positive_authorization(), "authorization_status": "pending_human_authorization"}, "authorization_status_not_approved"),
        "placeholder-time": ({**positive_authorization(), "authorized_at": "<required-iso8601>"}, "authorization_contains_placeholder"),
        "out-of-scope-channel": ({**positive_authorization(), "allowed_channels": ["web", "rss", "bilibili", "private"]}, "allowed_channels_out_of_scope"),
        "too-many-results": ({**positive_authorization(), "max_results_per_query": 11}, "max_results_per_query_mismatch"),
        "binary-allowed": ({**positive_authorization(), "allow_agent_reach_binary_invocation": True}, "agent_reach_binary_invocation_not_allowed_for_current_gate"),
    }
    positive_reasons = validate_auth_object(positive_authorization(), plan, runner_module)
    if positive_reasons:
        fail(f"self_test_positive_failed:{','.join(positive_reasons)}")
    negative_results = {}
    for name, (auth, expected) in cases.items():
        reasons = validate_auth_object(auth, plan, runner_module)
        if not any(reason.startswith(expected) or reason == expected for reason in reasons):
            fail(f"self_test_negative_failed:{name}:{','.join(reasons)}")
        negative_results[name] = {"expected": expected, "reasons": reasons}
    return {
        "positive_authorization_passed": True,
        "negative_cases": negative_results,
    }


def validate_default_missing_auth(runner_module) -> None:
    report = runner_module.build_report(DEFAULT_AUTH, execute=False)
    if report.get("status") != "blocked_pending_execution_authorization":
        fail("default_without_local_authorization_not_blocked")
    if "authorization_file_missing" not in report.get("authorization_reasons", []):
        fail("default_missing_authorization_reason_missing")
    if report.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("default_missing_authorization_invoked_live_search")


def validate_evidence(self_test: dict[str, Any]) -> None:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    if evidence.get("status") != "p7_authorization_precheck_ready":
        fail("evidence_status_mismatch")
    checks = evidence.get("precheck_checks", {})
    required_true = [
        "default_without_local_authorization_blocks",
        "requires_approved_p7_status",
        "requires_concrete_iso8601_window",
        "requires_allowed_channels_exactly_web_rss_bilibili",
        "requires_max_queries_5",
        "requires_max_results_per_query_10",
        "requires_agent_reach_binary_invocation_false",
        "requires_external_network_true",
        "requires_write_evidence_only_true",
        "requires_forbidden_actions_preserved",
        "requires_logging_redaction",
        "blocks_placeholder_authorization",
        "blocks_credential_like_authorization_text",
        "self_test_passed_without_network",
    ]
    for field in required_true:
        if checks.get(field) is not True:
            fail(f"precheck_check_not_true:{field}")
    if not self_test.get("positive_authorization_passed"):
        fail("self_test_not_passed")
    for marker in [
        "p7_authorization_precheck_ready",
        "authorization_file_missing",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", type=Path, help="Validate one concrete P7 authorization file")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory positive and negative authorization tests")
    args = parser.parse_args()
    plan = load_json(PLAN)
    runner_module = load_runner_module()
    if args.authorization:
        auth = load_json(args.authorization)
        reasons = validate_auth_object(auth, plan, runner_module)
        if reasons:
            fail(",".join(reasons))
        print(f"agent_reach_p7_authorization_precheck=pass authorization={args.authorization}")
        return
    self_test = run_self_test(plan, runner_module)
    validate_default_missing_auth(runner_module)
    if not args.self_test:
        validate_evidence(self_test)
    print(
        "agent_reach_p7_authorization_precheck=pass "
        "status=p7_authorization_precheck_ready "
        "default_without_local_authorization=blocked "
        "self_test=pass "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001"
    )


if __name__ == "__main__":
    main()
