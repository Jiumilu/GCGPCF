#!/usr/bin/env python3
"""Validate Agent-Reach P5B corrected authorization precheck artifacts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "fixtures/agent-reach/live-search-precheck-corrected-authorization-20260622.json"
P5_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p5-live-search-precheck-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p5b-live-search-precheck-corrected-authorization-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p5b-live-search-precheck-corrected-authorization-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001.md"

ALLOWED_CHANNELS = {"web", "rss", "bilibili"}
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
    raise SystemExit(f"agent_reach_p5b_live_search_precheck_corrected_authorization=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def parse_iso8601(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        fail(f"invalid_iso8601:{value}")
        raise exc


def main() -> None:
    submission = load_json(SUBMISSION)
    p5 = load_json(P5_EVIDENCE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    if p5.get("status") != "live_search_precheck_rejected":
        fail("p5_evidence_not_rejected")
    if p5.get("live_search_authorized") is not False:
        fail("p5_live_search_authorized_not_false")

    auth_text = submission.get("authorization_text", {})
    parsed = submission.get("parsed_authorization", {})
    if auth_text.get("authorized_by") != "lujunxiang":
        fail("authorized_by_mismatch")
    if set(auth_text.get("allowed_channels", [])) != ALLOWED_CHANNELS:
        fail("allowed_channels_mismatch")
    if auth_text.get("max_queries") != 5:
        fail("max_queries_mismatch")
    if auth_text.get("max_results_per_query") != 10:
        fail("max_results_per_query_mismatch")
    if not FORBIDDEN_ACTIONS.issubset(set(auth_text.get("forbidden_actions", []))):
        fail("forbidden_actions_missing")
    if auth_text.get("precheck_required_before_live") is not True:
        fail("precheck_required_not_true")

    authorized_at = parse_iso8601(parsed.get("authorized_at", ""))
    expires_at = parse_iso8601(parsed.get("expires_at", ""))
    if expires_at <= authorized_at:
        fail("expires_at_not_after_authorized_at")
    duration_seconds = (expires_at - authorized_at).total_seconds()
    if duration_seconds <= 86400:
        fail("expected_watch_window_exceeds_one_day")
    result = submission.get("precheck_result", {})
    if result.get("decision") != "pass_with_watch":
        fail("submission_decision_not_pass_with_watch")
    if "authorization_window_exceeds_one_day" not in result.get("watch_reasons", []):
        fail("submission_watch_reason_missing")
    if result.get("live_external_search_invoked") is not False:
        fail("submission_live_search_invoked_not_false")
    if result.get("agent_reach_binary_invoked") is not False:
        fail("submission_binary_invoked_not_false")

    if evidence.get("status") != "live_search_precheck_pass_with_watch":
        fail("evidence_status_mismatch")
    if evidence.get("current_admission") != "limited_candidate_only":
        fail("evidence_current_admission_mismatch")
    if evidence.get("authorization_status") != "corrected_authorization_precheck_passed":
        fail("evidence_authorization_status_mismatch")
    if evidence.get("precheck_decision") != "pass_with_watch":
        fail("evidence_precheck_decision_mismatch")
    if evidence.get("live_search_authorized") is not False:
        fail("evidence_live_search_authorized_not_false")
    if evidence.get("live_search_authorized_for_next_round_candidate") is not True:
        fail("evidence_next_round_candidate_not_true")
    if "authorization_window_exceeds_one_day" not in evidence.get("watch_reasons", []):
        fail("evidence_watch_reason_missing")
    accepted = evidence.get("accepted_controls", {})
    for field in [
        "authorized_by_present",
        "authorized_at_concrete_iso8601",
        "expires_at_concrete_iso8601",
        "expires_at_after_authorized_at",
        "allowed_channels_within_p4_boundary",
        "max_queries_within_limit",
        "max_results_per_query_within_limit",
        "forbidden_actions_preserved",
        "precheck_before_live_required",
    ]:
        if accepted.get(field) is not True:
            fail(f"accepted_control_not_true:{field}")
    controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    if evidence.get("next_round") != "GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001":
        fail("next_round_mismatch")

    for marker in [
        "live_search_precheck_pass_with_watch",
        "`2026-06-22T20:00:00+08:00`",
        "`2027-06-22T21:00:00+08:00`",
        "authorization_window_exceeds_one_day",
        "不声明真实搜索已调用",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p5b_live_search_precheck_corrected_authorization=pass "
        "status=live_search_precheck_pass_with_watch "
        "precheck_decision=pass_with_watch "
        "watch=authorization_window_exceeds_one_day "
        "live_search_authorized=false "
        "live_external_search_invoked=false "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
