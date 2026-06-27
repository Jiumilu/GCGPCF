#!/usr/bin/env python3
"""Run Agent-Reach P9S source-direct hit-rate evaluation behind an authorization gate."""

from __future__ import annotations

import argparse
import hashlib
import html
import http.client
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[2]
PRECHECK = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json"
DEFAULT_AUTH = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json"
DEFAULT_OUTPUT_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.json"
DEFAULT_OUTPUT_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.md"

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
TOPIC_KEYWORDS = {
    "green_supply_chain": ["绿色供应链", "green supply chain", "供应商", "ESG", "碳足迹", "scope 3", "供应链"],
    "phosphogypsum": ["磷石膏", "phosphogypsum", "综合利用", "污染控制", "无害化", "贮存"],
    "industrial_solid_waste": ["工业固废", "工业固体废物", "固体废物", "固废", "大宗固废", "大宗固体废弃物", "资源综合利用", "循环经济", "solid waste"],
    "zero_waste_city": ["无废城市", "zero-waste", "指标体系", "试点", "工业固废综合利用率"],
}
LOGIN_PATH_PATTERN = re.compile(r"(?i)(/login|/signin|/auth|/oauth|/sso|/passport|/user/login)")
LOGIN_CONTENT_PATTERN = re.compile(r"(?i)(password|登录|登陆|sign in|oauth|sso|captcha|验证码)")
ALLOWED_CONTENT_TYPE_PREFIXES = (
    "text/html",
    "text/plain",
    "text/xml",
    "application/xml",
    "application/rss+xml",
    "application/atom+xml",
    "application/json",
)
TRANSIENT_FETCH_ERROR_TYPES = (urllib.error.URLError, TimeoutError, ConnectionError)
MAX_TRANSIENT_RETRY_COUNT = 1
SKIPPED_DISCOVERY_EXTENSIONS = (".css", ".js", ".ico", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".woff", ".woff2", ".ttf", ".map")


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


def redact_text(value: str, limit: int = 360) -> str:
    text = re.sub(r"(?i)(token|cookie|authorization|secret|password)=([^&\s]+)", r"\1=<redacted>", value)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def decode_payload(payload: bytes, charset: str | None = None) -> str:
    encodings = [charset] if charset else []
    encodings.extend(["utf-8", "gb18030"])
    seen: set[str] = set()
    for encoding in encodings:
        if not encoding or encoding.lower() in seen:
            continue
        seen.add(encoding.lower())
        try:
            return payload.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return payload.decode("utf-8", errors="ignore")


def strip_html(payload: bytes | str) -> tuple[str, str]:
    text = decode_payload(payload) if isinstance(payload, bytes) else payload
    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    title = html.unescape(re.sub(r"<[^>]+>", " ", title_match.group(1))).strip() if title_match else ""
    body = re.sub(r"(?is)<(script|style).*?</\\1>", " ", text)
    body = html.unescape(re.sub(r"<[^>]+>", " ", body))
    body = re.sub(r"\s+", " ", body).strip()
    return title[:160], body[:1200]


