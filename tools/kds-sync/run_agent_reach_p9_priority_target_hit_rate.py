#!/usr/bin/env python3
"""Run Agent-Reach P9 priority target hit-rate evaluation behind an authorization gate."""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-precheck-20260626.json"
DEFAULT_AUTH = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-authorization.local.json"
P7_RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
DEFAULT_OUTPUT_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-live-run-20260626.json"
DEFAULT_OUTPUT_MD = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-live-run-20260626.md"

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
REQUIRED_AUTH_FIELDS = {
    "authorization_id",
    "authorization_status",
    "authorized_by",
    "authorized_at",
    "expires_at",
    "allowed_channels",
    "max_queries",
    "max_results_per_query",
    "allow_agent_reach_binary_invocation",
    "allow_external_network",
    "allow_write_evidence_only",
    "forbidden_actions",
    "logging_redaction",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_iso8601(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def load_p7_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", P7_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("p7_runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def planned_queries(precheck: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for topic in precheck.get("topics", []):
        for query in topic.get("query_expansion", []):
            rows.append({**query, "topic_id": topic["topic_id"], "topic_label": topic["label"]})
    return rows


def validate_authorization(auth_path: Path, precheck: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any] | None]:
    if not auth_path.exists():
        return False, ["authorization_file_missing"], None
    auth = load_json(auth_path)
    missing = sorted(REQUIRED_AUTH_FIELDS - set(auth))
    if missing:
        return False, [f"authorization_missing_fields:{','.join(missing)}"], auth
    reasons: list[str] = []
    queries = planned_queries(precheck)
    if auth.get("authorization_status") != "approved_for_p9_priority_target_hit_rate_live_run":
        reasons.append("authorization_status_not_approved")
    if auth.get("authorization_id") != "agent-reach-p9-priority-target-hit-rate-live-run":
        reasons.append("authorization_id_mismatch")
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
    if not set(auth.get("allowed_channels", [])) <= {"web", "rss", "bilibili"}:
        reasons.append("allowed_channels_out_of_scope")
    if "web" not in set(auth.get("allowed_channels", [])):
        reasons.append("web_channel_not_allowed")
    if auth.get("max_queries") != len(queries):
        reasons.append("max_queries_mismatch")
    if auth.get("max_results_per_query") != 5:
        reasons.append("max_results_per_query_mismatch")
    if auth.get("allow_agent_reach_binary_invocation") is not False:
        reasons.append("agent_reach_binary_invocation_not_allowed")
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
    return not reasons, sorted(set(reasons)), auth


def apply_domain_boost(candidate: dict[str, Any], query: dict[str, Any], precheck: dict[str, Any]) -> dict[str, Any]:
    boost = precheck["domain_boost_policy"]
    domain = candidate.get("source_domain", "")
    p0_domains = set(boost["priority_domains"]["P0"])
    p1_domains = set(boost["priority_domains"]["P1"])
    base_score = candidate["overall_score"]
    boost_value = 0.0
    priority_level = "none"
    if domain in p0_domains:
        boost_value += boost["p0_domain_boost"]
        priority_level = "P0"
    elif domain in p1_domains:
        boost_value += boost["p1_domain_boost"]
        priority_level = "P1"
    if domain.endswith(".gov.cn") or domain in {"mee.gov.cn", "miit.gov.cn", "ndrc.gov.cn", "pbc.gov.cn"}:
        boost_value += boost["official_government_domain_boost"]
    boosted = min(boost["maximum_boosted_overall_score"], round(base_score + boost_value, 4))
    expected_hit = domain in set(query.get("expected_priority_domains", []))
    return {
        **candidate,
        "topic_id": query["topic_id"],
        "topic_label": query["topic_label"],
        "expected_priority_domains": query["expected_priority_domains"],
        "business_fields": query["business_fields"],
        "raw_overall_score": base_score,
        "domain_boost": round(boost_value, 4),
        "boosted_overall_score": boosted,
        "priority_domain_level": priority_level,
        "expected_priority_domain_hit": expected_hit,
    }


def execute_live(precheck: dict[str, Any], p7_runner) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for query in planned_queries(precheck):
        try:
            fetch_query = {
                "query_id": query["query_id"],
                "project": "GFIS",
                "channel": query["channel"],
                "query": query["query"],
            }
            if query["channel"] == "web":
                rows = p7_runner.fetch_web_candidate(fetch_query, 5)
            elif query["channel"] == "rss":
                rows = p7_runner.fetch_rss_candidate(fetch_query, 5)
            elif query["channel"] == "bilibili":
                rows = p7_runner.fetch_bilibili_candidate(fetch_query, 5)
            else:
                rows = []
            if not rows:
                errors.append({"query_id": query["query_id"], "topic_id": query["topic_id"], "error_type": "empty_result", "message": "No candidates returned for query."})
            for candidate in rows:
                candidates.append(apply_domain_boost(candidate, query, precheck))
        except Exception as exc:
            errors.append({"query_id": query["query_id"], "topic_id": query["topic_id"], "error_type": exc.__class__.__name__, "message": p7_runner.redact_text(str(exc))})
    return candidates, errors


def hit_rate_report(precheck: dict[str, Any], candidates: list[dict[str, Any]], query_errors: list[dict[str, Any]]) -> dict[str, Any]:
    topics = {topic["topic_id"]: topic for topic in precheck.get("topics", [])}
    topic_reports: dict[str, Any] = {}
    for topic_id, topic in topics.items():
        topic_candidates = [candidate for candidate in candidates if candidate.get("topic_id") == topic_id]
        hit_domains = {candidate["source_domain"] for candidate in topic_candidates if candidate.get("expected_priority_domain_hit")}
        p0_domains = set(precheck["domain_boost_policy"]["priority_domains"]["P0"])
        p0_hit_domains = hit_domains & p0_domains
        expected_queries = [query["query_id"] for query in topic["query_expansion"]]
        query_ids_with_candidates = {candidate["query_id"] for candidate in topic_candidates}
        topic_reports[topic_id] = {
            "candidate_count": len(topic_candidates),
            "expected_priority_domain_hit_count": len(hit_domains),
            "expected_p0_domain_hit_count": len(p0_hit_domains),
            "query_candidate_coverage": round(len(query_ids_with_candidates) / len(expected_queries), 4),
            "missing_query_ids": sorted(set(expected_queries) - query_ids_with_candidates),
            "threshold_pass": (
                len(p0_hit_domains) >= topic.get("minimum_p0_domain_hits_required", 0)
                and len(hit_domains) >= topic.get("minimum_total_domain_hits_required", 0)
                and len(set(expected_queries) - query_ids_with_candidates) == 0
            ),
        }
    return {
        "candidate_count": len(candidates),
        "query_error_count": len(query_errors),
        "topic_reports": topic_reports,
        "topic_coverage": round(sum(1 for item in topic_reports.values() if item["threshold_pass"]) / len(topics), 4) if topics else 0,
        "threshold_pass": bool(topic_reports) and all(item["threshold_pass"] for item in topic_reports.values()) and not query_errors,
    }


def build_report(auth_path: Path, execute: bool) -> dict[str, Any]:
    precheck = load_json(PRECHECK)
    p7_runner = load_p7_runner()
    authorized, reasons, auth = validate_authorization(auth_path, precheck)
    base = {
        "id": "agent-reach-p9-priority-target-hit-rate-live-run-20260626",
        "date": "2026-06-26",
        "current_admission": "limited_candidate_only",
        "authorization_valid": authorized,
        "authorization_reasons": reasons,
        "authorization_path": display_path(auth_path),
        "execution_requested": execute,
        "planned_query_count": len(planned_queries(precheck)),
        "security_controls": {
            "live_external_search_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "non_claims": ["candidate_only", "not_source_of_record", "not_kds_canonical_written", "not_gfis_source_of_record_written", "not_accepted", "not_integrated", "not_production_ready"],
    }
    if not authorized:
        return {**base, "status": "blocked_pending_p9_live_authorization", "candidates": [], "query_errors": [], "hit_rate_report": hit_rate_report(precheck, [], [])}
    if not execute:
        return {**base, "status": "authorized_execution_not_requested", "candidates": [], "query_errors": [], "hit_rate_report": hit_rate_report(precheck, [], [])}
    candidates, errors = execute_live(precheck, p7_runner)
    hit_rate = hit_rate_report(precheck, candidates, errors)
    return {
        **base,
        "status": "p9_priority_target_hit_rate_completed" if hit_rate["threshold_pass"] else "p9_priority_target_hit_rate_rework_required",
        "candidates": candidates,
        "query_errors": errors,
        "hit_rate_report": hit_rate,
        "security_controls": {**base["security_controls"], "live_external_search_invoked": True},
    }


def render_markdown(report: dict[str, Any]) -> str:
    hit_rate = report.get("hit_rate_report", {})
    controls = report.get("security_controls", {})
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-PRIORITY-TARGET-HIT-RATE-LIVE-RUN-20260626",
            "title: Agent-Reach P9 重点对象命中率运行证据 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-live-run-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-live-run-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9 重点对象命中率运行证据 2026-06-26",
            "",
            f"- status: `{report.get('status')}`",
            f"- authorization_valid: `{report.get('authorization_valid')}`",
            f"- execution_requested: `{report.get('execution_requested')}`",
            f"- live_external_search_invoked: `{controls.get('live_external_search_invoked')}`",
            f"- planned_query_count: `{report.get('planned_query_count')}`",
            f"- candidate_count: `{hit_rate.get('candidate_count', 0)}`",
            f"- query_error_count: `{hit_rate.get('query_error_count', 0)}`",
            f"- topic_coverage: `{hit_rate.get('topic_coverage', 0)}`",
            f"- threshold_pass: `{hit_rate.get('threshold_pass', False)}`",
            "",
            "## 非声明",
            "",
            "- This evidence is candidate-only.",
            "- This evidence does not create source-of-record.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )


def write_evidence(report: dict[str, Any], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", type=Path, default=DEFAULT_AUTH)
    parser.add_argument("--execute-live", action="store_true")
    parser.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()
    report = build_report(args.auth, args.execute_live)
    if args.write_evidence:
        write_evidence(report, args.output_json, args.output_md)
        report = {**report, "written_evidence": {"json": display_path(args.output_json), "markdown": display_path(args.output_md)}}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
