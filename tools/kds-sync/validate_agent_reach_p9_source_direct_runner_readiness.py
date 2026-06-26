#!/usr/bin/env python3
"""Validate Agent-Reach P9S source-direct runner readiness without live fetch."""

from __future__ import annotations

import importlib.util
import http.client
import json
import tempfile
import urllib.error
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_p9_source_direct_hit_rate.py"
PRECHECK = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json"
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-runner-readiness-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-runner-readiness-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_runner_readiness=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p9_source_direct_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_positive_auth(request: dict[str, Any]) -> dict[str, Any]:
    fields = request["required_authorization_fields"]
    return {
        **fields,
        "authorized_by": "readiness-validator",
        "authorized_at": "2026-06-26T00:00:00+08:00",
        "expires_at": "2027-06-26T23:59:59+08:00",
    }


def validate_report_shape(report: dict[str, Any], expected_status: str, live_expected: bool) -> None:
    if report.get("status") != expected_status:
        fail(f"status_mismatch:{report.get('status')}")
    controls = report.get("security_controls", {})
    if controls.get("live_external_fetch_invoked") is not live_expected:
        fail("live_fetch_flag_mismatch")
    if controls.get("credential_written") is not False:
        fail("credential_written_not_false")
    if controls.get("browser_cookie_extraction_invoked") is not False:
        fail("cookie_extraction_not_false")
    if report.get("hit_rate_report", {}).get("candidate_count") != 0:
        fail("candidate_count_not_zero_in_readiness")
    if report.get("hit_rate_report", {}).get("fetch_error_count") != 0:
        fail("fetch_error_count_not_zero_in_readiness")


