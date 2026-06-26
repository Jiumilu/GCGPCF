#!/usr/bin/env python3
"""Validate Agent-Reach P9S source-direct live authorization intake without live fetch."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json"
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
DEFAULT_AUTH = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-authorization-intake-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-authorization-intake-20260626.md"

ALLOWED_METHODS = {"target_url", "sitemap", "rss", "public_list_page", "site_search_endpoint_without_credentials"}
FORBIDDEN_ACTIONS = {
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
}
REQUIRED_AUTH_FIELDS = {
    "authorization_id",
    "authorization_status",
    "authorized_by",
    "authorized_at",
    "expires_at",
    "allowed_methods",
    "max_targets",
    "max_entrypoints_per_target",
    "max_pages_per_entrypoint",
    "allow_external_network",
    "allow_write_evidence_only",
    "forbidden_actions",
    "logging_redaction",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_live_authorization_intake=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def parse_iso8601(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def validate_auth(auth: dict[str, Any], precheck: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    missing = sorted(REQUIRED_AUTH_FIELDS - set(auth))
    if missing:
        reasons.append(f"authorization_missing_fields:{','.join(missing)}")
        return reasons
    if auth.get("authorization_id") != "agent-reach-p9-source-direct-hit-rate-live-run":
        reasons.append("authorization_id_mismatch")
    if auth.get("authorization_status") != "approved_for_p9_source_direct_hit_rate_live_run":
        reasons.append("authorization_status_not_approved")
    if not auth.get("authorized_by"):
        reasons.append("authorized_by_missing")
    authorized_at = parse_iso8601(auth.get("authorized_at"))
    expires_at = parse_iso8601(auth.get("expires_at"))
    if authorized_at is None:
        reasons.append("authorized_at_invalid")
    if expires_at is None:
        reasons.append("expires_at_invalid")
    now = datetime.now(timezone.utc)
    if authorized_at and expires_at:
        if expires_at <= authorized_at:
            reasons.append("expires_at_not_after_authorized_at")
        if now < authorized_at.astimezone(timezone.utc):
            reasons.append("authorization_not_yet_active")
        if now > expires_at.astimezone(timezone.utc):
            reasons.append("authorization_expired")
    if set(auth.get("allowed_methods", [])) != ALLOWED_METHODS:
        reasons.append("allowed_methods_mismatch")
    if auth.get("max_targets") != len(precheck.get("source_direct_targets", [])):
        reasons.append("max_targets_mismatch")
    if auth.get("max_entrypoints_per_target") != 3:
        reasons.append("max_entrypoints_per_target_mismatch")
    if auth.get("max_pages_per_entrypoint") != 5:
        reasons.append("max_pages_per_entrypoint_mismatch")
    if auth.get("allow_external_network") is not True:
        reasons.append("external_network_not_allowed")
    if auth.get("allow_write_evidence_only") is not True:
        reasons.append("write_scope_not_evidence_only")
    if not FORBIDDEN_ACTIONS.issubset(set(auth.get("forbidden_actions", []))):
        reasons.append("forbidden_actions_missing")
    redaction = auth.get("logging_redaction", {})
    for field in ["redact_tokens", "redact_cookies", "redact_authorization_headers", "redact_query_personal_data", "persist_redacted_snippets_only"]:
        if redaction.get(field) is not True:
            reasons.append(f"redaction_not_true:{field}")
    return sorted(set(reasons))


def build_report(auth_path: Path) -> dict[str, Any]:
    precheck = read_json(PRECHECK)
    request = read_json(REQUEST)
    if precheck.get("status") != "p9_source_direct_hit_rate_precheck_ready":
        fail("precheck_status_mismatch")
    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("authorization_request_status_mismatch")
    base = {
        "id": "agent-reach-p9-source-direct-live-authorization-intake-20260626",
        "date": "2026-06-26",
        "current_admission": "limited_candidate_only",
        "authorization_path": display_path(auth_path),
        "planned_target_count": len(precheck.get("source_direct_targets", [])),
        "max_entrypoints_per_target_required": 3,
        "max_pages_per_entrypoint_required": 5,
        "allowed_methods_required": sorted(ALLOWED_METHODS),
        "live_external_fetch_invoked": False,
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
            "authorization_intake_only",
            "not_live_fetch_invoked",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }
    if not auth_path.exists():
        return {
            **base,
            "status": "blocked_pending_p9_source_direct_authorization",
            "authorization_valid": False,
            "authorization_reasons": ["authorization_file_missing"],
            "ready_for_live_execution": False,
        }
    auth = read_json(auth_path)
    reasons = validate_auth(auth, precheck)
    return {
        **base,
        "status": "p9_source_direct_live_authorization_intake_ready" if not reasons else "blocked_invalid_p9_source_direct_authorization",
        "authorization_valid": not reasons,
        "authorization_reasons": reasons,
        "ready_for_live_execution": not reasons,
        "authorized_by_present": bool(auth.get("authorized_by")),
        "authorized_at": auth.get("authorized_at"),
        "expires_at": auth.get("expires_at"),
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-LIVE-AUTHORIZATION-INTAKE-20260626",
            "title: Agent-Reach P9S Source Direct Live Authorization Intake 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-live-authorization-intake-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-live-authorization-intake-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Live Authorization Intake 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- authorization_valid: `{report['authorization_valid']}`",
            f"- ready_for_live_execution: `{report['ready_for_live_execution']}`",
            f"- planned_target_count: `{report['planned_target_count']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            "",
            "## Boundary",
            "",
            "- This evidence validates authorization intake only.",
            "- This evidence does not invoke live target-site fetch.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )


def main() -> None:
    report = build_report(DEFAULT_AUTH)
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_live_authorization_intake=pass "
        f"status={report['status']} authorization_valid={str(report['authorization_valid']).lower()} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
