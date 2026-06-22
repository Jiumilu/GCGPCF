#!/usr/bin/env python3
"""Validate Agent-Reach P5 live search precheck rejection artifacts."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "fixtures/agent-reach/live-search-precheck-authorization-submission-20260622.json"
P4_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p5-live-search-precheck-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p5-live-search-precheck-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001.md"

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
PLACEHOLDER_RE = re.compile(r"<[^>]+>")
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
    raise SystemExit(f"agent_reach_p5_live_search_precheck=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def is_concrete_iso8601(value: str) -> bool:
    if PLACEHOLDER_RE.search(value):
        return False
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def main() -> None:
    submission = load_json(SUBMISSION)
    p4 = load_json(P4_EVIDENCE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    if p4.get("status") != "live_search_authorization_pack_ready":
        fail("p4_evidence_not_ready")
    if p4.get("live_search_authorized") is not False:
        fail("p4_live_search_authorized_not_false")

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

    authorized_at = parsed.get("authorized_at", "")
    expires_at = parsed.get("expires_at", "")
    if is_concrete_iso8601(authorized_at):
        fail("authorized_at_should_be_rejected")
    if is_concrete_iso8601(expires_at):
        fail("expires_at_should_be_rejected")
    result = submission.get("precheck_result", {})
    if result.get("decision") != "reject":
        fail("submission_decision_not_reject")
    if result.get("reason") != "authorization_window_contains_placeholders":
        fail("submission_rejection_reason_mismatch")
    if result.get("live_external_search_invoked") is not False:
        fail("submission_live_search_invoked_not_false")
    if result.get("agent_reach_binary_invoked") is not False:
        fail("submission_binary_invoked_not_false")

    if evidence.get("status") != "live_search_precheck_rejected":
        fail("evidence_status_mismatch")
    if evidence.get("current_admission") != "limited_candidate_only":
        fail("evidence_current_admission_mismatch")
    if evidence.get("authorization_status") != "rejected_missing_concrete_time_window":
        fail("evidence_authorization_status_mismatch")
    if evidence.get("live_search_authorized") is not False:
        fail("evidence_live_search_authorized_not_false")
    if evidence.get("precheck_decision") != "reject":
        fail("evidence_precheck_decision_not_reject")
    for reason in ["authorized_at_contains_placeholder", "expires_at_contains_placeholder"]:
        if reason not in evidence.get("rejection_reasons", []):
            fail(f"missing_rejection_reason:{reason}")
    failed = evidence.get("failed_controls", {})
    for field in ["authorized_at_concrete_iso8601", "expires_at_concrete_iso8601", "expires_at_after_authorized_at"]:
        if failed.get(field) is not False:
            fail(f"failed_control_not_false:{field}")
    controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    if evidence.get("next_round") != "GPCF-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001":
        fail("next_round_mismatch")

    for marker in [
        "live_search_precheck_rejected",
        "`2026-06-22T<开始时间>+08:00`",
        "`2026-06-22T<结束时间>+08:00`",
        "不声明真实搜索已授权",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["输入", "动作", "输出", "检查", "反馈", "下一轮"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p5_live_search_precheck=pass "
        "status=live_search_precheck_rejected "
        "precheck_decision=reject "
        "reason=authorization_window_contains_placeholders "
        "live_search_authorized=false "
        "live_external_search_invoked=false "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