def build_report() -> dict[str, Any]:
    precheck = load_json(PRECHECK)
    request = load_json(REQUEST)
    runner = load_runner()
    if precheck.get("status") != "p9_source_direct_hit_rate_precheck_ready":
        fail("precheck_status_mismatch")
    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("authorization_request_status_mismatch")
    missing_report = runner.build_report(ROOT / "fixtures/agent-reach/__missing_p9s_auth__.json", execute=False)
    validate_report_shape(missing_report, "blocked_pending_p9_source_direct_authorization", False)
    with tempfile.TemporaryDirectory(prefix="agent-reach-p9s-readiness-") as tmp_dir:
        auth_path = Path(tmp_dir) / "auth.json"
        auth_path.write_text(json.dumps(build_positive_auth(request), ensure_ascii=False, indent=2), encoding="utf-8")
        authorized_report = runner.build_report(auth_path, execute=False)
    validate_report_shape(authorized_report, "authorized_execution_not_requested", False)
    title, body = runner.strip_html("<html><title>无废城市</title><body>工业固废 综合利用</body></html>".encode("utf-8"))
    if "无废城市" not in title or "工业固废" not in body:
        fail("html_strip_self_test_failed")
    gb18030_payload = "<html><title>磷石膏</title><body>无废城市 工业固废 综合利用</body></html>".encode("gb18030")
    gb18030_text = runner.decode_payload(gb18030_payload, "gb18030")
    gb_title, gb_body = runner.strip_html(gb18030_text)
    if "磷石膏" not in gb_title or "无废城市" not in gb_body:
        fail("gb18030_decode_self_test_failed")
    discovered = runner.discover_urls(
        {"domain": "mee.gov.cn", "topics": ["phosphogypsum", "zero_waste_city"]},
        "https://www.mee.gov.cn/",
        """
        <html>
          <a href="/home/ztbd/2020/wfcsjssdgz/">无废城市</a>
          <a href="https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/gthw/gtfwwrkzbz/202506/t20250610_1121013.shtml">磷石膏</a>
          <a href="https://example.com/token=abc">跨域</a>
        </html>
        """,
        limit=5,
    )
    if "https://www.mee.gov.cn/home/ztbd/2020/wfcsjssdgz/" not in discovered:
        fail("same_domain_html_discovery_missing")
    if any("example.com" in url for url in discovered):
        fail("cross_domain_discovery_not_rejected")
    sitemap_discovered = runner.discover_urls(
        {"domain": "miit.gov.cn", "topics": ["industrial_solid_waste"]},
        "https://www.miit.gov.cn/sitemap.xml",
        "<urlset><url><loc>https://www.miit.gov.cn/jgsj/jns/wjfb/art/solid-waste.html</loc></url></urlset>",
        limit=5,
    )
    if "https://www.miit.gov.cn/jgsj/jns/wjfb/art/solid-waste.html" not in sitemap_discovered:
        fail("sitemap_discovery_missing")
    asset_filtered = runner.discover_urls(
        {"domain": "greenscs.com", "topics": ["green_supply_chain"]},
        "https://www.greenscs.com/",
        """
        <html>
          <a href="/favicon.ico">favicon</a>
          <a href="/static/app.css">css</a>
          <a href="/green-supply-chain.html">绿色供应链</a>
        </html>
        """,
        limit=5,
    )
    if any(url.endswith((".ico", ".css")) for url in asset_filtered):
        fail("static_asset_discovery_not_filtered")
    if "https://www.greenscs.com/green-supply-chain.html" not in asset_filtered:
        fail("static_asset_filter_removed_valid_page")
    if runner.reject_final_url({"domain": "mee.gov.cn"}, "https://example.com/login") != "final_url_domain_mismatch:example.com":
        fail("cross_domain_redirect_rejection_missing")
    if runner.reject_final_url({"domain": "mee.gov.cn"}, "https://www.mee.gov.cn/user/login") != "final_url_login_path":
        fail("login_path_rejection_missing")
    if runner.reject_login_like_content("登录", "password captcha") != "login_like_content":
        fail("login_content_rejection_missing")
    if "text/html" not in runner.ALLOWED_CONTENT_TYPE_PREFIXES or "application/rss+xml" not in runner.ALLOWED_CONTENT_TYPE_PREFIXES:
        fail("allowed_content_type_prefixes_missing")
    if any(prefix.startswith("application/pdf") for prefix in runner.ALLOWED_CONTENT_TYPE_PREFIXES):
        fail("binary_content_type_allowed")
    original_fetch_url = runner.fetch_url
    retry_state = {"count": 0}

    def flaky_fetch(_url: str):
        retry_state["count"] += 1
        if retry_state["count"] == 1:
            raise urllib.error.URLError("temporary offline fixture")
        return 200, "retry", "绿色供应链", "<html>绿色供应链</html>", "https://www.mee.gov.cn/", "text/html"

    runner.fetch_url = flaky_fetch
    try:
        *_result, retry_count = runner.fetch_url_with_retry("https://www.mee.gov.cn/")
    finally:
        runner.fetch_url = original_fetch_url
    if retry_count != 1 or retry_state["count"] != 2:
        fail("transient_retry_self_test_failed")
    original_urlopen = runner.urllib.request.urlopen

    class PartialResponse:
        status = 200
        headers = type(
            "Headers",
            (),
            {
                "get_content_type": lambda self: "text/html",
                "get_content_charset": lambda self: "utf-8",
            },
        )()

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self, _limit: int):
            raise http.client.IncompleteRead("<html><title>工业固废</title><body>固体废物 资源综合利用</body></html>".encode("utf-8"))

        def geturl(self):
            return "https://www.miit.gov.cn/solid-waste.html"

    runner.urllib.request.urlopen = lambda *_args, **_kwargs: PartialResponse()
    try:
        _status, partial_title, partial_body, _raw, _final_url, _content_type = runner.fetch_url("https://www.miit.gov.cn/solid-waste.html")
    finally:
        runner.urllib.request.urlopen = original_urlopen
    if "工业固废" not in partial_title or "资源综合利用" not in partial_body:
        fail("incomplete_read_partial_not_parsed")
    return {
        "id": "agent-reach-p9-source-direct-runner-readiness-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_runner_readiness_ready",
        "current_admission": "limited_candidate_only",
        "runner": "tools/kds-sync/run_agent_reach_p9_source_direct_hit_rate.py",
        "precheck_fixture": "fixtures/agent-reach/p9-source-direct-hit-rate-precheck-20260626.json",
        "authorization_request": "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json",
        "missing_authorization_status": missing_report["status"],
        "authorized_no_execute_status": authorized_report["status"],
        "planned_target_count": authorized_report["planned_target_count"],
        "planned_entrypoint_count": authorized_report["planned_entrypoint_count"],
        "source_direct_discovery_enabled": True,
        "source_direct_charset_fallback_enabled": True,
        "source_direct_redirect_guard_enabled": True,
        "source_direct_login_guard_enabled": True,
        "source_direct_content_type_guard_enabled": True,
        "source_direct_static_asset_filter_enabled": True,
        "source_direct_incomplete_read_partial_enabled": True,
        "source_direct_transient_retry_enabled": True,
        "source_direct_max_transient_retry_count": runner.MAX_TRANSIENT_RETRY_COUNT,
        "source_direct_max_pages_per_entrypoint": 5,
        "live_external_fetch_invoked": False,
        "non_claims": [
            "runner_readiness_only",
            "not_live_fetch_invoked",
            "not_source_of_record",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-RUNNER-READINESS-20260626",
            "title: Agent-Reach P9S Source Direct Runner Readiness 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-runner-readiness-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-runner-readiness-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Runner Readiness 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- runner: `{report['runner']}`",
            f"- missing_authorization_status: `{report['missing_authorization_status']}`",
            f"- authorized_no_execute_status: `{report['authorized_no_execute_status']}`",
            f"- planned_target_count: `{report['planned_target_count']}`",
            f"- planned_entrypoint_count: `{report['planned_entrypoint_count']}`",
            f"- source_direct_discovery_enabled: `{report['source_direct_discovery_enabled']}`",
            f"- source_direct_charset_fallback_enabled: `{report['source_direct_charset_fallback_enabled']}`",
            f"- source_direct_redirect_guard_enabled: `{report['source_direct_redirect_guard_enabled']}`",
            f"- source_direct_login_guard_enabled: `{report['source_direct_login_guard_enabled']}`",
            f"- source_direct_content_type_guard_enabled: `{report['source_direct_content_type_guard_enabled']}`",
            f"- source_direct_transient_retry_enabled: `{report['source_direct_transient_retry_enabled']}`",
            f"- source_direct_max_transient_retry_count: `{report['source_direct_max_transient_retry_count']}`",
            f"- source_direct_max_pages_per_entrypoint: `{report['source_direct_max_pages_per_entrypoint']}`",
            f"- live_external_fetch_invoked: `{report['live_external_fetch_invoked']}`",
            "",
            "## 边界",
            "",
            "- 本证据只验证 P9S source-direct runner readiness。",
            "- 本证据不执行目标站点直连读取。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_runner_readiness=pass "
        f"status={report['status']} targets={report['planned_target_count']} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