def topic_terms(target: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    for topic_id in target.get("topics", []):
        terms.extend(TOPIC_KEYWORDS.get(topic_id, []))
    return terms


def same_target_domain(target: dict[str, Any], url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.netloc) and parsed.netloc.endswith(target["domain"])


def is_static_asset_url(url: str) -> bool:
    return urlparse(url).path.lower().endswith(SKIPPED_DISCOVERY_EXTENSIONS)


def discover_urls(target: dict[str, Any], base_url: str, raw_text: str, limit: int = 5) -> list[str]:
    urls = [base_url]
    seen = {base_url}
    terms = [term.lower() for term in topic_terms(target)]
    link_candidates: list[tuple[int, str]] = []
    for pattern in [
        r"<loc>\s*([^<]+)\s*</loc>",
        r"<link>\s*([^<]+)\s*</link>",
        r"""href=["']([^"']+)["']""",
    ]:
        for match in re.finditer(pattern, raw_text, re.IGNORECASE):
            url = html.unescape(match.group(1).strip())
            absolute = urljoin(base_url, url)
            if absolute in seen or not same_target_domain(target, absolute) or is_static_asset_url(absolute):
                continue
            folded = absolute.lower()
            score = sum(1 for term in terms if term.lower() in folded)
            link_candidates.append((score, absolute))
            seen.add(absolute)
    for _score, url in sorted(link_candidates, key=lambda item: (-item[0], item[1])):
        urls.append(url)
        if len(urls) >= limit:
            break
    return urls


def validate_target_url(target: dict[str, Any], url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return "url_not_https"
    if not parsed.netloc.endswith(target["domain"]):
        return f"url_domain_mismatch:{parsed.netloc}"
    return None


def fetch_url(url: str) -> tuple[int | None, str, str, str, str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "Agent-Reach-P9S-candidate-only/1.0"})
    with urllib.request.urlopen(request, timeout=12) as response:
        content_type = response.headers.get_content_type()
        if not any(content_type.lower().startswith(prefix) for prefix in ALLOWED_CONTENT_TYPE_PREFIXES):
            raise ValueError(f"content_type_not_allowed:{content_type}")
        try:
            payload = response.read(128_000)
        except http.client.IncompleteRead as exc:
            payload = exc.partial
        charset = response.headers.get_content_charset()
        raw_text = decode_payload(payload, charset)
        title, body = strip_html(raw_text)
        return response.status, title, body, raw_text, response.geturl(), content_type


def fetch_url_with_retry(url: str) -> tuple[int | None, str, str, str, str, str, int]:
    attempts = 0
    while True:
        try:
            result = fetch_url(url)
            return (*result, attempts)
        except TRANSIENT_FETCH_ERROR_TYPES:
            if attempts >= MAX_TRANSIENT_RETRY_COUNT:
                raise
            attempts += 1


def reject_final_url(target: dict[str, Any], final_url: str) -> str | None:
    reason = validate_target_url(target, final_url)
    if reason:
        return f"final_{reason}"
    if LOGIN_PATH_PATTERN.search(urlparse(final_url).path):
        return "final_url_login_path"
    return None


def reject_login_like_content(title: str, body: str) -> str | None:
    text = f"{title} {body}"[:1200]
    if LOGIN_CONTENT_PATTERN.search(text) and not any(keyword in text for keyword in ["绿色供应链", "磷石膏", "工业固废", "无废城市"]):
        return "login_like_content"
    return None


def reject_empty_content(title: str, body: str) -> str | None:
    if not title.strip() and not body.strip():
        return "empty_text_content"
    return None


def topic_keyword_hits(topic_id: str, text: str) -> list[str]:
    folded = text.lower()
    return [keyword for keyword in TOPIC_KEYWORDS.get(topic_id, []) if keyword.lower() in folded]


def build_candidate(target: dict[str, Any], entrypoint: dict[str, Any], requested_url: str, final_url: str, status_code: int | None, title: str, body: str, discovery_rank: int, content_type: str) -> dict[str, Any]:
    text = f"{title} {body}"
    topic_hits = {topic_id: topic_keyword_hits(topic_id, text) for topic_id in target["topics"]}
    hit_count = sum(len(hits) for hits in topic_hits.values())
    authority_score = 0.92 if target["priority"] == "P0" else 0.82
    relevance_score = min(0.95, round(0.55 + min(hit_count, 5) * 0.08, 4))
    freshness_score = 0.7
    traceability_score = 1.0
    priority_boost = 0.08 if target["priority"] == "P0" else 0.03
    score = min(0.99, round((relevance_score * 0.45) + (authority_score * 0.35) + (freshness_score * 0.1) + (traceability_score * 0.1) + priority_boost, 4))
    candidate_id = f"p9s-{target['target_id']}-{hashlib.sha256(final_url.encode('utf-8')).hexdigest()[:10]}"
    return {
        "candidate_id": candidate_id,
        "target_id": target["target_id"],
        "source_domain": target["domain"],
        "priority": target["priority"],
        "topics": target["topics"],
        "business_fields": target["business_fields"],
        "entrypoint_method": entrypoint["method"],
        "discovery_rank": discovery_rank,
        "requested_url": requested_url,
        "url": final_url,
        "final_url": final_url,
        "content_type": content_type,
        "http_status": status_code,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "title": redact_text(title, 180),
        "snippet_redacted": redact_text(body, 420),
        "topic_keyword_hits": topic_hits,
        "relevance_score": relevance_score,
        "authority_score": authority_score,
        "freshness_score": freshness_score,
        "traceability_score": traceability_score,
        "overall_score": score,
        "non_claims": ["candidate_only", "not_kds_canonical_written", "not_gfis_source_of_record_written"],
        "candidate_only": True,
    }


def validate_authorization(auth_path: Path, precheck: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any] | None]:
    if not auth_path.exists():
        return False, ["authorization_file_missing"], None
    auth = load_json(auth_path)
    missing = sorted(REQUIRED_AUTH_FIELDS - set(auth))
    if missing:
        return False, [f"authorization_missing_fields:{','.join(missing)}"], auth
    reasons: list[str] = []
    targets = precheck.get("source_direct_targets", [])
    if auth.get("authorization_id") != "agent-reach-p9-source-direct-hit-rate-live-run":
        reasons.append("authorization_id_mismatch")
    if auth.get("authorization_status") != "approved_for_p9_source_direct_hit_rate_live_run":
        reasons.append("authorization_status_not_approved")
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
    if auth.get("max_targets") != len(targets):
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
    return not reasons, sorted(set(reasons)), auth


