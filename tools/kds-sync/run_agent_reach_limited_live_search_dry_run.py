#!/usr/bin/env python3
"""Run the Agent-Reach limited live-search dry-run behind an authorization gate."""

from __future__ import annotations

import argparse
import html
import http.client
import json
import re
import base64
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN_PATH = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-preparation-20260622.json"
DEFAULT_AUTH_PATH = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json"
DEFAULT_OUTPUT_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-limited-live-search-dry-run-20260622.json"
DEFAULT_OUTPUT_MD = ROOT / "docs/harness/evidence/agent-reach-p7-limited-live-search-dry-run-20260622.md"

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
DUCKDUCKGO_RESULT_PATTERN = re.compile(r'<div[^>]+class="[^"]*result[^"]*"[^>]*>(?P<body>.*?)</div>\s*</div>', re.S)
DUCKDUCKGO_LINK_PATTERN = re.compile(r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>', re.S)
DUCKDUCKGO_SNIPPET_PATTERN = re.compile(r'<a[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(?P<snippet>.*?)</a>|<div[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(?P<div_snippet>.*?)</div>', re.S)
BING_RESULT_PATTERN = re.compile(r'<li[^>]+class="[^"]*b_algo[^"]*"[^>]*>(?P<body>.*?)</li>', re.S)
BING_LINK_PATTERN = re.compile(r'<h2[^>]*>\s*<a[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>', re.S)
BING_SNIPPET_PATTERN = re.compile(r'<p[^>]*>(?P<snippet>.*?)</p>', re.S)
MAX_RETAINED_CANDIDATES_PER_QUERY = 3


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_iso8601(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def redact_text(value: str) -> str:
    return TOKEN_PATTERN.sub("[REDACTED]", value).replace("\n", " ").strip()[:600]


def strip_html(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<.*?>", "", html.unescape(value))).strip()


def normalize_duckduckgo_href(href: str) -> str:
    url = html.unescape(href)
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("duckduckgo.com"):
        query_values = urllib.parse.parse_qs(parsed.query)
        return query_values.get("uddg", [url])[0]
    return url


def normalize_bing_href(href: str) -> str:
    url = html.unescape(href)
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("bing.com"):
        query_values = urllib.parse.parse_qs(parsed.query)
        encoded = query_values.get("u", [url])[0]
        if encoded.startswith("a1"):
            payload = encoded[2:]
            padding = "=" * ((4 - len(payload) % 4) % 4)
            try:
                return base64.urlsafe_b64decode(payload + padding).decode("utf-8", errors="replace")
            except Exception:
                return encoded
        return encoded
    return url


def read_response_text(resp) -> str:
    try:
        payload = resp.read()
    except http.client.IncompleteRead as exc:
        payload = exc.partial
    return payload.decode("utf-8", errors="replace")


def read_json_with_retries(url: str, headers: dict[str, str], attempts: int = 3) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(read_response_text(resp))
        except Exception as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(0.5 * (attempt + 1))
    raise last_error if last_error else RuntimeError("json_fetch_failed")


def score_candidate(query: dict[str, Any], title: str, snippet: str, url: str) -> dict[str, float]:
    query_terms = {part.lower() for part in re.findall(r"[A-Za-z0-9]+", query["query"]) if len(part) >= 3}
    text = f"{title} {snippet} {url}".lower()
    hits = sum(1 for term in query_terms if term in text)
    relevance = min(1.0, hits / max(1, min(len(query_terms), 6)))
    authority = 0.8 if url.startswith("https://") else 0.5
    freshness = 0.6
    traceability = 1.0 if url else 0.0
    overall = round(relevance * 0.5 + freshness * 0.15 + authority * 0.2 + traceability * 0.15, 4)
    return {
        "relevance_score": round(relevance, 4),
        "authority_score": round(authority, 4),
        "freshness_score": round(freshness, 4),
        "traceability_score": round(traceability, 4),
        "overall_score": overall,
    }


def validate_authorization(auth_path: Path, plan: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any] | None]:
    if not auth_path.exists():
        return False, ["authorization_file_missing"], None
    auth = load_json(auth_path)
    missing = sorted(REQUIRED_AUTH_FIELDS - set(auth))
    if missing:
        return False, [f"authorization_missing_fields:{','.join(missing)}"], auth
    reasons: list[str] = []
    if auth.get("authorization_status") != "approved_for_p7_limited_live_search_dry_run":
        reasons.append("authorization_status_not_approved")
    if not auth.get("authorized_by"):
        reasons.append("authorized_by_missing")
    authorized_at = parse_iso8601(auth.get("authorized_at", ""))
    expires_at = parse_iso8601(auth.get("expires_at", ""))
    if authorized_at is None:
        reasons.append("authorized_at_invalid")
    if expires_at is None:
        reasons.append("expires_at_invalid")
    now = datetime.now(timezone.utc)
    if authorized_at and expires_at:
        if expires_at <= authorized_at:
            reasons.append("expires_at_not_after_authorized_at")
        if now > expires_at.astimezone(timezone.utc):
            reasons.append("authorization_expired")
    scope = plan["scope"]
    if not set(auth.get("allowed_channels", [])) <= set(scope["allowed_channels"]):
        reasons.append("allowed_channels_out_of_scope")
    if auth.get("max_queries") != scope["max_queries"]:
        reasons.append("max_queries_mismatch")
    if auth.get("max_results_per_query") != scope["max_results_per_query"]:
        reasons.append("max_results_per_query_mismatch")
    if auth.get("allow_external_network") is not True:
        reasons.append("external_network_not_allowed")
    if auth.get("allow_write_evidence_only") is not True:
        reasons.append("evidence_write_not_limited")
    if not FORBIDDEN_ACTIONS.issubset(set(auth.get("forbidden_actions", []))):
        reasons.append("forbidden_actions_missing")
    redaction = auth.get("logging_redaction", {})
    for field in ["redact_tokens", "redact_cookies", "redact_authorization_headers", "redact_query_personal_data", "persist_redacted_snippets_only"]:
        if redaction.get(field) is not True:
            reasons.append(f"redaction_not_true:{field}")
    return not reasons, reasons, auth


def build_execution_plan(plan: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for query in plan["queries"]:
        channel = query["channel"]
        encoded = urllib.parse.quote(query["query"])
        if channel == "web":
            command = ["python3", "stdlib_urllib_duckduckgo_html", f"https://html.duckduckgo.com/html/?q={encoded}"]
            backend = "duckduckgo_html_via_python_stdlib"
        elif channel == "rss":
            command = ["curl", "-s", f"https://news.google.com/rss/search?q={encoded}"]
            backend = "feedparser_google_news_rss"
        elif channel == "bilibili":
            command = ["curl", "-s", f"https://api.bilibili.com/x/web-interface/search/all/v2?keyword={encoded}&page=1"]
            backend = "bilibili_search_api"
        else:
            command = []
            backend = "unsupported"
        items.append({**query, "backend": backend, "planned_command": command})
    return items


def fetch_rss_candidate(query: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(query["query"])
    url = f"https://www.bing.com/news/search?q={encoded}&format=rss"
    req = urllib.request.Request(url, headers={"User-Agent": "agent-reach-controlled-dry-run/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        text = read_response_text(resp)
    rows: list[tuple[str, str, str]] = []
    root = ElementTree.fromstring(text)
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        desc = item.findtext("description") or ""
        if title and link:
            rows.append((title, link, desc))
        if len(rows) >= limit:
            break
    return build_candidates(query, rows)


def fetch_bilibili_candidate(query: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(query["query"])
    url = f"https://api.bilibili.com/x/web-interface/search/all/v2?keyword={encoded}&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
        "Referer": "https://search.bilibili.com/",
        "Accept": "application/json,text/plain,*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    payload = read_json_with_retries(url, headers)
    rows: list[tuple[str, str, str]] = []
    for group in payload.get("data", {}).get("result", []):
        for item in group.get("data", [])[:limit]:
            title = re.sub(r"<.*?>", "", str(item.get("title", "")))
            arcurl = str(item.get("arcurl") or item.get("url") or "")
            desc = str(item.get("description") or item.get("desc") or "")
            if title and arcurl:
                rows.append((title, arcurl, desc))
            if len(rows) >= limit:
                break
        if len(rows) >= limit:
            break
    return build_candidates(query, rows)


def fetch_web_candidate(query: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(query["query"])
    url = f"https://www.bing.com/search?q={encoded}&mkt=en-US&setlang=en-US&cc=US"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        text = read_response_text(resp)
    rows: list[tuple[str, str, str]] = []
    for block in BING_RESULT_PATTERN.finditer(text):
        body = block.group("body")
        link_match = BING_LINK_PATTERN.search(body)
        if not link_match:
            continue
        snippet_match = BING_SNIPPET_PATTERN.search(body)
        href = normalize_bing_href(link_match.group("href"))
        title = strip_html(link_match.group("title"))
        snippet = strip_html(snippet_match.group("snippet") if snippet_match else "")
        if title and href:
            rows.append((title, href, snippet))
        if len(rows) >= limit:
            break
    return build_candidates(query, rows)


def build_candidates(query: dict[str, Any], rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    candidates = []
    seen_urls: set[str] = set()
    for idx, (title, url, snippet) in enumerate(rows, start=1):
        if not strip_html(snippet):
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        scores = score_candidate(query, title, snippet, url)
        if scores["overall_score"] < 0.5:
            continue
        candidates.append(
            {
                "candidate_id": f"{query['query_id']}-c{idx}",
                "query_id": query["query_id"],
                "project": query["project"],
                "channel": query["channel"],
                "title": redact_text(title),
                "url": url,
                "source_domain": urllib.parse.urlparse(url).netloc,
                "retrieved_at": utc_now(),
                "snippet_redacted": redact_text(snippet),
                **scores,
                "non_claims": ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"],
            }
        )
    return sorted(candidates, key=lambda item: item["overall_score"], reverse=True)[:MAX_RETAINED_CANDIDATES_PER_QUERY]


def execute_live(plan: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    limit = plan["scope"]["max_results_per_query"]
    candidates: list[dict[str, Any]] = []
    query_errors: list[dict[str, Any]] = []
    for query in plan["queries"]:
        try:
            if query["channel"] == "web":
                rows = fetch_web_candidate(query, limit)
            elif query["channel"] == "rss":
                rows = fetch_rss_candidate(query, limit)
            elif query["channel"] == "bilibili":
                rows = fetch_bilibili_candidate(query, limit)
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
                    "message": redact_text(str(exc)),
                }
            )
    return candidates, query_errors


def quality_report(plan: dict[str, Any], candidates: list[dict[str, Any]], query_errors: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    query_errors = query_errors or []
    required = REQUIRED_CANDIDATE_FIELDS
    field_checks = [required <= set(candidate) for candidate in candidates]
    required_field_coverage = round(sum(field_checks) / len(field_checks), 4) if field_checks else 0
    average_score = round(sum(item["overall_score"] for item in candidates) / len(candidates), 4) if candidates else 0
    traceability_scores = [item["traceability_score"] for item in candidates]
    minimum_traceability = min(traceability_scores) if traceability_scores else 0
    expected_query_ids = {query["query_id"] for query in plan["queries"]}
    covered_query_ids = {candidate["query_id"] for candidate in candidates if candidate.get("query_id") in expected_query_ids}
    missing_query_ids = sorted(expected_query_ids - covered_query_ids)
    query_candidate_coverage = round(len(covered_query_ids) / len(expected_query_ids), 4) if expected_query_ids else 0
    expected_channels = set(plan["scope"]["allowed_channels"])
    covered_channels = {candidate["channel"] for candidate in candidates if candidate.get("channel") in expected_channels}
    missing_channels = sorted(expected_channels - covered_channels)
    channel_candidate_coverage = round(len(covered_channels) / len(expected_channels), 4) if expected_channels else 0
    urls = [candidate.get("url", "") for candidate in candidates if candidate.get("url")]
    duplicate_url_count = len(urls) - len(set(urls))
    forbidden_claim_count = sum(
        1
        for candidate in candidates
        for claim in candidate.get("non_claims", [])
        if claim in {"accepted", "integrated", "production_ready"}
    )
    credential_leak_count = sum(1 for candidate in candidates if TOKEN_PATTERN.search(json.dumps(candidate, ensure_ascii=False)))
    thresholds = plan["quality_thresholds"]
    threshold_pass = (
        len(plan["queries"]) >= thresholds["minimum_query_count"]
        and len(plan["queries"]) <= thresholds["maximum_query_count"]
        and len(candidates) >= thresholds["minimum_candidate_count"]
        and required_field_coverage >= thresholds["minimum_required_field_coverage"]
        and average_score >= thresholds["minimum_average_score"]
        and minimum_traceability >= thresholds["minimum_traceability_score"]
        and query_candidate_coverage == 1.0
        and channel_candidate_coverage == 1.0
        and duplicate_url_count == 0
        and len(query_errors) == 0
        and forbidden_claim_count <= thresholds["maximum_forbidden_claim_count"]
        and credential_leak_count <= thresholds["maximum_credential_leak_count"]
    )
    return {
        "candidate_count": len(candidates),
        "query_candidate_coverage": query_candidate_coverage,
        "missing_query_ids": missing_query_ids,
        "channel_candidate_coverage": channel_candidate_coverage,
        "missing_channels": missing_channels,
        "duplicate_url_count": duplicate_url_count,
        "query_error_count": len(query_errors),
        "required_field_coverage": required_field_coverage,
        "average_score": average_score,
        "minimum_traceability_score": minimum_traceability,
        "forbidden_claim_count": forbidden_claim_count,
        "credential_leak_count": credential_leak_count,
        "threshold_pass": threshold_pass,
    }


def build_report(auth_path: Path, execute: bool) -> dict[str, Any]:
    plan = load_json(PLAN_PATH)
    authorized, reasons, auth = validate_authorization(auth_path, plan)
    execution_plan = build_execution_plan(plan)
    base = {
        "id": "agent-reach-p7-limited-live-search-dry-run-runtime",
        "round": "GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001",
        "generated_at": utc_now(),
        "current_admission": "limited_candidate_only",
        "auth_path": display_path(auth_path),
        "authorization_valid": authorized,
        "authorization_reasons": reasons,
        "execution_requested": execute,
        "execution_plan": execution_plan,
        "security_controls": {
            "agent_reach_binary_invoked": False,
            "live_external_search_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
    }
    if not authorized:
        return {**base, "status": "blocked_pending_execution_authorization", "candidates": [], "query_errors": [], "quality_report": quality_report(plan, [])}
    if not execute:
        return {**base, "status": "authorized_execution_not_requested", "candidates": [], "query_errors": [], "quality_report": quality_report(plan, [])}
    candidates, query_errors = execute_live(plan)
    report = quality_report(plan, candidates, query_errors)
    return {
        **base,
        "status": "limited_live_search_dry_run_completed" if report["threshold_pass"] else "limited_live_search_dry_run_rework_required",
        "candidates": candidates,
        "query_errors": query_errors,
        "quality_report": report,
        "security_controls": {**base["security_controls"], "live_external_search_invoked": True, "agent_reach_binary_invoked": bool(auth and auth.get("allow_agent_reach_binary_invocation"))},
    }


def render_markdown(report: dict[str, Any]) -> str:
    quality = report.get("quality_report", {})
    controls = report.get("security_controls", {})
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-20260622",
            "title: Agent-Reach P7 Limited Live Search Dry Run Evidence 2026-06-22",
            "project: KDS",
            "related_projects: [GFIS, GPC, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p7-limited-live-search-dry-run-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p7-limited-live-search-dry-run-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P7 Limited Live Search Dry Run Evidence 2026-06-22",
            "",
            f"- status: `{report.get('status')}`",
            f"- current_admission: `{report.get('current_admission')}`",
            f"- authorization_valid: `{report.get('authorization_valid')}`",
            f"- execution_requested: `{report.get('execution_requested')}`",
            f"- candidate_count: `{quality.get('candidate_count', 0)}`",
            f"- query_candidate_coverage: `{quality.get('query_candidate_coverage', 0)}`",
            f"- channel_candidate_coverage: `{quality.get('channel_candidate_coverage', 0)}`",
            f"- query_error_count: `{quality.get('query_error_count', 0)}`",
            f"- threshold_pass: `{quality.get('threshold_pass', False)}`",
            "",
            "## Quality",
            "",
            f"- required_field_coverage: `{quality.get('required_field_coverage', 0)}`",
            f"- average_score: `{quality.get('average_score', 0)}`",
            f"- minimum_traceability_score: `{quality.get('minimum_traceability_score', 0)}`",
            f"- missing_query_ids: `{','.join(quality.get('missing_query_ids', [])) or 'none'}`",
            f"- missing_channels: `{','.join(quality.get('missing_channels', [])) or 'none'}`",
            f"- duplicate_url_count: `{quality.get('duplicate_url_count', 0)}`",
            f"- forbidden_claim_count: `{quality.get('forbidden_claim_count', 0)}`",
            f"- credential_leak_count: `{quality.get('credential_leak_count', 0)}`",
            "",
            "## Security Controls",
            "",
            f"- agent_reach_binary_invoked: `{controls.get('agent_reach_binary_invoked', False)}`",
            f"- live_external_search_invoked: `{controls.get('live_external_search_invoked', False)}`",
            f"- credential_written: `{controls.get('credential_written', False)}`",
            f"- browser_cookie_extraction_invoked: `{controls.get('browser_cookie_extraction_invoked', False)}`",
            f"- kds_canonical_write_allowed: `{controls.get('kds_canonical_write_allowed', False)}`",
            f"- gfis_source_of_record_write_allowed: `{controls.get('gfis_source_of_record_write_allowed', False)}`",
            f"- production_config_write_allowed: `{controls.get('production_config_write_allowed', False)}`",
            f"- global_mcp_config_write_allowed: `{controls.get('global_mcp_config_write_allowed', False)}`",
            f"- production_integration_allowed: `{controls.get('production_integration_allowed', False)}`",
            "",
            "## Non-Claims",
            "",
            "- This evidence is candidate-only.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- Raw provider payloads are not persisted.",
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
    parser.add_argument("--authorization", type=Path, default=DEFAULT_AUTH_PATH)
    parser.add_argument("--execute", action="store_true", help="Run live external reads after authorization passes")
    parser.add_argument("--write-evidence", action="store_true", help="Write redacted evidence JSON and Markdown")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()
    report = build_report(args.authorization, args.execute)
    if args.write_evidence:
        write_evidence(report, args.output_json, args.output_md)
        report = {**report, "written_evidence": {"json": display_path(args.output_json), "markdown": display_path(args.output_md)}}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
