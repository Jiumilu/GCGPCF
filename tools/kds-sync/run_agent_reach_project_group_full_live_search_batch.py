#!/usr/bin/env python3
"""Run one Agent-Reach P8 project-group live-search batch behind an authorization gate."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN_PATH = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
P7_RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
DEFAULT_OUTPUT_DIR = ROOT / "docs/harness/evidence"

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
REQUIRED_AUTH_FIELDS = {
    "authorization_id",
    "authorization_status",
    "authorized_by",
    "authorized_at",
    "expires_at",
    "batch_id",
    "allowed_channels",
    "max_queries",
    "max_results_per_query",
    "allow_agent_reach_binary_invocation",
    "allow_external_network",
    "allow_write_evidence_only",
    "forbidden_actions",
    "logging_redaction",
}
REQUIRED_CANDIDATE_FIELDS = {
    "candidate_id",
    "query_id",
    "project",
    "channel",
    "title",
    "url",
    "source_domain",
    "retrieved_at",
    "snippet_redacted",
    "relevance_score",
    "authority_score",
    "freshness_score",
    "traceability_score",
    "overall_score",
    "non_claims",
}
TOKEN_PATTERN = re.compile(r"(?i)(api[_-]?key|token|secret|authorization|cookie)[=:]\S+")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def batch_by_id(plan: dict[str, Any], batch_id: str) -> dict[str, Any] | None:
    for batch in plan.get("batches", []):
        if batch.get("batch_id") == batch_id:
            return batch
    return None


def default_auth_path(batch_id: str) -> Path:
    batch_number = batch_id.rsplit("-", 1)[-1]
    return ROOT / f"fixtures/agent-reach/project-group-full-live-search-batch-{batch_number}-authorization.local.json"


def default_output_json(batch_id: str) -> Path:
    batch_number = batch_id.rsplit("-", 1)[-1]
    return DEFAULT_OUTPUT_DIR / f"agent-reach-p8-full-live-search-batch-{batch_number}-20260622.json"


def default_output_md(batch_id: str) -> Path:
    batch_number = batch_id.rsplit("-", 1)[-1]
    return DEFAULT_OUTPUT_DIR / f"agent-reach-p8-full-live-search-batch-{batch_number}-20260622.md"


def validate_authorization(auth_path: Path, plan: dict[str, Any], batch: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any] | None]:
    if not auth_path.exists():
        return False, ["authorization_file_missing"], None
    auth = load_json(auth_path)
    missing = sorted(REQUIRED_AUTH_FIELDS - set(auth))
    if missing:
        return False, [f"authorization_missing_fields:{','.join(missing)}"], auth
    reasons: list[str] = []
    batch_id = batch["batch_id"]
    queries = batch.get("queries", [])
    policy = plan.get("batch_policy", {})
    if auth.get("authorization_status") != "approved_for_p8_project_group_full_live_search_batch":
        reasons.append("authorization_status_not_approved")
    if auth.get("authorized_by") != "lujunxiang":
        reasons.append("authorized_by_mismatch")
    if auth.get("batch_id") != batch_id:
        reasons.append("batch_id_mismatch")
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
    if set(auth.get("allowed_channels", [])) != set(policy.get("allowed_channels", [])):
        reasons.append("allowed_channels_mismatch")
    if auth.get("max_queries") != len(queries):
        reasons.append("max_queries_mismatch")
    if auth.get("max_results_per_query") != policy.get("max_results_per_query"):
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


def build_execution_plan(batch: dict[str, Any], p7_runner) -> list[dict[str, Any]]:
    return p7_runner.build_execution_plan({"queries": batch.get("queries", [])})


def execute_live(batch: dict[str, Any], limit: int, p7_runner) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: list[dict[str, Any]] = []
    query_errors: list[dict[str, Any]] = []
    for query in batch.get("queries", []):
        try:
            if query["channel"] == "web":
                rows = p7_runner.fetch_web_candidate(query, limit)
            elif query["channel"] == "rss":
                rows = p7_runner.fetch_rss_candidate(query, limit)
            elif query["channel"] == "bilibili":
                rows = p7_runner.fetch_bilibili_candidate(query, limit)
            else:
                rows = []
            if not rows:
                query_errors.append(
                    {
                        "query_id": query["query_id"],
                        "project": query["project"],
                        "channel": query["channel"],
                        "error_type": "empty_result",
                        "message": "No candidates returned for query.",
                    }
                )
            candidates.extend(rows)
        except Exception as exc:
            query_errors.append(
                {
                    "query_id": query["query_id"],
                    "project": query["project"],
                    "channel": query["channel"],
                    "error_type": exc.__class__.__name__,
                    "message": p7_runner.redact_text(str(exc)),
                }
            )
    return candidates, query_errors


def quality_report(batch: dict[str, Any], candidates: list[dict[str, Any]], query_errors: list[dict[str, Any]], requirements: dict[str, Any] | None = None) -> dict[str, Any]:
    requirements = requirements or {}
    queries = batch.get("queries", [])
    expected_query_ids = {query["query_id"] for query in queries}
    expected_channels = {query["channel"] for query in queries}
    covered_query_ids = {candidate.get("query_id") for candidate in candidates if candidate.get("query_id") in expected_query_ids}
    covered_channels = {candidate.get("channel") for candidate in candidates if candidate.get("channel") in expected_channels}
    urls = [candidate.get("url") for candidate in candidates if candidate.get("url")]
    field_checks = [REQUIRED_CANDIDATE_FIELDS <= set(candidate) for candidate in candidates]
    overall_scores = [candidate.get("overall_score", 0) for candidate in candidates]
    average_score = round(sum(overall_scores) / len(overall_scores), 4) if overall_scores else 0
    traceability_scores = [candidate.get("traceability_score", 0) for candidate in candidates]
    forbidden_claim_count = sum(
        1
        for candidate in candidates
        for claim in candidate.get("non_claims", [])
        if claim in {"accepted", "integrated", "production_ready"}
    )
    credential_leak_count = sum(1 for candidate in candidates if TOKEN_PATTERN.search(json.dumps(candidate, ensure_ascii=False)))
    report = {
        "candidate_count": len(candidates),
        "query_candidate_coverage": round(len(covered_query_ids) / len(expected_query_ids), 4) if expected_query_ids else 0,
        "missing_query_ids": sorted(expected_query_ids - covered_query_ids),
        "channel_candidate_coverage": round(len(covered_channels) / len(expected_channels), 4) if expected_channels else 0,
        "missing_channels": sorted(expected_channels - covered_channels),
        "duplicate_url_count": len(urls) - len(set(urls)),
        "query_error_count": len(query_errors),
        "required_field_coverage": round(sum(field_checks) / len(field_checks), 4) if field_checks else 0,
        "average_score": average_score,
        "average_overall_score": average_score,
        "minimum_candidate_overall_score": min(overall_scores) if overall_scores else 0,
        "minimum_traceability_score": min(traceability_scores) if traceability_scores else 0,
        "forbidden_claim_count": forbidden_claim_count,
        "credential_leak_count": credential_leak_count,
    }
    report["threshold_pass"] = (
        report["query_candidate_coverage"] == 1.0
        and report["channel_candidate_coverage"] == 1.0
        and report["duplicate_url_count"] == 0
        and report["query_error_count"] == 0
        and report["required_field_coverage"] == 1.0
        and report["candidate_count"] >= len(queries)
        and report["average_overall_score"] >= requirements.get("minimum_average_overall_score", 0)
        and report["minimum_candidate_overall_score"] >= requirements.get("minimum_candidate_overall_score", 0)
        and report["minimum_traceability_score"] >= requirements.get("minimum_traceability_score", 0)
        and report["forbidden_claim_count"] == 0
        and report["credential_leak_count"] == 0
    )
    return report


def build_report(batch_id: str, auth_path: Path, execute: bool) -> dict[str, Any]:
    plan = load_json(PLAN_PATH)
    batch = batch_by_id(plan, batch_id)
    if batch is None:
        raise SystemExit(f"agent_reach_p8_batch_runner=fail reason=batch_not_found:{batch_id}")
    p7_runner = load_p7_runner()
    authorized, reasons, auth = validate_authorization(auth_path, plan, batch)
    execution_plan = build_execution_plan(batch, p7_runner)
    controls = {
        "agent_reach_binary_invoked": False,
        "live_external_search_invoked": False,
        "credential_written": False,
        "browser_cookie_extraction_invoked": False,
        "kds_canonical_write_allowed": False,
        "gfis_source_of_record_write_allowed": False,
        "production_config_write_allowed": False,
        "global_mcp_config_write_allowed": False,
        "production_integration_allowed": False,
    }
    base = {
        "id": "agent-reach-p8-project-group-full-live-search-batch-runtime",
        "round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001",
        "generated_at": utc_now(),
        "batch_id": batch_id,
        "current_admission": "limited_candidate_only",
        "auth_path": display_path(auth_path),
        "authorization_valid": authorized,
        "authorization_reasons": reasons,
        "execution_requested": execute,
        "execution_plan": execution_plan,
        "projects": [query["project"] for query in batch.get("queries", [])],
        "query_ids": [query["query_id"] for query in batch.get("queries", [])],
        "security_controls": controls,
    }
    if not authorized:
        return {**base, "status": "blocked_pending_execution_authorization", "candidates": [], "query_errors": [], "quality_report": quality_report(batch, [], [], plan.get("quality_requirements", {}))}
    if not execute:
        return {**base, "status": "authorized_execution_not_requested", "candidates": [], "query_errors": [], "quality_report": quality_report(batch, [], [], plan.get("quality_requirements", {}))}
    candidates, query_errors = execute_live(batch, plan["batch_policy"]["max_results_per_query"], p7_runner)
    quality = quality_report(batch, candidates, query_errors, plan.get("quality_requirements", {}))
    return {
        **base,
        "status": "p8_live_search_batch_completed" if quality["threshold_pass"] else "p8_live_search_batch_rework_required",
        "candidates": candidates,
        "query_errors": query_errors,
        "quality_report": quality,
        "security_controls": {**controls, "live_external_search_invoked": True, "agent_reach_binary_invoked": bool(auth and auth.get("allow_agent_reach_binary_invocation"))},
    }


def render_markdown(report: dict[str, Any]) -> str:
    batch_id = report.get("batch_id", "unknown")
    batch_number = str(batch_id).rsplit("-", 1)[-1]
    quality = report.get("quality_report", {})
    controls = report.get("security_controls", {})
    return "\n".join(
        [
            "---",
            f"doc_id: GPCF-DOC-AGENT-REACH-P8-FULL-LIVE-SEARCH-BATCH-{batch_number.upper()}-20260622",
            f"title: Agent-Reach P8 全量真实搜索批次 {batch_number} 证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            f"kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-full-live-search-batch-{batch_number}-20260622.md",
            f"source_path: docs/harness/evidence/agent-reach-p8-full-live-search-batch-{batch_number}-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            f"# Agent-Reach P8 全量真实搜索批次 {batch_number} 证据 2026-06-22",
            "",
            f"- status: `{report.get('status')}`",
            f"- batch_id: `{batch_id}`",
            f"- current_admission: `{report.get('current_admission')}`",
            f"- authorization_valid: `{report.get('authorization_valid')}`",
            f"- execution_requested: `{report.get('execution_requested')}`",
            f"- live_external_search_invoked: `{controls.get('live_external_search_invoked', False)}`",
            f"- candidate_count: `{quality.get('candidate_count', 0)}`",
            f"- query_candidate_coverage: `{quality.get('query_candidate_coverage', 0)}`",
            f"- channel_candidate_coverage: `{quality.get('channel_candidate_coverage', 0)}`",
            f"- duplicate_url_count: `{quality.get('duplicate_url_count', 0)}`",
            f"- query_error_count: `{quality.get('query_error_count', 0)}`",
            f"- average_overall_score: `{quality.get('average_overall_score', 0)}`",
            f"- minimum_candidate_overall_score: `{quality.get('minimum_candidate_overall_score', 0)}`",
            f"- minimum_traceability_score: `{quality.get('minimum_traceability_score', 0)}`",
            f"- threshold_pass: `{quality.get('threshold_pass', False)}`",
            "",
            "## 安全边界",
            "",
            f"- agent_reach_binary_invoked: `{controls.get('agent_reach_binary_invoked', False)}`",
            f"- credential_written: `{controls.get('credential_written', False)}`",
            f"- browser_cookie_extraction_invoked: `{controls.get('browser_cookie_extraction_invoked', False)}`",
            f"- kds_canonical_write_allowed: `{controls.get('kds_canonical_write_allowed', False)}`",
            f"- gfis_source_of_record_write_allowed: `{controls.get('gfis_source_of_record_write_allowed', False)}`",
            f"- production_config_write_allowed: `{controls.get('production_config_write_allowed', False)}`",
            f"- global_mcp_config_write_allowed: `{controls.get('global_mcp_config_write_allowed', False)}`",
            f"- production_integration_allowed: `{controls.get('production_integration_allowed', False)}`",
            "",
            "## 非声明",
            "",
            "- 本证据仅为候选数据。",
            "- 本证据不主张 accepted、integrated 或 production_ready。",
            "- 本证据不写入 KDS canonical Markdown。",
            "- 本证据不写入 GFIS source-of-record。",
            "- 原始供应商返回载荷不会持久化。",
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
    parser.add_argument("--batch-id", default="p8-batch-1", choices=["p8-batch-1", "p8-batch-2", "p8-batch-3"])
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()
    auth_path = args.authorization or default_auth_path(args.batch_id)
    output_json = args.output_json or default_output_json(args.batch_id)
    output_md = args.output_md or default_output_md(args.batch_id)
    report = build_report(args.batch_id, auth_path, args.execute)
    if args.write_evidence:
        write_evidence(report, output_json, output_md)
        report = {**report, "written_evidence": {"json": display_path(output_json), "markdown": display_path(output_md)}}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