def execute_live(precheck: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for target in precheck.get("source_direct_targets", []):
        for entrypoint in target.get("entrypoints", [])[:3]:
            if entrypoint.get("method") not in ALLOWED_METHODS:
                errors.append({"target_id": target["target_id"], "discovery_rank": 0, "critical": True, "error_type": "method_not_allowed", "message": entrypoint.get("method", "")})
                continue
            entry_url = entrypoint["url"]
            reason = validate_target_url(target, entry_url)
            if reason:
                errors.append({"target_id": target["target_id"], "url": entry_url, "discovery_rank": 0, "critical": True, "error_type": "target_url_rejected", "message": reason})
                continue
            try:
                status_code, title, body, raw_text, final_url, content_type, retry_count = fetch_url_with_retry(entry_url)
                reason = reject_final_url(target, final_url) or reject_login_like_content(title, body) or reject_empty_content(title, body)
                if reason:
                    errors.append({"target_id": target["target_id"], "url": entry_url, "discovery_rank": 0, "critical": True, "error_type": "target_response_rejected", "message": reason})
                    continue
                discovered_urls = discover_urls(target, entry_url, raw_text, limit=5)
                candidates.append(build_candidate(target, entrypoint, entry_url, final_url, status_code, title, body, 0, content_type))
                candidates[-1]["retry_count"] = retry_count
            except urllib.error.HTTPError as exc:
                errors.append({"target_id": target["target_id"], "url": entry_url, "discovery_rank": 0, "critical": True, "error_type": "http_error", "message": redact_text(f"{exc.code} {exc.reason}")})
                continue
            except Exception as exc:
                errors.append({"target_id": target["target_id"], "url": entry_url, "discovery_rank": 0, "critical": True, "error_type": exc.__class__.__name__, "message": redact_text(str(exc))})
                continue
            for discovery_rank, url in enumerate(discovered_urls[1:], start=1):
                try:
                    status_code, title, body, _raw_text, final_url, content_type, retry_count = fetch_url_with_retry(url)
                    reason = reject_final_url(target, final_url) or reject_login_like_content(title, body) or reject_empty_content(title, body)
                    if reason:
                        errors.append({"target_id": target["target_id"], "url": url, "discovery_rank": discovery_rank, "critical": False, "error_type": "target_response_rejected", "message": reason})
                        continue
                    candidates.append(build_candidate(target, entrypoint, url, final_url, status_code, title, body, discovery_rank, content_type))
                    candidates[-1]["retry_count"] = retry_count
                except urllib.error.HTTPError as exc:
                    errors.append({"target_id": target["target_id"], "url": url, "discovery_rank": discovery_rank, "critical": False, "error_type": "http_error", "message": redact_text(f"{exc.code} {exc.reason}")})
                except Exception as exc:
                    errors.append({"target_id": target["target_id"], "url": url, "discovery_rank": discovery_rank, "critical": False, "error_type": exc.__class__.__name__, "message": redact_text(str(exc))})
    return candidates, errors


def hit_rate_report(precheck: dict[str, Any], candidates: list[dict[str, Any]], fetch_errors: list[dict[str, Any]]) -> dict[str, Any]:
    topics = sorted(precheck.get("coverage_requirements", {}).get("required_topics", []))
    topic_reports: dict[str, Any] = {}
    critical_errors = [error for error in fetch_errors if error.get("critical") is not False]
    for topic_id in topics:
        topic_targets = [target for target in precheck.get("source_direct_targets", []) if topic_id in target.get("topics", [])]
        topic_candidates = [candidate for candidate in candidates if topic_id in candidate.get("topics", [])]
        p0_hits = {candidate["source_domain"] for candidate in topic_candidates if candidate.get("priority") == "P0"}
        total_hits = {candidate["source_domain"] for candidate in topic_candidates}
        keyword_hit_candidates = [
            candidate["target_id"]
            for candidate in topic_candidates
            if candidate.get("topic_keyword_hits", {}).get(topic_id)
        ]
        topic_reports[topic_id] = {
            "target_count": len(topic_targets),
            "candidate_count": len(topic_candidates),
            "p0_domain_hit_count": len(p0_hits),
            "total_domain_hit_count": len(total_hits),
            "keyword_hit_candidate_count": len(set(keyword_hit_candidates)),
            "target_coverage": round(len({candidate["target_id"] for candidate in topic_candidates}) / len(topic_targets), 4) if topic_targets else 0,
            "threshold_pass": bool(p0_hits) and bool(total_hits) and bool(keyword_hit_candidates),
        }
    return {
        "candidate_count": len(candidates),
        "fetch_error_count": len(fetch_errors),
        "critical_fetch_error_count": len(critical_errors),
        "noncritical_fetch_error_count": len(fetch_errors) - len(critical_errors),
        "target_availability_warning_count": len(critical_errors),
        "topic_reports": topic_reports,
        "topic_coverage": round(sum(1 for item in topic_reports.values() if item["threshold_pass"]) / len(topic_reports), 4) if topic_reports else 0,
        "threshold_pass": bool(topic_reports) and all(item["threshold_pass"] for item in topic_reports.values()),
    }


def build_report(auth_path: Path, execute: bool) -> dict[str, Any]:
    precheck = load_json(PRECHECK)
    authorized, reasons, _auth = validate_authorization(auth_path, precheck)
    base = {
        "id": "agent-reach-p9-source-direct-hit-rate-live-run-20260626",
        "date": "2026-06-26",
        "current_admission": "limited_candidate_only",
        "authorization_valid": authorized,
        "authorization_reasons": reasons,
        "authorization_path": display_path(auth_path),
        "execution_requested": execute,
        "planned_target_count": len(precheck.get("source_direct_targets", [])),
        "planned_entrypoint_count": sum(len(target.get("entrypoints", [])) for target in precheck.get("source_direct_targets", [])),
        "security_controls": {
            "live_external_fetch_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "non_claims": [
            "candidate_only",
            "not_source_of_record",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }
    if not authorized:
        return {**base, "status": "blocked_pending_p9_source_direct_authorization", "candidates": [], "fetch_errors": [], "hit_rate_report": hit_rate_report(precheck, [], [])}
    if not execute:
        return {**base, "status": "authorized_execution_not_requested", "candidates": [], "fetch_errors": [], "hit_rate_report": hit_rate_report(precheck, [], [])}
    candidates, errors = execute_live(precheck)
    hit_rate = hit_rate_report(precheck, candidates, errors)
    return {
        **base,
        "status": "p9_source_direct_hit_rate_completed" if hit_rate["threshold_pass"] else "p9_source_direct_hit_rate_rework_required",
        "candidates": candidates,
        "fetch_errors": errors,
        "hit_rate_report": hit_rate,
        "security_controls": {**base["security_controls"], "live_external_fetch_invoked": True},
    }


def render_markdown(report: dict[str, Any]) -> str:
    hit_rate = report.get("hit_rate_report", {})
    controls = report.get("security_controls", {})
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-HIT-RATE-LIVE-RUN-20260626",
            "title: Agent-Reach P9S Source Direct 命中率运行证据 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct 命中率运行证据 2026-06-26",
            "",
            f"- status: `{report.get('status')}`",
            f"- authorization_valid: `{report.get('authorization_valid')}`",
            f"- execution_requested: `{report.get('execution_requested')}`",
            f"- live_external_fetch_invoked: `{controls.get('live_external_fetch_invoked')}`",
            f"- planned_target_count: `{report.get('planned_target_count')}`",
            f"- candidate_count: `{hit_rate.get('candidate_count', 0)}`",
            f"- fetch_error_count: `{hit_rate.get('fetch_error_count', 0)}`",
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
